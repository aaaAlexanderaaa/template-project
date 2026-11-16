---
doc_type: authority-map
status: current
authority: normative
---

# Documentation Map & Single-Source Topology

Every fact in this repository has one authoritative home. Helper scripts under
`scripts/` read these files, check cross-references against actual Git history
and source code imports, and present the result to AI sessions (`project.py context`
and `project.py status`) plus the local calm-platter web workbench
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
3. **Banned writing habits**:
   - **No coined buzzwords or theatrical metaphors**: Use ordinary words (`详情抽屉`,
     `目录说明`, `三段式`, `模块依赖图`) rather than invented terms (`上下文胶囊`,
     `三幕剧`, `稀缺暖陶红`, `技术内生模块`).
   - **No defensive disclaimer chains**: Do not stack `"is not"` / `"does not prove"` /
     `"cannot prove"` / `"不是"` / `"不等于"` / `"不能证明"` disclaimers. When a scope boundary
     matters, state in one or two plain sentences what belongs elsewhere.
   - **No conflicting numbering on the same page**: Do not use `L1/L2` for two
     different meanings or mix `L1/L2` with `C2/C3` on the same screen.
   - **No raw backend enums or internal chat codes in human views**: Translate
     state tokens (`ready_for_check`, `stable`, `unclaimed_or_docs`) into plain
     human wording in UI copy and drop internal chat codes (`A1`, `P0`) from
     documentation.
<!-- /required-reading: language-standard -->
