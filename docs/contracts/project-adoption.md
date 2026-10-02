---
doc_type: contract
status: current
authority: normative
contract_role: governance
implementation: implemented
verification_status: partial
last_reconciled: 2026-10-02
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
- AI-guided discovery and onboarding, including the learning survey of every
  current rule and the requirement to leave a result;
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

Maintainer feedback asked this template to capture the mechanism behind late
repairs to time policy and demonstration data. A missing shared decision can
spread through several components until repair requires coordinated changes.
The accepted transfer is early recognition of that condition, with policy
chosen by each adopting project rather than copied from the original system.

### source[6] — 2026-08-24

The maintainer rejected a proposed checklist of incidents from another
project. The template should teach how to recognize an applicable engineering
risk, not require every adopter to revisit unrelated repairs. Adoption value
and target-project scope govern what is transferred.

### source[7] — 2026-08-27

> “When adopting external material, triage it by authorship before deciding
> how much to trust it.”

### source[8] — 2026-09-14

English rendering of maintainer feedback distilled from the maintainer's
collaboration archive: when mining history for rules, recurrence measures a
problem's stubbornness, not a preference's weight; the weight signal is
whether the rule was institutionalized — written into standing rules or
tooling — not how often it was said.

### source[9] — 2026-09-10

The maintainer authorized lessons about decision attribution and requirement
scope from experience in an assistant-assisted project. The
[learning record](../plans/2026-09-10-reference-feedback-learning.md#source-evidence-and-selection)
provides self-contained examples: an assistant-authored classification must not
be presented as the owner's wording, and an accepted example does not establish
an exhaustive requirement. The underlying project is not part of this public
repository; these are reported motivations and the template's synthesis.

### source[10] — 2026-09-25

English paraphrase of the maintainer's request: support learning this template
and loading separately supplied collaboration background and decision
preferences in a new or existing project. Publish the general onboarding,
alignment, and context-selection method; keep personal material separate.
Earlier feedback asked for a coarse alignment process and context appropriate
to the recipient's task. This account states the authorized public scope; it
does not reproduce the private conversation or imply access to its records.

### source[11] — 2026-10-02

English paraphrase of the maintainer's decision: learning this discipline must
change the target repository, or explicitly say that nothing needs to change,
or explicitly list the changes whose method needs confirmation before they are
made. During learning, every current rule is opened and compared with that
repository. Seeing a name without opening the rule is not learning. Sessions
after learning still open a rule when the work reaches it. Copying the
template wholesale, enabling enforcement, replacing existing instructions, and
changing product code wait for confirmation of method.

### source[12] — 2026-10-02

English paraphrase of the maintainer's decision: a request to learn assumes
the discipline now in force has not met the owner's expectation. The survey
starts from what the owner had to repeat and what the loaded rules caused the
agent to do. A filled policy, a declared stage, or an assessment that reported
no gap does not show the expectation was met.

### source[13] — 2026-10-02

English paraphrase of the maintainer's decision after a landing copied this
repository into a directory that already held the owner's files: that
directory was not empty, so the copy was not starting a new project. The
landing never said what the project was, and a greenfield label stood in for
that statement. The directory was not a git repository; the landing never
said so and did not initialize one before adding files.

### source[14] — 2026-10-02

English paraphrase of the maintainer's decision: onboarding is unfinished
while the agent entrypoint still describes the checkout as a documentation
and project-discipline repository, or its text still matches this template,
and the checkout's git remote is not this template's repository.

### source[15] — 2026-10-02

English paraphrase of the maintainer's choices after two reviews found the
new sentences requiring two actions. When a directory already holds files and
the owner also asks to start from this repository, ask before copying or
refusing. Learning states what the project is, and initializes git and
commits the current files before it writes into a directory that has files
and no repository. A copied entrypoint that still treats the checkout as this
discipline template is replaced with what the project is, without waiting for
a method confirmation. The checker reports that unfinished entrypoint when
any of its identity claims remain. A system or tool note that no further
action is required does not cancel a named end; the owner's own later stop
or new end does. If git cannot be initialized, adding template files stops
and the owner is told. A correction of a rule is written into the entrypoint
and into the contract that owns the sentence; once the contract holds it,
the entrypoint keeps the pointer and drops the repeated full text.

## Vocabulary

- **Greenfield:** an empty directory, before product implementation or project
  authority exists. The name only says the directory started empty. Files
  already in the target directory are not this case. If those files are
  present and the owner asks to start from this repository, ask before
  copying or refusing.
- **Brownfield:** a project that is already running. It has code, decisions,
  workflows, or delivery obligations. The name only says that; it does not
  describe what the project is.
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
and enforcement stage. For formal adoption, AI performs read-only inventory,
identifies conflicts and risks, drafts the assessment and migration plan, and
executes only the confirmed scope. A learning ending may write its judgment
and a contract change whose method did not need a further decision. Existing
product and organizational authorities retain their ownership until explicitly
reconciled or superseded.

The template owner ranks the source template's transfer value. Existing
development, governance, architecture, and surface contracts continue to own
the ranked practices themselves. A visiting agent uses the ranking to allocate
attention and decide what is relevant to carry forward; target-project evidence
may change applicability, while target authority still governs any resulting
write or enforcement decision.

- from: source[1], source[2], source[3], source[4], source[15] (2026-10-02 learning may write a settled contract change)

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

Onboarding begins by reading. It inventories architecture, source roots,
existing documentation, contracts, tests, CI/release paths, trackers, owners,
and active delivery obligations before proposing replacements. The first
result of that reading is a statement of what the project is, under
[the existing-directory rule](#an-existing-directory-is-described-before-template-files-are-added).
Learning then writes only as its ending allows. Formal adoption does not
rewrite authority during that inventory.

- from: source[1], source[2], source[11], source[13]

### Learning and personal context have a bounded entry path

A request to learn the discipline assumes the discipline now in force has not
met the owner's expectation. Find that mismatch first: what the owner had to
repeat, and what the loaded rules caused the agent to do. A filled policy, a
declared stage, a passing or failing checker, or an earlier assessment that
reported no gap does not show the expectation was met.

The request also authorizes a survey of every current rule against the target
repository, and it requires one of the endings below. Seeing a title, a table
row, or a link without opening the rule is not a survey. It does not by itself
authorize a governance migration, new CI gates,
replacement of the target's existing instructions, or product-code changes.
Use the formal adoption assessment and stages when adoption or enforcement
changes are requested.

Learning opens:

- the documentation authority map, including its language-style section;
- every current contract: development discipline, the governance decision
  boundary, this contract, agent execution, the documentation harness,
  foundational runtime, and autonomous operation;
- the engineering-judgment contract, recorded as a target draft rather than
  a current rule;
- every row of development discipline's concern table, followed into the
  section that owns that row;
- the behavior guides: onboarding, project operation, research, information
  access, and Grill.

Plans, evidence, and source chronology stay closed unless a judgment depends
on a disputed decision or a recovery. After learning, a later task still opens
a rule when the work reaches it. The written judgment is how that later task
sees what this repository was already compared with.

For each opened rule, record one result:

- it applies, and the repository already satisfies it;
- it applies, and the repository does not yet satisfy it;
- it does not apply, together with the repository fact that makes that so.

A note that only says "not triggered" is not a result.

Learning ends in one of these ways, and a session may both write and ask:

1. The target repository contains the judgment and the changes whose method
   did not need a further decision. Tell the owner what changed. Write the
   judgment in the existing agent entrypoint, the text the next session loads,
   and change the contract that owns each changed rule. The entrypoint names
   the rule, the result, and the contract section. It does not paste that
   section or a second copy of a product fact. After the contract holds the
   rule, the entrypoint keeps the pointer and drops the repeated full text.
   If that entrypoint does not exist, add one that carries the judgment and
   leaves other instructions untouched. A copied description that still treats
   this checkout as the engineering discipline template is not an existing
   project instruction; replace it in this ending with what this project is.
2. Nothing in the repository needs to change. Say so. Name the rules that
   apply and are already satisfied, and give the repository fact for every
   rule that does not apply. This ending is available only when the comparison
   with the owner's expectation has been made and no applicable rule is
   unsatisfied. A filled policy file is not that comparison. A summary that
   omits those results is not this ending.
3. One or more changes need a decision about how they will be made. List each
   change and the intended method, and wait. Do not make those changes yet.
   Copying this template wholesale, enabling enforcement, replacing existing
   instructions, and changing product code are in this group.

Finishing in conversation alone, while a change in the first group is still
unwritten, is not learning.

Before that ending, state what the project is: the material already in the
directory, the use the owner has given it, and what is absent. When the ending
will write a file into a directory that already holds files and is not a git
repository, say so, initialize git, and commit those files first. If git
cannot be initialized, stop adding files and tell the owner. An ending that
writes nothing does not require that commit.

- from: source[10], source[11], source[12], source[15] (2026-10-02 learning states the project and commits before a write)

When the user supplies collaboration background and decision preferences,
start at that material's onboarding entrypoint and use the applicable context.
Treat background, preference, inference, and permission as distinct. Reconcile
a material conflict with the current task and target authority; an ordinary
preference difference within the decision envelope is not a blocker. Personal
context is optional: its absence does not prevent authorized work, and a
missing path is reported without searching unrelated private locations.

Keep personal material at the location and visibility authorized by its owner.
Learning it does not authorize copying it, its local paths, or derived personal
details into a public repository, issue, review, or worker assignment. A general
lesson can enter the target's existing owner after removing identifying and
personal context and checking applicability. A project-specific choice may be
recorded in an audience-appropriate form under
[decision preservation](development-discipline.md#preserve-decisions-and-evidence).
Use a private or session-local locator for personal context; this public
template must remain usable without any individual's memory or account.

- from: source[10] (2026-09-25 separate personal context and public method)

### An existing directory is described before template files are added

Before any file from this template is copied into a target, state what that
project is. Name the material already in the directory, the use the owner has
given it, and what is absent. A class label does not replace that statement.
The statement decides whether a template file may be added.

A directory that already holds the owner's files is not an empty start.
Missing product code, a missing agent entrypoint, and missing contracts do
not make it empty. This repository is the starting tree when the target
directory is empty. When the directory already holds files and the owner also
asks to start from this repository, stop and ask whether to copy. Do not copy
and do not treat the request as already refused.

When the directory already holds files and is not a git repository, say so.
Initialize git and commit that tree as the first revision before any template
file is added, and before a learning ending writes a file there. The owner's
material and the added files then stay separable. If git cannot be
initialized, stop adding template files and tell the owner. That stop does
not cancel other work that adds no template file. Leaving the missing
repository unmentioned is not a finished look at the project.

Onboarding is unfinished while the agent entrypoint still treats the checkout
as this discipline template and the git remote is not
https://github.com/aaaAlexanderaaa/template-project. It still treats the
checkout that way while any of these claims remain: that this repository is
the engineering discipline template; that its work is documentation and
project discipline; that onboarding into any other checkout is unfinished
while the entrypoint still says this; that a task is to learn this template;
or that a task is adoption into another project. A checkout with no git
remote still has that unfinished entrypoint. The template's own checkout is
the case where those claims and that remote belong together. Finishing
replaces those claims with what this project is, without waiting for a
separate confirmation of method. The documentation checker reports the
unfinished entrypoint when any of those claims remain and the directory is a
git repository.

- from: source[13] (2026-10-02 existing directory is not an empty start), source[14] (2026-10-02 template entrypoint means onboarding is unfinished), source[15] (2026-10-02 ask before copying, replace the template claims)

### Current and target truth stay separate

The baseline records what is true now, including contradictions and debt. An
aspirational architecture or governance profile remains target/planning until
implemented and verified. Passing the template checker is not permission to
rewrite history or label an incomplete migration adopted.

- from: source[2]

### Existing authority is preserved until reconciled

Onboarding does not overwrite ADRs, contracts, tracker ownership, release
procedures, or local agent instructions. Learning may add its judgment to the
local agent entrypoint and must leave the existing instructions in place.
Replacing those instructions waits for confirmation of method. A copied claim
that this checkout is the engineering discipline template is not one of those
instructions; replacing it with what this project is does not wait. Conflicts
are catalogued and resolved through the normal authority and supersession
process.

- from: source[2], source[3], source[11], source[15] (2026-10-02 a copied template claim is not an existing instruction)

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
  what the human owner actually wanted when their origin is available; a later
  quotation with a missing original remains a reported statement with that
  limitation, rather than becoming direct evidence merely through quote marks;
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

Inspect the source artifact and relevant changes before accepting a report's
explanation of what happened. A commit establishes a change, not who originated
every statement or whether users benefited. Use [decision preservation](development-discipline.md#preserve-decisions-and-evidence)
for attribution and acceptance; do not copy a source project's approval labels
or stricter ceremony into the target by default. For each selected lesson,
identify its mechanism, target owner, existing coverage, and applicability
limit. Keep already-covered lessons as corroboration rather than adding a
second rule. Rejected or uncertain source claims remain evidence, not policy.

- from: source[7] (2026-08-27 authorship triage), source[8] (2026-09-14 recurrence and preference weight), source[9] (2026-09-10 attribution and applicability)

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

- If onboarding begins rewriting product behavior, stop and return to the
  inventory plus a separately authorized implementation plan. A learning
  judgment added to the agent entrypoint is not a product rewrite.
- If existing and template authorities conflict, keep the affected boundary in
  `observed` or `baselined` until reconciled.
- If governance causes disproportionate delivery interruption, narrow managed
  scope rather than falsely declaring compliance.
- If an adoption transition is later disproved, move back to the last supported
  stage, preserve the evidence, and record the cause.

## Acceptance evidence

- A current onboarding guide covers an empty start and a brownfield path, and
  requires a statement of what the project is before either label. A directory
  that already holds files is not an empty start: the guide forbids copying
  this repository over it, and requires git to be initialized and the current
  tree committed before template files are added.
- Onboarding stays unfinished while the agent entrypoint still describes the
  checkout as this discipline template and the git remote is not
  https://github.com/aaaAlexanderaaa/template-project.
- A reusable adoption-assessment template captures every required record field.
- Root, contributor, agent, and documentation entrypoints route onboarding to
  this contract and guide.
- Root reader and agent entrypoints expose the transfer-value order before
  adoption mechanics, with interaction and epistemic discipline first.
- The onboarding guide explains that target evidence may promote a conditional
  discipline without changing document authority or requiring wholesale copy.
- The learning path names every current rule to open, the three results for
  each rule, and the three endings. Later tasks still open a rule when the
  work reaches it.
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

Verification remains `partial`: the maintainer reports greenfield and
brownfield adoption since 2026-07 (see the September 14 account). The underlying
project evidence is not public. Independent usability, proportionality, and
stage-transition behavior remain unproven.

Verified on 2026-08-27:

- the authorship-triage invariant and the transfer-value-order invariant first-tier mention landed; the full Python 3.11 fixture suite
  and both repository checker modes pass;
- verification remains partial: no visiting agent has yet applied the
  authorship triage to real external material under this contract.

Maintainer-reported adoption on 2026-09-14:

- the maintainer reports greenfield and brownfield adoption since 2026-07.
  The resulting corrections are inspectable in this repository; the original
  adoption records are not public. Report and limits:
  [2026-09-14 first-party adoption feedback](../evidence/2026-09-14-first-party-adoption-feedback.md);
- adoption by a repository independent of the maintainer remains unproven, so
  verification stays `partial`.

## Explicit non-goals

- Onboarding is not a mandatory cleanup of all historical debt.
- The framework does not choose the project's roadmap or governance profile.
- An assessment does not authorize unrelated code migration.
- Staged enforcement is not permission to leave scope or debt unowned.

## Reconciliation log

- **2026-10-02 — an existing directory is not an empty start:** before template
  files are added, state what the project is. Files already present block
  copying this repository in as the starting tree. When those files have no
  git repository, say so, initialize git, and commit that tree first.
  Onboarding stays unfinished while the entrypoint still describes the
  checkout as this discipline template and the git remote is not this
  template's repository. When files are already present and the owner asks to
  start from this repository, ask before copying or refusing. A copied
  template claim is replaced in the learning ending. A rule change is written
  in the owning contract, and the entrypoint then keeps the pointer.
  - from: source[13], source[14], source[15]

- **2026-10-02 — learning assumes the current discipline missed the expectation:**
  a learning request starts from the mismatch between what the owner had to
  repeat and what the loaded rules caused. A filled policy or an earlier
  no-gap assessment is not evidence that the expectation was met. Ending with
  nothing to change requires that comparison.
  - from: source[12]

- **2026-10-02 — learning must survey every current rule and leave a result:**
  a learning request opens every current rule, records whether it applies,
  and ends by writing the settled changes, by stating that nothing needs to
  change together with the facts, or by listing changes whose method needs
  confirmation. Later tasks still open a rule when the work reaches it.
  Wholesale copy, enforcement, replacement of existing instructions, and
  product-code changes stay in the confirmation group. Personal context
  boundaries are unchanged.
  - from: source[11]

- **2026-09-25 — learning with optional personal context:** added an entry path
  distinct from formal migration, with source and visibility boundaries.
  Alignment and delegated context remain at their existing owners.
  [Change and verification](../plans/2026-09-25-personal-context-onboarding.md).
  - from: source[10] (2026-09-25 separate personal context and public method)

- **2026-09-14 — maintainer adoption account recorded:** the maintainer reported
  completed greenfield and brownfield adoptions. This replaces the blanket
  no-real-project note with a qualified account; independent adoption remains
  unproven and underlying records are not public.

- **2026-09-10 — provenance limits applied to learning:** distinguished direct
  records from later quotations and behavior changes from intent or outcome
  claims. Learning now checks target applicability and existing coverage;
  decision attribution routes to its development owner. The
  [learning record](../plans/2026-09-10-reference-feedback-learning.md#progress-and-closure)
  records verification and limits.
  - from: source[9]

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
