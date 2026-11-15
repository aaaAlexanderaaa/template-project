---
doc_type: plan
status: completed
authority: planning
last_reconciled: 2026-07-28
implements: [docs/contracts/development-discipline.md, docs/contracts/governance-decision-boundary.md, docs/contracts/agent-execution-discipline.md, docs/contracts/documentation-harness.md]
supersedes: []
---

# Engineering harness enablement plan

## Cold-start summary

The governance framework prevents many unsafe or incoherent changes, but it can
still make an agent seek approval for reversible engineering choices, specify a
delivery contract before enough facts are known, and infer applicable quality
concerns from several documents. It also treats documentation primarily as an
incremental output, without a sufficiently explicit subtraction path or a way
to identify non-normative projections that may drift from their owner.

The authorized end state grants a positive engineering decision envelope,
introduces disposable controlled experiments, routes work through the smallest
applicable concern set, governs cross-cutting quality attributes through one
ownership model, and manages document stock without universal volume limits.

## Risk classification

- Profile: `high-risk`
- Rationale: changes the governance semantics used by every agent-driven change,
  including when implementation may proceed, when a contract is required, and
  which review lenses activate.
- Required independent review: one fresh design context before dependent
  implementation and one fresh holistic context after implementation. Reviews
  run serially because the available provider has a request-rate limit.
- Human authorization: the repository owner approved the complete scope on
  2026-07-28, including independent subagent review.

## Authority and prerequisites

- Structural authority: `ARCHITECTURE.md`
- Development owner: `docs/contracts/development-discipline.md`
- Decision authority owner: `docs/contracts/governance-decision-boundary.md`
- Agent route owner: `docs/contracts/agent-execution-discipline.md`
- Mechanical scope owner: `docs/contracts/documentation-harness.md`
- Documentation lifecycle owner: `docs/README.md`
- Existing implementation baseline: at revision
  `feat: govern style ownership and layering` (2026-07-27), run
  `uv run --python 3.11 python -m unittest discover -s tests -p 'test_*.py'`
  and `uv run --python 3.11 python scripts/check_docs.py`; command output, not a
  copied count, owns the inventory.

Activated concerns from development D8:

| Trait | Concern | Normative owner | Plan disposition |
|---|---|---|---|
| Public governance contracts change | Compatibility | Changed public semantics remain owned by development D1/D8, governance G6/G7, agent A2/A8, and harness H12 | Preserve published paths and invariant ids; update all known consumers in one cutover |
| Agent work selection and completion change | Experience | `docs/contracts/governance-decision-boundary.md` G6/G7 and `docs/contracts/agent-execution-discipline.md` A8 | Project the positive routes and defaults through entrypoints without adding conditions |
| Documentation metadata/checker changes | Dependency and build integrity | `docs/contracts/documentation-harness.md` H4/H9/H10/H12 | Write fixtures first and retain the contract's Python 3.11 standard-library boundary |
| Cross-document projections change | State integrity | `docs/contracts/documentation-harness.md` H12 | Implement its typed relationship, lifecycle compatibility, recovery, and advisory behavior |

Independent review is not a D8 concern. The `high-risk` classification above
activates A1/A3/A4; the review topology below records its serial design and
final contexts.

Security/privacy, product-runtime performance, persistence migration, and
production rollout are not activated by this documentation-harness change.

## Complete end state

An agent can select one of four routes without synthesizing several rule sets:

1. routine bounded delivery with no new governance artifact;
2. controlled experiment for a missing technical fact;
3. material delivery with only the concerns triggered by the change;
4. high-risk delivery with the triggered specialist lenses and independent
   evaluation.

The governance boundary positively authorizes reversible local implementation
choices. The development contract owns one concern-trigger table and one
quality-attribute ownership model. Templates collect only activated concerns.
Root entrypoints route to those owners instead of reproducing their full rules.

Documentation growth has a lifecycle: update an existing owner before creating
a new document; merge still-live decisions; summarize only when history has
lasting value; retire completed, historical, superseded, and disposable work
from the active read path. No checker uses document count, length, or blanket
retention age as a quality or deletion proxy; explicit lifecycle review
deadlines remain. Current canonical guide projections declare `projection_of`
to current normative contract or surface owners. A later-dated source
reconciliation produces an advisory review signal rather than automatic
failure; same-day edit order remains outside the date-based proof.

## Current state and gap

| Concern | Current fact | Gap |
|---|---|---|
| Agent autonomy | Blocker classes are narrow | No equally explicit positive engineering discretion |
| Learning under uncertainty | Investigation is read-only before a contract | No safe implementation experiment before delivery intent is known |
| Applicability | Risk profiles and many stack-specific rules exist | No single concern router that derives the smallest obligation set |
| Quality attributes | Functional, UI, failure, and selected backend properties are covered | Performance/capacity, security/privacy, reliability, cost, dependency integrity, and production learning have no shared ownership form |
| Defect guards | Every defect asks for a sibling guard | No proportional exit when no repeatable mechanism or worthwhile guard exists |
| Document stock | Lifecycle states and supersession exist | Creation is explicit; merging, synthesis, active read-set removal, and disposal are weak |
| Document coupling | Authority order and links exist | Purpose-specific projections can drift without declaring their owner |

## Seven-phase execution loop

| Phase | Required output | Applicability or evidence |
|---|---|---|
| 1. Domain and authority | Current contracts, checker, templates, and entrypoints reviewed | Complete; contract owners listed above |
| 2. Fixture or controlled boundary | Repository-copy checker fixtures | Existing deterministic fixture harness applies |
| 3. Contract and design | Four updated contracts, authority-map stock rules, and this plan | Complete; initial failure reconciled and serial re-review passed |
| 4. Test first | Projection, lifecycle, and template-routing failures observed | Complete; new negative fixtures failed before implementation |
| 5. Implementation | Checker, templates, architecture skeleton, guides, and compact entrypoints | Complete |
| 6. Regression | Full fixtures, repository check, strict check, whitespace and scoped audits | Complete; all commands and duplication audit pass |
| 7. Holistic evaluation | Fresh-context verdict plus document subtraction/coupling audit | Complete; final independent verdict `PASS` |

## Work-selection fallback

The named work remains executable. If one implementation path blocks, continue
only unaffected tasks already authorized here. Newly discovered governance
features remain recommendations; they are not added to this plan merely because
they are adjacent.

## Review topology

| Stage | Required lenses/context | Reviewer identity | Result or blocked reason |
|---|---|---|---|
| Self-design | Contract consistency, agent/operator efficiency, maintenance and document stock | Primary implementation context | Complete; draft contracts landed |
| Independent design | Same inputs without implementation reasoning trace; include anti-bloat and coupling risks | isolated serial design-review context, run alone | Initial `FAIL`; reconciled serial re-review `PASS` |
| Synthesis | Reconcile independent findings against owner-approved outcome | Primary context after review | Complete; eight original and two residual findings incorporated |
| Final | Fresh-context six-dimensional evaluation and stock/coupling audit | isolated holistic-evaluation context, run alone | Initial failures corrected; final `PASS` with no high/medium findings |

Human governance exception: none. A provider rate limit changes review
scheduling, not the required independence.

## Documentation ownership and stock impact

No new normative contract or guide is created. This active plan has a distinct
execution lifecycle and will become `completed`. High-risk design and final
evidence require separate durable records because they support different claims
and contexts; each will become `historical` after closure.

Existing completed plans are not rewritten. Entrypoint duplication will be
reduced where the new rule owner is clear. The final audit records documents
merged, shortened, retired, or deliberately retained, with reasons rather than
volume targets.

Implementation subtraction result: no existing canonical document was merged
or retired because each still owns a distinct bounded context. The only new
records are this execution plan and the design/final evidence required by the
high-risk claim. Root entrypoints and reusable templates were shortened or
routed where they had copied normative semantics; both current guides now
declare their exact projection owners. Completed historical plans remain
unchanged and outside the active read set.

### Coupling and subtraction inventory

This inventory owns the intended treatment of every current guide, root
entrypoint, and reusable template in scope. It is a review record, not a text
similarity or document-volume gate.

| Document | Existing coupling | Intended treatment |
|---|---|---|
| `docs/guides/onboarding.md` | Restates adoption stages, severity, and authority behavior | Declare projections to project-adoption, governance, and documentation-harness contracts; retain procedure-specific consequences |
| `docs/guides/project-operation.md` | Restates decision, execution, guard, and completion rules | Declare projections to governance, development, and agent-execution contracts; replace the copied execution sequence with route links and operator procedure |
| `docs/guides/README.md` | Routes guide selection | Retain as a compact non-canonical index; no projection metadata |
| `README.md` | Routes the repository workflow | Retain routing only; remove any copied concern or route semantics found during implementation |
| `AGENTS.md` | Restates contract gate, class guard, review, and work-selection rules | Expose the four route choices compactly; route boundary, D8, D6, and review semantics to their owners |
| `CONTRIBUTING.md` | Restates contract, class-guard, and high-risk review rules | Keep contributor checklist prompts; replace unconditional rules with owner links and activated-route language |
| `templates/README.md` | Routes template selection | Retain as the inventory owner; distinguish routine work, which uses no plan template |
| `templates/ci/docs-check.example.yml` | Its strict-mode comment enumerates advisory classes | Retain the two-job example but describe strict advisory promotion generically so new advisory classes do not require a copied list |
| `templates/adoption-assessment.md` | Collects adoption authority decisions | Retain purpose-limited prompts and governance owner link; do not copy route or concern tables |
| `templates/agent-execution-plan.md` | Allows routine plans and requires fresh/independent review for all profiles | Limit to material/high-risk; add activated-concern owner links; make phase 7 ordinary holistic evaluation and the high-risk review block removable |
| `templates/implementation-plan.md` | Stores contract requirements in a planning table and requires class guards | Store owner links, steps, and evidence only; make defect guard proportional and concern-driven |
| `templates/contract.md` | Generic normative contract prompts | Add a compact activated-quality ownership section; do not copy D8 triggers |
| `templates/backend-change.md` | Always presents broad backend quality fields | Add concern selection and mark quality subsections conditional on activated owners |
| `templates/frontend-surface.md` | Purpose-specific experience and style contract | Retain reachable-state prompts; route shared-value ownership and independent review conditions |
| `templates/cross-stack-change.md` | Purpose-specific shared-boundary contract | Retain interface/state prompts; add activated-quality owner links without copying triggers |
| `templates/style-system.md` | Normative style ownership contract | Retain because it owns a distinct bounded context; route exception authority |
| `templates/evidence-preserving-data.md` | Normative data/evidence contract | Retain purpose-specific lifecycle prompts; add only activated owner links |
| `templates/guide.md` | Guide skeleton lacks projection declaration | Add optional current-guide projection metadata and explain its narrow source type |
| `templates/issue-tracker.md` | Requires a class guard for every defect | Make sibling guard conditional on a repeatable mechanism and bounded value |
| `templates/independent-review.md` | Independent evidence record | Identify high-risk activation; keep specialist lenses conditional |
| `templates/holistic-evaluation.md` | Evaluates a fixed outcome set | Evaluate contract outcomes plus activated qualities; require fresh context only when risk does |
| `templates/verification-report.md` | Verification evidence record | Add activated-quality evidence reference without owning thresholds |
| `templates/handoff.md` | Compact work continuation record | Retain routing and observed outcomes; do not add normative semantics |

## Verification and evidence matrix

| Claim | Evidence class | Command/probe | Expected negative path | Durable record |
|---|---|---|---|---|
| Projection targets are valid normative owners | Fixture guard | `python -m unittest tests.test_check_docs` | Missing, escaping, non-guide projection, or non-current/non-normative source fails | Harness contract + final evidence |
| Projection drift is visible but proportional | Clock-controlled fixture | same suite | Later-dated source advises; `--strict` blocks; equal/newer guide passes; same-day ordering is explicitly unproved | Harness contract + final evidence |
| Lifecycle stock cannot claim incoherent authority | Fixture guard | same suite | Completed non-plan, current retired contract, and one-sided supersession fail | Harness contract + final evidence |
| Templates collect activated concerns without duplicating trigger semantics | Template fixtures + inventory audit | repository check and scoped `rg` | Routine agent plan, mandatory material independent review, missing concern-owner routing, or copied trigger table fails review/fixture as applicable | Final evidence |
| Routine and experiment routes are executable from the agent entrypoint | Cold-read review | follow `AGENTS.md` links | Reader must not synthesize several conflicting routes | Independent final evaluation |
| Existing governance remains stable | Regression | full unittest suite and both checker modes | All pre-existing fixtures remain green | Final evidence |

## Layered completion

- Task acceptance: each contract, checker, template, and entrypoint task passes
  its focused guards.
- Task-group outcome: the four routes, activated concerns, positive discretion,
  and document lifecycle operate as one coherent harness.
- Objective outcome: implementation and independent holistic evaluation close;
  real-project adoption effectiveness remains `partial` under the existing
  adoption promise.
- Release-gate claims: not applicable to this template-only change.

## Progress and closure

- **2026-07-28 — active:** owner approved scope and serial independent review;
  contracts and authority-map target semantics landed before dependent
  implementation.
- Current executable step: none; reusable-template objective complete.
- Contract/plan/issue/evidence updates required at closure: restore implemented
  statuses after fixtures and entrypoints land; complete this plan; retain the
  two review records as historical evidence. Complete; no issue record was
  needed after review findings were corrected in scope.
- Final revision and verdict: working tree based on
  `feat: govern style ownership and layering` (2026-07-27); independent `PASS`.
