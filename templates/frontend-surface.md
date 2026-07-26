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

Every translated item cites at least one raw anchor.

### Outcomes

- **O1 — {{outcome}}**
  From: raw[{{N}}]

### Reachable states

| State | Entry condition | Visible result | Available actions | Exit/error behavior | From |
|---|---|---|---|---|---|
| `{{state}}` | {{condition}} | {{result}} | {{actions}} | {{behavior}} | raw[{{N}}] |

Include applicable empty, loading, populated, error, stale, disabled, selected,
expanded, unauthorized, offline, and archived states.

### Layout and size contract

| Element/region | Width contract | Height contract | Overflow/scroll owner | Conditions | From |
|---|---|---|---|---|---|
| `{{stable handle}}` | {{min/max/intrinsic}} | {{min/max/content}} | {{owner}} | {{state/container}} | raw[{{N}}] |

Define narrow, intermediate, and wide container behavior from the layout's own
constraints. Device names may be used as verification fixtures, not as the sole
source of breakpoints.

### Interaction map

| ID | Stable handle | Trigger/input | Precondition | Expected state delta | Focus/scroll result | From |
|---|---|---|---|---|---|---|
| `{{id}}` | `{{selector/role/test id}}` | {{click/key/touch/etc.}} | {{state}} | {{delta}} | {{result}} | raw[{{N}}] |

### Content and visual logic

- Hierarchy: {{primary/secondary/supporting}}
- Typography and density roles: {{contract}}
- Empty/error language: {{contract}}
- Shared component variants used: {{variants}}
- Surface-specific exceptions and owner: {{exceptions or none}}
- From: raw[{{N}}]

### Accessibility and input

- Semantic structure: {{headings/landmarks/control roles}}
- Keyboard and focus: {{order/restoration/trap/escape}}
- Touch and pointer: {{targets/gestures/hover alternatives}}
- Screen reader announcements: {{dynamic state}}
- Contrast, motion, zoom, and text scaling: {{support}}
- From: raw[{{N}}]

### Responsive and browser support

| Container/viewport band | Layout state | Navigation/interaction changes | Required engines/inputs |
|---|---|---|---|
| {{range derived from constraints}} | {{state}} | {{changes}} | {{targets}} |

## Known abnormality classes

List prior or plausible failures the verifier must check explicitly:

- {{hard clipping, hidden scroll affordance, stretched item, lost focus, etc.}}

## Verification matrix

| State | Range/environment | Functional | Structural geometry | Perceptual | Accessibility | Independent review |
|---|---|---|---|---|---|---|
| {{state}} | {{environment}} | pending | pending | pending | pending | pending |

Geometric claims must cite rendered measurements, not static stylesheet values.

## Reconciliation log

- **{{YYYY-MM-DD}} — {{classification}}:** {{what changed and which raw or
  translated item was corrected}}
