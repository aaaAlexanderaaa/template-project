---
doc_type: evidence
status: historical
authority: evidence
last_reconciled: 2026-10-28
subject: public-task-method-research
---

# Public task methods and what this template should learn

## Finding and requested outcome

Public practice supplies concrete task techniques that can improve the current
CheatSheet. The useful contribution is the specific intervention: how to choose
the next question, preserve a failure signal, generate meaningfully different
designs, observe understanding, or repair the working environment. The current
collection should gain those mechanisms and grounded cases before gaining more
task headings. This is the researcher's recommendation, not a newly adopted
rule or a claim of measured superiority.

The owner requested online research after questioning whether the new
CheatSheets came from external practice, historical experience, project rules
or implementer invention. They named `grill-me` as an example while preserving
the broader common-task scope. This report investigates public sources and
compares them with the existing collection. It does not install the sources,
execute their instructions, or change current task authority.

## Sources and evidence strength

The [source inventory](2026-10-28-public-task-method-sources.json) records URLs,
actual reading scope, version limits, discovery and failed retrievals.
Research followed primary repository artifacts, a named maintainer's posts,
relevant change diffs, an evaluation design and provider guidance. Catalogs and
search snippets supplied leads only. Many files belong to one maintainer's
collection and do not represent independent confirmations.

Three distinctions determine what these sources support:

- An inspected procedure establishes what the public method instructs.
- A maintainer's incident account establishes a reported experience; its
  underlying transcript and outcome may remain unavailable.
- A comparison harness or suite establishes an evaluation design. It does not
  establish a numerical benefit without the relevant results and conditions.

Repository ownership and a human coauthor do not establish that every line was
human-written. Some inspected commits explicitly list an AI coauthor, and the
gstack sections identify themselves as generated. Their concrete instructions
are inspectable; claims about actual benefit retain their separate evidence
status. The method recommendations below are this researcher's adaptations.

## Useful techniques from public practice

### Work the current decision dependencies

Matt Pocock's current `grill-me` is a small user entrypoint calling shared
`grilling`. The method asks prerequisite-ready decisions in rounds, recomputes
the remaining dependencies and separates investigable facts from human choices.
The [round-based change](https://github.com/mattpocock/skills/commit/a4b2009a1a3ac9575506c10b4c84f08f9bba7a38)
replaced a one-question rhythm and retired a separate batching experiment.
This establishes an actual method revision, not measured latency savings.
[Shared method](https://github.com/mattpocock/skills/blob/main/skills/productivity/grilling/SKILL.md).

For this template, work the existing
[decision frontier](../guides/project-operation.md#work-a-dependent-decision-frontier):
if retention depends on the chosen storage model, settle that dependency before
asking for a retention setting. A settled independent choice can proceed in
the same round. Existing authorization and local engineering discretion remain
with their current owners.

A more concrete experience appears in the
[self-interview repair](https://github.com/mattpocock/skills/commit/e5932a7a47e5cae312c1b814ce6194b09aa27be1):
the maintainer's record reports an agent answering its own design questions
when the interview was composed into another workflow. The shared method was
changed to separate facts the agent obtains from decisions the human answers.
This is a reported failure plus an inspected change, rather than an original
session independently revalidated here. It illustrates why a short method's
consumer context matters as much as its standalone wording.

### Change the evidence when conversation cannot settle the question

Pocock's [usage cautions](https://www.aihero.dev/things-people-get-wrong-with-grill-me-and-grill-with-docs)
distinguish questions answerable in conversation from questions needing a
prototype or concrete experience. They describe handing an unresolved question
to a prototype and returning with observations, while warning about excessive
scope and prolonged questioning. These are practitioner recommendations, not
validated universal context-window or throughput thresholds.

The transferable move is to state the unresolved property and obtain the
appropriate observation. A question about the feel of a workflow needs an
experience of that workflow. Rephrasing the interview repeatedly adds little.
The existing experiment and frontend owners still govern any trial.

### Keep the reported failure observable while shrinking the reproduction

[Pocock's diagnosis method](https://github.com/mattpocock/skills/blob/main/skills/engineering/diagnosing-bugs/SKILL.md)
starts with an executable signal sensitive to the reported symptom, reduces
inputs and steps while that signal still fails, gives hypotheses distinguishable
predictions, then rechecks the original larger case after correction. It also
tags temporary instrumentation for removal.

This improves the current generic failing-boundary card with a specific move:
remove one suspected prerequisite, rerun the same observation, and preserve
what still causes the failure. An intermittent incident needs an honest
reproduction-rate limit; the source's percentages, fixed hypothesis counts and
timing examples are not portable acceptance thresholds.

[Superpowers' tracing example](https://github.com/obra/superpowers/blob/main/skills/systematic-debugging/root-cause-tracing.md)
adds a concrete reported case: an empty directory value reached a git operation
through several callers. The useful lesson is tracing the bad value back to
its producer rather than patching the final operation. Its stated test totals
are the author's account, not a run repeated here.

### Split delivery through behavior and declare real dependencies

[Pocock's ticket method](https://github.com/mattpocock/skills/blob/main/skills/engineering/to-tickets/SKILL.md)
forms independently verifiable slices across the needed layers and records
their blocking edges. It treats a wide mechanical refactor separately, with
an expand/migrate/contract sequence or an explicit integration boundary.

For the template, the practical question becomes: what complete behavior can
this step make observable, and what actually prevents it from starting? A
separate API, UI and test ticket does not automatically make a useful slice.
The target's coherent-end-state and compatibility owners govern intermediate
states; the source's tracker setup, publication and per-breakdown approvals
are not prerequisites for a local task.

### Generate alternatives by changing a real design constraint

[Design It Twice](https://github.com/mattpocock/skills/blob/main/skills/engineering/codebase-design/DESIGN-IT-TWICE.md)
gives separate designers contrasting objectives such as a minimal interface,
flexibility or an easy common case, then compares caller examples and trade-offs.
This supplies a concrete way to obtain alternatives that differ substantively.

Use it when a consequential design is stuck around one proposal. Keep the
original purpose and binding constraints common; vary the specific objective
that could reveal another solution. Existing comparison and delegation owners
select the execution strategy. A fixed worker quota and same-model agreement
are not evidence of better design.

### Test what an abstraction earns before removing it

[Pocock's design reference](https://github.com/mattpocock/skills/blob/main/skills/engineering/codebase-design/SKILL.md)
asks what complexity would return to callers if a module disappeared. This is a
useful concrete probe for the existing simplification card: preserve behavior,
trace the caller obligations, and compare the resulting whole.

The related [architecture survey](https://github.com/mattpocock/skills/blob/main/skills/engineering/improve-codebase-architecture/SKILL.md)
prioritizes experienced friction and changed areas. Its prescribed HTML report,
exclusive vocabulary and automatic delegation are source-specific packaging.
The template should preserve its own language, task scope and evidence form.

### Repair the environment using the actual session

[Pocock's retro](https://github.com/mattpocock/skills/blob/main/skills/engineering/retro/SKILL.md)
looks through primary session material for navigation problems, unwired checks,
mechanical mistakes, ineffective instructions and expensive retrieval. It favors
deterministic enforcement for mechanical patterns and identifies instructions
that produce no behavior change.

This turns the existing experience card into a useful investigation: follow
one recurring mistake to the exact missing pointer, default or guard, check
whether an equivalent facility already exists, and change that surface. The
source's proposal that implementation need not load coding standards conflicts
with this template's activated mandatory reading; that division should not be
imported. A retro's output remains recommendations until authorized execution.

### Check understanding against a concrete predicted outcome

A different [grill-me by Joshua Wheelock](https://github.com/joshuawheelock/grill-me/blob/main/skills/grill-me/SKILL.md)
is a code-comprehension quiz. It traces implementation, asks a focused behavior
question and grades the answer semantically against the inspected code. Its
[README example](https://github.com/joshuawheelock/grill-me#see-it-in-action)
illustrates mistaking atomic file replacement for safe concurrent event append.
The example is a reported account, not a concurrency failure reproduced here.

For project understanding, ask what happens under a concrete trigger and
verify the answer at the relevant boundary. Code establishes actual behavior;
the current contract establishes intended behavior. A mismatch may expose a
code defect, a misunderstanding or an unresolved contract, rather than making
the implementation the authority on desired behavior. This is distinct from
both design interviewing and this template's problem-finding Grill role.

### Match the instruction to the observed failure

[Superpowers' skill-writing method](https://github.com/obra/superpowers/blob/main/skills/writing-skills/SKILL.md)
separates ignored obligations, wrong output shape, missing structural elements
and conditional behavior. It pairs them with different instruction forms and
proposes testing against a no-guidance baseline. Its reported wording comparison
was not independently reanalysed here.

For this template, compare actual work before and after a candidate method.
Judge task success, omissions, human correction and effort alongside compliance.
The source's fixed repetition counts, blanket deletion instructions and
no-exception ceremony are not adopted. The strongest new task is to learn
whether a proposed recipe changes a real failing decision at all.

### Let the purpose select the kind of inquiry

gstack separates [startup diagnosis](https://github.com/garrytan/gstack/blob/main/office-hours/sections/phase-2a-startup-diagnostic.md)
from [builder exploration](https://github.com/garrytan/gstack/blob/main/office-hours/sections/phase-2b-builder-brainstorm.md).
The former asks about existing user workarounds and actual unassisted use; the
latter explores surprising uses and concrete things worth trying. This supplies
a useful distinction for a template serving commercial, learning and creative
work. Neither revenue nor novelty should silently replace the owner's purpose.

One practical task is to observe someone using the artifact without the
author's rescue, then investigate a consequential mismatch. Another is to
combine a capability with a different activity and make one concrete trial.
The source's forced discomfort, required payment framing, persistence after
impatience, telemetry and external-tool machinery remain outside the proposal.

## What this changes in the current CheatSheet assessment

| Existing part | Assessment and useful next revision |
|---|---|
| Clarify intent | The existing SOP already owns dependent decision sequencing. Add a worked dependency case and a clear route to it, rather than another general interview rule. |
| Diagnose a failure | Keep the current boundary and sibling checks; add failure-sensitive observation, minimization and rechecking the original case. |
| Compare alternatives | Add contrasting design constraints and caller examples so another agent can construct genuinely different proposals. |
| Understand or explain a project | Add prediction against actual behavior and an appropriate reader task; keep a quiz optional and never turn every explanation into an exam. |
| Retain experience | Use an actual session to identify the responsible default, retrieval path or guard. Saving another lesson is weaker than fixing the next matching action. |
| Expand the library | Require a useful method contribution rather than a new heading. Keep general recipes as navigation; prioritize specific cases that change decisions. |

[Anthropic's authoring guidance](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices#evaluation-and-iteration)
recommends observing representative tasks without the skill, adding minimal
instructions for real gaps, and testing related use with another instance.
Its concision guidance asks what the model already knows, and its navigation
guidance examines missed references. This supports prioritizing a real gap and
retrieval failure over exhaustive generic explanations; it is provider guidance,
not a comparative result for this project's recipes.

## Recommended next work and evidence needed

First, choose one real recurring task where the current approach fails or costs
the owner effort. Preserve that baseline, extract a concrete method from these
sources and relevant authorized history, and compare a later matching task.
Keep original goal, actual evidence, important context and evaluation criteria
comparable. Use a countercase where the method should add no burden. Record
rescues and failures, not only successful output.
Both comparison arms retain governing authority, the required core and complete
activated detail. Vary the optional method whose contribution is being tested;
disclose other changes instead of crediting that method for the whole result.

The strongest feasible alternative is to replace the whole collection with an
external framework. That would supply more packaging immediately, but would
also change authorization, reading, tool and workflow defaults that already
have owners here. Selective transfer better preserves the target's established
boundaries. Another broad rewrite of all twelve prompts would improve their
surface without first resolving which changes earn their place.

The public [Superpowers evaluation suite](https://github.com/prime-radiant-inc/superpowers-evals/blob/main/suites/conversation_routine_use.yaml)
declares stock and treatment comparisons. Its
[evaluation README](https://github.com/prime-radiant-inc/superpowers-evals#conversation-author-to-report-workflow)
describes private criteria and deterministic checks. These are useful design
references; no associated numerical results were evaluated or rerun here.
Successful compliance and useful outcomes remain distinguishable.

## Limits and stopping judgment

This research identifies concrete mechanisms, source-specific excesses, current
coverage and a justified next investment. That is sufficient for the requested
investigation. Further prompt catalogs would mainly add variants; the remaining
uncertainty concerns target-task effects and historical applicability.

The study did not mine the owner's full historical conversations, install a
framework, run external scripts, disclose project content to another agent
service, or conduct new effectiveness experiments. Public repositories are
rolling sources except where a specific commit is supplied; the pinned grilling
version and current main differ slightly and are not claimed identical.
The source inventory retains access failures and partial reading boundaries.
This report supplies researched candidates and a concrete assessment, without
retroactively changing the origin or evidence status of the existing recipes.
