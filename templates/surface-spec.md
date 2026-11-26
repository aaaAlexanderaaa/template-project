---
id: ui.example-surface
domain: example
kind: surface-spec
summary: "{{Who reads/uses this screen and what job it helps them complete}}"
promise: "{{What the reader can always find, do, and trust on this screen}}"
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
- **Page Archetype**: {{Pick one: `Data Operations & Management` | `Long-Form Reading` | `Lightweight Utility` | `Showcase & Orientation` (see `docs/contracts/frontend-and-visual-discipline.md`, Section 4.3)}}

## 2. Reader, Task & Information Organization (Principles)

- **Target reader and first questions**: {{Reader background, what they already know, and the exact questions the first screen answers}}
- **Primary task and single focus**: {{The one main thing this screen helps the reader do, and what is deliberately secondary}}
- **Organizing scheme and layers**: {{How content is grouped at each level (task, topic, time, ...), what sits in the summary / working / detail layers, and how a detail keeps its context and a way back (`docs/contracts/information-organization.md`)}}
- **States**: {{Loading, empty, partial, error, stale, and success behavior, with counts tied to the underlying data}}

## 3. Best-Practice Baseline (Mandatory)

- **Accessibility**: {{Measured contrast of the text/background token pairs in use (`>= 4.5:1`, large text `>= 3:1`, meaningful marks `>= 3:1`); keyboard order and visible focus; targets `>= 24px`; labels and text alternatives; reduced-motion behavior}}
- **Stability and performance**: {{How layout shift is prevented (reserved space, `scrollbar-gutter: stable`, `tabular-nums`) and how refresh keeps stale data visible}}
- **Data presentation**: {{Encodings chosen by perceptual accuracy, labeled units, numerator/denominator/scope for rates, and distinction of physical facts / AI records / human approvals}}

## 4. Owner Preferences Applied

- **Preference source**: {{Default calm-platter style from `docs/contracts/frontend-and-visual-discipline.md` Section 4, or this project's own recorded preferences (link)}}
- **Canvas vs platter split** (default style): {{What quiet filters/hints sit on `--bg-canvas` vs what sits inside the single `--bg-platter`, with no duplicate stats and no card-in-card walls}}
- **Window widths** (default style): {{Behavior across `<680px`, `680–1024px`, `1024–1440px`, and `>1440px`, hiding low-priority table columns rather than adding horizontal scrollbars}}
- **Long fields** (default style): {{Middle truncation + click-to-expand details for UUID/SHA/paths, and disabled-in-place controls}}

## 5. Styles & Verification

- **Style ownership**: {{`:root` tokens isolated in `tokens.css`; component CSS follows `max_style_lines` in `docs-policy.toml`}}
- **Verification**: Verified against the pre-delivery self-check (`docs/contracts/frontend-and-visual-discipline.md#pre-delivery-ui-self-check`): principle checks, measured best-practice checks, and preference checks across `540px`, `800px`, `1280px`, and `2560px+`.
