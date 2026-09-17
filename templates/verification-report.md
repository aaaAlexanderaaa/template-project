---
doc_type: evidence
status: historical
authority: evidence
last_reconciled: {{YYYY-MM-DD}}
subject: {{initiative-or-contract}}
---

# {{Initiative}} verification report

## Claim being verified

- Contract and section: `{{path}}`
- Original request/source and accepted interpretation: {{wording or links}}
- Revision/build: `{{commit/build id}}`
- Observable outcomes: {{outcomes}}
- Verifier: {{person/context}}
- Independence required: {{yes/no and why}}
- Activated quality owners: {{contract sections or none; do not restate their
  thresholds}}

## Environment

- Date/time: {{timestamp/timezone}}
- Runtime/platform/browser/device: {{environment}}
- Configuration and fixture identity: {{non-secret identity}}
- Starting state: {{state}}
- Required materials: {{supplied paths or obtainable public sources; access limits}}
- Reproduction command: `{{command runnable with those materials}}`

## Result matrix

| User scenario / trigger | Promised result / quality boundary | Observed result | Evidence at affected boundary | Result |
|---|---|---|---|---|
| {{starting state and action}} | {{functional requirement or quality owner}} | {{actual result and user next action}} | {{measurement, process/browser/artifact observation, or review}} | pass/fail/partial/not_run |

### Actual effects

Apply [bidirectional verification](../docs/contracts/development-discipline.md#verify-promised-and-observed-behavior-in-both-directions).
Inspect requests, writes, events, notifications, and other relevant effects,
including ones absent from the expected-result list. A pure text correction may
state that no external effects are involved instead of filling an empty table.

| Observed effect / target | Authorizing requirement | Expected vs actual count and timing | Disposition |
|---|---|---|---|
| {{boundary observation}} | {{owning section or undeclared}} | {{per operation and relevant window/freshness}} | {{within boundary / missing / extra / excessive / suppressed / unknown}} |

Compare the delivered user outcome with the original request, not only the
accepted interpretation. Record observation coverage and limits; no observation
means unknown, not zero effects.

For a [scope or interpretation discrepancy](../docs/contracts/development-discipline.md#outcomes-before-means),
trace where it entered and which decision supports it; inspect affected guards
as well as prose. When broader coverage is claimed, include a plausible case
beyond the initial sample. For a proposed local correction, inspect the whole
result in context under [causal analysis](../docs/contracts/development-discipline.md#analysis-exposes-the-decisive-causal-mechanism).
A correct library rule or complete fields alone do not prove its application.

## Failure and negative-path checks

| Failure class | Injection/reproduction | Expected recovery/error | Observed | Result |
|---|---|---|---|---|
| {{class}} | {{method}} | {{contract and user's next action}} | {{observation}} | pass/fail/partial/not_run |

When applicable, distinguish a valid empty result from missing coverage,
unmatched input, or rejected findings; follow the owning failure policy.

## Anomalies

- abnormality[{{registered-slug}}]: result={{pass|fail|not_run}}; evidence={{path-or-observation}}; issue={{issue-id-or-none}}

An empty anomaly list means none were observed in this run; it does not prove
that unknown anomalies cannot exist.

## Limitations

- {{states, platforms, data volumes, or failure modes not covered}}

## Verdict

`{{PASS / FAIL / PARTIAL}}`

Explain whether the contract may move to `verification_status: enforced`, must
remain partial, or requires reconciliation.
