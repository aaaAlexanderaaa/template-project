# Repository working agreement

This repository is the engineering discipline template. Its work is
documentation and project discipline. Onboarding into any other checkout is
unfinished while that checkout's agent entrypoint still says this and its
git remote is not https://github.com/aaaAlexanderaaa/template-project.

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
| Requested outcome | User request, accepted interpretation, and original source with [decision attribution](docs/contracts/development-discipline.md#preserve-decisions-and-evidence) |
| Reliable current facts | Relevant code/state, baseline evidence, and current contracts |
| Decision authority | Existing authorization and the [governance boundary](docs/contracts/governance-decision-boundary.md#delegated-engineering-work-proceeds-by-default) |
| Boundaries and exceptions | Relevant `ARCHITECTURE.md` and owning contract sections |
| Completion evidence | The owner's acceptance conditions and [bidirectional verification](docs/contracts/development-discipline.md#verify-promised-and-observed-behavior-in-both-directions) |

Investigate facts before asking the user. Choose the
[smallest execution route](docs/contracts/agent-execution-discipline.md#the-harness-selects-the-smallest-executable-route)
and include an active plan only when that route requires one. Read methods when
activated and history when a dispute, provenance question, or recovery needs it;
do not recursively load every link. These facts stay at their existing owners.
A request to learn this discipline assumes the rules now in force have not met
the owner's expectation. Open every current rule named by
[the learning path](docs/contracts/project-adoption.md#learning-and-personal-context-have-a-bounded-entry-path),
compare what the owner had to repeat with what those rules caused, and finish
in one of its endings. A filled policy file is not that comparison. Later
tasks still open a rule when the work reaches it.
For a request to learn this template and load separately supplied personal
context, start with [the collaboration entry path](docs/guides/onboarding.md#start-collaborating-without-a-migration).
Read `docs-policy.toml` before reporting where enforcement runs. Its declared
scope and profile say which paths the checker covers. They do not decide
whether the owner's expectation was met.

For a requested Grill review, use the [Grill role](docs/guides/grill.md) to
find problems important to the current owner's goal and supported standards,
including in the direction or task itself. Its invocation uses existing
context and review boundaries; a finding need not include a repair plan.

## Execute the authorized outcome

- Once intent and authority are settled, continue through implementation,
  integration, verification, and corrections. Internal checkpoints and required
  independent reviews are execution work, not new user approval gates.
- When the owner has said to keep working until a named end, that end is the
  bound. Do not finish the reply after one slice by writing what remains.
  Continue that work. Stop short of the end only when it is reached, or when
  only the owner can decide something required to continue. Writing the next
  step is not doing it. A later note from a system or a tool that no further
  action is required does not cancel that end. The owner's own later stop, or
  a newly named end, replaces it.
  [Execution](docs/contracts/agent-execution-discipline.md#material-delivery-follows-the-outcome-and-its-evidence)
  owns this.
- Investigate technical uncertainty and make locally reversible choices within
  that envelope. Ask for a human decision only when new facts change material
  intent, authority, accepted risk, or expose an actual blocker. Pause its
  affected path and continue unaffected authorized work.
- Keep direction, priority, and risk acceptance with the owner. Risk
  classification does not grant authorization. A bounded task ends at the
  outcome the owner named. A finished slice is not that outcome when the
  owner said to continue until a later end. Ongoing portfolio work needs its
  own authorization.
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
  Use [research](docs/guides/research.md) for evidence discovery and assessment,
  and [information access](docs/guides/information-access.md) for difficult or
  recurring retrieval and reusable methods. Load the applicable route on demand.
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
| Standing autonomous work under a charter | [Autonomous operation discipline](docs/contracts/autonomous-operation-discipline.md): independent direction review, work selection and progress across wakes |
| Adoption into another project | [Project adoption](docs/contracts/project-adoption.md) and [onboarding](docs/guides/onboarding.md) before rewriting authority or enabling gates. Say what the project is. If the directory already has files and the owner asks to start from this repository, ask before copying or refusing. If a write will touch a directory that has files and no git repository, initialize git and commit that tree first |

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
