---
doc_type: plan
status: completed
authority: planning
last_reconciled: 2026-10-28
implements: [docs/contracts/development-discipline.md, docs/contracts/agent-execution-discipline.md, docs/contracts/documentation-harness.md]
supersedes: []
---

# Reliable rule reading and useful delivery

Owner correction, 2026-10-28: this completed design record narrowed the
implementation's acceptance toward visualization. The owner rejected that
substitution. Its portable source-reading decisions remain inputs for the
[current template implementation](2026-10-28-rule-reading-implementation.md);
its visualization trial and earlier completion judgment do not bound the
original template-improvement request. Read that current plan for scope.

## Decision and intended result

Keep the existing owners of purpose, authority, engineering behavior and
verification. Give tasks an explicit route to their complete applicable rules,
teach the important decisions through worked examples, and judge delivery by
what the intended user can accomplish. This connects the template's existing
discipline to the moment an agent chooses and evaluates its work.

The selected design adds a small rule-reading command, explicit reading units
inside existing owners, and a worked visualization procedure. The first
behavioral trial uses the original request to understand this repository's
structure and progress. A successful trial produces a usable explanation,
traceable evidence and a justified completion decision.

The current assignment ends with an implementation-ready design, a peer review
and repository validation. The implementation sequence below describes the
subsequent change; current contracts continue to own operative behavior.

## Owner request and current basis

The owner authorized design on 2026-10-28 after identifying these needs in the
preceding conversation. This is an English rendering of that feedback:

- Explain both the overall purpose and the practical choices a rule teaches.
- Make applicable detailed rules reliably available, even when general rules
  already appear comprehensive. Distinguish scope, authority and importance.
- Preserve mission, purpose and intended results as work becomes goals, tasks,
  measurements and procedures.
- Make decisions, explain which problems a change solves, and name a useful
  point of success.

Baseline: clean working tree at `fa01192`. The current entrypoint routes tasks
to domain rules. [Task context](../README.md#task-context) already preserves
purpose and applicable constraints; [execution depth](../contracts/agent-execution-discipline.md#risk-selects-the-execution-depth)
preserves activated boundaries on every route; [outcomes before means](../contracts/development-discipline.md#outcomes-before-means)
preserves the original request at closure. The
[checker](../contracts/documentation-harness.md#purpose) validates structure and
declared relationships. These are useful foundations for the change.

The observed visualization failure had two distinct mechanisms. The initial
version emphasized document categories. The revision emphasized file coverage
and tested interactions, even after the relevant analysis rules had been read.
The user still lacked a useful explanation, and the inline delivery failed to
load. Reading reliability and the effect of rules on judgment therefore need
separate acceptance evidence.

This design changes documentation and a local reading interface. Authorization,
isolation and product state remain with their existing owners. The proposed
implementation is material governance and tooling work with recoverable local
effects. Its classification follows the
[existing risk rule](../contracts/agent-execution-discipline.md#risk-selects-the-execution-depth).

## Rule ownership and reading boundaries

### Keep the distinctions independent

| Decision | Owner | Practical meaning |
|---|---|---|
| Who may decide or grant an exception | Existing governance and behavioral owners | A plan consumes authority; an authorized exception identifies its exact scope |
| Which concern applies | Development's existing concern routing table | Judge the requested result, actual actions and produced artifact, including work outside the checkout |
| Which text must be obtained | The rule's owner declares a complete reading unit | Read all applicable conditions, actions, exceptions and acceptance requirements together |
| How strongly it binds | The operative rule and its exception policy | A local mandatory requirement can constrain a global default |
| What demonstrates success | The outcome and verification owners | Source delivery, correct application and user benefit have distinct evidence |

Global guidance carries the original purpose, authority, evidence discipline and
the route to further rules. Domain rules enter before a decision that depends
on them, including analysis and design before implementation. Methods and
examples enter where they help make that decision. Provenance and history
remain available for disputes, reconciliation and recovery.

### Declare complete units in the existing owners

Use paired Markdown comments around an operative unit. Its stable identifier
is local to its source file. Ordinary heading links navigate into the unit:

```text
<!-- required-reading: frontend -->
## Frontend development contract
...the complete current section and its subsections...
<!-- /required-reading: frontend -->
```

The owner places each boundary around the whole applicable decision: purpose
and scope where needed, requirements, exceptions, failure handling and
acceptance. A dependency that lives elsewhere is an explicit required-reading
link, using this exact directive outside fenced examples:

```text
- required-reading: [Concern routing](../contracts/development-discipline.md#activate-concerns-instead-of-expanding-ceremony)
```

Markdown link paths are relative to the containing document; command-line
owner references are relative to the repository root. The reader follows
declared dependencies until the required set is complete. Ordinary citations
remain navigation. The normal entrypoint contains
one directive to task context; that unit requires authority order, language
style and concern routing. These references declare the common reading set at
its existing owners. A target heading resolves to its enclosing declared unit;
an unmarked target resolves to the full document. The file path and declared
identifier establish unit identity independently of the displayed heading.
The checker catches renamed or missing navigation anchors.

The first declarations cover task context, authority order, language style,
concern routing, the frontend contract and the operative data-analysis body
through acceptance evidence. Data-analysis provenance stays outside that body. Other referenced
owners use their full document until they declare a narrower complete unit.
This provides a working default for every existing concern during adoption.

Development's existing routing table gains a `Required reading` column. Each
cell links to declared units and names any required project-specific binding
as `owner:CONCERN-SLUG`. Concern slugs come from the concern labels using the
existing heading-slug convention. The trigger remains in the existing
`Change trait` column. `AGENTS.md`, guides and
templates point to that table; a generated view may repeat its navigation.

The table can select an existing owner by reference. A project-specific owner,
such as a surface or interface contract, is resolved from the current task and
architecture. The task records that binding alongside its existing concern
entry. Missing applicable authority follows the existing contract-first route.

### Obtain the required text through one local command

Add `scripts/read_rules.py` with three operations. These are proposed interfaces:

```text
python3 scripts/read_rules.py list
python3 scripts/read_rules.py prepare --concern experience --concern analytical-claims --owner experience=docs/design/project-map.md
python3 scripts/read_rules.py read --unit docs/contracts/data-analysis-discipline.md#data-analysis-discipline --digest EXPECTED
```

`list` prints the current routing rows and their reading targets. `prepare`
reads the entrypoint's required-reading directives, adds selected concerns and
project-specific bindings, follows explicit dependencies and removes duplicate
units. One call reads the selected sources into an immutable content set,
rechecks their identities, and emits both the inventory and every complete
unit, ending with an aggregate completion marker.
Each source has its path, unit identity, heading, authority, lifecycle, digest
and byte count. A detected concurrent source change aborts preparation for
renewal. The identities describe the obtained content and support later
revalidation.

The normal entrypoint requires preparation before a choice depends on an
activated concern. Previously obtained units can be reused under the validity
conditions below. The call transcript and complete output are the task's
source-delivery record; the existing task context carries consequential
choices and their evidence. A routine lookup uses its current common context
and reads the requested facts directly.

`read` is the recovery operation: it emits one unit against the expected
snapshot digest, with explicit start/end markers. Repeated `--owner` options
bind project-specific contracts through repository-relative references.
Multiple applicable owners can bind the same concern. Binding checks the
required document role, normative authority, lifecycle and surface or interface
identity against current architecture and accepted task scope. The example
surface path above is created as that trial's surface contract before its
implementation. A command argument identifies a source; the governing owner
and task authorization establish its authority.

For the trial, the current Experience row selects the frontend unit and its
surface owner; Analytical claims selects the data-analysis unit. Both apply
to the interactive explanation. A request to find a file selects the direct
lookup route. These cases also test selection itself, including omission of
one required concern and selection of an unrelated one.

The command reads Markdown and resolves local links. It executes no commands
from a rule. Paths stay within the checkout. It detects missing targets,
unclosed or duplicate units, dependency cycles, unsupported lifecycle states
and unresolved required owner bindings. A failure names the affected unit and
the source that needs correction. Target rules are identified as future
behavior and included only through `prepare --target REFERENCE` for the
governed change; historical and superseded material remains reference material.

The agent selects concerns from the requested result and observed actions.
The command provides resolution and complete source output for that
selection. Semantic selection remains an engineering judgment: when scope is
unclear, inspect the relevant scope and trigger rather than infer an exemption
from the summary. A changed task is checked for newly applicable concerns.

When the host truncates prepared output, use `read --part N --part-size BYTES
--digest EXPECTED` to obtain a unit as numbered transport parts. Parts reassemble
to the exact unit text; the size controls transport only. A digest mismatch
requires a new preparation. Each response identifies its part and whether it
is the last part. Parts preserve UTF-8 characters and the original text when
reassembled. The agent obtains every part before dependent work. Tool truncation, a missing
part or a changed source causes a re-read of the affected unit. This output
record supports a claim about source delivery; application is demonstrated by
the resulting decisions and artifacts.

The host's transcript establishes whether the entrypoint route was followed.
The portable command supplies text and structural checks; host-specific hooks
can later enforce invocation where the host supports them. The behavioral trial
observes invocation through the normal route before claiming reliable use.
Owner review checks semantic completeness when requirements or unit boundaries
change; syntax validation checks markers, heading coverage and dependencies.

Reuse a unit while its source digest, applicable scope and retained context
remain valid. On a handoff or context restart, carry the original purpose,
selected owner references and outstanding evidence in the existing handoff.
The receiving context obtains the necessary operative text again.

## Preserve purpose through decisions and delivery

### Carry the reason for the current task

Keep a short account in the existing task context or plan: the original
request, the intended user result, the selected interpretation and its reason,
material scope choices and the evidence required for completion. Link the
original decision when work is handed off or converted into a specification.

Purpose guides long-term choices. A stage goal selects a useful change within
it. Measurements observe selected effects; procedures help produce and check
them. Each translation retains its parent reason and identifies consequential
assumptions. A change to intent or accepted scope returns to the authorized
decision owner. Ordinary execution carries the relevant purpose and boundaries;
direction reviews examine the wider mission and alternatives.

Use this concrete task account for the visualization trial:

> The owner wants to understand how this engineering-discipline template works
> and what progress has been achieved. The explanation should connect the
> overall purpose, a real task's path through the rules, and implementation and
> verification evidence. The selected presentation combines those views and
> keeps source access nearby. File coverage supports an inventory claim;
> reader use and delivery observations support the understanding claim.

This account stays with the work as it becomes a surface contract, artifact
and verification report. The applicable existing templates carry it in their
current outcome and source fields.

### Teach judgment with a worked visualization procedure

Add `docs/guides/project-visualization.md`, linked from the existing guide
index and concern route. It explains the actual choices below and links to
the normative owners.

| Work | Concrete action in this repository | Useful result |
|---|---|---|
| Establish the question | Recover the request for structure and progress; inspect repository purpose, current owners and relevant implementation evidence | A supported account of what the template changes in engineering work |
| Find explanatory relationships | Follow a real bounded task from user intent through authority, activated rules, execution and verification | Relationships with named meanings and sources |
| Explain progress | Connect current and target commitments to implementation and verification evidence at the observed revision | A reader can distinguish achieved capability, a documented rule and a remaining evidence gap |
| Build the main view | Show those relationships and progress together, with source access and a file index where useful | The default view answers the reader's question |
| Check use and delivery | Have a fresh reader use the artifact; exercise loading and the required interactions in the delivery environment | An explanation the reader can actually use |

The guide includes a finished example and explains what made it useful. Its
sources support each selected relationship. The file-location countercase
uses the same repository to serve a maintainer finding files; its main view
is an index. The contrast teaches how the reader's task changes selection.

The explanation begins with material such as this, developed against the
observed revision:

> This repository supplies engineering discipline for agents and maintainers.
> It helps a requested change reach a coherent result by making purpose,
> decision authority, engineering boundaries and completion evidence explicit.
> Adoption transfers those practices into a project's existing owners.
>
> Consider a request for an interactive explanation of project progress. The
> owner sets the desired understanding. The agent researches current facts,
> identifies the applicable interface and analysis rules, and defines the
> explanation and its evidence before building the view. Verification checks
> the actual artifact and its delivery, including whether a reader can explain
> the project from it. A correct file index serves a different, useful task:
> finding the relevant material.
>
> The repository already contains a runnable documentation checker for metadata,
> source citations, lifecycle and local relationships. Its contract records
> implemented and enforced status. Development and agent execution also record
> implemented discipline, with partial verification. This gives a concrete
> distinction between a working structural check and behavioral effectiveness
> that must be established through real use.

The sources are the [entrypoint](../../AGENTS.md),
[adoption value order](../contracts/project-adoption.md#transfer-value-is-ranked-before-its-carriers),
[concern routing](../contracts/development-discipline.md#activate-concerns-instead-of-expanding-ceremony),
[verification](../contracts/development-discipline.md#verify-promised-and-observed-behavior-in-both-directions),
and the current metadata and implementation of
[the harness](../contracts/documentation-harness.md),
[development](../contracts/development-discipline.md) and
[agent execution](../contracts/agent-execution-discipline.md).

When feedback says the result is confusing, inspect the existing explanation
against its sources and the reader's task. Strengthen the research when the
explanation lacks support; revise the presentation when it fails to convey a
supported account; repair the delivery path when the artifact fails to open.
Recheck the affected result after the correction.

### Make a decision and name success

The existing language owner and Grill procedure will teach a positive decision
with reasons: what works, what the result enables, which correction deserves
attention and what observation establishes a sufficient result. Place a
material uncertainty beside the claim it limits and identify its consequence.
Close the bounded task when its acceptance evidence supports completion.

Grill examines the original purpose, the actual artifact, the strongest
alternative and the assumption that could change the decision. Its verdict
can retain a sound choice, select a correction or identify an owner decision.
Use the current role and independence boundaries. A mandatory review keeps its
existing authority; ordinary self-checks stay inside the task.

## File changes and implementation order

| Order | Existing owner or proposed file | Result |
|---|---|---|
| 1 | `docs/README.md` task context and language style | Own complete-reading semantics, independent rule distinctions and clear decisions with sufficient completion evidence |
| 2 | `docs/contracts/development-discipline.md` concern routing, outcomes and verification | Declare targets at the current trigger owner and retain the original purpose through the actual result |
| 3 | `docs/contracts/data-analysis-discipline.md` and development's frontend section | Declare complete operative units at their current owners |
| 4 | `docs/contracts/documentation-harness.md`, `scripts/read_rules.py`, `scripts/check_docs.py`, `tests/test_read_rules.py`, existing checker fixtures | Specify and implement source resolution and structural validation, including complete units and explicit dependencies |
| 5 | `AGENTS.md`, `docs/guides/README.md`, `docs/guides/project-operation.md`, `docs/guides/grill.md`, `templates/agent-execution-plan.md`, `templates/handoff.md`, `templates/verification-report.md` | Reconcile navigation and existing fields with the changed owners; retire redundant projections |
| 6 | `docs/guides/project-visualization.md` and the trial's surface and evidence records | Supply a usable procedure, a finished example and observations of the reader's task |

Update the normative owners before the dependent command, projections and
guide. Inspect the relevant units before editing them. Keep machine checks at
the harness owner and judgment standards at their current behavioral owners.

The chosen approach supports current Markdown navigation and adds deterministic
resolution. A prose-only entrypoint costs less initially but leaves source
delivery to the same discretionary step that failed. An always-load-everything
profile spends every task's context on unrelated domains and history. The
selected units concentrate complete requirements where they apply, while
ordinary lookups keep their direct route.

## Acceptance and failure recovery

### Structural and command checks

Fixture tests exercise complete units, owner bindings, dependencies, fenced
examples, duplicate removal, lifecycle selection, path containment, partial
output and source changes. Ordinary heading links remain valid. The checker
validates declared relationships; it leaves purpose and taste to the relevant
artifact and reader evaluation.

Source-resolution failure pauses the dependent claim and names a repair at its
owner. Other authorized work continues. If the command is unavailable, read
the same declared units directly and retain their identities in task context.
If the delivery environment fails, use an observable diagnostic and a usable
alternative delivery where available, then establish the affected claim in
that environment.

### Behavioral trial

| Case | Observation that establishes the result |
|---|---|
| Rich global guidance plus a visualization request | The execution record contains the complete applicable frontend and analysis units before their dependent choices |
| Complete rules have been obtained | The produced explanation follows a meaningful relationship and its sources; file coverage serves its stated inventory purpose |
| An apparently complete specification weakens an earlier decision | Comparing it with the original request exposes and corrects the changed meaning |
| Technical checks pass while the reader remains confused | The completion decision follows the reader result and identifies a concrete research or presentation correction |
| A local preview works while actual delivery fails | The delivery result drives the recovery action and the completion claim |
| A maintainer asks to locate files | An efficient lookup or index succeeds through the routine route; compare extra reads, planning, reviews and elapsed effort with the current baseline |
| A fresh context continues the work | It recovers the original purpose, relevant rules and next action from the normal entrypoint and handoff |

Compare the current route with the revised route on matching tasks, retaining
the initial artifacts, source identity, reader observations and actual effort.
Check both the motivating failure and the ordinary file-location case. The
source-delivery check and the reader task support different claims.

Give the independent reader only the delivered artifact and ordinary usage
instructions. Ask them to explain what engineering behavior this template
changes, follow a concrete task through the applicable rules and verification,
and distinguish achieved capability from documented commitments using the
provided sources. Evaluate the meaning of their answers against the observed
repository evidence. A supported answer identifies the relationships and their
sources and recognizes a material unsupported conclusion. The current owner
retains judgment over the intended value and experience.

Test actual loading and required interactions separately in the target delivery
environment. Record the reader's answers and the environment observation in the
existing verification report, alongside the source-delivery transcript and
artifact decisions. These establish three concrete results: the rules reached
the agent, the artifact follows them, and the user receives a useful result.

Adopt the owner changes and supporting command as one coherent change. During
integration, direct reading supplies the same complete units. Reconcile the
entrypoint, tool and guides before calling the new route ready.

### Completion decision

This implementation succeeds when the ordinary task entrypoint leads to the
complete applicable rules, those rules inform the produced explanation, and a
fresh reader can use the delivered visualization to explain how the template
works and what progress its evidence supports. A complete file index remains
useful for the separate location task.

That result makes the visualization route ready for continued use and provides
a tested example for other domains. Repository integration also passes Python
3.11 or newer unit discovery, the documentation checker and whitespace checks.

## Design review and closure

A separate Chatgptbox conversation reviewed the complete initial proposal and
bounded task context. The [review record](../evidence/2026-10-28-rule-design-review.json)
preserves the exact input, its digest and the returned judgment. The reviewer
retained the architecture and requested concrete corrections. The revised
design makes these decisions:

| Review issue | Adopted decision |
|---|---|
| Resolution could be followed by incomplete reading | Use one `prepare` operation to resolve and emit the complete selected set; validate expected digests during recovery |
| Perfect concern selection and supplied owner authority were assumed | Specify overlapping Experience and Analytical claims, exercise missed and extra concerns, and validate owner role, lifecycle, identity and task authority |
| Unit identity depended on mutable headings | Use a stable local unit identifier with ordinary heading navigation; treat multipart output as truncation recovery |
| The example promised an explanation without showing one | Include the concrete purpose, task path and evidence-status explanation above |
| Reader success lacked observable answers | Require source-supported answers about purpose, task flow and achieved progress, plus a separate target-environment observation |
| Simple tasks and migration needed protection | Compare the direct lookup's actual effort and adopt owners, command and projections as one coherent change |

Design integration also exposed the fixture clock's coupling to the live
checkout. The existing fixture baseline advances to 2026-10-28. Inherited open
commitments use that date only inside copied fixtures; each aging scenario
adds its own records. Checks against the real checkout retain the actual
deadlines. The existing promise-aging tests continue to exercise the real
checker policy.

The selected design is ready for implementation. The design task is complete:
the ownership boundaries, normal and recovery interfaces, worked explanation,
file changes, adoption order and task-specific success conditions are specified.
The peer review's material corrections are incorporated. The future behavioral
trial evaluates the implemented route and its delivered visualization.

Final validation used Python 3.14.2. All 122 unit tests passed in 28.907 seconds.
The documentation checker passed with 54 canonical documents and 16 templates;
whitespace checks passed. The actual checkout retains its existing overdue
independent-adoption-review advisory. The initial integration checks exposed an
invalid example link and the old fixture date; both were corrected before the
passing run. Changes in this design task consist of this record, its review
attachment and the fixture-baseline repair.

## Sources for the selected mechanisms

- [Superpowers discovery guidance](https://github.com/obra/superpowers/blob/main/skills/writing-skills/references/discovery.md): its reported review example motivates separating machine discovery from the complete procedure.
- [Matt Pocock's documented transfer failures](https://github.com/mattpocock/skills/blob/main/docs/engineering/grill-with-docs.md): explicit dependencies and original decisions need to survive subsequent specifications.
- [OpenAI instruction discovery](https://learn.chatgpt.com/docs/agent-configuration/agents-md): the host's automatic instruction chain has a concrete scope and size limit; local reading must be observed through its own interface.
- [DORA measurement pitfalls](https://dora.dev/guides/dora-metrics/): measurements support improvement and retain their application context.
