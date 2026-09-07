---
document_role: structural-authority
template_state: unconfigured
last_reconciled: 2026-09-07
---

# Architecture

> Template status: fill this document before adding product implementation.
> Replace every double-brace prompt. Once adopted, this file is the structural
> authority and must describe the current system rather than an aspirational
> mixture of current and future states.

## 1. System purpose

- Product/system: `{{project-name}}`
- Primary users: `{{primary-users}}`
- Problem boundary: `{{what-this-system-owns}}`
- Explicit non-goals: `{{what-this-system-does-not-own}}`

## 2. Bounded contexts and layers

| Context or layer | Owns | Public interface | May depend on | Must not know |
|---|---|---|---|---|
| `{{context-name}}` | `{{state-or-behavior}}` | `{{public-interface}}` | `{{allowed-dependencies}}` | `{{private-semantics}}` |

State the dependency direction explicitly. A lower-level or generic layer must
not acquire product-specific knowledge through convenience imports, shared
storage reads, or copied status vocabularies.

## 3. Ownership map

| Invariant | Authoritative owner | Consumers | Enforcement surface |
|---|---|---|---|
| `{{state-transition-or-rule}}` | `{{owner}}` | `{{consumers}}` | `{{enforcement-surface}}` |

Every material invariant must have one owner. Consumers may render or compose
the public contract but may not independently redefine it.

Date/time and operator-visible demo data belong in this map when they exist.
They are not a separate questionnaire. The method is
`docs/contracts/foundational-runtime-discipline.md`.

## 4. Public contracts

Document interfaces crossing module, service, process, persistence, or team
boundaries:

- version and compatibility policy;
- request/response/event shapes;
- ordering and duplicate behavior;
- validation and error taxonomy;
- authorization and capability boundary;
- deprecation and removal policy.

Link each interface to its normative contract under `docs/contracts/`.

For every quality concern activated by [development § activate-concerns](docs/contracts/development-discipline.md#activate-concerns-instead-of-expanding-ceremony),
link the current or target contract that owns its scenario, boundary, failure
policy, observation surface, and escalation/exception policy. This structural
map names the owner; it does not copy the threshold or policy.

## 5. State and lifecycle

For each durable entity or long-running operation, define:

- identity and state machine;
- legal and illegal transitions;
- persistence owner;
- transaction or atomicity boundary;
- idempotency and concurrency behavior;
- timeout, retry, cancellation, recovery, and manual-intervention states;
- archival and retention behavior.

## 6. Frontend boundary

If the project has a frontend, define:

- which backend contracts are authoritative;
- what state is frontend-owned versus merely projected;
- component or design-system ownership;
- which module owns shared visual values, and the order in which style layers
  win when they disagree;
- the scoping mechanism, what it actually contains, and what leaks past it;
- the override surface each unit publishes, and how a consumer obtains a value
  the shared layer does not publish;
- routing and extension points;
- accessibility, browser, input, and responsive support policy;
- which time-policy scope, clock, input interpretation, and display role the
  surfaces consume when they display or accept date/time.

Per-surface behavior belongs under `docs/design/`, not in this structural map.

## 7. Runtime and deployment

- Runtime topology: `{{processes-services-jobs}}`
- Configuration sources and precedence: `{{sources-and-precedence}}`
- Secret ownership: `{{mechanism}}`
- Health and observability: `{{logs-metrics-traces-audit}}`
- Deployment and rollback unit: `{{unit}}`
- Data migration and compatibility window: `{{policy}}`
- Recovery objectives: `{{recovery-objectives}}`
- Time policy and clock: `{{scope-resolution-storage-calendar-input-display-clock-or-n/a}}`
- Demonstration-data runtime: `{{temporal-promise-labels-refresh-retention-gate-or-n/a}}`

## 8. Hard and soft boundaries

Classify extension points:

- **Hard:** state identity, integrity, protocol shape, geometry, accessibility,
  authorization, or dependency direction. Consumers cannot override it.
- **Soft:** presentation or configuration explicitly exposed through a finite
  public API, including the named visual values and theme surface a unit
  publishes for consumers to set.
- **Family/group:** a declared owner provides named variants while protecting
  shared behavior.

Anything not explicitly public is private to its owner. Reachability is not
publication: a value or handle a consumer can technically select, but the owner
never published, is private, and depending on it is a boundary violation rather
than a supported extension.

## 9. Structural fitness tests

`architecture-rules.toml` is the portable baseline enforcement manifest. In an
adopted project, set it to `configured` with at least one non-vacuous path and
forbidden-reference rule, or to `not_applicable` with a substantive rationale.
The generic checker evaluates those literal boundary rules.

List additional language-native or runtime checks that prove the architecture
remains true:

- `{{semantic-dependency-or-import-check}}`
- `{{public-contract-or-schema-compatibility-check}}`
- `{{state-and-recovery-lifecycle-test}}`
- `{{permission-or-capability-isolation-test}}`
- `{{frontend-ownership-or-geometry-guard}}`
- `{{scoped-time-policy-clock-and-input-guard}}`
- `{{demo-refresh-idempotency-and-environment-gate}}`

## 10. Reconciliation log

Record dated structural changes, superseded decisions, and links to the
contracts and plans that implemented them.

- **2026-09-07:** runtime prompts identify policy scope and role resolution,
  demo temporal promises, and the selected refresh/retention strategy.

- **2026-08-24:** runtime prompts name business timezone/clock and
  demonstration-data only when those exist. A 15-row early-declaration
  register was added and then removed: it turned historical pits into
  onboarding ceremony. Method:
  `docs/contracts/foundational-runtime-discipline.md`.
