---
id: ADR-005
kind: decision
status: current
title: "Adopt five-standard calm-platter Frontend Design Specification and rebuild Perspective Web UI"
sources:
  - SRC-010
  - SRC-011
  - SRC-012
  - SRC-013
affects:
  - discipline.entry-and-contracts
  - discipline.guides-and-skills
  - discipline.templates
  - exemplar.shared
  - exemplar.checkout
  - perspective.context-pack
  - perspective.server
  - ui.perspective-web
supersedes: []
---

# ADR-005: Adopt Five-Standard Calm-Platter Frontend Design Specification & Rebuild Perspective Web UI

- **Context & problem**:
  Task `T-204` held the local Perspective Web UI frozen pending explicit owner choice ([ADR-004](ADR-004-discipline-first-architecture-and-open-closed-loop-review.md)). In `SRC-013`, the owner supplied a complete **Frontend Design Specification** aligned across five industry standards and instructed both incorporating it into the template's normative frontend rules and rebuilding `scripts/projectlib/web/` to match it.
- **Chosen approach**:
  1. Expand [frontend-and-visual-discipline.md](../contracts/frontend-and-visual-discipline.md), [surface-spec.md](../../templates/surface-spec.md), and [surface-spec.zh.md](../../templates/surface-spec.zh.md) to codify:
     - **Five reference standards**: Apple HIG canvas-vs-single-platter hierarchy (`#F5F5F7` / `#FFFFFF` + vibrancy popovers), Calm Technology + Tufte Data-Ink Ratio, Jef Raskin / `NSToolbar` spatial consistency (fixed `32px` bar, fixed control order, disabled-in-place), Intrinsic Web Design `@container` + Priority+ progressive collapse (`<680px` / `680-1024px` / `1024-1440px` / `>1440px`), and Tufte Sidenotes for long-form reading.
     - **Six core trade-off rules & four page archetypes**: Data Operations & Management (`100dvh` outer frame, inner scroll, `28px` status bar), Long-Form Reading (`min-height: 100dvh` natural scroll + right margin notes), Lightweight Utility, and Showcase & Orientation.
     - **Exact `:root` CSS tokens, anti-jitter layout constraints (`scrollbar-gutter: stable`, 3-column topbar grid, fixed tab widths, `tabular-nums`), seven banned patterns, and a 6-item pre-delivery self-check**.
  2. Rebuild `scripts/projectlib/web/` as a 4-view `NSToolbar` workbench (`导览 / 架构与边界 / 推进与溯源 / 全库文档`), moving legacy prototype drafts to approved implementation and re-enabling `scripts/projectlib/web/` distribution in `project.py init`.
  3. Align `examples/reference-app` tokens with the canonical `--bg-canvas` / `--bg-platter` / `--ink-*` token set while keeping backward-compatible token aliases for `CheckoutCard`.
- **Trade-offs & rejected alternatives**:
  - Rejecting marketing-style hero banners, duplicate stat cards above tables, `border-left` colored callouts, nested card-in-card walls, lazy horizontal `overflow-x: auto` table scrollbars, and permanent 3–4 narrow columns keeps multi-scale complex repositories (from `template-project` up to 100k+ LOC repos) calm, spatially stable, and legible from `540px` splits up to `3440px` displays.
