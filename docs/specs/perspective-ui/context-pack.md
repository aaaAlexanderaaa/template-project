---
id: perspective.context-pack
domain: perspective-ui
kind: module-spec
summary: "Builds progressive context packs, bidirectional traceability trees, and structured project overview payloads."
promise: "Every file, document path, module, domain, quote, or decision query returns exact business context, multi-spec task links, and code telemetry without misattributing superseded decisions."
owns:
  - "scripts/projectlib/context_pack.py"
  - "scripts/projectlib/briefing_pack.py"
depends_on:
  - graph.model
  - graph.indexer
  - graph.validator
sources:
  - SRC-013
  - SRC-014
  - SRC-016
  - SRC-017
  - SRC-019
  - SRC-020
---

# Context Pack & Web Payload Builder

## 1. Purpose, Public Interface & Non-Goals

- **Public interface**: `build_context_pack(graph, target)`, `build_lineage_trace(graph, node_id)`, and `serialize_perspective_payload(graph, csrf_token)`.
- **Out of scope**: Mutating files on disk, spawning subprocesses, or making web UI layout decisions.

## 2. Lookup & Traceability Assembly Flow

```mermaid
flowchart LR
  Query["File, Doc, Module, Quote, ADR, or Task ID"] --> Resolve{"Match Target Type"}
  Resolve -->|Source or Decision| Trace["Direct Task Match (sources / decisions IDs; Exclude Superseded Drift)"]
  Resolve -->|Module, File, Doc| Pack["Domain -> Promise -> Linked SRC/ADR -> Files"]
  Resolve -->|Unmatched| NotFound["Return found=false Diagnostic"]
  Pack --> Out["JSON / CLI Context Payload"]
```

## 3. State Ownership, Hard Invariants & Forbidden Couplings

- **Direct Lineage Precision**: `build_lineage_trace` attributes tasks to a source directly when `src_id in t.sources`, and attributes tasks to a decision ONLY when `dec.id in t.decisions` (for active decisions matching `affects` when no explicit task override conflicts, and NEVER sweeping current tasks onto `superseded` ADRs).
- **Complete Inbox Links**: Blocked and ready tasks retain full `specs`, `sources`, and `design_docs` arrays in addition to primary display metadata.
- **Forbidden couplings**: Imports `graph.*` read-only; never runs `git`, edits TOML, or imports `server.py`.
