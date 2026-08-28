---
doc_type: plan
status: completed
authority: planning
last_reconciled: 2026-08-28
implements: [docs/contracts/governance-decision-boundary.md, docs/contracts/development-discipline.md, docs/contracts/engineering-judgment-discipline.md]
supersedes: []
---

# Engineering judgment discipline adoption plan

## Cold-start summary

The owner reviewed the template's discipline coverage and found it strong on
process truthfulness (authority, evidence, verification, lifecycle) but thin
on engineering judgment itself: how to define and evaluate user experience,
how to manage complexity and when to refactor, how to avoid reinventing the
wheel, how to compare solutions, and how to report problems with impact,
ROI, the conditions under which they do not matter, and the assumptions that
accepting a risk would make. The owner directed mining of settled industry
material — the Google SRE books, *A Philosophy of Software Design*,
TigerBeetle's TIGER_STYLE, hacker-laws, the Grug Brained Developer essay, a
97-things architecture summary, and an agent-rules gist — with the raw
sources archived locally first so future mining can re-read originals rather
than trust summaries.

The raw archive lives in `archive/external/` (gitignored, checker-skipped)
with an authorship-triaged manifest. Seven parallel mining passes produced
candidate disciplines, each with provenance, material strength, a suggested
owner, and an over-design boundary. The owner confirmed the landing shape:
small strengthenings to current contracts, one new target contract, and a
reading-list guide.

## Authority and prerequisites

- Behavioral contracts: `docs/contracts/development-discipline.md` (D6, D8),
  `docs/contracts/governance-decision-boundary.md` (G3, G7)
- New contract target: `docs/contracts/engineering-judgment-discipline.md`
- Documentation authority: `docs/README.md`
- Baseline evidence: the owner conversation of 2026-08-28; the seven mining
  reports; the local raw archive under `archive/external/`
- Decisions already confirmed: the three-part landing shape (strengthen
  existing, draft new target contract, land reading list)

## Complete end state

- G3 and the risk state require problem reports to name who bears the
  impact, its rough magnitude, the conditions under which it does not
  matter, and what accepting the risk would assume; G7 option sets state
  when the difference between options does not matter.
- The D8 routing table's minimum questions cover the scenarios industry
  practice has already settled: schema evolution (state integrity), named
  resource bounds and chosen exhaustion behavior (performance/capacity),
  error budget, actionable-alert test, and postmortem trigger
  (reliability/operations), existing-solution search and cost categories
  (dependency), displaced complexity and task signals (experience). D6 names
  postmortem output and monitoring failure as category sources.
- A new `status: target` contract owns the judgment method: complexity
  vocabulary, checkable refactor triggers, the in-envelope comparison
  procedure, build-vs-reuse accounting, standpoint declaration, and the
  rule format that carries its own over-design boundary.
- A reading-list guide records the sources, their authorship classes, what
  to mine from each, and what was deliberately rejected.
- The fixture suite and both checker modes pass.

## Current state and gap

Current contracts cover collaboration, agent execution, documentation, and
adoption. The D8 table routes concerns but several rows predate the settled
industry answers for their scenario. G3 requires benefit/cost on
recommendations but not immateriality conditions or risk-acceptance
assumptions on problem reports. No contract owns complexity triggers,
in-envelope decision method, reuse accounting, or standpoint declaration.

## Execution order within one coherent change

1. Land this plan.
2. Strengthen `governance-decision-boundary.md` (G3, risk state, G7,
   required behaviors, source anchor, reconciliation log).
3. Strengthen `development-discipline.md` (five D8 rows, D6, source anchor,
   reconciliation log).
4. Draft `engineering-judgment-discipline.md` as `status: target`.
5. Land `docs/guides/engineering-reading.md`; register it and the new
   contract in the directory READMEs.
6. Move the fixture clock to 2026-08-28; run the full fixture suite and
   both checker modes.

## Risk register

| Risk | Mitigation |
|---|---|
| New text becomes ceremony (a questionnaire per change) | Every invariant carries its own over-design boundary; D8's activation model means untriggered concerns create no obligation |
| Vocabulary import from mined sources (O8) | Plain language only; metaphors and coined terms stay in the archive |
| Target contract read as current authority | `status: target`, `implementation: not_started`; projections (AGENTS.md and entrypoints) are deliberately not updated until adoption |
| UX evaluation material remains thin | Recorded as an open gap in the reading guide; HEART/Nielsen-class sources named as candidates for a later mining pass |

## Verification matrix

| Claim | Evidence |
|---|---|
| Checker and fixtures pass | `python3 -m unittest discover -s tests -p 'test_*.py'`; `python3 scripts/check_docs.py` and `--strict` |
| D8 Time/Demo routing untouched | `test_d8_routes_foundational_runtime_concerns` stays green |
| Source anchors resolve bidirectionally | Checker source-citation rules on edited contracts |
| No broken links or metadata drift | Repository check output |

## Completion record

Landed 2026-08-28:

- `governance-decision-boundary.md`: G3 problem reports now carry who bears
  the impact, rough magnitude, immateriality conditions, and the
  risk-acceptance assumption; the risk state row and required behaviors
  match; G7 option sets state when the difference between options does not
  matter. Source anchor source[7] added.
- `development-discipline.md`: five D8 rows extended (state integrity,
  performance/capacity, reliability/operations, dependency, experience); D6
  names postmortem output and monitoring failure as category sources;
  source anchor source[7] added.
- `engineering-judgment-discipline.md` created as `status: target`,
  `implementation: not_started`, `verification_status: pending`, J1-J6.
- `docs/guides/engineering-reading.md` created with the source table,
  authorship classes, mining method, rejected list, and the UX-evaluation
  gap; registered in the contracts, guides, and plans READMEs.
- Projections reconciled: `project-operation.md` restates the extended G7
  option fields; `onboarding.md` needed only its date. Fixture clock moved
  to 2026-08-28 with the two date-coupled test expectations.
- Verification: full Python 3.11 fixture suite (107 tests) passes;
  `python3 scripts/check_docs.py` and `--strict` both pass with no
  findings; `git status` shows only the intended files (`archive/` stays
  gitignored).

Remaining layer: the target contract's acceptance evidence requires a real
material change to exercise J3 and a real problem report to use the new G3
fields; entrypoint projections (AGENTS.md) deliberately unchanged until the
contract approaches current status.
