---
doc_type: contract
status: target
authority: normative
implementation: not_started
verification_status: pending
last_reconciled: {{YYYY-MM-DD}}
supersedes: []
---

# {{Cross-stack feature}} contract

## User outcome

{{What becomes possible or correct for the user?}}

## Shared vocabulary

| Term/state | Canonical meaning | Authoritative owner | Frontend label/projection |
|---|---|---|---|
| `{{term}}` | {{meaning}} | {{backend/module owner}} | {{projection}} |

## End-to-end state matrix

| Domain state | API/event representation | Frontend state | Allowed user action | Mutation result |
|---|---|---|---|---|
| `{{state}}` | {{shape}} | `{{ui-state}}` | {{action}} | {{result}} |

Include loading, empty, stale, partial, unauthorized, conflict, retryable, and
terminal failure states where applicable.

## Ownership boundary

- Backend/domain owner decides: {{truth, transitions, authorization}}
- Frontend owner decides: {{presentation, local interaction state}}
- Shared/versioned contract: {{schema/types/events}}
- Rules the frontend must not reconstruct: {{rules}}
- UI-only state the backend must not absorb: {{state}}

## Activated quality attributes

| Concern | Normative owner | Shared boundary/failure policy | Producer steps | Consumer steps | Evidence |
|---|---|---|---|---|---|
| {{concern or none}} | `{{contract and section}}` | {{link, not duplicated policy}} | {{steps}} | {{steps}} | {{guard/probe}} |

## Interface contract

### Read path

- Request/query: {{shape}}
- Response: {{shape}}
- Empty/stale/partial semantics: {{semantics}}
- Pagination/order/count consistency: {{contract}}

### Mutation path

- Command: {{shape}}
- Preconditions and authorization: {{contract}}
- Success response and authoritative refresh: {{contract}}
- Conflict/retry/terminal errors: {{mapping}}
- Idempotency and duplicate interaction: {{contract}}

### Event or live-update path

- Ordering, resume, duplication, and loss behavior: {{contract or not applicable}}

## Frontend surface projection

- Affected surface contract: `docs/design/{{surface}}.md`
- Reachable states added/changed: {{states}}
- Interaction and focus behavior: {{behavior}}
- Responsive/accessibility implications: {{implications}}
- Visual hierarchy outcome: {{outcome}}
- Style layer impact: {{new shared values, new variants, or none}}

## Compatibility and cutover

- Producer/consumer deployment order: {{order}}
- Compatibility decision: {{single cutover or bounded window}}
- Old behavior removal condition: {{condition}}
- Data migration/backfill: {{procedure}}
- Rollback: {{procedure}}

## Acceptance matrix

| Scenario | Backend assertion | Frontend assertion | End-to-end evidence |
|---|---|---|---|
| {{scenario}} | {{state/API}} | {{display/interaction}} | {{test/probe}} |

## Failure-category guards

Retain only categories activated by this boundary or a repeatable defect
mechanism. Record why a local guard is sufficient when broader coverage is not
proportionate.

- API self-consistency: {{guard}}
- Cross-surface consistency: {{guard}}
- Stale/duplicate interaction: {{guard}}
- Authorization mismatch: {{guard}}
- Recovery/replay equivalence: {{guard}}

## Non-goals

- {{explicit exclusion}}

## Reconciliation log

- **{{YYYY-MM-DD}}:** {{decision or conflict resolution}}
