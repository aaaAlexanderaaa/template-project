---
doc_type: plan
status: completed
authority: planning
last_reconciled: 2026-09-07
implements: [docs/contracts/agent-execution-discipline.md, docs/contracts/development-discipline.md, docs/contracts/governance-decision-boundary.md, docs/contracts/foundational-runtime-discipline.md, docs/contracts/documentation-harness.md]
supersedes: []
---

# Make execution proportionate to consequences

## Cold-start summary

The maintainer approved the preceding adjustment proposal, then authorized
implementation with English edits. English rendering of the accepted scope:
narrow high-risk triggers; allow bounded, low-impact new behavior to use a
lightweight delivery route; correct overgeneralized time and demonstration
policies; and keep the goal, reliable facts, authority, boundaries, and
completion evidence easy to locate. Read specific methods for the task and
history for a dispute, provenance question, or recovery need.

The earlier suggestions about global prompting quotas and mandatory frontend
design passes were not selected. Preserve those unrelated boundaries. The
language instruction selects English for edits; it does not establish an
empirical claim about relative model performance across languages.

Baseline: `ca8b29c7c0f0bb909dc548166599f9b29529edfd`, initially clean worktree;
Python 3.14.2. Current authority: [execution risk and routing](../contracts/agent-execution-discipline.md#risk-selects-the-execution-depth),
[delivery contracts](../contracts/development-discipline.md#contract-before-material-delivery-evidence-before-certainty),
[authorized execution](../contracts/governance-decision-boundary.md#delegated-engineering-work-proceeds-by-default),
[runtime policy](../contracts/foundational-runtime-discipline.md#time-and-calendar),
and [task context](../README.md#task-context).

## Risk and authorization

High-risk under the current profile: these reusable rules govern future
authorization, risk classification, and delivery. Use independent design
review and a fresh completion context under the current requirements; the
proposed rules cannot waive this task's review. Review checkpoints are execution
work within the authorization, not serial requests for human approval.

Root owns all edits. Reviewers are read-only and receive this request rendering,
the accepted proposal, governing sources, and baseline rather than root's
reasoning history. No other repository write workstream is registered.

## Complete end state

- Execution keeps three profiles. Consequences and recovery cost select risk;
  architecture or behavior keywords alone do not require high-risk review.
  Small changes to isolation or authorization still require it. Unknown
  technical impact is investigated, never silently assumed low.
- Routine can include authorized low-impact new behavior within an existing
  owner, with bounded effects and credible verification, without a standalone
  plan. Update the existing behavior contract before implementation. Published
  interface changes, durable-state semantics, substantive cross-owner coordination,
  migrations, or substantial recovery/dependency work require material delivery
  at minimum; high-risk consequences override convenience.
- Time policy identifies its scope and storage/calculation/display/input roles.
  Explicit per-tenant or per-object zones are valid. Check conformance to the
  declared policy rather than requiring every runtime setting to be identical.
- Demonstration data declares its temporal promise. Current-day scenes need
  freshness; labeled historical or fixed-reference scenes can retain dates.
  Refresh and retention follow the selected strategy while retaining write
  isolation, allowlisted scope, repeat safety, and recovery.
- AGENTS routes the five task facts and hard constraints without a second fact
  store. Current owner sections precede optional methods and historical
  explanation; handoffs carry actionable facts plus current source links.
- Templates, current guides, architecture prompts, entrypoints, and focused
  guards agree with the owning rules. Existing headings are retained where
  useful; renamed headings have their live incoming references reconciled.

## Execution and verification

1. Obtain independent design perspectives and synthesize findings here before
   changing normative owners or dependent templates.
2. Reconcile the owning contracts and documentation context owner; then
   update their direct projections and templates. Keep one rule owner and avoid
   a new risk engine, policy registry, template family, or universal size quota.
3. Replace the test that freezes the single-zone solution with focused routing
   checks. Use structural fixtures only for mechanical promises; validate
   classification and policy suitability through independent scenario review.
   The current source-citation checker counts only citations after the source
   block, forcing provenance ahead of operative rules. Reconcile the harness
   contract and count citations outside that block regardless of order; retain
   dangling, unused, duplicate, and date checks. Cover front, middle, and end
   placement plus invalid references and self-citation before moving the
   selected contract/template source blocks behind their operative sections.
4. Run the full Python suite, normal and strict documentation checks, and
   whitespace validation; correct failures. Complete fresh-context review,
   reconcile all affected lifecycle states, and close this plan.

| Scenario / claim | Expected outcome | Evidence |
|---|---|---|
| Local list sorting with no persistence, permission, or public interface change | Routine; existing behavior owner updated; relevant effects verified; no standalone plan | Independent reading of entrypoint through owner and copied forms |
| One-line tenant-isolation or authorization change | High-risk despite small diff or easy code rollback | Independent classification and counterexample review |
| Coordinated cross-service interface migration | Material at least, with compatibility/recovery plan; high-risk when consequences warrant | Independent classification review |
| Per-tenant settlement zones | Explicit scope and roles represent the requirement without a global single-zone exception | Runtime/template walkthrough |
| Host defaults silently interpret business input | Policy violation remains observable | Negative policy walkthrough |
| Dynamic today scenes versus labeled historical examples | Different freshness policies; safe writes and repeat behavior preserved | Runtime/template walkthrough |
| Fresh task context | Goal, facts, authority, boundaries, and completion evidence reachable without loading history | Fresh-context reviewer trace |
| Existing mechanical integrity | Required templates, citations, lifecycle, and adoption gates continue to work | Python suite and checker results |

These reviews verify reusable guidance and representative decisions, not a
deployed multi-tenant runtime or a measured improvement in agent efficiency.
Real adopter effectiveness remains partial.

## Progress and closure

- Planning and coordination: root recorded authorized scope and baseline;
  independent design review pending. No normative or implementation edit yet.
- Baseline suite: 114 tests passed in 15.286 seconds on Python 3.14.2.
- Design contexts: `/root/execution_design_review` reviews execution and context;
  `/root/runtime_design_review` reviews runtime policy. Both are read-only and
  use the three required lenses. Root will synthesize before implementation.
- Initial review attempts failed due to workspace credits; after the maintainer
  requested continuation, both independent contexts completed on September 7.
- Design synthesis: both reviewers found the proposal suitable. Root accepted
  all required refinements: classification does not grant authorization;
  recovery includes external effects; all published interface changes are
  material at least; substantive ownership coordination is distinct from file
  count; applicable concerns and exceptions survive the lightweight route.
  Time policy resolves scope and roles, including dynamic absence and explicit
  user-local presentation; instant persistence is distinct from civil types.
  Demo verification checks dates and labels, with repeat/retention and mutation
  safeguards even for historical regeneration. Source-order independence must
  exclude self-citation and leave surface translation checks unchanged.
- Root began normative reconciliation after the reviewers' suitability findings.
  All repository edits remain root-owned; reviewers made no file changes.
- Shared surfaces reconciled: the five contracts, documentation context owner,
  root entrypoints, architecture prompts, current guide projections, affected
  templates, and source-citation checker/tests. Cross-stack routing already
  links the shared owners and required no specialized runtime table. Template
  inventory and adoption settings remain applicable without configuration edits.
- Source regression: middle/end source placement failed under the old checker,
  and a dangling citation before definitions incorrectly passed. The revised
  checker passes all 16 source-related tests, including self-citation and
  definition-validation cases. One initial invalid-date fixture expectation was
  corrected to the existing diagnostic; it was not an implementation defect.
- Implementation verification: 118 tests passed in 16.141 seconds on Python
  3.14.2; normal/strict documentation checks passed (28 canonical documents,
  15 selected templates), and `git diff --check` passed. A current-section scan
  found no remaining single-zone, mandatory clock-relative-demo, or
  no-new-semantics statements in the affected live rules.
- Fresh completion context `/root/completion_review` is reviewing the diff and
  scenarios. Root announced and added a material fallback for delivery outside
  routine conditions after investigation, and clarified that explicit owner
  review requirements remain binding. No code or test logic changed after the
  full suite; the final review result is recorded below.
- Independent completion review: `/root/completion_review` received original
  maintainer wording, the accepted scope, current files, and the baseline diff
  without producing the design or implementation. It found no actionable
  defects across system consistency, user/operator outcomes, and maintenance.
  Every scenario in the matrix resolved as intended. Additional negative cases
  confirmed that unrequested sorting is not authorized by a routine label,
  unknown impact requires investigation, and explicit owner review obligations
  remain binding. The review found no need for another human decision.
- Fresh-context observation: the reviewer followed AGENTS to the five task
  facts, then request/baseline, governance authority, architecture and owner
  boundaries, execution depth, and completion evidence. Runtime and checker
  methods were read because this task activated them. Historical provenance
  and a prior handoff chain were not needed for the scenario decisions.
- Independent checks: five surface-citation/template regressions passed in
  0.613 seconds, and whitespace validation passed. The reviewer inspected the
  source fixtures and confirmed that surface validation was unchanged; it
  relied on root's reported full-suite and checker results instead of claiming
  to have rerun them.
- Provenance and projections: read-only comparisons against the baseline
  confirmed preservation of all prior source-block content in the seven
  reordered files, with operative rules before each source heading. Both
  current guide projections were reconciled; no historical record was rewritten
  to present an old policy as current. New and revised prose is English;
  preserved original stakeholder quotations retain their source language.
- Completion: the approved template adjustment is implemented and independently
  reviewed in the working tree based on the baseline above. This plan is
  completed and leaves the active read set. No commit or deployment was made.
  Real-adopter effectiveness and deployed-runtime correctness remain unproved;
  the relevant disciplines retain their partial verification status.
