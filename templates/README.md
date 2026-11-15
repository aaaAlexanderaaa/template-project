# Starter Templates (Minimal Single-Source Files)

This directory contains minimal starter skeletons transferred into new or
adopting repositories via `python3 scripts/project.py init --target <dir>`.
They preserve core engineering rules, five-part architecture sections, owner
UI approval gates, and open closed-loop independent review protocols:

- [AGENTS.md](AGENTS.md) / [AGENTS.zh.md](AGENTS.zh.md) — Bilingual working agreement for downstream projects (plain language, proactive architecture design, approval boundaries, open closed-loop review).
- [docs-readme.md](docs-readme.md) / [docs-readme.zh.md](docs-readme.zh.md) — Starter `docs/README.md` with authoritative map and language standard.
- [ARCHITECTURE.md](ARCHITECTURE.md) / [ARCHITECTURE.zh.md](ARCHITECTURE.zh.md) — Bilingual five-part system overview (positioning, runtime `mermaid` flow, forbidden couplings, state/constraints, verification).
- [adr.md](adr.md) / [adr.zh.md](adr.zh.md) — Cross-module architectural decision (`docs/decisions/ADR-NNN-slug.md`).
- [domain-readme.md](domain-readme.md) / [domain-readme.zh.md](domain-readme.zh.md) — Per-domain overview with boundaries, runtime flow, and forbidden couplings (`docs/specs/<domain>/README.md`).
- [module-spec.md](module-spec.md) / [module-spec.zh.md](module-spec.zh.md) — Module spec claiming source globs, interfaces, invariants, and dependencies (`docs/specs/<domain>/<module>.md`).
- [surface-spec.md](surface-spec.md) / [surface-spec.zh.md](surface-spec.zh.md) — Frontend UI surface spec with explicit Owner Design Approval gate (`docs/design/<surface>.md`).
- [independent-review.md](independent-review.md) / [independent-review.zh.md](independent-review.zh.md) — Open-ended, rationale-blind independent review and closed-loop re-verification record.
- [sources.toml](sources.toml) — Append-only ledger for verbatim user quotes (`docs/sources.toml`).
- [work.toml](work.toml) — Roadmap slots (`done/now/next/later`) and task states (`docs/work.toml`).
- [architecture-rules.toml](architecture-rules.toml) — Optional custom forbidden-pattern boundary rules (`architecture-rules.toml`).
- [adoption-assessment.md](adoption-assessment.md) / [adoption-assessment.zh.md](adoption-assessment.zh.md) — Read-only inventory before enabling enforcement in an existing codebase.
- [charter.md](charter.md) / [charter.zh.md](charter.zh.md) — Standing bounds for unattended autonomous runs.
- [ci/docs-check.example.yml](ci/docs-check.example.yml) — CI workflow running tests and `check_docs.py`.
