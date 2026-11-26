# Role: End-to-end tests for project.py CLI subcommands, init/sync workflows, HTTP perspective routes, and TOML write-backs.
# Out of scope: Static validator boundary permutations (covered by test_ssot_and_check_docs.py) and web UI checks (test_web_workbench.py).
# Anchors: spec=perspective.context-pack, spec=perspective.server, SRC-014, SRC-015

from __future__ import annotations

import json
import re
import shutil
import socket
import subprocess
import sys
import tempfile
import threading
import tomllib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from projectlib.loader import load_project_graph  # noqa: E402
from projectlib.server import (  # noqa: E402
    archive_completed_milestone,
    create_perspective_server,
    export_standalone_html,
)


def _dispatch_http(
    httpd: object,
    method: str,
    path: str,
    payload: dict | None = None,
    headers: dict[str, str] | None = None,
    raw_body: bytes | None = None,
) -> tuple[int, str]:
    """Send a real HTTP/1.1 request over an in-process kernel socketpair (sandbox-safe)."""
    if raw_body is not None:
        body_bytes = raw_body
    elif payload is not None:
        body_bytes = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    else:
        body_bytes = b""
    req_lines = [
        f"{method} {path} HTTP/1.1",
        "Host: 127.0.0.1",
        "Connection: close",
    ]
    for hk, hv in (headers or {}).items():
        req_lines.append(f"{hk}: {hv}")
    if raw_body is not None or payload is not None:
        req_lines.append("Content-Type: application/json; charset=utf-8")
        req_lines.append(f"Content-Length: {len(body_bytes)}")
    raw_req = ("\r\n".join(req_lines) + "\r\n\r\n").encode("utf-8") + body_bytes

    client_sock, server_sock = socket.socketpair()

    def _run_server() -> None:
        try:
            handler_cls = httpd.RequestHandlerClass  # type: ignore[attr-defined]
            handler_cls(server_sock, ("127.0.0.1", 0), httpd)
        finally:
            server_sock.close()

    try:
        worker = threading.Thread(target=_run_server, daemon=True)
        worker.start()
        client_sock.sendall(raw_req)
        client_sock.shutdown(socket.SHUT_WR)
        chunks: list[bytes] = []
        while True:
            data = client_sock.recv(65536)
            if not data:
                break
            chunks.append(data)
        worker.join(timeout=5)
    finally:
        client_sock.close()

    raw_resp = b"".join(chunks)
    head_bytes, _, resp_body = raw_resp.partition(b"\r\n\r\n")
    status_line = head_bytes.splitlines()[0].decode("latin1")
    status_code = int(status_line.split()[1])
    return status_code, resp_body.decode("utf-8")


class ProjectCliAndServerTests(unittest.TestCase):
    def test_project_init_cli_context_trace_and_archive(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            proc = subprocess.run(
                [sys.executable, str(SCRIPTS_DIR / "project.py"), "--root", str(target), "init", "--name", "Demo Service"],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertTrue((target / "docs-policy.toml").is_file())
            self.assertTrue((target / "ARCHITECTURE.md").is_file())
            self.assertTrue((target / "AGENTS.md").is_file())
            self.assertTrue((target / "docs" / "README.md").is_file())
            self.assertTrue((target / "scripts" / "check_docs.py").is_file())

            chk_init = subprocess.run(
                [sys.executable, str(target / "scripts" / "check_docs.py"), "--strict"],
                cwd=target,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(chk_init.returncode, 0, chk_init.stdout + chk_init.stderr)

            # init must refuse to overwrite template-project itself
            guard_proc = subprocess.run(
                [sys.executable, str(SCRIPTS_DIR / "project.py"), "--root", str(ROOT), "init", "--name", "Overwrite"],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertNotEqual(guard_proc.returncode, 0)

            (target / "docs" / "specs").mkdir(parents=True, exist_ok=True)
            (target / "docs" / "specs" / "core.md").write_text(
                '---\nid: core.svc\ndomain: core\nowns: ["src/**"]\nsources: [SRC-001]\npromise: Fast response.\n---\n# Core Svc\n',
                encoding="utf-8",
            )
            (target / "src").mkdir(parents=True, exist_ok=True)
            (target / "src" / "main.py").write_text("# Role: Demo entrypoint.\ndef main():\n    return 1\n", encoding="utf-8")
            (target / "docs" / "work.toml").write_text(
                '[[milestones]]\nid = "M-DONE"\ndomain = "core"\nslot = "done"\nname = "Bootstrap"\n\n'
                '[[milestones]]\nid = "M-NOW"\ndomain = "core"\nslot = "now"\nname = "Active Slice"\n\n'
                '[[tasks]]\nid = "T-DONE"\nmilestone = "M-DONE"\ntitle = "Seed repo"\nstate = "done"\nhuman_check = "approved"\nspecs = ["core.svc"]\n\n'
                '[[tasks]]\nid = "T-NOW"\nmilestone = "M-NOW"\ntitle = "Build feature"\nstate = "active"\nhuman_check = "pending"\nspecs = ["core.svc"]\nsources = ["SRC-001"]\n',
                encoding="utf-8",
            )

            ctx_proc = subprocess.run(
                [sys.executable, str(SCRIPTS_DIR / "project.py"), "--root", str(target), "context", "src/main.py", "--json"],
                capture_output=True,
                text=True,
                check=True,
            )
            capsule = json.loads(ctx_proc.stdout)
            self.assertTrue(capsule["found"])
            self.assertEqual(capsule["module"]["id"], "core.svc")
            self.assertEqual(capsule["module"]["promise"], "Fast response.")

            doc_ctx_proc = subprocess.run(
                [sys.executable, str(SCRIPTS_DIR / "project.py"), "--root", str(target), "context", "AGENTS.md", "--json"],
                capture_output=True,
                text=True,
                check=True,
            )
            doc_ctx = json.loads(doc_ctx_proc.stdout)
            self.assertTrue(doc_ctx["found"])
            self.assertEqual(doc_ctx["focus_kind"], "document")

            task_txt_proc = subprocess.run(
                [sys.executable, str(SCRIPTS_DIR / "project.py"), "--root", str(target), "context", "T-NOW"],
                capture_output=True,
                text=True,
                check=True,
            )
            self.assertIn("in progress", task_txt_proc.stdout)
            self.assertNotIn("Verbatim L1", task_txt_proc.stdout)

            trace_proc = subprocess.run(
                [sys.executable, str(SCRIPTS_DIR / "project.py"), "--root", str(target), "trace", "SRC-001", "--json"],
                capture_output=True,
                text=True,
                check=True,
            )
            trace = json.loads(trace_proc.stdout)
            self.assertTrue(trace["found"])
            self.assertEqual(trace["modules"][0]["id"], "core.svc")

            # Archive M-DONE into docs/archive/work-m-done.toml
            arch_path = archive_completed_milestone(target, "M-DONE")
            self.assertTrue(arch_path.is_file())
            self.assertNotIn('id = "M-DONE"', (target / "docs" / "work.toml").read_text(encoding="utf-8"))
            self.assertIn('id = "M-DONE"', arch_path.read_text(encoding="utf-8"))

            reloaded = load_project_graph(target)
            self.assertTrue(reloaded.milestones["M-DONE"].archived)
            self.assertFalse(reloaded.milestones["M-NOW"].archived)

            with tempfile.TemporaryDirectory() as zh_tmp:
                zh_dir = Path(zh_tmp)
                zh_init = subprocess.run(
                    [sys.executable, str(SCRIPTS_DIR / "project.py"), "init", "--target", str(zh_dir), "--name", "中文服务", "--lang", "zh"],
                    capture_output=True,
                    text=True,
                    check=True,
                )
                self.assertIn("中文服务", zh_init.stdout)
                self.assertIn("原型验证期 (0->0.1)", zh_init.stdout)
                self.assertNotIn("stage=prototype", zh_init.stdout)
                self.assertIn("首个可用版本", (zh_dir / "docs" / "work.toml").read_text(encoding="utf-8"))
                self.assertIn("先用平实直接的中文", (zh_dir / "AGENTS.md").read_text(encoding="utf-8"))
                self.assertIn("系统架构总览", (zh_dir / "ARCHITECTURE.md").read_text(encoding="utf-8"))
                self.assertIn("平实", (zh_dir / "docs" / "README.md").read_text(encoding="utf-8"))
                self.assertIn("示例模块", (zh_dir / "docs" / "specs" / "example" / "module.md").read_text(encoding="utf-8"))
                zh_chk = subprocess.run(
                    [sys.executable, str(zh_dir / "scripts" / "check_docs.py"), "--strict"],
                    cwd=zh_dir,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(zh_chk.returncode, 0, zh_chk.stdout + zh_chk.stderr)

    def test_http_server_routes_and_toml_writebacks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            subprocess.run(
                [sys.executable, str(SCRIPTS_DIR / "project.py"), "--root", str(root), "init", "--name", "Web Perspective Repo"],
                check=True,
                capture_output=True,
            )
            (root / "docs" / "specs").mkdir(parents=True, exist_ok=True)
            (root / "docs" / "specs" / "billing.md").write_text(
                '---\nid: billing.api\ndomain: core\nowns: ["src/**"]\nsources: [SRC-001]\npromise: Accurate billing.\n---\n# Billing API\n',
                encoding="utf-8",
            )
            (root / "src").mkdir(parents=True, exist_ok=True)
            (root / "src" / "billing.py").write_text("# Role: Billing API.\ndef charge():\n    return True\n", encoding="utf-8")
            (root / "docs" / "work.toml").write_text(
                '[[milestones]]\nid = "M-1"\ndomain = "core"\nslot = "now"\nname = "Billing Rollout"\n\n'
                '[[tasks]]\nid = "T-READY"\nmilestone = "M-1"\ntitle = "Invoice export"\nstate = "ready_for_check"\nhuman_check = "pending"\nspecs = ["billing.api"]\n\n'
                '[[tasks]]\nid = "T-BLOCKED"\nmilestone = "M-1"\ntitle = "Refund policy"\nstate = "blocked"\nhuman_check = "pending"\nspecs = ["billing.api"]\nsources = ["SRC-001"]\nblocker_question = "支持全额还是按比例退款？"\nblocker_options = ["A: 仅全额", "B: 支持按比例"]\n',
                encoding="utf-8",
            )
            for cmd in (
                ["git", "init"],
                ["git", "config", "user.email", "test@example.com"],
                ["git", "config", "user.name", "Test"],
                ["git", "add", "."],
                ["git", "commit", "-m", "initial"],
            ):
                subprocess.run(cmd, cwd=root, check=True, capture_output=True)

            httpd = create_perspective_server(root, host="127.0.0.1", port=0)
            try:
                st_html, html = _dispatch_http(httpd, "GET", "/")
                self.assertEqual(st_html, 200)
                self.assertIn("Project Overview", html)
                self.assertIn('name="project-csrf"', html)

                st_css, css = _dispatch_http(httpd, "GET", "/styles/tokens.css")
                self.assertEqual(st_css, 200)
                self.assertIn("--bg-canvas: #F5F5F7;", css)
                self.assertIn("--bg-platter: #FFFFFF;", css)

                st_404, _ = _dispatch_http(httpd, "GET", "/../docs-policy.toml")
                self.assertEqual(st_404, 404)

                st_g, body_g = _dispatch_http(httpd, "GET", "/api/graph")
                self.assertEqual(st_g, 200)
                graph_json = json.loads(body_g)
                token = graph_json["csrf_token"]
                self.assertEqual(graph_json["project"]["name"], "Web Perspective Repo")
                self.assertEqual(len(graph_json["blocked_inbox"]), 1)
                self.assertEqual(graph_json["blocked_inbox"][0]["task_id"], "T-BLOCKED")

                st_c, body_c = _dispatch_http(httpd, "GET", "/api/context?q=billing.api")
                self.assertEqual(st_c, 200)
                cap_json = json.loads(body_c)
                self.assertTrue(cap_json["found"])
                self.assertEqual(cap_json["module"]["promise"], "Accurate billing.")

                # Reject POST without X-Project-Token or from foreign Origin
                st_no_tok, _ = _dispatch_http(httpd, "POST", "/api/tasks/approve", {"task_id": "T-READY"})
                self.assertEqual(st_no_tok, 403)
                st_bad_orig, _ = _dispatch_http(
                    httpd,
                    "POST",
                    "/api/tasks/approve",
                    {"task_id": "T-READY"},
                    headers={"X-Project-Token": token, "Origin": "https://evil.example"},
                )
                self.assertEqual(st_bad_orig, 403)

                auth_headers = {"X-Project-Token": token}
                # Malformed JSON -> 400; missing task_id -> 404
                st_bad_json, _ = _dispatch_http(
                    httpd, "POST", "/api/tasks/approve", headers=auth_headers, raw_body=b"{invalid"
                )
                self.assertEqual(st_bad_json, 400)
                st_missing, _ = _dispatch_http(
                    httpd, "POST", "/api/tasks/approve", {"task_id": "T-MISSING"}, headers=auth_headers
                )
                self.assertEqual(st_missing, 404)

                # Approve T-READY (transitions ready_for_check -> done + approved)
                st_app, body_app = _dispatch_http(httpd, "POST", "/api/tasks/approve", {"task_id": "T-READY"}, headers=auth_headers)
                self.assertEqual(st_app, 200)
                self.assertTrue(json.loads(body_app)["ok"])

                # Resolve T-BLOCKED with multiline/quoted human decision (tests TOML escaping)
                resolution_text = "首期只做\"全额退款\"\n并保留'''原单凭证'''。"
                st_blk, body_blk = _dispatch_http(
                    httpd,
                    "POST",
                    "/api/tasks/resolve-blocker",
                    {"task_id": "T-BLOCKED", "resolution": resolution_text},
                    headers=auth_headers,
                )
                self.assertEqual(st_blk, 200)
                self.assertTrue(json.loads(body_blk)["ok"])

                # Mark review anchor & verify /api/diff + /api/tests/run schemas
                st_rev, body_rev = _dispatch_http(httpd, "POST", "/api/review/mark", {}, headers=auth_headers)
                self.assertEqual(st_rev, 200)
                self.assertTrue(json.loads(body_rev)["ok"])

                (root / "README.md").write_text("# Role: Root README.\nUpdated.\n", encoding="utf-8")
                st_diff, body_diff = _dispatch_http(httpd, "GET", "/api/diff")
                self.assertEqual(st_diff, 200)
                diff_json = json.loads(body_diff)
                self.assertTrue(diff_json["domains"], diff_json)
                for dg in diff_json["domains"]:
                    self.assertIsInstance(dg["files"], int)
                    self.assertIsInstance(dg["changed_files"], list)

                st_tests, body_tests = _dispatch_http(httpd, "POST", "/api/tests/run", {}, headers=auth_headers)
                self.assertEqual(st_tests, 200)
                tests_json = json.loads(body_tests)
                self.assertIn("ok", tests_json)
                self.assertIn("exit_code", tests_json.get("result", {}))

                updated = load_project_graph(root)
                self.assertEqual(updated.tasks["T-READY"].human_check, "approved")
                self.assertEqual(updated.tasks["T-READY"].state, "done")
                self.assertEqual(updated.tasks["T-BLOCKED"].state, "active")
                self.assertEqual(updated.tasks["T-BLOCKED"].blocker_question, "")
                self.assertIn("SRC-002", updated.sources)
                self.assertEqual(updated.sources["SRC-002"].quote, resolution_text)

                out_html = export_standalone_html(root, root / "snapshot.html")
                snap_txt = out_html.read_text(encoding="utf-8")
                self.assertIn("window.__PERSPECTIVE_DATA__", snap_txt)
                self.assertNotIn('src="/js/app.js"', snap_txt)
                self.assertNotIn("cdn.jsdelivr.net", snap_txt)
                self.assertNotIn("style=\"", snap_txt)
            finally:
                httpd.server_close()

    def test_init_nonstandard_dirs_copied_checkout_and_sync(self) -> None:
        # 1. Mixed non-standard dir (backend/*.vue) + user scripts/deploy.py + root manage.py
        with tempfile.TemporaryDirectory() as tmp1:
            repo1 = Path(tmp1)
            (repo1 / "backend").mkdir()
            (repo1 / "backend" / "app.vue").write_text("<!-- Role: Vue app root. -->\n<template><div /></template>\n", encoding="utf-8")
            (repo1 / "scripts").mkdir()
            (repo1 / "scripts" / "deploy.py").write_text("# Role: Deploy helper.\ndef deploy(): return 0\n", encoding="utf-8")
            (repo1 / "manage.py").write_text("# Role: Management runner.\ndef run(): return 0\n", encoding="utf-8")
            res1 = subprocess.run(
                [sys.executable, str(SCRIPTS_DIR / "project.py"), "init", "--target", str(repo1), "--name", "后端服务", "--lang", "zh", "--stage", "usable"],
                capture_output=True, text=True, check=False,
            )
            self.assertEqual(res1.returncode, 0, res1.stdout + res1.stderr)
            pol1 = (repo1 / "docs-policy.toml").read_text(encoding="utf-8")
            self.assertIn('stage = "observed"', pol1)
            for root_name in ("backend", "scripts", "manage.py"):
                self.assertIn(root_name, pol1)
            self.assertEqual(subprocess.run([sys.executable, "-B", str(repo1 / "scripts" / "check_docs.py")], cwd=repo1, capture_output=True).returncode, 0)
            strict1 = subprocess.run([sys.executable, "-B", str(repo1 / "scripts" / "check_docs.py"), "--strict"], cwd=repo1, capture_output=True, text=True)
            self.assertNotEqual(strict1.returncode, 0)
            self.assertIn("unclaimed_source", strict1.stdout)
            st1 = subprocess.run([sys.executable, "-B", str(repo1 / "scripts" / "project.py"), "status", "--json"], cwd=repo1, capture_output=True, text=True, check=True)
            st1_data = json.loads(st1.stdout)
            file_paths = {f["path"] for cap in st1_data.get("capsules", {}).values() for f in cap.get("telemetry", {}).get("files", [])}
            self.assertIn("backend/app.vue", file_paths)
            self.assertIn("scripts/deploy.py", file_paths)
            self.assertIn("manage.py", file_paths)
            self.assertFalse(any("scripts/projectlib/" in p for p in file_paths), file_paths)

        # 2. Full copied template checkout (with template docs, domains, ADRs, examples, non-template remote)
        with tempfile.TemporaryDirectory() as tmp2:
            repo2 = Path(tmp2)
            for fname in ("AGENTS.md", "ARCHITECTURE.md", "README.md", "README_CN.md", "docs-policy.toml", "architecture-rules.toml"):
                shutil.copy2(ROOT / fname, repo2 / fname)
            shutil.copytree(ROOT / "docs", repo2 / "docs")
            shutil.copytree(ROOT / "examples", repo2 / "examples")
            shutil.copytree(ROOT / "tests", repo2 / "tests")
            for cmd in (["git", "init"], ["git", "config", "user.email", "t@e.com"], ["git", "config", "user.name", "T"], ["git", "remote", "add", "origin", "https://example.com/forked-app.git"], ["git", "add", "."], ["git", "commit", "-m", "fork"]):
                subprocess.run(cmd, cwd=repo2, check=True, capture_output=True)
            head2 = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=repo2, check=True, capture_output=True, text=True).stdout.strip()
            res2 = subprocess.run(
                [sys.executable, str(SCRIPTS_DIR / "project.py"), "init", "--target", str(repo2), "--name", "Forked App", "--lang", "en"],
                capture_output=True, text=True, check=False,
            )
            self.assertEqual(res2.returncode, 0, res2.stdout + res2.stderr)
            pol2 = (repo2 / "docs-policy.toml").read_text(encoding="utf-8")
            self.assertIn('identity = "product"', pol2)
            self.assertNotIn('identity = "template"', pol2)
            self.assertFalse((repo2 / "docs" / "specs" / "discipline").exists())
            self.assertFalse((repo2 / "examples" / "reference-app").exists())
            self.assertFalse((repo2 / "README_CN.md").exists())
            self.assertNotIn("SRC-022", (repo2 / "docs" / "sources.toml").read_text(encoding="utf-8"))
            self.assertIn(f'review_anchor_sha = "{head2}"', pol2)
            strict2 = subprocess.run([sys.executable, "-B", str(repo2 / "scripts" / "check_docs.py"), "--strict"], cwd=repo2, capture_output=True, text=True)
            self.assertEqual(strict2.returncode, 0, strict2.stdout + strict2.stderr)
            self.assertIn("check_docs: OK", strict2.stdout)
            status2 = subprocess.run([sys.executable, "-B", str(repo2 / "scripts" / "project.py"), "status"], cwd=repo2, capture_output=True, text=True)
            self.assertEqual(status2.returncode, 0, status2.stdout + status2.stderr)
            self.assertIn("+0 commits", status2.stdout)

            # 3. --sync preserves review_anchor_sha, inserts missing harness_paths/discipline_version, skips example starter, prints Synced + docs/README & legacy severity notices
            old_pol = re.sub(r'^\s*(?:discipline_version|review_anchor_sha)\s*=.*\r?\n?', "", pol2, flags=re.MULTILINE)
            old_pol = re.sub(r'harness_paths\s*=\s*\[.*?\]\r?\n?', "", old_pol, flags=re.S)
            old_pol = old_pol.replace("[collaboration]\n", '[collaboration]\nreview_anchor_sha = "abc1234"\n', 1)
            old_pol = old_pol.replace('disclaimer_phrases = "advisory"', 'startup_disclaimers = "error"') + "\n# custom_marker\n"
            (repo2 / "docs-policy.toml").write_text(old_pol, encoding="utf-8")
            res_sync = subprocess.run(
                [sys.executable, str(SCRIPTS_DIR / "project.py"), "init", "--target", str(repo2), "--sync"],
                capture_output=True, text=True, check=False,
            )
            self.assertEqual(res_sync.returncode, 0, res_sync.stdout + res_sync.stderr)
            self.assertIn("Synced", res_sync.stdout)
            self.assertIn("AGENTS.md", res_sync.stdout)
            self.assertIn("docs-readme.md", res_sync.stdout)
            self.assertIn("startup_disclaimers", res_sync.stdout)
            import tomllib
            expected_ver = tomllib.loads((ROOT / "docs-policy.toml").read_text(encoding="utf-8"))["discipline_version"]
            synced_pol = (repo2 / "docs-policy.toml").read_text(encoding="utf-8")
            self.assertIn(f'discipline_version = "{expected_ver}"', synced_pol)
            self.assertIn('review_anchor_sha = "abc1234"', synced_pol)
            self.assertIn('"scripts/projectlib"', synced_pol)
            self.assertIn("# custom_marker", synced_pol)
            self.assertEqual(subprocess.run([sys.executable, "-B", str(repo2 / "scripts" / "check_docs.py"), "--strict"], cwd=repo2, capture_output=True).returncode, 0)

            for hp_snippet in ("harness_paths = ['tests', 'tmp']\n", 'harness_paths = [\n  "tests"\n  # keep\n]\n'):
                variant = re.sub(r"\[layout\].*?(?=\n\[|\Z)", f"[layout] # paths\nsource_roots = [\"src\"]\n{hp_snippet}", pol2, count=1, flags=re.S)
                variant = variant.replace("[collaboration]\n", "[collaboration] # team\n", 1)
                (repo2 / "docs-policy.toml").write_text(variant, encoding="utf-8")
                v_sync = subprocess.run([sys.executable, str(SCRIPTS_DIR / "project.py"), "init", "--target", str(repo2), "--sync"], capture_output=True, text=True, check=False)
                self.assertEqual(v_sync.returncode, 0, v_sync.stdout + v_sync.stderr)
                parsed_v = tomllib.loads((repo2 / "docs-policy.toml").read_text(encoding="utf-8"))
                self.assertIn("scripts/projectlib", parsed_v["layout"]["harness_paths"])
                self.assertEqual(subprocess.run([sys.executable, "-B", str(repo2 / "scripts" / "check_docs.py"), "--strict"], cwd=repo2, capture_output=True).returncode, 0)

        # 4. In-place init on remote-less ZIP copy & cloned repo with --lang zh (+ --sync without docs/specs or code files)
        with tempfile.TemporaryDirectory() as tmp3:
            zip_repo = Path(tmp3)
            for fname in ("AGENTS.md", "ARCHITECTURE.md", "README.md", "README_CN.md", "docs-policy.toml", "architecture-rules.toml"):
                shutil.copy2(ROOT / fname, zip_repo / fname)
            for sub in ("docs", "examples", "scripts", "templates", "tests", ".agents"):
                shutil.copytree(ROOT / sub, zip_repo / sub, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            res_zip = subprocess.run([sys.executable, "-B", "scripts/project.py", "init", "--name", "ZipApp", "--lang", "zh"], cwd=zip_repo, capture_output=True, text=True, check=False)
            self.assertEqual(res_zip.returncode, 0, res_zip.stdout + res_zip.stderr)
            self.assertIn("决策", (zip_repo / "templates" / "adr.md").read_text(encoding="utf-8"))
            self.assertEqual(subprocess.run([sys.executable, "-B", "scripts/check_docs.py", "--strict"], cwd=zip_repo, capture_output=True).returncode, 0)

        with tempfile.TemporaryDirectory() as tmp4:
            nospec = Path(tmp4)
            (nospec / "docs").mkdir()
            (nospec / "AGENTS.md").write_text("# LegacyRepo\nPlain repo guide.\n", encoding="utf-8")
            (nospec / "ARCHITECTURE.md").write_text("# LegacyRepo\nSystem overview.\n", encoding="utf-8")
            (nospec / "docs" / "sources.toml").write_text('[[sources]]\nid = "SRC-001"\ndate = "2026-11-15"\nstatus = "active"\ncontext = "Goal"\nquote = "Initial goal"\n', encoding="utf-8")
            (nospec / "docs" / "work.toml").write_text('[[milestones]]\nid = "M-01"\ndomain = "core"\nname = "M1"\nslot = "now"\n', encoding="utf-8")
            (nospec / "docs-policy.toml").write_text('version = 2\n[project]\nidentity = "product"\ndefault_stage = "usable"\nlanguage = "en"\n[layout]\nsource_roots = ["src"]\n', encoding="utf-8")
            sync_empty = subprocess.run([sys.executable, "-B", str(SCRIPTS_DIR / "project.py"), "init", "--target", str(nospec), "--sync"], capture_output=True, text=True, check=False)
            self.assertEqual(sync_empty.returncode, 0, sync_empty.stdout + sync_empty.stderr)
            self.assertIn("usable", sync_empty.stdout)
            self.assertNotIn("New Project", sync_empty.stdout)
            self.assertNotIn("preserved existing docs/README.md", sync_empty.stdout)
            self.assertFalse((nospec / "docs" / "specs" / "example").exists())
            self.assertFalse((nospec / "src" / "example").exists())
            self.assertFalse((nospec / "tests" / "test_smoke.py").exists())


if __name__ == "__main__":
    unittest.main()
