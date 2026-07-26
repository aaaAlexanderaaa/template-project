---
doc_type: guide
status: current
authority: guidance
last_reconciled: 2026-07-26
---

# AI-guided project onboarding

## Purpose

Adopt this repository's governance in a greenfield or running project without
mistaking template content for project truth, overwriting existing authority,
or turning onboarding into an unbounded cleanup program.

The normative behavior is defined by the
[project adoption contract](../contracts/project-adoption.md) and the
[governance decision boundary](../contracts/governance-decision-boundary.md).

## Preconditions

- An adopting human owner is available to confirm scope, profile, priority
  authority, and risk acceptance.
- The AI or contributor has read-only access to the target repository and its
  existing project-control sources.
- Active incidents, releases, migrations, and destructive operations are known
  before governance files are changed.
- Existing changes and local instructions will be preserved.

## Procedure

### 1. Classify the adoption

- **Greenfield:** no product implementation or established project authority.
  Use the template as the starting repository, establish current structural
  authority, select the initial managed boundary, then begin implementation.
- **Brownfield:** existing code, decisions, workflows, or delivery obligations.
  Begin with an `observed` read-only assessment and use staged enforcement.

### 2. Inventory before proposing

Inspect, without rewriting:

- architecture, modules, services, persistence, and source roots;
- READMEs, ADRs, contracts, tickets, plans, and agent instructions;
- tests, CI, deployment, rollback, observability, and incident procedures;
- product/direction owner, priority source, maintainers, and risk authority;
- active work, release commitments, known debt, and unresolved conflicts.

Do not infer authority from recency or file length. Mark facts, unknowns, and
conflicts separately.

### 3. Create the adoption assessment

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

### 4. Declare the confirmed decisions in `docs-policy.toml`

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
- **Severity.** Time-based findings — overdue targets and promises, expired
  pending evidence — are advisory by default. Run `--strict` on a schedule
  rather than promoting them on every push. A rule you set to `off` stays off
  even under `--strict`.

Unknown keys in `[adoption]` and `[severity]` are rejected rather than ignored,
so a typo or a setting from an older revision of the template surfaces as a
failure with the replacement named.

### 5. Separate current and target state

Describe the current system in `ARCHITECTURE.md` only when it is verified. Put
future behavior in target contracts and active plans. Do not make architecture
look clean by deleting evidence of current debt or by copying aspirational
template prompts into current authority.

### 6. Plan one bounded migration

Use [implementation-plan.md](../../templates/implementation-plan.md) for the
first managed boundary. A brownfield adoption normally moves through:

1. `observed` — read-only facts and conflicts;
2. `baselined` — profile, scope, authority, and historical debt confirmed;
3. `scoped_enforcement` — selected boundaries are contractually and
   mechanically governed;
4. `adopted` — every agreed adoption outcome has evidence.

Historical debt does not automatically block unrelated delivery. New work must
not silently expand a baseline debt class.

### 7. Reconcile entrypoints

Update root and local `AGENTS.md`, contributor guidance, architecture ownership,
source roots, CI entrypoints, and applicable contracts for the selected scope.
Preserve or supersede existing instructions explicitly; never assume copied
template files outrank project-specific authority.

## Verification

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
- [AI agent execution discipline](../contracts/agent-execution-discipline.md)
- [Project operation after onboarding](project-operation.md)
