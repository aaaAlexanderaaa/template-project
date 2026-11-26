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
   persisted state, and rendered output. Write checks against expected behavior
   rather than broken current state, and verify rendered UIs in a real browser
   across widths rather than mocked DOM tests alone.
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
checking, not Independent Review. A valid Independent Review requires the first
four conditions together, plus the remaining conditions whenever they apply:

1. **Fresh context with withheld author rationale**: Run in a fresh conversation
   or subagent that did not write the code or proposal. Supply only verbatim user
   goals (`docs/sources.toml` `SRC-*`), standing repository agreements, and the
   deliverable itself—withhold the author's self-justifications and defense until
   after the reviewer records its first judgment. Verify that isolation actually
   holds (for example, that no build-session instructions were injected into the
   reviewer) instead of assuming it from "a new subagent was started".
2. **Open-ended holistic mandate first**: Never pre-limit an independent
   reviewer to a narrow bug-hunting list (such as asking only whether JS
   functions escape strings) or to a yes/no gate ("does subnet X pass the four
   checks?"). A gate question makes the reviewer audit the author's checklist
   instead of asking what the checklist missed. Start with an open question
   asking what fails overall across goal alignment, system design,
   cross-document consistency, and real usability; targeted checks may follow
   only after open discovery.
3. **Architecture, consistency & outcome scope**: Examine whole-system
   boundaries, single-source ownership, operational logic, hard constraints, plain
   language, and whether downstream adopters or unfamiliar readers actually get
   the intended value—rather than stopping at local code syntax. Check judgments
   with open expectation violations first and consider removing or simplifying
   rules before proposing additions.
4. **Closed-loop re-verification**: After fixing issues raised by an independent
   review, re-verify from both ends:
   - Return to the **original reviewer context** (when still open) with the
     updated deliverable to confirm the reported root flaws actually vanished.
   - Launch a **fresh unprimed reviewer** when structural changes are large
     enough that a fresh first impression is required.
5. **Expectation first for coverage and freshness**: Reading only the
   deliverable finds what is wrong but not what is missing. When a review judges
   coverage or currency (knowledge content, landscape overviews, dependency or
   standards surveys), the reviewer first builds, without seeing the
   deliverable, a list of what must be covered for the stated reader and
   boundary; only then compares the deliverable against that list and marks
   missing, outdated, and superfluous items. For currency, the list comes from
   dated sources retrieved during the review (condition 6); items recalled from
   memory serve only as search starting points.
6. **Currency is settled by retrieved, dated evidence, not by anyone's
   memory**: Every model and every person has a knowledge horizon. Switching to
   another model or asking a person only picks a different horizon, not a
   correct one. Claims about the current state of a field are checked against
   primary sources fetched at review time, each recorded with its publication
   date and retrieval date. The check must explicitly cover the window between
   the deliverable's latest dated item and today, using date-anchored discovery
   ("releases since <date>", maintained release trackers, the latest edition of
   annual reports) rather than searches for names already known. Record the
   queries, retrieval date, and covered window. Another model or the owner adds
   value by suggesting different search directions or judging relevance; their
   recollection is not evidence. When retrieval is unavailable, mark the claim
   "currency unverified as of <date>" instead of passing it.
7. **Reviewers report findings; the owner confirms status**: Reviewers return
   findings with severity, not "pass" or "conditional pass" verdicts. Milestone
   claims such as "complete", "saturated", or "approved" change only after the
   findings are resolved and the owner confirms; the author never upgrades a
   conditional result to a pass on their own.
8. **Vary the angle**: A neutral comprehension question, a deliberately
   critical question, a comparison across the whole collection, or a hands-on
   usage walkthrough surface different problems. Use at least two angles for
   milestone reviews; a useful finding from one angle keeps its value without a
   vote.
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
- Separate exact, reproducible engineering facts from open-domain or multi-definition data (such as history, industry, or social research): present differing sources and premises side by side, drop clear errors, and never fabricate false precision or hand-tuned composite scores.
