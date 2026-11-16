---
id: graph.indexer
domain: graph-engine
kind: module-spec
summary: "Generic repository graph loader, dynamic directory indexer, static AST/ES import scanner, and Git telemetry collector."
promise: "Builds a unified repository graph for any project using this discipline without hardcoding template-project internal domain names."
owns:
  - "scripts/projectlib/loader.py"
  - "scripts/projectlib/doc_inventory.py"
  - "scripts/projectlib/git_telemetry.py"
  - "scripts/projectlib/import_scanner.py"
depends_on:
  - graph.model
sources:
  - SRC-013
  - SRC-015
  - SRC-017
  - SRC-018
  - SRC-019
  - SRC-020
---

# Graph Loader, Document Indexer, Import Scanner & Git Telemetry

## 1. Purpose, Public Interface & Non-Goals

- **Public interface**: `load_project_graph(root)`, `save_runtime_state`, `index_repository_docs_and_dirs`, `scan_files_and_imports`, `collect_git_telemetry`, and `compare_git_refs`.
- **Out of scope**: Emitting validation exit codes (`validator.py`), modifying tracked TOML/Markdown sources, or assuming `template-project` domains on host codebases.

## 2. Indexing & Day-0 Synthesis Flow

```mermaid
flowchart LR
  Disk["docs-policy.toml, sources.toml, specs/, work.toml"] --> Load["load_project_graph()"]
  Load -->|Zero Modules (Day 0)| Synth["Synthesize Directory Preview Modules"]
  Load -->|Specs Present| Real["Resolve Domain/Module Ownership + Dynamic Dir Domains"]
  Real --> Telemetry["Scan Python/JS/TS/CSS Imports + Git Lag/Diff"]
  Synth --> Telemetry
```

## 3. State Ownership, Constraints & Forbidden Couplings

- **Review Anchor Resolution**: `loader.py` reads `[collaboration].review_anchor_sha` from `docs-policy.toml` as tracked baseline and applies local overrides from `tmp/project-state.json` when present.
- **Dynamic Domain Inference**: `doc_inventory.py` holds generic folder descriptions only and assigns a directory a single domain ONLY when matched docs/`owns` patterns map unambiguously to one domain; shared multi-domain directories keep `domain = ""`.
- **Forbidden couplings**: Imports ONLY `graph.model`; must never import `perspective-ui` or hardcode template domains. Also inspects working-tree changes when `compare_git_refs` receives an empty `base_ref` and tracks uncommitted worktree digest in `tmp/project-state.json` so `mark-reviewed` clears cleanly.
