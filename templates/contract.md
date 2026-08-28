---
doc_type: contract
status: target
authority: normative
implementation: not_started
verification_status: pending
last_reconciled: {{YYYY-MM-DD}}
supersedes: []
---

# {{Contract title}}

## Purpose

What durable problem does this contract solve? State the user or system outcome,
not only the implementation mechanism.

## Scope

### In scope

- {{behavior, state, interface, or surface}}

### Out of scope

- {{explicit non-goal}}

## Source anchors

Record dated stakeholder language, incidents, standards, or prior decisions.
Quote source language when interpretation matters.

### source[1] — {{YYYY-MM-DD}}

> “{{verbatim statement}}”

Context: {{where the request, incident, standard, or decision was recorded}}

### source[2] — {{YYYY-MM-DD}}

{{Evidence or decision}}

## Vocabulary

| Term | Meaning | Excluded meaning |
|---|---|---|
| `{{term}}` | {{definition}} | {{common ambiguity}} |

## Ownership and boundary

- Authoritative owner: `{{module/service/surface}}`
- Consumers: `{{consumers}}`
- Public contract: `{{interface}}`
- Private implementation details consumers must not infer: `{{details}}`

## Activated quality attributes

List only concerns activated through development D8. This contract, or the
linked normative contract, must own the boundary and failure policy; do not
copy the D8 trigger table.

| Quality concern | Scenario | Boundary/response | Guard or observation | Escalation/exception policy |
|---|---|---|---|---|
| {{concern or none, including time and calendar or demonstration data}} | {{scenario}} | {{measurable or qualitative boundary}} | {{guard/signal}} | {{owner, path, or explicitly non-waivable}} |

## States and triggers

| State | Entry trigger | Allowed actions | Exit trigger | Failure behavior |
|---|---|---|---|---|
| `{{state}}` | {{trigger}} | {{actions}} | {{trigger}} | {{behavior}} |

List invalid transitions explicitly.

## Normative invariants

- **INV-1 — {{name}}.** {{rule}}
  - from: source[{{N}}]
  Enforcement: `{{type/test/runtime guard}}`

## Required behaviors

- **RB-1.** {{positive requirement}}

## Forbidden behaviors

- **FB-1.** {{behavior that would violate ownership or intent}}

## Failure, recovery, and intervention

- Retryable failures: {{classification}}
- Terminal failures: {{classification}}
- Timeout behavior: {{behavior}}
- Recovery identity and persisted state: {{contract}}
- Manual intervention: {{who, when, how}}

## Compatibility and migration

- Current state: {{facts}}
- Cutover policy: {{atomic / compatibility window / dual-read, with rationale}}
- Data migration: {{method and idempotency}}
- Rollback: {{method and limitations}}
- Removal criteria for temporary compatibility, if any: {{criteria and owner}}

## Acceptance evidence

| Outcome | Guard or verification | Durable evidence |
|---|---|---|
| {{observable outcome}} | {{test/probe/review}} | {{path or pending}} |

## Promise register

Use this only for a concrete future reconciliation commitment. Every open
promise has an explicit owner and due date; delete the example when none exist.

- promise[{{stable-id}}]: due={{YYYY-MM-DD}}; status=open; owner={{owner}}; description={{concrete promised alignment}}

## Reconciliation log

- **{{YYYY-MM-DD}}:** {{ambiguity, translation correction, requirement change,
  implementation regression, or evidence conflict}}
