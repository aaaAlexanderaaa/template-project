---
doc_type: contract
status: current
authority: normative
contract_role: governance
implementation: implemented
verification_status: partial
last_reconciled: 2026-08-06
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

## Source anchors

### source[1] — 2026-07-26

> “它作为一个治理框架，它不应该去帮助开发者定义优先级，它只能作为辅助，
> 而不做决策。”

### source[2] — 2026-07-26

> “可以帮助开发者识别那些他没有识别到的风险和，应该注意到的对长期项目
> 发展带来的异常。但他不应该在开发者有自己的想法的时候，阻碍他说你这个
> 想法不对。”

### source[3] — 2026-07-26

> “同意”采用有限治理权、AI 引导式 onboarding 和 brownfield 分阶段收紧。

### source[4] — 2026-07-28

> “赋能而不是阻碍，让 agent 可以清楚自己什么该做和不该做，而不是因为未能
> 理解用户的需求和场景时刻担心犯错。”

### source[5] — 2026-08-06

> “如果在项目开发、决策或者设计当中有不确定的东西，就给用户做选择题，
> 而不是自己瞎折腾，做出来不满意以后又花很多成本去改。”

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
| `risk` | Plausible adverse outcome or long-term abnormality | Fact plus causal mechanism exists | Record impact, likelihood limits, and options |
| `recommendation` | Non-binding preferred response | Trade-offs can be compared | Direction authority accepts, rejects, or defers |
| `human_decision_required` | No authorized choice exists | Options materially change intent, priority, or risk | Obtain and record the owner's choice |
| `execution_blocker` | One path cannot proceed truthfully or safely | A blocker class below is proven | Resolve, change path, or record an allowed exception |

The state must be explicit. A recommendation cannot be worded or enforced as a
blocker merely because the framework strongly prefers it.

- from: source[1], source[2], source[3]

## Normative invariants

### G1 — Humans own direction and priority

The framework consumes a declared priority source. It may identify missing
outcomes, dependency conflicts, aging work, concentrated risk, or likely
long-term maintenance cost, but those findings remain inputs to the authorized
owner's decision.

When no priority authority exists, an agent presents candidate work and its
evidence as recommendations and requests a decision. It does not convert its
own ranking into project authority.

- from: source[1], source[2]

### G2 — Blockers are narrow and evidence-backed

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

### G3 — Advice preserves disagreement

Recommendations state their evidence, assumptions, expected benefit, cost,
alternatives, and limitations. A rejected recommendation remains evidence or
history; it does not silently return as a mandatory rule.

- from: source[2]

### G4 — Exceptions are explicit, scoped, and reviewable

An authorized owner may accept a governance exception when the governing rule
permits human waiver. The record names the rule, scope, reason, date, owner,
residual risk, expiry or review trigger, and recovery path. An exception cannot
manufacture missing product authority or silently waive legal or safety
authority owned elsewhere.

- from: source[1], source[3]

### G5 — Work selection consumes authority

An agent may resume already authorized in-progress work, follow a declared
priority order, and perform read-only portfolio diagnosis. When it discovers
untracked work, it records the candidate and evidence before non-trivial
implementation, but the portfolio owner decides its priority unless an
existing policy already determines it.

- from: source[1], source[2]

### G6 — Delegated engineering work proceeds by default

Within an authorized outcome and managed scope, an agent or contributor may
make a local engineering choice without requesting approval when the choice is
reversible at reasonable cost and does not change product meaning, a public
contract, authorization or capability, irreversible or durable-state
semantics, an activated quality-attribute boundary, or another owner's private
rule. Normal naming, decomposition, test organization, and equivalent internal
implementation choices belong to this envelope.

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

- from: source[4]

### G7 — Missing knowledge is routed, not automatically escalated

Route uncertainty by what resolves it and by the cost of being wrong:

- an unfamiliar, externally checkable fact or reference uses development D10's
  authoritative-source research rather than guessing;
- an unavailable tool uses development D11's capability-preserving fallback
  before the task is described as blocked;
- a missing technical fact first produces bounded read-only investigation and,
  when necessary, the controlled experiment defined by development D1;
- a locally reversible implementation choice inside G6 is made and verified by
  the implementer rather than returned for serial approval;
- unknown product intent, a material design or decision trade-off, authority,
  expensive-to-reverse preference, or risk acceptance produces
  `human_decision_required`.

A required human decision is presented as a bounded option set when genuine
alternatives exist. Each option names the outcome, material trade-offs,
reversibility or switching cost, and the evidence limitation; a recommendation
may be included but must remain visibly non-binding. Do not manufacture a
multiple-choice question when the repository already contains the answer, when
investigation can establish a fact, or when only one path satisfies current
authority.

An experiment does not authorize product behavior, production exposure,
privileged access, or irreversible mutation. Its result may inform a later
recommendation or contract, but cannot silently become either.

- from: source[4], source[5]

## Required behaviors

- Every governance-facing report distinguishes facts, risks, recommendations,
  required human decisions, and execution blockers.
- A priority source is named before autonomous project-level work selection.
- Missing priority produces a decision request, not agent-authored direction.
- Choices inside the engineering decision envelope proceed without serial human
  approval; material assumptions remain visible in the plan or evidence.
- Missing knowledge follows G7: research checkable references, seek a
  capability-preserving tool fallback, investigate technical facts, make
  reversible local choices, and present bounded options only for decisions
  that belong to the human owner.
- A blocker includes scope, evidence, recovery, and available human authority.
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

- D10-D12 and G7 have one explicit uncertainty route across the agent,
  contributor, README, and current operating-guide projections;
- the fixed-date documentation fixtures were reconciled with the new canonical
  dates, and all 106 tests pass under Python 3.11;
- `python scripts/check_docs.py --strict` passes with no findings.

## Reconciliation log

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
