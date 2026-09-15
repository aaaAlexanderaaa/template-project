---
doc_type: authority-map
status: current
authority: normative
last_reconciled: 2026-09-15
---

# Documentation authority map

Document authority comes from metadata and document role, not modification
time, filename, or length.

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

## Task context

Start with enough current context to determine five things: the requested
outcome; facts and their evidence; who may decide; applicable boundaries and
exceptions; and evidence sufficient for completion. Obtain these from the
request, relevant architecture and contract sections, observed baseline, and
an active plan only when required. This is a reading rule, not a new document
or a form to fill for every task. Do not copy a second set of product facts
into the agent entrypoint.

Read detailed methods when a task activates them. A link does not require
recursive reading. Expand context for a dependency, conflict, missing fact, or
activated concern, and read the whole owner when section-level reading leaves
its scope or interactions unclear. Short context never waives an applicable
constraint, exception, or original requirement.

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

## Language style

Canonical documents are written in plain language. Name things with the
repository's existing vocabulary or with a plain description of the thing
itself. Do not coin compressed terms, slogans, or metaphors to make a document
sound systematic: a coined term reads as authority, spreads into later
documents and conversations, and must then be unlearned everywhere. When a
concept genuinely needs a name, define it once in the owning document's
vocabulary section and use that name consistently.

Wording is not decoration. The phrasing of a descriptive document guides the
language of the work that follows it, so plain writing keeps later writing
plain.

Use English for repository rules, templates, and working records, following
the maintainer's language preference. Preserve original stakeholder wording when
interpretation matters and label translations. Review instructions and user
messages from the reader's position: name the actor, condition, action, result,
and available next step when relevant. Explain an internal term before relying
on it. Replace a vague promise such as "state reconciled" with what changed or
remains unresolved. Word lists and an "AI writing" detector cannot establish
that a reader understands the result; inspect a concrete task or message.

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
prefer routing and a compact executable path. `README_CN.md` is the Chinese
homepage companion to `README.md`; it is not a second authority. They are
intentionally not made canonical merely to obtain a checker field; their
duplication risk is handled by keeping normative trigger semantics out of them
and reviewing their links when an owning contract changes.

## Conflict rule

Do not silently merge conflicting documents. Mark the affected document
`needs_reconciliation`, record the disagreement and sources, determine which
direction is current, and preserve an explicit supersession chain.

## Evidence tiers

- Working evidence belongs in `tmp/` and may disappear.
- Durable evidence supporting a current contract belongs in `docs/evidence/`.
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
