# Role: Immutable data structures for the stitched Single-Source-of-Truth project graph, plus the single
# module-to-quote lineage rule shared by context packs, traces, web payloads, and check_docs reminders.
# Out of scope: File IO, Git subprocess calls, AST parsing, or HTTP transport.
# Anchors: spec=graph.model, ADR-002, SRC-015, SRC-018

from __future__ import annotations

import re
from dataclasses import dataclass, field
from functools import lru_cache
from typing import Any


@dataclass(frozen=True)
class MermaidDiagram:
    title: str
    code: str
    source_path: str
    line: int


@dataclass(frozen=True)
class SourceAnchor:
    id: str
    date: str
    status: str
    context: str
    quote: str
    origin_path: str


@dataclass(frozen=True)
class DomainSpec:
    id: str
    name: str
    stage: str
    summary: str
    promise: str
    doc_path: str
    non_goals: str = ""
    mermaid_blocks: tuple[MermaidDiagram, ...] = ()
    body_markdown: str = ""


@dataclass(frozen=True)
class ModuleSpec:
    id: str
    domain: str
    kind: str  # module-spec | surface-spec
    stage: str
    title: str
    summary: str
    promise: str
    owns: tuple[str, ...]
    depends_on: tuple[str, ...]
    sources: tuple[str, ...]
    supersedes: tuple[str, ...]
    doc_path: str
    mermaid_blocks: tuple[MermaidDiagram, ...] = ()
    body_markdown: str = ""


@dataclass(frozen=True)
class DecisionRecord:
    id: str
    status: str  # current | superseded
    title: str
    sources: tuple[str, ...]
    affects: tuple[str, ...]
    supersedes: tuple[str, ...]
    superseded_by: str
    doc_path: str
    body_markdown: str = ""


@dataclass(frozen=True)
class Milestone:
    id: str
    domain: str
    name: str
    slot: str  # done | now | next | later
    depends_on: tuple[str, ...]
    era: str
    origin_path: str
    archived: bool = False


@dataclass(frozen=True)
class WorkTask:
    id: str
    milestone: str
    title: str
    state: str  # todo | active | blocked | ready_for_check | done
    human_check: str  # pending | approved | not_required
    specs: tuple[str, ...]
    decisions: tuple[str, ...]
    sources: tuple[str, ...]
    blocker_question: str = ""
    blocker_options: tuple[str, ...] = ()
    selected_option: str = ""
    parent: str = ""
    origin_path: str = ""
    archived: bool = False


@dataclass(frozen=True)
class RepoDoc:
    path: str
    title: str
    category: str  # entry | contract | guide | skill | spec | design | decision | template | config
    summary: str
    body_markdown: str
    line_count: int
    domain: str = ""
    owner_module: str = ""
    mermaid_blocks: tuple[MermaidDiagram, ...] = ()


@dataclass(frozen=True)
class DirectoryEntry:
    path: str
    label_zh: str
    label_en: str
    summary_zh: str
    summary_en: str
    file_count: int
    doc_count: int
    total_lines: int
    domain: str
    doc_paths: tuple[str, ...] = ()


@dataclass(frozen=True)
class FileStat:
    path: str
    lines: int
    is_style: bool
    has_role_header: bool
    owner_module: str | None


@dataclass(frozen=True)
class ImportEdge:
    source_file: str
    source_module: str | None
    target_ref: str
    target_module: str | None
    line: int
    allowed: bool


@dataclass(frozen=True)
class ModuleTelemetry:
    module_id: str
    file_count: int = 0
    total_loc: int = 0
    max_file_path: str = ""
    max_file_loc: int = 0
    oversized_files: tuple[tuple[str, int], ...] = ()
    git_doc_lag_commits: int = 0
    recent_commits: int = 0


@dataclass(frozen=True)
class ValidationFinding:
    rule_id: str
    severity: str  # error | advisory
    path: str
    message: str
    line: int = 0


@dataclass
class ProjectGraph:
    root_dir: str
    system_id: str
    project_name: str
    one_liner: str
    default_stage: str
    discipline_version: str
    identity: str
    policy: dict[str, Any]
    system_mermaid: tuple[MermaidDiagram, ...] = ()
    architecture_markdown: str = ""
    domains: dict[str, DomainSpec] = field(default_factory=dict)
    modules: dict[str, ModuleSpec] = field(default_factory=dict)
    decisions: dict[str, DecisionRecord] = field(default_factory=dict)
    sources: dict[str, SourceAnchor] = field(default_factory=dict)
    milestones: dict[str, Milestone] = field(default_factory=dict)
    tasks: dict[str, WorkTask] = field(default_factory=dict)
    repo_docs: tuple[RepoDoc, ...] = ()
    directory_map: tuple[DirectoryEntry, ...] = ()
    files: tuple[FileStat, ...] = ()
    import_edges: tuple[ImportEdge, ...] = ()
    module_telemetry: dict[str, ModuleTelemetry] = field(default_factory=dict)
    git_summary: dict[str, Any] = field(default_factory=dict)
    runtime_state: dict[str, Any] = field(default_factory=dict)
    parse_errors: list[ValidationFinding] = field(default_factory=list)
    is_day_zero_synthetic: bool = False


def module_source_refs(graph: ProjectGraph, spec: ModuleSpec) -> tuple[list[str], list[tuple[str, str]]]:
    """Return `(direct, via_decisions)` for a module. `direct` is the spec's own `sources`: quotes specifically about
    this module, shown in full. `via_decisions` lists `(SRC id, ADR id)` for quotes reached through non-superseded ADRs
    whose `affects` name the module or its domain; readers see them as one-line references. This is the only
    module-source rule: context packs, `build_lineage_trace`, web payloads, and `check_docs` reminders all call it.
    Task sources stay on tasks."""
    direct: list[str] = []
    for sid in spec.sources:
        if sid and sid not in direct:
            direct.append(sid)
    via: list[tuple[str, str]] = []
    seen = set(direct)
    for dec in sorted(graph.decisions.values(), key=lambda d: d.id):
        if dec.status != "superseded" and (spec.id in dec.affects or spec.domain in dec.affects):
            for sid in dec.sources:
                if sid and sid not in seen:
                    seen.add(sid)
                    via.append((sid, dec.id))
    return direct, via


def derive_module_source_ids(graph: ProjectGraph, spec: ModuleSpec) -> list[str]:
    """All `SRC-*` ids governing a module (direct first, then via ADRs)."""
    direct, via = module_source_refs(graph, spec)
    return direct + [sid for sid, _ in via]


def source_one_liner(graph: ProjectGraph, sid: str, limit: int = 120) -> str:
    """One-line summary of a source for compact references: its `context`, else the start of its quote."""
    src = graph.sources.get(sid)
    if src is None:
        return ""
    text = " ".join((src.context or src.quote).split())
    return text[:limit] + ("…" if len(text) > limit else "")


def _normalize_posix_path(raw: str) -> str:
    p = raw.replace("\\", "/").strip()
    while p.startswith("./"):
        p = p[2:]
    return p


def normalize_doc_roots(raw_roots: Any) -> tuple[str, ...]:
    """Normalize `[layout].doc_roots` entries into POSIX relative paths without leading `./`."""
    if not isinstance(raw_roots, (list, tuple)):
        return ()
    out: list[str] = []
    seen: set[str] = set()
    for item in raw_roots:
        raw = str(item).strip().replace("\\", "/")
        if not raw:
            continue
        if raw in (".", "./"):
            norm = "."
        elif raw.startswith("/"):
            norm = raw.rstrip("/") or "/"
        else:
            while raw.startswith("./"):
                raw = raw[2:]
            norm = raw.rstrip("/") or "."
        if norm not in seen:
            seen.add(norm)
            out.append(norm)
    return tuple(out)


@lru_cache(maxsize=256)
def _glob_to_regex(pattern: str) -> re.Pattern[str]:
    """Compile a POSIX path glob (`*` within a segment, `**` across directories, `?`, `[...]`)."""
    parts: list[str] = ["^"]
    i, n = 0, len(pattern)
    while i < n:
        ch = pattern[i]
        if pattern.startswith("**/", i) and (i == 0 or pattern[i - 1] == "/"):
            parts.append("(?:.+/)?")
            i += 3
        elif pattern.startswith("/**", i) and i + 3 == n:
            parts.append("/.*")
            i += 3
        elif pattern.startswith("**", i):
            parts.append(".*")
            i += 2
        elif ch == "*":
            parts.append("[^/]*")
            i += 1
        elif ch == "?":
            parts.append("[^/]")
            i += 1
        elif ch == "[":
            j = i + 1
            if j < n and pattern[j] in ("!", "^"):
                j += 1
            if j < n and pattern[j] == "]":
                j += 1
            while j < n and pattern[j] != "]":
                j += 1
            if j >= n:
                parts.append(r"\[")
                i += 1
            else:
                body = pattern[i + 1 : j]
                neg = ""
                if body and body[0] in ("!", "^"):
                    neg = "^"
                    body = body[1:]
                body = body.replace("\\", r"\\").replace("[", r"\[")
                if body.startswith("]"):
                    body = r"\]" + body[1:]
                if body.startswith("-"):
                    body = r"\-" + body[1:]
                if neg and "/" not in body:
                    body = "/" + body
                cls_expr = f"[{neg}{body}]"
                try:
                    re.compile(cls_expr)
                    parts.append(cls_expr)
                except re.error:
                    parts.append(re.escape(pattern[i : j + 1]))
                i = j + 1
        else:
            parts.append(re.escape(ch))
            i += 1
    parts.append("$")
    return re.compile("".join(parts))


def match_path_pattern(rel_path: str, pattern: str) -> bool:
    """Match a POSIX relative path against a file, directory prefix, or POSIX glob (`*`, `**`, `?`, `[...]`)."""
    rel = _normalize_posix_path(rel_path).rstrip("/")
    pat = _normalize_posix_path(pattern)
    if not pat or not rel:
        return False
    if pat.endswith("/**/"):
        pat = pat[:-1]
    norm = pat.rstrip("/")
    if norm and (rel == norm or ("*" not in norm and "?" not in norm and rel.startswith(norm + "/"))):
        return True
    if not any(ch in pat for ch in "*?["):
        return False
    if pat.endswith("/**"):
        prefix = pat[:-3].rstrip("/")
        if prefix and "*" not in prefix and "?" not in prefix and rel.startswith(prefix + "/"):
            return True
        if not any(ch in prefix for ch in "*?["):
            return False
    return bool(_glob_to_regex(pat).match(rel))


def matches_any_pattern(rel_path: str, patterns: tuple[str, ...] | list[str]) -> bool:
    return any(match_path_pattern(rel_path, pat) for pat in patterns)
