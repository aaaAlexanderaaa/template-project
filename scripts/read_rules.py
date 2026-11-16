#!/usr/bin/env python3
# Role: CLI for rule-span preparation (`list`, `prepare`, `read`, `overview`) and external repo `onboard` inventory.
# Out of scope: Mutating target repositories without explicit confirmation or running web servers.
# Anchors: spec=graph.validator, ADR-002, SRC-010, SRC-012

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tomllib
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True

if sys.version_info < (3, 11):
    raise SystemExit("read_rules requires Python 3.11 or newer.")

if __package__:
    from .projectlib.loader import load_project_graph
    from .rule_reading import RuleError, RuleRepository, utf8_parts
else:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from projectlib.loader import load_project_graph
    from rule_reading import RuleError, RuleRepository, utf8_parts

SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build", "tmp", "archive"}
CODE_EXTS = {".py", ".js", ".mjs", ".cjs", ".jsx", ".ts", ".tsx", ".go", ".rs", ".java", ".rb", ".c", ".cpp", ".cs", ".swift", ".kt"}
UI_EXTS = {".css", ".scss", ".less", ".html", ".tsx", ".jsx", ".vue", ".svelte"}


def inspect_external_target(template_root: Path, target: Path) -> dict[str, Any]:
    target = target.resolve()
    if not target.is_dir():
        raise RuleError(f"target directory does not exist: {target}")

    tpl_policy = tomllib.loads((template_root / "docs-policy.toml").read_text(encoding="utf-8"))
    tpl_version = str(tpl_policy.get("discipline_version", "unknown"))

    git_ok = False
    dirty_count = 0
    try:
        rc = subprocess.run(
            ["git", "--no-optional-locks", "rev-parse", "--is-inside-work-tree"],
            cwd=target,
            capture_output=True,
            text=True,
            check=False,
        )
        git_ok = rc.returncode == 0 and rc.stdout.strip() == "true"
        if git_ok:
            st = subprocess.run(
                ["git", "--no-optional-locks", "status", "--porcelain"],
                cwd=target,
                capture_output=True,
                text=True,
                check=False,
            )
            dirty_count = len([ln for ln in st.stdout.splitlines() if ln.strip()])
    except OSError:
        git_ok = False

    existing_entrypoints = [
        name
        for name in ("AGENTS.md", "CLAUDE.md", "GEMINI.md", "ARCHITECTURE.md", "docs-policy.toml")
        if (target / name).is_file()
    ]

    tpl_budgets = tpl_policy.get("budgets", {})
    target_version = None
    target_identity = ""
    src_budget = int(tpl_budgets.get("max_source_lines", 500))
    css_budget = int(tpl_budgets.get("max_style_lines", 300))
    banned_dirs = {str(d).lower() for d in tpl_budgets.get("forbid_catchall_dirs", ["utils", "helpers", "common", "misc"])}
    harness_paths: list[str] = []
    if (target / "docs-policy.toml").is_file():
        try:
            tp = tomllib.loads((target / "docs-policy.toml").read_text(encoding="utf-8"))
            target_version = str(tp.get("discipline_version", "legacy-v1"))
            target_identity = str(tp.get("project", {}).get("identity", "")).strip().lower()
            bcfg = tp.get("budgets", {})
            src_budget = int(bcfg.get("max_source_lines", 500))
            css_budget = int(bcfg.get("max_style_lines", 300))
            if "forbid_catchall_dirs" in bcfg:
                banned_dirs = {str(d).lower() for d in bcfg.get("forbid_catchall_dirs", [])}
            harness_paths = [str(p).rstrip("/") for p in tp.get("layout", {}).get("harness_paths", []) if str(p).strip()]
        except (OSError, tomllib.TOMLDecodeError, ValueError, TypeError):
            target_version = "unparseable"

    total_files = 0
    total_loc = 0
    has_ui_files = False
    oversized: list[dict[str, Any]] = []
    catchall_dirs: list[str] = []
    top_dirs: dict[str, int] = {}

    is_adopter_repo = (
        (target / "scripts" / "projectlib").is_dir()
        and target_identity != "template"
        and not (target / "docs" / "specs" / "discipline").is_dir()
    )
    copied_tools = {"scripts/project.py", "scripts/check_docs.py", "scripts/read_rules.py", "scripts/rule_reading.py"}

    def _is_harness_or_copied(rel_path: str) -> bool:
        if is_adopter_repo and (rel_path in copied_tools or rel_path.startswith("scripts/projectlib/")):
            return True
        if rel_path.startswith("docs/archive/"):
            return True
        return any(rel_path == hp or rel_path.startswith(f"{hp}/") for hp in harness_paths)

    for dirpath, dirnames, filenames in os.walk(target):
        dirnames[:] = [d for d in sorted(dirnames) if d not in SKIP_DIRS and not d.startswith(".")]
        for d in dirnames:
            if d.lower() in banned_dirs:
                catchall_dirs.append((Path(dirpath) / d).relative_to(target).as_posix())
        for fn in sorted(filenames):
            if fn.startswith("."):
                continue
            fp = Path(dirpath) / fn
            rel = fp.relative_to(target).as_posix()
            if _is_harness_or_copied(rel):
                continue
            total_files += 1
            ext = fp.suffix.lower()
            if ext in UI_EXTS:
                has_ui_files = True
            if ext in (CODE_EXTS | UI_EXTS):
                try:
                    lc = len(fp.read_text(encoding="utf-8", errors="ignore").splitlines())
                except OSError:
                    lc = 0
                total_loc += lc
                top = rel.split("/", 1)[0] if "/" in rel else "(root)"
                top_dirs[top] = top_dirs.get(top, 0) + lc
                limit = css_budget if ext in {".css", ".scss", ".less"} else src_budget
                if lc > limit:
                    oversized.append({"path": rel, "lines": lc, "budget": limit})

    if total_files == 0:
        recommended_path = "Path A — Empty directory: initialize git and bootstrap `prototype` (0->0.1) skeleton."
    elif target_version:
        recommended_path = (
            f"Path C — Version sync: target has discipline_version={target_version}, template has {tpl_version}."
        )
    else:
        recommended_path = (
            "Path B — Existing codebase: preserve existing files, ensure clean git commit first, "
            "and start `[adoption].stage = 'observed'`."
        )

    contract_rel_paths = [
        "AGENTS.md",
        "docs/README.md#language-standard",
        "docs/contracts/collaboration-and-governance.md",
        "docs/contracts/architecture-and-modularity.md",
        "docs/contracts/delivery-and-verification.md",
        "docs/contracts/adoption-and-synchronization.md",
    ]
    if has_ui_files:
        contract_rel_paths.append("docs/contracts/frontend-and-visual-discipline.md")
    required_contracts: list[str] = []
    for raw_p in contract_rel_paths:
        base_rel, _, frag = raw_p.partition("#")
        if (target / base_rel).is_file():
            required_contracts.append(raw_p)
        else:
            qual = (template_root / base_rel).as_posix()
            required_contracts.append(f"{qual}#{frag}" if frag else qual)

    return {
        "target": str(target),
        "template_discipline_version": tpl_version,
        "target_discipline_version": target_version,
        "is_git_repo": git_ok,
        "uncommitted_entries": dirty_count,
        "existing_entrypoints": existing_entrypoints,
        "total_files": total_files,
        "code_and_style_loc": total_loc,
        "has_ui_or_style_files": has_ui_files,
        "top_directories_by_loc": dict(sorted(top_dirs.items(), key=lambda x: -x[1])[:10]),
        "oversized_files": sorted(oversized, key=lambda x: -x["lines"])[:15],
        "catchall_directories": sorted(catchall_dirs)[:20],
        "budgets_used": {"max_source_lines": src_budget, "max_style_lines": css_budget},
        "recommended_adoption_path": recommended_path,
        "required_reading_before_judgment": required_contracts,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    sub = parser.add_subparsers(dest="operation", required=True)

    sub.add_parser("list", help="Show concern slugs and rule units.")

    ov = sub.add_parser("overview", help="Summarize current contracts, domains, specs, ADRs, and active tasks.")
    ov.add_argument("--format", choices=("text", "json"), default="text")
    ov.add_argument("--json", action="store_const", const="json", dest="format")

    prep = sub.add_parser("prepare", help="Emit complete rule units for selected concerns.")
    prep.add_argument("--concern", action="append", default=[])
    prep.add_argument("--target", action="append", default=[])
    prep.add_argument("--include", action="append", default=[])
    prep.add_argument("--owner", action="append", default=[], help="Optional concern=path owner binding.")

    rd = sub.add_parser("read", help="Read a rule unit verified against its sha256 digest.")
    rd.add_argument("--unit", required=True)
    rd.add_argument("--digest", required=True)
    rd.add_argument("--part", type=int)
    rd.add_argument("--part-size", type=int, default=12000)

    ob = sub.add_parser("onboard", help="Inventory an external target repository before adoption or sync.")
    ob.add_argument("--target", type=Path, required=True)
    ob.add_argument("--format", choices=("text", "json"), default="text")
    ob.add_argument("--json", action="store_const", const="json", dest="format")

    args = parser.parse_args(argv)
    try:
        if args.operation == "list":
            repo = RuleRepository(args.root)
            sys.stdout.write(json.dumps(repo.routes(), ensure_ascii=False, indent=2) + "\n")
            return 0
        if args.operation == "prepare":
            repo = RuleRepository(args.root)
            valid_concerns = set(repo.CONCERN_MAP.keys()) | {"general"}
            owner_paths: list[str] = []
            for item in args.owner:
                if "=" in item:
                    c_key, c_path = item.split("=", 1)
                    if c_key not in valid_concerns:
                        raise RuleError(
                            f"unknown concern `{c_key}` in --owner `{item}`; valid: {', '.join(sorted(valid_concerns))}"
                        )
                    owner_paths.append(c_path)
                else:
                    owner_paths.append(item)
            units = repo.prepare(args.concern, args.target, [*args.include, *owner_paths])
            sys.stdout.write(repo.transcript(units))
            return 0
        if args.operation == "read":
            repo = RuleRepository(args.root)
            unit = repo.read(args.unit, args.digest)
            parts = utf8_parts(unit.data, args.part_size) if args.part is not None else [unit.data]
            idx = args.part if args.part is not None else 1
            if not 1 <= idx <= len(parts):
                raise RuleError(f"part must be between 1 and {len(parts)}")
            header = {
                "identity": unit.identity,
                "file_sha256": unit.file_digest,
                "part": idx,
                "total": len(parts),
                "bytes": len(parts[idx - 1]),
            }
            sys.stdout.write(json.dumps(header, ensure_ascii=False) + "\nBEGIN CONTENT\n")
            sys.stdout.write(parts[idx - 1].decode("utf-8") + "\nEND CONTENT\n")
            return 0
        if args.operation == "overview":
            graph = load_project_graph(args.root)
            summary = {
                "project": graph.project_name,
                "discipline_version": graph.discipline_version,
                "domains": sorted(graph.domains.keys()),
                "modules": sorted(graph.modules.keys()),
                "decisions": {k: v.status for k, v in sorted(graph.decisions.items())},
                "sources_count": len(graph.sources),
                "active_tasks": [t.id for t in graph.tasks.values() if not t.archived and t.state != "done"],
            }
            if args.format == "json":
                sys.stdout.write(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
            else:
                print(f"Project: {summary['project']} (discipline_version={summary['discipline_version']})")
                print(f"Domains ({len(summary['domains'])}): {', '.join(summary['domains'])}")
                print(f"Module specs ({len(summary['modules'])}): {', '.join(summary['modules'])}")
                print(f"Sources: {summary['sources_count']} | Open tasks: {', '.join(summary['active_tasks']) or 'none'}")
            return 0
        if args.operation == "onboard":
            report = inspect_external_target(args.root, args.target)
            if args.format == "json":
                sys.stdout.write(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
            else:
                print(f"Onboarding Inventory for: {report['target']}")
                print(f"• Recommended route: {report['recommended_adoption_path']}")
                print(f"• Git repo: {report['is_git_repo']} (uncommitted entries: {report['uncommitted_entries']})")
                print(f"• Existing entrypoints: {', '.join(report['existing_entrypoints']) or 'none'}")
                print(f"• Code/style LOC: {report['code_and_style_loc']} across {report['total_files']} files (UI/CSS={report['has_ui_or_style_files']})")
                if report["oversized_files"]:
                    top_ov = ", ".join(f"{x['path']} ({x['lines']}L/{x['budget']}L)" for x in report["oversized_files"][:5])
                    print(f"• Oversized files (budget={report['budgets_used']['max_source_lines']}L code / {report['budgets_used']['max_style_lines']}L style): {top_ov}")
                if report["catchall_directories"]:
                    print(f"• Catch-all directories: {', '.join(report['catchall_directories'][:5])}")
                print("• Required reading before applicability judgment:")
                for r in report["required_reading_before_judgment"]:
                    print(f"  - {r}")
            return 0
    except (RuleError, OSError, UnicodeError) as exc:
        print(f"read_rules: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
