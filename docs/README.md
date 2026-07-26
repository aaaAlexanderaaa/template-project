---
doc_type: authority-map
status: current
authority: normative
last_reconciled: 2026-07-26
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

Implementation states: `not_started`, `in_progress`, `partial`, `implemented`,
`retired`.

Verification states: `pending`, `partial`, `enforced`, `not_applicable`.

Repository-wide aging, template inventory, adoption roots, and optional
abnormality deadlines live in `docs-policy.toml`. Concrete future commitments
use structured `promise[id]` records with explicit due dates rather than
natural-language TODO detection.

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

Use `templates/agent-execution-plan.md` for material execution,
`templates/independent-review.md` for genuinely independent perspectives,
and `templates/holistic-evaluation.md` for completion review. If independence
is required but unavailable, record a blocked state or an explicit human
governance exception; never relabel same-context analysis as independent.

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
