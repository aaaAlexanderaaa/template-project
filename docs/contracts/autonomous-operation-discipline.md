---
doc_type: contract
status: current
authority: normative
contract_role: governance
implementation: implemented
verification_status: partial
last_reconciled: 2026-09-15
review_due: 2026-12-14
supersedes: []
---

# Autonomous operation discipline

## Purpose

This contract governs agent work that continues toward a high-level objective
across many unsupervised wakes — around-the-clock operation or scheduled
self-evolution — after the owner has authorized that mode. The collaboration
mode's assumptions fail quietly here: authorization was per task, the owner's
judgment was exercised live in each session, and continuity was carried by
conversation. Unattended operation replaces these with a standing charter,
written artifacts, and a taste corpus, and its characteristic failures are
direction drift, self-confirming judgment, and triggers deferred forever.

Original request/source: source[1], with the alignment decisions in source[2]
and source[3].
Accepted interpretation: an owner can hand an agent a bounded objective, leave,
and return to a system that stayed inside its authorization, recorded what it
did, and escalated what it could not decide.

## Scope

### In scope

- the standing charter as the vehicle of continuous authorization;
- the epoch protocol: how one unattended wake orients, acts, verifies, and
  records;
- the planner, executor, and reviewer identities and their separation when one
  agent plays all three;
- representation and calibration of owner taste;
- behavior when no authorized work is executable;
- deferral control for triggers the agent evaluates itself;
- evolution of this discipline by ratified proposal.

### Out of scope

- scheduling or orchestration machinery (cron, daemons, CI triggers);
- per-task collaboration mode, which needs no charter;
- risk classification, execution depth, and independence evidence within one
  change, owned by [agent execution](agent-execution-discipline.md);
- the authority classes a charter may delegate and the engineering decision
  envelope inside it, owned by
  [governance](governance-decision-boundary.md#delegated-engineering-work-proceeds-by-default);
- product direction, priority, and risk acceptance, which remain with the
  human owner in every mode.

## Vocabulary

| Term | Meaning | Excluded meaning |
|---|---|---|
| `charter` | Standing written authorization for autonomous work, in the two layers below | A task ticket, a plan, or agent-authored priority |
| `base charter` | Project-level layer: taste corpus location, forbidden zones, resource ceilings, sync cadence, halt conditions | Objective selection |
| `objective charter` | Per-objective layer: the high-level goal, scope, stop conditions, and an expiry date | A milestone plan with phase approvals |
| `epoch` | One bounded wake: orient, act, verify, record | A phase gate requiring owner approval |
| `planner identity` | The position loyal to the objective's meaning and direction | A planning step that any pass can rubber-stamp |
| `executor identity` | The position loyal to observed fact | Permission to absorb friction silently |
| `reviewer identity` | The position loyal to the standard and the taste corpus | An editor, or a same-context summary |
| `taste corpus` | The owner's corrections and decisions; the highest authority on preference | The agent's written summary of those corrections |
| `taste model` | The agent's derivative, falsifiable hypothesis of owner preference | Owner authority of any kind |
| `sync` | The scheduled owner contact that reviews calibration, deferrals, role conflicts, and amendment proposals | Approval of individual tasks |
| `calibration ritual` | Comparison of recorded predictions against the owner's actual decisions at a sync | A retrospective the agent grades itself |
| `deferral record` | Written justification for not acting on a fired trigger, naming the changed condition that will allow it | A note to handle it "next time" |
| `reflection artifact` | The output that makes a reflection pass real: an owner question, a risk record, a reconciliation proposal, or an explicit no-findings note | An activity log |

## Ownership and boundary

- This contract owns standing autonomous operation: the charter, the epoch
  protocol, role identities, taste calibration, and deferral control.
- [Agent execution](agent-execution-discipline.md) owns risk classification,
  the smallest executable route, and independence evidence within a change;
  its [work-selection fallback](agent-execution-discipline.md#work-selection-has-no-silent-idle-state-or-invented-priority)
  applies inside a live charter.
- [Governance](governance-decision-boundary.md) owns what may be authorized at
  all; a charter is one form of its declared authorization and never transfers
  direction, priority, or risk acceptance.
- [Development](development-discipline.md) owns concern activation and
  verification standards; an epoch obeys them unchanged.
- A charter never overrides a current contract. It authorizes work under them.

## States and triggers

| State | Entry trigger | Allowed actions | Exit trigger | Failure behavior |
|---|---|---|---|---|
| `dormant` | No live charter, an expired charter, or no scheduled wake | Read-only diagnosis; preparing renewal material | A wake begins under a live charter | Expiry never self-renews; silence keeps the state dormant |
| `orienting` | A wake begins under a live charter | Read the charter, current contracts, current state, and open questions; select the route | Route selected: execute, reflect, halt, or escalate | Charter ambiguity halts the affected scope |
| `executing` | Authorized work selected | Implement and verify per [agent-execution § smallest-route](agent-execution-discipline.md#the-harness-selects-the-smallest-executable-route) | Work verified and recorded, a stop condition reached, or the wake budget spent | A halt condition moves the scope to `halted` |
| `reflecting` | No authorized executable work remains | Multi-perspective reflection that ends in a reflection artifact | Artifact recorded, including an explicit no-findings note | Reflection without an artifact is recorded as drift |
| `halted` | A halt condition, a repeated deferral, or charter ambiguity | Write the owner question; read-only preservation | An owner answer or charter renewal | Never self-resumes on silence |

Invalid transitions: `dormant` to `executing` without `orienting`; `halted` to
`executing` without an owner answer; any state to `executing` after charter
expiry.

## Normative invariants

### Standing work runs under a live charter

No autonomous work begins or continues without a live charter. The base
charter names the taste corpus location, forbidden zones, resource ceilings,
sync cadence, and halt conditions; each objective charter names one high-level
goal, its scope, its stop conditions, and an expiry date. Expiry downgrades
the agent to `dormant` or read-only mechanically — by date, not by the agent's
judgment that work remains. Renewal is an explicit owner act; silence is not
renewal. The agent may shrink its charter's scope when uncertain and may never
extend it, and it never edits the charter itself.

- from: source[2] (2026-09-15 alignment decisions), source[3] (2026-09-15 idle and deferral amendments)

### Every wake re-orients from artifacts

A wake is a cold start. Continuity exists only in written artifacts, so each
epoch begins by reading the charter, the applicable contracts, the recorded
current state, and the open questions left by earlier epochs — not by trusting
impressions. Plans are re-derived per epoch from the objective and current
facts; a previous epoch's plan is input, not authority. Each epoch ends by
recording what changed, what was verified, and what remains open. Work that
was not recorded is treated as not done.

- from: source[1] (2026-09-15 autonomy design question)

### Trigger evaluation is recorded and deferral is counted

Trigger conditions are expressed mechanically wherever possible: dates,
counts, checker results, measurable thresholds. Where agent judgment is
unavoidable, the evaluation still leaves a written record. Deferring a fired
trigger requires a deferral record naming the changed condition that will
allow it to fire. The same trigger deferred at two consecutive evaluations
escalates to the owner at the earliest contact channel the base charter
names, and the trigger's action does not run autonomously meanwhile. "The
next wake will handle it" without a recorded condition is a named failure
mode, not a scheduling choice.

- from: source[3] (2026-09-15 idle and deferral amendments)

### Roles are identities with loyalties, not pipeline stages

The planner, executor, and reviewer are standing relationships to the same
objective, defined by loyalty and prohibition. The planner is loyal to the
objective's meaning — why the work exists and whether the direction still
holds — and does not deliver. The executor is loyal to observed fact — what
actually happened when the work ran — and never absorbs friction silently;
it surfaces execution problems upward. The reviewer is loyal to the standard
and the taste corpus, and never edits; editing would make it complicit in the
output it judges. All three share the same contracts, evidence discipline,
and taste corpus. A conflict between identities is a signal to escalate, not
material to average into a compromise the charter did not authorize. An
identity persists across epochs and accumulates a track record — planner
direction calls, reviewer finding validity — which feeds calibration.

- from: source[1] (2026-09-15 autonomy design question)

### Role separation survives single-agent operation

One agent may hold all three identities, but never in one pass. The reviewer
pass receives the governing contract and the evidence, not the executor's
reasoning trace; [agent-execution § independence-evidence](agent-execution-discipline.md#independence-is-evidence-not-a-label)
still governs, and high-risk work still requires its fresh-context review.
Cadence is layered: the executor acts every wake; the planner acts at epoch
boundaries and whenever direction is in doubt; the reviewer acts at
milestones and on high-risk triggers. Running the full three-identity ritual
on every trivial wake is ceremony, not discipline.

- from: source[1] (2026-09-15 autonomy design question), source[2] (2026-09-15 alignment decisions)

### Reviewer findings are answered in writing

A high-risk finding blocks the affected path until resolved or waived by the
owner. Every other finding requires the executor's written response — accept,
or rebut with the recorded basis — because silently absorbed feedback is
feedback lost. A role conflict that cannot be resolved under the charter goes
to the owner at the next sync, or immediately when it is high-risk. The
reviewer's loyalty is to the standard, so planner urgency never overrules a
finding on its own.

- from: source[2] (2026-09-15 alignment decisions)

### Idle produces reflection artifacts or rest, never busywork

When no authorized executable work remains, dormancy is a legitimate epoch
outcome, not a failure. The alternative is a reflection pass, never
manufactured activity: re-examine the objective against the current state,
re-open historical trade-offs and test whether their assumptions still hold
so past decisions stay re-examinable rather than fossilized, walk the product
from the target user's position and judge its coherence, and look for
architecture and test improvements. Each additional perspective exists to
expose self-consistency gaps that one position cannot see. Every reflection
pass ends in a reflection artifact. Activity without an artifact or a goal
linkage is drift and is recorded as such.

- from: source[1] (2026-09-15 autonomy design question), source[3] (2026-09-15 idle and deferral amendments)

### Taste lives in a corpus; the model is a hypothesis

The taste corpus — the owner's corrections and decisions — is the highest
authority on preference, outranking any text derived from it, including this
discipline's own summaries. The taste model is a hypothesis and is labeled as
one wherever it is used. Before each sync, the agent records its predictions
of pending owner decisions; the calibration ritual compares predictions with
the owner's actual answers, and the corpus absorbs every correction. The
per-epoch override rate is the primary health metric of autonomous operation.
A rising override rate, or a conflict between corpus and model, is a
top-priority escalation and shrinks autonomous scope until calibration. The
owner may carve taste-dense domains out of the charter entirely.

- from: source[1] (2026-09-15 autonomy design question), source[2] (2026-09-15 alignment decisions)

### The discipline evolves by ratified proposal

Changes sort into three tiers. Implementation choices inside the envelope
proceed under existing governance. Behavior changes update their existing
contract owners under the delivery-contract rule. Changes to a charter or to
this discipline are proposal-only for the agent: the proposal names the
observed failure or evidence that motivates it, and takes effect only when
the owner ratifies it. The agent never edits its own authorization source,
including to fix a charter defect; a defective charter is a halt condition,
not an invitation.

- from: source[2] (2026-09-15 alignment decisions)

## Required behaviors

- A live two-layer charter exists before the first autonomous wake and is
  re-read at every wake; `templates/charter.md` is the starting shape, or its
  adopted equivalent in a project.
- Each epoch leaves a record: the route taken, artifacts changed,
  verification run, open questions, and any deferrals.
- Every trigger evaluation leaves a record; deferrals are counted per
  trigger.
- Every reviewer finding carries a severity and, when non-blocking, the
  executor's written response.
- Predictions of pending owner decisions are written before each sync and
  compared at the calibration ritual.
- Every reflection pass ends in a reflection artifact.
- Charter and discipline amendments arrive at a sync as proposals with their
  motivating evidence.

## Forbidden behaviors

- Do not act autonomously without a live charter, or infer authorization from
  silence, past activity, or the cost of stopping.
- Do not edit the charter, extend its expiry, or reinterpret its stop
  conditions to keep working.
- Do not defer a fired trigger without a recorded condition, or defer the
  same trigger at two consecutive evaluations.
- Do not present the executor's own pass as reviewer output, or same-context
  notes as independent review.
- Do not present the taste model as owner authority; the corpus outranks it.
- Do not manufacture activity to avoid a dormant epoch, and do not treat a
  dormant epoch as failure.
- Do not end a reflection pass without an artifact.
- Do not average a role conflict into a compromise the charter did not
  authorize.
- Do not treat a previous epoch's plan as authority.
- Do not repair an out-of-charter action silently; stop, record, restore what
  is reversible, and report.

## Failure, recovery, and intervention

- Expired or missing charter: enter `dormant`; read-only diagnosis may
  continue; renewal is an owner act.
- Halt condition: enter `halted` with a written owner question that names
  options; resume only on an owner answer.
- Second consecutive deferral of a trigger: escalate at the earliest contact
  channel the base charter names; the affected scope pauses.
- Rising override rate or corpus-model conflict: request calibration early
  and shrink autonomous scope to lower-risk routes until it happens.
- Discovered out-of-charter action: stop the affected scope, record, restore
  what is reversible, and report at the earliest channel.
- Lost or corrupt epoch records: reconstruct from artifacts; claimed work
  that cannot be verified is treated as not done.

## Acceptance evidence

This contract is implemented when:

- agent and contributor entrypoints route standing autonomous work to this
  contract;
- the work-selection and authority owners name the charter as the standing
  authorization form;
- the documentation checker and fixture suite pass with the contract in
  place.

Verified on 2026-09-15:

- `AGENTS.md`, `docs/README.md`, `docs/contracts/README.md`, and
  `docs/guides/project-operation.md` route standing autonomous operation to
  this contract; [governance § work-selection](governance-decision-boundary.md#work-selection-consumes-authority)
  and [agent-execution § work-selection](agent-execution-discipline.md#work-selection-has-no-silent-idle-state-or-invented-priority)
  name the charter as the standing authorization form;
- `python3 -m unittest discover -s tests -p 'test_*.py'` passed the full
  fixture suite;
- `python3 scripts/check_docs.py` passed in normal and strict modes.

Also on 2026-09-15, a fresh-context independent review of this landing
([record](../evidence/2026-09-15-autonomous-operation-review.md)) returned
safe-to-keep; its four corrections — scan-report summarization, two citation
gloss backfills, contributor-entrypoint routing, and template-exemplar
glosses — were applied and the suite re-verified green.

Verification remains `partial`: the repository proves structural routing, not
that a real project stays healthy across unattended epochs. The behavioral
evidence is the promise below; if it has not materialized by its due date,
mark this contract `historical` or merge its live rules into
[agent execution](agent-execution-discipline.md) rather than letting it age
as unexercised authority.

## Promise register

- promise[first-party-epoch-evidence]: due=2026-11-14; status=open; owner=template-maintainer; description=run a first-party project through multiple chartered epochs and reconcile this contract against the epoch records, calibration results, and deferral log

## Source anchors

Record dated stakeholder language, incidents, standards, or prior decisions.

### source[1] — 2026-09-15

> English rendering of the maintainer's original request: the current
> discipline assumes continuous human-agent collaboration. It does not cover
> self-iteration under the discipline: once the agent holds the owner's
> taste, preferences, and decision logic and is authorized around a
> high-level goal, it can keep decomposing, thinking, and iterating —
> running around the clock, or waking on a schedule to understand the
> project and evolve itself. Roles such as planner, executor, and reviewer
> are needed, but as identities and positions with different loyalties, not
> as jobs in a fixed pipeline.

Context: the maintainer's design question that opened this contract's
alignment round.

### source[2] — 2026-09-15

> English rendering of the maintainer's alignment decisions: the taste corpus
> is primary and the model derivative; the discipline itself may evolve by
> agent proposal with human ratification; role cadence is layered (executor
> continuous, planner per epoch, reviewer at milestones and high-risk
> triggers); reviewer findings block only when high-risk and otherwise
> require a written response; the charter is layered (project-level base plus
> per-objective) with mechanical expiry; the contract lands as `current`.

Context: the maintainer's answers to the seven alignment choices.

### source[3] — 2026-09-15

> English rendering of the maintainer's amendments: when nothing is
> executable, the answer is not pure stillness — re-examine the objective,
> review the project's history and its historical trade-offs, walk the
> product from the target user's position, and improve architecture and
> tests, because more perspectives expose self-consistency gaps and keep
> trade-offs re-examinable. And: a threshold left to the agent's own judgment
> gets deferred to "the next round" forever; that failure mode must be
> designed against.

Context: the maintainer's corrections to the idle-behavior and charter-expiry
choices in the same alignment round.

## Reconciliation log

- **2026-09-15 — contract created from the alignment round:** records the
  agreed positions on taste representation, discipline evolution, role
  cadence, reviewer teeth, idle reflection, layered charters with mechanical
  expiry and counted deferral, and landing as a current contract with
  behavioral evidence outstanding.
  - from: source[1] (2026-09-15 autonomy design question), source[2] (2026-09-15 alignment decisions), source[3] (2026-09-15 idle and deferral amendments)
