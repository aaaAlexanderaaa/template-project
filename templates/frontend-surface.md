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

What concrete subject does the surface represent, who uses it, and what single
job does it help them complete? Describe intended feel and hierarchy without
prematurely choosing pixel values.

## Raw layer

### raw[1] — {{YYYY-MM-DD}}

> {{Verbatim stakeholder language about the subject, audience, job, feel, or
> rejected generic direction}}

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

### Design direction and content

- Concrete subject, audience, and single user job: {{accepted translation}}
- Design thesis: {{one sentence tying the presentation to that subject/job}}
- Subject-specific anchors: {{materials, artifacts, language, workflows, or
  real content that justify the direction}}
- Candidate direction reviewed: {{named color roles, typography roles, layout
  concept, content voice, and motion intent}}
- Generic defaults or rejected alternatives: {{what was rejected and why it
  did not fit this brief}}
- Hierarchy and layout signature: {{primary/secondary/supporting and the one
  memorable element, or none}}
- Typography and density roles: {{contract and brief-specific rationale}}
- Motion purpose and reduced-motion equivalent: {{purpose/equivalent or none}}
- Interface vocabulary and action/result continuity: {{canonical terms and
  active labels}}
- Empty/error language and recovery direction: {{contract}}
- Disposable probe evidence and disposition: {{tmp path, accepted result and
  cleanup, or none}}
- Shared component variants used: {{variants}}
- Surface-specific exceptions and owner: {{exceptions or none}}
- from: raw[{{N}}]

Candidates and probes do not own values. Carry accepted decisions through the
style and theming contract below; remove decoration that cannot be justified by
the subject, hierarchy, or user job.

### Style and theming contract

- Style layer this surface writes into: {{layer}}
- Values consumed, by tier: {{named values, not literals}}
- Override surface used on shared units: {{published names and variants}}
- Theme, mode, density, or direction variants supported: {{axes}}
- Values defined locally, with owner and removal condition: {{values or none}}
- Escalations held by this surface: {{registered ids or none}}
- from: raw[{{N}}]

Record a value the shared layer does not publish as an exception with an owner.
Do not restate the shared layer's rules here; name what this surface consumes.

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

## Activated quality attributes

Experience concerns above are intrinsic to this surface. List only additional
D8 concerns activated by its implementation or operation, and link their
normative owner rather than copying a threshold.

| Concern | Normative owner | Boundary/failure policy | Surface evidence |
|---|---|---|---|
| {{performance/security/privacy/reliability/dependency/production learning or none}} | `{{contract and section}}` | {{link}} | {{probe/observation}} |

## Known abnormality classes

This section is optional in an adopted surface. If present, every entry uses
the exact structured form below. Pending evidence expires according to
`docs-policy.toml`.

- abnormality[{{stable-slug}}]: state=pending; evidence=pending:{{YYYY-MM-DD}}; guard=pending; description={{hard clipping, hidden scroll affordance, stretched item, lost focus, etc.}}

## Verification matrix

| State | Range/environment | Functional | Structural geometry | Brief/design direction | Perceptual | Accessibility | Independent review (high-risk only) |
|---|---|---|---|---|---|---|---|
| {{state}} | {{environment}} | pending | pending | pending | pending | pending | pending |

Geometric claims must cite rendered measurements, not static stylesheet values.
Theme and mode variants are environments in the range column, not new columns.
A style-ownership claim is structural: it is proved by the declared guard, not
by a screenshot, which shows what rendered rather than who owned it.
Perceptual review checks subject and user-job fidelity, hierarchy, content
voice, action-name continuity, deliberate restraint, and whether a generic
default survived without a brief-specific reason.

## Reconciliation log

- **{{YYYY-MM-DD}} — {{classification}}:** {{what changed and which raw or
  translated item was corrected}}
