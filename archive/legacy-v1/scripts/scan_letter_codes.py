#!/usr/bin/env python3
"""Report letter-number tokens (A11, G7, INV-2, ...) as health-assessment material.

Internal codes are cheap to write and expensive to read: a token like A11 is
self-evident only to its author. This scan makes their accumulation visible;
it is not a gate and always exits zero. Concentration in historical records
(completed plans, dated evidence, archives) is expected — history stays as
written. Tokens in living documents (contracts, surfaces, guides, issues,
entrypoints, templates) deserve a human look, and reconciliation-log entries
inside a living contract are history too: read the hits, then judge.
By default only living hits print per-line detail (capped per file);
historical and other groups print per-file counts — use --verbose for
everything.

Benign constants such as UTF-8 or SHA-256 are allowlisted; extend ALLOWED when
the project legitimately owns one. The pattern targets uppercase code-shaped
tokens; lowercase-led spellings such as v2 are intentionally out of scope.
"""

from __future__ import annotations

import argparse
import os
import re
from collections import Counter
from pathlib import Path

TOKEN_RE = re.compile(r"\b[A-Z]{1,6}-?\d{1,4}\b")

ALLOWED = {
    "UTF-8", "UTF-16", "UTF-32",
    "SHA-1", "SHA-224", "SHA-256", "SHA-384", "SHA-512",
    "MD2", "MD5", "BASE32", "BASE64",
}

SCAN_SUFFIXES = {".md", ".py", ".toml", ".yaml", ".yml", ".txt", ".json", ".sh"}

SKIPPED_DIRECTORIES = {
    ".git", ".hg", ".svn", ".idea", ".vscode",
    ".mypy_cache", ".pytest_cache", ".ruff_cache", ".tox",
    ".venv", "__pycache__", "node_modules", "venv", "vendor",
}

HISTORICAL_ROOTS = {("docs", "plans"), ("docs", "evidence"), ("archive",), ("tmp",)}
LIVING_ROOTS = {
    ("docs", "contracts"), ("docs", "design"), ("docs", "guides"), ("docs", "issues"),
}

MAX_SNIPPET = 100
MAX_DETAIL_LINES_PER_FILE = 30


def classify(relative: Path) -> str:
    parts = relative.parts
    if parts[:2] in HISTORICAL_ROOTS or parts[:1] in HISTORICAL_ROOTS:
        return "historical"
    if parts[:2] in LIVING_ROOTS or parts[0] == "templates":
        return "living"
    if len(parts) == 1 or (parts[0] == "docs" and len(parts) == 2):
        return "living"
    return "other"


def scan(root: Path) -> dict[str, dict[Path, list[tuple[int, str, str]]]]:
    findings: dict[str, dict[Path, list[tuple[int, str, str]]]] = {
        "living": {},
        "historical": {},
        "other": {},
    }
    for current, directory_names, file_names in os.walk(root):
        directory_names[:] = sorted(
            name for name in directory_names if name not in SKIPPED_DIRECTORIES
        )
        for name in sorted(file_names):
            path = Path(current) / name
            if path.suffix.lower() not in SCAN_SUFFIXES:
                continue
            relative = path.relative_to(root)
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            for lineno, line in enumerate(text.splitlines(), start=1):
                for token in TOKEN_RE.findall(line):
                    if token in ALLOWED:
                        continue
                    findings[classify(relative)].setdefault(relative, []).append(
                        (lineno, token, line.strip())
                    )
    return findings


def report(
    findings: dict[str, dict[Path, list[tuple[int, str, str]]]], verbose: bool
) -> None:
    living_tokens: Counter[str] = Counter()
    totals: Counter[str] = Counter()
    for group in ("living", "historical", "other"):
        files = findings[group]
        totals[group] = sum(len(hits) for hits in files.values())
        print(f"\n== {group} ({totals[group]} token(s) in {len(files)} file(s)) ==")
        detail = verbose or group == "living"
        for path in sorted(files):
            hits = files[path]
            if not detail:
                print(f"{path.as_posix()}: {len(hits)} token(s)")
                continue
            print(path.as_posix())
            shown = hits if verbose else hits[:MAX_DETAIL_LINES_PER_FILE]
            for lineno, token, line in shown:
                snippet = line if len(line) <= MAX_SNIPPET else line[: MAX_SNIPPET - 3] + "..."
                print(f"  {lineno}: {token} — {snippet}")
            if len(hits) > len(shown):
                print(f"  ... and {len(hits) - len(shown)} more in this file")
        if group == "living":
            for hits in files.values():
                living_tokens.update(token for _, token, _ in hits)
    print("\n== summary ==")
    for group in ("living", "historical", "other"):
        print(f"{group}: {totals[group]}")
    if living_tokens:
        common = ", ".join(
            f"{token}x{count}" for token, count in living_tokens.most_common(10)
        )
        print(f"most frequent in living documents: {common}")
    print("\nHealth-assessment material, not a gate: this report always exits 0.")
    print("Historical and other groups print per-file counts; --verbose prints every hit.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="repository root (defaults to the script's repository)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="print every hit; the default details only living documents",
    )
    args = parser.parse_args()
    report(scan(args.root.resolve()), verbose=args.verbose)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
