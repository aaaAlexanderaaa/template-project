---
id: ui.perspective-web
domain: perspective-ui
kind: surface-spec
stage: usable
summary: "Calm-platter 4-view Project Overview web workbench built under SRC-022 and ADR-005 for unfamiliar visitors, project owners, and independent reviewers."
promise: "Any reader navigates whole-repo purpose, runtime flow, module boundaries, full documentation with Tufte sidenotes, verbatim lineage, and row-expanded context cleanly across 540px to 3440px viewports without raw noise."
owns:
  - "scripts/projectlib/web/**"
depends_on:
  - perspective.context-pack
sources:
  - SRC-016
---

# Project Overview Web Workbench (`T-204`)

## 1. Owner Design Approval Gate & Page Archetypes

- **Design Status**: `approved` under owner specification `SRC-022` and architecture decision `ADR-005`. The implementation task (`T-204`) and its sign-off state live in `docs/work.toml`. `project.py init` distributes the rebuilt files under [scripts/projectlib/web/](../../scripts/projectlib/web/).
- **Approved Option & Historical Reference**: Earlier options drafted in [frontend-design-options.html](frontend-design-options.html) compared **Option A:** a 4-view workbench with a fixed top bar, **Option B:** a single linear long-form narrative scroll, and **Option C:** a persistent three-column IDE browser. In `SRC-022`, the owner locked in the five-standard specification matching **Option A:**'s fixed `32px` top navigation bar (`NSToolbar`), a single white central platter over a `#F5F5F7` canvas, and task-specific page scrolling (`100dvh` locked frames for dense management tables; natural page scroll plus Tufte sidenotes for long-form reading).
- **Target Readers**:
  1. Unfamiliar visitors seeking what the repository builds, what it excludes, how data and control flow end-to-end, and how folders map to modules.
  2. Project owners checking domain health, resolving blocking questions inline, approving completed work, and tracing verbatim requirements (`SRC-*` -> `ADR-*` -> modules -> tasks).
  3. Downstream project adopters launching the exact same workbench on multi-subsystem codebases up to 100k+ lines, 500 tasks, and 200 documents.

## 2. Four Top-Bar Views & Scroll Archetypes

| Fixed Tab | Page Archetype | Scroll & Framing | Content Delivered |
|---|---|---|---|
| **1. `Overview`** (`导览`) | **Showcase & Orientation** | Natural page scroll, single centered white platter (`max-width: 1080px`) | Conditional pending-decision / awaiting-approval rows (inline downward expansion), repository one-liner, subsystem purpose & code-vs-doc breakdown, full-width `Mermaid` system flow diagrams, 3–4 essential reading entrypoints, and directory responsibility table (all doc links expandable inline). |
| **2. `Boundaries`** (`架构与边界`) | **Data Operations & Management** | Locked `100dvh` outer frame, inner platter scroll, sticky table headers, fixed `28px` status bar | Canvas filters (subsystem selector, `Issues only N`, sub-mode tabs: `Module Matrix` / `Dependency Map` / `Check Findings`) -> borderless tabular-numeric matrix with 6px status dots, LOC vs budget cap, violation/lag counts, Priority+ hidden-column header hints -> inline 12px-gapped white context card on row click. |
| **3. `Roadmap`** (`推进与溯源`) | **Data Operations & Management** | Locked `100dvh` outer frame, inner platter scroll, sticky `Domain > Milestone` path bar on scroll, fixed `28px` status bar | Canvas sub-modes (`Roadmap & Tasks` / `Lineage & ADRs` / `Git Diff & Tests`), status filters, collapsible domain/milestone tree (`1px` indent guide) plus swimlane SVG toggle -> clickable `SRC-*`/`ADR-*` trace table & capped provenance SVG -> Git ref diff comparison table with file status and line deltas. |
| **4. `Documents`** (`全库文档`) | **Long-Form Reading** | Natural page scroll (`min-height: 100dvh`), sticky document breadcrumb, grid `max-width: 1040px` | On-demand left vibrancy drawer (`Contents` / `Search` with focus-preserving filter / `Page Notes`) -> `700px` centered white reading platter (Markdown prose, callouts, anchor headings, embedded `Mermaid` SVG) -> `240px` right Tufte sidenotes rail aligned on canvas (moving inline at `<1024px`) -> temporary bottom-right `Back` button after cross-doc jumps. |

## 3. Anti-Jitter, Responsive Priority+ & Provenance Rules

- **Canvas vs Platter & Restraint**: Underlying `#F5F5F7` canvas holds quiet view filters and page-level summaries; only the main reading or working panel uses `#FFFFFF` with a subtle hairline border and natural shadow. Zero thick `border-left` callouts, card-in-card walls, duplicate top metric cards, table horizontal scrollbars (`overflow-x: auto`), hover-jump animations, or emojis.
- **Zero-Shift Fixed Controls**: Every scrollbar container reserves `scrollbar-gutter: stable`; `#topbar` locks `32px` height across a 3-column grid (`minmax(0, 1fr) auto minmax(0, 1fr)`) with fixed-width bold-reserved view tabs (`#btn-doc-drawer`, `#btn-run-tests`, `#btn-mark-reviewed`, `#btn-lang` keep fixed widths/positions and switch `disabled` in place rather than hiding or reflowing during `POST` updates); `@container topbar` collapses action buttons into the `···` vibrancy menu at `<= 1080px` so half-screens and `1024px` windows never collide with view tabs.
- **Container-Driven Table Collapsing**: Under `@container workspace`, `.col-pri-3` hides at `<= 1024px` and `.col-pri-2` also hides at `<= 680px`, showing exact hidden-column notes in table headers while clicking any row expands full 4-part context inline (with middle-truncated SHAs/paths and one-click copy).
- **Signal Separation & Language**: Every detail section separates `[Human quote & approval]`, `[AI-maintained spec]`, and `[Measured fact]`. Template-project defaults to plain Chinese in the browser (`web_default_lang`) with instant `EN` / `中文` switching and downstream `language` inheritance.

## 4. File Split & Line Budgets

Line-budget reminders are configured in [docs-policy.toml](../../docs-policy.toml) (`max_style_lines` for stylesheets, `max_source_lines` for scripts).

| Layer | File | Single Responsibility |
|---|---|---|
| Document shell | `scripts/projectlib/web/index.html` | Fixed `32px` topbar, 4 view hosts, `28px` statusbar, floating toast, and on-demand doc drawer |
| Design tokens | `scripts/projectlib/web/styles/tokens.css` | Authoritative CSS `:root` variables |
| Viewport & layout | `scripts/projectlib/web/styles/layout.css` | Page scroll archetypes, 3-col topbar grid, `@container` breakpoints, max-width caps |
| Controls & surfaces | `scripts/projectlib/web/styles/components.css` | Canvas filters, single platter, dots, buttons, toast, vibrancy popover & drawer |
| Tables & tree | `scripts/projectlib/web/styles/tables-and-inline.css` | Borderless `tabular-nums` tables, Priority+ column hiding, `1px` tree guides, 12px inline cards |
| Reading & SVG | `scripts/projectlib/web/styles/prose-and-svg.css` | Markdown prose, heading scroll margins, callouts, `240px` Tufte sidenotes, SVG strokes |
| Accessibility | `scripts/projectlib/web/styles/accessibility.css` | Visible `:focus-visible` outline and `prefers-reduced-motion` handling shared by every view |
| Copy & enum translators | `scripts/projectlib/web/js/i18n.js` | Plain ZH/EN dictionary, enum/rule translators, middle truncation, and SVG wrapping |
| Markdown & anchors | `scripts/projectlib/web/js/markdown.js` | Markdown/table/callout parser, `required-reading` anchors, heading scroll, relative doc-link resolution, and Tufte alignment |
| Diagram renderer | `scripts/projectlib/web/js/diagrams.js` | Local `Mermaid` flowchart and sequence SVG renderer |
| Topology charts | `scripts/projectlib/web/js/charts.js` | Timeline, capped provenance flow, domain bypass map, and module dependency SVGs |
| Context & sidenotes | `scripts/projectlib/web/js/drawer.js` | Subsystem digest, 4-part inline context cards, Markdown reader, and multi-kind Tufte sidenotes |
| Roadmap panels | `scripts/projectlib/web/js/roadmap_panels.js` | Provenance trace rows, latest test run card, and Git diff comparison table |
| View assembly | `scripts/projectlib/web/js/views.js` | Pure HTML string assembly and exact status counts for all 4 views |
| Keyboard & hover | `scripts/projectlib/web/js/interactions.js` | Esc closes the more menu or doc drawer and returns focus, Enter/Space toggles focusable rows, prose hover highlights sidenotes |
| State & routing | `scripts/projectlib/web/js/app.js` | Single `uiState` owner, non-destructive search updates, smooth refresh, jump history, CSRF writes |

## 5. Pre-Delivery Verification Scope

Before closing `T-204`, verify every item of [pre-delivery-ui-self-check](../contracts/frontend-and-visual-discipline.md#pre-delivery-ui-self-check) (principles, measured WCAG 2.2 AA contrast/keyboard/focus/motion baseline, and calm-platter preferences) across `540px`, `800px`, `1280px`, and `2560px+` viewports plus synthetic `500`-task / `4`-level / `200`-doc scale data in headless Chromium, `unittest`, and `check_docs.py --strict`.
