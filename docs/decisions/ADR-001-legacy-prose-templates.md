---
id: ADR-001
kind: decision
status: superseded
title: "Legacy v1 16-template prose headings and 90-day calendar aging"
sources:
  - SRC-001
  - SRC-004
affects:
  - discipline.templates
  - graph.validator
supersedes: []
---

# ADR-001: Legacy v1 Prose Templates & Calendar Aging (Superseded)

- **Original approach**: Enforced 16 Markdown templates with 8–12 mandatory H2
  prose headings each, inline English paraphrases, and `90-day` calendar
  staleness deadlines.
- **Why superseded**: Mandatory prose headings forced agents to write repetitive
  boilerplate and defensive disclaimers, calendar deadlines failed unrelated CI
  builds without code changes, and prose-only documents could not be stitched
  mechanically into a scalable multi-domain roadmap or architecture map.
  Superseded by `ADR-002` and `ADR-003`.
