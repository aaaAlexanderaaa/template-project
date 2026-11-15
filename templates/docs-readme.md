---
doc_type: authority-map
status: current
authority: normative
---

# Documentation Map & Language Standard

## 1. Authoritative Owners

| Fact | Single authoritative file |
|---|---|
| System purpose & top-level flow | `ARCHITECTURE.md` |
| Domain summary & maturity `stage` | `docs/specs/<domain>/README.md` |
| Module `owns`, `depends_on`, & `promise` | `docs/specs/<domain>/<module>.md` |
| UI surface design, approval gate & layout options | `docs/design/<surface>.md` |
| Cross-module architectural trade-offs | `docs/decisions/ADR-*.md` |
| Verbatim user quotes in original language | `docs/sources.toml` |
| Milestones (`done/now/next/later`) & tasks | `docs/work.toml` |
| Collaboration mode, source roots & line budgets | `docs-policy.toml` |

## 2. Pre-Edit Task Context Lookup

<!-- required-reading: task-context -->
### Task context

Before changing behavior, read five facts from their authoritative owners:

1. **Requested outcome & original words**: Read the user's request and run
   `python3 scripts/project.py context <target>` to inspect linked `SRC-*`
   quotes and prior `ADR-*` decisions.
2. **Current code & module owner**: Open the owning `docs/specs/.../*.md` spec
   and inspect the actual files matched by its `owns` patterns.
3. **Stage & collaboration mode**: Check `stage` (`prototype | usable | stable`)
   on the domain/project and `[collaboration]` in `docs-policy.toml`.
4. **Boundaries**: Check `depends_on` in the module spec, `architecture-rules.toml` (optional),
   and file-size / CSS budgets in `docs-policy.toml`.
5. **Completion check**: Verify both promised behavior and absence of unintended
   side effects on the real execution path.
<!-- /required-reading: task-context -->

## 3. Plain Language Standard

<!-- required-reading: language-standard -->
### Language standard

Write all project documentation, CLI text, and UI labels in plain, direct
prose matching the owner's chosen language (never force another language onto the
project, while keeping `docs/sources.toml` quotes verbatim):

- Explain directly what each module or screen is, how it works, and what problem
  it solves.
- Ban coined jargon, metaphors, conflicting numbering on the same page, stacked
  defensive disclaimers, and raw backend enum names in human-facing copy.
<!-- /required-reading: language-standard -->
