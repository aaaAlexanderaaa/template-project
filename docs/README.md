---
doc_type: authority-map
status: current
authority: normative
last_reconciled: 2026-10-30
---

# Documentation authority map

Document authority comes from metadata and document role, not modification
time, filename, or length.

<!-- required-reading: authority-order -->
## Authority order

1. `ARCHITECTURE.md` owns structural boundaries, dependency direction, and
   system-wide ownership.
2. `docs/contracts/` owns current cross-surface behavior and invariants.
3. `docs/design/` owns current frontend surface behavior.
4. `docs/plans/` owns execution order only. A plan cannot override a current
   contract.
5. `docs/issues/` owns the lifecycle of reported findings, not intended
   behavior.
6. `docs/guides/` explains procedures and operations.
7. `docs/evidence/` supports claims but cannot override a contract.
8. `templates/` has no authority until copied, completed, and landed in the
   appropriate authoritative directory.

<!-- /required-reading: authority-order -->

<!-- required-reading: task-context -->
## Task context

- required-reading: [Authority order](#authority-order)
- required-reading: [Language style](#language-style)
- required-reading: [Development core](contracts/development-discipline.md#core-invariants)
- required-reading: [Governance core](contracts/governance-decision-boundary.md#normative-invariants)
- required-reading: [Execution risk](contracts/agent-execution-discipline.md#risk-selects-the-execution-depth)
- required-reading: [Execution route](contracts/agent-execution-discipline.md#the-harness-selects-the-smallest-executable-route)
- required-reading: [Completion](contracts/agent-execution-discipline.md#completion-is-layered)

Start with enough current context to determine five things: the requested
outcome; facts and their evidence; who may decide; applicable boundaries and
exceptions; and evidence sufficient for completion. Obtain these from the
request, relevant architecture and contract sections, observed baseline, and
an active plan only when required. This is a reading rule, not a new document
or a form to fill for every task. Do not copy a second set of product facts
into the agent entrypoint. A learning judgment names the rule, the result,
and the contract section that holds the fact.

The required core includes [essential reasoning for AI work](contracts/development-discipline.md#keep-essential-reasoning-active):
awareness of incomplete framing, instruction effects, conditional behavior,
unresolved gaps and loss across transfers. It must be available before the
agent recognizes a specialist trigger. Preserve its meaning through context
reduction and continuation; a pointer to unread text does not establish receipt.
Detailed cases and methods remain on demand. A passing checklist cannot close
an uncertainty it was not able to observe.

Use the following reading classes. They select context; the authority order
still decides who owns a decision.

| Class | What is obtained | When |
|---|---|---|
| Global required core | This task context, authority and language; development's complete core, governance's operative core, execution risk/route/completion | Before selecting or closing work; reuse retained, unchanged units |
| Activated mandatory detail | The complete applicable domain and project-owner units, including their dependencies and exceptions | Before decisions that depend on the concern; global core supplies no exemption |
| Execution method | The full method selected by the task, such as material delivery, research, Grill, adoption or standing autonomy | When used; the method's review and evidence duties remain binding |
| Provenance and history | Source anchors, prior decisions and dated evidence | A dispute, recovery or claim needs their contents |

Strength is independent of reading class. A mandatory condition binds within
its trigger and authority. A default selects a usual route while leaving
alternatives inside the same boundaries. A method explains how to act;
reference material supplies evidence. Resolve a conflict through the owning
authority and its exception policy. The adoption value order prioritizes
attention; it grants no exemption from an applicable requirement.

For the practical sequence and worked task decisions, use
[project operation](guides/project-operation.md#execute-one-task-from-request-to-result).
It explains how these owners work together without becoming another authority.
For a concrete obstacle, the [practical task CheatSheet](guides/task-cheatsheet.md)
offers optional moves and prompts across common scenarios. Select a fitting
method within this context; the recipes add no required reading dependency.

Rule authority, applicability, reading scope, requirement strength and completion
evidence answer different questions. Authority decides who can change a rule;
a concern trigger decides when it applies; a declared unit decides what text
must be obtained; mandatory/default/reference wording decides its force;
observations decide whether the requested result was achieved. A broad global
rule does not replace an activated domain's detailed requirements.

Before making choices that depend on an activated concern, run
`python3 scripts/read_rules.py prepare` with its concern and owner bindings.
The command emits the complete selected units and explicit dependencies with
source identities. Add `--include REFERENCE` for a selected current execution
method and its dependencies. Obtain every new body and the final completion
marker. If output
is truncated, use digest-checked `read` recovery from the
[harness protocol](contracts/documentation-harness.md#complete-rule-delivery-is-a-read-only-transaction).
On failure or where the command is unavailable, directly read the same complete
units and retain their source identities. A manifest alone proves no reading;
source delivery alone proves no application.

A unit may be reused while its body, metadata, scope and retained context remain
valid. In one live context, `--context ID --retained MANIFEST` revalidates the
whole current selection and marks unchanged bodies as caller-asserted retained;
it supplies new or changed bodies. Supply only a version-2 manifest whose full
reused bodies are still available. The label cannot establish memory or understanding.
On restart, handoff or unknown retention, recover purpose and locators, then
obtain current units again without `--retained`. Ordinary file lookup uses the
already obtained core and direct facts;
it adds no domain plan or independent review. Current and explicitly selected
target rules remain distinguishable. Methods are read when used. An ordinary
link does not require recursive reading; only explicit `required-reading`
directives create reading dependencies. A request to learn the discipline is the exception: obtain
every current rule named by
[the learning path](contracts/project-adoption.md#learning-and-personal-context-have-a-bounded-entry-path)
and understand its reason before judging which apply. The adoption owner's
[reading order](contracts/project-adoption.md#understand-rules-before-judging-applicability)
keeps source acquisition separate from applicability and adoption, including
for projects with an existing discipline. Later tasks return to opening a rule
when the work reaches it. Expand context for a dependency, conflict, missing
fact or activated concern, and read the whole owner when section-level reading leaves
its scope or interactions unclear. Short context never waives an applicable
constraint, exception, or original requirement.

Examining one practice within a narrow request or an authorized concrete task uses
[bounded extraction](contracts/project-adoption.md#take-one-practice-into-an-authorized-task)
instead of claiming a full learning survey. The
[operation card](guides/project-operation.md#take-one-practice-into-a-task)
keeps that choice explicit; governed work still obtains the required core and
activated detail.

For an ongoing project, purpose guides choices, goals name desired changes,
methods organize work, and tasks execute bounded steps. Task completion may
leave its goal open; a finished goal need not exhaust the project's purpose.
The owner's named end still bounds the current assignment.

Choose context by the decision being made. Routine execution uses the current
task and its parent outcome; selecting work needs goals and alternatives;
changing an approach needs its assumptions and evidence; questioning direction
needs the original purpose and accepted trade-offs. Purpose and boundaries
remain binding at every level without reopening them at every step. Retain a
settled choice while its authority and decisive assumptions remain valid;
new evidence reopens the affected choice, not the whole project by default.
Later feedback refines the ongoing outcome unless the owner replaces it.
Check the combined requirements before closure, not only the latest correction.

Development's [active comparison rule](contracts/development-discipline.md#analysis-exposes-the-decisive-causal-mechanism)
owns when consequential inquiry needs deliberate differences in evidence,
questions, standpoint or model, and how their results retain usable limits.

When corrections recur or successful execution produces disappointing value,
use [judgment diagnosis](contracts/development-discipline.md#improve-judgment-before-amplifying-effort)
to locate the affected choice, observation or response before prescribing more
activity. Settled ordinary work does not reopen its whole direction.

At a recurring decision, follow the permitted locator for
[reusable experience](contracts/development-discipline.md#experience-changes-the-next-matching-action)
before rediscovering a method. Carry applicable experience and return conditions
with a handoff, rather than making every task reread all historical lessons.

When separately supplied personal context is relevant, read its onboarding
entrypoint for collaboration background, decision preferences, and deeper
reading conditions. Apply [the adoption boundary](contracts/project-adoption.md#learning-and-personal-context-have-a-bounded-entry-path)
before transferring any material. The [alignment route](contracts/governance-decision-boundary.md#missing-knowledge-is-routed-not-automatically-escalated)
decides which unknowns require conversation; the [delegation owner](contracts/agent-execution-discipline.md#delegated-work-carries-bounded-context-and-returns-to-an-owner)
decides what a recipient needs. A private profile does not join every worker's
startup context or replace the target project's current authority.

Source anchors and reconciliation history explain provenance; read them when
intent is disputed, a prior decision needs investigation, or recovery needs
that evidence. They are not mandatory startup context merely because they
share a file with current rules.
Place operative rules before source chronology when reorganizing an owner;
preserve source anchors and live references. Source-placement validation is
owned by [the harness](contracts/documentation-harness.md#contract-source-anchors-are-conditionally-bidirectional).
Plans and handoffs link to precise current sections and state the next action,
verified baseline, material unresolved assumptions, and completion evidence.
They do not require a prior handoff chain or a plan when the route needs none.
A plan, handoff, or task description is written for a reader who has none of
the current context — goal, expected end state, current state, and gap — and
a fresh reader's misreading is a defect in the document, not in the reader.
Memory or a generated summary is a locator, not a replacement for current authority.

At closure, merge still-live decisions into their owner, mark the plan
completed, and replace startup links to old working records with links to the
current decision. Preserve history that supports a live claim or recovery;
delete scratch material that no longer serves either. Do not create a fresh
summary that requires reading every older summary to understand it.

<!-- /required-reading: task-context -->

## Required metadata

Canonical Markdown documents under `docs/` carry frontmatter:

- `doc_type`: `authority-map`, `contract`, `surface-contract`, `plan`,
  `issue-tracker`, `guide`, or `evidence`;
- `status`: lifecycle state;
- `authority`: `normative`, `planning`, `guidance`, or `evidence`;
- `last_reconciled`: last date the document was checked against its sources;
- contracts also use `implementation` and `verification_status`;
- target contracts and surfaces may set `review_due` to override the configured
  aging deadline;
- replacements use `supersedes` and `superseded_by`.
- `reading_entrypoint` may publish a complete declared unit for file-only
  reading; the [harness protocol](contracts/documentation-harness.md#complete-rule-delivery-is-a-read-only-transaction)
  owns its resolution and retained-context behavior.
- a `status: current` canonical guide that intentionally summarizes current
  normative contracts or surface contracts may use `projection_of`; this
  declares a reconciliation dependency, not shared ownership.

Lifecycle relationship fields use repository-root-relative paths. Markdown
links may be document-relative. Neither form may be absolute or escape the
repository, even when the external target happens to exist locally.

## Lifecycle

- `current`: authoritative for present behavior.
- `target`: accepted future behavior, not yet the standard for current code.
- `active`: implementation or triage is in progress.
- `completed`: a finished plan retained for history.
- `historical`: context or evidence only.
- `superseded`: replaced; requires `superseded_by`.
- `needs_reconciliation`: conflict or ambiguity blocks dependent work.

The active read set consists of applicable `current`, `target`, `active`, and
`needs_reconciliation` documents. `completed`, `historical`, and `superseded`
documents remain searchable history but do not join normal change authority or
work selection merely because they remain on disk.

Implementation states: `not_started`, `in_progress`, `partial`, `implemented`,
`retired`.

Verification states: `pending`, `partial`, `enforced`, `not_applicable`.

Repository-wide aging, template inventory, adoption roots, and optional
abnormality deadlines live in `docs-policy.toml`. Concrete future commitments
use structured `promise[id]` records with explicit due dates rather than
natural-language TODO detection.

## Document stock and coupling

Documentation is governed by decisions and ownership, not by file or line
counts. A large system may need many contracts; a small system may need few.
Neither volume is evidence of quality by itself, and the harness must not ship
universal documentation budgets.

Before creating a canonical document:

1. identify the decision, behavior, procedure, finding, or evidence it owns;
2. update an existing owner when the reason for change is the same;
3. split only when authority, lifecycle, audience, or reason for change is
   genuinely distinct;
4. name the lifecycle exit: merge, supersede, mark historical, or delete
   disposable evidence.

Long-term maintenance includes subtraction:

- merge still-live decisions into their surviving normative owner;
- retain a concise historical synthesis when chronology, rejected alternatives,
  audit, or recovery value would otherwise be lost;
- mark completed plans and historical evidence out of the active read set;
- supersede replaced authority bidirectionally;
- remove scratch evidence once it supports no live claim.

Both ends of a supersession are canonical documents. The replaced document is
`status: superseded` and names `superseded_by`; the replacement names the same
document through `supersedes`. Both ends have the same `doc_type` and
`authority`, so supersession changes a decision within one authority class
rather than promoting a plan, guide, or evidence record into a normative owner.

<!-- required-reading: language-style -->
## Language style

Content serves its consumer. For a response, report, guide, prompt or other
authored output, use the current task to establish the intended reader, their
situation and prior knowledge, and what they want and need to understand,
decide, do or experience. Before drafting and against the actual draft, ask:

- Who will use this, and what do they already know?
- Why should they spend attention here? What benefit does this add to what
  they already have, and what would they miss by skipping it?
- Which conclusion, distinction or next action should become clear?
- Which details earn their place? What useful meaning would their removal lose?
- Where must the reader decode internal language, reconstruct our work or
  reconcile repetition? Can selection, order, an example or a precise link
  remove that burden?

Let the answers change the content, not become a preface or another form.
Lead with what matters to that reader. Remove or relocate process narration
that does not help them; keep required evidence available for its audit or
reproduction consumer through a precise route. A short answer can remain short.
Judge information density by useful meaning for the reader's effort, not by
word count: a necessary example or qualification can improve it. Preserve the
reasoning, distinctions and material uncertainty needed to use the result.

Canonical documents are written in plain language. Name things with the
repository's existing vocabulary or with a plain description of the thing
itself. Do not coin compressed terms, slogans, or metaphors to make a document
sound systematic: a coined term reads as authority, spreads into later
documents and conversations, and must then be unlearned everywhere. When a
concept genuinely needs a name, define it once in the owning document's
vocabulary section and use that name consistently.

Use plain English throughout published rules, templates, working records, and
history. Render stakeholder feedback in English with enough context to explain
the issue and the accepted decision. Distinguish a translated quotation from
a paraphrase; preserve its meaning and scope without requiring the reader to
understand a private conversation. Review instructions and user messages from
the reader's position: name the actor, condition, action, and result.
Name the next step when the owner must act before work can continue. When
the owner has already said to continue, the next step is the work itself.
Explain an internal term before relying
on it. Replace a vague promise such as "state reconciled" with what changed or
remains unresolved. Word lists and an "AI writing" detector cannot establish
that a reader understands the result; inspect a concrete task or message.

Give the reader a supported positive judgment: what the result enables, why
the selected action is sound, and which observation makes this bounded work
sufficient. Keep material uncertainty beside the claim it changes. Close when
the requested result and applicable evidence support completion.

State conclusions and own them: precise uncertainty is required, but
dissolving a verdict into hedging, borrowed authority, or defensive citation
is a clarity defect, not caution. Examples and defaults are teaching
material — write the usage you want copied, because readers copy them.
Reason in the order the problem needs; write in the order the reader needs —
compression that costs the reader more than it saves is not brevity.

When citing a normative invariant from another document, link to its owning
contract and heading slug rather than quoting a letter code; within a
contract, cite its own invariants by short name. Letter-prefixed codes remain
valid in contracts that have not migrated.
`docs/contracts/documentation-harness.md` owns the identifier convention and
its mechanical validation.

One normative rule has one owner. Other documents may:

- **route:** point a reader to the owner without restating the rule;
- **project:** summarize only what a specific operator or contributor needs;
- **explain:** provide non-normative examples and procedure;
- **evidence:** record what was observed and what remains unproved.

A projection does not introduce new conditions. `projection_of` is deliberately
narrow: only a canonical `doc_type: guide`, `authority: guidance`, and
`status: current` document may declare it, and every repository-root-relative
target must be a canonical `status: current`, `authority: normative` contract or
surface contract. It is not a general dependency field for plans, evidence,
root entrypoints, templates, architecture, or historical documents.

The lifecycle matrix has one valid operating state: current guide to current
normative source. If a source becomes `target`, `needs_reconciliation`,
`superseded`, or otherwise leaves current authority, the guide relationship is
invalid until the guide is reconciled against a current replacement or removes
both the projection and its restatement. Marking the guide
`needs_reconciliation` truthfully removes it from current guidance while that
recovery occurs; it does not make a stale projection authoritative.

When a projected source has a later `last_reconciled` date than its guide, the
harness reports the guide for review. The finding is advisory because a source
change may not affect the projected section. The reviewer updates the guide's
date when still aligned, changes the projection when affected, or removes the
relationship when it no longer restates that authority. Date granularity cannot
detect same-day source changes made after a guide was checked; same-day coupling
remains a review limitation rather than a mechanically proven freshness claim.

Root entrypoints such as `README.md`, `AGENTS.md`, and `CONTRIBUTING.md` should
prefer routing and a compact executable path. `README_CN.md` retains a short
English link to the main overview for existing inbound links. Root entrypoints
are intentionally not made canonical merely to obtain a checker field; their
duplication risk is handled by keeping normative trigger semantics out of them
and reviewing their links when an owning contract changes.

<!-- /required-reading: language-style -->

## Conflict rule

Do not silently merge conflicting documents. Mark the affected document
`needs_reconciliation`, record the disagreement and sources, determine which
direction is current, and preserve an explicit supersession chain.

## Evidence tiers

- Working evidence belongs in `tmp/` and may disappear.
- Durable evidence supporting a current contract belongs in `docs/evidence/`.
  Reproduction instructions identify supplied materials or obtainable public
  sources and required conditions. Unpublished maintainer experience can
  explain a decision, but its summary does not make the original evidence
  available to readers or verify an adopting project.
- Large binaries should remain outside Git unless the project explicitly
  chooses a binary-artifact store. Commit structured summaries and stable
  references instead.

## Agent execution profile

This template repository applies
`docs/contracts/agent-execution-discipline.md` to its own material agent work.
An adopting project selects its agent-governance depth during onboarding and
reconciles its local instructions explicitly; copying the files does not grant
an agent product-direction or priority authority. Review records and holistic
evaluations remain evidence, plans remain planning, and product behavior still
belongs in contracts.

Routine work uses existing owners, including an update for authorized local
behavior when required by [development](contracts/development-discipline.md#contract-before-material-delivery-evidence-before-certainty),
and no standalone plan. Use
`templates/agent-execution-plan.md` for material execution and retain its review
block only for high-risk work. `templates/independent-review.md` records
genuinely independent perspectives; `templates/holistic-evaluation.md` records
completion review when a separate record is warranted. If required independence
is unavailable, record a blocked state or an explicit human governance
exception; never relabel same-context analysis as independent.

Work the owner has authorized to continue across unattended wakes — scheduled
or around-the-clock — is governed by
`docs/contracts/autonomous-operation-discipline.md`: its charter is the
standing authorization form, and its epoch, role-identity, calibration, and
deferral rules apply instead of per-task interaction.

## Governance and onboarding

`docs/contracts/governance-decision-boundary.md` owns the boundary between
human product authority and governance assistance. Developers or product owners
retain direction, priority, trade-offs, and risk acceptance. Governance output
is explicitly a fact, risk, recommendation, required human decision, or a
narrow evidence-backed execution blocker.

`docs/contracts/project-adoption.md` owns greenfield and brownfield adoption.
Use `docs/guides/onboarding.md` and `templates/adoption-assessment.md` to
inventory current truth, preserve existing authority, declare managed scope and
priority ownership, and move through evidence-backed adoption stages. After
onboarding, `docs/guides/project-operation.md` describes how agents consume
rather than invent project priority.

With Python 3.11 or newer, run `python3 scripts/check_docs.py` after changing
canonical documentation. Run the standard-library unit suite when changing the
checker or templates:

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
```
