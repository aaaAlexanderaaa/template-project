# Role: Zero-dependency local HTTP service, CSRF gate, review/test triggers, and standalone HTML exporter.
# Out of scope: AST import resolution (owned by import_scanner.py) and raw TOML string escaping.
# Anchors: spec=perspective.server, ADR-002, SRC-014, SRC-015, SRC-016, SRC-019

from __future__ import annotations

import html as html_mod
import json
import mimetypes
import re
import secrets
import shlex
import subprocess
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlsplit

from .briefing_pack import serialize_perspective_payload
from .cli_format import fmt_stage
from .context_pack import build_context_pack
from .git_telemetry import compare_git_refs, get_head_sha, get_working_tree_digest
from .loader import load_project_graph, save_runtime_state
from .toml_writer import append_verbatim_source, archive_completed_milestone, mutate_task_in_work_toml

WEB_DIR = Path(__file__).resolve().parent / "web"
ALLOWED_LOCAL_HOSTS = {"127.0.0.1", "localhost", "::1"}
STYLE_FILES = ("tokens.css", "layout.css", "components.css", "tables-and-inline.css", "prose-and-svg.css")
JS_BUNDLE_ORDER = (
    "i18n.js",
    "markdown.js",
    "diagrams.js",
    "charts.js",
    "drawer.js",
    "roadmap_panels.js",
    "views.js",
    "app.js",
)


def mark_review_anchor(root: Path) -> dict[str, Any]:
    sha = get_head_sha(root)
    wt_digest = get_working_tree_digest(root)
    policy_path = root / "docs-policy.toml"
    if not wt_digest and sha and policy_path.is_file():
        raw = policy_path.read_text(encoding="utf-8")
        if re.search(r"^\s*review_anchor_sha\s*=", raw, flags=re.MULTILINE):
            updated = re.sub(
                r'^(\s*review_anchor_sha\s*=\s*)"[^"]*"',
                rf'\1"{sha}"',
                raw,
                count=1,
                flags=re.MULTILINE,
            )
        elif "[collaboration]" in raw:
            updated = raw.replace("[collaboration]\n", f'[collaboration]\nreview_anchor_sha = "{sha}"\n', 1)
        else:
            updated = raw.rstrip() + f'\n\n[collaboration]\nreview_anchor_sha = "{sha}"\n'
        if updated != raw:
            policy_path.write_text(updated, encoding="utf-8")
    return save_runtime_state(root, {"last_review_sha": sha, "last_review_wt_digest": wt_digest})


def run_configured_tests(root: Path) -> dict[str, Any]:
    graph = load_project_graph(root)
    cmd_str = str(graph.policy.get("commands", {}).get("test", "python3 -m unittest discover -s tests -p 'test_*.py'"))
    argv = shlex.split(cmd_str)
    if not argv:
        return {"exit_code": 1, "head_sha": get_head_sha(root), "output_tail": "Empty test command", "command": ""}
    proc = subprocess.run(argv, cwd=root, shell=False, capture_output=True, text=True, timeout=60, check=False)
    tail = "\n".join((proc.stdout + "\n" + proc.stderr).strip().splitlines()[-15:])
    record = {"exit_code": proc.returncode, "head_sha": get_head_sha(root), "output_tail": tail, "command": cmd_str}
    save_runtime_state(root, {"last_test_run": record})
    return record


def _render_fallback_overview_html(payload: dict[str, Any]) -> str:
    """Render a self-contained static HTML overview when bundled web/ assets are omitted."""
    proj = payload["project"]
    lang = str(proj.get("language", "en")).lower()
    is_zh = lang == "zh"
    esc = html_mod.escape
    data_json = json.dumps(payload, ensure_ascii=False).replace("</", "<\\/")

    blocked_items = "".join(
        f"<li><strong>{esc(b['task_id'])}</strong> [{esc(b['domain_name'])}]: {esc(b['blocker_question'])}"
        + (
            "<ul>" + "".join(f"<li>{esc(opt)}</li>" for opt in b.get("blocker_options", [])) + "</ul>"
            if b.get("blocker_options")
            else ""
        )
        + (f"<div><small>{esc(', '.join(b.get('design_docs', [])))}</small></div>" if b.get("design_docs") else "")
        + "</li>"
        for b in payload.get("blocked_inbox", [])
    )
    domain_items = "".join(
        f"<li><strong>{esc(d['name'])}</strong> ({esc(fmt_stage(d['stage'], lang))}) — "
        f"{'代码' if is_zh else 'code'} {int(d.get('loc', 0))}, "
        f"{'文档' if is_zh else 'docs'} {int(d.get('doc_count', 0))} ({int(d.get('doc_loc', 0))})"
        + (f"<br><small>{esc(', '.join(m['name'] for m in d.get('now_milestones', [])))}</small>" if d.get("now_milestones") else "")
        + "</li>"
        for d in payload.get("domains", [])
    )
    dir_items = "".join(
        f"<li><code>{esc(de['path'])}</code> ({esc(de['label_zh'] if is_zh else de['label_en'])}) — "
        f"{de['file_count']} / {de['doc_count']}: {esc(de['summary_zh'] if is_zh else de['summary_en'])}</li>"
        for de in payload.get("directory_map", [])
    )
    return (
        "<!doctype html><html><head><meta charset='utf-8'>"
        f"<title>{esc(proj['name'])} — {'项目总览' if is_zh else 'Project Overview'}</title>"
        "<style>body{font-family:system-ui,sans-serif;max-width:860px;margin:40px auto;padding:0 20px;line-height:1.6;color:#1f2937}"
        "h1,h2{color:#111827}ul{padding-left:20px}code{background:#f3f4f6;padding:1px 5px;border-radius:4px}</style></head><body>"
        f"<h1>{esc(proj['name'])} ({esc(fmt_stage(proj['stage'], lang))})</h1>"
        f"<p>{esc(proj.get('one_liner', ''))}</p>"
        f"<p>{'代码' if is_zh else 'Code'}: {int(proj.get('total_loc', 0))} | "
        f"{'文档' if is_zh else 'Docs'}: {int(proj.get('doc_count', 0))} ({int(proj.get('doc_loc', 0))}) | "
        f"{'业务域' if is_zh else 'Domains'}: {int(proj.get('domain_count', 0))}</p>"
        + (f"<h2>{'待负责人拍板决定' if is_zh else 'Needs Owner Decision'}</h2><ul>{blocked_items}</ul>" if blocked_items else "")
        + f"<h2>{'各业务域与进度' if is_zh else 'Domains & Progress'}</h2><ul>{domain_items}</ul>"
        + f"<h2>{'目录结构总览' if is_zh else 'Directory Overview'}</h2><ul>{dir_items}</ul>"
        + f"<script>window.__PERSPECTIVE_DATA__ = {data_json};</script></body></html>"
    )


def export_standalone_html(root: Path, output_path: Path) -> Path:
    graph = load_project_graph(root)
    payload = serialize_perspective_payload(graph)
    if not (WEB_DIR / "index.html").is_file():
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(_render_fallback_overview_html(payload), encoding="utf-8")
        return output_path

    css = "\n".join(
        (WEB_DIR / "styles" / name).read_text(encoding="utf-8")
        for name in STYLE_FILES
        if (WEB_DIR / "styles" / name).is_file()
    )
    js_chunks: list[str] = ["(() => {"]
    for name in JS_BUNDLE_ORDER:
        js_path = WEB_DIR / "js" / name
        if not js_path.is_file():
            continue
        cleaned_lines: list[str] = []
        for ln in js_path.read_text(encoding="utf-8").splitlines():
            if ln.startswith("import "):
                continue
            if ln.startswith("export function "):
                cleaned_lines.append("function " + ln[len("export function ") :])
            elif ln.startswith("export async function "):
                cleaned_lines.append("async function " + ln[len("export async function ") :])
            elif ln.startswith("export const "):
                cleaned_lines.append("const " + ln[len("export const ") :])
            else:
                cleaned_lines.append(ln)
        js_chunks.append("\n".join(cleaned_lines))
    js_chunks.append("})();")
    bundled_js = "\n".join(js_chunks)

    shell = (WEB_DIR / "index.html").read_text(encoding="utf-8")
    shell = re.sub(r'<link rel="stylesheet" href="/styles/[^"]+" />\s*', "", shell)
    shell = shell.replace("</head>", f"  <style>\n{css}\n  </style>\n</head>")
    data_json = json.dumps(payload, ensure_ascii=False).replace("</", "<\\/")
    shell = re.sub(
        r'<script[^>]*src="/js/[^"]+"[^>]*></script>\s*',
        "",
        shell,
    )
    shell = shell.replace(
        "</body>",
        f"<script>window.__PERSPECTIVE_DATA__ = {data_json};</script>\n<script>\n{bundled_js}\n</script>\n</body>",
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(shell, encoding="utf-8")
    return output_path


def _is_authorized_local_post(headers: Any, expected_token: str) -> tuple[bool, str]:
    sec_site = str(headers.get("Sec-Fetch-Site", "")).strip().lower()
    if sec_site == "cross-site":
        return False, "Blocked cross-site POST request."
    origin = str(headers.get("Origin", "")).strip()
    if origin:
        host = (urlsplit(origin).hostname or "").lower()
        if host not in ALLOWED_LOCAL_HOSTS:
            return False, f"Disallowed Origin `{origin}`."
    provided = str(headers.get("X-Project-Token", "")).strip()
    if not provided or not secrets.compare_digest(provided, expected_token):
        return False, "Missing or invalid X-Project-Token header."
    return True, ""


def create_perspective_server(root: Path, host: str = "127.0.0.1", port: int = 8765) -> ThreadingHTTPServer:
    root = root.resolve()
    csrf_token = secrets.token_hex(16)

    class PerspectiveHandler(BaseHTTPRequestHandler):
        def log_message(self, fmt: str, *args: Any) -> None:
            return

        def _send_json(self, obj: Any, status: int = 200) -> None:
            raw = json.dumps(obj, ensure_ascii=False).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)

        def _read_json_body(self) -> dict[str, Any]:
            try:
                length = int(self.headers.get("Content-Length", "0"))
            except ValueError as exc:
                raise ValueError("Invalid Content-Length header.") from exc
            if length <= 0:
                return {}
            data = json.loads(self.rfile.read(length).decode("utf-8"))
            if not isinstance(data, dict):
                raise ValueError("JSON body must be an object.")
            return data

        def do_GET(self) -> None:  # noqa: N802
            parsed = urlsplit(self.path)
            route = parsed.path
            qs = parse_qs(parsed.query)

            if route in ("/api/graph", "/api/overview"):
                graph = load_project_graph(root)
                self._send_json(serialize_perspective_payload(graph, csrf_token=csrf_token))
                return
            if route in ("/api/context", "/api/capsule"):
                q = (qs.get("q") or [""])[0]
                graph = load_project_graph(root)
                self._send_json(build_context_pack(graph, q))
                return
            if route == "/api/diff":
                base = (qs.get("base") or [""])[0]
                target = (qs.get("target") or ["HEAD"])[0]
                graph = load_project_graph(root)
                self._send_json(compare_git_refs(root, graph.modules, base, target))
                return

            rel = "index.html" if route in ("", "/") else route.lstrip("/")
            asset = (WEB_DIR / rel).resolve()
            if not asset.is_file() or not asset.is_relative_to(WEB_DIR.resolve()):
                if rel == "index.html":
                    notice = (
                        "<!doctype html><html><head><meta charset='utf-8'><title>Project Overview Service</title>"
                        "<style>body{font-family:system-ui,sans-serif;max-width:680px;margin:48px auto;line-height:1.6}</style>"
                        "</head><body>"
                        "<h1>Project Overview API Running</h1>"
                        "<p>Static web assets in <code>scripts/projectlib/web/</code> are omitted in this repository.</p>"
                        "<p>Use <code>python3 scripts/project.py status</code>, <code>context</code>, <code>trace</code>, "
                        "<code>check</code>, or query <code>/api/graph</code>, <code>/api/context?q=&lt;id&gt;</code>, or <code>/api/diff</code> directly.</p>"
                        "</body></html>"
                    ).encode("utf-8")
                    self.send_response(200)
                    self.send_header("Content-Type", "text/html; charset=utf-8")
                    self.send_header("Content-Length", str(len(notice)))
                    self.end_headers()
                    self.wfile.write(notice)
                    return
                self.send_error(404, "Not Found")
                return
            ctype, _ = mimetypes.guess_type(str(asset))
            raw = asset.read_bytes()
            if rel == "index.html":
                html = raw.decode("utf-8").replace(
                    "</head>",
                    f'  <meta name="project-csrf" content="{csrf_token}" />\n</head>',
                )
                raw = html.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", f"{ctype or 'application/octet-stream'}; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)

        def do_POST(self) -> None:  # noqa: N802
            ok_auth, reason = _is_authorized_local_post(self.headers, csrf_token)
            if not ok_auth:
                self._send_json({"ok": False, "error": reason}, status=403)
                return

            route = urlsplit(self.path).path
            try:
                body = self._read_json_body()
            except (ValueError, UnicodeDecodeError, json.JSONDecodeError):
                self._send_json({"ok": False, "error": "Invalid JSON body."}, status=400)
                return
            if route == "/api/tasks/approve":
                ok = mutate_task_in_work_toml(root, str(body.get("task_id", "")), human_check="approved")
                if not ok:
                    self._send_json({"ok": False, "error": "Task not found."}, status=404)
                    return
                self._send_json({"ok": True})
                return
            if route == "/api/tasks/resolve-blocker":
                res_text = str(body.get("resolution", "")).strip()
                if not res_text:
                    self._send_json({"ok": False, "error": "Resolution text is required."}, status=400)
                    return
                ok = mutate_task_in_work_toml(
                    root,
                    str(body.get("task_id", "")),
                    new_state="active",
                    resolution_quote=res_text,
                )
                if not ok:
                    self._send_json({"ok": False, "error": "Task not found."}, status=404)
                    return
                self._send_json({"ok": True})
                return
            if route == "/api/review/mark":
                st = mark_review_anchor(root)
                self._send_json({"ok": True, "state": st})
                return
            if route == "/api/tests/run":
                rec = run_configured_tests(root)
                self._send_json({"ok": rec["exit_code"] == 0, "result": rec})
                return
            self.send_error(404, "Unknown endpoint")

    srv = ThreadingHTTPServer((host, port), PerspectiveHandler)
    srv.daemon_threads = True
    srv.csrf_token = csrf_token  # type: ignore[attr-defined]
    return srv


__all__ = [
    "append_verbatim_source",
    "archive_completed_milestone",
    "create_perspective_server",
    "export_standalone_html",
    "mark_review_anchor",
    "mutate_task_in_work_toml",
    "run_configured_tests",
]
