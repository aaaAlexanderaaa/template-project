---
doc_type: guide
status: current
authority: guidance
last_reconciled: 2026-09-28
projection_of: [docs/contracts/development-discipline.md, docs/contracts/agent-execution-discipline.md, docs/contracts/project-adoption.md]
---

# Research: choose useful observations before committing to an explanation

## Purpose

Use this method for exploratory, comparative, disputed, or consequential
multi-claim inquiry. It helps choose what to investigate, relate evidence to
claims, and return an answer with a defensible scope. The
[inquiry invariant](../contracts/development-discipline.md#unknown-references-are-researched-not-reconstructed)
owns the behavior. A direct fact lookup can remain a source check and answer.

This is a callable role and method, not an installed agent or mandatory
pipeline. The current agent can use it. Delegate only when a bounded assignment
has value under the existing [delegation rule](../contracts/agent-execution-discipline.md#delegated-work-carries-bounded-context-and-returns-to-an-owner).
For difficult retrieval, use [information access](information-access.md).
For a challenge to purpose, standards, or the resulting work, use existing
[Grill](grill.md). The task owner integrates their findings and owns delivery.

## Preconditions

Recover the original question and intended use, agreed scope and constraints,
known evidence, consequential uncertainties, and available resource envelope
from existing task context. Exploration can itself be the intended use; do not
invent a decision the owner has not asked to make. Investigate available facts
before asking for missing intent. Personal standards use existing permitted
context and onboarding; this method creates no new taste profile.

## Invocation

When the current task already supplies its context:

> Use `docs/guides/research.md` to investigate this question. Choose useful next
> observations, follow sources and credible alternatives, and return findings,
> evidence relationships, important gaps, and why you stopped.

A separate worker receives this bounded assignment, completed from the task:

```text
Use docs/guides/research.md as the research role.
Original question and intended use: [owner request or faithful account]
Agreed scope, standards, and current evidence: [permitted references]
Uncertainties to investigate: [known questions; allow important new ones]
Tools, permitted sources, and shared resource/stop boundary: [total time or
attempt allowance across retrieval routes; any additional tool-specific caps]
Existing access knowledge, if relevant: [permitted locator]
Return destination: [task owner or existing artifact]

Investigate rather than merely outline a search plan. Choose subsequent
observations from what you find. Keep source statements, your interpretation,
and supported conclusions distinguishable. Return checkable evidence for
decisive claims, source dependencies, important alternatives and gaps, the
actual stopping reason, and useful access knowledge. Do not change standing
instructions or expand permissions. Report unavailable evidence honestly.
```

## Procedure

### Establish what could change the understanding

Identify the important questions, plausible explanations, and observations
that would distinguish them. For an unfamiliar topic, begin with a provisional
map of relevant people, organizations, terms, events, and evidence types.
Let new material revise that map. Do not force every inquiry into a hypothesis
matrix or a fixed set of dimensions.

For example, a reported increase in sales may reflect greater use, higher
prices, temporary incentives, or a changed measurement definition. Another
opinion about growth may add less than observations that distinguish those
possibilities. Finding a previously missing explanation is useful progress too.

### Explore and change direction from the evidence

Start with sources suited to the question. Follow named entities, original
datasets, references in either direction, terminology changes, and substantive
disagreements. Look across platforms, periods, regions, affected groups, or
methods when those differences could change the answer. Typical, unsuccessful,
and exceptional cases can reveal different boundaries; their relevance depends
on the task rather than a mandatory checklist.

At a branch decision, identify what the next observation could resolve or
uncover. If results repeat the same underlying material, consider a different
source class or search path. A new query string is not necessarily a new
perspective. Preserve significant avenues not reached. Do not substitute many
low-value searches for investigating the strongest unresolved question.

### Keep claims attached to observations

Read the material needed for each decisive assertion. Search snippets and
citations are discovery routes; they do not establish unread content. Inspect
measurement definitions, dates, populations, and the inference from result to
claim when those carry the conclusion. A source's reputation or primary status
does not establish every interpretation made from it.

For work with several dependent claims, a compact table in the existing task
record can help:

| Claim or question | Actual observation and source location | Origin and relationship to other evidence | Interpretation, counterevidence, or limit |
|---|---|---|---|
| What is being established? | What was read or measured, with relevant date/scope | Independent collection, shared dataset, quotation, or unknown dependence | What follows, what does not, and what remains unresolved |

This is an optional representation, not a form for each lookup. One report
quoted by five articles is one underlying observation for that claim; the
articles may still contribute distinct interpretations. Different accounts
or platforms do not automatically establish independent collection. Preserve
unknown dependence rather than assigning a convenient effective-citation score.

### Revisit explanations and decide whether to continue

Compare credible alternatives using observations that discriminate between
them. Look for evidence that would weaken the leading explanation, not just
additional favorable examples. Independence and contradiction are separate:
opposed opinions can share a source, and independent observations can agree.
Do not manufacture a balanced debate when support is unequal.

Temporary synthesis is useful for identifying missing evidence. Keep it
revisable, and let a draft send the inquiry back to acquisition. Before final
delivery, inspect the decisive claims, important alternatives, unexplored
directions, and reading limits against what the answer promises.

Stop for a reason the record supports: the bounded question is answered;
further relevant paths have diminishing returns; needed evidence is
inaccessible; or the authorized budget is exhausted. State the searched scope
and consequential remaining gaps. Lack of novelty within one source cluster
does not prove broad saturation. Do not claim statistical coverage without a
defined population, method, and supporting observations.

### Return the useful result

Choose the output that helps the reader: an answer, evidence comparison,
annotated source list, changed question, or precise unresolved uncertainty.
Rewrite source material when that adds useful explanation, accessibility, or
comparison. New prose is not a success condition.

Provide checkable support for decisive claims and make the strongest remaining
limitation visible. A delegated researcher returns evidence and judgments to
the task owner; several successful workers do not prove a coherent final
answer. Pass reusable access findings to their permitted existing owner through
the [access method](information-access.md#retain-experience-at-the-next-decision-point).

## Verification

Inspect whether the actual work found useful evidence or important omissions,
recognized dependent sources, tested relevant alternatives, and checked the
assertions that determine the answer. Compare the final scope with the original
question. When evaluating this method, retain the actual query/source path,
useful findings, stopping reason, and observed cost proportionately; prose
length, citations, filled fields, and self-scored information gain are not
proof of better research. Exercise an ordinary lookup as a burden countercase.

A standards reviewer may use relevant authorized preference evidence. A fresh
reader receives what the intended reader would actually have. Their different
inputs test different claims; hidden background should not make an unclear
answer pass. Simulated audience reactions remain hypotheses under the existing
[evidence classes](../contracts/agent-execution-discipline.md#evidence-classes-remain-explicit).

## Failure and recovery

| Symptom | Response |
|---|---|
| Many sources repeat the same report | Trace the origin; seek a relevant independent observation or narrow corroboration claims |
| Search stays anchored to the initial words | Follow entities, references, disputed definitions, or a missing evidence type |
| Citation checks pass but the inference is weak | Examine the decisive measurement or reasoning, and revise the claim |
| A source or important section cannot be read | Invoke access work within the remaining budget; expose the gap if unresolved |
| Writing reveals an unanswered question | Return to investigation or narrow the answer; do not fill the gap with fluent explanation |
| The method creates paperwork without useful learning | Reduce the representation or scope at its owner; evaluate the repeated cost before adding a rule |

## Safety and rollback

Current task authority, privacy, and resource boundaries remain in force.
Research findings do not authorize edits to defaults, deployment, new data
collection permissions, or personal-context copying. Stop affected unsupported
claims while continuing independent authorized work. Preserve consequential
negative results; retire obsolete working notes under the existing lifecycle.

## Related authority

- [Inquiry](../contracts/development-discipline.md#unknown-references-are-researched-not-reconstructed)
- [Evidence preservation](../contracts/development-discipline.md#real-content-is-never-deleted-or-fabricated-for-presentation)
- [Causal analysis](../contracts/development-discipline.md#analysis-exposes-the-decisive-causal-mechanism)
- [Resources](../contracts/agent-execution-discipline.md#billed-rate-limited-and-account-bound-resources-are-spent-deliberately)
- [Personal-context boundary](../contracts/project-adoption.md#learning-and-personal-context-have-a-bounded-entry-path)
