---
doc_type: guide
status: current
authority: guidance
last_reconciled: 2026-08-06
projection_of: [docs/contracts/governance-decision-boundary.md, docs/contracts/development-discipline.md, docs/contracts/agent-execution-discipline.md]
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

Inside an authorized outcome, use the engineering decision envelope in the
governance contract: locally reversible choices inside current authority and
activated boundaries proceed without serial approval. Investigate uncertainty
about technical reversibility before turning it into a human decision.

### 3. Resolve uncertainty without guessing or serial approval

Use the uncertainty route owned by development D10-D12 and governance G7:

- inspect repository evidence, then consult primary or official external
  sources with available network or retrieval tools for unfamiliar checkable
  references;
- when one tool is unavailable, identify its required capability and seek a
  fallback that preserves semantics, safety, and evidence strength;
- investigate missing technical facts, using a bounded D1 experiment only when
  read-only evidence cannot answer them;
- make and verify locally reversible engineering choices inside G6;
- present a bounded option set when the human owner must decide product intent,
  a material trade-off, an expensive-to-reverse preference, authority, or risk
  acceptance.

Answer the explicit question and surface a materially more consequential
unasked premise or risk when evidence supports the connection. State the
causal mechanism and its limits; do not replace the requested work or silently
expand its scope.

### 4. Run the change-execution loop

Use A8 in the agent execution contract to choose the smallest route. Routine
work consumes existing authority and focused guards without creating a plan.
An unresolved technical fact uses development D1's disposable experiment path
before delivery. Material delivery uses the seven-phase plan and only the
concerns activated through development D8. High-risk work adds the independent
design and fresh-context completion evidence required by A1/A3/A4.

The route links its normative owners rather than restating their boundaries in
the plan. Use the agent execution profile only at the depth selected during
onboarding or subsequently authorized by the project owner.

### 5. Report governance output precisely

Classify every material output as `fact`, `risk`, `recommendation`,
`human_decision_required`, or `execution_blocker`. A blocker must name the
exact path blocked, evidence, recovery, and available decision. Do not present
a preferred implementation as the only valid product direction.

### 6. Close the correct layer

Report task, task-group/key-result, objective, and release-gate completion
separately. Completing an implementation task does not close a higher outcome.
Return higher-layer results to the human-owned portfolio source; the governance
framework does not silently reprioritize remaining work.

## Verification

- The selected item traces to a human-owned priority source or explicit choice.
- Recommendations and blockers use the correct classification.
- External claims identify checkable authoritative sources, unavailable tools
  have capability-preserving fallback evidence or explicit limitations, and
  human option sets are reserved for decisions the owner actually owns.
- Analysis explains the causal mechanism and bounds any surfaced unasked issue
  to evidence and authorized scope.
- The execution plan links the applicable current/target contracts.
- Every activated concern links the contract that owns its boundary and
  failure/escalation policy.
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
