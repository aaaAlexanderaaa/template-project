---
doc_type: evidence
status: historical
authority: evidence
last_reconciled: {{YYYY-MM-DD}}
subject: {{initiative-or-objective}}
---

# {{Initiative}} holistic evaluation

## Claim and completion layer

- Claim under evaluation: {{observable outcome}}
- Original request/source and accepted interpretation: {{wording or links}}
- Completion layer: `{{task / task-group / objective / release-gate}}`
- Governing contracts: `{{paths-and-revisions}}`
- Implementation revision/build: `{{identity}}`

## Independence

- Evaluator/context identity: {{identity}}
- Relationship to design and implementation: {{relationship}}
- Fresh-context requirement: {{required/not required and why}}
- Requirement achieved: {{yes/no, blocked state, or governance exception}}

## Evidence inventory

| Evidence | Class | Claim supported | Reproduction path | What it does not prove |
|---|---|---|---|---|
| {{record}} | {{unit/integration/artifact/real-runtime/manual}} | {{claim}} | `{{command-or-path}}` | {{limitation}} |

## Six-dimensional evaluation

| Dimension | Questions | Finding | Evidence | Result |
|---|---|---|---|---|
| Functional outcome | Does the delivered result fulfill the original request as well as the contract? | {{finding}} | {{evidence}} | pass/fail/partial/not_run |
| Contract and domain logic | Are ownership, states, and invariants coherent? | {{finding}} | {{evidence}} | pass/fail/partial |
| User/operator experience | Are reachable states understandable and usable? | {{finding}} | {{evidence}} | pass/fail/partial |
| Failure and recovery | Do negative paths fail and recover as contracted? | {{finding}} | {{evidence}} | pass/fail/partial |
| Integration and compatibility | Do producers, consumers, artifacts, and migrations align? | {{finding}} | {{evidence}} | pass/fail/partial |
| Maintainability and operations | Are tests, observability, docs, and rollback sufficient? | {{finding}} | {{evidence}} | pass/fail/partial |

Apply [bidirectional verification](../docs/contracts/development-discipline.md#verify-promised-and-observed-behavior-in-both-directions)
to the integrated result. Account for actual external effects, including those
absent from the acceptance list, and inspect applicable identity, frequency,
freshness, user cost, and recovery boundaries. Link existing observations;
do not create a second requirements inventory. Missing observations are unknown
or not run, never a pass.

### Activated quality outcomes

| Concern | Normative owner/boundary | Finding | Evidence | Result |
|---|---|---|---|---|
| {{activated concern or none}} | `{{contract and section}}` | {{finding}} | {{evidence}} | pass/fail/partial |

## Failure and recovery

- Negative paths exercised: {{cases}}
- Recovery or rollback observed: {{result}}
- Unexercised destructive/irreversible paths: {{cases and substitute evidence}}

## Residual risks

| Risk | Impact | Evidence gap | Owner and disposition |
|---|---|---|---|
| {{risk}} | {{impact}} | {{gap}} | {{owner/action}} |

## Verdict

`{{PASS / FAIL / BLOCKED / PARTIAL}}`

State which completion layer may close and which higher-layer claims remain
open. Link required issues, reconciliation records, or exceptions: {{paths}}.
