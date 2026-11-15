# Role: Public entrypoint for the pure single-source project graph model and frontmatter parser.
# Out of scope: Subprocess Git queries, HTTP server transport, or CLI argument parsing.
# Anchors: spec=graph.model, ADR-002

from .frontmatter import (
    as_str_tuple,
    extract_markdown_structure,
    has_inline_role_header,
    heading_slug,
    parse_frontmatter,
)
from .model import (
    DecisionRecord,
    DirectoryEntry,
    DomainSpec,
    FileStat,
    ImportEdge,
    MermaidDiagram,
    Milestone,
    ModuleSpec,
    ModuleTelemetry,
    ProjectGraph,
    RepoDoc,
    SourceAnchor,
    ValidationFinding,
    WorkTask,
)

__all__ = [
    "DecisionRecord",
    "DirectoryEntry",
    "DomainSpec",
    "FileStat",
    "ImportEdge",
    "MermaidDiagram",
    "Milestone",
    "ModuleSpec",
    "ModuleTelemetry",
    "ProjectGraph",
    "RepoDoc",
    "SourceAnchor",
    "ValidationFinding",
    "WorkTask",
    "as_str_tuple",
    "extract_markdown_structure",
    "has_inline_role_header",
    "heading_slug",
    "parse_frontmatter",
]
