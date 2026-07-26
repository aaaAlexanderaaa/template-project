#!/usr/bin/env python3
"""Validate documentation governance for the discipline template.

The checker is dependency-free on Python 3.11+. It validates declared syntax
and relationships; it does not judge whether product prose is semantically
correct.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from collections import defaultdict
from collections.abc import Iterable, Iterator, Sequence
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from fnmatch import fnmatch
from pathlib import Path
from typing import Any
from urllib.parse import unquote

MINIMUM_PYTHON = (3, 11)


def require_supported_python(version_info: Sequence[int] = sys.version_info) -> None:
    """Fail with an actionable message before any 3.11-only import is attempted."""

    if tuple(version_info[:2]) >= MINIMUM_PYTHON:
        return
    required = ".".join(str(part) for part in MINIMUM_PYTHON)
    current = ".".join(str(part) for part in version_info[:2])
    raise SystemExit(
        f"check_docs requires Python {required} or newer; "
        f"current runtime is {current}. "
        f"Select a Python {required}+ interpreter and rerun the command."
    )


require_supported_python()

import tomllib

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
VALID_PROMISE_STATUSES = {"open", "resolved", "cancelled"}
VALID_ABNORMALITY_STATES = {"pending", "active", "retired"}
VALID_ABNORMALITY_RESULTS = {"pass", "fail", "not_run"}
VALID_CONTRACT_ROLES = {"product", "governance"}

# Declaration manifests share one lifecycle vocabulary so an adopter learns it
# once: shipped-but-unfilled, in force, or deliberately not applicable.
VALID_MANIFEST_STATUSES = {"template", "configured", "not_applicable"}

# Keys the optional style-ownership manifest reads. Validated for the same
# reason `[adoption]` is: a configuration surface where a typo is a silent
# no-op is worse than no configuration surface.
KNOWN_STYLE_KEYS = {
    "version",
    "status",
    "rationale",
    "scan",
    "scan_exclude",
    "layers",
    "tiers",
}

ERROR = "error"
ADVISORY = "advisory"
OFF = "off"
VALID_SEVERITIES = {ERROR, ADVISORY, OFF}

# Adoption stages come from docs/contracts/project-adoption.md. Early stages are
# source-preserving: the harness reports adoption gaps without blocking work.
ADOPTION_STAGES = ("observed", "baselined", "scoped_enforcement", "adopted")
ADVISORY_ADOPTION_STAGES = {"observed", "baselined"}

# Rules whose severity a project may retune in `[severity]`. Everything not
# listed here is a structural error: the repository contradicts itself.
CONFIGURABLE_RULES = {
    # A calendar date passed. Nothing in the repository changed.
    "target_aging": ADVISORY,
    "overdue_promise": ADVISORY,
    "pending_abnormality_aging": ADVISORY,
    # Product code exists but the adoption artifacts are incomplete. Blocking
    # from `scoped_enforcement` onward; reported only before that.
    "adoption_gate": ERROR,
    # Product code exists outside every configured source root, so the adoption
    # gates above would silently evaluate against nothing.
    "source_root_configuration": ERROR,
    # Documentation still references a known template that the selected profile
    # does not require and the project has deleted.
    "trimmed_template_link": ADVISORY,
}

# Rules that describe unfinished adoption rather than a contradiction. Before
# the owner has committed to enforcement they are reported, not blocking: an
# adopter must be able to put the check into CI on the first day.
STAGE_SENSITIVE_RULES = {"adoption_gate", "source_root_configuration"}

# `[adoption]` keys the checker reads. Anything else is a typo or a key from an
# earlier revision that now silently does nothing.
KNOWN_ADOPTION_KEYS = {
    "stage",
    "source_roots",
    "placeholder_names",
    "harness_paths",
    "managed_paths",
    "minimum_live_contracts",
    "source_suffixes",
}

# Retired keys, mapped to what replaced them, so an upgrading adopter is told
# how to migrate rather than losing the setting without a word.
RETIRED_ADOPTION_KEYS = {
    "governance_contracts": (
        "mark those contracts with `contract_role: governance` in their own "
        "frontmatter instead"
    ),
}

# Never product code, at any depth, in any layout.
IGNORED_DIRECTORY_NAMES = {
    ".git",
    ".hg",
    ".svn",
    ".idea",
    ".vscode",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".tox",
    ".venv",
    "__pycache__",
    "node_modules",
    "venv",
    "vendor",
}

# Governance surface of the template itself, relative to the repository root.
GOVERNANCE_PATHS = ("docs", "templates", "archive", "tmp")

DEFAULT_SOURCE_SUFFIXES = (
    ".c",
    ".cc",
    ".cpp",
    ".cs",
    ".css",
    ".dart",
    ".ex",
    ".exs",
    ".go",
    ".h",
    ".hpp",
    ".java",
    ".js",
    ".jsx",
    ".kt",
    ".m",
    ".mjs",
    ".php",
    ".py",
    ".rb",
    ".rs",
    ".scala",
    ".sql",
    ".svelte",
    ".swift",
    ".ts",
    ".tsx",
    ".vue",
)

LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
PLACEHOLDER_RE = re.compile(r"\{\{[^}]+\}\}")
H2_RE = re.compile(r"^##\s+(.+?)\s*$")
H3_RE = re.compile(r"^###\s+(.+?)\s*$")
HEADING_RE = re.compile(r"^#{2,6}\s+(.+?)\s*$")
RAW_HEADING_RE = re.compile(r"^#{3,4}\s+raw\[(\d+)\]")
RAW_DEFINITION_RE = re.compile(
    r"^#{3,4}\s+raw\[(\d+)\]\s*[—–-]\s*(\d{4}-\d{2}-\d{2})\s*$"
)
SOURCE_HEADING_RE = re.compile(r"^#{3,4}\s+source\[(\d+)\]")
SOURCE_DEFINITION_RE = re.compile(
    r"^#{3,4}\s+source\[(\d+)\]\s*[—–-]\s*(\d{4}-\d{2}-\d{2})\s*$"
)
FROM_RE = re.compile(r"^\s*-\s*from:\s*(.+?)\s*$", re.IGNORECASE)
RAW_REF_RE = re.compile(r"raw\[(\d+)\]")
SOURCE_REF_RE = re.compile(r"source\[(\d+)\]")
PROMISE_RE = re.compile(r"^\s*-\s*promise\[([a-z0-9][a-z0-9-]*)\]:\s*(.+?)\s*$")
ABNORMALITY_RE = re.compile(r"^\s*-\s*abnormality\[([a-z0-9][a-z0-9-]*)\]:\s*(.+?)\s*$")


@dataclass(frozen=True)
class DocRecord:
    path: Path
    metadata: dict[str, str]
    text: str


@dataclass(frozen=True)
class Finding:
    path: Path
    message: str
    severity: str
    rule: str | None


def path_matches(relative: str, patterns: Iterable[str]) -> bool:
    """Match a repository-relative POSIX path against globs or directory prefixes.

    Matching uses `fnmatch`, which does not treat `/` specially, so `*` spans
    directory separators exactly as `**` does: `src/billing/*` also matches
    `src/billing/deep/nested/a.py`. Both places that consume this — managed
    scope and harness exemptions — only ever widen what is skipped, so the
    permissive reading is the safe one.
    """

    for raw in patterns:
        pattern = str(raw).strip().strip("/")
        if not pattern:
            continue
        if relative == pattern or relative.startswith(f"{pattern}/"):
            return True
        if fnmatch(relative, pattern):
            return True
    return False


def iter_files(directory: Path) -> Iterator[Path]:
    """Yield files under `directory`, pruning tool and dependency trees.

    Pruning during the walk rather than filtering afterwards keeps the cost
    proportional to the project instead of to its vendored dependencies.
    """

    for current, directory_names, file_names in os.walk(directory):
        directory_names[:] = sorted(
            name for name in directory_names if name not in IGNORED_DIRECTORY_NAMES
        )
        base = Path(current)
        for name in sorted(file_names):
            yield base / name


def parse_frontmatter_text(text: str) -> tuple[dict[str, str], str | None]:
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


def parse_record_fields(payload: str) -> tuple[dict[str, str], list[str]]:
    fields: dict[str, str] = {}
    errors: list[str] = []
    for item in payload.split(";"):
        stripped = item.strip()
        if not stripped:
            continue
        if "=" not in stripped:
            errors.append(f"record item lacks '=': {stripped}")
            continue
        key, value = stripped.split("=", 1)
        key = key.strip()
        value = value.strip()
        if not key or not value:
            errors.append(f"record item has empty key/value: {stripped}")
        elif key in fields:
            errors.append(f"duplicate record field: {key}")
        else:
            fields[key] = value
    return fields, errors


def normalized_heading(value: str) -> str:
    value = re.sub(r"[`*_~]", "", value.strip())
    return re.sub(r"\s+", " ", value).lower()


def heading_inventory(text: str) -> set[str]:
    headings: set[str] = set()
    for line in text.splitlines():
        if match := HEADING_RE.match(line):
            headings.add(normalized_heading(match.group(1)))
    return headings


def section_bounds(lines: list[str], heading: str) -> tuple[int, int] | None:
    wanted = normalized_heading(heading)
    start: int | None = None
    for index, line in enumerate(lines):
        match = H2_RE.match(line)
        if not match:
            continue
        current = normalized_heading(match.group(1))
        if start is None and current == wanted:
            start = index
            continue
        if start is not None:
            return start, index
    if start is None:
        return None
    return start, len(lines)


def h3_subsections(
    lines: list[str], start: int, end: int
) -> list[tuple[str, int, int]]:
    """Return title/start/end bounds for level-three subsections in a range."""

    starts: list[tuple[str, int]] = []
    for index in range(start, end):
        if match := H3_RE.match(lines[index]):
            starts.append((match.group(1).strip(), index))
    return [
        (
            title,
            subsection_start,
            starts[offset + 1][1] if offset + 1 < len(starts) else end,
        )
        for offset, (title, subsection_start) in enumerate(starts)
    ]


def relation_values(raw: str) -> list[str]:
    value = raw.strip()
    if not value or value == "[]":
        return []
    if value.startswith("[") and value.endswith("]"):
        value = value[1:-1]
        return [part.strip().strip("\"'") for part in value.split(",") if part.strip()]
    return [value]


class DocumentationChecker:
    def __init__(self, root: Path, today: date, strict: bool = False):
        self.root = root.resolve()
        self.docs = self.root / "docs"
        self.templates = self.root / "templates"
        self.today = today
        self.strict = strict
        self.findings: list[Finding] = []
        self.policy: dict[str, Any] = {}
        self.records: list[DocRecord] = []
        self.metadata_by_path: dict[Path, dict[str, str]] = {}
        self.abnormalities: dict[str, Path] = {}
        self.required_templates: list[str] = []

    def add(self, path: Path, message: str, rule: str | None = None) -> None:
        severity = self.severity_for(rule)
        if severity == OFF:
            return
        self.findings.append(Finding(path, message, severity, rule))

    @property
    def errors(self) -> list[Finding]:
        return [finding for finding in self.findings if finding.severity == ERROR]

    @property
    def advisories(self) -> list[Finding]:
        return [finding for finding in self.findings if finding.severity == ADVISORY]

    @property
    def stage(self) -> str:
        stage = str(self.policy.get("adoption", {}).get("stage", "adopted")).strip()
        return stage if stage in ADOPTION_STAGES else "adopted"

    def severity_for(self, rule: str | None) -> str:
        """Resolve a rule's severity from stage defaults and `[severity]` policy."""

        if rule is None:
            return ERROR
        default = CONFIGURABLE_RULES.get(rule, ERROR)
        if rule in STAGE_SENSITIVE_RULES and self.stage in ADVISORY_ADOPTION_STAGES:
            default = ADVISORY
        configured = self.policy.get("severity", {}).get(rule)
        severity = str(configured) if configured is not None else default
        if severity not in VALID_SEVERITIES:
            severity = default
        # `off` is a decision the project made; a scheduled strict run reports
        # harder, it does not overturn a rule the owner switched off.
        if self.strict and severity == ADVISORY:
            return ERROR
        return severity

    def validate_policy_shape(self) -> None:
        policy_path = self.root / "docs-policy.toml"
        adoption = self.policy.get("adoption", {})
        declared_stage = adoption.get("stage")
        if declared_stage is not None and str(declared_stage) not in ADOPTION_STAGES:
            self.add(
                policy_path,
                f"[adoption].stage must be one of {', '.join(ADOPTION_STAGES)}: "
                f"{declared_stage}",
            )
        for key in adoption:
            if key in KNOWN_ADOPTION_KEYS:
                continue
            if replacement := RETIRED_ADOPTION_KEYS.get(key):
                self.add(
                    policy_path,
                    f"[adoption].{key} is no longer read; {replacement}, then "
                    "delete the key",
                )
            else:
                self.add(
                    policy_path,
                    f"[adoption].{key} is not a recognised key; known keys are "
                    f"{', '.join(sorted(KNOWN_ADOPTION_KEYS))}",
                )
        for rule, severity in self.policy.get("severity", {}).items():
            if rule not in CONFIGURABLE_RULES:
                self.add(
                    policy_path,
                    f"[severity].{rule} is not a configurable rule; known rules are "
                    f"{', '.join(sorted(CONFIGURABLE_RULES))}",
                )
            elif str(severity) not in VALID_SEVERITIES:
                self.add(
                    policy_path,
                    f"[severity].{rule} must be error, advisory, or off: {severity}",
                )

    def display_path(self, path: Path) -> str:
        try:
            return str(path.relative_to(self.root))
        except ValueError:
            return str(path)

    def load_toml(self, path: Path, label: str) -> dict[str, Any]:
        if not path.exists():
            self.add(path, f"missing required {label}")
            return {}
        try:
            with path.open("rb") as handle:
                data = tomllib.load(handle)
        except (OSError, tomllib.TOMLDecodeError) as exc:
            self.add(path, f"invalid {label}: {exc}")
            return {}
        if data.get("version") != 1:
            self.add(path, f"{label} requires version = 1")
        return data

    def canonical_paths(self) -> list[Path]:
        if not self.docs.exists():
            return []
        return [
            path
            for path in sorted(self.docs.rglob("*.md"))
            if path == self.docs / "README.md" or path.name != "README.md"
        ]

    def load_records(self) -> None:
        if not self.docs.exists():
            self.add(self.docs, "missing docs directory")
            return
        for path in self.canonical_paths():
            text = path.read_text(encoding="utf-8")
            metadata, error = parse_frontmatter_text(text)
            if error:
                self.add(path, error)
            record = DocRecord(path, metadata, text)
            self.records.append(record)
            self.metadata_by_path[path.resolve()] = metadata

    def parse_iso_date(self, path: Path, field: str, value: str) -> date | None:
        try:
            return date.fromisoformat(value)
        except ValueError:
            self.add(path, f"{field} must be YYYY-MM-DD: {value}")
            return None

    def validate_docs_layout(self) -> None:
        if not self.docs.exists():
            return
        for path in sorted(self.docs.glob("*.md")):
            if path.name != "README.md":
                self.add(
                    path,
                    "docs root may contain only README.md; route the document "
                    "to contracts/, design/, plans/, issues/, guides/, or evidence/",
                )

    def validate_metadata(self, record: DocRecord) -> None:
        path = record.path
        metadata = record.metadata
        for key in ("doc_type", "status", "authority", "last_reconciled"):
            if not metadata.get(key):
                self.add(path, f"missing required metadata: {key}")

        doc_type = metadata.get("doc_type", "")
        status = metadata.get("status", "")
        authority = metadata.get("authority", "")
        implementation = metadata.get("implementation", "")
        verification = metadata.get("verification_status", "")

        if doc_type and doc_type not in VALID_DOC_TYPES:
            self.add(path, f"invalid doc_type: {doc_type}")
        if status and status not in VALID_STATUSES:
            self.add(path, f"invalid status: {status}")
        if authority and authority not in VALID_AUTHORITIES:
            self.add(path, f"invalid authority: {authority}")

        reconciled: date | None = None
        if value := metadata.get("last_reconciled"):
            reconciled = self.parse_iso_date(path, "last_reconciled", value)
        tolerance = int(
            self.policy.get("aging", {}).get("future_date_tolerance_days", 0)
        )
        if reconciled and reconciled > self.today + timedelta(days=tolerance):
            self.add(path, f"last_reconciled is in the future: {reconciled}")

        if value := metadata.get("review_due"):
            self.parse_iso_date(path, "review_due", value)

        if status == "superseded" and not metadata.get("superseded_by"):
            self.add(path, "status superseded requires superseded_by")

        if PLACEHOLDER_RE.search(record.text):
            self.add(path, "unresolved {{placeholder}} in canonical documentation")

        if path == self.docs / "README.md":
            if doc_type != "authority-map" or authority != "normative":
                self.add(
                    path,
                    "docs/README.md requires doc_type: authority-map and "
                    "authority: normative",
                )
            if status != "current":
                self.add(path, "docs/README.md must remain status: current")

        if path.is_relative_to(self.docs / "contracts"):
            if doc_type != "contract" or authority != "normative":
                self.add(
                    path,
                    "contracts require doc_type: contract and authority: normative",
                )
            role = metadata.get("contract_role", "product")
            if role not in VALID_CONTRACT_ROLES:
                self.add(
                    path,
                    f"contract_role must be product or governance: {role}",
                )
            self.validate_contract_lifecycle(path, status, implementation, verification)

        if path.is_relative_to(self.docs / "design"):
            if doc_type != "surface-contract" or authority != "normative":
                self.add(
                    path,
                    "surface docs require doc_type: surface-contract and authority: normative",
                )
            for key in (
                "surface",
                "implementation",
                "contract_scope",
                "verification_status",
            ):
                if not metadata.get(key):
                    self.add(path, f"surface contract missing metadata: {key}")
            if implementation and implementation not in VALID_IMPLEMENTATIONS:
                self.add(path, f"invalid implementation: {implementation}")
            if verification and verification not in VALID_VERIFICATIONS:
                self.add(path, f"invalid verification_status: {verification}")
            scope = metadata.get("contract_scope", "")
            if scope and scope not in VALID_SCOPES:
                self.add(path, f"invalid contract_scope: {scope}")
            if status == "current" and scope != "current-ui":
                self.add(path, "current surface requires contract_scope: current-ui")
            if status == "target" and scope != "future-ui":
                self.add(path, "target surface requires contract_scope: future-ui")
            if status == "current" and implementation == "not_started":
                self.add(path, "current surface cannot be implementation: not_started")
            if status == "target" and implementation == "implemented":
                self.add(
                    path, "target surface cannot claim implementation: implemented"
                )

        if path.is_relative_to(self.docs / "plans"):
            if doc_type != "plan" or authority != "planning":
                self.add(path, "plans require doc_type: plan and authority: planning")
            if status == "current":
                self.add(path, "plans cannot be current; land behavior in a contract")
            if not metadata.get("implements"):
                self.add(path, "plans require an implements relationship to a contract")

        if path.is_relative_to(self.docs / "issues") and (
            doc_type != "issue-tracker" or authority != "normative"
        ):
            self.add(
                path,
                "issues require doc_type: issue-tracker and authority: normative",
            )

        if path.is_relative_to(self.docs / "guides") and (
            doc_type != "guide" or authority != "guidance"
        ):
            self.add(path, "guides require doc_type: guide and authority: guidance")

        if path.is_relative_to(self.docs / "evidence") and (
            doc_type != "evidence" or authority != "evidence"
        ):
            self.add(
                path, "evidence requires doc_type: evidence and authority: evidence"
            )

    def validate_contract_lifecycle(
        self, path: Path, status: str, implementation: str, verification: str
    ) -> None:
        if not implementation:
            self.add(path, "contract missing implementation status")
        elif implementation not in VALID_IMPLEMENTATIONS:
            self.add(path, f"invalid implementation: {implementation}")
        if not verification:
            self.add(path, "contract missing verification_status")
        elif verification not in VALID_VERIFICATIONS:
            self.add(path, f"invalid verification_status: {verification}")
        if status == "current" and implementation == "not_started":
            self.add(path, "current contract cannot be implementation: not_started")
        if status == "target" and implementation == "implemented":
            self.add(path, "target contract cannot claim implementation: implemented")

    def validate_relationships(self, record: DocRecord) -> None:
        for field in ("implements", "supersedes", "superseded_by"):
            for value in relation_values(record.metadata.get(field, "")):
                if PLACEHOLDER_RE.search(value):
                    continue
                target = unquote(value.split("#", 1)[0].strip())
                if not target:
                    continue
                if Path(target).is_absolute():
                    self.add(
                        record.path,
                        f"{field} path must be repository-relative: {value}",
                    )
                    continue
                resolved = (self.root / target).resolve()
                if not resolved.is_relative_to(self.root):
                    self.add(
                        record.path,
                        f"{field} path escapes repository: {value}",
                    )
                elif not resolved.exists():
                    self.add(record.path, f"{field} points to missing path: {value}")

    def validate_target_aging(self, record: DocRecord) -> None:
        metadata = record.metadata
        if metadata.get("status") != "target":
            return
        if metadata.get("doc_type") not in {"contract", "surface-contract"}:
            return

        if due_raw := metadata.get("review_due"):
            deadline = self.parse_iso_date(record.path, "review_due", due_raw)
        else:
            reconciled_raw = metadata.get("last_reconciled", "")
            reconciled = self.parse_iso_date(
                record.path, "last_reconciled", reconciled_raw
            )
            max_age = int(self.policy.get("aging", {}).get("target_max_age_days", 90))
            deadline = reconciled + timedelta(days=max_age) if reconciled else None
        if deadline and self.today > deadline:
            self.add(
                record.path,
                f"target document review overdue since {deadline}; promote, "
                "supersede, mark historical, or reconcile it",
                rule="target_aging",
            )

    def validate_promises(self, record: DocRecord) -> None:
        seen: set[str] = set()
        for lineno, line in enumerate(record.text.splitlines(), start=1):
            match = PROMISE_RE.match(line)
            if not match:
                continue
            promise_id, payload = match.groups()
            if promise_id in seen:
                self.add(record.path, f"line {lineno}: duplicate promise[{promise_id}]")
            seen.add(promise_id)
            fields, errors = parse_record_fields(payload)
            for error in errors:
                self.add(record.path, f"line {lineno}: promise[{promise_id}] {error}")
            required = {"due", "status", "owner", "description"}
            missing = sorted(required - fields.keys())
            if missing:
                self.add(
                    record.path,
                    f"line {lineno}: promise[{promise_id}] missing {', '.join(missing)}",
                )
                continue
            status = fields["status"]
            if status not in VALID_PROMISE_STATUSES:
                self.add(
                    record.path,
                    f"line {lineno}: promise[{promise_id}] invalid status: {status}",
                )
            deadline = self.parse_iso_date(
                record.path, f"promise[{promise_id}].due", fields["due"]
            )
            if deadline and status == "open" and self.today > deadline:
                self.add(
                    record.path,
                    f"line {lineno}: open promise[{promise_id}] overdue since {deadline}",
                    rule="overdue_promise",
                )

    def validate_surface_citations(self, record: DocRecord) -> None:
        if record.metadata.get("doc_type") != "surface-contract":
            return
        lines = record.text.splitlines()
        raw_bounds = section_bounds(lines, "Raw layer")
        translated_bounds = section_bounds(lines, "Translated layer")
        if not raw_bounds:
            self.add(record.path, "surface contract missing ## Raw layer")
            return
        if not translated_bounds:
            self.add(record.path, "surface contract missing ## Translated layer")
            return
        if raw_bounds[0] >= translated_bounds[0]:
            self.add(record.path, "Raw layer must appear before Translated layer")
            return

        definitions = self.collect_anchor_definitions(
            record.path,
            lines[raw_bounds[0] + 1 : raw_bounds[1]],
            raw_bounds[0] + 2,
            "raw",
        )
        citations: set[int] = set()
        subsections = h3_subsections(
            lines, translated_bounds[0] + 1, translated_bounds[1]
        )
        if not subsections:
            self.add(
                record.path,
                "Translated layer must define at least one ### subsection",
            )
        for title, subsection_start, subsection_end in subsections:
            subsection_citations: set[int] = set()
            for index in range(subsection_start + 1, subsection_end):
                match = FROM_RE.match(lines[index])
                if not match:
                    continue
                ids = {int(value) for value in RAW_REF_RE.findall(match.group(1))}
                if not ids:
                    self.add(
                        record.path,
                        f"line {index + 1}: surface `from:` line must cite raw[N]",
                    )
                subsection_citations.update(ids)
            if not subsection_citations:
                self.add(
                    record.path,
                    f"translated subsection lacks raw citation: {title}",
                )
            citations.update(subsection_citations)
        self.compare_anchor_sets(record.path, "raw", definitions, citations)

    def validate_contract_sources(self, record: DocRecord) -> None:
        if record.metadata.get("doc_type") != "contract":
            return
        lines = record.text.splitlines()
        bounds = section_bounds(lines, "Source anchors")
        if not bounds:
            return
        definitions = self.collect_anchor_definitions(
            record.path,
            lines[bounds[0] + 1 : bounds[1]],
            bounds[0] + 2,
            "source",
        )
        citations: set[int] = set()
        for line in lines[bounds[1] :]:
            if match := FROM_RE.match(line):
                citations.update(
                    int(value) for value in SOURCE_REF_RE.findall(match.group(1))
                )
        self.compare_anchor_sets(record.path, "source", definitions, citations)

    def collect_anchor_definitions(
        self,
        path: Path,
        lines: list[str],
        start_lineno: int,
        kind: str,
    ) -> set[int]:
        heading_re = RAW_HEADING_RE if kind == "raw" else SOURCE_HEADING_RE
        definition_re = RAW_DEFINITION_RE if kind == "raw" else SOURCE_DEFINITION_RE
        definitions: set[int] = set()
        for offset, line in enumerate(lines):
            lineno = start_lineno + offset
            if not (heading := heading_re.match(line)):
                continue
            anchor_id = int(heading.group(1))
            definition = definition_re.match(line)
            if not definition:
                self.add(
                    path,
                    f"line {lineno}: {kind}[{anchor_id}] heading requires YYYY-MM-DD",
                )
                continue
            if anchor_id in definitions:
                self.add(path, f"line {lineno}: duplicate {kind}[{anchor_id}]")
            definitions.add(anchor_id)
            self.parse_iso_date(path, f"{kind}[{anchor_id}] date", definition.group(2))
        if not definitions:
            self.add(
                path, f"{kind} anchor section must define at least one dated anchor"
            )
        return definitions

    def compare_anchor_sets(
        self, path: Path, kind: str, definitions: set[int], citations: set[int]
    ) -> None:
        for anchor_id in sorted(citations - definitions):
            self.add(path, f"citation does not resolve: {kind}[{anchor_id}]")
        for anchor_id in sorted(definitions - citations):
            self.add(path, f"{kind}[{anchor_id}] defined but never cited")

    def required_template_files(self) -> list[str]:
        """Resolve the template inventory for the project's declared profile.

        Tiers are cumulative in `tier_order`, so a small project selects
        `minimal` and never carries ceremony it will not fill in. An explicit
        `required_files` list overrides the profile entirely.
        """

        config = self.policy.get("templates", {})
        policy_path = self.root / "docs-policy.toml"
        if explicit := config.get("required_files"):
            return [str(name) for name in explicit]

        order = [str(tier) for tier in config.get("tier_order", [])]
        tiers = config.get("tiers", {})
        profile = str(config.get("profile", "")).strip()
        if not order or not tiers:
            self.add(
                policy_path,
                "[templates] needs either required_files or tier_order plus "
                "[templates.tiers]",
            )
            return []
        if profile not in order:
            self.add(
                policy_path,
                f"[templates].profile must be one of {', '.join(order)}: "
                f"{profile or '(unset)'}",
            )
            return []
        for tier in order:
            if tier not in tiers:
                self.add(policy_path, f"[templates.tiers] is missing tier: {tier}")

        selected: list[str] = []
        for tier in order[: order.index(profile) + 1]:
            for name in tiers.get(tier, []):
                if str(name) not in selected:
                    selected.append(str(name))
        return selected

    def validate_templates(self) -> None:
        config = self.policy.get("templates", {})
        required_files = self.required_templates
        required_sections = config.get("required_sections", {})
        expected_types = config.get("doc_types", {})
        for filename in required_files:
            path = self.templates / filename
            if not path.exists():
                self.add(path, "required template is missing")
                continue
            text = path.read_text(encoding="utf-8")
            metadata, error = parse_frontmatter_text(text)
            if error:
                self.add(path, error)
                continue
            for key in ("doc_type", "status", "authority", "last_reconciled"):
                if not metadata.get(key):
                    self.add(path, f"template missing metadata: {key}")
            expected_type = expected_types.get(filename)
            if not expected_type:
                self.add(
                    path,
                    "required template has no declared doc_type in "
                    "[templates.doc_types]",
                )
            elif metadata.get("doc_type") != expected_type:
                self.add(
                    path,
                    f"template doc_type must be {expected_type}: {metadata.get('doc_type')}",
                )
            if not PLACEHOLDER_RE.search(text):
                self.add(path, "template contains no {{placeholder}} values")
            headings = heading_inventory(text)
            for section in required_sections.get(filename, []):
                if normalized_heading(section) not in headings:
                    self.add(path, f"template missing required section: {section}")

            if filename == "frontend-surface.md":
                if "### raw[1] — {{YYYY-MM-DD}}" not in text:
                    self.add(path, "surface template missing dated raw[1] example")
                if "- from: raw[{{N}}]" not in text:
                    self.add(
                        path, "surface template missing standard raw citation example"
                    )
                if "- abnormality[{{stable-slug}}]:" not in text:
                    self.add(
                        path, "surface template missing abnormality record example"
                    )
                lines = text.splitlines()
                translated_bounds = section_bounds(lines, "Translated layer")
                if not translated_bounds:
                    self.add(path, "surface template missing Translated layer")
                else:
                    subsections = h3_subsections(
                        lines,
                        translated_bounds[0] + 1,
                        translated_bounds[1],
                    )
                    if not subsections:
                        self.add(
                            path,
                            "surface template Translated layer needs a ### subsection",
                        )
                    for title, subsection_start, subsection_end in subsections:
                        has_citation = any(
                            (match := FROM_RE.match(lines[index]))
                            and "raw[{{N}}]" in match.group(1)
                            for index in range(subsection_start + 1, subsection_end)
                        )
                        if not has_citation:
                            self.add(
                                path,
                                "surface template translated subsection lacks raw "
                                f"citation: {title}",
                            )
            if normalized_heading("Source anchors") in headings:
                if "### source[1] — {{YYYY-MM-DD}}" not in text:
                    self.add(path, "source template missing dated source[1] example")
                if "- from: source[{{N}}]" not in text:
                    self.add(
                        path, "source template missing standard source citation example"
                    )
            if filename == "contract.md":
                promise_lines = [
                    line for line in text.splitlines() if line.startswith("- promise[")
                ]
                required_parts = (
                    "promise[{{stable-id}}]",
                    "due={{YYYY-MM-DD}}",
                    "status=open",
                    "owner={{owner}}",
                    "description={{concrete promised alignment}}",
                )
                if len(promise_lines) != 1 or not all(
                    part in promise_lines[0] for part in required_parts
                ):
                    self.add(
                        path, "contract template missing structured promise example"
                    )
            if (
                filename == "verification-report.md"
                and "- abnormality[{{registered-slug}}]:" not in text
            ):
                self.add(
                    path, "verification template missing abnormality reference example"
                )

    def validate_abnormalities(self) -> None:
        pending_days = int(
            self.policy.get("aging", {}).get("pending_abnormality_max_age_days", 30)
        )
        design_records = [
            record
            for record in self.records
            if record.metadata.get("doc_type") == "surface-contract"
        ]
        for record in design_records:
            lines = record.text.splitlines()
            bounds = section_bounds(lines, "Known abnormality classes")
            if not bounds:
                continue
            found = 0
            for lineno, line in enumerate(
                lines[bounds[0] + 1 : bounds[1]], start=bounds[0] + 2
            ):
                if not (match := ABNORMALITY_RE.match(line)):
                    continue
                found += 1
                slug, payload = match.groups()
                if slug in self.abnormalities:
                    self.add(
                        record.path,
                        f"line {lineno}: duplicate global abnormality[{slug}]",
                    )
                else:
                    self.abnormalities[slug] = record.path
                fields, errors = parse_record_fields(payload)
                for error in errors:
                    self.add(record.path, f"line {lineno}: abnormality[{slug}] {error}")
                required = {"state", "evidence", "guard", "description"}
                missing = sorted(required - fields.keys())
                if missing:
                    self.add(
                        record.path,
                        f"line {lineno}: abnormality[{slug}] missing {', '.join(missing)}",
                    )
                    continue
                state = fields["state"]
                if state not in VALID_ABNORMALITY_STATES:
                    self.add(
                        record.path,
                        f"line {lineno}: abnormality[{slug}] invalid state: {state}",
                    )
                    continue
                self.validate_abnormality_evidence(
                    record.path,
                    lineno,
                    slug,
                    state,
                    fields["evidence"],
                    fields["guard"],
                    pending_days,
                )
            if found == 0:
                self.add(
                    record.path,
                    "Known abnormality classes section must contain a structured "
                    "abnormality[slug] record or be removed",
                )

        for record in self.records:
            if record.metadata.get("doc_type") != "evidence":
                continue
            lines = record.text.splitlines()
            bounds = section_bounds(lines, "Anomalies")
            if not bounds:
                continue
            for lineno, line in enumerate(
                lines[bounds[0] + 1 : bounds[1]], start=bounds[0] + 2
            ):
                if not (match := ABNORMALITY_RE.match(line)):
                    continue
                slug, payload = match.groups()
                if slug not in self.abnormalities:
                    self.add(
                        record.path,
                        f"line {lineno}: abnormality[{slug}] is not registered by a surface",
                    )
                fields, errors = parse_record_fields(payload)
                for error in errors:
                    self.add(record.path, f"line {lineno}: abnormality[{slug}] {error}")
                required = {"result", "evidence", "issue"}
                missing = sorted(required - fields.keys())
                if missing:
                    self.add(
                        record.path,
                        f"line {lineno}: abnormality[{slug}] missing {', '.join(missing)}",
                    )
                elif fields["result"] not in VALID_ABNORMALITY_RESULTS:
                    self.add(
                        record.path,
                        f"line {lineno}: abnormality[{slug}] invalid result: {fields['result']}",
                    )

    def validate_abnormality_evidence(
        self,
        path: Path,
        lineno: int,
        slug: str,
        state: str,
        evidence: str,
        guard: str,
        pending_days: int,
    ) -> None:
        if state == "pending":
            if not evidence.startswith("pending:"):
                self.add(
                    path,
                    f"line {lineno}: pending abnormality[{slug}] requires pending:YYYY-MM-DD evidence",
                )
                return
            pending_date = self.parse_iso_date(
                path, f"abnormality[{slug}] pending date", evidence.split(":", 1)[1]
            )
            if pending_date and self.today > pending_date + timedelta(
                days=pending_days
            ):
                self.add(
                    path,
                    f"line {lineno}: abnormality[{slug}] evidence pending for more than {pending_days} days",
                    rule="pending_abnormality_aging",
                )
            return

        if evidence.startswith("pending:"):
            self.add(
                path,
                f"line {lineno}: {state} abnormality[{slug}] cannot use pending evidence",
            )
        elif evidence.startswith("docs/evidence/"):
            evidence_path = (self.root / evidence).resolve()
            evidence_root = (self.docs / "evidence").resolve()
            if not evidence_path.is_relative_to(evidence_root):
                self.add(
                    path,
                    f"line {lineno}: abnormality[{slug}] evidence path escapes "
                    f"docs/evidence: {evidence}",
                )
            elif not evidence_path.exists():
                self.add(
                    path,
                    f"line {lineno}: abnormality[{slug}] evidence path missing: {evidence}",
                )
        elif evidence.startswith("issue:"):
            issue_id = evidence.split(":", 1)[1]
            issue_text = "\n".join(
                issue.read_text(encoding="utf-8")
                for issue in sorted((self.docs / "issues").glob("*.md"))
                if issue.name != "README.md"
            )
            if issue_id not in issue_text:
                self.add(
                    path,
                    f"line {lineno}: abnormality[{slug}] issue not found: {issue_id}",
                )
        else:
            self.add(
                path,
                f"line {lineno}: abnormality[{slug}] evidence must be docs/evidence/... or issue:<id>",
            )
        if state == "active" and guard in {"pending", "none", "not_applicable"}:
            self.add(
                path,
                f"line {lineno}: active abnormality[{slug}] requires a concrete guard",
            )

    def validate_local_links(self) -> None:
        skip_dirs = {".git", "tmp", "archive"}
        for path in sorted(self.root.rglob("*.md")):
            if any(part in skip_dirs for part in path.relative_to(self.root).parts):
                continue
            text = path.read_text(encoding="utf-8")
            for raw_target in LINK_RE.findall(text):
                target = raw_target.strip()
                if target.startswith("<") and ">" in target:
                    target = target[1 : target.index(">")]
                else:
                    target = target.split(maxsplit=1)[0]
                if target.startswith(("http://", "https://", "mailto:", "#")):
                    continue
                if PLACEHOLDER_RE.search(target):
                    continue
                target_path = unquote(target.split("#", 1)[0])
                if not target_path:
                    continue
                if Path(target_path).is_absolute():
                    self.add(
                        path, f"absolute local Markdown link is not portable: {target}"
                    )
                    continue
                resolved = (path.parent / target_path).resolve()
                if not resolved.is_relative_to(self.root):
                    self.add(
                        path,
                        f"local Markdown link escapes repository: {target}",
                    )
                elif not resolved.exists():
                    self.add(
                        path,
                        f"broken local Markdown link: {target}",
                        rule=self.trimmed_template_rule(resolved),
                    )

    def trimmed_template_rule(self, resolved: Path) -> str | None:
        """Classify a missing link target that a lower profile legitimately drops.

        A project on `minimal` deletes templates it will never fill in. The
        catalogue prose that still mentions them is stale, not broken, so it
        must not fail the build the way a typo does.
        """

        if resolved.parent != self.templates:
            return None
        if resolved.name in self.required_templates:
            return None
        if resolved.name not in self.known_template_files():
            return None
        return "trimmed_template_link"

    def known_template_files(self) -> set[str]:
        config = self.policy.get("templates", {})
        known = {str(name) for name in config.get("required_files", [])}
        for names in config.get("tiers", {}).values():
            known.update(str(name) for name in names)
        known.update(str(name) for name in config.get("doc_types", {}))
        return known

    def source_roots(self) -> list[str]:
        adoption = self.policy.get("adoption", {})
        roots = adoption.get("source_roots", ["src"])
        return [str(root).strip().strip("/") for root in roots if str(root).strip()]

    def product_files(self) -> list[Path]:
        """Files the adoption gates govern, narrowed by stage-managed scope."""

        adoption = self.policy.get("adoption", {})
        placeholders = set(adoption.get("placeholder_names", ["README.md", ".gitkeep"]))
        product: list[Path] = []
        for source_root in self.source_roots():
            directory = self.root / source_root
            if not directory.exists():
                continue
            product.extend(
                path
                for path in iter_files(directory)
                if path.name not in placeholders
            )
        managed = [
            str(pattern)
            for pattern in adoption.get("managed_paths", [])
            if str(pattern).strip()
        ]
        if self.stage == "scoped_enforcement" and managed:
            product = [
                path
                for path in product
                if path_matches(path.relative_to(self.root).as_posix(), managed)
            ]
        return sorted(product)

    def validate_source_root_configuration(self) -> None:
        """Catch code that lives outside every configured root.

        Without this, a repository whose sources are in `app/` or `packages/`
        reports a clean check while every adoption gate silently evaluates
        against an empty file set.

        Files directly in the repository root are exempt. `setup.py`,
        `conftest.py`, `noxfile.py`, `vite.config.ts`, and their equivalents are
        build and tooling configuration in every layout this template targets;
        treating them as unclaimed product code would fail an adopter's very
        first run for something no source root is supposed to own.
        """

        adoption = self.policy.get("adoption", {})
        roots = self.source_roots()
        harness = [
            str(entry).strip().strip("/")
            for entry in adoption.get("harness_paths", [])
            if str(entry).strip()
        ]
        suffixes = {
            str(suffix).lower()
            for suffix in adoption.get("source_suffixes", DEFAULT_SOURCE_SUFFIXES)
        }
        excluded = [*GOVERNANCE_PATHS, *roots, *harness]

        outside: list[str] = []
        for path in iter_files(self.root):
            if path.suffix.lower() not in suffixes:
                continue
            relative = path.relative_to(self.root)
            if len(relative.parts) == 1:
                continue
            posix = relative.as_posix()
            if path_matches(posix, excluded):
                continue
            outside.append(posix)

        if not outside:
            return
        outside.sort()
        sample = ", ".join(outside[:5])
        if len(outside) > 5:
            sample += f", and {len(outside) - 5} more"
        self.add(
            self.root / "docs-policy.toml",
            "source files exist outside every configured source root, so the "
            f"adoption gates check nothing: {sample}. Add the owning directory to "
            "[adoption].source_roots, or — if it is tooling rather than product "
            "code — to [adoption].harness_paths, which accepts directory names "
            "and glob patterns alike",
            rule="source_root_configuration",
        )

    def validate_architecture(self) -> None:
        architecture = self.root / "ARCHITECTURE.md"
        if not architecture.exists():
            self.add(architecture, "missing structural authority template")
            architecture_metadata: dict[str, str] = {}
            architecture_text = ""
        else:
            architecture_text = architecture.read_text(encoding="utf-8")
            architecture_metadata, error = parse_frontmatter_text(architecture_text)
            if error:
                self.add(architecture, error)
            if architecture_metadata.get("document_role") != "structural-authority":
                self.add(architecture, "document_role must be structural-authority")
            if architecture_metadata.get("template_state") not in {
                "unconfigured",
                "configured",
            }:
                self.add(
                    architecture, "template_state must be unconfigured or configured"
                )

        manifest_name = self.policy.get("architecture", {}).get(
            "manifest", "architecture-rules.toml"
        )
        manifest_path = self.root / manifest_name
        manifest = self.load_toml(manifest_path, "architecture fitness manifest")
        manifest_status = manifest.get("status", "")
        if manifest_status not in {"template", "configured", "not_applicable"}:
            self.add(
                manifest_path,
                "architecture manifest status must be template, configured, or not_applicable",
            )

        product = self.product_files()
        self.validate_source_root_configuration()
        if product:
            if architecture_metadata.get("template_state") != "configured":
                self.add(
                    architecture,
                    "product source exists but architecture template_state is not configured",
                    rule="adoption_gate",
                )
            if PLACEHOLDER_RE.search(architecture_text):
                self.add(
                    architecture,
                    "product source exists but ARCHITECTURE.md still has placeholders",
                    rule="adoption_gate",
                )
            if manifest_status == "template":
                self.add(
                    manifest_path,
                    "product source exists but architecture fitness is still template",
                    rule="adoption_gate",
                )
            self.validate_live_product_contracts(product)

        if manifest_status == "configured":
            self.validate_architecture_rules(manifest_path, manifest)
        elif manifest_status == "not_applicable":
            rationale = str(manifest.get("rationale", "")).strip()
            if len(rationale) < 20 or PLACEHOLDER_RE.search(rationale):
                self.add(
                    manifest_path,
                    "not_applicable architecture fitness requires a substantive rationale",
                )

    def validate_live_product_contracts(self, product: list[Path]) -> None:
        adoption = self.policy.get("adoption", {})
        minimum = int(adoption.get("minimum_live_contracts", 1))
        contracts = self.docs / "contracts"
        live = 0
        for record in self.records:
            # Contracts may be grouped into per-domain subdirectories; every
            # other pass reads them recursively, so counting must too.
            if not record.path.is_relative_to(contracts):
                continue
            metadata = record.metadata
            if metadata.get("contract_role", "product") != "product":
                continue
            if metadata.get("status") not in {"current", "target"}:
                continue
            if metadata.get("implementation") not in {
                "in_progress",
                "partial",
                "implemented",
            }:
                continue
            live += 1
        if live < minimum:
            self.add(
                product[0].parent,
                f"product source exists but only {live} live implementation contract(s); "
                f"minimum is {minimum}",
                rule="adoption_gate",
            )

    def resolve_globs(
        self,
        manifest_path: Path,
        label: str,
        includes: Any,
        excludes: Any = (),
    ) -> set[Path]:
        """Resolve repository-contained include/exclude globs to real files.

        Glob safety has one owner. Every manifest that reaches the filesystem
        goes through here, so an escape rejected for one declaration cannot be
        accepted for another.
        """

        matched: set[Path] = set()
        if not isinstance(includes, list):
            self.add(manifest_path, f"{label} include must be a list")
            return matched
        for include in includes:
            if (
                not isinstance(include, str)
                or not include
                or PLACEHOLDER_RE.search(include)
            ):
                self.add(manifest_path, f"{label} has invalid include glob")
                continue
            include_path = Path(include)
            if include_path.is_absolute() or ".." in include_path.parts:
                self.add(
                    manifest_path,
                    f"{label} include glob must stay inside repository: {include}",
                )
                continue
            try:
                for path in self.root.glob(include):
                    if not path.is_file():
                        continue
                    if not path.resolve().is_relative_to(self.root):
                        self.add(
                            manifest_path,
                            f"{label} include glob resolved outside repository: "
                            f"{include}",
                        )
                        continue
                    matched.add(path)
            except (NotImplementedError, ValueError) as exc:
                self.add(
                    manifest_path,
                    f"{label} has invalid include glob {include!r}: {exc}",
                )
        if not isinstance(excludes, list):
            self.add(manifest_path, f"{label} exclude must be a list")
            excludes = []
        valid_excludes: list[str] = []
        for exclude in excludes:
            if (
                not isinstance(exclude, str)
                or not exclude
                or PLACEHOLDER_RE.search(exclude)
                or Path(exclude).is_absolute()
                or ".." in Path(exclude).parts
            ):
                self.add(manifest_path, f"{label} has invalid exclude glob")
                continue
            valid_excludes.append(exclude)
        return {
            path
            for path in matched
            if not any(
                path.relative_to(self.root).match(exclude)
                for exclude in valid_excludes
            )
        }

    def validate_style_ownership(self) -> None:
        """Validate the optional style-ownership declaration.

        The manifest does not ship. A project that owns no style — a service, a
        library, a command-line tool — creates no file and the harness asks
        nothing of it. Everything checked below is path, index, and string
        arithmetic: the checker never parses a stylesheet, computes a
        specificity, or simulates a cascade.
        """

        manifest_path = self.root / "style-ownership.toml"
        if not manifest_path.exists():
            return
        manifest = self.load_toml(manifest_path, "style ownership manifest")
        if not manifest:
            return
        for key in manifest:
            if key not in KNOWN_STYLE_KEYS:
                self.add(
                    manifest_path,
                    f"unknown style manifest key: {key}; known keys are "
                    f"{', '.join(sorted(KNOWN_STYLE_KEYS))}",
                )
        status = str(manifest.get("status", "")).strip()
        if status not in VALID_MANIFEST_STATUSES:
            self.add(
                manifest_path,
                "style manifest status must be template, configured, or "
                f"not_applicable: {status or '(unset)'}",
            )
            return
        if status == "not_applicable":
            rationale = str(manifest.get("rationale", "")).strip()
            if len(rationale) < 20 or PLACEHOLDER_RE.search(rationale):
                self.add(
                    manifest_path,
                    "not_applicable style ownership requires a substantive rationale",
                )
            return
        if status == "template":
            return
        self.validate_style_layers(manifest_path, manifest)
        self.validate_style_tiers(manifest_path, manifest)

    def validate_style_layers(
        self, manifest_path: Path, manifest: dict[str, Any]
    ) -> None:
        """Every declared corpus file resolves to exactly one declared layer.

        This is the mechanical form of "precedence is declared, not emergent".
        A file claimed by no layer is the failure that matters: where the
        realizing mechanism gives unlayered style the highest authority, an
        omission escalates rather than defaults.
        """

        layers = manifest.get("layers", [])
        if not isinstance(layers, list) or not layers:
            self.add(
                manifest_path, "configured style manifest needs at least one layer"
            )
            return
        corpus = self.resolve_globs(
            manifest_path,
            "scan",
            manifest.get("scan", []),
            manifest.get("scan_exclude", []),
        )
        if not corpus:
            self.add(
                manifest_path,
                "style manifest scan matches no files (vacuous corpus)",
            )
        claims: dict[Path, list[str]] = defaultdict(list)
        seen: set[str] = set()
        for index, layer in enumerate(layers, start=1):
            if not isinstance(layer, dict):
                self.add(manifest_path, f"style layer #{index} must be a table")
                continue
            name = str(layer.get("name", "")).strip()
            if not name:
                self.add(manifest_path, f"style layer #{index} missing name")
                continue
            if name in seen:
                self.add(manifest_path, f"duplicate style layer name: {name}")
            seen.add(name)
            if not str(layer.get("owner", "")).strip():
                self.add(manifest_path, f"style layer {name} missing owner")
            includes = layer.get("include", [])
            if not isinstance(includes, list) or not includes:
                self.add(
                    manifest_path, f"style layer {name} needs non-empty include globs"
                )
                continue
            for path in self.resolve_globs(
                manifest_path,
                f"style layer {name}",
                includes,
                layer.get("exclude", []),
            ):
                claims[path].append(name)
        for path in sorted(corpus):
            owners = claims.get(path, [])
            relative = path.relative_to(self.root).as_posix()
            if not owners:
                self.add(
                    manifest_path,
                    f"style corpus file resolves to no declared layer: {relative}",
                )
            elif len(owners) > 1:
                self.add(
                    manifest_path,
                    "style corpus file resolves to more than one layer "
                    f"({', '.join(sorted(owners))}): {relative}",
                )

    def validate_style_tiers(
        self, manifest_path: Path, manifest: dict[str, Any]
    ) -> None:
        """Value tiers reference one way only.

        Array order is the reference order, so an upward or self reference is a
        strict index comparison. The graph is acyclic by construction; there is
        no traversal to get subtly wrong.
        """

        tiers = manifest.get("tiers", [])
        if not isinstance(tiers, list) or not tiers:
            return
        order: dict[str, int] = {}
        for index, tier in enumerate(tiers):
            if not isinstance(tier, dict):
                self.add(manifest_path, f"style tier #{index + 1} must be a table")
                continue
            name = str(tier.get("name", "")).strip()
            if not name:
                self.add(manifest_path, f"style tier #{index + 1} missing name")
                continue
            if name in order:
                self.add(manifest_path, f"duplicate style tier name: {name}")
            else:
                order[name] = index
            if not str(tier.get("owner", "")).strip():
                self.add(manifest_path, f"style tier {name} missing owner")
        for index, tier in enumerate(tiers):
            if not isinstance(tier, dict):
                continue
            name = str(tier.get("name", "")).strip()
            if not name:
                continue
            references = tier.get("may_reference", [])
            if not isinstance(references, list):
                self.add(
                    manifest_path, f"style tier {name} may_reference must be a list"
                )
                continue
            for reference in references:
                target = str(reference).strip()
                if target not in order:
                    self.add(
                        manifest_path,
                        f"style tier {name} references undeclared tier: {target}",
                    )
                elif order[target] >= index:
                    self.add(
                        manifest_path,
                        f"style tier {name} may reference only lower tiers: {target}",
                    )

    def validate_architecture_rules(
        self, manifest_path: Path, manifest: dict[str, Any]
    ) -> None:
        rules = manifest.get("rules", [])
        if not isinstance(rules, list) or not rules:
            self.add(
                manifest_path,
                "configured architecture manifest needs at least one rule",
            )
            return
        seen: set[str] = set()
        for index, rule in enumerate(rules, start=1):
            if not isinstance(rule, dict):
                self.add(manifest_path, f"architecture rule #{index} must be a table")
                continue
            rule_id = str(rule.get("id", "")).strip()
            if not rule_id:
                self.add(manifest_path, f"architecture rule #{index} missing id")
                continue
            if rule_id in seen:
                self.add(manifest_path, f"duplicate architecture rule id: {rule_id}")
            seen.add(rule_id)
            includes = rule.get("include", [])
            excludes = rule.get("exclude", [])
            patterns = rule.get("forbidden_patterns", [])
            if not isinstance(includes, list) or not includes:
                self.add(manifest_path, f"rule {rule_id} needs non-empty include globs")
                continue
            if not isinstance(patterns, list) or not patterns:
                self.add(
                    manifest_path,
                    f"rule {rule_id} needs non-empty forbidden_patterns",
                )
                continue
            filtered = self.resolve_globs(
                manifest_path, f"rule {rule_id}", includes, excludes
            )
            if not filtered:
                self.add(
                    manifest_path, f"rule {rule_id} matches no files (vacuous rule)"
                )
                continue
            for path in sorted(filtered):
                try:
                    text = path.read_text(encoding="utf-8")
                except UnicodeDecodeError:
                    self.add(path, f"rule {rule_id} matched a non-text file")
                    continue
                for forbidden in patterns:
                    if (
                        not isinstance(forbidden, str)
                        or not forbidden
                        or PLACEHOLDER_RE.search(forbidden)
                    ):
                        self.add(
                            manifest_path,
                            f"rule {rule_id} has invalid forbidden pattern",
                        )
                        continue
                    for lineno, line in enumerate(text.splitlines(), start=1):
                        if forbidden in line:
                            self.add(
                                path,
                                f"line {lineno}: architecture rule {rule_id} forbids {forbidden!r}",
                            )

    def run(self) -> bool:
        self.policy = self.load_toml(self.root / "docs-policy.toml", "docs policy")
        self.validate_policy_shape()
        self.required_templates = self.required_template_files()
        self.validate_docs_layout()
        self.load_records()
        for record in self.records:
            self.validate_metadata(record)
            self.validate_relationships(record)
            self.validate_target_aging(record)
            self.validate_promises(record)
            self.validate_surface_citations(record)
            self.validate_contract_sources(record)
        self.validate_templates()
        self.validate_abnormalities()
        self.validate_local_links()
        self.validate_architecture()
        self.validate_style_ownership()
        return not self.errors

    def print_group(self, findings: list[Finding]) -> None:
        grouped: dict[Path, list[str]] = defaultdict(list)
        for finding in findings:
            grouped[finding.path].append(finding.message)
        for path in sorted(grouped, key=self.display_path):
            print(f"\n{self.display_path(path)}")
            for message in grouped[path]:
                print(f"  - {message}")

    def print_report(self) -> None:
        errors = self.errors
        advisories = self.advisories
        if errors:
            print(
                f"check_docs: {len(errors)} error(s) in "
                f"{len({finding.path for finding in errors})} path(s) — "
                "these block"
            )
            self.print_group(errors)
        if advisories:
            if errors:
                print()
            print(
                f"check_docs: {len(advisories)} advisory finding(s) in "
                f"{len({finding.path for finding in advisories})} path(s) "
                "— not blocking; rerun with --strict to enforce"
            )
            self.print_group(advisories)
        if errors:
            return
        if advisories:
            print()
        print(
            "check_docs: OK — "
            f"{len(self.records)} canonical document(s), "
            f"{len(self.required_templates)} template(s) "
            f"(profile: {self.template_profile()}), "
            f"adoption stage: {self.stage}, links and policy valid"
        )

    def template_profile(self) -> str:
        config = self.policy.get("templates", {})
        if config.get("required_files"):
            return "explicit"
        return str(config.get("profile", "unset"))


def parse_args(argv: Iterable[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="repository root (defaults to the checker repository)",
    )
    parser.add_argument(
        "--today",
        default=datetime.now().astimezone().date().isoformat(),
        help="clock date for deterministic aging checks (YYYY-MM-DD)",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="treat advisory findings as errors (for a scheduled hygiene job)",
    )
    return parser.parse_args(argv)


def main(argv: Iterable[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        today = date.fromisoformat(args.today)
    except ValueError:
        print(f"check_docs: invalid --today date: {args.today}")
        return 2
    checker = DocumentationChecker(args.root, today, strict=args.strict)
    checker.run()
    checker.print_report()
    return 0 if not checker.errors else 1


if __name__ == "__main__":
    sys.exit(main())
