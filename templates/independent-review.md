---
doc_type: evidence
status: historical
authority: evidence
last_reconciled: {{YYYY-MM-DD}}
subject: {{initiative-or-contract}}
---

# {{Initiative}} independent review

## Review scope and independence

- Governing contract and revision: `{{path-and-revision}}`
- Risk profile: `{{material / high-risk}}`
- Reviewer/context identity: {{identity}}
- Independence basis: {{why this context did not produce the proposal}}
- Independence required and achieved: {{yes/no with reason}}

Same-context role-play must be labeled non-independent.

## Inputs

- Contract/design: `{{path}}`
- Baseline evidence and fixtures: `{{paths}}`
- Constraints supplied to every perspective: {{constraints}}
- Deliberately withheld information, if any: {{item and reason}}

## Perspective findings

### System and contract consistency

{{Ownership, invariants, compatibility, failure, and architecture findings.}}

### User or operator experience

{{Reachable states, usability, recovery, accessibility, and operational findings.}}

### Engineering and maintenance

{{Complexity, testing, observability, extensibility, and migration findings.}}

Add security, privacy, reliability, or domain lenses when the risk requires
them.

## Synthesis

| Finding | Perspectives agreeing | Severity | Required action | Owner |
|---|---|---|---|---|
| {{finding}} | {{lenses}} | {{level}} | {{action}} | {{owner}} |

## Disagreements and human decisions

- Unresolved disagreement: {{none or exact conflict}}
- Human-authority decision required: {{none or decision and deadline}}
- Governance exception: {{none or authority, scope, date, residual risk}}

## Limitations

- {{Missing environment, evidence class, domain expertise, or independence}}

## Verdict and follow-up

`{{PASS / FAIL / BLOCKED / PARTIAL}}`

- Required follow-up: {{action or none}}
- Evidence/issue links: `{{paths}}`
