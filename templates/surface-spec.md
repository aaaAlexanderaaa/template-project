---
id: ui.example-surface
domain: example
kind: surface-spec
summary: "{{Who reads/uses this screen and what job it helps them complete}}"
promise: "{{Context encapsulation, calm single-platter layout, and interaction guarantee}}"
owns:
  - "src/ui/example/**"
depends_on:
  - example.module
sources:
  - SRC-001
---

# {{Surface Title}}

## 1. Owner Design Approval Gate & Archetype

- **Design Status**: `pending_owner_choice` (change to `approved` only after explicit owner selection; block any UI task in `docs/work.toml` while pending; historical sketches never count as consent).
- **Approved Option & Reference**: {{Selected layout option and link to `SRC-*` confirmation}}
- **Page Archetype**: {{Pick one: `Data Operations & Management` (`100dvh` outer lock + inner scroll + `28px` status bar) | `Long-Form Reading` (`min-height: 100dvh` scroll + right Tufte sidenotes) | `Lightweight Utility` | `Showcase & Orientation`}}

## 2. Target Reader & Calm Hierarchy

- **Target reader / user persona**: {{Reader background and exact first-screen questions answered}}
- **Canvas vs Platter Split**: {{What quiet filters/hints sit directly on `--bg-canvas` (`#F5F5F7`) vs what sits inside the single `--bg-platter` (`#FFFFFF`), keeping zero same-screen duplicate stats and no card-in-card walls}}
- **Priority+ Responsive Breakpoints (`@container`)**: {{Exact behavior across `<680px` (1/3 split + `···` overflow + 2–3 cols), `680–1024px`, `1024–1440px`, and `>1440px` (`max-width <= 1200px` / `<= 1080px`), hiding low-priority table columns rather than adding horizontal scrollbars}}
- **Anti-Jitter & Long Fields**: {{`scrollbar-gutter: stable`, fixed-width tabs, `tabular-nums`, middle truncation + click-to-expand details for UUID/SHA/paths, and disabled-in-place controls}}

## 3. Data Provenance, Layered CSS & Self-Check

- **Authoritative data & styles**: {{Truthful distinction of physical facts / AI specs / human approvals; `:root` tokens isolated in `tokens.css`; component CSS `<= 300` lines; zero thick `border-left` banners, emojis, or hover-jump animations}}
- **Verification**: Verified against the 6-item pre-delivery self-check (`docs/contracts/frontend-and-visual-discipline.md#pre-delivery-ui-self-check`) across `540px`, `800px`, `1280px`, and `2560px+`.
