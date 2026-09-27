---
doc_type: contract
status: current
authority: normative
contract_role: governance
implementation: implemented
verification_status: partial
last_reconciled: 2026-09-27
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
and source[3], refined by source[6] after an actual autonomous-use failure.
Accepted interpretation: an owner can hand an agent a bounded objective, leave,
and return to a system that stayed inside its authorization, recorded what it
did, and escalated what it could not decide. It must also produce observable
progress toward the original value, with independent challenge capable of
rejecting a busy but unproductive direction.

## Scope

### In scope

- the standing charter as the vehicle of continuous authorization;
- the epoch protocol: how one unattended wake orients, acts, verifies, and
  records;
- planning and execution continuity, with a separate fresh review context;
- work selection by expected contribution and progress across multiple wakes;
- representation and calibration of owner taste;
- behavior when no authorized work is executable;
- deferral control for triggers the agent evaluates itself;
- evolution of this discipline by ratified proposal.

### Out of scope

- implementation of scheduling machinery (cron, daemons, CI triggers);
  the review dispatch and continuation behavior it must enforce is in scope;
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
| `reflecting` | Scheduled review is due, progress or quality raises doubt, or no worthwhile executable work remains | Fresh independent challenge of direction and results; bounded investigation | Findings addressed under the review rule, or a supported no-findings result | Further work depending on the questioned direction waits; unaffected authorized maintenance can continue |
| `halted` | A halt condition, a repeated deferral, or charter ambiguity | Write the owner question; read-only preservation | An owner answer or charter renewal | Never self-resumes on silence |

Invalid transitions: `dormant` to `executing` without `orienting`; `halted` to
`executing` without an owner answer; any state to `executing` after charter
expiry.

## Normative invariants

### Standing work runs under a live charter

No autonomous work begins or continues without a live charter. The base
charter names the taste corpus location, forbidden zones, resource ceilings,
sync cadence, independently dispatched review cadence, limits on unreviewed
work, and halt conditions; each objective charter names one high-level
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
recording the useful change or learning, its evidence, and what remains open.
Execution evidence identifies the artifact version, check actually run,
observed result and time, with a durable reference to the direct tool result
or artifact. A model-written success summary cannot stand in for that result;
missing execution remains unknown. After compressing or moving history, verify
that the evidence needed for current claims is still retrievable.
Keep active state concise at its existing owner; link history for investigation
rather than copying the growing run log into every wake. A claimed change
without a record needs reconstruction and verification before it is relied on.

- from: source[1] (2026-09-15 autonomy design question), source[6]

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

Planning protects the objective's meaning and compares worthwhile directions.
Execution implements the selected work and reports observed effects and
friction. Review challenges whether the work deserves confidence, including
its interpretation of the objective. Switching role names in an ongoing
context does not make that judgment independent.

The implementer owns integration and repair. A reviewer identifies consequential
problems and the evidence that supports them; supplying an implementation plan
is not a condition for a valid finding. Severity follows the effect on the
owner's outcome and trust, including product value and taste, not only technical
risk. A supported no-findings conclusion is valid; strictness never requires
inventing faults or maximizing their count.

- from: source[1], source[6]

### Direction review uses a fresh independently dispatched context

For standing autonomous work, a fresh agent that did not plan or produce the
work reviews direction and value. Separate passes in the execution context
cannot satisfy this requirement. The reviewer receives the original agreed
high-level purpose, relevant accepted preferences and trade-offs, real
boundaries, baseline and current artifacts, and access to needed evidence.
Private context follows the existing audience boundary. It receives an open
question about what matters and what is missing, with freedom to inspect beyond
the changed items, reject the selected work, and identify overlooked directions.
Do not narrow this assignment to a defect list, approved answer, or optimization
recipe. Record its first judgment before showing the executor's rationale;
then allow factual clarification without replacing the original finding.

The charter names a finite review interval, a bound on work or exposure before
review, and the dispatch mechanism and its owner. The harness checks these
before assigning more work, including when the backlog remains full. Neither
a favorable executor report nor a new task resets the deadline. Material
changes in assumptions, repeated corrections, loss of credible progress, and
project-defined signs of degraded judgment bring review forward. Unexplained
internal language may be such a signal: investigate the current assumptions
and outputs instead of only substituting words. A vocabulary or punctuation
check cannot establish sound judgment.

Before enabling unattended expansion, exercise this dispatch once: retain the
reviewer's context identity, supplied inputs, artifact version, due/observed
review time, and returned findings. Demonstrate that a due but unavailable
review cannot be cleared by the executor's own approval. Persist that state
through task changes and restarts using harness-owned scheduling or review
records outside the executor's unilateral control. A Markdown reminder alone
is not operational enforcement. If the environment cannot supply this
separation, report the limit and keep affected expansion paused, unless the
owner grants a scoped exception. Review availability cannot reduce the required
evidence. Routine authorized repair outside the questioned scope may continue.
High-risk changes retain their additional independent design requirements.

- from: source[2], source[6]

### Reviewer findings are answered and independently closed

A finding that undermines the intended value or confidence in the current work
pauses further work relying on the challenged assumption while it is resolved.
A high-risk finding also blocks its affected path under the existing risk rules.
Preserve the finding and respond with a correction, evidence-backed rebuttal,
or a precise unresolved owner decision. The implementer cannot close a
consequential finding using its own verdict, passing mechanical checks, or a
claim that the criticized convention is already familiar internally.

The reviewer or another fresh qualified context checks the response against
the finding and actual artifacts. An owner settles unresolved preference,
direction, or risk-acceptance choices. Keep contradictory evidence visible;
do not repeatedly replace reviewers until one approves. If repeated reviews
agree while real use or owner feedback keeps disagreeing, revisit their shared
brief, evidence, method, and capability before commissioning another identical
pass. Continue unaffected authorized work. Review is execution work, not a new
human approval gate for every correction. A formal `halted` state still follows
its owner-answer recovery rule.

- from: source[2], source[6]

### Work selection compares value before committing effort

Within the issuer's priorities and delegated selection criteria, use
[governance's recommendation rule](governance-decision-boundary.md#advice-preserves-disagreement)
to compare substantive candidates and explain the strongest alternative not
chosen. Work outside that envelope remains a recommendation for the owner.
Include unfinished important outcomes and plausible changes to the approach;
small, easy, well-sourced or easily counted tasks cannot define the candidate
set on their own. Enabling work is valuable when evidence connects it to a
useful result or a consequential uncertainty it will resolve.

Do not restart this comparison for every mechanical step. Retain the choice,
its decisive assumption, and the observation that would justify switching.
Reopen it when evidence changes the ranking or at the next direction review.
A mandatory repair justifies urgency by the failure it prevents or the work it
actually unblocks; the word "maintenance" is not a blanket priority.

- from: source[6]

### A sequence of wakes advances a coherent outcome

A wake's budget bounds exposure; it does not bound the ambition to an easy task
that fits one wake. Carry a worthwhile effort across wakes using a recoverable
checkpoint: the outcome and selection reason, observed baseline, completed
useful change or learning, next step and dependencies, accepted limitations,
and evidence that would change the approach. Keep this at the existing task
owner, with links to decisions and artifacts, separate from the issuer-only
charter. The executor updates this state within the delegated criteria; a state
update cannot amend authorization or reset due review. Finish coherent work before
switching to a fresh easy task unless new evidence warrants the switch.

At selection time, name what progress should become observable by the next
review and how much time or resource can be spent learning before re-evaluation.
The horizon follows the work: research may resolve a critical uncertainty
before it changes a product. Do not require a commit or feature on every wake.
Review compares the baseline and current result, remaining distance to the
purpose, resource use, and owner intervention, across the whole interval.
Checks passed, entries produced, issues closed, and self-predicted next tasks
are activity evidence; none substitutes for that comparison.

If the expected result or learning has not appeared by the agreed horizon,
record the absent evidence and obtain the fresh review before repeating the
same approach or enlarging its budget. That review can support continuation
with a revised evidence horizon inside the existing charter, a different
approach, a bounded experiment, or a stop. Finishing a batch does not reset the
missing progress. Preserve negative results and rejected approaches so later
wakes do not rediscover them. Workflow prediction is separate from predicting
owner choices; only actual owner responses calibrate the latter.

- from: source[6]

### Idle produces reflection artifacts or rest, never busywork

When no authorized executable work remains, dormancy is a legitimate epoch
outcome, not a failure. The alternative is the fresh review defined above, never
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
authority on preference, outranking derived summaries. Retain each decision's
date, context, and scope; a choice for one brief does not automatically become
a universal preference. The taste model is a hypothesis and is labeled as such
wherever used. Before each sync, record predictions of pending owner decisions
and the assumptions behind them. Compare them with actual answers and retain
corrections without rewriting the original prediction. Silence is not agreement.

Apply the [personal-context boundary](project-adoption.md#learning-and-personal-context-have-a-bounded-entry-path)
to the corpus, derived model, and prediction records. Keep them within their
permitted audience. Public charters use references that reveal no private
content or location; resolve private sources through approved private context or a persistent locator.
Public records contain only project-relevant decisions authorized for that
repository's readers.

A correction is evidence to explain. Compare what the owner said, what context
was available at the decision, what was inferred, and what the agent did. The
following examples call for different responses and may coexist:

| Supported cause | Response |
|---|---|
| An applicable, established requirement was misunderstood or ignored | Correct the affected interpretation or execution and the input, example, or guard that allowed recurrence; verify before repeating the affected decision |
| Necessary context was missing, stale, or never loaded | Repair its retrieval or handoff at the decision point and revisit dependent choices |
| The owner changed the goal or constraint | Date and reconcile the change at its owner; record whether the earlier choice fit the earlier conditions |
| An authorized exploration revealed an unexpressed preference | Preserve the alternative, reaction, and applicable scope as new evidence; update the hypothesis without inventing a prior requirement |

These are causal explanations supported by records. Calling an action an
exploration does not excuse violating known requirements or exceeding its
permission. If the cause is uncertain, retain that uncertainty and investigate.

Review correction patterns at sync alongside progress toward the objective,
observed quality, and the owner's intervention cost. If reporting an override
rate, show corrected and reviewed decision counts, decision types, and the
period; unreviewed decisions do not count as agreement. A small or changing
sample cannot establish a trend. Agreement rate alone is not a health score,
and avoiding useful authorized exploration merely to lower it defeats the
objective.

Investigate a rising rate or a corpus-model conflict at the next orientation;
do not defer this signal indefinitely. Apply known owner decisions immediately
within their scope. If unresolved interpretation or repeated failure could
cause another material error, pause those affected decisions and seek early
calibration through the charter's channel. Continue unaffected authorized work.
A local pause under this rule does not itself enter `halted`. Resume those
decisions when the cause is resolved and verified within the current charter,
or after the owner settles the outstanding decision. If a charter halt condition,
repeated deferral, or charter ambiguity triggers `halted`, the state table's
owner-answer requirement governs recovery; internal repair cannot release it.
A numeric increase alone neither changes the charter nor requires blanket
scope reduction. The owner may exclude taste-dense domains from autonomy
entirely.

- from: source[1] (2026-09-15 autonomy design question), source[2] (2026-09-15 alignment decisions), source[4] (2026-09-25 cause-based calibration), source[5] (2026-09-26 review clarifications)

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
- Scheduled direction review runs even with executable work remaining; the
  harness retains due state and cannot accept executor self-approval.
- Each multi-wake effort retains its baseline, reason for selection, strongest
  alternative, progress horizon, and recoverable next step at its existing owner.
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
- Do not count workflow prediction as owner-preference calibration, or reset a
  progress/review deadline by changing tasks, compressing logs, or restarting.
- Do not repair an out-of-charter action silently; stop, record, restore what
  is reversible, and report.

## Failure, recovery, and intervention

- Expired or missing charter: enter `dormant`; read-only diagnosis may
  continue; renewal is an owner act.
- Halt condition: enter `halted` with a written owner question that names
  options; resume only on an owner answer.
- Second consecutive deferral of a trigger: escalate at the earliest contact
  channel the base charter names; the affected scope pauses.
- Rising correction rate or corpus-model conflict: investigate under
  [preference calibration](#taste-lives-in-a-corpus-the-model-is-a-hypothesis).
  Pause affected decisions when unresolved interpretation or recurring failure
  risks another material error; continue unaffected authorized work.
- Discovered out-of-charter action: stop the affected scope, record, restore
  what is reversible, and report at the earliest channel.
- Lost or corrupt epoch records: reconstruct from artifacts; claimed work
  that cannot be verified is treated as not done.

## Acceptance evidence

Repository integration is present when:

- agent and contributor entrypoints route standing autonomous work to this
  contract;
- the work-selection and authority owners name the charter as the standing
  authorization form;
- the documentation checker and fixture suite pass with the contract in
  place.

Operational adoption additionally demonstrates independently dispatched review,
a due-review failure that prevents affected expansion, a consequential finding
resolved with fresh verification, and a multi-wake outcome or useful negative
result compared with its baseline. Records distinguish reported behavior from
observed dispatch and artifacts. A record of activity is not proof of value.
This template contains no scheduler implementation; an adopting harness must
provide and exercise these controls before claiming enforced autonomy.

The [2026-09-27 delivery review](../evidence/2026-09-27-autonomous-progress-review.md)
records the historical challenge, independent rule review, correction recheck
and structural verification for these additions. None is a multi-epoch runtime
test of the new controls.

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

Context: the accepted proposal specified owner preference evidence, human
ratification, proportionate role cadence, responses to review findings, layered
authorization, mechanical expiry, and current contract status. This English
account contains the decision scope; the original conversation is not supplied.

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

### source[4] — 2026-09-25

English account of the accepted proposal: distinguish repeated misunderstanding,
missing context, changed goals, and discovery through authorized exploration
when responding to corrections. Treat correction frequency as a signal for
investigation, not the main measure of autonomy or an automatic reason for
blanket scope reduction. The maintainer explicitly authorized implementing this
proposal. Existing charter authority, halt conditions, and deferral controls
remain in force; no live charter is amended by this template change.

### source[5] — 2026-09-26

The maintainer requested a fresh independent review with a named model. The
review identified ambiguous recovery wording between a local preference pause
and the existing `halted` state, and a missing privacy route where charter
fields invite references to personal source material. These are reading-based
findings, recorded with their limits in the [review evidence](../evidence/2026-09-26-design-and-onboarding-review.md).
The corrections clarify existing state authority and apply the adoption
contract's personal-context boundary at the point of use.

### source[6] — 2026-09-27

Public interpretation of the maintainer's authorized refinement after actual
autonomous use: challenge direction in a genuinely fresh agent context using
the agreed high-level goal and an open review assignment; identify consequential
quality failures without requiring an optimization plan; compare the chosen
work with its strongest alternative and inspect candidate coverage; preserve
meaningful progress across a long-running loop.

Context: this request authorizes the general discipline changes. Private case
records and personal preferences remain outside this public repository. The
review dispatch, progress horizons and independent closure are implementation
choices to make the requested separation effective, not measured guarantees.

## Reconciliation log

- **2026-09-27 — direction and value across autonomous wakes:** replaced the
  single-context reviewer allowance with independently dispatched fresh review;
  added candidate comparison, progress horizons and independent closure.
  Operational enforcement belongs to the adopting harness and requires observed
  evidence; multi-epoch effectiveness remains partial.
  - from: source[6]


- **2026-09-26 — independent review reconciled:** distinguished a local pause
  from formal `halted` recovery and routed corpus, model, and prediction records
  through the existing personal-context boundary. Charter fields now carry
  the permitted audience and safe source reference.
  - from: source[5]

- **2026-09-26 — corrections interpreted by cause:** replaced override-rate
  optimization and automatic blanket narrowing with evidence-based responses
  and containment of affected decisions. Reconciled recovery instructions and
  the charter template. [Evidence](../evidence/2026-09-26-design-and-onboarding-review.md)
  records review limits; multi-epoch effectiveness remains unverified.
  - from: source[4]

- **2026-09-15 — contract created from the alignment round:** records the
  agreed positions on taste representation, discipline evolution, role
  cadence, reviewer teeth, idle reflection, layered charters with mechanical
  expiry and counted deferral, and landing as a current contract with
  behavioral evidence outstanding.
  - from: source[1] (2026-09-15 autonomy design question), source[2] (2026-09-15 alignment decisions), source[3] (2026-09-15 idle and deferral amendments)
