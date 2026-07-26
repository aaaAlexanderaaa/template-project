---
doc_type: guide
status: current
authority: guidance
last_reconciled: 2026-07-26
---

# AI-guided project onboarding

## Purpose

Adopt this repository's governance in a greenfield or running project without
mistaking template content for project truth, overwriting existing authority,
or turning onboarding into an unbounded cleanup program.

The normative behavior is defined by the
[project adoption contract](../contracts/project-adoption.md) and the
[governance decision boundary](../contracts/governance-decision-boundary.md).

## Preconditions

- An adopting human owner is available to confirm scope, profile, priority
  authority, and risk acceptance.
- The AI or contributor has read-only access to the target repository and its
  existing project-control sources.
- Active incidents, releases, migrations, and destructive operations are known
  before governance files are changed.
- Existing changes and local instructions will be preserved.

## Procedure

### 1. Classify the adoption

- **Greenfield:** no product implementation or established project authority.
  Use the template as the starting repository, establish current structural
  authority, select the initial managed boundary, then begin implementation.
- **Brownfield:** existing code, decisions, workflows, or delivery obligations.
  Begin with an `observed` read-only assessment and use staged enforcement.

### 2. Inventory before proposing

Inspect, without rewriting:

- architecture, modules, services, persistence, and source roots;
- READMEs, ADRs, contracts, tickets, plans, and agent instructions;
- tests, CI, deployment, rollback, observability, and incident procedures;
- product/direction owner, priority source, maintainers, and risk authority;
- active work, release commitments, known debt, and unresolved conflicts.

Do not infer authority from recency or file length. Mark facts, unknowns, and
conflicts separately.

### 3. Create the adoption assessment

Copy
[adoption-assessment.md](../../templates/adoption-assessment.md) into
`docs/evidence/YYYY-MM-DD-adoption-assessment.md`. Complete it from verified
repository evidence rather than chat memory.

The human owner confirms:

- project-defined governance profile;
- managed paths and boundaries;
- explicit exclusions;
- authoritative priority source;
- immediate rules versus advisory rules;
- current adoption stage.

### 4. Separate current and target state

Describe the current system in `ARCHITECTURE.md` only when it is verified. Put
future behavior in target contracts and active plans. Do not make architecture
look clean by deleting evidence of current debt or by copying aspirational
template prompts into current authority.

### 5. Plan one bounded migration

Use [implementation-plan.md](../../templates/implementation-plan.md) for the
first managed boundary. A brownfield adoption normally moves through:

1. `observed` — read-only facts and conflicts;
2. `baselined` — profile, scope, authority, and historical debt confirmed;
3. `scoped_enforcement` — selected boundaries are contractually and
   mechanically governed;
4. `adopted` — every agreed adoption outcome has evidence.

Historical debt does not automatically block unrelated delivery. New work must
not silently expand a baseline debt class.

### 6. Reconcile entrypoints

Update root and local `AGENTS.md`, contributor guidance, architecture ownership,
source roots, CI entrypoints, and applicable contracts for the selected scope.
Preserve or supersede existing instructions explicitly; never assume copied
template files outrank project-specific authority.

## Verification

- The assessment names evidence for every current-state claim.
- The adopting human confirmed profile, scope, priority authority, and stage.
- Current and target descriptions are visibly separate.
- Existing authorities are preserved or have explicit supersession links.
- The first managed boundary has a contract, plan, and verification path.
- The repository check passes for the scope claimed as enforced.
- Remaining debt, exclusions, decisions, and higher adoption stages stay open.

Passing the checker proves structural validity, not semantic correctness or
project-wide adoption.

## Failure and recovery

- If product behavior is being rewritten during assessment, stop and create a
  separately authorized implementation plan.
- If copied template guidance conflicts with existing authority, keep the
  affected boundary `observed` or `baselined` and reconcile it.
- If adoption interrupts delivery disproportionately, narrow managed scope and
  preserve the residual gap instead of declaring false compliance.
- If transition evidence is later disproved, return to the last supported stage
  and record the evidence conflict.

## Safety and rollback

Onboarding is additive until a separately reviewed supersession or migration is
authorized. Do not delete existing documentation, tests, CI, deployment paths,
or tracker records as part of inventory. Keep a recoverable revision for every
entrypoint changed during adoption.

## Related authority

- [Documentation authority map](../README.md)
- [Development discipline](../contracts/development-discipline.md)
- [AI agent execution discipline](../contracts/agent-execution-discipline.md)
- [Project operation after onboarding](project-operation.md)
