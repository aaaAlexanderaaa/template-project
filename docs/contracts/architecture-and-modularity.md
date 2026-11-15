---
doc_type: contract
status: current
authority: normative
---

# Architecture, Modularity & Style Ownership

<!-- required-reading: decomposition-and-ownership -->
## Five Pillars of Clear System & Module Architecture

A repository architecture is clear only when a human reader or new AI session can
inspect its structure and runtime behavior without reverse-engineering source
files. Every system or module architecture description must answer five
concrete parts:

1. **Positioning, Promises & Non-Goals (`ARCHITECTURE.md`)**: Who the system
   serves, what outcome it guarantees, and which work sits outside its boundary.
2. **End-to-End Runtime / Control Logic & Failure Paths**: How requests, state
   transitions, or governance gates run from trigger to completion, including
   failure handling and closed feedback loops (expressed as `mermaid` flowcharts
   or sequence diagrams). Static `import` graphs show module coupling only and
   leave runtime flow, state transitions, and gate conditions unexplained.
3. **Bounded Domains, Narrow Interfaces & Forbidden Couplings**: Which domains
   (`docs/specs/<domain>/README.md`) split the codebase, what maturity `stage`
   (`prototype | usable | stable`) governs each domain, what narrow interface
   crosses boundaries, and which cross-layer calls or state leaks are banned.
4. **Single Source of State & Hard Invariants / Constraints**: Which single
   file or store owns each core fact (`sources.toml`, specs, `work.toml`, DB),
   and what hard limits, human-approval gates, or compatibility rules hold.
5. **Module Entrypoints, Role Headers & Fitness Checks (`docs/specs/<domain>/<module>.md`)**:
   Which `owns` globs, `promise`, and `depends_on` edges define each module,
   what public entrypoint exposes it, the 2–3 line `# Role:` header at the top
   of core files stating owned duty, excluded duty, and governing spec/`SRC-*`/
   `ADR-*` anchor, and which automated checks enforce those boundaries.
<!-- /required-reading: decomposition-and-ownership -->

<!-- required-reading: single-source-of-state -->
## Single Source of State

Whenever a piece of state or configuration is read in more than one place:

- Name **one authoritative owner** (one table/file on disk, one backend domain
  owner, or one frontend state store / URL parameter).
- Compute derived views, counts, badges, and UI summaries mechanically from that
  owner instead of maintaining parallel mutable flags that drift out of sync.
- Lower-level and shared modules (`domain/`, `shared/`, `platform/`) never
  import upper feature or transport layers (`features/`, `app/`, HTTP/UI).
- **Explicit time and fixture isolation**: Pass explicit UTC timestamps or
  injected clock helpers across module boundaries instead of scattered local
  time calls, and keep demo or test fixtures separate from production data paths.
<!-- /required-reading: single-source-of-state -->

<!-- required-reading: anti-monolith -->
## Preventing Monolith Files & Catch-All Buckets

- **Split by cohesive responsibility before crossing file budgets**: Keep source
  files under `[budgets].max_source_lines` (default `500` lines; split plan
  required before growing oversized legacy files) and stylesheets under
  `[budgets].max_style_lines` (default `300` lines).
- **No dumping-ground directories**: Avoid `utils/`, `helpers/`, `common/`, or
  `misc/`. Name shared packages after the specific domain capability or mechanism
  they own (for example, `money/`, `markdown_frontmatter/`, `git_telemetry/`).
- Follow a clear layered module layout (illustrated in `template-project`'s `examples/reference-app/`: `domain/` → `shared/` → `features/<feature>/index.*` → `app/`).
<!-- /required-reading: anti-monolith -->

<!-- required-reading: css-modularity -->
## Frontend CSS Layering & Ownership

Once an interface grows beyond a single static page, CSS must be modularized
into three explicit layers:

1. **Design Tokens (`styles/tokens.css`)**: Single source for color palette,
   typography scale, spacing, radii, and elevation custom properties (`--*`).
   Feature stylesheets reference tokens rather than hardcoding hex colors.
2. **Base & Layout Shell (`styles/base.css` / `styles/layout.css`)**: Document
   resets and page-level structural regions only—zero feature-specific business
   classes.
3. **Component-Scoped Styles (`<Component>.module.css` or scoped component CSS
   colocated beside the component)**: Each component owns its own internal
   layout and states, exposing deliberate CSS custom properties or props when
   callers need controlled variation.
<!-- /required-reading: css-modularity -->
