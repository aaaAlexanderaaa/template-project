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
alternatives, and limitations. A rejected recommendation remains evidence or
history; it does not silently return as a mandatory rule. Agreement is held
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

- from: source[2], source[7], source[10]

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

An experiment does not authorize product behavior, production exposure,
privileged access, or irreversible mutation. Its result may inform a later
recommendation or contract, but cannot silently become either.

- from: source[4], source[5], source[6], source[8]

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

Verified on 2026-09-14:

- first-party projects applying this boundary under delivery pressure since
  2026-07 confirmed the bounded option set with trade-off context as the
  stable decision interface, and produced the bidirectional-boundary and
  genuine-agreement clarifications recorded in the reconciliation log.
  Evidence: [2026-09-14 first-party adoption feedback](../evidence/2026-09-14-first-party-adoption-feedback.md);
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

> “Agreed with your understanding: adopt frontend-design, uninstall
> ui-ux-pro-max, and learn what is worth learning.”

### source[7] — 2026-08-28

> “When presenting a choice to the user, provide the context needed to trade
> off — the ROI and the assumptions accepted along with the risk — rather
> than reporting a problem without saying what impact it has or under what
> conditions it does not matter. The standpoint matters: the user, the
> product manager, and the architect cut into the same problem differently.”

### source[8] — 2026-09-06

Original maintainer wording in this task:

> “如果所有的待确认项都确定好了，那就直接瀑布式开发到本次任务结束，
> 不要分什么阶段123来让用户review或确认”

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

## Reconciliation log

- **2026-09-15 — standing charter as declared authorization:** the
  work-selection invariant now names a charter under
  `autonomous-operation-discipline.md` as one form of declared authorization
  for unattended execution, with pre-named pause points. The authority classes
  are unchanged.

- **2026-09-14 — bidirectional boundary and genuine agreement:** first-party
  adoption feedback confirmed the option-set interface and added two
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
