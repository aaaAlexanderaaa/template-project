---
doc_type: contract
status: current
authority: normative
contract_role: governance
implementation: implemented
verification_status: partial
last_reconciled: 2026-09-27
review_due: 2026-10-24
supersedes: []
---

# Governance decision boundary

## Purpose

This contract defines the boundary between developer or product authority and
the repository's governance framework. Governance improves the quality and
truthfulness of decisions; it does not replace the person who owns product
direction, priority, or risk appetite.

## Scope

In scope:

- governance findings, recommendations, human decisions, and execution gates;
- project priority and portfolio integration;
- agent behavior when priority or authority is missing;
- explicit exceptions and residual-risk ownership.

Out of scope:

- choosing a product vision, roadmap, commercial priority, or user value;
- scoring one universal portfolio model;
- preventing an authorized owner from changing a contract or accepting risk;
- replacing legal, security, safety, or domain-specific authority.

## Vocabulary

- **Direction authority:** the human owner authorized to decide product intent,
  priority, trade-offs, and risk acceptance.
- **Governance framework:** contracts, guides, checks, and agents that expose
  facts, risks, conflicts, and evidence quality.
- **Execution blocker:** a bounded condition that prevents one implementation
  path from proceeding truthfully or safely; it is not a rejection of product
  intent.
- **Governance exception:** a dated, scoped human decision accepting a named
  deviation and its residual risk.
- **Engineering decision envelope:** reversible implementation choices an agent
  or contributor may make inside authorized product intent, public contracts,
  permission boundaries, durable-state rules, and any declared risk budget.

## Ownership and boundary

| Concern | Authoritative owner | Governance may | Governance must not |
|---|---|---|---|
| Product direction and user value | Developer/product owner | surface evidence and alternatives | substitute its own preference |
| Portfolio priority | Declared portfolio owner | consume priority and expose dependencies | invent or silently reorder priority |
| Reversible implementation mechanics | Implementer inside the engineering decision envelope | choose, implement, test, and revise without per-choice approval | change product meaning, public promises, privileged behavior, irreversible state, or accepted risk |
| Technical and lifecycle truth | Declared system/contract owner | detect contradictions and missing evidence | rewrite current truth to fit a proposal |
| Risk acceptance | Authorized human owner | explain impact and record disposition | treat an unaccepted risk as accepted |
| Mechanical integrity | Checker/test owner | fail on stable declared invariants | claim semantic judgment from syntax alone |

- from: source[1], source[2]

## States and triggers

Every material governance observation is expressed as one of these states:

| State | Meaning | Trigger | Required next action |
|---|---|---|---|
| `fact` | Reproducible current observation | Read-only evidence exists | Preserve source and scope |
| `risk` | Plausible adverse outcome or long-term abnormality | Fact plus causal mechanism exists | Record impact and its rough magnitude, likelihood limits, the conditions under which it does not matter, and options |
| `recommendation` | Non-binding preferred response | Trade-offs can be compared | Direction authority accepts, rejects, or defers |
| `human_decision_required` | No authorized choice exists | Options materially change intent, priority, or risk | Obtain and record the owner's choice |
| `execution_blocker` | One path cannot proceed truthfully or safely | A blocker class below is proven | Resolve, change path, or record an allowed exception |

The state must be explicit. A recommendation cannot be worded or enforced as a
blocker merely because the framework strongly prefers it.

- from: source[1], source[2], source[3]

## Normative invariants

### Humans own direction and priority

The framework consumes a declared priority source. It may identify missing
outcomes, dependency conflicts, aging work, concentrated risk, or likely
long-term maintenance cost, but those findings remain inputs to the authorized
owner's decision.

When no priority authority exists, an agent presents candidate work and its
evidence as recommendations and requests a decision. It does not convert its
own ranking into project authority.

- from: source[1], source[2]

### Blockers are narrow and evidence-backed

An `execution_blocker` is allowed only for:

- unresolved conflict between applicable current authorities;
- missing authorization for destructive, irreversible, privileged, or
  materially expansive action;
- a mechanically invalid configuration or unavailable required dependency;
- missing contract, evidence, or independent review that an already adopted
  risk profile explicitly requires;
- an implementation path that cannot satisfy the declared coherent end state.

A blocker rejects or pauses the path, not the product idea. The response must
name the evidence, the exact scope blocked, at least one recovery option, and
the human decision available where applicable.

- from: source[2], source[3]

### Advice preserves disagreement

Recommendations state their evidence, assumptions, expected benefit, cost,
alternatives, and limitations. For a substantive claim that some next work is
most valuable, show the real candidates considered, the strongest feasible
alternative not chosen, and why
it loses under the current purpose and constraints. Explain where the candidates
came from and which plausible direction remains unexamined. Compare expected
user value, reduction of a binding constraint or important uncertainty, reuse
where relevant, whole-life cost, and cost of delay. Use evidence and reasons
rather than a total score that hides decisive differences. Exploration stops
when further search is unlikely to change the immediate choice or an authorized
reversible step can answer the uncertainty more cheaply; retain that limit.
Do not invent a weak second option or a claim of exhaustive coverage. A direct
local fix needs no portfolio comparison.

State this reasoning with the recommendation; in unattended work retain it for
the next review or owner sync and revisit it when facts change. This comparison
does not create a new approval gate or override the issuer's priorities.

A rejected recommendation remains evidence or history; it does not silently
return as a mandatory rule. Agreement is held
to the same standard: a recommendation or plan is endorsed because its
evidence was checked, not because agreeing is smoother — instant agreement
without independent judgment is a failure mode, not alignment.

A problem report is incomplete when it stops at "something is wrong". A risk
or recommendation that asks for attention also states: who bears the impact
(the user, the operator, the product, or the engineering organization); the
impact's rough magnitude — a range, or an explicit unknown with its cost of
finding out, is acceptable; the conditions under which the problem does not
matter; and what accepting the risk would assume. An option presented for
decision carries the same fields plus its reversibility or switching cost.

- from: source[2], source[7], source[10], source[12]

### Exceptions are explicit, scoped, and reviewable

An authorized owner may accept a governance exception when the governing rule
permits human waiver. The record names the rule, scope, reason, date, owner,
residual risk, expiry or review trigger, and recovery path. An exception cannot
manufacture missing product authority or silently waive legal or safety
authority owned elsewhere.

- from: source[1], source[3]

### Work selection consumes authority

An agent may resume already authorized in-progress work, follow a declared
priority order, and perform read-only portfolio diagnosis. When it discovers
untracked work, it records the candidate and evidence before non-trivial
implementation, but the portfolio owner decides its priority unless an
existing policy already determines it. A standing charter under
[autonomous operation](autonomous-operation-discipline.md) is one form of
declared authorization for unattended execution: it pre-authorizes a bounded
operation set and pre-names the decision points that must pause. It never
transfers direction, priority, or risk acceptance.

- from: source[1] (2026-07-26 no framework-defined priority), source[2] (2026-07-26 advisory-not-blocking boundary)

### Delegated engineering work proceeds by default

Within an authorized outcome and managed scope, an agent or contributor may
make a local engineering choice without requesting approval when the choice is
reversible at reasonable cost and does not change product meaning, a public
contract, authorization or capability, irreversible or durable-state
semantics, an activated quality-attribute boundary, or another owner's private
rule. Normal naming, decomposition, test organization, and equivalent internal
implementation choices belong to this envelope.

An explicit request for new behavior can authorize updating its normative
owner and delivering that behavior under [development's delivery-contract rule](development-discipline.md#contract-before-material-delivery-evidence-before-certainty).
That authorization is separate from discretion over implementation mechanics.
[Execution risk](agent-execution-discipline.md#risk-selects-the-execution-depth)
selects records and reviews after authority is established; a routine label
never grants permission to invent product behavior or relax a boundary.

When no risk budget is declared, the default envelope permits a choice that is
inside current authority, managed scope, and every activated boundary, is
locally reversible, and creates no uncontracted durable-state or external
effect. Uncertainty about technical reversibility is investigated as a
technical fact. A human decision is needed when the evidence instead exposes
unknown product intent, missing authority, or risk acceptance, not merely
because investigation was initially required.

The implementer records an assumption when it materially affects verification
or a later decision; it does not turn every ordinary choice into a decision
request. A preference difference inside the envelope is review feedback, not a
governance blocker.

Authorization covers the agreed outcome through implementation, integration,
verification, and necessary corrections. Internal plans, test failures that
can be fixed within scope, and dependency checkpoints do not create new human
approval gates. Give progress updates and continue. Required independent
reviews remain execution work; they are not requests for the user to approve
each phase.

If new evidence exposes a material change of intent, authority, accepted risk,
or a bounded execution blocker, pause the affected path, explain what changed,
and present a concrete decision with its available evidence. Continue unaffected
authorized work. Do not infer authority for a new task after this one is done.

The boundary runs in both directions. Destructive, irreversible, or externally
visible action without explicit authorization is a violation — and so is
returning authorized, reversible, or read-only work for approval. Both spend
what the boundary exists to protect.

- from: source[4], source[8], source[9], source[10]

### Missing knowledge is routed, not automatically escalated

Route uncertainty by what resolves it and by the cost of being wrong:

- an unfamiliar, externally checkable fact or reference uses [development § research-unknowns](development-discipline.md#unknown-references-are-researched-not-reconstructed)'s
  authoritative-source research rather than guessing;
- an unavailable tool uses [development § capability-fallback](development-discipline.md#tool-failure-triggers-capability-preserving-fallback)'s capability-preserving fallback
  before the task is described as blocked;
- a missing technical fact first produces bounded read-only investigation and,
  when necessary, the controlled experiment defined by [development § contract-first](development-discipline.md#contract-before-material-delivery-evidence-before-certainty);
- a locally reversible implementation choice inside the decision-envelope invariant is made and verified by
  the implementer rather than returned for serial approval;
- unknown product intent, a material design or decision trade-off, authority,
  expensive-to-reverse preference, or risk acceptance produces
  `human_decision_required`.

A required human decision is presented as a bounded option set when genuine
alternatives exist. Each option names the outcome, material trade-offs,
reversibility or switching cost, and the evidence limitation; a recommendation
may be included but must remain visibly non-binding. When the difference
between the options would not change the outcome under stated conditions, the
option set says so instead of manufacturing a preference. Do not manufacture a
multiple-choice question when the repository already contains the answer, when
investigation can establish a fact, or when only one path satisfies current
authority.

When several human-owned decisions depend on one another, map those
dependencies and work the current **decision frontier**: ask only decisions
whose prerequisites are settled, and do not place two questions in the same
round when one answer could change the other. Recompute the frontier after each
round. An empty frontier is not delivery authorization by itself. Establish the
owner's authorization for the shared understanding before landing the resulting
material contract or beginning dependent delivery. An existing explicit
instruction that covers that understanding is sufficient; ask only when that
authority is missing or the understanding materially changed.

The frontier is a sequencing method, not a reason to interrogate every local
choice. Researchable facts, controlled technical learning, and choices inside
the decision-envelope invariant stay on their existing routes. If the decision scope cannot remain coherent
in one session, split it by user outcome or contract boundary rather than
substituting an arbitrary question limit for unresolved branches.

Use a coarse alignment state to decide what is needed next. These are
conditions of understanding, not mandatory meetings, recorded status fields,
or a sequence every task must traverse:

| Current understanding | Next action | Ready to proceed when |
|---|---|---|
| The intended result is unclear | Read the request and relevant context; establish who benefits, in what situation, and what should change | There is a supported interpretation of the purpose |
| An unknown could change the choice | Investigate checkable facts; bring only human-owned choices to the owner with a recommendation, alternatives, and consequences | The decisive information is known or can be learned within an authorized reversible step |
| Purpose and boundaries are sufficient | Capture a proportionate brief in the existing task or behavior owner and proceed under current authorization | The next action has a meaningful result and evidence path |
| Feedback changes an assumption | Reopen the affected interpretation or choice and continue unaffected work | The changed assumption has been reconciled |

For an open-ended task, a useful brief identifies the problem and intended
value, current state and available evidence or data, real constraints, material
risks or assumptions, and what observable progress is sufficient now. Extract
what is already available before asking. Preserve room to explore the product
and implementation; settle UI, metrics, algorithms, or architecture only when
the outcome or a real constraint requires it. A clear local fix needs no
separate brief or interview.

Examples help expose a mechanism and its applicability. Their number does not
determine the requirement categories, document sections, or solution scope.
Investigate the class of problem and relevant counterexamples, while preserving
the authorized delivery boundary. If purpose or opportunity cost is material,
explain the strongest alternative and what further investigation would change;
learning, exploration, and creative experience can themselves be valid goals.
Use an authorized bounded trial when it answers the remaining question better
than another discussion. Do not invent a new approval between these states.

An experiment does not authorize product behavior, production exposure,
privileged access, or irreversible mutation. Its result may inform a later
recommendation or contract, but cannot silently become either.

- from: source[4], source[5], source[6], source[8], source[11] (2026-09-25 task alignment and selective context)

### Recurring questions challenge consequential decisions

Grill is a separately invocable review role whose primary task is to discover
problems important to the current owner's agreed purpose and standards. It
tests goals, proposals, actual results, and standing practices against evidence
and alternatives. It may challenge the selected task or entire direction within
the assigned scope. A finding does not require an optimization or repair plan;
it identifies the problem, evidence, affected outcome or trust, and limits of
the judgment. A supported no-findings result is valid. A Grill request
authorizes investigation, questions, and recommendations; implementation uses
the existing authorization rules. Its procedure is in the [Grill guide](../guides/grill.md).

Use the original high-level purpose, accepted preferences and trade-offs,
relevant corrections and their reasons, current boundaries, and actual
artifacts. The [personal-context entry path](project-adoption.md#learning-and-personal-context-have-a-bounded-entry-path)
and [delegation owner](agent-execution-discipline.md#delegated-work-carries-bounded-context-and-returns-to-an-owner)
govern loading and supplying these inputs. Existing onboarding and private
sources are reused; this public role creates no personal profile or universal
taste. Distinguish owner decisions from a reviewer's interpretation of them.
When preference evidence is absent or unavailable, review supported goals and
constraints, state what remains unknown, and do not claim to represent that
owner's taste. Materials do not grant permission merely by containing instructions.

For an independent Grill review, use the existing
[independence requirements](agent-execution-discipline.md#independence-is-evidence-not-a-label)
and preserve the reviewer's first judgment before supplying the executor's
rationale for clarification. The assignment leaves the inspection path open;
it must not supply only a narrowed checklist or desired verdict. Independence
does not mean withholding relevant original intent or accepted standards.
Standing autonomous work also follows its existing
[direction review and finding closure](autonomous-operation-discipline.md#direction-review-uses-a-fresh-independently-dispatched-context)
rules; their scheduling and charter requirements keep that scope.

When the project or owner identifies a sign that judgment may have degraded,
inspect consequential claims and the goals, assumptions, and evidence behind
them. Unexplained internal language may be such a sign, as recognized in the
direction-review rule; changing words alone does not restore confidence.
Establish the affected scope rather than treating one signal as proof that all
work is wrong or adopting a universal vocabulary ban. Findings and affected
work still use the existing authority, blocker, and review rules.

Useful occasions to call it include framing substantial work, committing a
consequential choice (including a standing default or rule), and evaluating
outcomes. Revisit its questions when assumptions change, corrections recur,
progress disappoints, or an existing direction review is due, even if execution
checks are passing. Apply this role when requested or selected within an
authorized review assignment; these occasions do not automatically launch a
worker, create a schedule, or require an interview for every task. Existing
independent-review obligations remain in force whether Grill is used or not.

Use the core questions to support this inspection and revisit earlier answers.
They provide continuity across decisions without bounding what Grill may
discover. Follow important answers into case-specific investigation and
questions; a completed list alone establishes neither value nor sound judgment.

| Core question | What the answer must make visible |
|---|---|
| What useful change are we trying to produce, for whom, and why does it matter now? | The original purpose, an observable outcome, and the reason this work deserves attention rather than merely producing an artifact |
| What do we know, what are we assuming, and what would change our mind? | Observations and their sources, consequential unknowns, and evidence that could disprove the leading explanation |
| What mechanism creates the problem, and where should we intervene? | Whether the proposal changes an action or its frequency, information, a standing rule, authority, or the goal; why that intervention addresses the cause |
| What is the strongest feasible alternative, including leaving things unchanged? | A real comparison under current constraints, the binding trade-off, and conditions under which the choice would not matter |
| Who benefits, who bears the cost, and what else changes if this keeps happening? | Immediate and cumulative effects, affected people and future tasks, displaced work, induced behavior, and relevant feedback or observation delays |
| Where does this answer stop applying, and who may decide the change? | Scope, counterexamples, existing authorization, other owners' boundaries, and any genuinely unresolved human decision |
| How will we learn whether it worked, and when should we change or stop it? | A relevant baseline, observable benefit and harm, a review occasion or evidence horizon, and a correction, withdrawal, or recovery owner |

First use the request and available evidence to answer. Show the consequential
gap or disagreement with its basis; then investigate checkable facts, make
authorized local choices, and bring human-owned decisions to the owner through
the [uncertainty route](#missing-knowledge-is-routed-not-automatically-escalated).
Human questions follow its decision frontier and carry context, genuine
options where useful, and trade-offs. A supported answer is valid; do not
manufacture disagreement. A clear routine task can reuse established answers
and proceed without an interview or a separate question record.

For changes to defaults, agent entrypoints, templates, or enforcement, trace
the expected behavior across future uses before changing the owning rule.
Compare a standing change with a local correction, a conditional trigger, or
better information where these are credible alternatives. Examine both the
failure the change should prevent and a normal case where applying it could
add cost or suppress useful work. Account for repetition and delayed effects;
reverting a file does not recover spent resources or undo completed actions.
Use the existing [risk assessment](agent-execution-discipline.md#risk-selects-the-execution-depth)
and [verification](development-discipline.md#verify-promised-and-observed-behavior-in-both-directions)
owners to select proportionate evidence, and retain unknown effects as unknown.
Questioning a rule neither authorizes changing it nor makes it immutable.

Keep decision-changing answers, unresolved assumptions, and the reason to
revisit them in the existing brief, contract, plan, or evidence. At a revisit,
compare the earlier answer with current observations and explain what held or
changed. Reuse settled authority rather than asking for the same approval;
reopen an answer when evidence, a counterexample, or a consequential omission
challenges its applicability. End a round with a supported next action, a
bounded investigation, a human decision, or a justified stop. Continue
unaffected authorized work. Question counts and completed forms are activity,
not proof of better decisions.

- from: source[13] (2026-09-27 recurring Grill questions), source[14] (2026-09-27 owner standards and independent judgment)

## Required behaviors

- Every governance-facing report distinguishes facts, risks, recommendations,
  required human decisions, and execution blockers.
- A priority source is named before autonomous project-level work selection.
- Missing priority produces a decision request, not agent-authored direction.
- Choices inside the engineering decision envelope proceed without serial human
  approval; material assumptions remain visible in the plan or evidence.
- Missing knowledge follows the route-uncertainty invariant: research checkable references, seek a
  capability-preserving tool fallback, investigate technical facts, make
  reversible local choices, and present bounded options only for decisions
  that belong to the human owner.
- Dependent human decisions use the route-uncertainty invariant's decision
  frontier and establish authorization for the shared understanding without
  moving facts or local engineering choices into an interview, or asking for
  the same confirmation again.
- A blocker includes scope, evidence, recovery, and available human authority.
- A risk or problem report names who bears the impact, its rough magnitude,
  the conditions under which it does not matter, and what accepting it would
  assume.
- Accepted deviations use a durable governance-exception record.
- A Grill assignment inspects outcomes against the current owner's supported
  purpose and standards, using the recurring questions above. Later sessions
  compare important earlier answers with observed outcomes and side effects.

## Forbidden behaviors

- Do not describe a developer's authorized idea as wrong merely because a
  different trade-off is preferred.
- Do not turn risk scoring into product priority without delegated authority.
- Do not use contract-first discipline to freeze contracts against authorized
  requirement changes.
- Do not present an advisory finding as mechanically enforced.
- Do not treat silence as risk acceptance or priority approval.
- Do not turn reversible implementation discretion or a resolvable technical
  unknown into a product-direction question.

## Failure, recovery, and intervention

If the framework overreaches, reclassify the output, preserve the original
record, and return the decision to the declared owner. If the owner is unknown,
pause only the affected decision and continue safe, already authorized work.
If a blocker is disputed, reproduce its evidence and reconcile the governing
contract before dependent implementation.

## Acceptance evidence

- The [2026-09-27 Grill delivery review](../evidence/2026-09-27-grill-review.md)
  records a fresh consumer applying the separately invocable role to unseen
  proposal/default scenarios, its invocation and authority checks, and passing
  repository checks for the initial delivery. It separately records the
  goal-and-standards revision's passing repository checks and incomplete fresh
  consumer verification after reviewer access failures. The initial results
  do not establish the revised judgments or sustained decision-quality
  improvement; behavioral verification remains partial.
- Contributor and agent entrypoints state the authority boundary.
- Project-operation guidance consumes rather than creates portfolio priority.
- The agent work-selection rule distinguishes discovery from authorization.
- The contributor and agent entrypoints state the positive engineering decision
  envelope and controlled-learning route.
- Onboarding asks the adopting owner to declare governance scope and priority
  authority.
- Documentation checks and fixture tests remain green after the new reusable
  onboarding record is registered.

Verified on 2026-07-26:

- contributor, agent, onboarding, project-operation, and assessment entrypoints
  use the five output classes and preserve human priority authority;
- `python3 -m unittest discover -s tests -p 'test_*.py'` passed the full fixture
  suite;
- `python3 scripts/check_docs.py --today 2026-07-26` passed. The checker's
  summary line reports the current document and template inventory; restating a
  count here would only go stale.

Verification remains `partial`: the repository proves structural reachability
and terminology alignment, not how an independent real project applies the
decision boundary under delivery pressure.

Verified on 2026-07-28:

- `AGENTS.md`, `CONTRIBUTING.md`, and project-operation guidance expose the
  positive decision envelope and controlled-learning route;
- the Python 3.11 fixture suite and both repository checker modes pass; the
  final high-risk holistic evaluation remains a separate objective-level gate.

Verified on 2026-08-06:

- [development § research-unknowns](development-discipline.md#unknown-references-are-researched-not-reconstructed), [development § capability-fallback](development-discipline.md#tool-failure-triggers-capability-preserving-fallback), [development § causal-mechanism](development-discipline.md#analysis-exposes-the-decisive-causal-mechanism), and the route-uncertainty invariant have one explicit uncertainty route across the agent,
  contributor, README, and current operating-guide projections;
- dependency-aware human decisions have one normative trigger in the route-uncertainty invariant; the
  operating guide may explain frontier sequencing but cannot broaden the set
  of decisions returned to the owner;
- the fixed-date documentation fixtures were reconciled with the new canonical
  dates, and all 106 tests pass under Python 3.11;
- `python scripts/check_docs.py --strict` passes with no findings.

Maintainer-reported adoption on 2026-09-14:

- the maintainer reports that projects applying this boundary since 2026-07
  found bounded options with trade-off context useful and motivated the
  bidirectional-boundary and genuine-agreement clarifications. These are
  reported outcomes, not independently reproduced observations.
  Report and limits: [2026-09-14 first-party adoption feedback](../evidence/2026-09-14-first-party-adoption-feedback.md);
- the partial note above still holds for adopters independent of the
  maintainer.

## Source anchors

### source[1] — 2026-07-26

> “As a governance framework, it should not help developers define priority.
> It may only assist; it does not make the decision.”

### source[2] — 2026-07-26

> “It may help developers see risks they have not identified and abnormalities
> that matter for long-term project health. It must not, when the developer
> already has an idea, block them by saying that idea is wrong.”

### source[3] — 2026-07-26

> “Agreed” to adopt bounded governance authority, AI-guided onboarding, and
> staged tightening for brownfield projects.

### source[4] — 2026-07-28

> “Enable rather than obstruct. An agent should know clearly what it should
> and should not do, instead of constantly fearing mistakes because it has
> not understood the user's needs and situation.”

### source[5] — 2026-08-06

> “When something is uncertain in development, decision-making, or design,
> give the user a multiple-choice question instead of thrashing on your own
> and paying a high cost later to change work they do not want.”

### source[6] — 2026-08-06

The maintainer accepted a proposal to learn selected visual-design and
question-sequencing practices from external material. The accepted repository
change gives genuine human decisions their prerequisite context and carries
visual choices through the existing surface and style owners. The
[change record](../plans/2026-08-06-decision-frontier-and-frontend-design.md)
explains that scope. Personal tool installation was separate from the portable
method and is not a dependency for adopters.

### source[7] — 2026-08-28

> “When presenting a choice to the user, provide the context needed to trade
> off — the ROI and the assumptions accepted along with the risk — rather
> than reporting a problem without saying what impact it has or under what
> conditions it does not matter. The standpoint matters: the user, the
> product manager, and the architect cut into the same problem differently.”

### source[8] — 2026-09-06

Maintainer feedback in the template review task, rendered in English: once
the pending decisions are settled, continue through the authorized task to a
working end state. Do not stop for user review at artificial phases. Stop when
new facts actually prevent completion or require a decision outside the agreed
scope.

### source[9] — 2026-09-07

English rendering of the maintainer's approval: implement the scoped proposal
for consequence-based risk, lightweight authorized local behavior, scoped
runtime policy, and task-relevant context. Use English for repository edits.

### source[10] — 2026-09-14

English rendering of maintainer feedback distilled from first-party adoption:
the authorization boundary is bidirectional — unauthorized destructive or
externally visible action is a violation, and so is interrupting the owner to
approve authorized, reversible, or read-only work. During alignment, instant
agreement without independent judgment is a failure mode.

### source[11] — 2026-09-25

English paraphrase of the maintainer's request: generalize a coarse requirement
alignment process that uses existing context, collects only information that
changes the decision, and supports both new and existing projects. Examples
identify a class of problem rather than an exhaustive list. The public scope
is stated in [adoption source 10](project-adoption.md#source10--2026-09-25);
personal background and preferences are not part of this source account.

### source[12] — 2026-09-27

Public interpretation of the maintainer's request: use leverage in choosing
important work; explain the real candidates, the strongest alternative not
chosen, and whether the search omitted more valuable directions. Avoid spending
large effort on low-value detail while the important outcome remains unchanged.

Context: authorized general-method refinement after observed autonomous use;
private material is retained outside this public repository.

### source[13] — 2026-09-27

English rendering of the maintainer's request: the project's Grill Agent
practice needs strengthening or completion; some questions are worth asking
regularly, whether through a fixed template or fixed questions. The request
followed an assessment of the discipline through Meadows' leverage points,
including the impact of changing defaults such as adding operations to
`AGENTS.md`.

The maintainer then selected a separately invocable Grill role focused on
challenging goals, assumptions, and proposals, rather than embedding it as the
default collaboration flow.

The question set, recurring-use conditions, and operating-guide assignment
are implementer choices for that request, not questions dictated verbatim by
the maintainer or a claimed adoption of all of Meadows' framework.

### source[14] — 2026-09-27

Public account of an explicitly accepted revision proposal: strengthen Grill
as a reviewer of problems important to the current owner's goals and standards,
with freedom to challenge direction and without requiring a repair plan for a
valid finding. Reuse existing personal-context onboarding and delegation;
personal standards stay separate from this public method. Independent review
receives relevant intent and evidence, preserves its first judgment before
executor explanation, and investigates the scope of a loss of confidence.
Verify differing owner standards, goal failure despite task completion,
consequential findings without repairs, and supported no-findings outcomes.

The accepted scope is the existing role, its governing section, necessary
invocation cues, and extended delivery evidence. It does not authorize a new
preference store, scoring system, onboarding system, or runtime automation.

## Reconciliation log

- **2026-09-27 — Grill follows the current owner's standards:** connected the
  role to existing personal-context, delegation, and independent-review owners.
  Findings may question the work's value or direction without prescribing its
  repair; confidence concerns require evidence and a stated affected scope.
  - from: source[14]

- **2026-09-27 — recurring Grill questions:** added a stable question set and
  conditions for using and revisiting it, with consequence tracing for standing
  defaults. A dedicated guide carries the separately invocable role; existing
  authorization, uncertainty routing, execution risk, and independence owners
  still apply.
  Behavioral effectiveness remains partial pending real-project use.
  - from: source[13]

- **2026-09-27 — meaningful work comparison:** substantive priority claims
  expose candidate coverage, the strongest alternative and decisive trade-off,
  with a bounded search and no additional approval ritual.
  - from: source[12]


- **2026-09-25 — alignment follows missing understanding:** added coarse
  conditions for investigation, human choice, action, and scoped realignment
  within the existing uncertainty route. No new approval state is introduced.
  - from: source[11] (2026-09-25 task alignment and selective context)

- **2026-09-15 — standing charter as declared authorization:** the
  work-selection invariant now names a charter under
  `autonomous-operation-discipline.md` as one form of declared authorization
  for unattended execution, with pre-named pause points. The authority classes
  are unchanged.

- **2026-09-14 — bidirectional boundary and genuine agreement:** first-party
  adoption feedback motivated the option-set clarification and added two
  clarifications: the authorization boundary punishes over-asking as well as
  unauthorized action, and agreement without independent judgment is a
  failure mode during alignment.
  - from: source[10]

- **2026-09-07 — authorization and execution depth separated:** an authorized
  local behavior change can update its existing owner through the lightweight
  route. Classification cannot create authorization or expand implementation
  discretion into product direction.
  - from: source[9]

- **2026-09-06 — continuous authorized delivery:** clarified that existing
  authorization persists through internal checkpoints and independent reviews;
  only a new material decision or actual blocker pauses its affected path.
  - from: source[8]

- **2026-08-28 — problem reports carry impact context:** G3 and the risk
  state now require who bears the impact, its rough magnitude, the
  conditions under which the problem does not matter, and the assumption
  that accepting the risk would make. G7 option sets state when the
  difference between options does not matter instead of manufacturing a
  preference. Source: owner direction of 2026-08-28, mined against archived
  external materials (error-budget policy as the quantified form of risk
  acceptance; architecture decisions framed as investments with ROI).
  Verification remains partial until real project reports exercise the
  fields. Plan: `docs/plans/2026-08-28-engineering-judgment-discipline.md`.
  - from: source[7]
- **2026-08-06 — dependent decisions use a frontier:** the owner approved the
  reviewed extraction of the grilling method without its parallel glossary or
  ADR outputs. G7 now sequences only genuine human decisions by prerequisite,
  requires shared-understanding confirmation before dependent material work,
  and explicitly preserves the existing fact, experiment, and G6 routes.
- **2026-08-06 — uncertainty routing made explicit:** reconciled the owner's
  preference for choice-based clarification with the existing positive
  engineering envelope. G7 now distinguishes researchable facts, unavailable
  tools, technical experiments, reversible local choices, and material human
  decisions; only the last category returns a bounded option set by default.
  Verification remains partial because repository checks establish consistent
  projection, not real-project decision quality.
- **2026-07-26 — target created:** recorded limited governance authority as the
  agreed operating model: decision support without product-direction takeover.
- **2026-07-26 — implemented:** reconciled contributor and agent entrypoints,
  project-operation guidance, onboarding scope, and the agent work-selection
  protocol. Real-project behavioral evidence remains outstanding.
- **2026-07-28 — positive delegation target landed:** bounded blockers were
  insufficient to prevent approval-seeking on ordinary engineering choices.
  G6 now grants reversible local discretion and G7 routes technical unknowns to
  investigation or controlled experiments. Agent/contributor entrypoints and
  project-operation guidance now expose that route. Verification remains
  partial until a real adopter exercises the boundary under delivery pressure.
- **2026-08-20 — publication language:** source anchors are published as
  English renderings of the original authorizations. Contracts that cite the
  same statement use the same wording; meaning is unchanged.
- **2026-08-28 — cutover to heading-slug identifiers:** the G1–G7 codes were
  retired; headings are now the identifiers per [documentation-harness § invariant-citations](documentation-harness.md#invariant-citations-resolve-to-headings).
  Incoming references across living documents were rewritten to slug links in
  the same change. Earlier entries in this log, completed plans, and dated
  evidence keep the codes as written.
