---
doc_type: guide
status: current
authority: guidance
last_reconciled: 2026-11-01
projection_of: [docs/contracts/project-adoption.md, docs/contracts/governance-decision-boundary.md, docs/contracts/documentation-harness.md, docs/contracts/foundational-runtime-discipline.md, docs/contracts/agent-execution-discipline.md, docs/contracts/autonomous-operation-discipline.md]
---

# AI-guided project onboarding

## Purpose

Learn applicable practices and begin collaboration in a new or running
project. When governance adoption is requested, carry out a bounded migration
that preserves existing authority. Separately supplied personal context can
inform decisions without becoming public project content.

The normative behavior is defined by the
[project adoption contract](../contracts/project-adoption.md) and the
[governance decision boundary](../contracts/governance-decision-boundary.md).

## Preconditions

- The task's current authorization is known. In a formal migration, unresolved
  scope, profile, priority authority, or risk acceptance needs its human owner;
  an existing instruction may already settle those choices.
- Formal adoption inventory is read-only until the owner confirms scope and
  method. Learning may write its judgment and other changes whose method does
  not need a further decision, and needs write access for that ending.
- Active incidents, releases, migrations, and destructive operations are known
  before governance files are changed.
- Existing changes and local instructions will be preserved.

## Procedure

### Read source rules before deciding what to change

- required-reading: [Understand rules before judging applicability](../contracts/project-adoption.md#understand-rules-before-judging-applicability)

Start external learning at [the adoption owner's reading order](../contracts/project-adoption.md#understand-rules-before-judging-applicability).
For broad learning, adoption, upgrade or discipline restructuring, obtain the
complete learning set below. Read each rule's operative source and dependencies
and understand its problem, mechanism and limits before judging applicability.
Keep a missing explanation unresolved and follow relevant source evidence when
needed. A title, value tier or apparently familiar local rule cannot do that
comparison. Reading does not install the template or change local authority.

| Target project | What changes after source understanding |
|---|---|
| Empty start | Establish project purpose and owners, then choose what to adopt for its actual work. |
| Older discipline | Compare the current local rules and exceptions with the newly understood source; preserve valid local decisions during an authorized upgrade. |
| Independently developed discipline | Map each mechanism to existing coverage, a concrete gap or an evidenced reason it does not apply. Equivalent local coverage needs no duplicate source rule. |

For example, a service with no UI still reads the source learning set before
classifying the graphical frontend rules. The source's graphical scope and
the observed absence of a graphical surface support non-applicability; the
filename alone does not. It separately checks the non-graphical Experience
requirements for its CLI. This comparison authorizes no UI implementation.

### Start collaborating without a migration

For a narrow practice request or method inquiry within an authorized concrete
task, use the
[bounded extraction route](../contracts/project-adoption.md#take-one-practice-into-an-authorized-task)
and [operation card](project-operation.md#take-one-practice-into-a-task).
The implementer can locate a candidate; the owner need not name it. Read and
understand its source before deciding its fit. A broad learning or
discipline request keeps the full survey below; it cannot silently become a
single-practice extraction. Neither route requires invented prior corrections.

The [complete-reading route](../README.md#task-context) can deliver declared
units and dependencies. The learning request below keeps its wider, explicitly
required set: obtain every named rule, using direct whole-owner reading where
needed. A task preparation manifest alone does not complete that comparison.

For a request to learn the discipline and use supplied personal context,
follow [the bounded entry path](../contracts/project-adoption.md#learning-and-personal-context-have-a-bounded-entry-path).
For corrective learning, find what the owner had to repeat and what the loaded
rules caused. First-time learning compares the current expectation and baseline;
keep missing historical evidence unknown. A filled policy, a
declared stage, or an earlier assessment that reported no gap is not that
finding. Open every rule that path names. A title or a link is not enough. Plans,
evidence, and source chronology stay closed unless a judgment depends on them.

The set is the documentation authority map, including language style; every
current contract (development discipline, governance, adoption, agent
execution, the documentation harness, foundational runtime, data analysis and
autonomous operation); the engineering-judgment contract, recorded as a target
draft;
every row of development discipline's concern table, followed into the section
that owns that row; and the behavior guides for onboarding, project operation,
research, information access, and Grill.

Inspect the target's own entrypoint, current work, and boundaries. An existing
project keeps its current owners; an empty one supplies no facts merely by
resembling this template. If personal context was supplied, read its onboarding
entrypoint and follow its reading conditions. Keep it at its supplied private
location. If unavailable, state the missing source and continue work that does
not depend on it. Use
[the alignment route](../contracts/governance-decision-boundary.md#missing-knowledge-is-routed-not-automatically-escalated)
for choices that change the outcome. When work is handed on, carry the
relevant decisions under
[bounded delegation](../contracts/agent-execution-discipline.md#delegated-work-carries-bounded-context-and-returns-to-an-owner).
Do not commit a profile or its private path to create a permanent startup hook.

For each opened rule, record one result: it applies and is already satisfied;
it applies and is not yet satisfied; or it does not apply, with the repository
fact that makes that so. Use the rule's reason and actual local coverage to
support consequential judgments. "Not triggered" without that fact is not a
result; a similar local heading does not establish equivalent coverage.

Learning ends in one of these ways. A session may both write and ask:

1. The repository contains the judgment and the changes whose method did not
   need a further decision. Say what changed. Write the judgment in the
   existing agent entrypoint, and change the contract that owns each changed
   rule. The entrypoint names the rule, the result, and the contract section.
   It does not paste that section or a second copy of a product fact. After
   the contract holds the rule, the entrypoint keeps the pointer. If there is
   none, add one that carries the judgment and leaves other instructions
   untouched. A copied claim that this checkout is the engineering discipline
   template is not an existing instruction; replace it here with what this
   project is.
2. Nothing needs to change. Say so. Name the rules that apply and are already
   satisfied, and give the repository fact for every rule that does not apply.
   Use this only after the comparison with the owner's expectation, and only
   when no applicable rule is unsatisfied. A filled policy file is not that
   comparison.
3. Some changes need a decision about method. List each change and the
   intended method, and wait. Copying this template wholesale, enabling
   enforcement, replacing existing instructions, and changing product code
   are in this group.

Finishing in conversation alone, while a change in the first group is still
unwritten, is not learning. Before that ending, state what the project is.
When the ending will write a file into a directory that already holds files
and is not a git repository, initialize git and commit those files first. If
git cannot be initialized, stop adding files and tell the owner. No adoption
report or migration is required for learning. Continue a product task the
owner already requested after the ending. Learning does not start a
product-code change. If the request was only to learn, stop at that ending.

For example, an existing service with established architecture keeps those
commitments. A known local defect that the owner has not already requested is
listed with the intended method and waits. A new product with an unclear
audience first resolves that choice because it changes the design. A worker
checking a parser needs its input/output and failure contract; a reviewer
judging a product experience also needs the original user goal and the
relevant accepted trade-offs.

For explicitly authorized standing autonomy, also read the
[autonomous operation contract](../contracts/autonomous-operation-discipline.md).
Before unattended expansion, exercise independent review dispatch and its
unavailable-review behavior in the actual harness. Merely loading these files
does not supply a scheduler, a fresh context, or enforced review due state.
Use the existing task/checkpoint owner for execution continuity and relevant
experience locators. When claiming that the adopted workflow retains learning,
observe a fresh continuation finding and applying it, including a changed
condition that requires revision. This is evidence for the claim, not a new
recording system or an extra approval phase.

The assessment, stage, and enforcement steps below apply when formal adoption
or enforcement is requested. They are not prerequisites for learning. The
project statement, and the git commit before a write, are part of learning.

### Keep reasoning usable in the next project

Use [essential reasoning](../contracts/development-discipline.md#keep-essential-reasoning-active)
and [repeated transfer](../contracts/project-adoption.md#invariants-survive-repeated-transfer)
when turning a learned practice into local instructions. Keep a concise account
of what the next executor needs to notice before selecting a method. Preserve
its reason, scope, exceptions and unresolved status, with detailed owners
available through the normal entrypoint. A slogan such as "think critically"
does not tell the executor what should change.

For example, a source may teach that a passing checklist has limited coverage.
Translating that to "always complete the checklist" loses the reason. The local
instructions should still let an executor investigate an unexpected user failure
outside the listed categories. Likewise, "retain lessons" must not become a
claim that a recorded remedy was applied or effective. Open subagent discovery
is another application; it does not define this practice's scope.

Exercise the route being claimed: source guidance to the learner's local
instructions, then those instructions to a fresh executor's decision or action.
Give the executor the local material it would actually receive, without the
source author's explanation or a list of expected answers. Keep the intermediate
artifact unchanged and inspect the result against the original purpose. Where
relevant, vary the task or working condition so recognition is tested beyond
the teaching example. A required source that cannot be opened is a missing
dependency, not permission to improvise it.

If the next executor misses the point, locate the first loss or misleading
condition and fix that owner. Preserve the failed attempt and any intervention.
Use the existing task evidence, including its unresolved disposition and
permitted next step. Further generations, real operation and sustained effect
remain unverified until observed; no fixed number of copies proves them.

### 1. Orient by transfer value

Before selecting files or enforcement mechanisms, use [project-adoption § transfer-value-order](../contracts/project-adoption.md#transfer-value-is-ranked-before-its-carriers)'s
base order:

`interaction and epistemic discipline` → `truth, ownership, and boundaries` →
`delivery discipline` → `activated domain disciplines` → `carriers and tools`.

This order allocates attention; it does not change document authority or require
wholesale adoption. Inspect the target before final selection: an activated UI,
state, security, reliability, data, or other boundary promotes its applicable
discipline. Learning and adoption draw from the same values, while any write or
enforcement change remains subject to the target project's authority.

Within the first tier, weigh external material by authorship ([adoption § authorship-triage](../contracts/project-adoption.md#external-material-is-triaged-by-authorship-before-adoption)) before it
informs any selection: inspect original decision records where available,
retain the limits of later quotations, and use machine-generated narrative as
a lead to verify. Compare each lesson's mechanism with the target's existing
owners and coverage before adopting it; source vocabulary and approval labels
do not become target policy by copying them.

### 2. Say what the project is, then classify

Before a class label and before any copy, state what this project is. Name
the material already in the directory, the use the owner has given it, and
what is absent. A class label does not replace that statement. In the
adoption contract, an empty start is called greenfield and an already-running
project is called brownfield. Either name only classifies the directory.
[The existing-directory rule](../contracts/project-adoption.md#an-existing-directory-is-described-before-template-files-are-added)
owns it.

A directory that already contains files is not an empty start. No product
code, no agent entrypoint, and no contract do not make it empty. When those
files are present and the owner also asks to start from this repository, stop
and ask whether to copy. Do not copy, and do not treat the request as already
refused.

When those files are present and the directory is not a git repository, say
so in the same account. Initialize git and commit the current files as the
first revision before adding any template file, and before a learning ending
writes a file there. If git cannot be initialized, stop adding template files
and tell the owner.

Onboarding is unfinished while `AGENTS.md` still treats this checkout as the
engineering discipline template and no git remote is
https://github.com/aaaAlexanderaaa/template-project. Any one of these claims
is enough: this repository is the engineering discipline template; its work
is documentation and project discipline; onboarding into any other checkout
is unfinished while the entrypoint still says this; a task is to learn this
template; a task is adoption into another project. A checkout with no remote
is unfinished. Finishing replaces those claims with what this project is,
without a separate confirmation of method. Where the directory is a git
repository, the checker reports any remaining claim.

- **Empty start:** the directory has no files. This repository is then the
  starting tree. Establish current structural authority, select the initial
  managed boundary, then begin implementation.
- **Already running:** the project has code, decisions, workflows, or delivery
  obligations. The adoption contract calls this brownfield. Begin with an
  `observed` read-only assessment and use staged enforcement.
- A directory that already holds data, notes, or other owner files, and is
  not a running product, still gets the statement above. It is not an empty
  start.

### 3. Inventory before proposing

Inspect, without rewriting:

- architecture, modules, services, persistence, and source roots;
- implicit clocks, timezones, civil-date rules, and any seed or demo dataset
  operators or customers can see;
- style layers, shared visual values, theme mechanisms, and existing override
  debt, where the project has a frontend;
- READMEs, ADRs, contracts, tickets, plans, and agent instructions;
- tests, CI, deployment, rollback, observability, and incident procedures;
- product/direction owner, priority source, maintainers, and risk authority;
- active work, release commitments, known debt, and unresolved conflicts.

Do not infer authority from recency or file length. Mark facts, unknowns, and
conflicts separately.

### 4. Create the adoption assessment

Copy
[adoption-assessment.md](../../templates/adoption-assessment.md) into
`docs/evidence/YYYY-MM-DD-adoption-assessment.md`. Complete it from verified
repository evidence rather than chat memory.

The human owner confirms:

- project-defined governance profile;
- managed paths and boundaries;
- explicit exclusions;
- authoritative priority source;
- immediate rules versus advisory rules;
- current adoption stage.

### 5. Declare the confirmed decisions in `docs-policy.toml`

The harness reads the owner's decisions instead of assuming one project shape.
Set these before running the check for the first time:

```toml
[adoption]
stage = "observed"              # or baselined / scoped_enforcement / adopted
source_roots = ["app", "lib"]   # the project's real layout
harness_paths = ["scripts", "setup.py", "*.config.*"] # declared tooling
managed_paths = []              # in scoped_enforcement: the governed boundaries

[templates]
profile = "minimal"             # or standard / full
```

Consequences worth knowing before you choose:

- **Stage** decides whether adoption gaps block. `observed` and `baselined`
  report them and still exit zero, so a running project can put the check into
  CI on day one — including before the source roots are right. Getting the
  layout wrong at an early stage produces a report, not a red build.
  `scoped_enforcement` and `adopted` block.
- **Source roots** decide what "product code" means. If code exists outside all
  of them, the check names the paths rather than passing on nothing. This
  includes root application files: `source_roots = ["main.py"]` declares one
  and activates the adoption gates. Declare actual build/tooling paths in
  `harness_paths`, including root files and glob patterns such as `tools/**`.
- **Profile** decides the template inventory, and tiers are cumulative. A small
  project selects `minimal` and may delete the templates it will never fill in;
  documentation that still references a deleted template becomes an advisory,
  not a default build failure. The retained test command explicitly skips
  optional-template cases while continuing the general infrastructure tests.
- **Severity.** Review signals that should not fail an unrelated change by
  default are advisory. Run `--strict` on a schedule rather than promoting them
  on every push. A rule you set to `off` stays off even under `--strict`.

  `rule_phrasing` is off by default; set it `advisory` to list disclaimer
  phrases in the startup rules. Most of them mark limits a rule keeps, so a
  finding asks for a judgment rather than a rewrite.
Unknown keys in `[adoption]` and `[severity]` are rejected rather than ignored,
so a typo or a setting from an older revision of the template surfaces as a
failure with the replacement named.

### 6. Separate current and target state

Describe the current system in `ARCHITECTURE.md` only when it is verified. Put
future behavior in target contracts and active plans. Do not make architecture
look clean by deleting evidence of current debt or by copying aspirational
template prompts into current authority.

If the project stores or shows date/time, or shows seed data to operators
or customers, name the owner in the `ARCHITECTURE.md` runtime prompts and
read [foundational runtime](../contracts/foundational-runtime-discipline.md).
Do not fill a catalog of historical pits. A brownfield inventory records an
implicit clock, zone resolution, or fixed demo dates as facts. Determine the
applicable scope and temporal promise before calling those values defects;
rewriting them is a separately authorized cutover.

### 7. Plan one bounded migration

Use [implementation-plan.md](../../templates/implementation-plan.md) for the
first managed boundary. A brownfield adoption normally moves through:

1. `observed` — read-only facts and conflicts;
2. `baselined` — profile, scope, authority, and historical debt confirmed;
3. `scoped_enforcement` — selected boundaries are contractually and
   mechanically governed;
4. `adopted` — every agreed adoption outcome has evidence.

Historical debt does not automatically block unrelated delivery. New work must
not silently expand a baseline debt class.

### 8. Reconcile entrypoints

Update root and local `AGENTS.md`, contributor guidance, architecture ownership,
source roots, CI entrypoints, and applicable contracts for the selected scope.
Preserve or supersede existing instructions explicitly; never assume copied
template files outrank project-specific authority.

Keep the root entrypoint short and route to task-relevant owner sections.
Preserve current requirements and exceptions; move completed work and supporting
chronology out of routine startup reading. The confirmed adoption scope remains
authorized through its implementation and verification. Internal checkpoints
do not require repeating that confirmation.

## Verification

For learning and personal-context onboarding, verify that every rule in the
learning set was opened, that each has one of the three results, and that the
session ended by writing the settled changes, by stating that nothing needs
to change together with the facts, or by listing the changes whose method
needs confirmation. Verify that existing instructions were left in place,
private material stayed within its permitted audience, and the next action
follows the agreed task.
Check a material preference against its source and context when relying on it;
mere agreement with a generated summary is not corroboration.

To test whether this route helps actual work, give a fresh agent a bounded
real task, the target's entrypoint, and the supplied sources without the
implementer's conversation. Observe the inputs it actually reads, what it
does, and where it needs help. Inspect the resulting artifact or action against
the original task. If it misreads intent or stalls, trace the failure to the
source, example, or missing context at that decision point and repair that
owner. Record the case and its limits; a hypothetical walkthrough or successful
link check does not establish real adoption. This can use the next authorized
task and creates no separate approval or universal benchmark gate.

For formal governance adoption:

- The assessment states what the project is: material already present, the
  use the owner has given it, and what is absent. A class label alone is not
  that statement.
- A directory that already held files was not treated as an empty start. If
  the owner also asked to start from this repository, the account shows the
  question and the owner's answer before any copy.
- If those files had no git repository, the account says so, and the first
  revision is that tree before any template file.
- The agent entrypoint states what this project is. If it still says the
  checkout is the engineering discipline template, a git remote is
  https://github.com/aaaAlexanderaaa/template-project.
- The assessment names evidence for every current-state claim.
- The adopting human confirmed profile, scope, priority authority, and stage.
- Current and target descriptions are visibly separate.
- Existing authorities are preserved or have explicit supersession links.
- The first managed boundary has a contract, plan, and verification path.
- The repository check passes for the scope claimed as enforced. At an early
  stage this means outstanding adoption work is reported rather than absent;
  it must not be satisfied by fabricating architecture or contracts.
- Remaining debt, exclusions, decisions, and higher adoption stages stay open.

Passing the checker proves structural validity, not semantic correctness or
project-wide adoption.

## Failure and recovery

- If product behavior is being rewritten during assessment, stop and create a
  separately authorized implementation plan.
- If copied template guidance conflicts with existing authority, keep the
  affected boundary `observed` or `baselined` and reconcile it.
- If adoption interrupts delivery disproportionately, narrow managed scope and
  preserve the residual gap instead of declaring false compliance.
- If transition evidence is later disproved, return to the last supported stage
  and record the evidence conflict.

## Safety and rollback

Onboarding is additive until a separately reviewed supersession or migration is
authorized. Do not delete existing documentation, tests, CI, deployment paths,
or tracker records as part of inventory. Keep a recoverable revision for every
entrypoint changed during adoption. When the directory already holds files and
has no git repository, that revision is the git commit of those files made
before any template file is added.

## Related authority

- [Documentation authority map](../README.md)
- [Development discipline](../contracts/development-discipline.md)
- [Foundational runtime](../contracts/foundational-runtime-discipline.md)
- [AI agent execution discipline](../contracts/agent-execution-discipline.md)
- [Project operation after onboarding](project-operation.md)
