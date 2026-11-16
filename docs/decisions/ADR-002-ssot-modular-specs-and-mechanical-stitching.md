---
id: ADR-002
kind: decision
status: current
title: "Single-Source-of-Truth modular specs stitched mechanically with verbatim sources and work queues"
sources:
  - SRC-013
  - SRC-014
  - SRC-015
  - SRC-017
  - SRC-018
  - SRC-019
affects:
  - discipline.entry-and-contracts
  - discipline.templates
  - graph.model
  - graph.indexer
  - graph.validator
  - perspective.context-pack
  - perspective.server
  - ui.perspective-web
supersedes:
  - ADR-001
---

# ADR-002: Single-Source-of-Truth Modular Specs & Mechanical Stitching

- **Context**: Maintaining duplicate `.toml` module or decision registries
  alongside Markdown design specs creates double maintenance, while pure
  free-form prose prevents zero-LLM mechanical indexing.
- **Chosen approach**:
  1. `ARCHITECTURE.md`, `docs/specs/<domain>/README.md`,
     `docs/specs/<domain>/<module>.md`, and `docs/design/<surface>.md` own
     system, domain, and module boundaries via thin `---` frontmatter (`id`,
     `summary`, `promise`, `owns`, `depends_on`, `sources`) plus plain prose and
     standard `mermaid` blocks.
  2. `docs/sources.toml` stores verbatim `SRC-*` user quotes once.
  3. `docs/work.toml` (plus optional domain shards and `docs/archive/work-*.toml`)
     stores dynamic milestone slots (`done/now/next/later`), task states, and
     human blockers by referencing IDs without duplicating descriptions.
  4. `check_docs.py` and `project.py` stitch these single-source files with AST
     imports, repository document inventories, and Git history for both AI
     sessions and the local web UI.
