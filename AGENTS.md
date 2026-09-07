# Repository working agreement

The requested observable outcome is the objective. Contracts, tests, documents,
and checks preserve intent and expose mistakes; completing them alone is not
completion of the task. Compare delivery with the original request as well as
its accepted interpretation.

When transferring practices, preserve the [adoption value order](docs/contracts/project-adoption.md#transfer-value-is-ranked-before-its-carriers):
interaction and epistemic discipline; truth, ownership, and boundaries; coherent
verified delivery; activated domain disciplines; then documentation and tooling.
This order guides attention, not authority or mandatory copying.

## Establish the current task context

Use the [task-context rule](docs/README.md#task-context) to locate:

| Needed fact | Read or observe |
|---|---|
| Requested outcome | User request, accepted interpretation, and original source |
| Reliable current facts | Relevant code/state, baseline evidence, and current contracts |
| Decision authority | Existing authorization and the [governance boundary](docs/contracts/governance-decision-boundary.md#delegated-engineering-work-proceeds-by-default) |
| Boundaries and exceptions | Relevant `ARCHITECTURE.md` and owning contract sections |
| Completion evidence | The owner's acceptance conditions and [bidirectional verification](docs/contracts/development-discipline.md#verify-promised-and-observed-behavior-in-both-directions) |

Investigate facts before asking the user. Choose the
[smallest execution route](docs/contracts/agent-execution-discipline.md#the-harness-selects-the-smallest-executable-route)
and include an active plan only when that route requires one. Read methods when
activated and history when a dispute, provenance question, or recovery needs it;
do not recursively load every link. These facts stay at their existing owners.
Read `docs-policy.toml` before reporting a governance gap; its declared scope
and profile determine enforcement.

## Execute the authorized outcome

- Once intent and authority are settled, continue through implementation,
  integration, verification, and corrections. Internal checkpoints and required
  independent reviews are execution work, not new user approval gates.
- Investigate technical uncertainty and make locally reversible choices within
  that envelope. Ask for a human decision only when new facts change material
  intent, authority, accepted risk, or expose an actual blocker. Pause its
  affected path and continue unaffected authorized work.
- Keep direction, priority, and risk acceptance with the owner. Risk
  classification does not grant authorization. A bounded task ends at its
  outcome; ongoing portfolio work needs its own authorization.
- Preserve unrelated changes and explicit public boundaries. Keep one owner for
  each rule, investigate existing implementations before adding another, and
  complete one coherent end state. A diagnosis request authorizes investigation
  and explanation, not an unrequested implementation.
- Reconcile changed behavior at its existing owner before dependent code;
  follow the [delivery-contract rule](docs/contracts/development-discipline.md#contract-before-material-delivery-evidence-before-certainty).
  Plans, summaries, memory, and worker reports do not override current authority.
  An explicit instruction to adopt a rule supplies confirmation for that scope.
- Name a defect's mechanism and add a proportionate sibling guard where useful.
  Correct the responsible default, interface, example, or context route; retire
  redundant reminders instead of appending every incident to this entrypoint.
- Research unfamiliar checkable claims and try a capability-preserving fallback
  when a tool fails. Preserve evidence strength and uncertainty under the
  [inquiry rules](docs/contracts/development-discipline.md#unknown-references-are-researched-not-reconstructed).
  Use English for repository edits and plain explanations under the
  [language standard](docs/README.md#language-style).

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
