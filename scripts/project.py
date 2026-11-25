#!/usr/bin/env python3
# Role: Primary CLI (`status`, `context`, `trace`, `check`, `serve`, `export-html`, `archive-milestone`, `mark-reviewed`, `init`).
# Out of scope: Low-level AST/Git scanning internals (owned by scripts/projectlib/).
# Anchors: spec=perspective.server, ADR-002, SRC-014, SRC-015, SRC-016, SRC-017, SRC-018, SRC-019

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True

if __package__:
    from .projectlib.briefing_pack import serialize_perspective_payload
    from .projectlib.cli_format import print_context_pack, print_status, print_trace_summary
    from .projectlib.context_pack import build_context_pack, build_lineage_trace
    from .projectlib.init_repo import run_init_command
    from .projectlib.loader import load_project_graph
    from .projectlib.server import (
        archive_completed_milestone,
        create_perspective_server,
        export_standalone_html,
        mark_review_anchor,
    )
    from .projectlib.validator import validate_project_graph
else:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from projectlib.briefing_pack import serialize_perspective_payload
    from projectlib.cli_format import print_context_pack, print_status, print_trace_summary
    from projectlib.context_pack import build_context_pack, build_lineage_trace
    from projectlib.init_repo import run_init_command
    from projectlib.loader import load_project_graph
    from projectlib.server import (
        archive_completed_milestone,
        create_perspective_server,
        export_standalone_html,
        mark_review_anchor,
    )
    from projectlib.validator import validate_project_graph


def _cmd_status(root: Path, fmt: str) -> int:
    graph = load_project_graph(root)
    payload = serialize_perspective_payload(graph)
    if fmt == "json":
        sys.stdout.write(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
        return 0
    lang = str(graph.policy.get("project", {}).get("language", "en")).strip().lower() or "en"
    print_status(payload, lang=lang)
    return 0


def _cmd_context(root: Path, target: str, fmt: str) -> int:
    graph = load_project_graph(root)
    pack = build_context_pack(graph, target)
    if fmt == "json":
        sys.stdout.write(json.dumps(pack, ensure_ascii=False, indent=2) + "\n")
        return 0 if pack.get("found") else 1
    if not pack.get("found"):
        print(pack.get("message", "Not found"), file=sys.stderr)
        return 1
    lang = str(graph.policy.get("project", {}).get("language", "en")).strip().lower() or "en"
    print_context_pack(pack, target, task_obj=graph.tasks.get(target), lang=lang)
    return 0


def _cmd_trace(root: Path, node_id: str, fmt: str) -> int:
    graph = load_project_graph(root)
    tr = build_lineage_trace(graph, node_id)
    if fmt == "json":
        sys.stdout.write(json.dumps(tr, ensure_ascii=False, indent=2) + "\n")
        return 0 if tr.get("found") else 1
    if not tr.get("found"):
        print(tr.get("message", "Unknown node"), file=sys.stderr)
        return 1
    lang = str(graph.policy.get("project", {}).get("language", "en")).strip().lower() or "en"
    print_trace_summary(tr, lang=lang)
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Single-Source-of-Truth Project Overview CLI & Local Web Service.")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_st = sub.add_parser("status", help="Show multi-domain progress, blockers, and review accumulation.")
    p_st.add_argument("--format", choices=("text", "json"), default="text")
    p_st.add_argument("--json", action="store_const", const="json", dest="format")

    p_ctx = sub.add_parser("context", help="Show context pack for a source file, document, directory, or ID.")
    p_ctx.add_argument("target")
    p_ctx.add_argument("--format", choices=("text", "json"), default="text")
    p_ctx.add_argument("--json", action="store_const", const="json", dest="format")

    p_tr = sub.add_parser("trace", help="Trace bidirectional links from a user quote or ADR decision ID.")
    p_tr.add_argument("node_id")
    p_tr.add_argument("--format", choices=("text", "json"), default="text")
    p_tr.add_argument("--json", action="store_const", const="json", dest="format")

    p_chk = sub.add_parser("check", help="Run single-source & architecture boundary validation.")
    p_chk.add_argument("--strict", action="store_true")
    p_chk.add_argument("--diff-base", default=None)
    p_chk.add_argument("--format", choices=("text", "json"), default="text")
    p_chk.add_argument("--json", action="store_const", const="json", dest="format")

    p_srv = sub.add_parser(
        "serve",
        help="Run the local calm-platter Project Overview web workbench and HTTP API.",
    )
    p_srv.add_argument("--host", default="127.0.0.1")
    p_srv.add_argument("--port", type=int, default=8765)

    p_exp = sub.add_parser("export-html", help="Export a self-contained static HTML overview.")
    p_exp.add_argument("--output", type=Path, default=Path("tmp/project-perspective.html"))

    p_arc = sub.add_parser("archive-milestone", help="Move a completed milestone into docs/archive/.")
    p_arc.add_argument("milestone_id")

    sub.add_parser("mark-reviewed", help="Record current HEAD as the latest holistic review / Grill anchor.")

    p_init = sub.add_parser("init", help="Initialize a product repository with AGENTS.md, specs, and ledgers.")
    p_init.add_argument("--target", type=Path, default=None)
    p_init.add_argument("--name", default="New Project")
    p_init.add_argument("--stage", choices=("prototype", "usable", "stable"), default="prototype")
    p_init.add_argument("--lang", choices=("en", "zh"), default="en")
    p_init.add_argument(
        "--sync",
        action="store_true",
        help="Refresh transferable contracts, guides, skills, templates, and scripts in an adopted repository.",
    )

    args = parser.parse_args(argv)
    root = args.root.resolve()

    if args.cmd == "status":
        return _cmd_status(root, args.format)
    if args.cmd == "context":
        return _cmd_context(root, args.target, args.format)
    if args.cmd == "trace":
        return _cmd_trace(root, args.node_id, args.format)
    if args.cmd == "check":
        graph = load_project_graph(root)
        findings, _ = validate_project_graph(graph, strict=args.strict, diff_base=args.diff_base)
        errs = [f for f in findings if f.severity == "error"]
        if args.format == "json":
            sys.stdout.write(json.dumps({"ok": not errs, "count": len(findings)}, indent=2) + "\n")
        else:
            for f in findings:
                print(f"[{f.severity.upper()}] ({f.rule_id}) {f.path}: {f.message}")
            if not errs:
                print("project check: OK")
        return 1 if errs else 0
    if args.cmd == "serve":
        srv = create_perspective_server(root, args.host, args.port)
        actual_port = srv.server_address[1]
        print(f"Project Overview serving at http://{args.host}:{actual_port} (Ctrl+C to stop)")
        try:
            srv.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            srv.server_close()
        return 0
    if args.cmd == "export-html":
        out = args.output if args.output.is_absolute() else (root / args.output)
        written = export_standalone_html(root, out)
        print(f"Exported standalone HTML overview to {written}")
        return 0
    if args.cmd == "archive-milestone":
        arch = archive_completed_milestone(root, args.milestone_id)
        print(f"Archived milestone `{args.milestone_id}` to {arch}")
        return 0
    if args.cmd == "mark-reviewed":
        st = mark_review_anchor(root)
        print(f"Marked review anchor at {st.get('last_review_sha')}")
        return 0
    if args.cmd == "init":
        template_root = Path(__file__).resolve().parents[1]
        return run_init_command(template_root, args.target or root, args.name, args.stage, args.lang, sync=args.sync)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
