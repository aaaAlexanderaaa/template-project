---
id: ADR-004
kind: decision
status: current
title: "Discipline-first template architecture, five-part boundary/invariant specs, open closed-loop independent review, and explicit UI design approval gate"
sources:
  - SRC-010
  - SRC-011
  - SRC-013
  - SRC-019
  - SRC-020
affects:
  - discipline.entry-and-contracts
  - discipline.guides-and-skills
  - discipline.templates
  - graph.indexer
  - graph.validator
  - perspective.context-pack
  - perspective.server
  - ui.perspective-web
supersedes: []
---

# ADR-004: Discipline-First Architecture, Five-Part Specs, Open Closed-Loop Review & UI Approval Gate

- **Context & problem**:
  After the initial 2026.11 refactor, four structural distortions remained:
  1. Independent review lacked a normative definition, used narrow code checklists instead of open-ended architecture and consistency review, and left pre-refactor findings unclosed after refactoring; meanwhile tests checked Python script mechanics rather than whether the engineering discipline transfers intact.
  2. Repository overviews and diagrams centered on the Python document-extraction scripts (`Loader -> Indexer -> Validator`) rather than the engineering discipline itself, while copied starter templates stripped away core rules and `doc_inventory.py` hardcoded template domain names.
  3. System and module specs emphasized folder `owns` globs and static `depends_on` imports instead of domain runtime logic, state ownership, hard invariants, and forbidden couplings.
  4. The web interface in `scripts/projectlib/web/` kept extending an unapproved 4-section single-page layout without an owner sign-off.
- **Chosen approach**:
  1. Define Independent Review normatively in [delivery-and-verification.md](../contracts/delivery-and-verification.md) with four mandatory rules: fresh context with withheld author rationale, open-ended holistic mandate first, architecture/consistency/outcome scope, and closed-loop re-verification back to original and fresh reviewers. Pair script unit checks with automated downstream-transfer tests and five behavioral evaluation scenarios.
  2. Re-center [README.md](../../README.md), [README_CN.md](../../README_CN.md), [AGENTS.md](../../AGENTS.md), and [ARCHITECTURE.md](../../ARCHITECTURE.md) around the engineering discipline system, demoting `scripts/` to subordinate mechanical tooling, upgrading downstream `templates/`, and making `doc_inventory.py` repository-agnostic.
  3. Establish five core architecture elements in [architecture-and-modularity.md](../contracts/architecture-and-modularity.md) and downstream templates: purpose/non-goals, runtime business/control logic and failure paths, bounded responsibilities and explicitly forbidden couplings, single source of state and hard invariants, and fitness verification.
  4. Leave `scripts/projectlib/web/` frozen, mark task `T-204` `blocked` in [work.toml](../work.toml), and record a first-principles frontend critique plus three distinct layout options in [perspective-web.md](../design/perspective-web.md) for explicit owner choice (subsequently resolved by owner specification `SRC-022` in [ADR-005](ADR-005-calm-platter-frontend-specification-and-perspective-web.md)).
- **Trade-offs & rejected alternatives**:
  - Patching the unapproved 4-section UI layout again was rejected because incremental layout tweaks treat an unapproved draft as settled design authority and hide five structural comprehension failures.
  - Restoring heavy 12-section forms in templates was rejected; keeping thin YAML metadata paired with five concrete, non-ceremonial architecture headings gives clarity without paperwork overhead.
