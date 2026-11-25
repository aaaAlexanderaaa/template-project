# Role: Removes template-project-only content (internal domains, ADRs, designs, example app, internal tests) from a
# copied template checkout, and strips internal `Anchors:` comments from tool files shipped downstream.
# Out of scope: Writing starter files, syncing versions, or deciding when a checkout counts as copied (init_repo.py).
# Anchors: spec=perspective.server, ADR-004, SRC-020

from __future__ import annotations

import re
import shutil
from pathlib import Path

TEMPLATE_INTERNAL_DOMAINS = ("discipline", "graph-engine", "perspective-ui", "reference-app")
# Decision IDs that belong to template-project itself; extend when the template adds an ADR
# (tests/test_discipline_transfer_and_consistency.py checks this list against docs/decisions/).
TEMPLATE_INTERNAL_ADRS = ("ADR-001", "ADR-002", "ADR-003", "ADR-004", "ADR-005", "ADR-006", "ADR-007")
TEMPLATE_INTERNAL_TESTS = (
    "test_discipline_transfer_and_consistency.py",
    "test_project_cli_and_server.py",
    "test_read_rules_and_onboard.py",
    "test_reference_exemplar.py",
    "test_ssot_and_check_docs.py",
    "test_web_workbench.py",
    "test_chrome_geometry.py",
)


def sanitize_copied_checkout(target: Path) -> None:
    specs_dir = target / "docs" / "specs"
    if specs_dir.is_dir():
        for dom in TEMPLATE_INTERNAL_DOMAINS:
            if (specs_dir / dom).is_dir():
                shutil.rmtree(specs_dir / dom)
        if not any(specs_dir.iterdir()):
            specs_dir.rmdir()
    dec_dir = target / "docs" / "decisions"
    if dec_dir.is_dir():
        for adr in dec_dir.glob("ADR-*.md"):
            if adr.name.startswith(tuple(f"{adr_id}-" for adr_id in TEMPLATE_INTERNAL_ADRS)):
                adr.unlink(missing_ok=True)
        if not any(dec_dir.iterdir()):
            dec_dir.rmdir()
    for folder in ("docs/archive", "docs/evaluations", "archive/legacy-v1"):
        p = target / folder
        if p.is_dir():
            shutil.rmtree(p)
    arch_readme = target / "archive" / "README.md"
    if arch_readme.is_file() and "legacy-v1" in arch_readme.read_text(encoding="utf-8", errors="ignore"):
        arch_readme.unlink(missing_ok=True)
    if (target / "archive").is_dir() and not any((target / "archive").iterdir()):
        (target / "archive").rmdir()
    design_dir = target / "docs" / "design"
    if design_dir.is_dir():
        for df in ("perspective-web.md", "frontend-design-options.html"):
            (design_dir / df).unlink(missing_ok=True)
        des_readme = design_dir / "README.md"
        if des_readme.is_file() and "perspective-web.md" in des_readme.read_text(encoding="utf-8", errors="ignore"):
            des_readme.unlink(missing_ok=True)
        if not any(design_dir.iterdir()):
            design_dir.rmdir()
    ex_app = target / "examples" / "reference-app"
    if any((ex_app / p).is_file() for p in ("features/checkout/service.py", "domain/order_ledger.py", "src/checkout.py")):
        shutil.rmtree(ex_app)
        if (target / "examples").is_dir() and not any((target / "examples").iterdir()):
            (target / "examples").rmdir()
    tests_dir = target / "tests"
    if tests_dir.is_dir():
        for tf in TEMPLATE_INTERNAL_TESTS:
            (tests_dir / tf).unlink(missing_ok=True)
        t_readme = tests_dir / "README.md"
        if t_readme.is_file() and "test_reference_exemplar.py" in t_readme.read_text(encoding="utf-8", errors="ignore"):
            t_readme.unlink(missing_ok=True)
        if not any(tests_dir.iterdir()):
            tests_dir.rmdir()
    src_readme = target / "src" / "README.md"
    if src_readme.is_file() and "template-project" in src_readme.read_text(encoding="utf-8", errors="ignore"):
        src_readme.unlink(missing_ok=True)
        if (target / "src").is_dir() and not any((target / "src").iterdir()):
            (target / "src").rmdir()
    for rel in ("README_CN.md", "tmp/project-state.json"):
        (target / rel).unlink(missing_ok=True)


def strip_internal_anchors(text: str, suffix: str) -> str:
    if suffix == ".css":
        return re.sub(r"\n\s*\*\s*Anchors:.*?\*/", " */", text)
    if suffix == ".html":
        return re.sub(r"^\s*<!--\s*Anchors:.*?-->\r?\n?", "", text, flags=re.MULTILINE)
    return re.sub(r"^\s*(?:#|//)\s*Anchors:.*\r?\n?", "", text, flags=re.MULTILINE)
