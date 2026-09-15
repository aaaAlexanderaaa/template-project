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

Original request/source: {{dated wording or link}}.
Accepted interpretation: {{what the user will be able to accomplish}}.

## Scope

### In scope

- {{behavior, state, interface, or surface}}

### Out of scope

- {{explicit non-goal}}

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

List only concerns activated through [development § activate-concerns](../docs/contracts/development-discipline.md#activate-concerns-instead-of-expanding-ceremony). This contract, or the
linked normative contract, must own the boundary and failure policy; do not
copy the [development § activate-concerns](../docs/contracts/development-discipline.md#activate-concerns-instead-of-expanding-ceremony) trigger table.

| Quality concern | Scenario | Boundary/response | Guard or observation | Escalation/exception policy |
|---|---|---|---|---|
| {{concern or none, including time and calendar or demonstration data}} | {{scenario}} | {{measurable or qualitative boundary}} | {{guard/signal}} | {{owner, path, or explicitly non-waivable}} |

## States and triggers

| State | Entry trigger | Allowed actions | Exit trigger | Failure behavior |
|---|---|---|---|---|
| `{{state}}` | {{trigger}} | {{actions}} | {{trigger}} | {{behavior}} |

List invalid transitions explicitly.

## Normative invariants

### {{Plain-language invariant name}}

{{rule}}

- from: source[{{N}}] ({{source date and topic}})
- Enforcement: `{{type/test/runtime guard or bounded review}}`

## Required behaviors

- {{positive requirement}}

## Forbidden behaviors

- {{behavior that would violate ownership or intent}}

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

Use [bidirectional verification](../docs/contracts/development-discipline.md#verify-promised-and-observed-behavior-in-both-directions).
Include functional outcomes and activated quality boundaries; do not build the
requirements list from existing tests. Link the owner of a shared threshold.

| User scenario and trigger | Promised result and boundary | Verification at affected boundary | Observed result / evidence / status |
|---|---|---|---|
| {{starting state and action}} | {{functional or nonfunctional requirement}} | {{test/probe/review and relevant baseline}} | {{pending, then actual result and limitation}} |

For repeated or external effects, state target identity, allowed effects and
counts per operation, trigger frequency/freshness, and applicable timing. In
the result column or linked verification report, account for actual effects
that were absent from the expected list. Explain failure, partial/unknown
results, and the user's next action. Compare the final result with the original
request as well as this interpretation.

## Promise register

Use this only for a concrete future reconciliation commitment. Every open
promise has an explicit owner and due date; delete the example when none exist.

- promise[{{stable-id}}]: due={{YYYY-MM-DD}}; status=open; owner={{owner}}; description={{concrete promised alignment}}

## Source anchors

Record dated stakeholder language, incidents, standards, or prior decisions.
Quote source language when interpretation matters.

### source[1] — {{YYYY-MM-DD}}

> “{{verbatim statement}}”

Context: {{where the request, incident, standard, or decision was recorded}}

### source[2] — {{YYYY-MM-DD}}

{{Evidence or decision}}

## Reconciliation log

- **{{YYYY-MM-DD}}:** {{ambiguity, translation correction, requirement change,
  implementation regression, or evidence conflict}}
