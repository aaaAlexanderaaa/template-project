#!/usr/bin/env python3
# Role: CLI entrypoint for single-source graph validation, boundary checks, and git-diff contextual reminders.
# Out of scope: HTTP serving or mutating repository files.
# Anchors: spec=graph.validator, ADR-002, ADR-003, SRC-013, SRC-018

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True

if sys.version_info < (3, 11):
    raise SystemExit("check_docs requires Python 3.11 or newer.")

if __package__:
    from .projectlib.loader import load_project_graph
    from .projectlib.validator import validate_project_graph
else:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from projectlib.loader import load_project_graph
    from projectlib.validator import validate_project_graph


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate single-source docs, code ownership, and import boundaries.")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--strict", action="store_true", help="Promote advisories to errors.")
    parser.add_argument("--diff-base", default=None, help="Git ref to compute touched-module context against.")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args(argv)

    graph = load_project_graph(args.root)
    findings, nudges = validate_project_graph(graph, strict=args.strict, diff_base=args.diff_base)
    errors = [f for f in findings if f.severity == "error"]
    advisories = [f for f in findings if f.severity != "error"]

    if args.format == "json":
        payload = {
            "ok": len(errors) == 0,
            "error_count": len(errors),
            "advisory_count": len(advisories),
            "findings": [
                {"rule_id": f.rule_id, "severity": f.severity, "path": f.path, "line": f.line, "message": f.message}
                for f in findings
            ],
            "context_nudges": nudges,
        }
        sys.stdout.write(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
        return 1 if errors else 0

    for f in findings:
        loc = f"{f.path}:{f.line}" if f.line else f.path
        tag = "ERROR" if f.severity == "error" else "ADVISORY"
        print(f"[{tag}] ({f.rule_id}) {loc} — {f.message}")

    if nudges["touched_modules"]:
        stage_words = {
            "prototype": "prototype (0->0.1)",
            "usable": "usable (0.1->1)",
            "stable": "stable (1->N)",
        }
        print("\n--- Active Diff Context (Touched Modules & Verbatim User Quotes) ---")
        for item in nudges["touched_modules"]:
            st_lbl = stage_words.get(item["stage"], item["stage"])
            print(f"• {item['module']} ({st_lbl}, spec: {item['spec_path']})")
            if item["promise"]:
                print(f"  Promise: {item['promise']}")
            for q in item["sources"]:
                print(f"  [{q['id']}] “{q['excerpt']}”")

    if nudges.get("touched_docs"):
        print(
            "\n[PLAIN LANGUAGE REMINDER] Docs or UI copy changed: verify direct, ordinary wording "
            "in the project's chosen language (docs/README.md#language-standard) with zero coined jargon or raw enums."
        )

    if nudges["grill_suggested"]:
        c_n = nudges["commits_since_review"]
        m_n = len(nudges["modules_since_review"])
        print(
            f"\n[REVIEW SIGNAL] {c_n} commits across {m_n} modules accumulated since last review anchor. "
            "Consider asking the owner if a holistic check or `/grill` pass is helpful."
        )

    if not errors:
        print(
            f"check_docs: OK ({len(graph.domains)} domains, {len(graph.modules)} specs, "
            f"{len(graph.sources)} sources, {len(advisories)} advisories)."
        )
        return 0
    print(f"check_docs: FAILED with {len(errors)} error(s) and {len(advisories)} advisory(s).", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
