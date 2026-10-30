---
doc_type: guide
status: current
authority: guidance
last_reconciled: 2026-10-30
projection_of: [docs/contracts/development-discipline.md, docs/contracts/governance-decision-boundary.md, docs/contracts/agent-execution-discipline.md, docs/contracts/project-adoption.md]
---

# Review tasks and question CheatSheet

Review is one family in the [practical task CheatSheet](task-cheatsheet.md).
Start there when the current obstacle calls for diagnosis, delivery, inquiry,
continuity or learning rather than another review.

Choose a review that can change the current decision. These are optional task
templates and small experiments: use the fitting card, inspect its answer,
then stop or follow the consequential uncertainty. A useful supported result
can pass. The [task SOP](project-operation.md#execute-one-task-from-request-to-result)
orders execution; [Grill](grill.md) supplies the open review role. Their owners
retain authority, independence and evidence requirements.

## Choose the task

| What needs testing | Useful move | What it can reveal |
|---|---|---|
| An AI's verdict changes with wording, supplied context or whether it authored the work | [Choose wording and context together](#choose-wording-and-context-together) | Which observation the question actually elicits and what its answer can establish |
| A delegated investigation keeps finding only what its parent already expected | [Leave the discovery path open](#delegate-discovery-without-prescribing-the-answer) | Important problems beyond a supplied reading order or category list |
| The author keeps getting favorable but incomplete reviews | Two fresh reviewers receive the same open assignment; optionally add a separate external consumer | Repeated omissions, unstable judgments and what actual use adds |
| The work may depend on hidden context | Give a fresh reader only the consumer artifact | What the artifact communicates without the author's explanation |
| One review question has become predictable | Generate a different question, then dispatch it to another context | A new answer direction rather than another wording of the same rubric |
| Individual items pass but the collection feels repetitive | Read representative items together | Shared formulas, inconsistent boundaries and gaps visible only across items |
| A method or tool claims success | Use a normal adoption path and a plausible countercase | Hidden defaults, missing dependencies and a rule applied outside its useful scope |
| Findings keep recurring without change | Inspect one prior finding through its actual owner, correction and later use | A missing delivery or retrieval step rather than another discovery |

Same-question repetition tests stability; changing question, material or
standpoint explores different blind spots. Shared models and sources remain
shared. A valuable finding from one reviewer keeps its full evidential weight;
inspect it rather than keeping only the intersection of reports.

## Choose wording and context together

A question changes what an AI investigates and what information it uses to
fill gaps. Choose the wording, recipient and supplied material for the needed
observation. This matters in review, research, planning and self-improvement
whenever an AI answer informs a consequential judgment. Development's
[analysis rule](../contracts/development-discipline.md#analysis-exposes-the-decisive-causal-mechanism)
owns the evidence duty; execution owns actual independence.

The following are close English translations of the owner's three examples
from October 30, 2026. Preserve their distinctive wording when trying or
comparing them. They are selectable methods, not three mandatory rounds.

### An unfamiliar reviewer receives a reading complaint

Give a separate reviewer the actual reader-facing article and what its intended
reader would legitimately receive. Check that the selected environment does
not inject the author's project instructions, creation history or explanation.
The owner suggests an independent empty project or a one-shot API invocation;
either route needs inspection of what was actually supplied.

```text
I cannot understand this article, but I do not know how to describe where
the problem is. Please analyze it.
```

This invites diagnosis before the reader can name a rubric. It can expose
missing premises, inaccessible language or a broken explanatory sequence.
The recipient can still produce unsupported criticism, and its general model
knowledge remains present. Match legitimate audience knowledge to the claim;
removing information an actual specialist reader has can create a false gap.

### The contextual author receives a reading complaint

Keep the existing project and writing context, and address the author:

```text
I cannot understand the article you have written. Reflect on it.
```

The complaint makes diagnosing failure salient while the author retains
design intent and repair context. This can expose problems as well as help
explain or correct them; supplied background can also conceal what the article
fails to explain. An author's explanation to the reviewer has not changed
what the article itself communicates.

### The contextual author assesses its work

Keep the existing context and ask the author:

```text
Do you think the article is self-contained? Does it work as a readable text?
```

This is a low-cost self-assessment against named qualities. The author may
answer from its intent and background instead of discovering where an unfamiliar
reader would get stuck. It can check known requirements; a favorable answer
alone does not demonstrate outside-reader comprehension.

The owner reports decreasing diagnostic effectiveness across these three
conditions. Keep that observation and its purpose findable. This delivery has
not reproduced the ranking, and the examples change several factors together:
wording, context and relationship to the work. They do not isolate a single
cause or establish a universal ordering. More forceful criticism is not by
itself more accurate. Do not replace the examples with one softened request
for an objective assessment; that changes the method being evaluated.

### Dispatch, inspect and reuse the selected method

The person or AI selecting the method needs the task and its uncertainty.
The unfamiliar reviewer receives the consumer material, without this method's
predicted defects or the author's defense. A separate conformance reviewer
still receives original intent and governing standards. If several methods
are used, retain the outside reviewer's first answer before introducing author
context or other judgments; later clarification does not erase it.

Inspect actual inputs: project and global instructions, conversation history,
memory or retrieval when known, tool-provided context, and prior answers.
A new directory, a new role name or an instruction to forget is insufficient
evidence of isolation. A one-shot call still has its request and system
instructions. Record unknown conditions and narrow the claim, or choose an
available context that can support it. Keep the dispatcher's existing authority
and permitted effects intact.

In the existing task or review evidence, retain the exact question and artifact,
recipient relationship, actual context and known model/runtime conditions,
first response, subsequent clarification, and the finding's verification.
Label negative wording as actual reported feedback or a deliberate diagnostic
probe; a simulated complaint is not evidence that a real reader failed.
Inspect the cited passage or behavior and test what a revision changes.
Preserve a useful unique finding even if other methods missed it. Investigate
disagreement rather than choosing the most favorable answer or counting votes.

Retain useful variants with their conditions, successes and failure cases.
For a consequential comparison, use the same artifact and relevant audience
while varying the factor of interest; record combined changes when isolation
is impractical. Sample repeated outputs when variability matters. Judge by
confirmed discoveries, misses, false findings, cost and subsequent consumer
results where available. A small trial supports its observed cases, not a
general effectiveness rate. A routine spelling fix may need no extra review.

## Common task templates

Replace the bracketed inputs before dispatch. Keep the actual task, permissions,
artifact identity and stop bound explicit. Launch only the selected work within
the available authorization and resources.

### Delegate discovery without prescribing the answer

This applies [bounded delegation](../contracts/agent-execution-discipline.md#delegated-work-carries-bounded-context-and-returns-to-an-owner)
and is one example of [essential reasoning](../contracts/development-discipline.md#keep-essential-reasoning-active).
For discovery, the intended user outcome and real constraints guide the work;
the parent need not supply its preferred problem categories or investigation
sequence. Give useful source locators without presenting them as the only
places where a problem could exist.

```text
Find problems in [artifact/project and revision] that could prevent
[intended users] from achieving [their actual outcome]. The original request
and governing constraints are [sources]. Available material is [entrypoints].
Choose how to investigate. Return consequential findings with supporting
observations, useful supported conclusions and what remains unknown.
Read-only scope: [permitted sources/effects]. Stop at [bound] and return the
first judgment before seeing the parent's hypotheses or other reviews.
```

The owner's short example is "Find problems that could leave users
dissatisfied." The envelope supplies the facts and permissions that make it
usable. By contrast, "First read X, then evaluate Y from these three angles"
can channel discovery into the parent's existing model. Do not treat a longer
or shorter prompt as inherently better. Necessary hazards, authority and
evidence must still be supplied. Allow a supported absence of findings;
negative framing and problem counts do not establish value.

For a known defect reproduction or a specific contract check, a named path
and required lens can be exactly what the task needs. Keep that claim bounded.
Do not turn this example into a ban on detailed assignments or an obligation
to launch multiple agents. The broader duty is to inspect how instructions,
conditions and acceptance signals shape decisions, including outside review.

### Two reviewers and an external consumer

Useful after recurring corrections, a disputed completion claim or suspected
shared blind spots. Give the following identical assignment to two fresh
contexts. Supply original intent and standards, leaving inspection open.

```text
Review [actual project/artifact and revision] against [original request and
material accepted decisions]. The owner wants [observable change]. Existing
standards and constraints are [sources]; unresolved assumptions are [items].
Choose your inspection path, including the direction, selected task and
important omissions beyond the diff. Try normal use and a useful countercase.
Report consequential problems with evidence, supported positive conclusions,
and what remains unknown. A finding need not include a repair plan.
Read-only scope: [sources and permitted temporary probes]. Stop at [bound].
Return your first judgment before seeing another review or the executor's
defense. Keep the inspected source identity and observations with it.
```

When transfer or understanding is a separate uncertainty, give a third fresh
consumer a separate task. Let the artifact communicate its intended value.

```text
You encounter [consumer-facing entrypoint/artifact and revision] for the first
time. What would you take away, and what could you actually do with it?
Start through its normal entrypoints. Record your first understanding, then
try a bounded task using only the material you select. List actual dependencies,
where the attempt succeeds or stops, and what causes any missing understanding.
Allowed sources/effects: [scope]. Stop at [bound]. Return observations and
limits before reading other reviews. No implementation outside the trial.
```

The consumer gets no expected takeaway list. A conformance reviewer still gets
the original purpose and binding constraints: these assignments test different
things. Retain first reports, then verify findings against actual sources,
preserve unique discoveries, and investigate disagreements. Agreement alone
closes no claim. A later clarification can correct a finding without erasing it.

### Only the delivered artifact

Useful for hidden vocabulary, missing explanation and the reader's first action.
Prepare verified, uniquely owned data copies and a source manifest. Keep files
such as AGENTS.md as data snapshots rather than instruction entrypoints.

```text
Using only [named data copies], what is this trying to communicate, and what
can you understand or do after reading it?
```

Keep that substantive question intact when comparing runs. Put necessary
source access, data/instruction separation and tool permissions in the dispatch
envelope; they remain binding. Avoid adding the author's answer, past verdicts
or a list of expected defects to the comprehension question.

Use the [actual-context checks](#dispatch-inspect-and-reuse-the-selected-method)
before claiming isolation. A fresh directory and `fork_turns=none` establish
different facts; limited source access does not prove an empty context.

### Generate a new question

Useful when the current rubric repeatedly misses important problems.

```text
Read [artifact] and [questions already used]. Propose a question that could
reveal something important those questions leave unseen. Explain the different
answer direction it opens. A new adjective or role title alone adds little.
Sources/effects: [scope]. Return the question, then stop.
```

Select a useful question and ask it unchanged in a separate fresh context.
Keep generation distinct from the actual review. One good question may suffice;
new-question and repeated-review counts follow the uncertainty and resource
bound, rather than a standing quota.

## Small question experiments

Pick a move for the suspected failure; these examples are adaptations, not
verbatim owner quotations or a checklist to exhaust.

| Move | Example question | Best use and limit |
|---|---|---|
| Read the doorway | After only the opening, what do you expect this to deliver? After the ending, what did it establish? | Finds broken promises and premature conclusions; inspect the whole work before a final verdict. |
| Admit confusion | At which sentence do you first need information the artifact has not supplied? | Locates hidden prerequisites; preserve an intelligible result when none is missing. |
| Rehearse a wrong summary | A reader concludes [plausible interpretation]. Where could the artifact help them distinguish it from its claim? | Tests communication; the hypothetical reader is not evidence that anyone actually made that mistake. |
| Compare neighboring work | Which conclusion or structure could be exchanged between these items without changing their meaning? | Finds hollow templates across a collection; shared structure can also serve a real purpose. |
| Apply the rule to itself | Does this artifact meet the standard it asks others to meet? | Finds self-exemption; establish that the same scope really applies. |
| Try the normal copy | Use the supplied template at its documented destination and follow the promised next command. Where does it work or stop? | Tests the actual adoption path, including declared relocation, metadata and dependencies. |
| Remove a premise | What remains supported if the decisive assumption is false or one cited source is unavailable? | Finds the load-bearing claim and useful fallback; do not pretend the changed condition is real. |
| Change the standpoint | What would the actual reader, operator, competing explanation or affected person contest? | Opens another question; same-context role-play remains same-context evidence. |
| Challenge attention cost | Which part earns the reader's time, and which part could go without losing the useful result? | Tests value and subtraction. Charged framing is a deliberate stress probe whose accusations still need checking. |

## Turn answers into a decision

Check a consequential claim at its named source or actual boundary. Separate
execution failures, missing inputs, uncertainty and observed defects. Return
the first wording alongside any correction. Trace a systemic finding to the
default, schema, instruction or workflow that induces it; a local sentence
problem may need only a local correction.

Choose a supported action, a bounded further investigation, an actual owner
decision or a sufficient stop under the [existing authority](../contracts/governance-decision-boundary.md#delegated-engineering-work-proceeds-by-default).
Keep implementation and finding closure with their owner. Repeating a finding
does not carry out its repair. Retain a useful question or trick at the next
matching task entrypoint and replace redundant advice when it no longer helps.

These methods combine the owner's same-task review and external-consumer trial
with selected reported experiments from a neighboring project. The
[transfer record](../evidence/2026-10-28-review-method-transfer.md) identifies
the source scope and limits. Evidence supports useful choices in those cases,
not a universal ranking of prompts or guaranteed detection rate.
