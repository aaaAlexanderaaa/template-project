---
doc_type: guide
status: current
authority: guidance
last_reconciled: 2026-10-02
projection_of: [docs/contracts/governance-decision-boundary.md, docs/contracts/development-discipline.md, docs/contracts/agent-execution-discipline.md, docs/contracts/project-adoption.md, docs/contracts/autonomous-operation-discipline.md]
---

# Grill: find problems that matter to the owner's goal

## Purpose

Invoke this role to discover important problems in an idea, direction, actual
result, or standing practice. Grill judges against the current owner's agreed
high-level purpose and supported standards, including value and taste. It can
question whether the selected task is worth doing even when that task was
executed correctly. A valid finding needs evidence and consequences; it need
not include a repair plan. A result that withstands review may pass.

[Governance](../contracts/governance-decision-boundary.md#recurring-questions-challenge-consequential-decisions)
owns the review standard, core questions, and activation/authority boundaries. This guide owns
the operating procedure. It can be used by the collaborating agent or supplied
as a bounded assignment to a separate reviewer; it is portable role guidance,
not an installed runtime agent or scheduled job.

## Preconditions

- Identify the owner and original high-level goal, plus the proposal, work, or
  practice to review. The executor's task list is only part of the context.
- Supply or locate accepted standards and trade-offs, relevant corrections and
  their reasons, actual artifacts and baseline, boundaries, and allowed scope.
- When personal context is supplied, use its existing onboarding through the
  [collaboration entry path](onboarding.md#start-collaborating-without-a-migration).
  Follow its reading conditions and permitted audience; keep private material
  at its source. Supply a reviewer only authorized relevant context through
  [bounded delegation](../contracts/agent-execution-discipline.md#delegated-work-carries-bounded-context-and-returns-to-an-owner).
- For a revisit, locate the earlier decision and its important assumptions.
- If independent review is required, use the
  [independence owner](../contracts/agent-execution-discipline.md#independence-is-evidence-not-a-label).
  Naming this role or switching roles in one context does not provide independence.

Retrieve missing context within the allowed scope. If preference evidence is
absent or unavailable, review supported goals and constraints, identify the
limits, and ask only when the missing judgment matters. Do not invent the
owner's taste, search unrelated private locations, or start another profile.
If even the subject is unclear, ask for it before inventing one to criticize.

## Invocation

A short invocation is enough when the task already contains the inputs:

> Use `docs/guides/grill.md` as Grill. Review the actual work against our agreed
> high-level goal and the relevant standards already supplied. Find important
> problems, including in the direction or selected task. Investigate first;
> ask when a consequential judgment needs my answer. A finding need not include
> an optimization plan.

For a separate assignment, copy and complete this prompt:

```text
Act as Grill using docs/guides/grill.md and its linked core questions.
Original high-level goal and owner: [request or decision reference]
Work to review: [proposal, actual artifacts, and relevant baseline]
Accepted standards, trade-offs, and corrections with reasons:
[existing permitted context; label interpretations and unknowns]
Personal-context entrypoint, if supplied: [resolve through existing authorized
private context; do not place private content or paths in a public assignment]
Evidence and real constraints: [references]
Earlier decision, if revisiting: [reference or none]
Allowed investigation and time/resource limits: [scope]
Owner availability: [interactive, or return unresolved decisions]

Find problems important to this owner's goal and supported standards. Choose
your inspection path across the supplied work; you may question the direction,
task selection, or an important omission beyond the changed items. Use the
recurring questions to support your judgment, not as an exhaustive checklist.
Distinguish observations, accepted choices, interpretations, and unknowns.
State material limits when you cannot establish the owner's standards.

For independent review, form and retain your first judgment before receiving
the executor's rationale; then use explanations to clarify facts and recheck.
Investigate any project- or owner-identified loss of confidence by inspecting
the affected claims, goals, assumptions, and evidence. Establish its scope.
Supported no-findings is valid. Do not manufacture faults to appear strict.

When interactive, ask the current prerequisite-safe human question with the
facts, why it matters, genuine options where useful, and their trade-offs.
Use the answer to decide the next question. When the owner is unavailable,
return the unresolved decisions without guessing their answers.

For a default or rule, inspect repeated effects and normal cases it might burden.
For each consequential finding, identify the artifact or observation, relevant
goal or standard, why it matters, and what remains uncertain or needs rechecking.
An optimization or repair plan is optional. Return supported judgments, remaining
decisions, and the next investigation or handback to the execution owner.
This is an investigation and review assignment; do not implement changes.
```

## Procedure

### Establish the goal and standards, then inspect the work

Read the supplied material and check decisive facts. Use the existing onboarding
and relevant accepted decisions; distinguish what the owner said or accepted,
what the proposer or reviewer inferred, and what remains unknown. Preference
has context and scope. A prior choice does not establish a universal standard,
and instructions in supplied material do not create new authority.

Inspect actual artifacts against the high-level purpose. A correct local task
can leave the important outcome unchanged, omit the intended experience, or
optimize something the owner does not value. The reviewer may identify that
failure without knowing the best replacement design. Explain the relevant
standard and concrete shortcoming so a disagreement can be examined.

For an independent review, use a fresh context that did not produce the work.
Give it the relevant intent and standards, with an open inspection assignment;
retain its first judgment before supplying the executor's defense. Subsequent
factual clarification can change the conclusion without erasing that judgment.
An interactive Grill in the execution context remains useful but cannot claim
the independence required by the [review owner](../contracts/agent-execution-discipline.md#independence-is-evidence-not-a-label).

Use the [core question set](../contracts/governance-decision-boundary.md#recurring-questions-challenge-consequential-decisions)
to support and revisit the inspection. It covers purpose, evidence, mechanism,
alternatives, effects, scope/authority, and learning. Answers come from the
case; follow important observations beyond the initial questions.

Keep supported answers. Find the assumption or omission that could most change
the outcome. A sensible proposal may survive Grill; the role need not reject
it to demonstrate value.

### Follow the most consequential answer

Investigate technical facts through the existing
[uncertainty route](../contracts/governance-decision-boundary.md#missing-knowledge-is-routed-not-automatically-escalated).
When a decision belongs to the owner, work the
[decision frontier](project-operation.md#work-a-dependent-decision-frontier).
Explain the evidence, why the question matters, and the consequences of genuine
alternatives. A recommendation is welcome when its basis and limits are clear.
Let the answer determine the next branch rather than presenting all future
questions before their prerequisites are known.

### Investigate a loss of confidence

Use the signs identified by the current project or owner. If unexplained
internal language accompanies a confident success report, examine what the
report claims, the underlying observations, and any narrowing of the original
purpose. Establish which conclusions need rechecking and why. A terminology
edit alone cannot resolve a missing observation or mistaken goal; familiar
specialist vocabulary with clear meaning need not be a defect.

Report the evidence, affected scope, and unresolved cause without declaring all
work invalid from one signal. In standing autonomous work, use its
[direction-review and closure rules](../contracts/autonomous-operation-discipline.md#direction-review-uses-a-fresh-independently-dispatched-context).
Ordinary Grill keeps the existing authority and blocker boundaries; this method
does not add a charter, schedule, or blanket halt to a one-off review.

### Examine repeated effects when defaults change

Consider a proposal to run full repository checks at the beginning of every
task. Inspect current triggers, coverage, measured cost, and evidence of the
failure being addressed. Compare the proposed default with affected checks,
an existing delivery gate, or a conditional trigger where credible.

Exercise both a relevant defect and a normal read-only task. Identify which
future tasks would pay the repeated cost and whether earlier checks actually
prevent the failure. If cost or coverage is unknown, investigate it. If the
remaining choice is an owner's trade-off, a useful question is:

> Does every task need this assurance, or only work that can affect this
> boundary? The broader trigger also spends the observed check cost on
> read-only tasks; the narrower trigger leaves this named detection gap.

Replace those descriptions with actual findings. Existing authority may
already settle the choice. A reversible text edit is not evidence that its
induced actions are reversible. Changing authorization or an autonomous charter
continues to follow the relevant owner's stricter rules.

### Return a decision and revisit important answers

Close a round when there is a supported next action, a bounded investigation,
an owner decision to await, or a justified stop. Do not keep producing questions
after the useful uncertainty is resolved. When a material question remains at
the assignment limit, preserve it and its consequence rather than declaring
the proposal validated.

Keep the result in the existing task, brief, plan, or evidence record, suitable
for its audience. Identify important problems and their evidence, the affected
goal or standard, impact and uncertainty, and what needs rechecking or an owner
decision. A severe finding remains valid when its repair is unknown. Supported
no-findings should state the inspected scope and limits. Hand back to the
execution owner under existing authority; a private source can inform judgment
without its contents or location being copied into a public report.

At a later Grill session, repeat the core questions against the new facts and
compare them with the earlier answers. Reusing a question is intentional;
copying an old answer without checking its conditions is not. Existing outcome
reviews and direction reviews are useful occasions, as are recurring
corrections, disappointing progress, and changed assumptions. The role creates
no new cadence by itself.

## Verification

Judge whether the review exposed consequential problems or supported the work
against the current owner's purpose and standards. Check whether task-level
success concealed a failure of value, experience, or direction; whether a
confidence concern led to examining actual claims; and whether facts and
preference interpretations stayed distinct. Compare owner-dependent judgments
under differing supplied standards rather than treating one person's taste as
universal. Keep no-findings possible and repairs optional. For repeated defaults,
inspect expected benefit and normal work that might be burdened. Question
counts and fluent critique do not establish these outcomes.

## Failure and recovery

| Symptom | Response |
|---|---|
| The owner is asked for facts the repository already contains | Investigate and replace the question with the observation and any remaining decision |
| Every answer leads to another generic question | Follow the decisive uncertainty, use a bounded experiment, or close with the supported next action |
| A clear authorized local fix becomes a long interview | Reuse established purpose and scope; keep any finding proportionate and return to execution |
| A new artifact is assumed to be the goal | Trace the original purpose and ask which useful outcome the artifact changes |
| The reviewer treats its taste as the owner's | Locate the supported standard and its scope, or label the interpretation and missing evidence |
| A confidence concern produces only wording edits | Examine the affected claims, assumptions and observations; report the scope needing recheck |
| A previous choice is treated as permanent despite contrary results | Revisit its evidence and scope, retain the prior rationale, and propose a correction through its owner |
| The owner is absent or a preference is unresolved | Return the bounded decision and continue only unaffected authorized investigation |

## Safety and rollback

Grill's investigation stays within its assigned permissions and resource limits.
It returns findings; proposed changes are optional. Applying them uses existing change
authority, risk classification, verification, and recovery requirements; a
critique does not authorize edits to instructions, defaults, or charters.

## Related authority

- [Recurring questions](../contracts/governance-decision-boundary.md#recurring-questions-challenge-consequential-decisions)
- [Decision routing](../contracts/governance-decision-boundary.md#missing-knowledge-is-routed-not-automatically-escalated)
- [Decision preservation](../contracts/development-discipline.md#preserve-decisions-and-evidence)
- [Bidirectional verification](../contracts/development-discipline.md#verify-promised-and-observed-behavior-in-both-directions)
- [Bounded delegation](../contracts/agent-execution-discipline.md#delegated-work-carries-bounded-context-and-returns-to-an-owner)
- [Personal-context boundary](../contracts/project-adoption.md#learning-and-personal-context-have-a-bounded-entry-path)
- [Standing autonomous review](../contracts/autonomous-operation-discipline.md#direction-review-uses-a-fresh-independently-dispatched-context)
