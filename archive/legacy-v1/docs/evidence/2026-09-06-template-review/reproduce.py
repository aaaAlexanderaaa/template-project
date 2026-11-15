"""Inspect this repository baseline; optionally rerun its existing checks.

This script does not run coding agents or certify behavioral adoption.
Run: python3 docs/evidence/2026-09-06-template-review/reproduce.py --checks
"""

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys


PATHS = [
    "AGENTS.md",
    "ARCHITECTURE.md",
    "docs/README.md",
    "docs/contracts/development-discipline.md",
    "docs/contracts/agent-execution-discipline.md",
    "docs/contracts/governance-decision-boundary.md",
    "docs/contracts/documentation-harness.md",
    "docs/contracts/engineering-judgment-discipline.md",
    "docs/contracts/project-adoption.md",
    "docs-policy.toml",
    "templates/contract.md",
    "templates/backend-change.md",
    "scripts/check_docs.py",
    "tests/test_check_docs.py",
]


def run(root, command):
    result = subprocess.run(command, cwd=root, text=True, capture_output=True)
    return {"command": command, "exit_code": result.returncode,
            "stdout": result.stdout, "stderr": result.stderr}


def inspect(root):
    files = []
    for name in PATHS:
        data = (root / name).read_bytes()
        text = data.decode("utf-8")
        history = {}
        for match in re.finditer(
            r"^## (Source anchors|Reconciliation log)\n(.*?)(?=^## |\Z)",
            text, re.MULTILINE | re.DOTALL,
        ):
            history[match[1]] = len(match[0].encode("utf-8"))
        files.append({"path": name, "bytes": len(data),
                      "lines": len(text.splitlines()),
                      "sha256": hashlib.sha256(data).hexdigest(),
                      "source_and_history_section_bytes": history})
    return {
        "python": sys.version,
        "baseline": run(root, ["git", "rev-parse", "HEAD"]),
        "files": files,
        "entry_three_bytes": sum(item["bytes"] for item in files[:3]),
        "six_document_example_bytes": sum(item["bytes"] for item in files[:6]),
        "scope_limit": "Bytes on disk, not injected tokens or observed causal harm. "
                       "The six-document set is an illustrative governance read path, "
                       "not a claim that every task must read all six.",
        "repository_history": run(root, ["git", "log", "-12", "--date=iso-strict",
                                         "--format=%h %ad %s"]),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[3])
    parser.add_argument("--checks", action="store_true")
    args = parser.parse_args()
    result = inspect(args.root)
    if args.checks:
        result["checks"] = [
            run(args.root, [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"]),
            run(args.root, [sys.executable, "scripts/check_docs.py"]),
        ]
    print(json.dumps(result, indent=2))
    if any(item["exit_code"] != 0 for item in result.get("checks", [])):
        raise SystemExit(1)
