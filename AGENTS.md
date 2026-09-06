# Repository working agreement

The requested observable outcome is the objective. Contracts, tests, documents,
and checks preserve intent and expose mistakes; completing them alone is not
completion of the task. Compare delivery with the original request as well as
its accepted interpretation.

When transferring practices, preserve the [adoption value order](docs/contracts/project-adoption.md#transfer-value-is-ranked-before-its-carriers):
interaction and epistemic discipline; truth, ownership, and boundaries; coherent
verified delivery; activated domain disciplines; then documentation and tooling.
This order guides attention, not authority or mandatory copying.

## Start with the task

1. Identify the requested outcome, existing authorization, relevant current
   facts, and affected owner. Investigate before asking questions the repository
   or available primary sources can answer.
2. Read the relevant structural boundaries in `ARCHITECTURE.md`, the authority
   and [task-context rules](docs/README.md#task-context), and applicable current
   contracts or accepted target changes. Include an active plan only when it
   applies. Follow dependencies and exceptions; do not recursively load history
   or every linked domain document.
3. Read `docs-policy.toml` before reporting a governance gap. Declared adoption
   stage, source roots, managed scope, and template profile determine what is
   enforced. Do not widen scope or weaken a rule to make a check pass.
4. Choose the [smallest execution route](docs/contracts/agent-execution-discipline.md#the-harness-selects-the-smallest-executable-route).
   Routine work uses existing authority and focused guards, without a new plan.
   Material delivery reconciles its contract before dependent implementation
   and uses a plan with actual dependencies and claim-specific verification.
   An unknown material technical fact may use a [bounded experiment](docs/contracts/development-discipline.md#contract-before-material-delivery-evidence-before-certainty).
   High-risk work requires [independent design and completion review](docs/contracts/agent-execution-discipline.md#high-risk-design-uses-independent-lenses).

## Execute the authorized outcome

- Once intent and authority are settled, continue through implementation,
  integration, verification, and necessary corrections to task completion.
  Internal checkpoints and required reviews are execution work, not new user
  approval gates. Apply the [engineering decision envelope](docs/contracts/governance-decision-boundary.md#delegated-engineering-work-proceeds-by-default).
- Investigate technical uncertainty and make locally reversible choices within
  that envelope. Ask for a human decision only when new facts change material
  intent, authority, accepted risk, or expose an actual blocker. Pause its
  affected path and continue unaffected authorized work.
- Keep human direction, priority, and risk acceptance with the owner. A bounded
  task ends at its outcome; ongoing portfolio work needs its own authorization.
  Classify governance findings using the [decision boundary](docs/contracts/governance-decision-boundary.md#states-and-triggers).
- Preserve unrelated changes and explicit public boundaries. Keep one owner for
  each rule, investigate existing implementations before adding another, and
  complete one coherent end state. A diagnosis request authorizes investigation
  and explanation, not an unrequested implementation.
- Reconcile conflicts before editing dependent code. Plans, summaries, memory,
  and worker reports do not override current authority. Record adopted general
  rules at their existing owner; an explicit instruction to adopt supplies
  confirmation for that scope.
- Name a defect's mechanism and add a proportionate sibling guard where useful.
  Correct the responsible default, interface, example, or context route; retire
  redundant reminders instead of appending every incident to this entrypoint.
- Research unfamiliar checkable claims, preserve source strength and uncertainty,
  and try a capability-preserving fallback when a tool fails. Explain the
  decisive cause and its limits in plain language; follow the [inquiry rules](docs/contracts/development-discipline.md#unknown-references-are-researched-not-reconstructed)
  and [language standard](docs/README.md#language-style).

## Read domain rules when activated

[Development discipline](docs/contracts/development-discipline.md#activate-concerns-instead-of-expanding-ceremony)
owns concern triggers. Read its applicable owner before changing the boundary.

| Task touches | Read |
|---|---|
| User-facing interface | Applicable `docs/design/` surface; development's [frontend rules](docs/contracts/development-discipline.md#frontend-development-contract) |
| Service, state, persistence, or API | Development's [backend rules](docs/contracts/development-discipline.md#backend-and-service-development-contract) |
| Producer and consumer together | Development's [cross-stack rules](docs/contracts/development-discipline.md#cross-stack-coordination) |
| Time/calendar or operator-visible demo data | Applicable sections of [foundational runtime](docs/contracts/foundational-runtime-discipline.md) |
| Concurrent agents or delegated work | [Written coordination](docs/contracts/agent-execution-discipline.md#parallel-work-is-coordinated-in-writing) and [bounded delegation](docs/contracts/agent-execution-discipline.md#delegated-work-carries-bounded-context-and-returns-to-an-owner) |
| Adoption into another project | [Project adoption](docs/contracts/project-adoption.md) and [onboarding](docs/guides/onboarding.md) before rewriting authority or enabling gates |

## Verify and close

Use [bidirectional verification](docs/contracts/development-discipline.md#verify-promised-and-observed-behavior-in-both-directions):
check each functional promise and activated quality boundary, then inspect actual
external effects for missing, undeclared, excessive, or wrongly suppressed
behavior. Include relevant identity, frequency, freshness, failure/recovery,
and the user's next action. Passing tests cannot substitute for observing the
claimed outcome; missing evidence remains unknown or not run.

Run checks appropriate to the affected risk. Reconcile changed owners and
projections, update plan/issue/verification states, and retire obsolete working
context before claiming the relevant completion layer. For harness or template
changes, run both commands with Python 3.11 or newer:

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
python3 scripts/check_docs.py
```
