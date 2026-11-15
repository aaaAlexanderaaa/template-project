---
id: ADR-003
kind: decision
status: current
title: "Stage-calibrated rigor and commit/module-accumulated review cadence"
sources:
  - SRC-001
  - SRC-003
  - SRC-004
affects:
  - discipline.entry-and-contracts
  - discipline.guides-and-skills
  - graph.validator
  - exemplar.domain
  - exemplar.shared
  - exemplar.checkout
  - exemplar.app
supersedes: []
---

# ADR-003: Stage-Calibrated Rigor & Change-Accumulated Review Cadence

- **Context**: Dispatching three review subagents on an unbuilt `0 -> 0.1`
  prototype wastes tokens and stalls momentum, while calendar-day review timers
  bear no relation to AI development bursts.
- **Chosen approach**:
  1. Declare `stage` (`prototype | usable | stable`) per project or domain so
     early prototypes move fast while stable cores enforce strict boundaries.
  2. Declare `[collaboration]` (`mode`, `model_tier`, `auto_independent_review`,
     `review_anchor_sha`) in `docs-policy.toml` so interactive sessions on
     strong models keep `Grill` on-demand, nudged mechanically by accumulated
     unreviewed commits and touched modules rather than elapsed days.
