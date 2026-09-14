---
doc_type: contract
status: current
authority: normative
contract_role: governance
implementation: implemented
verification_status: partial
last_reconciled: 2026-09-14
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

- source-template transfer-value ordering for a visiting agent;
- AI-guided discovery and onboarding;
- greenfield initialization and brownfield adoption;
- governance profile, managed scope, and enforcement-stage decisions;
- current-state baselines, staged migration, verification, and recovery.

Out of scope:

- requiring every adopter to copy every ranked practice or carrier;
- creating a separate learning authority alongside adoption;
- automatically rewriting product architecture or code;
- declaring historical debt invalid merely because it predates the template;
- choosing product priority or risk appetite;
- requiring one repository layout, tracker, language, or CI provider.

## Source anchors

### source[1] — 2026-07-26

> “How to onboard correctly and quickly when using this template as a new
> project or applying it to a project that is already running.”

### source[2] — 2026-07-26

> “They may have a blind spot during onboarding and misunderstand this
> framework, so you need to provide some onboarding guidance, for example an
> Onboarding.md.”

### source[3] — 2026-07-26

> “Agreed” to adopt AI-guided onboarding, and to let brownfield projects
> tighten governance in stages.

### source[4] — 2026-08-06

> “I do not think this should keep adding files. Adoption and learning differ
> only in how strongly they are phrased. As a template that already holds a
> lot of knowledge and architecture, what you should give is a value ranking
> of everything in this project, so that when a new agent comes in and later
> leaves, and it decides for itself what to take, it has that ranking. For
> example, I think the interaction habits should have a very high priority.”
>
> “Agreed. Try adjusting it that way.”

### source[5] — 2026-08-24

> “This should not remain only in the current project; it also needs to be
> exported, for example by updating the Template Project.”

### source[6] — 2026-08-24

> “I agree that you should make the change in the Template project. But you
> also need to think about whether that change matches that project's own
> expectations, and you need to evaluate the value of this backfilled
> information. You cannot simply put down the historical pits you stepped in.
> How much value do those pits have? And how should a user look at them?”

### source[7] — 2026-08-27

> “When adopting external material, triage it by authorship before deciding
> how much to trust it.”

### source[8] — 2026-09-14

English rendering of maintainer feedback distilled from the maintainer's
collaboration archive: when mining history for rules, recurrence measures a
problem's stubbornness, not a preference's weight; the weight signal is
whether the rule was institutionalized — written into standing rules or
tooling — not how often it was said.

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
- **Transfer-value order:** the source template's default ranking of what a
  visiting agent should understand first, based on breadth, downstream
  leverage, error cost, portability, and dependence on target-project context.
- **Carrier:** a document layout, template, checker, CI example, or other
  mechanism that transports or enforces a practice but is not the practice's
  value by itself.

## Ownership and boundary

The adopting human owner selects the profile, managed scope, priority source,
and enforcement stage. AI performs read-only inventory, identifies conflicts
and risks, drafts the assessment and migration plan, and executes only the
confirmed scope. Existing product and organizational authorities retain their
ownership until explicitly reconciled or superseded.

The template owner ranks the source template's transfer value. Existing
development, governance, architecture, and surface contracts continue to own
the ranked practices themselves. A visiting agent uses the ranking to allocate
attention and decide what is relevant to carry forward; target-project evidence
may change applicability, while target authority still governs any resulting
write or enforcement decision.

- from: source[1], source[2], source[3], source[4]

## States and triggers

| Stage | Current truth | Enforcement | Entry trigger | Exit evidence |
|---|---|---|---|---|
| `observed` | Inventory is incomplete but source-preserving | Findings only | Onboarding starts | Authority, source roots, delivery path, and conflicts inventoried |
| `baselined` | Current behavior and historical gaps are recorded | New work must not silently expand named debt | Baseline confirmed by owner | Profile, managed scope, priority source, and migration plan confirmed |
| `scoped_enforcement` | Selected boundaries are reconciled | Declared rules gate only managed scope | First bounded migration lands | Every selected boundary has contract and verification evidence |
| `adopted` | Chosen profile is the normal project standard | Normal governance gates apply | All agreed adoption outcomes pass | Completion record and residual exceptions are durable |

The stage is a declared input, not a description. `[adoption].stage` in
`docs-policy.toml` selects it, and the repository check honours it: adoption
gates report without blocking in `observed` and `baselined`, and block from
`scoped_enforcement` onward. `[adoption].managed_paths` narrows the governed
file set in `scoped_enforcement` so declared rules gate only the confirmed
boundaries. The selected governance profile is likewise declared, as
`[templates].profile`.

An adopting repository must therefore be able to pass its own check at every
stage: an early stage reports the outstanding adoption work instead of
demanding that it be fabricated.

Greenfield projects may move directly from a completed initial assessment to
`scoped_enforcement`. Brownfield projects default to staged progression unless
the owner explicitly chooses and can verify an immediate cutover.

- from: source[1], source[3]

## Normative invariants

### Discover before translating

Onboarding begins read-only. It inventories architecture, source roots,
existing documentation, contracts, tests, CI/release paths, trackers, owners,
and active delivery obligations before proposing replacements.

- from: source[1], source[2]

### Current and target truth stay separate

The baseline records what is true now, including contradictions and debt. An
aspirational architecture or governance profile remains target/planning until
implemented and verified. Passing the template checker is not permission to
rewrite history or label an incomplete migration adopted.

- from: source[2]

### Existing authority is preserved until reconciled

Onboarding does not overwrite ADRs, contracts, tracker ownership, release
procedures, or local agent instructions. Conflicts are catalogued and resolved
through the normal authority and supersession process.

- from: source[2], source[3]

### Adoption is explicitly scoped

The assessment names the governance profile, managed paths and boundaries,
source roots, excluded scope, priority authority, and enforcement stage. The
framework must not infer that copying files grants authority over the entire
project.

Each of those decisions has a corresponding field in `docs-policy.toml`, and
the checker reads them rather than assuming one layout. A repository whose code
lives outside every declared source root is reported, not passed: silence must
not be mistaken for compliance.

- from: source[1], source[2], source[3]

### Historical debt does not become invisible or project-wide blocking

Brownfield baseline debt has evidence, category, affected boundary, owner, and
disposition. It does not block unrelated authorized delivery merely because it
exists. New work may not silently enlarge the same debt class; affected work
must resolve it, bound it, or obtain an explicit exception.

- from: source[1], source[3]

### Stage transitions require evidence

An AI or checker may recommend a transition, but the adopting owner confirms
profile and scope. Each transition records exit evidence, remaining gaps,
exceptions, and rollback or recovery. `adopted` is a project-level claim, not a
synonym for copying the template or passing one command.

- from: source[1], source[2], source[3]

### Transfer value is ranked before its carriers

A visiting agent must not have to infer the template's relative value from file
volume, mechanical visibility, or how easy an artifact is to copy. Source
entrypoints expose this base attention and extraction order before adoption
mechanics:

1. **Interaction and epistemic discipline:** investigate before asking, verify
   unfamiliar facts, preserve evidence strength when tools fail, explain causal
   boundaries, route uncertainty correctly, weigh external material by
   authorship, and preserve human direction and risk authority.
2. **Truth, ownership, and boundaries:** distinguish current from target truth,
   keep one owner per invariant, publish interfaces deliberately, preserve
   dependency direction, and keep historical debt visible and bounded.
3. **Delivery discipline:** describe one coherent end state, select execution
   depth by risk, choose credible evidence for the requested material outcome,
   guard repeatable defect mechanisms, verify failure and recovery, and
   recognize facts that leak across the system if left unnamed.
4. **Conditionally activated disciplines:** frontend, backend, cross-stack,
   style, data, operations, security, performance, time and calendar,
   demonstration data, or other specialist rules whose transfer value rises
   when the target project activates that concern.
5. **Carriers and enforcement mechanisms:** documentation topology, templates,
   adoption stages, policy manifests, the portable checker, and CI examples,
   selected only when they serve the target project's chosen practices.

This is a transfer-value order, not a document-authority order, universal
mandate, or substitute for target evidence. An activated conditional discipline
may move ahead of a general delivery concern for that project. Learning and
adoption consume the same ranking; they differ in authorized action, not in a
second body of source knowledge. Root projections stay compact and link to the
existing owners rather than copying their full rules.

- from: source[4], source[5], source[7]

### External material is triaged by authorship before adoption

External engineering material — another project's archive, a methodology
write-up, a generated report — mixes records of different strength. Before any
of it informs a contract, template, or practice, separate it by who authored
each part:

- dated human decisions, instructions, and corrections are primary evidence of
  what the human owner actually wanted;
- machine-generated summaries, self-described methodologies, and retrospective
  narratives are leads, not evidence: they may propose hypotheses, but an
  adopted claim must trace to a primary record or be independently verified;
- material whose authorship cannot be determined is treated as unverified.

The volume and polish of generated narrative is not evidence of value, and
importing its vocabulary can pollute the receiving documents. Recurrence is
also not a weight signal: repetition measures how stubborn a problem is, not
how much a preference weighs, and a rule institutionalized after one
statement can outweigh a complaint repeated weekly. An adoption or
learning record states which class each adopted lesson came from.

- from: source[7], source[8]

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
- Root reader and agent entrypoints expose the transfer-value order before
  adoption mechanics, with interaction and epistemic discipline first.
- The onboarding guide explains that target evidence may promote a conditional
  discipline without changing document authority or requiring wholesale copy.
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
- the declared stage and managed scope are checker inputs: fixtures confirm that
  `observed` and `baselined` report adoption gaps without failing the build,
  that `scoped_enforcement` gates only `managed_paths`, and that a rejected
  stage name fails;
- the full Python 3.11 fixture suite and the repository checker pass.

Verified on 2026-08-06:

- before entrypoint implementation, focused cold-read probes found none of the
  value-order headings in `README.md`, `AGENTS.md`, or the onboarding procedure;
- after implementation, `README.md` exposes the ranked value before usage
  mechanics, `AGENTS.md` exposes it before repository read order, and onboarding
  begins with transfer-value orientation before adoption classification;
- the projections put interaction and epistemic discipline first, distinguish
  transfer order from authority order, permit target evidence to promote an
  activated domain discipline, and place copyable carriers last;
- the full 106-test Python 3.11 fixture suite, normal repository check, strict
  repository check, and whitespace audit pass.

Verification remains `partial`: first-party greenfield and brownfield
repositories have completed this onboarding path since 2026-07 (see the
2026-09-14 entry), but no adopter independent of the maintainer has completed
it, so independent usability, proportionality, and stage-transition behavior
are not independently proven.

Verified on 2026-08-27:

- the authorship-triage invariant and the transfer-value-order invariant first-tier mention landed; the full Python 3.11 fixture suite
  and both repository checker modes pass;
- verification remains partial: no visiting agent has yet applied the
  authorship triage to real external material under this contract.

Verified on 2026-09-14:

- first-party greenfield and brownfield adoptions have completed this
  onboarding path since 2026-07, and their corrections are reconciled in the
  contracts they exercised. Evidence:
  [2026-09-14 first-party adoption feedback](../evidence/2026-09-14-first-party-adoption-feedback.md);
- adoption by a repository independent of the maintainer remains unproven, so
  verification stays `partial`.

## Explicit non-goals

- Onboarding is not a mandatory cleanup of all historical debt.
- The framework does not choose the project's roadmap or governance profile.
- An assessment does not authorize unrelated code migration.
- Staged enforcement is not permission to leave scope or debt unowned.

## Reconciliation log

- **2026-09-14 — first-party adoption evidence recorded:** the onboarding
  path has now been completed by first-party greenfield and brownfield
  projects; the independent-adoption gap is stated explicitly instead of a
  blanket no-real-project note.

- **2026-09-06 — delivery method aligned:** the transfer value order still
  prioritizes complete delivery over its carriers; evidence methods now follow
  the outcome-driven agent execution owner rather than a fixed test-first loop.

- **2026-08-27 — authorship triage added:** O8 requires separating external
  material by authorship before adoption: dated human instructions and
  decisions are primary evidence, machine-generated narrative is a lead to
  verify, and its vocabulary does not enter project documents. O7's first
  tier now names the triage. Source: review of an external project archive
  in which generated narrative had coined terminology the owner rejected as
  pollution.
  - from: source[7]
- **2026-08-24 — leak-class facts ranked, pit catalog rejected:** O7 delivery
  discipline includes the test for facts that leak if unnamed. Time/calendar
  and demonstration data remain conditional examples, not a required
  questionnaire. A 15-row adopter register of sibling incidents was retracted
  as ceremony. Method owner:
  `docs/contracts/foundational-runtime-discipline.md`.
  - from: source[5], source[6]
- **2026-08-06 — source transfer value ranked:** the owner rejected a separate
  learning-document expansion and required the template to rank what a visiting
  agent should take away. O7 now puts interaction and epistemic discipline
  first, then truth and ownership, delivery, conditionally activated domain
  practices, and finally their carriers. Existing README, agent, and onboarding
  entrypoints expose that order before mechanics without moving the underlying
  rules from their current owners. Verification remains partial until a fresh
  agent exercises the path from the real one-line referral.
- **2026-08-20 — publication language:** source anchors are published as
  English renderings of the original authorizations. Meaning is unchanged.
- **2026-07-26 — target created:** defined AI-guided greenfield/brownfield
  onboarding with explicit scope and evidence-backed staged enforcement.
- **2026-07-26 — implemented:** added current onboarding and post-adoption
  operation guides, a first-class assessment record, entrypoint routing, and
  missing-file/section guards. Real-project adoption evidence remains open.
- **2026-07-26 — stage and scope made mechanical:** the staged model existed
  only as prose, so an adopter at `observed` could not satisfy its own
  verification step without fabricating adoption artifacts. `[adoption].stage`,
  `managed_paths`, `source_roots`, and `[templates].profile` are now checker
  inputs.
- **2026-08-28 — cutover to heading-slug identifiers:** the O1–O8 codes were
  retired; headings are now the identifiers per [documentation-harness § invariant-citations](documentation-harness.md#invariant-citations-resolve-to-headings).
  Incoming references across living documents were rewritten to slug links in
  the same change. Earlier entries in this log, completed plans, and dated
  evidence keep the codes as written.
