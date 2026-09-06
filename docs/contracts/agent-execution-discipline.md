---
doc_type: contract
status: current
authority: normative
contract_role: governance
implementation: implemented
verification_status: partial
last_reconciled: 2026-09-06
review_due: 2026-10-24
supersedes: []
---

# AI agent execution discipline

## Purpose

This contract extends the repository's contract-first discipline with an
execution profile for autonomous or semi-autonomous coding agents. It governs
work selection, outcome-driven implementation and verification, independent design
review, fresh-context evaluation, layered completion, and truthful handling of
missing review authority.

It exists because a durable contract does not by itself prevent one agent from
reusing the same assumptions while designing, implementing, and approving its
own work.

## Scope

In scope:

- material feature, migration, cross-stack, and governance work performed by
  coding agents;
- work selection when no explicit executable task is available;
- written coordination between concurrently running agents or sessions;
- independence requirements for high-risk design and final evaluation;
- evidence classes and completion claims.

Out of scope:

- prescribing one agent framework, orchestration API, model, or vendor;
- requiring multiple agents for routine, mechanically bounded changes;
- replacing human authority for unresolved product or safety decisions;
- redefining a project's product or architecture contracts.

## Source anchors

### source[1] — 2026-07-26

> “The reusable template should absorb the multi-perspective design
> review, fresh-context evaluation, fixture-first engineering loop, KR sweep,
> and no-idle work-selection protocol.”

### source[2] — 2026-07-26

> “Do not present same-context analysis as independent review evidence; use a
> truthful blocked or governance-exception state when independent review is not
> available.”

### source[3] — 2026-07-26

> “The governance framework should not help developers define priority. It may
> identify risks and long-term abnormalities, but it must not, when the
> developer already has an idea, judge that idea wrong on their behalf.”

### source[4] — 2026-07-28

> “Enable rather than obstruct. An agent should know clearly what it should
> and should not do, instead of constantly fearing mistakes because it has
> not understood the user's needs and situation.”

### source[5] — 2026-08-27

> “Multiple parallel sessions need a written coordination method, and
> handoffs at context exhaustion have mature practices to follow.”

### source[6] — 2026-09-06

Maintainer feedback in the template review task, rendered in English: the
template must accommodate memory, long conversations, and delegated work
without losing the user's goal. Avoid compulsory phase approvals and excessive
startup documents. Deliver and verify the agreed task as a whole rather than
treating tests or process completion as the goal.

## Vocabulary and risk profiles

- **Routine change:** bounded implementation with an existing contract, no new
  semantics, no migration, and a small failure surface.
- **Material change:** changes behavior, a public contract, a durable state,
  more than one consumer, or an operator workflow.
- **High-risk change:** changes architecture, product semantics, authorization,
  irreversible data behavior, cross-process compatibility, or a high-impact UI
  interaction.
- **Independent review:** a review context that did not produce the proposal or
  implementation and receives the governing contract plus evidence rather than
  the implementer's unfiltered reasoning trace.
- **Governance exception:** an explicit human decision that waives or replaces
  a required review step for a named scope and records the residual risk.
- **Controlled experiment:** disposable, non-production implementation used to
  answer a named technical question that read-only investigation cannot answer;
  it creates evidence but no product contract or public behavior.
- **Activated concern:** a quality, compatibility, state, experience, or
  operational boundary triggered by the change traits in [development § activate-concerns](development-discipline.md#activate-concerns-instead-of-expanding-ceremony).

- from: source[1], source[2]

## Normative invariants

### Risk selects the execution depth

Routine work may use the base development discipline. Material work uses the
outcome-driven method below. High-risk work additionally requires independent
multi-perspective design review and fresh-context holistic evaluation.

The classification and rationale are recorded before implementation. A task is
not made routine merely to avoid review.

- from: source[1]

### Material delivery follows the outcome and its evidence

Establish the original request, accepted contract, current facts, and smallest
credible verification for each claim before dependent implementation. The
plan describes dependencies and one complete end state, not mandatory numbered
phases. It applies [development § bidirectional verification](development-discipline.md#verify-promised-and-observed-behavior-in-both-directions).

Use fixtures and a failing test first when they can expose the claimed defect
or protect a stable behavior. When the claim instead requires a built artifact,
real interaction, observation, or review, name that method and its limitations;
do not invent a meaningless failing test to satisfy a ritual. Record the
baseline relevant to the claim. A cheaper method cannot waive evidence or
independence required by the governing contract.

Implement, integrate, run affected guards, and evaluate the result against the
user's original outcome as well as the accepted contract. Correct discrepancies
within scope and continue through closure under [governance § authorized execution](governance-decision-boundary.md#delegated-engineering-work-proceeds-by-default).
Progress checkpoints do not request user approval. Fresh context is required
for completion evaluation when the risk classification requires it.

For an unresolved material technical fact, use the existing [controlled
experiment](development-discipline.md#contract-before-material-delivery-evidence-before-certainty)
path with its containment, expiry, cleanup, and concern-routing requirements.
It does not require a fictional product contract or failing test for behavior
not yet selected.

- from: source[1], source[4], source[6]

### High-risk design uses independent lenses

Before implementation, reviewers receive the original request or its source,
the accepted interpretation and contract, and baseline evidence. They evaluate
these through at least these lenses:

- system and contract consistency;
- user or operator experience;
- engineering cost, maintenance, and extensibility.

A separate synthesis identifies agreement, disagreement, residual risk, and
decisions requiring human authority. Every concern activated by [development § activate-concerns](development-discipline.md#activate-concerns-instead-of-expanding-ceremony)
selects an appropriate specialist or domain lens when that concern can affect
the high-risk outcome, and adds no review obligation when absent.

- from: source[1]

### Independence is evidence, not a label

The implementer cannot manufacture independence by writing several sections in
the same context. Review records identify the verifier context, inputs,
limitations, and whether independence was required and achieved.

Completion reviewers also receive the original request/source, accepted
interpretation, and observed results. They check for lost user intent as well
as conformance to the contract; a fresh context supplied only a mistaken
interpretation can repeat that mistake.

When the required independent context is unavailable, the work remains
`blocked` or `verifying` unless a human grants a documented governance
exception. Passing technical checks does not substitute for missing governance
evidence.

- from: source[2]

### Work selection has no silent idle state or invented priority

This fallback applies only when the owner has authorized ongoing autonomous
work against a portfolio or objective. Completing a bounded task is a valid
stopping point. Do not turn its completion into an unsolicited portfolio scan.
Within an authorized ongoing assignment, when no explicit executable task
exists, an autonomous agent:

1. resumes truthful in-progress work that is already authorized;
2. diagnoses blocked work without treating one blocker as project-wide;
3. consumes the highest-priority ready work from the declared portfolio or
   human owner;
4. if no task is ready, reviews the active portfolio read-only for an uncovered
   user outcome, boundary case, quality gap, or missing regression;
5. records candidate work with facts, risk, dependencies, and evidence limits;
6. when no authoritative priority exists, presents candidates as
   recommendations and requests a human decision before non-trivial
   implementation;
7. verifies completed task groups against their parent acceptance outcome;
8. reports completion only when no roadmap, release-gate, or reconciliation
   work remains within the claimed scope.

The declared portfolio or human owner owns priorities. Work discovery and risk
analysis do not grant the agent authority to rank or execute newly discovered
product work. The output classes and allowed blocker conditions are defined by
`governance-decision-boundary.md`.

- from: source[1], source[3], source[6]

### Completion is layered

- A task is complete when its requested outcome is observed under the accepted
  functional and quality boundaries, bidirectional effect verification closes,
  and its required evidence and affected regression pass.
- A task group or key result is complete when its integrated outcome is
  independently checked where required.
- An objective is complete when all outcomes pass, holistic evaluation closes,
  and contracts, plans, issues, guides, and evidence have final lifecycle
  states.
- A release gate is complete only when every gate claim has its own reproducible
  evidence.

Lower-level completion does not imply higher-level completion.

- from: source[1], source[2]

### Evidence classes remain explicit

Verification records name which class they provide, such as:

- unit or class-level guard;
- projection or seeded integration fixture;
- source-shaped or protocol-shaped fixture;
- generated scale evidence;
- built-entrypoint or packaged-artifact evidence;
- real process, HTTP, browser, device, or service evidence;
- operator-started manual diary;
- reviewed real-world sample or archive.

Each report states what it does not prove. Evidence classes may complement one
another but do not silently replace one another.

- from: source[1], source[2]

### The harness selects the smallest executable route

Before creating records, the agent determines which route applies:

- **Routine:** consume existing authority, make the bounded reversible change,
  run focused guards, and hand off without a new contract or plan.
- **Material with sufficient facts:** activate [development § activate-concerns](development-discipline.md#activate-concerns-instead-of-expanding-ceremony) concerns and run
  the outcome-driven delivery method.
- **Material with an unresolved technical fact:** route the experiment method
  through [development § activate-concerns](development-discipline.md#activate-concerns-instead-of-expanding-ceremony), run it inside [development § contract-first](development-discipline.md#contract-before-material-delivery-evidence-before-certainty)'s existing safety and
  disposal boundaries, then discard it or enter material delivery with its
  findings as evidence.
- **High-risk:** use the applicable material route plus independent review
  and fresh-context evaluation per the independent-lenses and
  independence-evidence invariants.

The current development discipline owns concern triggers and the governance
decision boundary owns engineering discretion and escalation. This contract
links those owners rather than restating their rules. Missing product intent or
risk authority remains a human decision; an ordinary reversible engineering
choice inside the declared envelope proceeds without serial approval.

- from: source[4]

### Parallel work is coordinated in writing

When more than one agent or session works the same repository concurrently,
coordination is written, not assumed:

- before starting, check the project's declared coordination surface — active
  plans, handoffs, or an explicit work register — for work that may touch the
  same files, contracts, or fixtures, and record your own scope there;
- when a change alters a shared surface — a public contract, a shared fixture
  or constant, a file another workstream is actively editing — announce it on
  that surface before or as it lands, so parallel workers see it before their
  next read;
- re-read a file before editing it when another workstream may have touched it
  since the last read; a stale read is the normal failure mode of parallel
  work, not an excuse for it;
- run the affected guards before claiming completion: the collision net for
  parallel work is the regression suite, not vigilance.

A handoff names the parallel work it knows about so the next session can
coordinate. When parallel changes conflict, reconcile them through the normal
authority order; the later worker does not silently revert the earlier one's
landed work.

- from: source[5]

### Delegated work carries bounded context and returns to an owner

Delegation is an optional execution strategy. Use it when a bounded part can
proceed independently and its integration cost is justified. Do not split a
tightly coupled decision merely to occupy agents.

Each assignment carries the parent outcome, the delegated result, current
authority and baseline, allowed writes and external effects, relevant context,
expected verification, and the stop/cancel condition. A short read-only task
may carry this in the native invocation; ongoing or concurrent writes use the
existing plan or handoff. Do not create a second task registry for compliance.
Unknown context inheritance is not evidence that a worker received a rule.

Workers return changed artifacts or observations, baseline/revision identity,
checks actually run, unresolved assumptions, and remaining work. The parent
checks stale baselines and conflicts, integrates the result, and verifies the
parent outcome. Several passing worker tasks do not establish that the combined
result works. Cancelled or late output is reviewed before use and must not
silently overwrite a newer decision or another worker's change.

- from: source[5], source[6]

## Required records

Material delivery work records only what its activated route requires:

- the governing contract and risk profile;
- the priority source or explicit human authorization for the selected work;
- a cold-start-capable implementation plan;
- claim-specific verification strategy and applicable controlled boundaries;
- relevant baseline, including a failing test result when that method is used;
- commands, environment, and evidence class for verification;
- independent review or the exact blocked/exception state when the risk profile
  requires it;
- when parallel work is active, the coordination entry and the shared-surface
  announcements made;
- final contract, plan, issue, and evidence lifecycle updates.

A controlled experiment uses a scratch record unless its result supports a
durable contract or decision. Routine work creates none of the records above
solely to prove that it is routine.

## Forbidden behaviors

- Do not call same-context notes independent reviews.
- Do not mark an objective complete because its implementation tasks are done.
- Do not treat unavailable user-started services or real data as automatically
  passing.
- Do not create untracked corrective implementation from a portfolio review.
- Do not convert an agent-authored recommendation into portfolio priority.
- Do not use a heavyweight review ritual for routine work without a recorded
  risk reason.
- Do not write a delivery contract to legitimize an unanswered experiment.
- Do not duplicate the concern trigger table in agent plans or entrypoints.
- Do not let temporary checkpoints become the undocumented end state.
- Do not edit from a stale read when parallel work is registered.
- Do not silently revert another workstream's landed change; reconcile through
  the normal authority order.

## Acceptance evidence

Mechanical enforcement covers record structure, template inventory, and links.
Behavioral effectiveness remains partial until adoption exercises actual agent
decisions and delivered outcomes. These are separate claims; a checker pass
does not establish the second.

This contract is implemented when:

- reusable templates exist for agent execution plans, independent review,
  holistic evaluation, and evidence-preserving data work;
- the documentation harness validates those templates as first-class
  deliverables;
- fixture tests prove missing or malformed required templates fail;
- repository guidance routes agent-driven material changes through this
  contract;
- repository guidance exposes the routine, controlled-experiment, material,
  and high-risk routes without requiring the agent to infer them from several
  documents;
- the correct Python runtime has a canonical, actionable verification path.

Verified on 2026-09-06:

- The [completed template change](../plans/2026-09-06-outcome-driven-template.md#progress-and-closure)
  records independent design and completion review, 114 passing fixtures, and
  normal/strict checker results. These support the revised template and routing
  claims. Native-agent adoption effectiveness remains partial.

Verified on 2026-07-26:

- `python3 -m unittest discover -s tests -p 'test_*.py'` passed the full fixture
  suite, including missing agent/adoption templates, missing-section, and
  unsupported-runtime cases;
- `python3 scripts/check_docs.py` passed; the checker's own summary line is the
  authority on the document and template inventory, so no count is restated here;
- the runtime preflight is covered without depending on a second interpreter
  being installed: the guard is asserted directly for 3.9, 3.10, and 2.7, and a
  source-order fixture keeps it ahead of the `tomllib` import.

Verified on 2026-07-28:

- `uv run --python 3.11 python -m unittest discover -s tests -p 'test_*.py'`
  passes the full fixture suite, including material-plan routing and removable
  high-risk review cases;
- normal and strict repository checks pass for the current guide projections,
  template inventory, and lifecycle state;
- scoped audits find no copied [development § activate-concerns](development-discipline.md#activate-concerns-instead-of-expanding-ceremony) trigger table or obsolete fresh-context
  requirement outside the high-risk route.

Verified on 2026-08-27:

- the written-coordination invariant added for written parallel-work coordination; the full Python 3.11
  fixture suite and both repository checker modes pass;
- behavioral effectiveness remains partial: no real multi-session project has
  exercised the coordination surface yet.

## Promise register

- promise[independent-adoption-review]: due=2026-10-24; status=open; owner=template-maintainer; description=obtain an independent adoption review after the first real product uses the agent execution profile

## Reconciliation log

- **2026-09-06 — outcome-driven execution:** replaced the fixed seven-phase
  default with dependency order and claim-specific verification; retained
  contract-before-delivery and required independent review. Bounded tasks may
  stop at completion. Delegation carries explicit scope and returns to an
  integrating owner. Verification status now states the outstanding behavioral
  limitation instead of implying that mechanical enforcement covers it.
  - from: source[6]

- **2026-08-27 — parallel coordination added:** A9 requires written
  coordination between concurrent agents or sessions: registered scope,
  announced shared-surface changes, re-reads before edits, and the guard
  suite as the collision net. Handoffs carry parallel-work context. Source:
  an external project archive whose human instruction stream showed parallel
  sessions colliding through stale reads and unannounced shared edits.
  - from: source[5]
- **2026-07-26 — contract created:** combined the template's contract-first
  governance with a risk-based AI execution profile derived from a concrete
  agent-driven product workflow.
- **2026-07-26 — implementation enforced:** registered four reusable templates,
  routed contributor entrypoints through the profile, and added fixture-backed
  template and Python-runtime checks. The real-project independent adoption
  review remains an explicit open promise rather than a completion blocker for
  the reusable harness itself.
- **2026-07-26 — priority authority reconciled:** clarified that the no-idle
  protocol consumes human-owned priority and may discover and recommend work,
  but cannot manufacture product direction or silently authorize execution.
- **2026-07-28 — proportional execution target landed:** added controlled
  experiments, concern-triggered specialist review, and a smallest-route
  selector so technical uncertainty no longer requires premature contracts and
  reversible routine work creates no governance artifacts. The material plan
  template now excludes routine work, makes high-risk review removable, and
  links activated concern owners; fixture and repository checks enforce the
  stable template surface.
- **2026-08-20 — publication redaction:** source[1] keeps the authorized
  practices and omits a sibling-project name that is not part of this
  template's public contract.
- **2026-08-20 — publication language:** remaining Chinese source anchors are
  published as English renderings of the original authorizations. Contracts
  that cite the same statement use the same wording; meaning is unchanged.
- **2026-08-28 — cutover to heading-slug identifiers:** the A1–A9 codes were
  retired; headings are now the identifiers per [documentation-harness § invariant-citations](documentation-harness.md#invariant-citations-resolve-to-headings).
  Incoming references across living documents were rewritten to slug links in
  the same change. Earlier entries in this log, completed plans, and dated
  evidence keep the codes as written.
