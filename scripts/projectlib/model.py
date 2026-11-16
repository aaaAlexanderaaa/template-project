# Role: Immutable data structures for the stitched Single-Source-of-Truth project graph.
# Out of scope: File IO, Git subprocess calls, AST parsing, or HTTP transport.
# Anchors: spec=graph.model, ADR-002, SRC-015, SRC-018

from __future__ import annotations

from dataclasses import dataclass, field
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
