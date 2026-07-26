---
doc_type: contract
status: target
authority: normative
implementation: not_started
verification_status: pending
last_reconciled: {{YYYY-MM-DD}}
supersedes: []
---

# {{Product}} style system contract

## Purpose

Declare who owns each shared visual decision, in what order those owners win,
and what consumers may change. Style decay is a dependency-direction and
precedence problem: it is prevented by declaring ownership, not by agreeing on
a naming convention.

Delete every section this project does not own. An empty declaration is worse
than an absent one.

## Scope

### In scope

- {{style corpus this contract governs, as paths or packages}}
- {{shared value vocabulary this contract governs}}

### Out of scope

- {{surface-specific appearance, which belongs in docs/design/<surface>.md}}
- {{explicit non-goal}}

## Source anchors

### source[1] — {{YYYY-MM-DD}}

> “{{verbatim statement, incident, or audit finding that motivated this}}”

Context: {{where this was recorded}}

## Vocabulary

| Term | Meaning here | Excluded meaning |
|---|---|---|
| `{{term}}` | {{definition}} | {{common ambiguity}} |

Name the mechanism this project actually uses. This contract does not assume a
language, preprocessor, component model, or delivery pipeline.

## Layer order and ownership

Lowest authority first. Every file in the style corpus resolves to exactly one
layer.

| Order | Layer | Owner | Contains | May depend on | Consumers may |
|---|---|---|---|---|---|
| 1 | `{{layer}}` | `{{owner}}` | `{{what lives here}}` | `{{lower layers}}` | `{{compose/extend/never touch}}` |

- from: source[{{N}}]

- Realizing mechanism: {{how the declared order is actually enforced at
  delivery}}
- Undeclared style lands in: {{position, per the mechanism's own rules}}
- If precedence depends on artifact or load order, state that dependency and
  the accepted risk: {{dependency and risk, or none}}

Where the mechanism grants undeclared style the highest authority rather than
the lowest, an omission is an escalation. The corpus declaration above is the
guard against it.

## Shared value tiers

A tier may reference only tiers below it. Nothing references upward.

| Order | Tier | Owner | Names describe | Consumable by |
|---|---|---|---|---|
| 1 | `{{raw values}}` | `{{owner}}` | {{the value itself}} | `{{internal only, or declared exception}}` |
| 2 | `{{roles}}` | `{{owner}}` | {{the decision the value serves}} | `{{consumers}}` |

- from: source[{{N}}]

- Governed value classes: {{color, spacing, type, radius, elevation, motion,
  z-order, or the subset this project governs}}
- Literals that remain legal, and where: {{exemptions}}
- Admission process for a new name: {{who approves, on what evidence}}
- Retirement process: {{how a name is deprecated and removed}}

A consumer binding to a raw value instead of a role is a tier reach-through:
record it below or fix it. A name that describes an appearance rather than a
decision cannot be re-pointed under a different theme, so it does not satisfy
the role tier.

## Published override surface

What consumers may set is finite and listed. Everything else is private.

| Unit | Published surface | Variants offered | Never overridable |
|---|---|---|---|
| `{{unit}}` | `{{named values a consumer may set}}` | `{{variants}}` | `{{internals}}` |

- from: source[{{N}}]

Reachability is not publication. A handle a consumer can technically select but
the owner never published is private, and depending on it is a boundary
violation rather than a supported extension.

## Theme and variant axes

| Axis | Values | Owner | Expressed by |
|---|---|---|---|
| `{{mode/brand/density/direction}}` | `{{values}}` | `{{owner}}` | `{{re-pointed names, not duplicated rules}}` |

- from: source[{{N}}]

A variant implemented as a parallel copy of a unit's rules is a fork, not a
theme.

## Responsive authority

| Band | Measured element | Owner | Behavior when the basis is absent |
|---|---|---|---|
| `{{band}}` | `{{the unit's own allotted space, or the display}}` | `{{owner}}` | `{{declared fallback}}` |

- from: source[{{N}}]

Thresholds derive from the layout's own constraints. Device names are
verification fixtures, not the source of a threshold.

## Escalation and exception register

Every construct that wins by outranking rather than by owning is listed here or
does not exist. Escalation that is a permanent, declared part of a layer's
contract belongs in the layer table above instead.

| ID | What is escalated | Owner | Reason | Removal condition |
|---|---|---|---|---|
| `{{id}}` | `{{forced priority, weight inflation, boundary reach}}` | `{{owner}}` | {{why}} | {{condition}} |

- from: source[{{N}}]

Record any exception carrying a committed removal date as a promise below, so
the date is mechanically aged rather than remembered.

## Decay budgets

Optional. Each metric this project chooses to govern declares how it is
measured and what the measurement cannot see. Omit the section rather than
declaring a metric nobody maintains.

| Metric | Unit | Method | Blind spots | Measured | Cap | Direction | Measured on |
|---|---|---|---|---|---|---|---|
| `{{metric}}` | {{unit}} | {{how}} | {{what it misses}} | {{value}} | {{cap}} | {{non-increasing}} | {{YYYY-MM-DD}} |

- from: source[{{N}}]

Choose the caps from this project's own measured baseline. A threshold copied
from another organization's published figure is not a budget.

## Acceptance evidence

| Outcome | Guard or verification | Durable evidence |
|---|---|---|
| Every corpus file resolves to one declared layer | {{guard}} | {{path or pending}} |
| Value tiers reference one way only | {{guard}} | {{path or pending}} |
| Consumers use only the published override surface | {{guard}} | {{path or pending}} |
| Escalations are registered and owned | {{guard}} | {{path or pending}} |

A style-ownership claim is a structural claim. It is proved by the declared
guard, not by a screenshot; perceptual evidence shows what rendered, not who
owned it.

## Promise register

Use only for a concrete future reconciliation commitment. Delete the example
when none exist.

- promise[{{stable-id}}]: due={{YYYY-MM-DD}}; status=open; owner={{owner}}; description={{concrete promised alignment}}

## Reconciliation log

- **{{YYYY-MM-DD}}:** {{ambiguity, translation correction, requirement change,
  implementation regression, or evidence conflict}}
