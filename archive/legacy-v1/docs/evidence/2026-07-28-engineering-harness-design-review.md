---
doc_type: evidence
status: historical
authority: evidence
last_reconciled: 2026-07-28
subject: engineering-harness-design
---

# Engineering harness independent design review

## Review scope and independence

- Review scope: contract and plan design before dependent implementation.
- Risk profile: `high-risk`.
- Reviewer/context identity: fresh serial design-review subagent
  in an isolated review context.
- Relationship to proposal: this context did not author the proposal,
  contracts, plan, templates, or checker implementation.
- Independence required and achieved: yes. The reviewer received the approved
  outcome and governing read order, then inspected repository authority and the
  current worktree without the implementer's reasoning trace.

## Inputs

- `ARCHITECTURE.md`
- `docs/README.md`
- `docs/contracts/development-discipline.md`
- `docs/contracts/governance-decision-boundary.md`
- `docs/contracts/agent-execution-discipline.md`
- `docs/contracts/documentation-harness.md`
- `docs/plans/2026-07-28-engineering-harness-enablement.md`
- `docs/contracts/project-adoption.md`, `docs/guides/onboarding.md`, and
  `templates/adoption-assessment.md` for the delegated-risk boundary
- `AGENTS.md`, `CONTRIBUTING.md`, `docs/guides/project-operation.md`,
  `templates/agent-execution-plan.md`, `templates/implementation-plan.md`,
  `docs-policy.toml`, and the existing checker/tests where needed
- Current unstaged/untracked diff as observed on 2026-07-28

## Perspective findings

### System and contract consistency

1. **HIGH - An activated quality boundary can fall into planning authority.**
   `development-discipline.md` D2 requires one authoritative owner, but D8 says
   an activated concern may name its owner, boundary, failure mode, and evidence
   in an existing "contract or plan" when an owner already exists. This has two
   defects: `docs/README.md` explicitly limits plans to execution order, and D8
   says nothing about the case where no owner exists. A plan can therefore
   become the only written source for a performance, security, reliability, or
   cost boundary, or the boundary can remain unowned. That contradicts both the
   authority map and the approved single-owner quality model.

   Required correction: make the applicable current/target contract the sole
   owner of the quality boundary, failure policy, and exception policy. A plan
   may record only the selected concern, owner link, implementation steps, and
   evidence. If no normative owner exists, delivery waits for the contract to
   establish one; an experiment may use only an already authorized safety
   boundary.

2. **HIGH - Material work still inherits high-risk review depth.** A1 reserves
   independent multi-perspective and fresh-context review for high-risk work,
   but A2 phase 7 requires every material change to be evaluated "from outside
   the implementation context." The current agent-plan template makes this
   stronger: it allows `routine` even though A8 says routine work creates no
   plan, requires a fresh-context phase-7 result, and always includes independent
   design, synthesis, and final-review rows. This directly defeats the smallest
   executable route and creates records for concerns that did not activate.

   Required correction: make material phase 7 a holistic evaluation against
   the contract, with fresh context required only by A3/A4. Remove `routine`
   from the agent-plan template, mark the review block as high-risk-only and
   removable for material work, and audit every reusable template so
   concern-specific sections are retained only when activated. Update the plan
   and fixture expectations to test these negative paths, not merely the
   presence of a route section.

3. **HIGH - The experiment route lacks complete containment and failure
   behavior.** D1 supplies question, path, time, and disposable boundaries, and
   G7 correctly says an experiment grants no privileged or irreversible
   authority. However, A8 sends unresolved material facts directly to an
   experiment without explicitly applying D8 to the experiment's own actions.
   A non-production experiment can still use sensitive data, an external
   service, a material compute budget, or reliability-sensitive infrastructure.
   The design also does not say what happens at expiry, on boundary escape, or
   when cleanup fails. D1's allowance for separately authorized privileged or
   irreversible work is not explicitly separated from the experiment's own
   authorization.

   Required correction: route the experiment method itself through D8 before
   execution. Record every activated owner and existing boundary, expiry/abort
   trigger, containment action, cleanup evidence, and escalation on cleanup or
   boundary failure. State explicitly that separate authorization remains a
   prerequisite and is not created by the experiment record. Scratch code must
   still be discarded even when findings are adopted.

4. **MEDIUM - Projection lifecycle and freshness semantics are not executable
   as specified.** H12 says `projection_of` participates in lifecycle validation
   but defines only a `current` projection pointing at a `current` source. The
   authority map's active read set also includes `active`, `target`, and
   `needs_reconciliation`; the design does not state how those statuses, a
   superseded source, or `ARCHITECTURE.md` behave. The plan's fixtures cover only
   older current projections. In addition, day-granularity `last_reconciled`
   cannot support the plan's broader claim that every source change produces a
   signal: a source and projection changed in that order on the same day compare
   equal.

   Required correction: define the allowed projection document types, source
   authority kinds, source/projection lifecycle matrix, and recovery for a
   superseded or reconciling source. Apply freshness to every applicable active
   projection, not only status `current`. Either store a monotonic source
   revision/fingerprint or narrow the claim to later-dated reconciliation,
   document the same-day false-negative limitation, and test it.

5. **MEDIUM - The new no-age rule contradicts existing lifecycle aging.** D9
   prohibits universal document age limits, and H12/Forbidden behaviors repeat
   that prohibition, while H3 and `docs-policy.toml` intentionally apply a
   repository-wide `target_max_age_days` default and other aging deadlines.
   "Age limit" is broad enough to outlaw the mechanism this contract already
   owns; the approved outcome required avoiding file and line quotas, not
   removing review deadlines.

   Required correction: prohibit document volume or blanket retention age as a
   quality/deletion proxy, while explicitly preserving target-review, promise,
   and pending-evidence deadlines owned by H3.

6. **MEDIUM - The quality model requires an exception even where waiver is not
   allowed, and its reliability trigger is incomplete.** D2 gives every quality
   attribute an "exception path," while governance G4 permits an exception only
   when the owning rule is waivable and forbids silent waiver of legal or safety
   authority. D8 activates reliability only for a new availability dependency
   or operator workflow, missing changes to timeout, retry, failover,
   degradation, or recovery behavior within an existing dependency.

   Required correction: require an escalation/exception policy that may
   explicitly be non-waivable, and broaden the reliability trait to cover
   availability and recovery behavior, including retry/timeout/failover changes.

### Agent and operator efficiency

7. **MEDIUM - The positive decision envelope has no default when a risk budget
   is absent.** G6 uses "reversible at reasonable cost," while the envelope
   definition requires "declared risk budgets." The adoption contract,
   onboarding guide, assessment template, and `docs-policy.toml` identify risk
   authority but do not declare a risk budget. An adopter following the shipped
   path can therefore reach the new rule with no objective way to know whether
   ordinary discretion is authorized, recreating the approval-seeking behavior
   the change is intended to remove.

   Required correction: say "any declared risk budget" and define the no-budget
   default in G6: proceed when the choice remains inside current authority,
   managed scope, and activated boundaries and is locally reversible without
   durable effects. Investigate uncertainty about reversibility; request a human
   decision only for product intent or risk acceptance. Add a budget field to
   onboarding only if projects are actually required to define one.

### Engineering, maintenance, anti-bloat, and coupling

8. **MEDIUM - The plan does not inventory the projections it promises to
   reconcile.** The implementation scope says guides and compact entrypoints
   will change, but the verification matrix checks only copied concern-trigger
   semantics and link traversal. Existing `AGENTS.md`, `CONTRIBUTING.md`,
   `docs/guides/project-operation.md`, and `templates/agent-execution-plan.md`
   restate contract-first, class-guard, seven-phase, review, or work-selection
   rules. `projection_of` applies only to canonical non-normative documents, so
   it cannot by itself manage root and template coupling. A final generic audit
   is too weak to prove the claimed subtraction.

   Required correction: add a concrete coupling inventory to the plan. For each
   canonical guide, decide and test `projection_of`; for every root entrypoint
   and reusable template, identify the exact rule text to replace with routing
   or a purpose-limited prompt. Keep semantic duplication review-based rather
   than adding forbidden similarity or volume checks. Replace the plan's copied
   "84 fixture tests" baseline with a command and revision so the plan does not
   create a count that becomes stale during its own implementation.

## Synthesis

| Finding | Perspectives agreeing | Severity | Required action | Owner |
|---|---|---|---|---|
| Quality boundaries can live in plans | system/contract, maintenance, coupling | high | keep normative boundary/failure/exception semantics in contracts | development-contract owner |
| Material route still requires high-risk review artifacts | system/contract, agent/operator, anti-bloat | high | make phase 7 and template review blocks risk-conditional | agent-contract and template owners |
| Experiment safety has no concern routing or containment failure protocol | system/contract, operator, maintenance | high | apply D8 to experiment actions and define abort/cleanup/escalation | development and agent-contract owners |
| Projection lifecycle/freshness is under-specified | system/contract, maintenance, coupling | medium | define lifecycle matrix and honest revision signal | harness-contract/checker owner |
| No-age language conflicts with H3 | system/contract, anti-bloat | medium | distinguish volume/retention proxies from review deadlines | development and harness-contract owners |
| Quality exception/reliability semantics are incomplete | system/contract, operator | medium | allow non-waivable policy and broaden reliability trigger | development-contract owner |
| Engineering envelope lacks a no-budget default | agent/operator, system/contract | medium | define default or add an adopted declaration surface | governance-contract owner |
| Coupling/subtraction work lacks an explicit inventory | maintenance, anti-bloat, coupling | medium | enumerate projection, routing, and deletion decisions in the plan | plan owner |

## Disagreements and human decisions

- Unresolved disagreement: none. The findings do not challenge the approved
  product/governance direction; they identify internal contradictions and
  missing failure semantics in the selected design.
- Human-authority decision required: none for the corrections above. They stay
  inside the approved outcome. A human decision is needed only if the owner
  chooses to require every adopter to declare a quantitative risk budget.
- Governance exception: none.

## Primary reconciliation disposition

The primary context accepted all eight findings without changing the approved
outcome. The failed verdict remains the historical result of the first review;
the serial independent re-review below is the effective pre-implementation
gate.

| Finding | Reconciliation |
|---|---|
| Quality authority in plans | D8 now reserves boundary, failure, and escalation/exception policy to current/target contracts; plans keep only owner links, steps, and evidence |
| Material route inheriting high-risk review | A2 phase 7 is now an ordinary contract/quality evaluation; fresh context remains high-risk-only, and the plan inventories the required template subtraction |
| Experiment containment | D1 routes experiment actions through D8 and requires existing safety owners, expiry, abort, containment, cleanup evidence, and cleanup/boundary escalation; scratch implementation is always discarded |
| Projection lifecycle/freshness | The authority map and H12 now limit projection to current canonical guides over current normative contracts/surfaces, define invalid-source recovery, and state the same-day date limitation |
| Age-rule conflict | D9 and H12 prohibit blanket retention age as a quality/deletion proxy while preserving H3 deadlines |
| Quality exception and reliability | D2 allows non-waivable policy; D8 includes timeout, retry, failover, degradation, and recovery changes |
| Missing risk-budget default | G6 uses any declared budget and supplies a locally reversible, no-durable-effect default inside current authority and activated boundaries |
| Missing subtraction inventory | The plan now names every current guide, root entrypoint, and reusable template with its intended projection, routing, retention, or subtraction treatment; the baseline uses commands and a revision rather than a copied count |

Primary runtime correction: the reviewer's default-interpreter observation is
accurate for `python3`, but its broader conclusion is not. The repository can
run Python 3.11 through `uv run --python 3.11`; before this review, the primary
context ran the repository check successfully with that command. No checker or
fixture implementation claim is inferred from that earlier check.

## Limitations

- This is a pre-implementation review. Projection, lifecycle, template, and
  entrypoint changes do not yet exist, so their implementation quality is not
  evaluated here.
- The available default interpreter is Python 3.9.25 and no Python 3.11 binary
  is installed. The 84-test suite and both repository-check modes correctly
  stopped at the supported-runtime preflight; `git diff --check` passed. These
  results describe the reviewer's direct environment only. As corrected in the
  primary disposition above, a managed Python 3.11 runtime is available through
  `uv`; neither observation validates the proposed checker behavior.
- The repository is an unconfigured template architecture, so real-project
  usability and risk-boundary behavior remain outside this evidence class.

## Verdict and follow-up

`FAIL`

The approved direction is coherent, but the current design is not ready for
dependent implementation. Correct findings 1-3 before implementation begins,
then incorporate findings 4-8 into the same contract/plan revision and have the
primary context synthesize the result. The required correction is design
reconciliation, not a governance exception or a change in product priority.

## Serial re-review

- Reviewer/context: the same isolated serial design-review subagent,
  continuing after primary reconciliation.
- Scope: all eight original findings plus the revised plan's D8 owner mapping
  and complete reusable-template coupling inventory.
- Result: the first re-review found two plan defects: independent review was
  incorrectly listed as a D8 concern, and
  `templates/ci/docs-check.example.yml` was absent from the inventory. The
  primary context moved review back to A1/A3/A4, added normative owner links for
  each real D8 concern, and added a retain-and-generalize CI-template
  disposition.
- Verification observed by reviewer: both repository checker modes passed
  through `uv run --python 3.11` for `--today 2026-07-28`, and
  `git diff --check` passed.

`PASS`

No high- or medium-severity design contradiction remains. The
pre-implementation design gate is satisfied; this verdict does not evaluate the
dependent checker, template, guide, or entrypoint implementation.
