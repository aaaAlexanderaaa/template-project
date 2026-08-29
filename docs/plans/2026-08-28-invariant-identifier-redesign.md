---
doc_type: plan
status: completed
authority: planning
last_reconciled: 2026-08-28
implements: [docs/contracts/documentation-harness.md, docs/contracts/engineering-judgment-discipline.md]
supersedes: []
---

# Invariant identifier redesign plan

## Cold-start summary

The owner asked how many symbol systems the repository has and found the
accumulating letter codes (D, G, A, O, H, INV, J) off-putting. Investigation
showed the deeper defect is not aesthetics but verification: invariant
references are the repository's only unvalidated reference layer. Document
links fail the checker when they break; a mistyped or orphaned "D8" never
does. The approved direction: make the invariant heading the identifier,
cite it with a Markdown link whose fragment is the heading's slug, validate
fragments mechanically (advisory first), and migrate contract by contract,
newest first. The day-old target engineering-judgment contract is the pilot.

## Authority and prerequisites

- Mechanical enforcement owner: `docs/contracts/documentation-harness.md`
  (H2 anchors, H7 reference containment, H9 severities)
- Language and citation style owner: `docs/README.md`
- Pilot subject: `docs/contracts/engineering-judgment-discipline.md`
  (`status: target`, 14 references, one day old)
- Baseline evidence: the citation inventory of 2026-08-28 (seven invariant
  namespaces, four anchor systems, ~450 letter-code references) and zero
  existing fragment links in the repository
- Decisions already confirmed: redesign direction, advisory-first staging,
  J-series pilot

## Complete end state

- documentation-harness H13 owns the identifier convention and its
  transition semantics; letter codes remain valid in unmigrated contracts.
- The checker resolves Markdown link fragments against the target document's
  headings; failures are `fragment_resolution` findings, advisory by
  default and retunable per H9, with `docs-policy.toml` registering the key.
- The engineering-judgment contract's headings carry no letter codes; its
  internal and incoming references use short names or slug links.
- `docs/README.md` routes citation style to H13.
- Fixture tests cover resolving, broken, strict-promoted, and
  off-under-strict fragment cases; the full suite and both checker modes
  pass.

## Current state and gap

`validate_local_links` strips fragments (`target.split("#", 1)[0]`) and
checks only file existence. Letter codes are unvalidated prose conventions.
The engineering-judgment contract uses J1–J6 headings with internal and
incoming code references.

## Execution order within one coherent change

1. Land this plan.
2. H13 + source anchor + reconciliation log in the harness contract;
   routing sentence in `docs/README.md`.
3. Checker: slug inventory, fragment validation, `CONFIGURABLE_RULES`
   registration; policy key registered in `docs-policy.toml`.
4. Pilot: rewrite the engineering-judgment contract's headings and
   references; update the reading guide's incoming reference.
5. Fixture tests; run the full suite and both checker modes.

## Risk register

| Risk | Mitigation |
|---|---|
| Mixed identifier forms read as inconsistency | H13 defines the transition: letters valid until a contract's wholesale cutover; mixed form within one contract is a defect |
| Fragment validation breaks adopters with legacy links | Default advisory; `off` survives `--strict` per H9 |
| Slug rule diverges from renderers | Use the renderer convention (lowercase, punctuation removed, spaces to hyphens); fixture pins the em-dash double-hyphen case implicitly via real headings |
| Heading renames become expensive | Intended: renames reconcile loudly in the same change, replacing silent rot |

## Verification matrix

| Claim | Evidence |
|---|---|
| Fragment links resolve or are found | New fixture cases |
| Real repository has no unresolved fragments | `check_docs.py` and `--strict` both clean |
| Advisory semantics honest | off-under-strict fixture; strict promotion via `assert_advises` |
| Pilot contract fully migrated | No `J\d` references remain; incoming links resolve |

## Completion record

Completed 2026-08-28.

- `docs/contracts/documentation-harness.md`: source[6], H13 (identifier
  convention, advisory-then-error staging, wholesale per-contract cutover),
  required-behavior bullet, acceptance-evidence row, reconciliation entry.
- `scripts/check_docs.py`: `heading_slug`/`heading_slug_inventory` helpers;
  `validate_local_links` now resolves link fragments against the target
  document's headings; `fragment_resolution` registered as advisory in
  `CONFIGURABLE_RULES` and in `docs-policy.toml`.
- `docs/README.md`: citation style routes to H13.
- Pilot cutover: `docs/contracts/engineering-judgment-discipline.md`
  headings carry no codes (source[3], reconciliation entry); the reading
  guide's incoming reference is a slug link.
- Three fixture tests: resolving fragment, broken fragment advisory with
  strict promotion, and off-survives-strict.

Verification:

- `uv run --python 3.11 python -m unittest discover -s tests -p 'test_*.py'`
  → PASS, 110 tests.
- `python3 scripts/check_docs.py` → PASS (25 documents, 15 templates).
- `python3 scripts/check_docs.py --strict` → PASS, zero fragment findings
  with the pilot's slug link in place.

Remaining transition debt: D, G, A, O, H, and INV namespaces keep their
letter codes until each contract's wholesale cutover; `fragment_resolution`
stays advisory until then. No date is promised for those cutovers — each is
recorded in its contract's reconciliation log when it happens.

**2026-08-28 addendum:** the owner directed the remaining cutovers the same
day. All six namespaces (D, G, A, O, H, INV) migrated wholesale, references
in living documents were rewritten to slug links, completed plans and dated
evidence were left as history, and `fragment_resolution` is now pinned to
`error` in this repository. Each contract's reconciliation log carries its
own cutover entry.
