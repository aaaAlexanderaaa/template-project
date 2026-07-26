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
- In scope: {{behavior}}
- Out of scope: {{non-goals}}

## Source anchors

- **source[1] — {{YYYY-MM-DD}}:** {{request, incident, or decision}}

## Ownership

| Concern | Authoritative owner | Public consumers | Forbidden duplicate owner |
|---|---|---|---|
| {{state/invariant}} | {{module/service/store}} | {{consumers}} | {{location}} |

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

## Authorization and capability boundary

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

- {{happy lifecycle invariant}}
- {{invalid transition}}
- {{duplicate/idempotency sibling case}}
- {{concurrent/race case}}
- {{restart or partial-write recovery}}
- {{permission denial}}
- {{API/persistence/count self-consistency}}

## Rollout and verification

| Stage | Preconditions | Checks | Abort/rollback condition |
|---|---|---|---|
| {{stage}} | {{conditions}} | {{checks}} | {{condition}} |

## Reconciliation log

- **{{YYYY-MM-DD}}:** {{decision or conflict resolution}}
