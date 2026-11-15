---
doc_type: contract
status: current
authority: normative
---

# Frontend, Visual Overview & Data Presentation Discipline

<!-- required-reading: reader-context-encapsulation -->
## 1. Reader Background, Five Industry Standards & Approval Gate

Design every user interface, operational dashboard, or project overview around
its reader's comprehension budget and align with five established desktop
interaction standards rather than marketing landing-page templates or
high-contrast default component kits:

- **Follow newcomer comprehension order, not raw internals**: Organize top
  orientation views in a reader's natural progression:
  `Whole-Repo Purpose & Scope -> End-to-End Runtime / Control Flow & Constraints -> Subsystems & Promises -> Decisions & Active Work -> Full Documents & Source Files`.
- **Keep unapproved structures blocked until explicit owner sign-off**: Draft
  interface architecture and design options in `docs/design/` via pre-code
  `/grill` before locking a layout; historical sketches or old UI files never
  count as owner consent while a design task stays `blocked` / `pending_owner_choice`.
- **Plain UI wording (zero raw enum leaks)**: Match the repository's chosen
  language and translate internal enum values (`ready_for_check`, `stable`,
  `blocked`, `approved`) into ordinary everyday wording.

| Dimension | Reference Standard & Products | Concrete Practice | Problem Solved |
|---|---|---|---|
| **Visual hierarchy** | **Apple Human Interface Guidelines** (macOS System Settings, Things 3, Craft) | Place secondary filters and helper captions directly on a soft neutral gray `--bg-canvas` without borders or shadows; place only the active main workspace inside one pure-white `--bg-platter` surface with subtle shadow; use translucent blur vibrancy for menus and popovers. | Avoids full-screen `1px` line grids and nested card-in-card walls. |
| **Attention management** | **Calm Technology** (Mark Weiser) + **Data-Ink Ratio** (Edward Tufte) | Remove decorative borders, colorful pill spam, and ornamental icons; center core data while placing secondary hints and structure at muted edges (`--ink-secondary` / `--ink-tertiary`), expanding full detail on hover or click. | Reduces visual fatigue while keeping secondary context immediately reachable. |
| **Spatial consistency** | **Recognition over Recall** + **Spatial Consistency** (Jef Raskin; macOS Menu Bar & `NSToolbar`) | Keep fixed, visible entrypoints in an unchanging order; disable temporarily unavailable controls in place rather than hiding or reordering them; avoid requiring memorized keyboard shortcuts or `Cmd+K`-only commands. | Matches names, positions, and active state to protect user muscle memory. |
| **Window scaling** | **Intrinsic Web Design** (CSS `@container`) + **Priority+ Progressive Collapse** (Linear desktop, TablePlus) | Enforce a centered `max-width` workspace cap; as desktop windows narrow (`3440px -> 1200px -> 800px -> 500px`), collapse side drawers and secondary table columns by business priority and move overflowing toolbar buttons in original order into a trailing `···` menu. | One desktop implementation adapts cleanly across 1/3 split panes, half-screens, laptops, and 34" ultrawide monitors. |
| **Long-form notes** | **Tufte Sidenotes** (Readwise Reader, Stripe Docs) | On wide screens (`>= 1024px`), align annotations and provenance notes in the right `--bg-canvas` margin beside the owning prose paragraph; on narrow windows, expand inline beneath the current line or in an anchored popover without jumping to the bottom. | Lets readers inspect context and references without losing reading position. |
<!-- /required-reading: reader-context-encapsulation -->

<!-- required-reading: visual-restraint-and-geometry -->
## 2. Trade-Off Rules, Page Archetypes, CSS Tokens & Breakpoints

### 2.1 Six Core Trade-Off Rules

1. **Balance discoverability and clean screens**: Keep brief, quiet, visible
   entrypoints in fixed coordinates (top text menu, row action affordance,
   `"3 columns hidden"` table header notice, `3/8` parent progress counts), and
   tuck large edit forms, low-frequency settings, and machine-long identifiers
   (`UUID`, `SHA256`, full file paths) inside click-to-expand layers. Move trailing
   toolbar actions into the right-hand `···` menu only when one row cannot fit them.
2. **Focus attention cleanly — never duplicate identical data on one screen**:
   Simplify surrounding chrome rather than shouting with oversized numbers or
   saturated badges. Never display identical counts or metrics twice in the same
   viewport (e.g., omit summary stat cards above a table that already shows those
   status counts in filters, headers, or the bottom bar). Omit vertical table
   gridlines and restrict dense management pages to grayscale ink plus `6px`
   low-saturation status dots (soft low-saturation backdrop gradients belong
   strictly on light orientation/showcase pages).
3. **Preserve capability while cutting steps**: Supply sensible defaults for 80%
   workflows and fold rare flags under `"Advanced"`. Support direct inline
   actions/edits and auto-save where safe instead of multi-step `"Edit -> Modal ->
   Edit -> Save"` chains; reveal batch action bars only while `>= 1` item is
   selected, and require clear scope confirmation modals before irreversible writes
   or deletions.
4. **Protect spatial muscle memory (zero pixel shift)**: Keep navigation tabs,
   menus, and action buttons in fixed order (never sort dynamically by frequency).
   Switching tabs, toggling row checkboxes, changing counts from `1` to `9,999`,
   or revealing a vertical scrollbar MUST produce `0px` topbar or toolbar shift:
   - Apply `scrollbar-gutter: stable` on scroll containers.
   - Use a 3-column grid `display: grid; grid-template-columns: minmax(0, 1fr) auto minmax(0, 1fr)` on centered-tab topbars.
   - Give bold-on-active text tabs fixed widths or hidden bold pseudo-element width reservations.
   - Apply `font-variant-numeric: tabular-nums` to all numeric columns, counts, timings, versions, and ratios.
5. **Handle large datasets and deep nesting in one centered workspace**: Avoid
   splitting wide screens into 3–4 cramped side-by-side panes:
   - **Nested trees/lists**: Draw `1px` `--hairline` vertical indentation guides; stick the active parent breadcrumb (`Domain > Milestone`) at the top during deep scrolling; clicking a complex item expands it downward inline into a white editing/detail card with `12px` vertical margin top and bottom so it stays visually separated from sibling rows.
   - **Cross-document jumps**: When following an internal link or TOC anchor to another section or file, display a temporary corner `Back to ...` button that disappears after one click.
6. **Adapt across desktop window sizes cleanly**: Keep compact `14px` desktop
   typography even in narrow split windows rather than enlarging buttons to
   mobile touch proportions:
   - **`< 680px` (1/3 side split)**: Single column (`12–16px` outer gutter); topbar condenses into `"View Select + 1 primary action + ···"`; tables retain `2–3` critical columns (remaining fields open inline on row click); TOC and notes open in an overlay drawer or inline block.
   - **`680px – 1024px` (half-screen)**: Compact desktop typography (`14px` prose), single-column platter (no permanent left+right sidebars), `4–5` core table columns, machine-long strings inside row details.
   - **`1024px – 1440px` (laptop / standard)**: Reading view `680–720px` prose centered alongside a `220–260px` right Tufte sidenote rail; management platter centered between `1040px` and `1180px`.
   - **`> 1440px` (ultrawide / 34")**: Strict centered `max-width` cap leaving `--bg-canvas` margins (`<= 1200px` management platter; `<= 1080px` reading prose + sidenotes combined; never expand `width: 100%` edge-to-edge). Ordinary tables forbid default `overflow-x: auto` horizontal scrollbars (reserve horizontal scroll strictly for 12+ column raw audit wide tables).

### 2.2 Four Page Archetypes

Assign every new view explicitly to one archetype matching its task density:

| Page Archetype | Use Cases | Scroll Mechanics | Topbar & Navigation | Type & Color Restraint |
|---|---|---|---|---|
| **1. Data Operations & Management** |Dashboards, boundary/route tables, nested task queues, Git diff tables | Outer shell locked to `100dvh`; inner list scrolls cleanly with sticky table `thead` and a fixed `28px` bottom status bar (`Shown X / Total Y`). | `32px` fixed single-row topbar; collapses cleanly to `"View Select + 1 button + ···"` under `680px`. | Compact sans-serif with `tabular-nums`; vertical-line-free tables; `6px` status dots; zero background gradients. |
| **2. Long-Form Reading & Research** | Multi-page technical specs, ADRs, source walkthroughs, knowledge docs | Natural page scroll (`min-height: 100dvh`) with a sticky current document/chapter breadcrumb bar. | `32px` persistent topbar + one on-demand left slide-over drawer (switching TOC, search, and note index inside). | Optional modern serif `h1` + sans body; right margin Tufte sidenotes on `--bg-canvas` (`1px` hover connector) at `>= 1024px`, inline/popover when narrow; `--highlight-wash` highlights. |
| **3. Lightweight Utility** | Format converters, short wizards, focused setup forms | Single centered platter when short; natural page scroll when taller than viewport. | Minimal single-row nav or direct centered platter. | Generous whitespace; show required inputs + 1 primary button by default; hide rare options in `"Advanced"`. |
| **4. Showcase & Orientation** | Repo landing overview, architecture onboarding, portfolios | Natural page scroll; internal grids adapt column count via `@container`. | Clean topbar or centered fixed-width segmented tabs (`0px` shift). | Calm heading scale; restrained edge tints permitted only when screen density is low. |

### 2.3 Canonical `:root` CSS Tokens, Refresh & Banned Patterns

Keep all color literals inside `tokens.css` (consuming CSS custom properties in
component/layout sheets) using a soft gray canvas paired with deep charcoal
ink rather than `#FFFFFF` background paired with `#000000` black:

```css
:root {
  --bg-canvas: #F5F5F7;
  --bg-platter: #FFFFFF;
  --bg-subtle-hover: rgba(0, 0, 0, 0.035);
  --bg-vibrancy: rgba(255, 255, 255, 0.78);
  --ink-primary: #1D1D1F;
  --ink-secondary: #51555E;
  --ink-tertiary: #868B96;
  --hairline: rgba(0, 0, 0, 0.065);
  --platter-border: rgba(0, 0, 0, 0.05);
  --platter-shadow: 0 1px 2px rgba(0, 0, 0, 0.03), 0 6px 20px rgba(0, 0, 0, 0.035);
  --popover-shadow: 0 4px 12px rgba(0, 0, 0, 0.06), 0 16px 36px rgba(0, 0, 0, 0.08);
  --accent-primary: #2F5D8A;
  --status-ok: #3B7A57;
  --status-warn: #B87333;
  --status-err: #B84040;
  --highlight-wash: rgba(47, 93, 138, 0.08);
  --radius-platter: 10px;
  --radius-control: 6px;
  --topbar-height: 32px;
  --statusbar-height: 28px;
}
```

- **Long fields, smooth refresh & empty states**: Keep UUIDs, 40-char SHAs, and
  full paths inside click-expanded cards; format necessary inline IDs with
  middle truncation (`prod-gw...8f2a`) plus hover full text and copy action. Keep
  existing data on screen during filter changes or periodic refreshes
  (`Stale-While-Revalidate`) with only a `2px` progress bar along the bottom edge
  of the topbar. Render empty search/filter results with plain text explanation
  plus a `[Clear filters]` action (no illustrations or emojis), and keep every
  filter badge and status counter identical to underlying filtered totals.
- **Forbidden patterns and approved replacements**:
  - Forbid thick colored left borders (`border-left: 4px solid ...`) and colorful pill walls -> use quiet tinted notes or `1px` full hairline borders, and `6px` low-saturation status dots with `--ink-primary` labels.
  - Forbid duplicate metrics on the same screen -> display counts once inside filter tabs, table headers, or the `28px` status bar.
  - Forbid nested cards inside cards or default 3-column equal card grids -> keep one `#FFFFFF` platter with internal whitespace, typography hierarchy, and inset `1px` `--hairline` horizontal dividers.
  - Forbid lazy `overflow-x: auto` horizontal scrollbars on ordinary tables -> progressively hide low-priority columns via `@container`, display `"N columns hidden"` in the header, and reveal full fields inline on click.
  - Forbid blue-purple gradients, neon glow borders, marketing hero slogans on internal tools, hover-lift (`translateY`) card bounce, number-ticker animations, or decorative emoji icons -> allow only `120–160ms` background/opacity transitions and plain text prefixes (e.g. `Questionable ·`).
<!-- /required-reading: visual-restraint-and-geometry -->

<!-- required-reading: honest-telemetry -->
## 3. Honest Data Provenance & Chart Clarity

Keep three signal classes visually and structurally distinct in every view:

1. **Physical repository facts** (Git commits, static AST imports, file line
   counts, and test runner exit codes);
2. **AI-maintained structured records** (module specs, `SRC-*` links, `ADR-*`
   decisions, and `work.toml` task state);
3. **Human decisions and approvals** (`human_check = "approved"` and verbatim
   choices on blocked tasks).

Include a diagram only when spatial dependencies clarify flow faster than prose.
Verify actual SVG bounds and rendered pages so labels never clip or collide, and
state explicit numerator, denominator, and scope alongside every displayed rate.
When source commits move ahead of their owning spec, display the exact domain
and commit lag directly rather than inventing synthetic summary prose.
<!-- /required-reading: honest-telemetry -->

<!-- required-reading: pre-delivery-ui-self-check -->
## 4. Six-Item Pre-Delivery UI Self-Check

Before handing back any created or modified frontend surface, verify all six
checks on the live rendered UI:

1. **Multi-width sweep**: Inspect `540px`, `800px`, `1280px`, and `2560px+` to confirm zero topbar wrapping, zero horizontal scrollbars on normal tables, and centered `max-width` platter caps (`<= 1200px` management / `<= 1080px` reading).
2. **Real data scale**: Validate with `500` rows, `4`-level nesting, and `200` doc pages that management views lock `100dvh` with inner list scrolling while reading views scroll naturally, with sticky headers, parent breadcrumbs, and topbar controls always reachable.
3. **Zero layout shift**: Verify tab switches, row checkboxes, count transitions (`1 -> 9,999`), and scrollbar appearance produce `0px` topbar/button shift.
4. **No duplication or raw surface noise**: Confirm zero duplicate metrics on screen, no uncollapsed UUIDs/hashes/full paths on main table surfaces, and muted secondary hints.
5. **Visible affordances & count parity**: Confirm fixed visible entrypoints (disabled in place when inapplicable) and exact parity between displayed counts, empty-state text, and filtered records.
6. **Banned-style scan**: Confirm zero decorative emojis, zero thick `border-left` callouts, zero nested card walls, zero neon/purple gradients, and zero hover-jump or ticker animations.
<!-- /required-reading: pre-delivery-ui-self-check -->
