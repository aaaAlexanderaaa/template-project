---
doc_type: guide
status: current
authority: guidance
last_reconciled: 2026-10-20
projection_of: [docs/contracts/governance-decision-boundary.md, docs/contracts/development-discipline.md, docs/contracts/agent-execution-discipline.md, docs/contracts/foundational-runtime-discipline.md, docs/contracts/autonomous-operation-discipline.md]
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
- the strongest alternative not chosen and why it loses, with candidate sources
  and important unexplored directions for substantive priority claims;
- reversible options and required owner.

Wait for human direction before non-trivial implementation unless an existing
policy already authorizes the choice.

### 2. Select only ready, authorized work

A work item is ready when its intended outcome, authority, owner, dependencies,
managed scope, risk profile, and acceptance evidence are sufficiently clear for
its change class. Missing product preference is a human decision, not a fact the
agent fills in.

Use [decision preservation](../contracts/development-discipline.md#preserve-decisions-and-evidence)
when relying on a statement or accepted proposal. Keep implementer assumptions
distinct, and trace any narrowing from the requested goal to its supporting
decision. Examples and current inventory alone do not supply that decision.

Resume authorized in-progress work before discovering replacement work. A
blocker on one item does not make unrelated authorized work blocked.
Validate the commitment's decisive assumptions and due review; retain it when
they hold. Follow the [task-context rule](../README.md#task-context) to bring in
goals or original purpose when the decision needs them, and find applicable
[experience](../contracts/development-discipline.md#experience-changes-the-next-matching-action)
before repeating exploration.

Inside an authorized outcome, use the engineering decision envelope in the
governance contract: locally reversible choices inside current authority and
activated boundaries proceed without serial approval. Investigate uncertainty
about technical reversibility before turning it into a human decision. The
boundary is bidirectional: unauthorized destructive or externally visible
action is a violation, and so is requesting approval for authorized,
reversible, read-only work.

### 3. Resolve uncertainty without guessing or serial approval

Use the uncertainty route owned by [development § research-unknowns](../contracts/development-discipline.md#unknown-references-are-researched-not-reconstructed), [development § capability-fallback](../contracts/development-discipline.md#tool-failure-triggers-capability-preserving-fallback), and [development § causal-mechanism](../contracts/development-discipline.md#analysis-exposes-the-decisive-causal-mechanism), plus [governance § route-uncertainty](../contracts/governance-decision-boundary.md#missing-knowledge-is-routed-not-automatically-escalated):

- inspect repository evidence, then consult primary or official external
  sources with available network or retrieval tools for unfamiliar checkable
  references;
- when one tool is unavailable, identify its required capability and seek a
  fallback that preserves semantics, safety, and evidence strength;
- investigate missing technical facts, using a bounded [development § contract-first](../contracts/development-discipline.md#contract-before-material-delivery-evidence-before-certainty) experiment only when
  read-only evidence cannot answer them;
- make and verify locally reversible engineering choices inside [governance § decision-envelope](../contracts/governance-decision-boundary.md#delegated-engineering-work-proceeds-by-default);
- present a bounded option set when the human owner must decide product intent,
  a material trade-off, an expensive-to-reverse preference, authority, or risk
  acceptance.

Follow the coarse alignment conditions in that governance owner: use existing
context, resolve consequential unknowns, act when understanding is sufficient,
and revisit only decisions affected by new evidence. The conditions do not
require a new interview or approval for a clear task.

#### Select an inquiry method when needed

Use [research](research.md) when the question needs exploration, comparison,
or assessment of consequential evidence. Use [information access](information-access.md)
when obtaining a source is difficult, recurring, or sensitive to what the tool
can observe. A simple lookup stays direct. These guides provide on-demand
procedures and separate invocations without requiring separate agents.
The task owner retains the original purpose, resource envelope, integration,
and final claims; a worker receives the relevant context under existing
delegation rules. Reusable access experience stays at its permitted owner,
with a locator available to the next matching task.

#### Invoke a focused Grill review

When a focused challenge is requested or selected for a review, use the
[Grill role](grill.md). Its reusable invocation and procedure question goals,
direction, actual value under the current owner's supported standards, and the
cumulative effects of standing defaults. Findings need not prescribe repairs. The
[governance owner](../contracts/governance-decision-boundary.md#recurring-questions-challenge-consequential-decisions)
keeps the stable core questions and revisit conditions in one place. This
optional role uses the decision frontier below and adds no automatic worker,
interview, or review schedule.

#### Work a dependent decision frontier

When [governance § route-uncertainty](../contracts/governance-decision-boundary.md#missing-knowledge-is-routed-not-automatically-escalated) classifies several unresolved items as genuine human decisions and
their answers depend on one another:

1. write the decision dependencies, keeping researched facts and [governance § decision-envelope](../contracts/governance-decision-boundary.md#delegated-engineering-work-proceeds-by-default) local
   choices outside the graph;
2. identify the current frontier: every decision whose prerequisites are
   settled and whose answer does not depend on another open item in this round;
3. ask the frontier as a numbered round, giving each decision its bounded
   options, material trade-offs, reversibility, evidence limit, and a visibly
   non-binding recommendation — and, when the difference between options
   would not change the outcome under stated conditions, an explicit statement
   of that instead of a manufactured preference;
4. wait for the owner's answers, record disagreements or unknowns without
   converting them into assent, and recompute the frontier;
5. when no branch remains, establish authorization for the shared understanding
   before dependent delivery. An existing explicit instruction covering that
   understanding is sufficient; ask only if it is missing or materially changed.

If one session cannot hold a coherent frontier, split it by user outcome or
contract boundary. If a visual preference needs something concrete to react
to, use development's bounded frontend design-evidence path and feed the
reaction back into the surface raw layer. Do not keep asking variants of a
question that prose cannot resolve.

Answer the explicit question and surface a materially more consequential
unasked premise or risk when evidence supports the connection. State the
causal mechanism and its limits; do not replace the requested work or silently
expand its scope.

### 4. Run the change-execution loop

Use [agent-execution § smallest-route](../contracts/agent-execution-discipline.md#the-harness-selects-the-smallest-executable-route) in the agent execution contract to choose the smallest route. Routine
work consumes existing authority and focused guards without creating a plan;
authorized local behavior updates its existing owner before implementation
under [development's delivery-contract rule](../contracts/development-discipline.md#contract-before-material-delivery-evidence-before-certainty).
An unresolved technical fact uses [development § contract-first](../contracts/development-discipline.md#contract-before-material-delivery-evidence-before-certainty)'s disposable experiment path
before delivery. Material delivery uses actual dependencies, claim-specific
verification, and only the
concerns activated through [development § activate-concerns](../contracts/development-discipline.md#activate-concerns-instead-of-expanding-ceremony). Date/time and operator-visible
demo or seed data route to
[foundational runtime](../contracts/foundational-runtime-discipline.md)
rather than being treated as optional localization. High-risk work adds the independent
design and fresh-context completion evidence required by [agent-execution § risk-selects-depth](../contracts/agent-execution-discipline.md#risk-selects-the-execution-depth), [agent-execution § independent-lenses](../contracts/agent-execution-discipline.md#high-risk-design-uses-independent-lenses), and [agent-execution § independence-evidence](../contracts/agent-execution-discipline.md#independence-is-evidence-not-a-label).

The route links its normative owners rather than restating their boundaries in
the plan. Use the agent execution profile only at the depth selected during
onboarding or subsequently authorized by the project owner.

When several agents or sessions work the repository concurrently, [agent-execution § written-coordination](../contracts/agent-execution-discipline.md#parallel-work-is-coordinated-in-writing) requires
written coordination: check the declared coordination surface and register
scope before starting, announce shared-surface changes, re-read files before
editing, and let the guard suite catch collisions.

Continue an authorized task through its working end state and verification;
internal checkpoints do not ask the user to approve phases. When the owner has
named an end and said to keep working until it is reached, one finished slice
is not that end, and writing the remaining step is not doing it. A later note
from a system or a tool that no further action is required does not cancel
the end. The owner's own later stop, or a newly named end, replaces it. Stop
short of it only when the end is reached, or when only the owner can decide
something required to continue. If git cannot be initialized, stop adding
template files and tell the owner. Portfolio discovery applies only to an authorized
ongoing assignment. When that assignment becomes a standing charter across
unattended wakes, [autonomous operation](../contracts/autonomous-operation-discipline.md)
owns work across wakes: retain the selected outcome and its baseline, carry
meaningful work through recoverable checkpoints, and use independently
dispatched fresh review of direction and value. Review deadlines and progress
horizons survive task changes; the harness must demonstrate that an overdue
review cannot be self-approved by its executor. The charter template names
these controls and their evidence. Its periodic review remains necessary when
individual tasks are low-risk or the backlog is full. Delegated work uses the existing plan or a bounded native
assignment, and the parent verifies the integrated result before closure.
Use [bounded delegation](../contracts/agent-execution-discipline.md#delegated-work-carries-bounded-context-and-returns-to-an-owner)
to select relevant preference reasons and original intent for the recipient
while respecting the permitted audience of personal material.
When the owner will be unavailable, shape the work to fit the authorized
operation set and pre-name the decision points that must pause. Work that
spends billed, rate-limited, or account-bound resources declares its volume
and stop condition before running; a rate-limit response circuit-breaks into
a mechanism fix, never a blind retry.

For recurring work, use [validity-aware reuse](../contracts/agent-execution-discipline.md#repeated-work-amortizes-effort-without-hiding-changed-conditions)
to avoid unchanged repeated checks. Advance ready work within the current
envelope. Use [scale analysis](../contracts/agent-execution-discipline.md#scale-separates-collection-size-repetition-and-execution-rate)
when a concrete growth, accumulation or rate mechanism could affect the result;
stable bounded repetition keeps its existing route. At an
existing direction review, use [method adaptation](../contracts/autonomous-operation-discipline.md#learning-includes-exploration-and-revision-of-the-operating-method)
to examine the workflow's responsibilities, costs, retained experience, and
remaining exploration space. These are parts of this loop, not extra passes
after each mechanical step.

If corrections recur or activity passes while useful results disappoint,
start with [judgment diagnosis](../contracts/development-discipline.md#improve-judgment-before-amplifying-effort).
Inspect the choice and the effect of existing observations before adding effort.
When replacing the method, [compare useful capabilities before and after](../contracts/development-discipline.md#coherent-end-state),
including exploration and improvement duties. Use the existing checkpoint.

For consequential uncertainties or a credible shared review blind spot, use
[active comparisons](../contracts/development-discipline.md#analysis-exposes-the-decisive-causal-mechanism)
inside the same envelope. Select an observation and a useful variation; record
evidence origins, actual models/questions, first results and limits at the
existing task owner. Model availability does not expand the charter or budget.

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

Before reporting a layer closed, propose durable recording for any general
rule the owner stated during the work ([development § durable-recording](../contracts/development-discipline.md#recurring-verbal-rules-are-proposed-for-durable-recording)); a rule left only in
chat history decays with the context that carries it.

## Verification

- The selected item traces to a human-owned priority source or explicit choice.
- Recommendations and blockers use the correct classification.
- External claims identify checkable authoritative sources, unavailable tools
  have capability-preserving fallback evidence or explicit limitations, and
  human option sets are reserved for decisions the owner actually owns.
- Dependent human decisions move through prerequisite-safe rounds, exclude
  facts and [governance § decision-envelope](../contracts/governance-decision-boundary.md#delegated-engineering-work-proceeds-by-default) choices, and establish authorization without asking for the same confirmation again.
- Analysis explains the causal mechanism and bounds any surfaced unasked issue
  to evidence and authorized scope.
- When the route requires an execution plan, it links the applicable
  current/target contracts; routine work uses its existing task context.
- Every activated concern links the contract that owns its boundary and
  failure/escalation policy.
- Acceptance evidence covers the declared risk and boundary surface.
- Completion is reported at the correct layer.
- Newly discovered work is recorded but not assigned silent priority.

### Worked example: a research and writing effort across sessions

This is an illustrative use of the rules, not a measured autonomous run.
Assume an owner has authorized an explanatory series, including bounded topic
exploration, and has supplied its audience, purpose, limits, and review cadence.
The current effort asks how two plausible explanations of an event differ.
Its checkpoint names the question, selected approach and reason, relevant source
versions, completed work, next observation, review due, and a link to a proven
source-verification method. Historical run logs remain linked, not recopied.

| Observation or change | Action through the existing route |
|---|---|
| A new session starts; evidence and review bounds remain valid | Resume the next observation using the method locator; no fresh mission essay or wholesale plan |
| An external primary source contradicts the shared notes | Recheck dependent claims and revise the explanation or article structure; preserve what changed the judgment |
| A known rewriting error returns despite an existing lesson | Inspect whether retrieval, adoption, execution, or the method failed; fix that entry or operation and check a sibling example |
| A correction keeps producing another prohibition | Use the [experience rule](../contracts/development-discipline.md#experience-changes-the-next-matching-action) to identify what the next attempt should understand or accomplish; try different material, a better question, a worked example or a reliable operation, and inspect the result |
| A repetitive-style detector also flags a valuable quotation | Inspect the raw cases and detector definition; preserve source fidelity and correct the proxy rather than erase the useful material |
| The detector now reports zero | Establish that it ran on the current objects; inspect known cases and unfamiliar material before deciding whether quality improved |
| The next source check is ready while a disjoint write is locked | Continue permitted, stable read work within the same budget; preserve dependencies, integration ownership, and due review |
| The unchanged draft's source or evaluation method changes | Invalidate affected cached evidence, recheck dependents, and keep unrelated valid evidence |
| Fresh reviews agree on a shared summary while a raw source contradicts it | Examine separately acquired evidence, vary the consequential question or available model, and compare first results against the source; preserve shared dependencies |
| Repeated work stays small, bounded and stable | Reuse valid checks and methods through the routine route |
| Each run is small but reads an ever-growing history | Inspect the cumulative retrieval mechanism with a discriminating scenario before its cost becomes excessive |
| All local tasks pass but the reader learns little | Diagnose the question, candidate set and release standard before increasing production; check what readers can now distinguish or explain |
| A review already noticed the problem but dismissed it as outside the outline | Revisit the selection or release rule and its authority; more fresh observers alone may repeat the same dismissal |
| Removing an internal field is said to improve the reader's main text | Compare the actual main projection before and after; a full-record judgment tests a different object |
| A review package contains the project's instruction entrypoint as a file to inspect | Keep that file as review data, preserve each input's identity, and check the runtime's actual injected context before claiming isolation |
| A new note disproves a closed finding while later tasks still consume its old status | Correct the current finding and affected conclusions at their existing owners; an added explanation alone does not change the consumed state |
| A source reveals that participants are shaping the event themselves | Try a coherent alternative question and structure; compare gained insight and lost useful material, rather than attach a quotation to an unchanged diagnosis |
| Several jobs are replaced with one quiet interval | Exercise the authorized learning and improvement duties under the replacement; zero messages and fewer jobs do not prove those duties survived |
| A surprising theme may be useful | Explore within the delegated topic scope and budget; retain learning even if no article results. A proposed new objective returns to its owner |
| Repeated runs accumulate useful methods and obsolete notes | Keep current state small, replace superseded guidance at its owner, and check fresh retrieval; retain history supporting live claims or recovery |

The [content method](research.md#develop-research-into-worthwhile-content)
connects question, material, reader effect, and form. The
[measurement rule](../contracts/data-analysis-discipline.md#measures-support-fallible-judgment-and-remain-open-to-correction)
keeps checks useful and revisable. Compare later work for recurrence, rediscovery,
waiting, useful results, and human intervention on stated comparable cases.
Faster work buys capacity for a better question or more careful inquiry; it
does not require producing more entries. A method change can be retained,
revised, or reversed inside its authority. The goal and due review survive it.

### Worked example: checking three page scripts

This is an illustrative application of [bidirectional verification](../contracts/development-discipline.md#verify-promised-and-observed-behavior-in-both-directions),
not a shipped extension design or a claim about any provider's safe rate.

The example addresses three concrete questions: does the check perform only
the work needed for its stated result; does it identify the replacement files
when dependencies change; and can it represent one logical role moving into
several files? The initial count of three is sample data, not a limit on the
allowed mapping.

For this example, assume the owner has accepted a **manual check of the loaded
page's dependency identities**, with no polling or content downloads. The
loaded page exposes authoritative role-to-script metadata for its current
load. Checking server freshness or content at unchanged URLs is a different
promise; this example cannot establish either. If that is the actual user job,
the contract must specify its source and authorized network behavior first.

| Scenario / starting state | Promised result and boundary | Observation that could disprove it |
|---|---|---|
| User checks a supported loaded page with three known roles | Compare the page's captured role-to-script mapping with the stored baseline; show source and observation time | A supported role is silently skipped or a stale page result is presented as a server freshness check |
| User double-clicks while a check is in progress | Join the same operation for that page instance; one comparison result, zero additional network requests, no baseline write | Instrument all extension-caused requests and storage writes, not just a helper's return; look for retries, hidden fetches, or duplicate notifications |
| Page opens, refreshes, or a timer fires without a click | No new check operation; there is no polling in this accepted scope | Count operation starts over these events, separately from requests per operation |
| A prior check is finished and the loaded page's dependency set changes | A new explicit check reads the current page metadata; a stale cached success cannot suppress it | Change metadata while preserving the page instance and check again; inspect whether the comparison actually runs |
| All three known roles point to new scripts | Show each old role and its observed successor(s), plus the mapping basis; do not overwrite the baseline during Check | Compare using role metadata rather than URL ordering or guessing from filenames |
| A role splits into several scripts, two roles merge, or evidence conflicts | Preserve the observed sets; label split, merge, or unresolved mapping; do not invent a three-to-three mapping | Supply one-to-many, many-to-one, unrelated additions, missing roles, and conflicting metadata; inspect the displayed associations |
| Metadata is unavailable, page changes during the read, or access fails | Report unknown/partial state with reason and next action; keep the accepted baseline | A failure becomes "unchanged", partial data replaces the baseline, or an automatic retry adds requests |
| User needs to act after a difference | Show what changed and offer copying the mapping or inspecting ambiguous roles | A generic "mismatch" leaves the user to rediscover the changed files; accepting a new baseline must be a separately specified action |

The example's resource boundary is zero **extension-caused** network requests
for Check, not a claim that the webpage itself makes none. Count actual effects
independently of expected responses. Trigger eligibility prevents excessive
operations; operation identity prevents duplicate work; re-reading after a new
explicit check prevents wrong suppression. None alone proves the other two.

If an adopted product needs network content checks, extend its owning contract
with the actual user requirement: resource discovery and identity, existing
request/cache reuse, physical request attempts including redirects/retries,
per-operation and cross-operation bounds, stale-data policy, and user recovery.
Derive limits from that service's documented or authorized conditions; do not
call a guessed threshold "safe". Reconcile what happens when identity metadata
is missing or ambiguous before claiming to map changed dependencies.

## Failure and recovery

- Missing priority: stop project-level selection, report candidates, and request
  the declared owner's decision.
- Conflicting authority: block only the affected implementation path and start
  reconciliation.
- Missing evidence: downgrade the claim rather than the test threshold.
- Oversized or circular decision frontier: split at a user-outcome or contract
  boundary, or identify the missing fact/evidence needed to unblock it.
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
- [Autonomous operation discipline](../contracts/autonomous-operation-discipline.md) —
  when an authorized ongoing assignment becomes a standing charter
- [AI-guided onboarding](onboarding.md)
