---
doc_type: contract
status: target
authority: normative
implementation: not_started
verification_status: pending
last_reconciled: {{YYYY-MM-DD}}
supersedes: []
---

# {{Backend/service change}} contract

## Outcome and scope

- User/system outcome: {{outcome}}
- Original request and accepted interpretation: {{source and intended user job}}
- In scope: {{behavior}}
- Out of scope: {{non-goals}}

## Source anchors

### source[1] — {{YYYY-MM-DD}}

{{Request, incident, or decision}}

## Ownership

| Concern | Authoritative owner | Public consumers | Forbidden duplicate owner |
|---|---|---|---|
| {{state/invariant}} | {{module/service/store}} | {{consumers}} | {{location}} |

## Activated quality attributes

Retain only rows activated through [development § activate-concerns](../docs/contracts/development-discipline.md#activate-concerns-instead-of-expanding-ceremony). Link another current/target
contract when it owns the boundary; do not restate its threshold here.

| Concern | Normative owner | Scenario and boundary | Failure/escalation policy | Evidence surface |
|---|---|---|---|---|
| {{performance/reliability/security/dependency/production learning/time and calendar/demonstration data or none}} | `{{contract and section}}` | {{scenario/boundary}} | {{policy or non-waivable}} | {{guard/signal}} |

## Normative invariants

### {{Plain-language invariant name}}

{{durable backend rule}}

- from: source[{{N}}]
- Enforcement: `{{type/test/runtime guard or bounded review}}`

## Public interface

- Contract/version: `{{name/version}}`
- Request/command schema: {{link or shape}}
- Response/event schema: {{link or shape}}
- Error taxonomy: {{stable error codes and meanings}}
- Ordering and delivery: {{ordering, at-most/at-least/exactly-once claims}}
- Compatibility policy: {{policy}}

## State machine

| Current state | Trigger | Preconditions | Next state | Durable side effects | Emitted evidence |
|---|---|---|---|---|---|
| `{{state}}` | {{trigger}} | {{guards}} | `{{state}}` | {{writes}} | {{event/log}} |

Invalid transitions:

- `{{state}} + {{trigger}}` → `{{stable error}}`

## Concurrency and idempotency

- Idempotency key/identity: {{contract}}
- Concurrent ownership or fencing: {{contract}}
- Duplicate request/event behavior: {{contract}}
- Ordering and race resolution: {{contract}}
- Atomicity boundary: {{transaction/journal/compensation}}

## Persistence and migration

- Source of truth: {{store}}
- Schema/version: {{version}}
- Migration: {{forward procedure, backup, idempotency}}
- Mixed-version behavior: {{allowed or forbidden}}
- Rollback/data recovery: {{procedure and data-loss budget}}

## Failure and recovery

| Failure class | Detection | Retry policy | Persisted state | Operator action | Terminal result |
|---|---|---|---|---|---|
| {{class}} | {{signal}} | {{policy}} | {{state}} | {{action/none}} | {{result}} |

## Time and calendar

Delete this section unless [development § activate-concerns](../docs/contracts/development-discipline.md#activate-concerns-instead-of-expanding-ceremony) activates Time and calendar.

- Business timezone: `{{IANA name or not_applicable rationale}}`
- Instant storage: `{{timezone-aware absolute moments; representation changes do not rewrite history}}`
- Calendar-day rules vs duration: `{{today / day-N / grouping vs TTL / locks / age}}`
- Public representation: `{{declared offset or zone form}}`
- Naive input: `{{attach business zone / reject / date-only}}`
- Clock: `{{injectable owner shared by production and tests}}`
- Drift: `{{subsystem mismatch fails startup}}`

## Demonstration data

Delete this section unless [development § activate-concerns](../docs/contracts/development-discipline.md#activate-concerns-instead-of-expanding-ceremony) activates Demonstration data.

- Relative business day: `{{in-progress / upcoming / completed relative to clock}}`
- Environment gate: `{{environments that may rewrite; production fail-closed}}`
- Same-day identity / cross-day replacement: `{{natural keys; allowlist not accumulated}}`
- Allowlisted scope: `{{identities the refresh may touch}}`
- Demo vs production completion: `{{labeled demo; does not close a production gate}}`

## Authorization and capability boundary

Delete this section unless [development § activate-concerns](../docs/contracts/development-discipline.md#activate-concerns-instead-of-expanding-ceremony) activates the security/privacy
concern for this change.

| Caller/role | Necessary operations | Explicitly hidden operations | Enforcement |
|---|---|---|---|
| {{caller}} | {{operations}} | {{operations}} | {{policy/test}} |

## Observability

- Correlation identity: {{id}}
- Required structured fields: {{fields}}
- Lifecycle events: {{events}}
- Metrics/alerts: {{signals}}
- Audit and retention: {{policy}}
- Diagnostic procedure: {{guide link}}

## Class-level acceptance tests

Start from the user outcome and activated quality owners; use
[bidirectional verification](../docs/contracts/development-discipline.md#verify-promised-and-observed-behavior-in-both-directions)
instead of treating existing tests as the requirement inventory.

| Scenario and trigger | Promised result / quality boundary | Actual effects at service boundary | Verification / result |
|---|---|---|---|
| {{starting state and action}} | {{requirement or owning section}} | {{requests, writes, events; targets, counts, timing; undeclared effects}} | {{probe/test/review; pass/fail/partial/not_run}} |

Retain only lifecycle behavior and activated-concern cases applicable to this
change.

- {{happy lifecycle invariant}}
- {{invalid transition}}
- {{duplicate/idempotency sibling case when the mechanism is repeatable}}
- {{concurrent/race case}}
- {{restart or partial-write recovery}}
- {{permission denial when security/privacy is activated}}
- {{API/persistence/count self-consistency}}
- {{missing or unexpected effects, including excess triggers and stale suppression}}
- {{user-visible partial result and actionable recovery}}

When no repeatable sibling mechanism exists or a broader guard would cost more
than the bounded risk warrants, record that reason and keep the correction
local.

## Rollout and verification

| Stage | Preconditions | Checks | Abort/rollback condition |
|---|---|---|---|
| {{stage}} | {{conditions}} | {{checks}} | {{condition}} |

## Reconciliation log

- **{{YYYY-MM-DD}}:** {{decision or conflict resolution}}
