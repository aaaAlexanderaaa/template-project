---
doc_type: issue-tracker
status: active
authority: normative
last_reconciled: {{YYYY-MM-DD}}
initiative: {{initiative-slug}}
---

# {{Initiative}} issue tracker

## {{SEVERITY-ID}} — {{Short finding}}

- **Status:** `unverified`
- **Reported:** {{YYYY-MM-DD, source}}
- **Affected outcome:** {{functionality/presentation/interaction/design/reliability}}
- **Initial claim:** {{what is believed to be wrong}}

### Evidence

- Source/location: `{{file:line, URL, log, probe, or reproduction}}`
- Reproduction: {{steps/command}}
- Expected: {{contract-backed behavior}}
- Observed: {{observation}}

### Verification

- Verdict: `{{verified/disproved/partial}}`
- Verifier/context and independence when required: {{identity and basis}}
- What is actually true: {{refined statement}}
- Evidence limitations: {{limitations}}

### Category and root mechanism

- Defect category: {{parser fragility/state inconsistency/permission leak/
  race/interactive clipping/cross-surface inconsistency/etc.}}
- Root mechanism: {{mechanism, not merely symptom}}
- Plausible sibling variants: {{variants}}

### Contract impact

- Relevant contract: `{{path and section}}`
- Classification: `{{implementation regression / contract gap / requirement
  change / evidence error}}`
- Required reconciliation: {{change or none}}

### Decision

- `{{accepted/wontfix/fix}}`
- Rationale and authority: {{decision}}

### Resolution

- Change: {{summary}}
- Revision/commit: {{id}}
- Sibling-variant guard: {{test/check and sibling case it catches, or local-only
  rationale when no repeatable mechanism or proportionate guard exists}}
- Verification evidence: {{path}}
- Final status: `resolved`
