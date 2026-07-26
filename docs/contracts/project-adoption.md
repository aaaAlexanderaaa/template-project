---
doc_type: contract
status: current
authority: normative
implementation: implemented
verification_status: partial
last_reconciled: 2026-07-26
review_due: 2026-10-24
supersedes: []
---

# Project adoption and onboarding discipline

## Purpose

This contract defines how a greenfield or existing project adopts the
engineering discipline template without confusing template examples with
project truth, erasing existing authority, or stopping useful delivery for an
unbounded compliance migration.

## Scope

In scope:

- AI-guided discovery and onboarding;
- greenfield initialization and brownfield adoption;
- governance profile, managed scope, and enforcement-stage decisions;
- current-state baselines, staged migration, verification, and recovery.

Out of scope:

- automatically rewriting product architecture or code;
- declaring historical debt invalid merely because it predates the template;
- choosing product priority or risk appetite;
- requiring one repository layout, tracker, language, or CI provider.

## Source anchors

### source[1] — 2026-07-26

> “采用这个模板项目去作为一个初始项目或者去应用到一个已经正在运行的项目
> 当中，如何正确而快速的 onboarding。”

### source[2] — 2026-07-26

> “有可能是他们在执行 onboarding 的时候会有盲点，就是错误的理解这一个
> 框架，所以你需要给出一些 onboarding 的指引，比如说出一个 Onboarding.md？”

### source[3] — 2026-07-26

> “同意”采用 AI 引导式 onboarding，并让 brownfield 项目分阶段收紧治理。

## Vocabulary

- **Greenfield:** a project without product implementation or established
  project authority.
- **Brownfield:** a running project with existing code, decisions, workflows,
  or delivery obligations.
- **Managed scope:** the paths, boundaries, contracts, and workflows currently
  governed by this framework.
- **Baseline debt:** a truthful, bounded pre-adoption gap that has an owner and
  disposition but is not misrepresented as newly compliant.
- **Adoption profile:** the human-selected depth of governance for the project.

## Ownership and boundary

The adopting human owner selects the profile, managed scope, priority source,
and enforcement stage. AI performs read-only inventory, identifies conflicts
and risks, drafts the assessment and migration plan, and executes only the
confirmed scope. Existing product and organizational authorities retain their
ownership until explicitly reconciled or superseded.

- from: source[1], source[2], source[3]

## States and triggers

| Stage | Current truth | Enforcement | Entry trigger | Exit evidence |
|---|---|---|---|---|
| `observed` | Inventory is incomplete but source-preserving | Findings only | Onboarding starts | Authority, source roots, delivery path, and conflicts inventoried |
| `baselined` | Current behavior and historical gaps are recorded | New work must not silently expand named debt | Baseline confirmed by owner | Profile, managed scope, priority source, and migration plan confirmed |
| `scoped_enforcement` | Selected boundaries are reconciled | Declared rules gate only managed scope | First bounded migration lands | Every selected boundary has contract and verification evidence |
| `adopted` | Chosen profile is the normal project standard | Normal governance gates apply | All agreed adoption outcomes pass | Completion record and residual exceptions are durable |

Greenfield projects may move directly from a completed initial assessment to
`scoped_enforcement`. Brownfield projects default to staged progression unless
the owner explicitly chooses and can verify an immediate cutover.

- from: source[1], source[3]

## Normative invariants

### O1 — Discover before translating

Onboarding begins read-only. It inventories architecture, source roots,
existing documentation, contracts, tests, CI/release paths, trackers, owners,
and active delivery obligations before proposing replacements.

- from: source[1], source[2]

### O2 — Current and target truth stay separate

The baseline records what is true now, including contradictions and debt. An
aspirational architecture or governance profile remains target/planning until
implemented and verified. Passing the template checker is not permission to
rewrite history or label an incomplete migration adopted.

- from: source[2]

### O3 — Existing authority is preserved until reconciled

Onboarding does not overwrite ADRs, contracts, tracker ownership, release
procedures, or local agent instructions. Conflicts are catalogued and resolved
through the normal authority and supersession process.

- from: source[2], source[3]

### O4 — Adoption is explicitly scoped

The assessment names the governance profile, managed paths and boundaries,
source roots, excluded scope, priority authority, and enforcement stage. The
framework must not infer that copying files grants authority over the entire
project.

- from: source[1], source[2]

### O5 — Historical debt does not become invisible or project-wide blocking

Brownfield baseline debt has evidence, category, affected boundary, owner, and
disposition. It does not block unrelated authorized delivery merely because it
exists. New work may not silently enlarge the same debt class; affected work
must resolve it, bound it, or obtain an explicit exception.

- from: source[1], source[3]

### O6 — Stage transitions require evidence

An AI or checker may recommend a transition, but the adopting owner confirms
profile and scope. Each transition records exit evidence, remaining gaps,
exceptions, and rollback or recovery. `adopted` is a project-level claim, not a
synonym for copying the template or passing one command.

- from: source[1], source[2], source[3]

## Required onboarding record

The durable assessment contains:

- project context and greenfield/brownfield classification;
- existing authority and decision-source inventory;
- current architecture, source roots, tests, CI, release, and tracker facts;
- governance profile, managed scope, exclusions, and priority authority;
- conflicts, baseline debt, risks, and limitations;
- current adoption stage and evidence;
- linked migration plan and verification path;
- human decisions still required.

## Failure, recovery, and intervention

- If onboarding begins rewriting product behavior, stop and return to read-only
  inventory plus a separately authorized implementation plan.
- If existing and template authorities conflict, keep the affected boundary in
  `observed` or `baselined` until reconciled.
- If governance causes disproportionate delivery interruption, narrow managed
  scope rather than falsely declaring compliance.
- If an adoption transition is later disproved, move back to the last supported
  stage, preserve the evidence, and record the cause.

## Acceptance evidence

- A current onboarding guide covers separate greenfield and brownfield paths.
- A reusable adoption-assessment template captures every required record field.
- Root, contributor, agent, and documentation entrypoints route onboarding to
  this contract and guide.
- Project-operation guidance preserves human priority authority after adoption.
- The documentation harness validates the assessment template and fixture tests
  cover missing-file and missing-section variants.

Verified on 2026-07-26:

- README and documentation authority guidance route both greenfield and
  brownfield adopters to `docs/guides/onboarding.md`;
- the reusable adoption assessment records current authority, present-state
  facts, governance scope, human priority ownership, staged enforcement,
  migration linkage, verification, and limitations;
- the two new fixture cases first failed before the assessment template existed
  and pass after registration;
- the full Python 3.11 fixture suite passes 36 tests and the repository checker
  validates 12 canonical documents and 14 templates.

Verification remains `partial`: no real greenfield or brownfield repository has
yet completed this onboarding path, so usability, proportionality, and stage
transition behavior are not independently proven.

## Explicit non-goals

- Onboarding is not a mandatory cleanup of all historical debt.
- The framework does not choose the project's roadmap or governance profile.
- An assessment does not authorize unrelated code migration.
- Staged enforcement is not permission to leave scope or debt unowned.

## Reconciliation log

- **2026-07-26 — target created:** defined AI-guided greenfield/brownfield
  onboarding with explicit scope and evidence-backed staged enforcement.
- **2026-07-26 — implemented:** added current onboarding and post-adoption
  operation guides, a first-class assessment record, entrypoint routing, and
  missing-file/section guards. Real-project adoption evidence remains open.
