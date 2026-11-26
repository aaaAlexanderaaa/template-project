---
doc_type: authority-map
status: current
authority: normative
---

# Documentation Map & Single-Source Topology

Every fact in this repository has one authoritative home. Helper scripts under
`scripts/` read these files, check cross-references against actual Git history
and source code imports, and present the result to AI sessions (`project.py context`
and `project.py status`) plus the local web overview
(`project.py serve`, specified in `docs/design/perspective-web.md`).

## 1. Where Each Fact Lives (Zero Duplication)

| Fact | Single authoritative file | How other files reference it |
|---|---|---|
| System purpose & cross-domain flows | `ARCHITECTURE.md` (thin frontmatter + standard `mermaid` blocks) | Linked directly |
| Domain purpose, maturity `stage`, & domain flows | `docs/specs/<domain>/README.md` (optional in single-domain repos) | `domain: <domain-id>` |
| Module responsibility, user promise, owned paths, & allowed dependencies | `docs/specs/<domain>/<module>.md` (thin frontmatter: `id`, `summary`, `promise`, `owns`, `depends_on`, `sources` + prose & `mermaid`) | Module `id` (e.g. `graph.indexer`) |
| UI surface layout, reader background, & interaction states | `docs/design/<surface>.md` (`kind: surface-spec`) | Surface `id` |
| Cross-module trade-offs & architectural changes | `docs/decisions/ADR-*.md` (frontmatter: `id`, `status`, `sources`, `affects`, `supersedes`) | Decision `id` (e.g. `ADR-002`) |
| Substantive direction-shaping owner quotes & original context | `docs/sources.toml` (`[[sources]]` chronologically ordered, `id = "SRC-*"` with exact unedited `'''...'''` text) | `SRC-*` ID |
| Roadmap slots (`done/now/next/later`), active task states, & human blockers | `docs/work.toml` (or per-domain `docs/specs/<domain>/work.toml` + `docs/archive/work-*.toml`) | Task / Milestone `id` referencing spec, ADR, and `SRC-*` IDs |
| Runtime collaboration mode, source roots, & file-size budgets | `docs-policy.toml` | Loaded automatically by `scripts/` |

## 2. Task Context Lookup

<!-- required-reading: task-context -->
### Task context

Before changing behavior, read five facts from their authoritative owners:

1. **Requested outcome & original words**: Read the user's request and run
   `python3 scripts/project.py context <target>` to inspect linked `SRC-*`
   quotes and prior `ADR-*` trade-offs.
2. **Current code & module owner**: Open the owning `docs/specs/.../*.md` spec
   and inspect the actual files matched by its `owns` patterns.
3. **Stage & collaboration mode**: Check `stage` (`prototype | usable | stable`)
   on the domain/project and `[collaboration]` in `docs-policy.toml`.
4. **Boundaries**: Check `depends_on` in the module spec, `architecture-rules.toml`,
   and file-size / CSS budgets in `docs-policy.toml`.
5. **Completion check**: Verify both promised behavior and absence of unintended
   side effects on the real execution path.
<!-- /required-reading: task-context -->

## 3. Plain Language Standard (Normative for Docs, CLI & UI)

<!-- required-reading: language-standard -->
### Language standard

Every agent working in this repository or in an adopting project must write in
plain, direct prose so an unfamiliar human reader and future AI sessions can
understand immediately without decoding insider terms:

1. **Follow the repository's chosen language**:
   - In `template-project` itself, normative docs, specs, and ADRs use **plain,
     direct English**; `docs/sources.toml` keeps **exact original quotes** in the
     owner's language without translating or paraphrasing; the local web viewer
     defaults to **plain Chinese** with a complete Chinese/English toggle.
   - In any project that adopts `template-project`, write the product's own docs,
     specs, ADRs, UI labels, and product-facing CLI/error messages in **the
     project owner's chosen language** (e.g., plain Chinese for a Chinese product,
     plain English for an English library); bundled `scripts/*.py` repository
     checker utilities keep English developer diagnostics alongside localized
     status summaries when configured.
2. **Direct explanation first**: State plainly what the object is, how it works,
   and what problem it solves before giving background or caveats.
3. **Positive-first rules and natural wording**:
   - State what good output looks like and where clear boundaries lie. Reserve
     detailed lists of unwanted writing habits for optional on-demand cleanup
     skills rather than default-loaded rules, because negative examples in
     default context prime clean models with habits they lacked and reinforce
     those habits in models that already have them (`SRC-036`).
   - Keep widely used technical terms natural (preserve standard English terms
     in non-English prose when translation hurts clarity), translate backend
     enum tokens into ordinary words in human views, keep numbering consistent
     on each page, and state scope boundaries directly in one or two plain
     sentences instead of stacking disclaimers.
<!-- /required-reading: language-standard -->
