# Role: Public entrypoint for the pure single-source project graph model and frontmatter parser.
# Out of scope: Subprocess Git queries, HTTP server transport, or CLI argument parsing.
# Anchors: spec=graph.model, ADR-002, ADR-008

import sys

# The scripts need a TOML reader, not a particular Python version: Python 3.11+
# ships `tomllib`; older Python can use the same reader installed as `tomli`.
try:
    import tomllib  # noqa: F401
except ModuleNotFoundError:
    try:
        import tomli as _tomli
    except ModuleNotFoundError:
        raise SystemExit("These scripts need a TOML reader: use Python 3.11 or newer, or run `python3 -m pip install tomli`.") from None
    sys.modules["tomllib"] = _tomli

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
