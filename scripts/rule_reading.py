"""Local Markdown resolution shared by the reader and documentation checker.

This module reads source as data. It has no shell, network, or cache interface.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote, urlsplit


def parse_frontmatter_text(text: str) -> tuple[dict[str, str], str | None]:
    opening = re.match(r"---\r?\n", text)
    if opening is None:
        return {}, "missing frontmatter"
    remaining = text[opening.end():]
    closing = re.search(r"(?m)^---\r?\n", remaining)
    if closing is None:
        return {}, "unterminated frontmatter"
    metadata = {}
    for line in remaining[:closing.start()].splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if ":" not in stripped:
            return metadata, f"invalid frontmatter line: {stripped}"
        key, value = stripped.split(":", 1)
        key = key.strip()
        if not key or key in metadata:
            return metadata, f"empty or duplicate frontmatter field: {key}"
        metadata[key] = value.strip().strip("\"'")
    return metadata, None


def heading_slug(value: str) -> str:
    """The repository's existing renderer-style heading convention."""
    value = re.sub(r"[^\w\s-]", "", value.strip().lower())
    return re.sub(r"\s", "-", value)


class RuleError(ValueError):
    """A declared reading boundary cannot be resolved safely."""


@dataclass(frozen=True)
class Span:
    identifier: str
    start: int
    end: int
    heading: str


@dataclass(frozen=True)
class Source:
    path: str
    data: bytes
    digest: str
    metadata: dict[str, str]
    lines: tuple[str, ...]
    visible: tuple[bool, ...]
    headings: dict[str, tuple[int, str]]
    spans: tuple[Span, ...]


@dataclass(frozen=True)
class Unit:
    path: str
    identifier: str
    heading: str
    authority: str
    status: str
    file_digest: str
    metadata_digest: str
    data: bytes
    dependencies: tuple[str, ...]

    @property
    def identity(self) -> str:
        return f"{self.path}#{self.identifier}"


@dataclass(frozen=True)
class Prepared:
    units: tuple[Unit, ...]
    delivered: tuple[Unit, ...]
    manifest: dict
    sources: tuple[Source, ...]


MARKER = re.compile(r"^<!-- (/?)required-reading: ([a-z][a-z0-9-]*) -->\s*$")
HEADING = re.compile(r"^#{1,6} (.+?)\s*#*\s*$")
DIRECTIVE = re.compile(r"^- required-reading: \[[^\]\n]+\]\(([^\s)]+)\)\s*$")
LINK = re.compile(r"\[[^\]]+\]\(([^\s)]+)\)")
ROUTING = "docs/contracts/development-discipline.md"


def visible_lines(lines: list[str]) -> tuple[bool, ...]:
    """Exclude fenced examples while keeping source byte offsets untouched."""
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
        raise RuleError("unclosed fenced example")
    return tuple(visible)


def utf8_parts(data: bytes, size: int) -> list[bytes]:
    if size < 4:
        raise RuleError("part-size must be at least 4 bytes for UTF-8 recovery")
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


class RuleRepository:
    def __init__(self, root: Path):
        self.root = root.resolve()
        self.sources: dict[str, Source] = {}
        self.targets: set[str] = set()

    def reference(self, reference: str, containing: str | None = None) -> tuple[str, str]:
        ref = urlsplit(reference)
        if ref.scheme or ref.netloc or ref.query or "\\" in reference:
            raise RuleError(f"nonlocal or unsupported reference: {reference}")
        base = (self.root / containing).parent if containing else self.root
        path = base / unquote(ref.path) if ref.path else self.root / (containing or "AGENTS.md")
        resolved = path.resolve()
        if not resolved.is_relative_to(self.root):
            raise RuleError(f"reference escapes repository: {reference}")
        relative = resolved.relative_to(self.root).as_posix()
        if resolved.suffix != ".md" or not resolved.is_file():
            raise RuleError(f"missing local Markdown source: {relative}")
        return relative, unquote(ref.fragment)

    def source(self, path: str) -> Source:
        path, _ = self.reference(path)
        if path in self.sources:
            return self.sources[path]
        try:
            data = (self.root / path).read_bytes()
            text = data.decode("utf-8")
            lines = text.splitlines(keepends=True)
            visible = visible_lines(lines)
            metadata, error = parse_frontmatter_text(text)
            if error and path != "AGENTS.md":
                raise RuleError(error)
            headings = {}
            spans = []
            opened = None
            used = set()
            for index, line in enumerate(lines):
                if not visible[index]:
                    continue
                if match := HEADING.match(line.rstrip("\r\n")):
                    slug = heading_slug(match[1])
                    # Ambiguous navigation should fail rather than silently pick one.
                    if slug in headings:
                        headings[slug] = (-1, match[1])
                    else:
                        headings[slug] = (index, match[1])
                marker = MARKER.match(line.rstrip("\r\n"))
                if "<!--" in line and "required-reading:" in line and not marker:
                    raise RuleError(f"line {index + 1}: malformed required-reading marker")
                if not marker:
                    continue
                closing, identifier = marker.groups()
                if not closing:
                    if opened:
                        raise RuleError(f"line {index + 1}: unclosed unit {opened[0]} before nested unit {identifier}")
                    if identifier in used or identifier == "document":
                        raise RuleError(f"line {index + 1}: duplicate or reserved unit {identifier}")
                    opened = (identifier, index + 1)
                    used.add(identifier)
                else:
                    if not opened or opened[0] != identifier:
                        raise RuleError(f"line {index + 1}: unmatched unit close {identifier}")
                    start = opened[1]
                    nonempty = [i for i in range(start, index) if lines[i].strip()]
                    if not nonempty or not visible[nonempty[0]] or not HEADING.match(lines[nonempty[0]].rstrip("\r\n")):
                        raise RuleError(f"unit {identifier} must begin at a heading")
                    for following in range(index + 1, len(lines)):
                        candidate = lines[following].strip()
                        if not candidate:
                            continue
                        next_heading = HEADING.match(candidate) if visible[following] else None
                        if next_heading:
                            first_level = len(lines[nonempty[0]]) - len(lines[nonempty[0]].lstrip("#"))
                            next_level = len(candidate) - len(candidate.lstrip("#"))
                            if next_level > first_level and next_heading[1] not in {"Source anchors", "Reconciliation log"}:
                                raise RuleError(f"unit {identifier} closes before a subordinate heading")
                            break
                        if visible[following] and MARKER.match(candidate):
                            continue
                        raise RuleError(f"unit {identifier} closes before remaining section prose")
                    heading = HEADING.match(lines[nonempty[0]].rstrip("\r\n"))[1]
                    spans.append(Span(identifier, start, index, heading))
                    opened = None
            if opened:
                raise RuleError(f"unclosed unit {opened[0]}")
            # Validate directive syntax even when a different unit was requested.
            for i, line in enumerate(lines):
                if visible[i] and re.match(r"^\s*- required-reading:", line) and not DIRECTIVE.match(line.rstrip("\r\n")):
                    raise RuleError(f"line {i + 1}: malformed required-reading directive")
            if "reading_entrypoint" in metadata and metadata["reading_entrypoint"] not in used:
                raise RuleError("reading_entrypoint must name a declared complete unit")
            source = Source(path, data, hashlib.sha256(data).hexdigest(), metadata,
                            tuple(lines), visible, headings, tuple(spans))
            self.sources[path] = source
            return source
        except (OSError, UnicodeError, RuleError) as exc:
            raise RuleError(f"{path}: {exc}") from exc

    def resolve(self, reference: str, containing: str | None = None, *, stable=False) -> Unit:
        path, fragment = self.reference(reference, containing)
        source = self.source(path)
        status = source.metadata.get("status", "entrypoint")
        if path != "AGENTS.md" and status != "current":
            if status != "target" or path not in self.targets:
                raise RuleError(f"{path}: unsupported lifecycle {status}; explicitly select a target with --target")
        published = not fragment and source.metadata.get("reading_entrypoint")
        if published:
            fragment = published
        span = next((s for s in source.spans if s.identifier == fragment), None)
        # Navigation anchors take precedence; stable ids recover a renamed heading.
        if fragment and fragment != "document" and fragment in source.headings and not ((stable or published) and span):
            index, _ = source.headings[fragment]
            if index < 0:
                raise RuleError(f"{path}: ambiguous heading anchor #{fragment}")
            span = next((s for s in source.spans if s.start <= index < s.end), None)
        elif fragment and fragment != "document" and span is None:
            raise RuleError(f"{path}: missing heading anchor or unit #{fragment}")
        start, end = (span.start, span.end) if span else (0, len(source.lines))
        dependencies = tuple(DIRECTIVE.match(source.lines[i].rstrip("\r\n"))[1]
            for i in range(start, end) if source.visible[i] and DIRECTIVE.match(source.lines[i].rstrip("\r\n")))
        return Unit(path, span.identifier if span else "document",
                    span.heading if span else next((h[1] for h in source.headings.values()), path),
                    source.metadata.get("authority", "entrypoint"), status, source.digest,
                    hashlib.sha256(json.dumps(source.metadata, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest(),
                    "".join(source.lines[start:end]).encode("utf-8"), dependencies)

    def routes(self) -> dict[str, dict]:
        path, _ = self.reference(ROUTING)
        source = self.source(path)
        if source.metadata.get("status") != "current" or source.metadata.get("authority") != "normative":
            raise RuleError(f"{path}: concern routing must be current normative authority")
        rows = {}
        active = False
        for line, visible in zip(source.lines, source.visible):
            if not visible:
                continue
            if line.startswith("| Change trait | Activated concern | Minimum questions |"):
                if "Required reading" not in line:
                    raise RuleError(f"{path}: concern table needs Required reading column")
                active = True
                continue
            if not active:
                continue
            if not line.startswith("|"):
                break
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if cells and all(re.fullmatch(r":?-+:?", c) for c in cells):
                continue
            if len(cells) != 4:
                raise RuleError(f"{path}: malformed concern row")
            trait, name, questions, required = cells
            slug = heading_slug(name)
            links = LINK.findall(required)
            tokens = re.findall(r"owner:([a-z][a-z0-9-]*)", required)
            rest = LINK.sub("", required)
            rest = re.sub(r"owner:[a-z][a-z0-9-]*", "", rest).replace(";", "").strip()
            if not slug or slug in rows or rest or not (links or tokens) or any(t != slug for t in tokens):
                raise RuleError(f"{path}: invalid Required reading declaration for {name}")
            rows[slug] = dict(name=name, trait=trait, questions=questions,
                              references=links, owner=bool(tokens))
        if not rows:
            raise RuleError(f"{path}: missing concern routing table")
        return rows

    def validate_owner(self, reference: str, concern: str) -> Unit:
        unit = self.resolve(reference)
        meta = self.source(unit.path).metadata
        kind = meta.get("doc_type")
        canonical = unit.path.startswith("docs/contracts/") if kind == "contract" else unit.path.startswith("docs/design/")
        if not canonical or meta.get("authority") != "normative" or kind not in {"contract", "surface-contract"}:
            raise RuleError(f"{unit.path}: owner must be a canonical normative contract or surface")
        if kind == "contract" and meta.get("contract_role", "product") not in {"product", "governance"}:
            raise RuleError(f"{unit.path}: owner requires a valid contract role")
        if kind == "surface-contract":
            expected_scope = "current-ui" if unit.status == "current" else "future-ui"
            if not meta.get("surface") or "{{" in meta.get("surface", "") or meta.get("contract_scope") != expected_scope:
                raise RuleError(f"{unit.path}: surface owner needs identity and compatible UI scope")
        return unit

    def closure(self, references: list[tuple[str, str | None]]) -> tuple[Unit, ...]:
        units = []
        done = set()
        active = []

        def visit(reference, containing):
            unit = self.resolve(reference, containing)
            if unit.identity in active:
                raise RuleError("dependency cycle: " + " -> ".join(active + [unit.identity]))
            if unit.identity in done:
                return
            active.append(unit.identity)
            for dependency in unit.dependencies:
                visit(dependency, unit.path)
            active.pop()
            done.add(unit.identity)
            units.append(unit)

        for reference, containing in references:
            visit(reference, containing)
        # Validate the complete graph before removing bodies already delivered
        # by a whole-file selection. Covered units can still have prerequisites.
        whole_documents = {unit.path for unit in units if unit.identifier == "document"}
        return tuple(unit for unit in units
                     if unit.identifier == "document" or unit.path not in whole_documents)

    @staticmethod
    def retained_units(receipt, context):
        """Validate caller assertions as data; current sources still decide closure."""
        if not isinstance(receipt, dict) or receipt.get("version") != 2:
            raise RuleError("retained manifest must be a version 2 object")
        if context is None or receipt.get("context") != context:
            raise RuleError("retained manifest requires the same live context")
        entries = receipt.get("units")
        if not isinstance(entries, list):
            raise RuleError("retained manifest requires a unit list")
        retained = {}
        for entry in entries:
            if not isinstance(entry, dict):
                raise RuleError("retained manifest has an invalid unit record")
            for key in ("identity", "path", "unit", "authority", "status"):
                if not isinstance(entry.get(key), str) or not entry[key]:
                    raise RuleError(f"retained manifest has an invalid {key}")
            if entry["identity"] != f"{entry['path']}#{entry['unit']}" or entry["identity"] in retained:
                raise RuleError("retained manifest has inconsistent or duplicate unit identities")
            if type(entry.get("bytes")) is not int or entry["bytes"] < 0:
                raise RuleError("retained manifest has an invalid byte count")
            for key in ("sha256", "file_sha256", "metadata_sha256"):
                if not isinstance(entry.get(key), str) or not re.fullmatch(r"[0-9a-f]{64}", entry[key]):
                    raise RuleError(f"retained manifest has an invalid {key}")
            if not isinstance(entry.get("delivery"), str) or entry["delivery"] not in {"emitted", "caller-asserted-retained"}:
                raise RuleError("retained manifest has an invalid delivery label")
            retained[entry["identity"]] = entry
        return retained

    def prepare(self, concerns=(), bindings=(), targets=(), *, includes=(), context=None, retained=None) -> Prepared:
        # Each preparation is a new read-only transaction, even for callers
        # reusing this Python object. Prior target selection grants no authority.
        self.sources.clear()
        self.targets.clear()
        if context is not None and (not isinstance(context, str) or not context.strip()
                                    or context.splitlines() != [context]
                                    or any(ord(char) < 32 for char in context)):
            raise RuleError("context must be a nonempty single-line identifier")
        previous = {} if retained is None else self.retained_units(retained, context)
        for reference in targets:
            path, _ = self.reference(reference)
            source = self.source(path)
            if source.metadata.get("status") != "target" or source.metadata.get("authority") != "normative" or source.metadata.get("doc_type") not in {"contract", "surface-contract"}:
                raise RuleError(f"{path}: --target requires a target normative contract or surface")
            self.targets.add(path)
        routes = self.routes()
        selected = list(dict.fromkeys(concerns))
        for concern in selected:
            if concern not in routes:
                raise RuleError(f"unknown concern {concern}; use list to inspect current routing")
        owners = {}
        for binding in bindings:
            concern, sep, reference = binding.partition("=")
            if not sep or not reference or concern not in selected or not routes[concern]["owner"]:
                raise RuleError(f"owner binding for unselected concern or absent slot: {binding}")
            self.validate_owner(reference, concern)
            owners.setdefault(concern, []).append(reference)
        entry = self.source("AGENTS.md")
        entry_dependencies = [DIRECTIVE.match(line.rstrip("\r\n"))[1]
            for line, visible in zip(entry.lines, entry.visible) if visible and DIRECTIVE.match(line.rstrip("\r\n"))]
        if not entry_dependencies:
            raise RuleError("AGENTS.md: missing explicit required-reading entry dependency")
        references = [(ref, "AGENTS.md") for ref in entry_dependencies]
        for concern in selected:
            route = routes[concern]
            if route["owner"] and concern not in owners:
                raise RuleError(f"missing owner for {concern}; bind --owner {concern}=PATH")
            references.extend((ref, ROUTING) for ref in route["references"])
            references.extend((ref, None) for ref in owners.get(concern, []))
        references.extend((ref, None) for ref in targets)
        references.extend((ref, None) for ref in includes)
        units = self.closure(references)
        records = []
        delivered = []
        for u in units:
            record = {"identity": u.identity, "path": u.path, "unit": u.identifier,
                "heading": u.heading, "authority": u.authority, "status": u.status,
                "bytes": len(u.data), "sha256": hashlib.sha256(u.data).hexdigest(),
                "file_sha256": u.file_digest, "metadata_sha256": u.metadata_digest}
            old = previous.get(u.identity, {})
            # A history-only edit refreshes the source identity but need not
            # repeat an unchanged operative body and unchanged metadata.
            reusable = bool(old) and all(old.get(key) == value for key, value in record.items()
                                        if key not in {"file_sha256", "heading"})
            record["delivery"] = "caller-asserted-retained" if reusable else "emitted"
            records.append(record)
            if not reusable:
                delivered.append(u)
        manifest = {"version": 2, "context": context, "concerns": selected,
            "owner_bindings": list(bindings), "includes": list(includes), "units": records,
            "sources": {p: s.digest for p, s in sorted(self.sources.items())}}
        return Prepared(units, tuple(delivered), manifest, tuple(self.sources.values()))

    def recheck(self, sources):
        for source in sources:
            path, _ = self.reference(source.path)
            if path != source.path or hashlib.sha256((self.root / path).read_bytes()).hexdigest() != source.digest:
                raise RuleError(f"{source.path}: source changed; rerun prepare before dependent work")

    def transcript(self, prepared: Prepared) -> str:
        output = ["READING MANIFEST\n", json.dumps(prepared.manifest, ensure_ascii=False, sort_keys=True) + "\n"]
        delivered = {u.identity for u in prepared.delivered}
        for unit in prepared.units:
            if unit.identity not in delivered:
                output.append(f"RETAINED UNIT {unit.identity} (caller assertion)\n")
                continue
            output.extend([f"BEGIN UNIT {unit.identity}\n", unit.data.decode("utf-8"),
                           f"\nEND UNIT {unit.identity}\n"])
        retained = len(prepared.units) - len(prepared.delivered)
        counts = f" delivered={len(prepared.delivered)} retained={retained}" if retained else ""
        output.append(f"READING COMPLETE units={len(prepared.units)}{counts}\n")
        result = "".join(output)
        self.recheck(prepared.sources)
        return result

    def read(self, reference: str, digest: str) -> Unit:
        path, _ = self.reference(reference)
        # Recovery preserves the explicitly named target's lifecycle label.
        self.targets.add(path)
        unit = self.resolve(reference, stable=True)
        if digest != unit.file_digest:
            raise RuleError(f"{path}: expected file digest changed; rerun prepare")
        self.recheck(tuple(self.sources.values()))
        return unit

    def validate_declarations(self, paths: list[str]) -> list[tuple[str, str]]:
        """Check syntax and declared closure; do not infer domain applicability."""
        errors = []
        references = []
        for path in paths:
            try:
                source = self.source(path)
                if source.metadata.get("status") == "target":
                    self.targets.add(path)
                if source.metadata.get("status") not in {"current", "target"} and path != "AGENTS.md":
                    continue
                for line, visible in zip(source.lines, source.visible):
                    if visible and (match := DIRECTIVE.match(line.rstrip("\r\n"))):
                        references.append((match[1], path))
            except RuleError as exc:
                errors.append((path, str(exc)))
        try:
            for route in self.routes().values():
                references.extend((ref, ROUTING) for ref in route["references"])
        except RuleError as exc:
            errors.append((ROUTING, str(exc)))
        for ref, containing in references:
            try:
                self.closure([(ref, containing)])
            except RuleError as exc:
                errors.append((containing or "AGENTS.md", str(exc)))
        return list(dict.fromkeys(errors))
