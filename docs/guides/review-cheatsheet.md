---
doc_type: guide
status: current
authority: guidance
last_reconciled: 2026-10-28
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

## Common task templates

Replace the bracketed inputs before dispatch. Keep the actual task, permissions,
artifact identity and stop bound explicit. Launch only the selected work within
the available authorization and resources.

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

A fresh directory and `fork_turns=none` establish different facts. Inspect what
the runtime actually supplies: project instructions, global instructions,
history, skills and model settings. Record known inheritance and unknowns;
limited source access is not proof of an empty context. If isolation cannot be
verified, label the observation at its actual strength and use a more suitable
permitted environment when the claim requires it.

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
