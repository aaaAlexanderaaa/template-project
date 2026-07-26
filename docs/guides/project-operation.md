---
doc_type: guide
status: current
authority: guidance
last_reconciled: 2026-07-26
---

# Project operation after onboarding

## Purpose

Use the governance framework to improve project decisions and execute
authorized work efficiently after onboarding, without delegating product
direction or portfolio priority to the framework.

The [governance decision boundary](../contracts/governance-decision-boundary.md)
is normative. This guide describes the operating loop.

## Preconditions

- The adoption assessment declares managed scope and current stage.
- A human-owned product/direction authority is known.
- An authoritative priority source or explicit owner is known.
- Current architecture and applicable contracts can be located.
- Existing in-progress and blocked work is truthfully represented.

## Procedure

### 1. Consume direction; do not manufacture it

Start from the declared priority source. The framework may report missing user
outcomes, dependency conflicts, aging work, risk concentration, maintenance
cost, and evidence gaps. These are decision inputs, not automatic priority.

When priority is absent or ambiguous, present a bounded candidate set with:

- verified facts and affected outcomes;
- risk and long-term cost;
- dependencies and readiness;
- expected benefit and evidence limits;
- reversible options and required owner.

Wait for human direction before non-trivial implementation unless an existing
policy already authorizes the choice.

### 2. Select only ready, authorized work

A work item is ready when its intended outcome, authority, owner, dependencies,
managed scope, risk profile, and acceptance evidence are sufficiently clear for
its change class. Missing product preference is a human decision, not a fact the
agent fills in.

Resume authorized in-progress work before discovering replacement work. A
blocker on one item does not make unrelated authorized work blocked.

### 3. Run the change-execution loop

For the selected item:

1. inspect current authority and evidence;
2. reconcile conflicts;
3. land or update the behavioral contract;
4. plan one coherent end state;
5. encode acceptance and sibling-variant guards;
6. implement and verify proportionally to risk;
7. update contract, plan, issue, guide, and evidence lifecycle.

Use the agent execution profile only at the depth selected during onboarding or
subsequently authorized by the project owner.

### 4. Report governance output precisely

Classify every material output as `fact`, `risk`, `recommendation`,
`human_decision_required`, or `execution_blocker`. A blocker must name the
exact path blocked, evidence, recovery, and available decision. Do not present
a preferred implementation as the only valid product direction.

### 5. Close the correct layer

Report task, task-group/key-result, objective, and release-gate completion
separately. Completing an implementation task does not close a higher outcome.
Return higher-layer results to the human-owned portfolio source; the governance
framework does not silently reprioritize remaining work.

## Verification

- The selected item traces to a human-owned priority source or explicit choice.
- Recommendations and blockers use the correct classification.
- The execution plan links the applicable current/target contracts.
- Acceptance evidence covers the declared risk and boundary surface.
- Completion is reported at the correct layer.
- Newly discovered work is recorded but not assigned silent priority.

## Failure and recovery

- Missing priority: stop project-level selection, report candidates, and request
  the declared owner's decision.
- Conflicting authority: block only the affected implementation path and start
  reconciliation.
- Missing evidence: downgrade the claim rather than the test threshold.
- Over-broad governance: narrow the affected gate or use an authorized,
  expiring exception with residual risk.

## Safety and rollback

Governance recommendations are reversible until an authorized change is
implemented. Preserve rejected options and superseded decisions as history.
Never use portfolio diagnosis as authorization for destructive, privileged, or
materially expansive work.

## Related authority

- [Project adoption contract](../contracts/project-adoption.md)
- [Development discipline](../contracts/development-discipline.md)
- [AI agent execution discipline](../contracts/agent-execution-discipline.md)
- [AI-guided onboarding](onboarding.md)
