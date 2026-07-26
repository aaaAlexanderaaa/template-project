#!/usr/bin/env python3
"""Validate the template's documentation lifecycle and local links.

The check is intentionally dependency-free. It validates document routing and
metadata; it does not pretend to prove that prose is semantically correct.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
TEMPLATES = ROOT / "templates"

VALID_DOC_TYPES = {
    "authority-map",
    "contract",
    "surface-contract",
    "plan",
    "issue-tracker",
    "guide",
    "evidence",
}
VALID_STATUSES = {
    "current",
    "target",
    "active",
    "completed",
    "historical",
    "superseded",
    "needs_reconciliation",
}
VALID_AUTHORITIES = {"normative", "planning", "guidance", "evidence"}
VALID_IMPLEMENTATIONS = {
    "not_started",
    "in_progress",
    "partial",
    "implemented",
    "retired",
}
VALID_VERIFICATIONS = {"pending", "partial", "enforced", "not_applicable"}
VALID_SCOPES = {"current-ui", "future-ui", "historical-ui"}

LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
PLACEHOLDER_RE = re.compile(r"\{\{[^}]+\}\}")


@dataclass
class Finding:
    path: Path
    messages: list[str] = field(default_factory=list)

    def add(self, message: str) -> None:
        self.messages.append(message)


def relative(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def parse_frontmatter(path: Path) -> tuple[dict[str, str], str | None]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}, "missing frontmatter"
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}, "unterminated frontmatter"

    metadata: dict[str, str] = {}
    for line in text[4:end].splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if ":" not in stripped:
            return metadata, f"invalid frontmatter line: {stripped}"
        key, value = stripped.split(":", 1)
        metadata[key.strip()] = value.strip().strip("\"'")
    return metadata, None


def validate_metadata(path: Path) -> Finding:
    finding = Finding(path)
    metadata, error = parse_frontmatter(path)
    if error:
        finding.add(error)
        return finding

    for key in ("doc_type", "status", "authority", "last_reconciled"):
        if not metadata.get(key):
            finding.add(f"missing required metadata: {key}")

    doc_type = metadata.get("doc_type", "")
    status = metadata.get("status", "")
    authority = metadata.get("authority", "")
    implementation = metadata.get("implementation", "")
    verification = metadata.get("verification_status", "")

    if doc_type and doc_type not in VALID_DOC_TYPES:
        finding.add(f"invalid doc_type: {doc_type}")
    if status and status not in VALID_STATUSES:
        finding.add(f"invalid status: {status}")
    if authority and authority not in VALID_AUTHORITIES:
        finding.add(f"invalid authority: {authority}")

    reconciled = metadata.get("last_reconciled", "")
    if reconciled:
        try:
            date.fromisoformat(reconciled)
        except ValueError:
            finding.add(f"last_reconciled must be YYYY-MM-DD: {reconciled}")

    if status == "superseded" and not metadata.get("superseded_by"):
        finding.add("status superseded requires superseded_by")

    if PLACEHOLDER_RE.search(path.read_text(encoding="utf-8")):
        finding.add("unresolved {{placeholder}} in canonical documentation")

    if path == DOCS / "README.md":
        if doc_type != "authority-map" or authority != "normative":
            finding.add(
                "docs/README.md requires doc_type: authority-map and "
                "authority: normative"
            )
        if status != "current":
            finding.add("docs/README.md must remain status: current")

    if path.is_relative_to(DOCS / "contracts"):
        if doc_type != "contract":
            finding.add("docs/contracts/*.md must use doc_type: contract")
        if authority != "normative":
            finding.add("contracts must use authority: normative")
        if not implementation:
            finding.add("contract missing implementation status")
        elif implementation not in VALID_IMPLEMENTATIONS:
            finding.add(f"invalid implementation: {implementation}")
        if not verification:
            finding.add("contract missing verification_status")
        elif verification not in VALID_VERIFICATIONS:
            finding.add(f"invalid verification_status: {verification}")
        if status == "current" and implementation == "not_started":
            finding.add("current contract cannot be implementation: not_started")
        if status == "target" and implementation == "implemented":
            finding.add("target contract cannot claim implementation: implemented")

    if path.is_relative_to(DOCS / "design"):
        if doc_type != "surface-contract":
            finding.add("docs/design/*.md must use doc_type: surface-contract")
        if authority != "normative":
            finding.add("surface contracts must use authority: normative")
        for key in ("surface", "implementation", "contract_scope", "verification_status"):
            if not metadata.get(key):
                finding.add(f"surface contract missing metadata: {key}")
        scope = metadata.get("contract_scope", "")
        if scope and scope not in VALID_SCOPES:
            finding.add(f"invalid contract_scope: {scope}")
        if status == "current" and scope != "current-ui":
            finding.add("current surface contract requires contract_scope: current-ui")
        if status == "target" and scope != "future-ui":
            finding.add("target surface contract requires contract_scope: future-ui")

    if path.is_relative_to(DOCS / "plans"):
        if doc_type != "plan" or authority != "planning":
            finding.add("plans require doc_type: plan and authority: planning")
        if status == "current":
            finding.add("plans cannot be current; land behavior in a contract")

    if path.is_relative_to(DOCS / "issues"):
        if doc_type != "issue-tracker" or authority != "normative":
            finding.add(
                "issues require doc_type: issue-tracker and authority: normative"
            )

    if path.is_relative_to(DOCS / "guides"):
        if doc_type != "guide" or authority != "guidance":
            finding.add("guides require doc_type: guide and authority: guidance")

    if path.is_relative_to(DOCS / "evidence"):
        if doc_type != "evidence" or authority != "evidence":
            finding.add("evidence requires doc_type: evidence and authority: evidence")

    return finding


def canonical_documents() -> list[Path]:
    return [
        path
        for path in sorted(DOCS.rglob("*.md"))
        if (path == DOCS / "README.md" or path.name != "README.md")
        and not path.is_relative_to(TEMPLATES)
    ]


def validate_docs_layout() -> list[Finding]:
    findings: list[Finding] = []
    for path in sorted(DOCS.glob("*.md")):
        if path.name != "README.md":
            finding = Finding(path)
            finding.add(
                "docs root may contain only README.md; route the document to "
                "contracts/, design/, plans/, issues/, guides/, or evidence/"
            )
            findings.append(finding)
    return findings


def validate_local_links() -> list[Finding]:
    findings: list[Finding] = []
    markdown_files = [
        path
        for path in sorted(ROOT.rglob("*.md"))
        if ".git" not in path.parts and not path.is_relative_to(TEMPLATES)
    ]
    for path in markdown_files:
        text = path.read_text(encoding="utf-8")
        missing: list[str] = []
        for raw_target in LINK_RE.findall(text):
            target = raw_target.strip().split(maxsplit=1)[0].strip("<>")
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target_path = unquote(target.split("#", 1)[0])
            if not target_path:
                continue
            resolved = (path.parent / target_path).resolve()
            if not resolved.exists():
                missing.append(target)
        if missing:
            finding = Finding(path)
            for target in sorted(set(missing)):
                finding.add(f"broken local Markdown link: {target}")
            findings.append(finding)
    return findings


def validate_adoption_gate() -> list[Finding]:
    """Prevent product code from arriving while architecture is still a prompt."""

    source_dir = ROOT / "src"
    product_files = [
        path
        for path in source_dir.rglob("*")
        if path.is_file() and path.name not in {"README.md", ".gitkeep"}
    ]
    if not product_files:
        return []

    findings: list[Finding] = []
    architecture = ROOT / "ARCHITECTURE.md"
    architecture_text = architecture.read_text(encoding="utf-8")
    if "Template status:" in architecture_text or "[name]" in architecture_text:
        finding = Finding(architecture)
        finding.add("product source exists but ARCHITECTURE.md is still the template")
        findings.append(finding)

    product_contracts = [
        path
        for path in canonical_documents()
        if path.parent == DOCS / "contracts"
        and path.name != "development-discipline.md"
    ]
    if not product_contracts:
        finding = Finding(source_dir)
        finding.add(
            "product source exists without a product contract under docs/contracts/"
        )
        findings.append(finding)
    return findings


def main() -> int:
    findings: list[Finding] = []
    findings.extend(validate_docs_layout())
    findings.extend(validate_metadata(path) for path in canonical_documents())
    findings.extend(validate_local_links())
    findings.extend(validate_adoption_gate())

    failures = [finding for finding in findings if finding.messages]
    if failures:
        print(f"check_docs: {len(failures)} file(s) need attention")
        for finding in failures:
            print(f"\n{relative(finding.path)}")
            for message in finding.messages:
                print(f"  - {message}")
        return 1

    print(
        "check_docs: OK — "
        f"{len(canonical_documents())} canonical document(s), local links valid"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
