---
doc_type: plan
status: active
authority: planning
last_reconciled: {{YYYY-MM-DD}}
implements: docs/contracts/{{contract}}.md
supersedes: []
---

# {{Initiative}} implementation plan

## Cold-start summary

Write enough that a fresh contributor can continue without conversation
history: what is changing, why now, current verified facts, and which contract
is authoritative.

## Authority and prerequisites

- Structural authority: `ARCHITECTURE.md` § “{{section}}”
- Behavioral contract: `docs/contracts/{{contract}}.md`
- Surface contract, if applicable: `docs/design/{{surface}}.md`
- Baseline evidence: `{{path}}`
- Decisions already confirmed: {{decisions}}

## Complete end state

Describe the system after the whole change lands. Do not describe an
intermediate coexistence state as the target.

## Current state and gap

| Concern | Current verified fact | Contract requirement | Gap/evidence |
|---|---|---|---|
| {{concern}} | {{fact}} | {{requirement}} | {{gap}} |

## Execution order within one coherent change

### 1. {{Dependency/contract foundation}}

- Files/systems: {{targets}}
- Change: {{change}}
- Guard added: {{class-level guard}}
- Checkpoint outcome: {{observable outcome}}

### 2. {{Producer/state owner}}

- Files/systems: {{targets}}
- Change: {{change}}
- Failure/recovery handling: {{handling}}
- Guard added: {{guard}}

### 3. {{Consumers/projections}}

- Files/surfaces: {{targets}}
- Change: {{change}}
- Compatibility/cutover: {{decision}}
- Guard added: {{guard}}

### 4. {{Verification and closure}}

- Commands/probes: {{checks}}
- Independent verification: {{required/not required, reason}}
- Status updates: {{contracts/plans/issues/guides}}

## Risk register

| Risk | Trigger | Impact | Prevention/detection | Recovery |
|---|---|---|---|---|
| {{risk}} | {{trigger}} | {{impact}} | {{guard}} | {{action}} |

## Verification matrix

| Outcome | Unit/class guard | Integration/lifecycle | User-visible/probe | Evidence path |
|---|---|---|---|---|
| {{outcome}} | {{check}} | {{check}} | {{check}} | {{path/pending}} |

## Rollout, migration, and rollback

- Deployment unit/order: {{plan}}
- Data backup/migration: {{plan}}
- Compatibility window: {{bounded policy or none}}
- Abort signal: {{signal}}
- Rollback procedure and data limits: {{procedure}}

## Explicit non-goals

- {{not included and why}}

## Progress log

- **{{YYYY-MM-DD}} — {{pending/in progress/done/blocked}}:** {{result and
  evidence; update facts rather than merely saying “worked on it”}}

## Completion record

- Final revision/commit: {{id}}
- Contract implementation status: {{status}}
- Contract verification status: {{status}}
- Issues resolved/superseded: {{links}}
- Durable evidence: {{links}}
