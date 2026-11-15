---
doc_type: contract
status: current
authority: normative
---

# Stage-Matched Delivery, Verification & Review

<!-- required-reading: stage-rigor -->
## 1. Rigor Scales With Domain Maturity Stage

Engineering ceremony must accelerate AI delivery rather than choke early work in
bureaucracy. Match verification and documentation weight to the domain's
`stage`:

| Stage | Goal | Required baseline | Deliberately deferred ceremony |
|---|---|---|---|
| `prototype` (`0 → 0.1`) | Validate core idea and user flow quickly | Brief `ARCHITECTURE.md` intent, runnable primary path, basic file modularity, safety/secret hygiene | No multi-agent review dispatch, no exhaustive edge-case matrices, no freeze on internal schemas |
| `usable` (`0.1 → 1`) | Deliver reliable user-facing capabilities | Module specs (`owns`, `depends_on`, `promise`), `SRC-*` quote links, real happy + failure-path tests, import & size checks | Heavy migration windows only on persisted user data |
| `stable` (`1 → N`) | Protect existing users and multi-domain boundaries | Full contract/spec reconciliation before breaking interface edits, backward-compatible migrations, regression guards, independent review on high-risk boundaries | None on public interfaces |

In large multi-subsystem repositories, a new experimental domain can declare
`stage: prototype` in `docs/specs/<domain>/README.md` while core domains remain
`stable`.
<!-- /required-reading: stage-rigor -->

<!-- required-reading: bidirectional-verification -->
## 2. Bidirectional Verification

Before claiming a task is ready:

1. **Promise → Observation**: Exercise the real runtime entrypoint (CLI, HTTP
   endpoint, or UI flow) for every promised user outcome and verify exit status,
   persisted state, and rendered output.
2. **Observation → Unintended Side Effects**: Check actual external effects
   (`git status`, written files, network/process side effects, layout bounds,
   error states) to confirm nothing extra broke, leaked, or silently failed.
3. **Separate Machine State From Human Acceptance**: Passing automated tests set
   a task to `ready_for_check` (or `done` for purely internal refactors); user-
   facing outcomes record human confirmation (`human_check = "approved"`)
   separately rather than conflating green unit tests with user satisfaction.
<!-- /required-reading: bidirectional-verification -->

<!-- required-reading: environment-aware-review -->
## 3. Environment-Aware Review & Change-Based Grill Cadence

Configure `[collaboration]` in `docs-policy.toml` to match how the repository
actually runs:

- **Interactive collaboration (`mode = "interactive"`)**: When working live with
  the human owner on a strong reasoning model, do not automatically spawn
  multiple review subagents on ordinary tasks. Reserve independent fresh-context
  review for irreversible migrations, security/auth boundaries, or explicit
  owner requests.
- **Unattended autonomous operation (`mode = "unattended"`)**: Require a
  standing charter (`templates/charter.md`), bounded write/resource limits, and
  fresh-context review before closing milestones across unattended wakes.
  Unattended loops must stop cleanly and enter dormancy on repeated verification
  failures, pending human blockers, or completed scope, and must never edit
  their own charter, budgets, or `human_check` approvals.
- **Change-accumulated `/grill` signal (no calendar timers)**: Count **commits
  and distinct modules touched since the last recorded review anchor** rather
  than elapsed calendar days. When accumulation crosses
  `grill_cadence_commits` or `grill_cadence_modules`, surface a concise prompt
  asking whether the owner wants a `/grill` pass.
<!-- /required-reading: environment-aware-review -->

<!-- required-reading: independent-review-definition -->
## 4. Independent Review Definition & Closed-Loop Protocol

Passing tests or running a directed code-bug checklist in a subagent is QA
checking, not Independent Review. A valid Independent Review requires four
conditions together:

1. **Fresh context with withheld author rationale**: Run in a fresh conversation
   or subagent that did not write the code or proposal. Supply only verbatim user
   goals (`docs/sources.toml` `SRC-*`), standing repository agreements, and the
   deliverable itself—withhold the author's self-justifications and defense until
   after the reviewer records its first judgment.
2. **Open-ended holistic mandate first**: Never pre-limit an independent
   reviewer to a narrow bug-hunting list (such as asking only whether JS
   functions escape strings). Start with an open question asking what fails
   overall across goal alignment, system design, cross-document consistency, and
   real usability; targeted checks may follow only after open discovery.
3. **Architecture, consistency & outcome scope**: Examine whole-system
   boundaries, single-source ownership, operational logic, hard constraints, plain
   language, and whether downstream adopters or unfamiliar readers actually get
   the intended value—rather than stopping at local code syntax.
4. **Closed-loop re-verification**: After fixing issues raised by an independent
   review, re-verify from both ends:
   - Return to the **original reviewer context** (when still open) with the
     updated deliverable to confirm the reported root flaws actually vanished.
   - Launch a **fresh unprimed reviewer** when structural changes are large
     enough that a fresh first impression is required.
<!-- /required-reading: independent-review-definition -->

<!-- required-reading: discipline-and-transfer-verification -->
## 5. Verifying Engineering Discipline & Shared Tooling

Python checks (`scripts/`) are supporting tooling while **engineering discipline and clear architecture** are the product outcome. Verification separates three layers rather than mistaking green helper-script tests for working discipline:

1. **Helper-tool unit tests**: Verify that parsers, import scanners, link checkers, TOML writers, and local HTTP routes behave deterministically.
2. **Governance & template transfer verification**: When maintaining shared discipline templates or onboarding suites, verify via `project.py init` and `read_rules.py onboard` that transferred `AGENTS.md`, `ARCHITECTURE.md`, specs, skills, and starter templates preserve every rule (priority order, three-perspective checks, five-part architecture boundaries, plain language, design-approval gates, and open closed-loop review) without leaking upstream template domains (`discipline`, `graph-engine`, `perspective-ui`, `reference-app`).
3. **Behavioral scenario evaluations**: Before trusting rule rewrites, test fresh unprimed AI sessions on realistic repository tasks (defined in [grill.md](../guides/grill.md#behavioral-discipline-evaluation-scenarios))—scoring real code/architecture outcomes and owner burden rather than form-filling compliance.
<!-- /required-reading: discipline-and-transfer-verification -->

## 6. Data & Metric Provenance

Whenever metrics, telemetry, or data-processing outputs are produced or displayed:

- Record the authoritative raw input source and computation command.
- State explicit filtering, exclusion, or sampling criteria rather than hiding caveats.
- Never silently drop invalid or anomalous inputs; surface explicit counts or errors so numbers remain reproducible.
