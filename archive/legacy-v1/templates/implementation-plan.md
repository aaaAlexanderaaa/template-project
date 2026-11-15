---
doc_type: plan
status: active
authority: planning
last_reconciled: {{YYYY-MM-DD}}
implements: docs/contracts/{{contract}}.md
supersedes: []
---

# {{Initiative}} implementation plan

Use for material delivery under [execution risk and routing](../docs/contracts/agent-execution-discipline.md#risk-selects-the-execution-depth).
Routine work updates its existing behavior owner when needed and uses focused
evidence without this standalone plan. Keep records proportionate to the
actual dependency, coordination, and recovery work.

## Cold-start summary

Write enough that a fresh contributor can continue without conversation
history: what is changing, why now, current verified facts, and which contract
is authoritative.

Link the original request/source and its accepted interpretation. Read the
relevant current sections; do not copy their history into this plan.

Distinguish the owner's requested change from the chosen deliverable or example.
State why this work advances that change and what would remain if only this
deliverable succeeded. Attribute a material narrowing to its actual decision;
an instruction to proceed does not erase earlier requirements.

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

| Activated concern or dependency | Current verified fact | Normative owner | Plan step/evidence gap |
|---|---|---|---|
| {{concern}} | {{fact}} | `{{contract and section}}` | {{step/gap}} |

The linked contract owns boundaries and failure/escalation policy. This plan
must not restate them.

## Execution order within one coherent change

Replace the example steps below with actual dependencies. They are internal
checkpoints, not requests for user approval. Continue the authorized outcome
through integration and verification; escalate only newly exposed decisions
outside its authority or an actual blocker.

### 1. {{Dependency/contract foundation}}

- Files/systems: {{targets}}
- Change: {{change}}
- Guard added: {{proportionate class-level guard or local-only rationale}}
- Checkpoint outcome: {{observable outcome}}

### 2. {{Producer/state owner}}

- Files/systems: {{targets}}
- Change: {{change}}
- Failure/recovery handling: {{handling}}
- Guard added: {{guard or not applicable with reason}}

### 3. {{Consumers/projections}}

- Files/surfaces: {{targets}}
- Change: {{change}}
- Compatibility/cutover: {{decision}}
- Guard added: {{guard or not applicable with reason}}

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

Select the credible evidence needed per claim; unused methods need no invented
test. Include activated quality boundaries and apply [bidirectional verification](../docs/contracts/development-discipline.md#verify-promised-and-observed-behavior-in-both-directions).

## Rollout, migration, and rollback

Delete this section when compatibility, durable-state, or production rollout
concerns are not activated.

- Deployment unit/order: {{plan}}
- Data backup/migration: {{plan}}
- Compatibility window: {{bounded policy or none}}
- Abort signal: {{signal}}
- Rollback procedure and data limits: {{procedure}}

## Explicit non-goals

- {{not included and why}}

## Current execution state

- Verified position and evidence: {{current state and locator}}
- Next executable action and sufficient ending: {{action and result}}
- Blocked conditions and unaffected ready work: {{facts or none}}

Replace this state as work advances. Link dated evidence where needed; do not
append a growing startup diary or another summary of previous summaries.

## Completion record

- Final revision/commit: {{id}}
- Contract implementation status: {{status}}
- Contract verification status: {{status}}
- Issues resolved/superseded: {{links}}
- Durable evidence: {{links}}
- Reusable feedback, when relevant: {{changed existing owner and matching
  entrypoint; saved / incorporated / subsequently used, with evidence or an
  explicit unobserved limit}}
- Working context retired: {{active links/state reconciled; history retained
  only where it supports a live claim or recovery}}
