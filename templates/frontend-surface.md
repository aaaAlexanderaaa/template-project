---
doc_type: surface-contract
surface: {{surface-slug}}
status: target
authority: normative
implementation: not_started
contract_scope: future-ui
verification_status: pending
last_reconciled: {{YYYY-MM-DD}}
supersedes: []
---

# {{Surface name}} — surface contract

## Purpose and user outcome

What job does this surface help the user complete? Describe intended feel and
hierarchy without prematurely choosing pixel values.

## Raw layer

### raw[1] — {{YYYY-MM-DD}}

> {{Verbatim stakeholder language}}

Context: {{where/when this was observed}}

### raw[2] — {{YYYY-MM-DD}}

> {{Verbatim changed requirement, rejection, or additional need}}

If this changes an older requirement, write `supersedes: raw[N]` explicitly.

## Translated layer

Every `###` translated subsection cites at least one raw anchor with a
`- from: raw[N]` line. Place additional citations adjacent to a more specific
claim when a subsection translates multiple sources. The checker enforces that
every subsection is cited, every citation resolves, and every defined raw
anchor is used.

### Outcomes

- **O1 — {{outcome}}**
  - from: raw[{{N}}]

### Reachable states

| State | Entry condition | Visible result | Available actions | Exit/error behavior |
|---|---|---|---|---|
| `{{state}}` | {{condition}} | {{result}} | {{actions}} | {{behavior}} |

- from: raw[{{N}}]

Include applicable empty, loading, populated, error, stale, disabled, selected,
expanded, unauthorized, offline, and archived states.

### Layout and size contract

| Element/region | Width contract | Height contract | Overflow/scroll owner | Conditions |
|---|---|---|---|---|
| `{{stable handle}}` | {{min/max/intrinsic}} | {{min/max/content}} | {{owner}} | {{state/container}} |

- from: raw[{{N}}]

Define narrow, intermediate, and wide container behavior from the layout's own
constraints. Device names may be used as verification fixtures, not as the sole
source of breakpoints.

### Interaction map

| ID | Stable handle | Trigger/input | Precondition | Expected state delta | Focus/scroll result |
|---|---|---|---|---|---|
| `{{id}}` | `{{selector/role/test id}}` | {{click/key/touch/etc.}} | {{state}} | {{delta}} | {{result}} |

- from: raw[{{N}}]

### Content and visual logic

- Hierarchy: {{primary/secondary/supporting}}
- Typography and density roles: {{contract}}
- Empty/error language: {{contract}}
- Shared component variants used: {{variants}}
- Surface-specific exceptions and owner: {{exceptions or none}}
- from: raw[{{N}}]

### Accessibility and input

- Semantic structure: {{headings/landmarks/control roles}}
- Keyboard and focus: {{order/restoration/trap/escape}}
- Touch and pointer: {{targets/gestures/hover alternatives}}
- Screen reader announcements: {{dynamic state}}
- Contrast, motion, zoom, and text scaling: {{support}}
- from: raw[{{N}}]

### Responsive and browser support

| Container/viewport band | Layout state | Navigation/interaction changes | Required engines/inputs |
|---|---|---|---|
| {{range derived from constraints}} | {{state}} | {{changes}} | {{targets}} |

- from: raw[{{N}}]

## Known abnormality classes

This section is optional in an adopted surface. If present, every entry uses
the exact structured form below. Pending evidence expires according to
`docs-policy.toml`.

- abnormality[{{stable-slug}}]: state=pending; evidence=pending:{{YYYY-MM-DD}}; guard=pending; description={{hard clipping, hidden scroll affordance, stretched item, lost focus, etc.}}

## Verification matrix

| State | Range/environment | Functional | Structural geometry | Perceptual | Accessibility | Independent review |
|---|---|---|---|---|---|---|
| {{state}} | {{environment}} | pending | pending | pending | pending | pending |

Geometric claims must cite rendered measurements, not static stylesheet values.

## Reconciliation log

- **{{YYYY-MM-DD}} — {{classification}}:** {{what changed and which raw or
  translated item was corrected}}
