# Role: Digest-checked Markdown rule span resolution for `read_rules.py`.
# Out of scope: Git telemetry, AST code import scanning, or web server rendering.
# Anchors: spec=graph.model, ADR-002, SRC-015

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote, urlsplit


class RuleError(ValueError):
    """A declared reading boundary cannot be resolved safely."""


MARKER = re.compile(r"^<!-- (/?)required-reading: ([a-z][a-z0-9-]*) -->\s*$")
HEADING = re.compile(r"^#{1,6} (.+?)\s*#*\s*$")
LINK = re.compile(r"\[[^\]]+\]\(([^\s)]+)\)")


def heading_slug(value: str) -> str:
    cleaned = re.sub(r"[^\w\s-]", "", value.strip().lower())
    return re.sub(r"\s", "-", cleaned)


def parse_frontmatter_text(text: str) -> tuple[dict[str, str], str | None]:
    opening = re.match(r"---\r?\n", text)
    if opening is None:
        return {}, "missing frontmatter"
    remaining = text[opening.end() :]
    closing = re.search(r"(?m)^---\r?\n", remaining)
    if closing is None:
        return {}, "unterminated frontmatter"
    metadata: dict[str, str] = {}
    for line in remaining[: closing.start()].splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or stripped.startswith("- "):
            continue
        if ":" not in stripped:
            return metadata, f"invalid frontmatter line: {stripped}"
        key, value = stripped.split(":", 1)
        key = key.strip()
        metadata[key] = value.strip().strip("\"'")
    return metadata, None


def visible_lines(lines: list[str]) -> tuple[bool, ...]:
    fence = None
    visible = []
    for line in lines:
        match = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line.rstrip("\r\n"))
        if fence:
            visible.append(False)
            if match and match[1][0] == fence[0] and len(match[1]) >= fence[1] and not match[2].strip():
                fence = None
        elif match:
            visible.append(False)
            fence = (match[1][0], len(match[1]))
        else:
            visible.append(True)
    if fence:
        raise RuleError("unclosed fenced block")
    return tuple(visible)


def utf8_parts(data: bytes, size: int) -> list[bytes]:
    if size < 4:
        raise RuleError("part-size must be at least 4 bytes")
    data.decode("utf-8")
    parts = []
    start = 0
    while start < len(data):
        end = min(start + size, len(data))
        while end < len(data) and data[end] & 0xC0 == 0x80:
            end -= 1
        parts.append(data[start:end])
        start = end
    return parts or [b""]


@dataclass(frozen=True)
class Span:
    identifier: str
    start: int
    end: int
    heading: str


@dataclass(frozen=True)
class Unit:
    path: str
    identifier: str
    heading: str
    authority: str
    status: str
    file_digest: str
    data: bytes

    @property
    def identity(self) -> str:
        return f"{self.path}#{self.identifier}" if self.identifier != "document" else self.path


class RuleRepository:
    """Resolves `<!-- required-reading: slug -->` spans across contracts and docs."""

    CONCERN_MAP = {
        "governance": (
            "docs/contracts/collaboration-and-governance.md#governance-boundary",
            "docs/contracts/collaboration-and-governance.md#three-perspectives",
            "docs/contracts/collaboration-and-governance.md#inquiry-and-fallback",
            "docs/contracts/collaboration-and-governance.md#self-supervision",
        ),
        "lineage": ("docs/contracts/collaboration-and-governance.md#three-level-bidirectional-lineage",),
        "architecture": (
            "docs/contracts/architecture-and-modularity.md#decomposition-and-ownership",
            "docs/contracts/architecture-and-modularity.md#anti-monolith",
        ),
        "state": ("docs/contracts/architecture-and-modularity.md#single-source-of-state",),
        "css": ("docs/contracts/architecture-and-modularity.md#css-modularity",),
        "verification": (
            "docs/contracts/delivery-and-verification.md#bidirectional-verification",
            "docs/contracts/delivery-and-verification.md#discipline-and-transfer-verification",
            "docs/guides/grill.md#behavioral-discipline-evaluation-scenarios",
        ),
        "stage": ("docs/contracts/delivery-and-verification.md#stage-rigor",),
        "review": (
            "docs/contracts/delivery-and-verification.md#environment-aware-review",
            "docs/contracts/delivery-and-verification.md#independent-review-definition",
        ),
        "frontend": (
            "docs/contracts/frontend-and-visual-discipline.md#frontend-layers",
            "docs/contracts/frontend-and-visual-discipline.md#frontend-principles",
            "docs/contracts/frontend-and-visual-discipline.md#frontend-best-practices",
            "docs/contracts/frontend-and-visual-discipline.md#owner-preferences",
            "docs/contracts/frontend-and-visual-discipline.md#reference-practices",
            "docs/contracts/frontend-and-visual-discipline.md#pre-delivery-ui-self-check",
        ),
        "information": (
            "docs/contracts/information-organization.md#reader-task-first",
            "docs/contracts/information-organization.md#organizing-schemes",
            "docs/contracts/information-organization.md#layering-and-disclosure",
            "docs/contracts/information-organization.md#form-follows-content",
            "docs/contracts/information-organization.md#document-types",
            "docs/contracts/information-organization.md#coverage-scope-freshness",
            "docs/contracts/information-organization.md#information-self-check",
        ),
        "onboarding": (
            "docs/contracts/adoption-and-synchronization.md#read-before-judgment",
            "docs/contracts/adoption-and-synchronization.md#existing-directory-safety",
            "docs/contracts/adoption-and-synchronization.md#incremental-version-sync",
        ),
        "language": ("docs/README.md#language-standard",),
        "general": (),
    }

    def __init__(self, root: Path):
        self.root = root.resolve()
        self.units: dict[str, Unit] = {}
        self._scan()

    def _scan(self) -> None:
        candidates = [
            self.root / "AGENTS.md",
            self.root / "ARCHITECTURE.md",
            self.root / "docs" / "README.md",
        ]
        contracts_dir = self.root / "docs" / "contracts"
        if contracts_dir.is_dir():
            candidates.extend(sorted(contracts_dir.glob("*.md")))
        guides_dir = self.root / "docs" / "guides"
        if guides_dir.is_dir():
            candidates.extend(sorted(guides_dir.glob("*.md")))

        for file_path in candidates:
            if not file_path.is_file():
                continue
            rel = file_path.relative_to(self.root).as_posix()
            raw_bytes = file_path.read_bytes()
            digest = hashlib.sha256(raw_bytes).hexdigest()
            text = raw_bytes.decode("utf-8")
            meta, _ = parse_frontmatter_text(text)
            authority = meta.get("authority", "normative")
            status = meta.get("status", "current")

            self.units[rel] = Unit(
                path=rel,
                identifier="document",
                heading=file_path.stem,
                authority=authority,
                status=status,
                file_digest=digest,
                data=raw_bytes,
            )

            lines = text.splitlines(keepends=True)
            vis = visible_lines(lines)
            open_span: tuple[str, int] | None = None
            for idx, (line, is_vis) in enumerate(zip(lines, vis)):
                if not is_vis:
                    continue
                m = MARKER.match(line.rstrip("\r\n"))
                if not m:
                    continue
                closing, slug = m.group(1), m.group(2)
                if not closing:
                    if open_span:
                        raise RuleError(f"unclosed required-reading marker '{open_span[0]}' in {rel}:{open_span[1]}")
                    open_span = (slug, idx + 1)
                elif open_span and open_span[0] == slug:
                    body_lines = lines[open_span[1] : idx]
                    h_title = slug
                    for bl in body_lines:
                        hm = HEADING.match(bl.rstrip("\r\n"))
                        if hm:
                            h_title = hm.group(1)
                            break
                    span_bytes = "".join(body_lines).encode("utf-8")
                    unit = Unit(
                        path=rel,
                        identifier=slug,
                        heading=h_title,
                        authority=authority,
                        status=status,
                        file_digest=digest,
                        data=span_bytes,
                    )
                    self.units[f"{rel}#{slug}"] = unit
                    open_span = None
            if open_span:
                raise RuleError(f"unclosed required-reading marker '{open_span[0]}' in {rel}:{open_span[1]}")

            # Also allow referencing Markdown heading sections not already wrapped in a span
            for idx, (line, is_vis) in enumerate(zip(lines, vis)):
                if not is_vis:
                    continue
                hm = HEADING.match(line.rstrip("\r\n"))
                if not hm:
                    continue
                level = line.index(" ")
                h_title = hm.group(1).strip()
                slug = heading_slug(h_title)
                if not slug or f"{rel}#{slug}" in self.units:
                    continue
                end_idx = len(lines)
                for j in range(idx + 1, len(lines)):
                    if not vis[j]:
                        continue
                    jm = HEADING.match(lines[j].rstrip("\r\n"))
                    if jm and lines[j].index(" ") <= level:
                        end_idx = j
                        break
                sec_bytes = "".join(lines[idx:end_idx]).encode("utf-8")
                self.units[f"{rel}#{slug}"] = Unit(
                    path=rel,
                    identifier=slug,
                    heading=h_title,
                    authority=authority,
                    status=status,
                    file_digest=digest,
                    data=sec_bytes,
                )

    def routes(self) -> dict[str, object]:
        return {
            "concerns": {k: list(v) for k, v in sorted(self.CONCERN_MAP.items())},
            "units": sorted(self.units.keys()),
        }

    def resolve_ref(self, ref: str) -> Unit:
        parsed = urlsplit(unquote(ref.strip()))
        if parsed.fragment:
            key = f"{parsed.path}#{parsed.fragment.lower()}"
            if key in self.units:
                return self.units[key]
            exact_key = f"{parsed.path}#{parsed.fragment}"
            if exact_key in self.units:
                return self.units[exact_key]
            raise RuleError(f"Unknown fragment #{parsed.fragment} in {parsed.path}")
        if parsed.path in self.units:
            return self.units[parsed.path]
        raise RuleError(f"unknown rule unit: {ref}")

    def prepare(self, concerns: list[str], targets: list[str], includes: list[str]) -> list[Unit]:
        selected: list[Unit] = []
        seen: set[str] = set()
        refs: list[str] = [
            "AGENTS.md",
            "docs/README.md#task-context",
            "docs/README.md#language-standard",
        ]
        for c in concerns:
            if c not in self.CONCERN_MAP:
                raise RuleError(f"unknown concern '{c}'; run `read_rules.py list`")
            refs.extend(self.CONCERN_MAP[c])
        refs.extend(targets)
        refs.extend(includes)
        for ref in refs:
            unit = self.resolve_ref(ref)
            if unit.identity not in seen:
                seen.add(unit.identity)
                selected.append(unit)
        return selected

    def transcript(self, units: list[Unit]) -> str:
        manifest = {
            "version": 2,
            "unit_count": len(units),
            "units": [
                {"identity": u.identity, "sha256": u.file_digest, "bytes": len(u.data)}
                for u in units
            ],
        }
        chunks = [json.dumps(manifest, ensure_ascii=False, indent=2), ""]
        for u in units:
            chunks.append(f"=== UNIT {u.identity} (sha256={u.file_digest[:12]}) ===")
            chunks.append(u.data.decode("utf-8").rstrip())
            chunks.append(f"=== END {u.identity} ===\n")
        return "\n".join(chunks)

    def read(self, unit_ref: str, expected_digest: str) -> Unit:
        cleaned = expected_digest.strip()
        if len(cleaned) < 6:
            raise RuleError(f"digest prefix for {unit_ref} must be at least 6 hex chars, got {expected_digest!r}")
        unit = self.resolve_ref(unit_ref)
        if not unit.file_digest.startswith(cleaned):
            raise RuleError(f"digest mismatch for {unit_ref}: expected {cleaned}, actual {unit.file_digest}")
        return unit
