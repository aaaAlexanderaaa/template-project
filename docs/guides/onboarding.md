---
doc_type: guide
status: current
authority: guidance
last_reconciled: 2026-09-27
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
- The AI or contributor has read-only access to the target repository and its
  existing project-control sources.
- Active incidents, releases, migrations, and destructive operations are known
  before governance files are changed.
- Existing changes and local instructions will be preserved.

## Procedure

### Start collaborating without a migration

For a request to learn the discipline and use supplied personal context,
follow [the bounded entry path](../contracts/project-adoption.md#learning-and-personal-context-have-a-bounded-entry-path):

1. Read the source template's working agreement and transfer-value order.
   Inspect the target's own entrypoint, current work, and boundaries relevant
   to the task. An existing project keeps its current owners; an empty one
   supplies no facts merely by resembling this template.
2. If personal context was supplied, read its onboarding entrypoint. Use its
   collaboration background and decision preferences where they matter;
   follow its reading conditions for deeper material. Keep it at its supplied
   private location. If unavailable, state the missing source and continue
   work that does not depend on it.
3. Use [the alignment route](../contracts/governance-decision-boundary.md#missing-knowledge-is-routed-not-automatically-escalated)
   to investigate facts and resolve only choices that change the outcome.
   Preserve useful design freedom in an open-ended brief. For a clear task,
   proceed directly within existing authorization.
4. Carry relevant decisions and reasons into an assignment under
   [bounded delegation](../contracts/agent-execution-discipline.md#delegated-work-carries-bounded-context-and-returns-to-an-owner).
   Retain session state or an existing private locator for later use; do not
   commit a profile or its private path to create a permanent startup hook.

Onboarding is sufficient when the agent can explain the current outcome,
applicable authority, material preferences or unknowns, and the next action.
Give a concise account of consequential choices or conflicts; no adoption
report, policy manifest, interview, or migration is needed for learning alone.
Continue the task already requested. If the request was only to onboard,
report readiness and material unresolved items without inventing product work.

For example, an existing service with established architecture and a known
local defect keeps those commitments and receives the bounded fix. A new
product with an unclear audience first resolves that choice because it changes
the design. A worker checking a parser needs its input/output and failure
contract; a reviewer judging a product experience also needs the original user
goal and the relevant accepted trade-offs.

For explicitly authorized standing autonomy, also read the
[autonomous operation contract](../contracts/autonomous-operation-discipline.md).
Before unattended expansion, exercise independent review dispatch and its
unavailable-review behavior in the actual harness. Merely loading these files
does not supply a scheduler, a fresh context, or enforced review due state.

The steps below apply when the user requests formal adoption or enforcement
changes. They are not prerequisites for the learning route above.

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

### 2. Classify the adoption

- **Greenfield:** no product implementation or established project authority.
  Use the template as the starting repository, establish current structural
  authority, select the initial managed boundary, then begin implementation.
- **Brownfield:** existing code, decisions, workflows, or delivery obligations.
  Begin with an `observed` read-only assessment and use staged enforcement.

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
harness_paths = ["scripts"]     # tooling that is not product code
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
  of them, the check names the paths rather than passing on nothing. Files
  directly in the repository root are never counted, so `setup.py`,
  `conftest.py`, and `vite.config.ts` need no entry. For a tooling directory,
  add it to `harness_paths`, which accepts glob patterns such as `tools/**`.
- **Profile** decides the template inventory, and tiers are cumulative. A small
  project selects `minimal` and may delete the templates it will never fill in;
  documentation that still references a deleted template becomes an advisory,
  not a build failure.
- **Severity.** Review signals that should not fail an unrelated change by
  default are advisory. Run `--strict` on a schedule rather than promoting them
  on every push. A rule you set to `off` stays off even under `--strict`.

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

For learning and personal-context onboarding, verify the relevant source was
actually read, the target's authority was preserved, private material stayed
within its permitted audience, and the next action follows the agreed task.
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
entrypoint changed during adoption.

## Related authority

- [Documentation authority map](../README.md)
- [Development discipline](../contracts/development-discipline.md)
- [Foundational runtime](../contracts/foundational-runtime-discipline.md)
- [AI agent execution discipline](../contracts/agent-execution-discipline.md)
- [Project operation after onboarding](project-operation.md)
