#!/usr/bin/env python3
"""Emit complete applicable Markdown rules and digest-checked recovery parts."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True

if __package__:
    from .rule_reading import RuleError, RuleRepository, utf8_parts
else:
    from rule_reading import RuleError, RuleRepository, utf8_parts


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    sub = parser.add_subparsers(dest="operation", required=True)
    sub.add_parser("list", help="show current traits, concern slugs and reading targets")
    overview = sub.add_parser("overview", help="discover declared rules, working records and review commitments")
    overview.add_argument("--source", action="append", default=[], metavar="PATH",
                          help="replace default AGENTS.md/docs scope; repeat for more local files/directories")
    overview.add_argument("--format", choices=("text", "json"), default="text")
    overview.add_argument("--outline", action="store_true", help="include the complete operative heading inventory")
    overview.add_argument("--today", metavar="YYYY-MM-DD", help="explicit calendar reference; otherwise dates stay unassessed")
    overview.add_argument("--offset", type=int, default=0)
    overview.add_argument("--limit", type=int)
    overview.add_argument("--snapshot", help="require the snapshot from a preceding page")
    prepare = sub.add_parser("prepare", help="emit selected complete units in one transaction")
    prepare.add_argument("--concern", action="append", default=[])
    prepare.add_argument("--owner", action="append", default=[], metavar="CONCERN=PATH")
    prepare.add_argument("--target", action="append", default=[], metavar="REFERENCE")
    prepare.add_argument("--include", action="append", default=[], metavar="REFERENCE",
                         help="include a current method or rule and its complete prerequisites")
    prepare.add_argument("--context", help="identify this live reading context")
    prepare.add_argument("--retained", type=Path, metavar="MANIFEST",
                         help="assert bodies from this same-context manifest are still fully available")
    read = sub.add_parser("read", help="recover a unit using its expected whole-file digest")
    read.add_argument("--unit", required=True)
    read.add_argument("--digest", required=True)
    read.add_argument("--part", type=int)
    read.add_argument("--part-size", type=int, default=12000)
    args = parser.parse_args(argv)
    try:
        sys.stdout.reconfigure(encoding="utf-8", newline="")
        if sys.version_info < (3, 11):
            raise RuleError("read_rules requires Python 3.11 or newer")
        repo = None if args.operation == "overview" else RuleRepository(args.root)
        if args.operation == "overview":
            if __package__:
                from .document_overview import DocumentOverview, calendar_date, render_text
            else:
                from document_overview import DocumentOverview, calendar_date, render_text
            try:
                today = calendar_date(args.today) if args.today is not None else None
            except ValueError as exc:
                raise RuleError(f"--today: {exc}") from exc
            view = DocumentOverview(args.root).build(args.source, today=today, offset=args.offset,
                                                     limit=args.limit, snapshot=args.snapshot, include_outline=args.outline)
            output = json.dumps(view, ensure_ascii=False, indent=2) + "\n" if args.format == "json" else render_text(view)
            sys.stdout.write(output)
            return 0 if view["coverage"]["scan_complete"] else 2
        elif args.operation == "list":
            output = json.dumps(repo.routes(), ensure_ascii=False, indent=2) + "\n"
            repo.recheck(tuple(repo.sources.values()))
            sys.stdout.write(output)
        elif args.operation == "prepare":
            receipt = None
            if args.retained is not None:
                try:
                    receipt = json.loads(args.retained.read_text(encoding="utf-8"))
                except json.JSONDecodeError as exc:
                    raise RuleError(f"invalid retained manifest JSON: {exc}") from exc
                if not isinstance(receipt, dict):
                    raise RuleError("retained manifest must be a version 2 object")
            prepared = repo.prepare(args.concern, args.owner, args.target,
                                    includes=args.include, context=args.context, retained=receipt)
            sys.stdout.write(repo.transcript(prepared))
        else:
            unit = repo.read(args.unit, args.digest)
            parts = utf8_parts(unit.data, args.part_size) if args.part is not None else [unit.data]
            index = args.part if args.part is not None else 1
            if not 1 <= index <= len(parts):
                raise RuleError(f"part must be between 1 and {len(parts)}")
            data = parts[index - 1]
            header = {"identity": unit.identity, "file_sha256": unit.file_digest,
                      "status": unit.status, "part": index, "total": len(parts), "bytes": len(data)}
            output = (json.dumps(header, ensure_ascii=False) + "\nBEGIN CONTENT\n").encode("utf-8")
            output += data + b"\nEND CONTENT\n" + (b"PART COMPLETE\n" if args.part is not None else b"UNIT COMPLETE\n")
            repo.recheck(tuple(repo.sources.values()))
            sys.stdout.buffer.write(output)
        return 0
    except (RuleError, OSError, UnicodeError) as exc:
        print(f"read_rules: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
