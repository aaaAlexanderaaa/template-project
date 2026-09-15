---
doc_type: contract
status: current
authority: normative
contract_role: governance
implementation: implemented
verification_status: partial
last_reconciled: 2026-09-15
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

- risk classification and delivery of local features, migrations, cross-stack,
  and governance work performed by coding agents;
- work selection when no explicit executable task is available;
- written coordination between concurrently running agents or sessions;
- independence requirements for high-risk design and final evaluation;
- evidence classes and completion claims.

Out of scope:

- prescribing one agent framework, orchestration API, model, or vendor;
- requiring multiple agents for routine, mechanically bounded changes;
- replacing human authority for unresolved product or safety decisions;
- redefining a project's product or architecture contracts.

## Vocabulary and risk profiles

- **Routine change:** authorized, bounded work within an existing owner, with
  low-impact effects that are inexpensive to recover and credible focused
  verification. It may add local behavior under the delivery-contract rule;
  none of the material or high-risk conditions below may apply.
- **Material change:** changes a published API, event, schema, or integration
  contract (including compatible additions), durable-state semantics, or a
  migration; requires a new normative owner, coordinated changes to separately
  owned commitments, or substantial dependency or recovery planning. Updating
  an existing surface contract for local behavior is not itself a published
  integration change. File count and incidental consumer edits do not select
  this profile. After investigation, delivery that does not meet the routine
  conditions uses this profile unless high-risk conditions apply.
- **High-risk change:** changes authorization or isolation enforcement, or has
  a credible failure path to serious confidentiality, integrity, availability,
  financial, safety, or critical user/operator harm. Broad exposure,
  difficult-to-recover effects, or a consequential compatibility failure can
  establish this profile. Architecture and product-meaning changes prompt this
  assessment; their names alone do not establish high risk.
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

- from: source[1], source[2], source[7]

## Normative invariants

### Risk selects the execution depth

Routine work may use the base development discipline. Material work uses the
outcome-driven method below. High-risk work additionally requires independent
multi-perspective design review and fresh-context holistic evaluation.

Assess actual effects, affected users and owners, failure impact, and recovery
cost before implementation. Reverting code does not undo a disclosure, an
incorrect privilege grant, or a destructive write. A one-line isolation change
is high-risk; a local list sort with bounded effects can be routine. Apply the
highest profile whose conditions hold. Investigate unknown technical impact
before claiming it is low; unavailable evidence or a reviewer cannot justify a
downgrade.

Record the classification and rationale in the existing task context for
routine work and in the execution plan for material/high-risk work. Routine
work creates no separate classification record. Risk selects execution depth,
not authorization: [governance](governance-decision-boundary.md#delegated-engineering-work-proceeds-by-default)
still owns permission to change behavior. Activated quality boundaries apply
on every route. Activation alone creates no new plan or review requirement;
explicit evidence and review requirements in the owning contract remain binding.

- from: source[1], source[7]

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
work against a portfolio or objective. The standing form of that authorization —
a charter with expiry, epoch records, role identities, and calibration — is
owned by [autonomous operation](autonomous-operation-discipline.md); this
invariant governs work selection within it. Completing a bounded task is a valid
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

- from: source[1] (2026-07-26 execution-profile origin), source[3] (2026-07-26 no agent-defined priority), source[6] (2026-09-06 outcome-driven feedback)

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

A simulation, mock, or controlled fake establishes that the system runs; it
does not establish that the outcome holds under real data, real counterparts,
or a real environment. A demonstration that required invisible manual
correction is evidence about the correction, not about the system.
Real-environment verification carries its own cost and risk, so bound it and
set its stop conditions before running it.

- from: source[1], source[2], source[8]

### Billed, rate-limited, and account-bound resources are spent deliberately

Work that spends billed, rate-limited, or account-bound resources declares
its expected volume and stop condition before running, and reports actual
spend against that declaration.

A rate-limit or quota response is a defect in our own mechanism — missing
idempotency, missing caching, unbounded concurrency, or blind retry — not
evidence that the other side raised its limits. The response is to
circuit-break and fix the mechanism, never to retry into the limit. Writes to
external systems are idempotent and atomic: a retry never replays a completed
effect, because account safety outranks feature completion.

When parallel calls share a cacheable prefix, a first call establishes the
cache before fan-out; when the cache demonstrably misses, the work falls back
to sequential execution without sunk-cost attachment. Concurrency — including
the number of delegated workers — is a knob set by upstream quota and task
shape: cross-validation and exhaustive collection justify more, single-thread
diagnosis justifies none. It is not a fixed preference.

Cost-awareness is the default, not a ceiling on declared-important work: the
owner may lift limits explicitly. Quotas exist to protect accounts and
attention, not to ration compute.

- from: source[8]

### The harness selects the smallest executable route

Before creating records, the agent determines which route applies:

- **Routine:** consume existing authority, update the existing behavior owner
  when authorized behavior changes under [development's delivery-contract rule](development-discipline.md#contract-before-material-delivery-evidence-before-certainty),
  implement and verify the bounded effects, and hand off without a standalone
  contract or plan. Preserve applicable concern boundaries and exceptions.
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

When the owner will be unavailable, shape the work to fit the authorized
operation set and pre-name the decision points that must pause, rather than
letting the work collide with an approval wall; prefer a read-only equivalent
over an approval-requiring step when it serves the same purpose. When
delegated work fails, first suspect the assignment's context, contracts, and
descriptions — not the worker.

- from: source[5], source[6], source[8]

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
Behavioral effectiveness is a separate claim: first-party adoption has
exercised these routes since 2026-07 (see the 2026-09-14 entry), and
independent adoption review remains open. A checker pass establishes only the
first.

The [September 7 change record](../plans/2026-09-06-proportionate-execution.md#progress-and-closure)
records the consequence-based routing review and focused/full checks. Its
scenario evidence covers reusable guidance, not measured adopter effectiveness.

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

Verified on 2026-09-14:

- first-party adoption since 2026-07 exercised the risk routes, written
  parallel coordination, and delegation in the maintainer's own projects;
  their feedback produced the resource-spending invariant, the delegation
  envelope, and the simulation boundary recorded in the reconciliation log.
  Evidence: [2026-09-14 first-party adoption feedback](../evidence/2026-09-14-first-party-adoption-feedback.md);
- behavioral effectiveness outside the maintainer's portfolio remains
  unproven; the independent adoption review promise below stays open.

## Promise register

- promise[independent-adoption-review]: due=2026-10-24; status=open; owner=template-maintainer; description=obtain an independent adoption review after the first real product uses the agent execution profile

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

### source[7] — 2026-09-07

English rendering of the maintainer's accepted proposal and instruction to
continue: classify changes by consequences, permit authorized low-impact new
behavior without a standalone plan, and make current task facts and boundaries
easy to locate. Keep required independent review for high-risk work.

### source[8] — 2026-09-14

English rendering of maintainer feedback distilled from first-party adoption:
work that spends billed, rate-limited, or account-bound resources declares
its volume and stops at its bound; a rate-limit response is a defect in our
own mechanism, so circuit-break and fix the mechanism rather than retrying
into it; a retry never replays a completed effect; concurrency follows
upstream quota and task shape; and when the owner is unavailable, work is
shaped to fit the authorized operation set with pre-named pause points.

## Reconciliation log

- **2026-09-15 — standing authorization routed:** the work-selection invariant
  now names `autonomous-operation-discipline.md` as the owner of the standing
  charter form of authorized ongoing work — expiry, epoch records, role
  identities, and calibration. The selection rules themselves are unchanged.

- **2026-09-14 — resource spending and delegation envelope:** added the
  billed, rate-limited, and account-bound resource invariant; the simulation
  and manual-correction boundary in evidence classes; and the
  unattended-execution and failure-attribution rules for delegation. Source:
  first-party adoption feedback, including an incident in which repeated
  non-atomic writes suspended a real account.
  - from: source[8]

- **2026-09-07 — consequence-based execution:** broadened routine work to
  authorized low-impact local behavior and retained material planning for
  published contracts, state semantics, and substantive coordination. Risk
  follows effects and recovery cost; authorization and isolation retain
  independent review. Classification creates no routine-only record.
  - from: source[7]

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
