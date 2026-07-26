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
- Revision/build: `{{commit/build id}}`
- Observable outcomes: {{outcomes}}
- Verifier: {{person/context}}
- Independence required: {{yes/no and why}}

## Environment

- Date/time: {{timestamp/timezone}}
- Runtime/platform/browser/device: {{environment}}
- Configuration and fixture identity: {{non-secret identity}}
- Starting state: {{state}}
- Reproduction command: `{{command}}`

## Result matrix

| Scenario/state | Expected | Structural evidence | Perceptual/operational evidence | Result |
|---|---|---|---|---|
| {{scenario}} | {{contract claim}} | {{measurement/test}} | {{observation}} | pass/fail |

## Failure and negative-path checks

| Failure class | Injection/reproduction | Expected recovery/error | Observed | Result |
|---|---|---|---|---|
| {{class}} | {{method}} | {{contract}} | {{observation}} | pass/fail |

## Anomalies

- `{{ID}}`: {{finding, severity, evidence, issue link}}

An empty anomaly list means none were observed in this run; it does not prove
that unknown anomalies cannot exist.

## Limitations

- {{states, platforms, data volumes, or failure modes not covered}}

## Verdict

`{{PASS / FAIL / PARTIAL}}`

Explain whether the contract may move to `verification_status: enforced`, must
remain partial, or requires reconciliation.
