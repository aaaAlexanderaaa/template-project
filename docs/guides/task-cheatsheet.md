---
doc_type: guide
status: current
authority: guidance
last_reconciled: 2026-11-01
projection_of: [docs/contracts/development-discipline.md, docs/contracts/governance-decision-boundary.md, docs/contracts/agent-execution-discipline.md]
---

# Practical task CheatSheet

Use a small, well-chosen action to move an actual task forward. Start with the
obstacle below, use or adapt the matching prompt, then inspect what changed.
These optional recipes help turn judgment into action. The
[task SOP](project-operation.md#execute-one-task-from-request-to-result) supplies
the execution order; current owners supply authority, complete applicable
rules and required evidence. A straightforward task can proceed directly.

Keep [essential reasoning](../contracts/development-discipline.md#keep-essential-reasoning-active)
available when the obstacle is unfamiliar or this table seems complete. The
questions and categories can themselves miss the problem. Let actual work
challenge the selected frame; a saved lesson or a passing recipe is not proof
that its intended effect occurred.

## Choose a useful move

| Current obstacle | Try | Useful result |
|---|---|---|
| The project is too large to understand from its README | [Follow one real task](#understand-a-project-through-one-real-task) | A grounded account of current capability and its remaining gap |
| The request admits several interpretations | [Make the first useful result concrete](#make-the-first-useful-result-concrete) | An executable next action or a specific owner decision |
| Something fails, but the cause is unclear | [Find the first failing boundary](#find-the-first-failing-boundary) | A reproduced mechanism, correction and recovery evidence |
| More searching keeps producing the same explanation | [Seek an observation that separates explanations](#seek-an-observation-that-separates-explanations) | Evidence that changes or bounds the conclusion |
| A tool cannot obtain the needed information | [Recover the needed capability](#recover-the-needed-capability) | Usable evidence or a precise remaining gap |
| Alternatives sound equally plausible | [Compare them at the deciding condition](#compare-at-the-deciding-condition) | A supported choice with a reason to revisit it |
| Implementation keeps stopping at partial pieces | [Deliver one complete behavior](#deliver-one-complete-behavior) | The authorized user result works across its boundary |
| The explanation sounds correct but teaches little | [Teach through a worked case](#teach-through-a-worked-case) | The reader can make the next relevant distinction or action |
| You need a starting question about direction, growth or value | [Choose a question from practice](task-starters.md) | A concrete observation, comparison or changed premise to pursue |
| An AI's answer changes with the question or its context | [Choose wording and context together](review-cheatsheet.md#choose-wording-and-context-together) | A deliberately selected method, with its actual conditions and evidence limits |
| A new session is repeating old investigation | [Resume at the next verifiable action](#resume-at-the-next-verifiable-action) | Valid progress continues with stale assumptions exposed |
| Useful experience stays buried in transcripts | [Make experience change the next task](#make-experience-change-the-next-task) | A later task finds and uses a conditional method |
| A principle survives in documents but its effect in another context is unknown | [Try the next learner and executor](onboarding.md#keep-reasoning-usable-in-the-next-project) | Observed decisions and the first missing or distorted condition, with remaining gaps explicit |
| Simplification may remove useful responsibilities | [Subtract while preserving useful behavior](#subtract-while-preserving-useful-behavior) | A simpler whole with important duties retained |
| Checks pass, but it is unclear whether the task is done | [Judge against the original outcome](#judge-against-the-original-outcome) | A supported completion decision or continued authorized work |
| Review misses problems or transfer depends on hidden context | [Choose a review experiment](review-cheatsheet.md) | An appropriate independent judgment or consumer observation |
| Another project needs just one useful practice | [Use the extraction card](project-operation.md#take-one-practice-into-a-task) | A bounded trial with its conditions and target authority intact |

## Adapt or construct a task

A useful short assignment connects the current situation, an action that could
change it, and an observable result sufficient for the requested end. For example:

> This CLI fails only after a rejected input. Trace that operation through its
> actual input, error and retry boundaries, repair the cause within the current
> behavior contract, and show that corrected input succeeds without carrying
> over the failed operation's state.

Choose the move for the uncertainty. Following an operation finds a boundary;
contrasting cases tests a condition; making a normal copy tests adoption;
removing a layer tests what it contributes. Change the input, observation or
standpoint when it could reveal something different. A new role name alone
does little. These moves can combine: diagnose a failure, compare two causes,
deliver the fix, then retain the useful method. Each result determines the
next move; the list is open to better task-specific approaches.

For work in the current context, reuse its settled purpose and permissions.
Replace brackets in the prompts with actual inputs. A separate worker also
gets the parent outcome, relevant current sources and revision, permitted
effects, return owner and effort/stop bound through
[bounded delegation](../contracts/agent-execution-discipline.md#delegated-work-carries-bounded-context-and-returns-to-an-owner).
Selecting a recipe does not launch a worker. The linked full method is read
when selected; a prompt is a starting action, not a substitute for applicable
detail. Keep results in the existing task or owner unless a durable artifact
serves a real need.

## Understand a project through one real task

Useful when an inventory of files gives little sense of progress.

```text
The owner wants to understand [project] for [current purpose]. Start with one
representative task a user or maintainer would perform. Follow its normal
entrypoint through the current owners, implementation and observed result.
Distinguish what works now, what is only planned, and what lacks evidence.
Use the surrounding project structure to explain that path and identify the
important gaps it leaves. Return a supported progress judgment and the next
relevant action. Keep this example's coverage explicit.
```

For a template, try a normal contract copy and its promised next command.
If only that path works, say which capability it proves and inspect the other
important requested boundaries before judging the whole project. Choose the
explanation's form after the facts and reader need are clear.
Owner: [outcomes and scope](../contracts/development-discipline.md#outcomes-before-means).

## Make the first useful result concrete

Useful when ambiguity, rather than implementation, is the next obstacle.

```text
Using [request, corrections and current facts], state who needs what change,
and what observable result would be useful now. Separate checkable unknowns
from choices that belong to the owner. Investigate the former and carry out
the smallest authorized action that advances the requested end. If a material
owner choice is still required, present the actual alternatives, consequences
and your recommendation with the evidence already available.
```

For "make errors clearer," inspect a reported error and its recovery flow
before asking about a wholesale redesign. A settled local fix can proceed;
a choice about discarding user work belongs with its authorized owner.
Method: [uncertainty and decision sequencing](project-operation.md#3-resolve-uncertainty-without-guessing-or-serial-approval).
For dependent choices, first settle whether recovery must work offline; that
answer changes which storage choices are viable. A separate language preference
may be answerable in the same round. Existing permission to make a local fix
still applies. See the [worked decision frontier](project-operation.md#work-a-dependent-decision-frontier).

## Find the first failing boundary

Useful for a defect with several plausible locations.

```text
Establish an observation that fails on [the actual reported symptom]. Reproduce
it under the relevant conditions. Remove one input or step at a time while the
same symptom remains observable. Follow the remaining operation, tracing the
first wrong value back to its producer. Give plausible causes different
predictions and obtain the observation that separates them. Within the
authorized repair, correct the cause; rerun the original larger case, recovery
and a useful sibling. Remove temporary instrumentation and return what is fixed.
```

If a template looks valid but its next command rejects omitted metadata, use
the actual copied template and documented relocation. A hand-crafted ideal
fixture could hide the default mismatch. Diagnosis-only work returns the
mechanism and evidence; implementation follows the task's authority.
For an intermittent failure, retain the observed frequency and conditions;
an unsuccessful reproduction leaves that mechanism unresolved. A simple,
already-localized defect can use its direct failing example without a separate
minimization exercise. Techniques adapted from
[failure-preserving diagnosis](https://github.com/mattpocock/skills/blob/main/skills/engineering/diagnosing-bugs/SKILL.md)
and [tracing a bad value upstream](https://github.com/obra/superpowers/blob/main/skills/systematic-debugging/root-cause-tracing.md).
Owner: [category-level repair](../contracts/development-discipline.md#fix-the-category-not-only-the-symptom).

## Seek an observation that separates explanations

Useful when a consequential explanation has weak or repetitive support.

```text
Investigate [question and intended use] from [current evidence]. Identify the
important plausible explanations and an observation that could distinguish
them, including one that could weaken the leading answer. Obtain the most
useful permitted evidence, let it change the question when warranted, and
check the decisive claims. Return the supported answer, important alternatives
or gaps, and the actual reason to stop within [shared resource bound].
```

If several reports repeat one release note, inspect the actual changed
behavior or an independently obtained observation before calling them
corroboration. A direct question about a documented flag can finish with the
relevant source and answer. Method: [research](research.md).

## Recover the needed capability

Useful when a failed tool is being mistaken for a failed task.

```text
We need to observe [specific property] to answer [parent question]. The current
route produced [actual result or failure]; previous attempts are [locator].
Check the relevant known method, then try a justified permitted fallback that
can observe that property within [remaining shared budget]. Return what was
actually obtained, its source identity and limits, or the exact remaining
capability gap and recovery option.
```

A text extraction may answer a prose question. An interaction claim needs
behavioral observation; source text alone may support only a narrower result.
Method: [information access](information-access.md).

## Compare at the deciding condition

Useful when a consequential choice depends on an uncertain difference.

```text
For [authorized choice], compare [credible alternatives] under [purpose and
binding constraints]. If another design is needed, vary a meaningful objective:
for example, minimize the interface versus make the common caller simplest.
Show how the same real caller would use each proposal and what work moves
elsewhere. Identify the condition that could change the choice, then inspect
evidence or run the smallest permitted comparison there, holding relevant inputs
fixed. Return gains, losses,
shared limitations and the supported choice or owner decision, plus what
would reopen it.
```

To choose between retaining a failure case as prose or adding a mechanical
guard, inspect whether the mechanism has a stable detectable sibling and
whether the guard preserves legitimate use. A disposable implementation trial
uses the existing experiment boundary before it runs. Ordinary settled choices
keep their direct route. For a storage API, compare a single general write call
with a small operation-specific interface using the same failed-write recovery
case; count the responsibilities each caller must now carry. The contrasting
objectives adapt [Design It Twice](https://github.com/mattpocock/skills/blob/main/skills/engineering/codebase-design/DESIGN-IT-TWICE.md).
They can be explored in one context; separate workers are an optional strategy,
not a property established by the prompt. Owner:
[causal comparisons](../contracts/development-discipline.md#analysis-exposes-the-decisive-causal-mechanism).

## Deliver one complete behavior

Useful when component completion keeps leaving the actual task unfinished.

```text
Deliver [authorized observable change] from [current baseline]. Reconcile its
existing owner first, then follow the real dependency order through producer,
consumer and recovery where applicable. Observe the promised result and actual
effects at the user's boundary. Fix discrepancies within scope and continue
until [the owner's named end] is supported. Keep intermediate checkpoints
recoverable and distinguish them from completion.
```

A new error state needs its producer, consumer message and viable retry to
agree. A bounded local sort can use focused ordering and recovery checks.
For a larger change, make a checkpoint a usable behavior across its necessary
layers, with actual blocking dependencies named. A broad mechanical migration
may instead need a compatibility sequence before its integrated behavior is
ready. This adapts the [behavioral slicing technique](https://github.com/mattpocock/skills/blob/main/skills/engineering/to-tickets/SKILL.md).
Select the [execution route](../contracts/agent-execution-discipline.md#the-harness-selects-the-smallest-executable-route)
and complete activated domain requirements for the actual change.

## Teach through a worked case

Useful when a correct abstraction leaves the reader unable to act.
Use the [reader-attention questions](task-starters.md#why-should-this-reader-spend-attention-here)
when selecting the explanation's content and reviewing its actual draft.

```text
Help [reader] understand [subject] so they can [next distinction or action].
Choose a source-backed case they recognize. Show the starting condition, the
decisive choice or mechanism, the resulting change and where the lesson stops
applying. Connect it to the general rule in plain language. Inspect whether
the delivered explanation lets the intended reader use that distinction or
take the next action; revise the explanation where it fails.
```

To explain risk-scaled execution, contrast an ordinary local sort with a
public API addition using their actual effects and recovery cost. Choose
prose, a table or a visual for the reader's task. Reader evidence follows the
[delivery verification owner](../contracts/development-discipline.md#verify-promised-and-observed-behavior-in-both-directions).
When understanding a mechanism matters, ask what will happen under one concrete
trigger and check the prediction against observed behavior. Inspect the current
contract separately for what should happen. This optional comprehension probe
adapts [a code-understanding quiz](https://github.com/joshuawheelock/grill-me/blob/main/skills/grill-me/SKILL.md).

## Resume at the next verifiable action

Useful after a restart or handoff when context is large or stale.

```text
Resume [original outcome] from [existing task/handoff and current sources].
Recover the named end, authority, verified baseline, live decisions and next
dependency. Recheck current files and decisive assumptions; retain what is
still valid. Execute the next authorized action and verify its result. Return
new observations and the remaining gap at the existing owner, with enough
context for the next session to act without rereading the whole history.
```

An old passing test remains historical evidence if its owner or inputs changed.
Recheck the affected boundary while preserving valid unrelated work.
Use the [handoff template](../../templates/handoff.md) when a durable handoff is
needed, and current [task context](../README.md#task-context) for rule recovery.

## Make experience change the next task

Useful for successful tricks as well as recurring mistakes.

```text
Inspect [actual task material and result]. Find the decision or operation where
useful judgment, time or attention was lost, or where a successful move changed
the outcome. Follow it to the responsible default, example, tool or retrieval
path; check whether an existing facility already handles it. Improve that
surface within authorization. Explain why the move helped and what would
invalidate it. Keep the conditions and a locator where the next
matching task starts. Observe whether that task finds and uses the change;
include a useful sibling and a case where it should stay out of the way.
```

A successful source-recovery method belongs at the next retrieval decision.
A useful review question belongs at the matching review entrypoint. A new
transcript alone supplies neither route. If every session rediscovers a command
and repairs its quoting, investigate the command's interface and documented
entrypoint before adding another warning. Stable operations can earn a narrow
mechanical helper; conditional judgment needs a usable case. Inspect the actual
later operation before claiming reduced rediscovery or owner effort. This
adapts [session-based environment retrospectives](https://github.com/mattpocock/skills/blob/main/skills/engineering/retro/SKILL.md).
Owner: [experience reuse](../contracts/development-discipline.md#experience-changes-the-next-matching-action).

## Subtract while preserving useful behavior

Useful when rules, documents, jobs or tools have become costly to maintain.

```text
Simplify [authorized scope] for [intended benefit]. Identify the useful duties,
distinctions and recovery paths in the current arrangement. Propose the simpler
whole and trace those capabilities to their surviving owners. Remove or merge
the redundant part within authorization, then exercise an important normal
use and a case that needs an easily lost duty. Return what became simpler,
what survived and any accepted trade-off.
```

Replacing several jobs with one quiet interval still needs evidence that
authorized investigation and improvement continue. Merging duplicate guidance
can preserve a single current rule and its task locator. Owners:
[coherent replacement](../contracts/development-discipline.md#coherent-end-state)
and [document lifecycle](../README.md#document-stock-and-coupling).
For an abstraction, first imagine removing it and trace which duties return
to each caller. Compare the complete resulting arrangement. This probe adapts
[the module-removal question](https://github.com/mattpocock/skills/blob/main/skills/engineering/codebase-design/SKILL.md).

## Judge against the original outcome

Useful at closure or when another passing check adds little information.

```text
Compare [observed delivery] with [original request, accepted decisions and
later corrections]. State what problem is solved and which evidence supports
that judgment. Inspect actual effects and any original requirement missing
from the chosen artifact or tests. Close the supported requested layer, or
continue the remaining authorized work. Route only a genuine owner decision
or proven blocker to its boundary.
```

A useful review collection establishes review methods. If review was an
example of a broader practical layer, exercise and deliver that layer too.
Owner: [layered completion](../contracts/agent-execution-discipline.md#completion-is-layered).

## Keep useful methods easy to find

Add or improve a recipe when a real task reveals a reusable move. Keep the
trigger, concrete action, useful result and conditions that explain its value.
Put specialized collections beside their existing method, as with
[review](review-cheatsheet.md), [research](research.md) and
[access](information-access.md); keep this selection table as their doorway.
Replace superseded advice. General principles remain at their current owners,
and measured trials stay in evidence. This supports many task forms without
turning every example into a new global rule or required template.

## Sources and current evidence

The original twelve recipes are implementer adaptations of project rules and
methods; their [delivery record](../evidence/2026-10-28-review-method-transfer.md)
preserves that origin. The linked public techniques were integrated on October
29 following [primary-source research](../evidence/2026-10-28-public-task-method-research.md).
The separate [question starters](task-starters.md) preserve translated and
combined questions from owner-provided history, with their transformations
identified. [Source and use evidence](../evidence/2026-10-29-task-method-transfer.md)
separates those contributions and the observed trials. It supports attribution
and bounded use; comparative effectiveness requires separate evidence.
