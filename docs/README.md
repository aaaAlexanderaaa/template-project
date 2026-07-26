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

With Python 3.11 or newer, run `python3 scripts/check_docs.py` after changing
canonical documentation. Run the standard-library unit suite when changing the
checker or templates:

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
```
