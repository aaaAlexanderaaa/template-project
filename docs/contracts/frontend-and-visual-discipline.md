---
doc_type: contract
status: current
authority: normative
---

# Frontend, Visual Design & Data Presentation Discipline

<!-- required-reading: frontend-layers -->
## 1. Four Layers, Their Order, and the Approval Gate

Frontend quality in this discipline is built from four layers. Read and apply
them in this order; a lower layer never overrides a higher one:

| Layer | What it is | Who it binds | How to use it |
|---|---|---|---|
| **1. Principles** (Section 2) | Durable reasons that hold for any product: serve the reader's task, make hierarchy match importance, stay consistent, show status, prevent errors, stay accessible, present data honestly | Every project | Use them to decide cases no rule mentions, and to explain every design choice |
| **2. Best practices** (Section 3) | Established, mostly measurable standards that implement the principles: WCAG 2.2 AA, typography and grouping basics, Core Web Vitals, form and state design, perceptual rules for charts | Every project (non-negotiable baseline) | Check them with tools and measurements, not by eye |
| **3. Owner preferences** (Section 4) | The owner's chosen look and interaction style: palette, spacing, density, specific pixel values, banned decorative patterns | The project whose owner chose them | Apply as the default style; an adopting project's owner may replace them |
| **4. Reference practices** (Section 5) | Products and authors worth studying | Nobody directly | Learn the decision behind a reference; never copy its surface or cite it as the only reason |

- **Conflicts resolve upward**: When an owner preference conflicts with a best
  practice or principle, follow the higher layer and tell the owner plainly
  what changed and why. Example: the original tertiary ink `#868B96` measured
  3.14:1 against the canvas, below the WCAG AA 4.5:1 text minimum, so the
  default became `#6B7079` (4.57:1) while keeping the same light-gray role.
- **Deciding a new view**: (1) name the reader and the task
  ([information-organization.md](information-organization.md#reader-task-first)),
  (2) apply the principles, (3) check the best-practice baseline, (4) apply the
  owner preferences, (5) look at references for proven solutions to the same
  problem.
- **Approval gate**: Draft interface architecture and design options in
  `docs/design/` and run a pre-code `/grill` before locking a layout.
  Historical sketches or old UI files never count as owner consent while a
  design task stays `blocked` / `pending_owner_choice`.
- **Plain UI wording**: Match the repository's chosen language and translate
  internal enum values (`ready_for_check`, `stable`, `blocked`, `approved`)
  into ordinary words.
<!-- /required-reading: frontend-layers -->

<!-- required-reading: frontend-principles -->
## 2. Principles

1. **Serve the reader's task and comprehension budget**: Each view answers the
   questions its reader arrives with, in the order they need them. Organize
   screens with [information-organization.md](information-organization.md);
   orientation views follow a newcomer's progression:
   `Whole-Repo Purpose & Scope -> End-to-End Runtime / Control Flow & Constraints -> Subsystems & Promises -> Decisions & Active Work -> Full Documents & Source Files`.
2. **Visual hierarchy matches importance**: One primary focus per view.
   Secondary information recedes in size, weight, and contrast but stays
   visible and reachable. If everything is emphasized, nothing is.
3. **Consistency and predictability**: The same thing looks and behaves the
   same everywhere; controls keep their place; users recognize options instead
   of recalling hidden commands.
4. **Visible system status and honest feedback**: Users always know what is
   happening (loading, saving, saved, failed, empty, stale) and what the
   numbers on screen refer to.
5. **Prevent errors and allow recovery**: Make the safe action the easy one,
   confirm irreversible actions with their scope, and offer undo where it is
   cheap.
6. **Accessible to everyone by default**: Content is perceivable, operable,
   understandable, and robust for people using keyboards, screen readers,
   zoom, reduced motion, or color-vision differences.
7. **Honest data presentation**: Visual encodings never exaggerate or hide;
   every rate shows its numerator, denominator, and scope; provenance stays
   visible.
8. **Restraint**: Every element must earn its place by helping the reader's
   task (Tufte's data-ink ratio, Calm Technology). Decoration that carries no
   information is removed.
9. **Form follows content**: Choose page structure from the task density and
   content type (see the page archetypes in Section 4.3), not from a favorite
   template.
<!-- /required-reading: frontend-principles -->

<!-- required-reading: frontend-best-practices -->
## 3. Best-Practice Baseline (Mandatory in Every Project)

### 3.1 Accessibility (WCAG 2.2 Level AA)

- **Contrast**: Text at least `4.5:1` against its background (`3:1` for text
  `>= 24px`, or bold `>= 18.66px`); icons, focus rings, input borders, and chart
  marks that carry meaning at least `3:1`. Measure token pairs with a contrast
  calculator; do not judge by eye. Disabled controls are exempt but must still
  be recognizable.
- **Never rely on color alone**: Pair status colors with text, shape, or
  position (for example a `6px` dot plus a word).
- **Keyboard and focus**: Every action works with the keyboard in a logical
  order; focus is always visible (`:focus-visible` outline at least `2px` with
  `3:1` contrast); no keyboard traps; overlays return focus when closed.
- **Targets**: Pointer targets at least `24 x 24` CSS px or spaced so their
  centers are `24px` apart.
- **Semantics**: Use native elements (`button`, `a`, `label`, `table`,
  headings in order, landmarks) before ARIA; every input has a visible label;
  meaningful images and SVG diagrams have text alternatives.
- **Zoom and reflow**: Content stays usable at `200%` zoom and reflows at a
  `320` CSS px wide viewport without two-dimensional scrolling (data tables and
  diagrams excepted, with a usable alternative).
- **Motion**: Respect `prefers-reduced-motion`; nothing flashes more than three
  times per second.

### 3.2 Typography, Grouping & Layout

- Body line length about `45–75` Latin characters (about `25–40` CJK
  characters); body line height `1.4–1.7` (use the upper end for CJK).
- A small type scale (about four to six sizes) applied consistently; numbers in
  tables and counters use `font-variant-numeric: tabular-nums`.
- Group related items by proximity, similarity, and alignment (Gestalt
  principles) before adding borders or boxes; use one spacing scale (for
  example multiples of `4px`).
- Font stacks include system fonts for every script the product displays
  (Latin and CJK).

### 3.3 Performance & Stability

- Meet Core Web Vitals "good" thresholds on real pages: Cumulative Layout Shift
  `< 0.1`, Interaction to Next Paint `< 200ms`, Largest Contentful Paint
  `< 2.5s`.
- Reserve space for content that loads later; keep stale data visible while
  refreshing instead of blanking the screen.

### 3.4 States, Forms & Interaction

- Design every state of every view: loading, empty, partial, error, offline,
  and success. Error messages say what happened and what the user can do.
- Forms keep visible labels, validate next to the field, preserve input after
  errors, and provide sensible defaults.
- Destructive or irreversible actions show their scope and ask for
  confirmation; reversible actions prefer undo.
- Use Nielsen's ten usability heuristics as a review lens for new flows.

### 3.5 Data Visualization & Honest Provenance

- Choose encodings by perceptual accuracy: position, then length, then angle
  or area, then color intensity (Cleveland & McGill, 1984). Bar charts start at
  zero; axes and units are labeled; label lines directly instead of using
  distant legends when possible; use color-blind-safe palettes.
- Include a diagram only when spatial relationships explain faster than prose.
  Verify actual SVG bounds on rendered pages so labels never clip or collide.
- State numerator, denominator, and scope beside every displayed rate; keep
  every filter badge, counter, and chart mark equal to the underlying data.
- Keep three signal classes visually and structurally distinct:
  1. **Physical repository facts** (Git commits, static imports, file line
     counts, test runner exit codes);
  2. **AI-maintained structured records** (module specs, `SRC-*` links,
     `ADR-*` decisions, `work.toml` task state);
  3. **Human decisions and approvals** (`human_check = "approved"` and verbatim
     choices on blocked tasks).
- When source commits move ahead of their owning spec, show the exact domain
  and commit lag rather than synthetic summary prose.

### 3.6 Internationalization

- No text inside images; layouts tolerate text expansion between languages;
  dates, numbers, and times use the reader's locale and time zone.
<!-- /required-reading: frontend-best-practices -->

<!-- required-reading: owner-preferences -->
## 4. Owner Preferences: Default Calm-Platter Style

This section records the template owner's aesthetic preferences. It ships as the **default style** for adopting projects.
An adopting project's owner may replace any part of it by recording their own
preferences in `docs/design/` (or an ADR linked to their `SRC-*` quote).
Replacing preferences never removes Sections 2 and 3. Each preference below
names the principle it serves, so a replacement can keep the reasoning while
changing the look.

### 4.1 Visual Approach

| Dimension | Preference | Serves principle |
|---|---|---|
| **Visual hierarchy** | Secondary filters and helper captions sit directly on a soft neutral gray `--bg-canvas` without borders or shadows; only the active main workspace sits inside one white `--bg-platter` surface with a subtle shadow; menus and popovers use translucent blur. Avoid full-screen `1px` line grids and nested card-in-card walls. | 2 Hierarchy, 8 Restraint |
| **Attention** | Remove decorative borders, colorful pill walls, and ornamental icons; core data in the center, secondary hints muted at the edges (`--ink-secondary` / `--ink-tertiary`), full detail on hover or click. | 2 Hierarchy, 8 Restraint |
| **Spatial consistency** | Fixed visible entrypoints in an unchanging order; disable temporarily unavailable controls in place instead of hiding or reordering them; no memorized-shortcut-only or `Cmd+K`-only commands. | 3 Consistency |
| **Window scaling** | Centered `max-width` workspace; as windows narrow (`3440px -> 1200px -> 800px -> 500px`), collapse side drawers and secondary table columns by business priority and move overflowing toolbar buttons, in order, into a trailing `···` menu. | 1 Reader task, 3 Consistency |
| **Long-form notes** | On wide screens (`>= 1024px`) annotations sit in the right canvas margin beside their paragraph; on narrow windows they open inline or in an anchored popover. | 1 Reader task |

### 4.2 Six Trade-Off Rules

1. **Discoverable yet clean**: Keep brief, quiet, visible entrypoints in fixed
   coordinates (top text menu, row action affordance, `"3 columns hidden"`
   header notice, `3/8` parent progress counts); tuck large edit forms,
   low-frequency settings, and machine-long identifiers (`UUID`, `SHA256`, full
   paths) inside click-to-expand layers. Move trailing toolbar actions into the
   `···` menu only when one row cannot fit them.
2. **Focus without shouting; never duplicate data on one screen**: Simplify
   surrounding chrome instead of using oversized numbers or saturated badges.
   Never show the same count or metric twice in one viewport. Omit vertical
   table gridlines; dense management pages use grayscale ink plus `6px`
   low-saturation status dots (soft low-saturation backdrop gradients only on
   light orientation pages).
3. **Keep capability, cut steps**: Sensible defaults for 80% of workflows,
   rare flags under `"Advanced"`, inline edits with safe auto-save instead of
   `"Edit -> Modal -> Edit -> Save"` chains, batch bars only while `>= 1` item is
   selected, and scope confirmation before irreversible writes.
4. **Zero pixel shift**: Navigation, menus, and action buttons keep a fixed
   order. Switching tabs, toggling checkboxes, counts changing from `1` to
   `9,999`, or a scrollbar appearing produce `0px` topbar or toolbar shift:
   - `scrollbar-gutter: stable` on scroll containers;
   - a 3-column topbar grid `grid-template-columns: minmax(0, 1fr) auto minmax(0, 1fr)` for centered tabs;
   - fixed widths or hidden bold pseudo-elements for bold-on-active tabs;
   - `tabular-nums` on numbers.
5. **One centered workspace for large data and deep nesting**: Avoid splitting
   wide screens into three or four cramped panes. Nested trees draw `1px`
   `--hairline` indentation guides, stick the active parent breadcrumb at the
   top, and expand a complex item inline into a white card with `12px` margin;
   cross-document jumps show a temporary `Back to ...` button.
6. **Desktop windows of every size**: Keep compact `14px` desktop type in
   narrow windows:
   - `< 680px`: single column, topbar `"View Select + 1 primary action + ···"`, `2–3` table columns, notes in drawers;
   - `680–1024px`: single-column platter, `4–5` table columns;
   - `1024–1440px`: reading prose `680–720px` plus a `220–260px` note rail; management platter `1040–1180px`;
   - `> 1440px`: centered caps (`<= 1200px` management, `<= 1080px` reading); ordinary tables never use `overflow-x: auto` (reserved for 12+ column audit tables).

### 4.3 Four Page Archetypes

| Page Archetype | Use Cases | Scroll Mechanics | Topbar & Navigation | Type & Color Restraint |
|---|---|---|---|---|
| **1. Data Operations & Management** | Dashboards, boundary/route tables, nested task queues, Git diff tables | Outer shell locked to `100dvh`; inner list scrolls with sticky `thead` and a `28px` bottom status bar (`Shown X / Total Y`). | `32px` single-row topbar; under `680px` becomes `"View Select + 1 button + ···"`. | Compact sans-serif with `tabular-nums`; tables without vertical lines; `6px` status dots; no background gradients. |
| **2. Long-Form Reading & Research** | Technical specs, ADRs, source walkthroughs, knowledge docs | Natural page scroll (`min-height: 100dvh`) with a sticky chapter breadcrumb. | `32px` topbar + one on-demand left drawer (TOC, search, notes). | Optional serif `h1` + sans body; right-margin sidenotes at `>= 1024px`, inline when narrow; `--highlight-wash` highlights. |
| **3. Lightweight Utility** | Converters, short wizards, setup forms | Single centered platter when short; natural scroll when taller. | Minimal single-row nav or direct centered platter. | Required inputs + 1 primary button by default; rare options under `"Advanced"`. |
| **4. Showcase & Orientation** | Repo landing overview, architecture onboarding, portfolios | Natural page scroll; grids adapt column count via `@container`. | Clean topbar or fixed-width segmented tabs (`0px` shift). | Calm heading scale; restrained edge tints only when density is low. |

### 4.4 Default Tokens and Banned Decorative Patterns

Keep all color literals inside `tokens.css`; component and layout sheets use
CSS custom properties. Default palette (soft gray canvas with deep charcoal
ink, not pure white with pure black):

```css
:root {
  --bg-canvas: #F5F5F7;
  --bg-platter: #FFFFFF;
  --bg-subtle-hover: rgba(0, 0, 0, 0.035);
  --bg-vibrancy: rgba(255, 255, 255, 0.78);
  --ink-primary: #1D1D1F;   /* 15.5:1 on canvas */
  --ink-secondary: #51555E; /* 6.9:1 on canvas */
  --ink-tertiary: #6B7079;  /* 4.57:1 on canvas; raised from #868B96 (3.14:1) to meet 4.5:1 */
  --hairline: rgba(0, 0, 0, 0.065);
  --control-border: #868B96; /* 3.1:1 on canvas: input & control border >= 3:1 */
  --platter-border: rgba(0, 0, 0, 0.05);
  --platter-shadow: 0 1px 2px rgba(0, 0, 0, 0.03), 0 6px 20px rgba(0, 0, 0, 0.035);
  --popover-shadow: 0 4px 12px rgba(0, 0, 0, 0.06), 0 16px 36px rgba(0, 0, 0, 0.08);
  --accent-primary: #2F5D8A;
  --status-ok: #3B7A57;
  --status-warn: #B87333;   /* 3.5:1: use for dots and icons, not for small text */
  --status-err: #B84040;
  --highlight-wash: rgba(47, 93, 138, 0.08);
  --radius-platter: 10px;
  --radius-control: 6px;
  --topbar-height: 32px;
  --statusbar-height: 28px;
}
```

- **Long fields, refresh, and empty states**: UUIDs, 40-char SHAs, and full
  paths live in click-expanded details; necessary inline IDs use middle
  truncation (`prod-gw...8f2a`) with hover full text and copy. Keep data on
  screen during refresh (stale-while-revalidate) with only a `2px` progress
  line under the topbar. Empty results show plain text plus `[Clear filters]`,
  without illustrations or emoji.
- **Banned patterns and replacements**:
  - Thick colored left borders (`border-left: 4px solid ...`) and colorful pill walls -> quiet tinted notes or `1px` full hairline borders, and `6px` status dots with `--ink-primary` labels.
  - Duplicate metrics on one screen -> show counts once in filter tabs, table headers, or the `28px` status bar.
  - Nested cards or default 3-column equal card grids -> one white platter with whitespace, type hierarchy, and inset `1px` `--hairline` dividers.
  - Lazy `overflow-x: auto` on ordinary tables -> hide low-priority columns via `@container`, show `"N columns hidden"`, reveal fields inline.
  - Blue-purple gradients, neon glow borders, marketing hero slogans on internal tools, hover-lift card bounce, number-ticker animations, decorative emoji -> `120–160ms` background/opacity transitions and plain text prefixes (`Questionable ·`).
<!-- /required-reading: owner-preferences -->

<!-- required-reading: reference-practices -->
## 5. Reference Practices

Study these for the decision they demonstrate. When citing one in a design
discussion, name the principle or best practice it illustrates; a product name
alone is never the reason for a choice.

| Reference | What to learn from it | Do not copy |
|---|---|---|
| Apple Human Interface Guidelines; macOS System Settings, Things 3, Craft | Canvas-versus-content hierarchy, restraint, native control behavior | Platform-specific chrome and brand look on the web |
| Mark Weiser & John Seely Brown, Calm Technology; Edward Tufte, data-ink ratio and sidenotes | Moving secondary information to the periphery; removing non-data ink; notes beside text | Minimalism that hides needed controls |
| Jef Raskin, *The Humane Interface*; macOS `NSToolbar` | Spatial consistency, modelessness, recognition over recall | Desktop-only assumptions where touch or keyboard users exist |
| Linear desktop app, TablePlus | Priority-based collapse, dense tables, fast keyboard paths alongside visible controls | Keyboard-only discovery |
| Readwise Reader, Stripe Docs | Long-form reading width, margin notes, code and prose side by side | Marketing layouts on documentation |
| GOV.UK Design System | Plain content, accessible components, form patterns tested with real users | Government branding |
| IBM Carbon (data tables), Material Design 3 (states) | Documented table, empty, loading, and error state patterns | Their visual style when it conflicts with the project's preferences |
| Nielsen Norman Group usability heuristics | A shared review vocabulary for usability problems | Heuristics as a checklist that replaces watching real use |
<!-- /required-reading: reference-practices -->

<!-- required-reading: pre-delivery-ui-self-check -->
## 6. Pre-Delivery UI Self-Check

Before handing back any created or modified frontend surface, verify on the
live rendered UI:

**Principles and information organization**

1. **Reader task**: A first-time reader can tell within 30 seconds what the view
   is for and complete its primary task; the view has one clear focus.
2. **States**: Loading, empty, error, and stale states are designed and their
   counts match the underlying data.

**Best-practice baseline (measure, do not eyeball)**

3. **Contrast**: Every text/background token pair in use measures `>= 4.5:1`
   (large text `>= 3:1`); meaningful non-text marks `>= 3:1`.
4. **Keyboard and focus**: All actions reachable by keyboard in a logical
   order with visible focus; overlays return focus; no traps.
5. **Zoom, motion, and stability**: Usable at `200%` zoom; reduced motion
   respected; no visible layout shift during tab switches, row toggles, count
   changes (`1 -> 9,999`), or scrollbar appearance.

**Owner preferences (default calm-platter style unless the project's owner replaced it)**

6. **Multi-width sweep**: At `540px`, `800px`, `1280px`, and `2560px+`: no
   topbar wrapping, no horizontal scrollbars on normal tables, centered caps
   (`<= 1200px` management / `<= 1080px` reading).
7. **Real data scale**: With `500` rows, `4`-level nesting, and `200` doc pages,
   management views lock `100dvh` with inner scrolling and reading views scroll
   naturally, with sticky headers, breadcrumbs, and topbar controls reachable.
8. **No duplication or raw noise**: No duplicate metrics; no uncollapsed
   UUIDs, hashes, or full paths on main surfaces; secondary hints muted.
9. **Banned-style scan**: No decorative emoji, thick `border-left` callouts,
   nested card walls, neon or purple gradients, hover-jump or ticker
   animations.
<!-- /required-reading: pre-delivery-ui-self-check -->
