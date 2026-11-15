---
doc_type: plan
status: completed
authority: planning
last_reconciled: 2026-09-17
implements: [docs/contracts/foundational-runtime-discipline.md, docs/contracts/development-discipline.md]
supersedes: []
---

# Foundational runtime discipline landing plan

## Cold-start summary

The template already holds collaboration, ownership, and agent-execution
discipline. It did not own the implementation facts that are cheap to declare
and expensive to retrofit: a unique business clock/calendar, demonstration
data that stays valid across civil days, and the sibling health classes
paid for in a long-running product. The template owner authorized exporting
that method into this repository as a domain-neutral contract plus an
`ARCHITECTURE.md` register, without copying the source product's zone,
ports, or fixtures.

## Risk classification

- Profile: `material`
- Rationale: the change alters reusable delivery contracts and adopter
  prompts consumed by later projects, but changes no product architecture,
  authorization, durable state, or user interaction in this repository.
- Required independent review: no; A1 reserves independent design and
  fresh-context completion review for high-risk work.

## Authority and prerequisites

- Structural authority: `ARCHITECTURE.md` remains an unconfigured product
  template; runtime prompts name zone/clock and demo when they exist.
- Behavioral contracts: `docs/contracts/foundational-runtime-discipline.md`
  owns the method; `docs/contracts/development-discipline.md` D8 owns
  concern routing to it.
- Priority source or human authorization: template owner, 2026-08-24,
  selected a new contract plus D8 routing, then required the landing to
  match this template's own consumption model rather than a pit catalog.
- Baseline evidence: timezone mentioned only as an optional frontend
  checklist bullet; demonstration-data lifecycle absent; README transfer
  order already distinguishes method from carriers.

## Engineering decision envelope

- Authorized outcome and managed scope: this template repository's
  contracts, architecture prompts, entrypoints, and adopter templates.
- Applicable boundaries: migrate the method, not the source product's
  IANA zone, demo port, or fixture identities; one owner per invariant.
- Reversible choices: section numbering, prompt wording, and how tightly
  the worked examples are specified.
- Human decisions still required: none for this landing; the owner
  selected the form.

## Activated concerns and owners

No product-facing runtime is present in this repository. Document
compatibility for the D8 routing table is owned by
`docs/contracts/development-discipline.md`. The new method owner is
`docs/contracts/foundational-runtime-discipline.md`. Plans do not copy
the D8 trigger table.

| Activated concern | Normative owner and section | Implementation steps | Evidence |
|---|---|---|---|
| Compatibility of D8 routing | `development-discipline.md` D8 | Add Time and calendar and Demonstration data rows; keep Experience from swallowing timezone | wiring test; checker |
| Time and calendar / Demonstration data method | `foundational-runtime-discipline.md` | Land invariants, register, and what-not-to-copy | contract; ARCHITECTURE §4 |

## Complete end state

Adopters see:

1. A recognition rule: a fact is worth naming early when an omitted
   default will be assumed in more than one place and changing it later is
   a cutover. This is how to look at source-project repairs; it is not a
   pit catalog.
2. D8 activates Time and calendar and Demonstration data and routes them
   to one owner. Untriggered concerns create no questionnaire.
3. Time and demonstration invariants are fully specified and domain-neutral.
4. `ARCHITECTURE.md` runtime prompts name zone/clock and demo refresh when
   those exist; there is no sibling-incident register.
5. Frontend, backend, cross-stack, onboarding, and compact entrypoints
   project those rules and do not copy the D8 table.

## Seven-phase execution loop

| Phase | Required output | Applicability or evidence |
|---|---|---|
| 1. Domain and authority | Method vs product numbers; D8 as router | maintainer-reported time-policy and demo-date repairs summarized in the foundational runtime source entries; template transfer-value order |
| 2. Fixture or controlled boundary | Checker today remains clock-controlled; new wiring test | `FIXED_TODAY` moved with last_reconciled; D8 routing test |
| 3. Contract and design | Landed foundational-runtime contract and D8 rows | this plan's implements list |
| 4. Test first | Wiring test fails before the contract and D8 rows exist | `test_d8_routes_foundational_runtime_concerns` |
| 5. Implementation | Smallest coherent projection set | ARCHITECTURE, templates, README, AGENTS, onboarding |
| 6. Regression | Fixture suite and repository check | `python3 -m unittest discover -s tests -p 'test_*.py'`; `python3 scripts/check_docs.py` |
| 7. Holistic evaluation | Method present; product numbers absent; completion layer named | task-layer landing; adopter effectiveness remains partial |

## Work-selection fallback

Named task is executable. No fallback selected.

Selected action and authority: land the authorized contract and projections
in this repository only; do not edit the source product.

## Verification and evidence matrix

| Claim | Evidence class | Command/probe | Expected failure/negative path | Durable record |
|---|---|---|---|---|
| D8 names Time and calendar and Demonstration data | unit | wiring test against repository files | missing concern rows fail | `tests/test_check_docs.py` |
| New contract is governance, not a fake product contract | unit | `contract_role: governance` assertion | product-minimum still unmet by this file | same test |
| ARCHITECTURE has runtime prompts, not a pit register | unit | timezone/demo prompts present; §4 register absent | a sibling-incident heading fails the wiring test | same test |
| Documentation harness still passes | artifact | checker + unittest | source-citation or future-date failures | command output |
| Product zone/port/fixtures were not copied | manual scoped read | search for source-product identifiers | named hits are defects | this plan |

## Layered completion

- Task acceptance: complete; unittest and repository check passed.
- Task-group or key-result outcome: this plan's end state, not a claim
  that adopters now declare clocks correctly.
- Objective outcome and holistic review: not claimed; verification of the
  new contract stays `partial`.
- Release-gate claims, if applicable: none.

## Progress and closure

- Current executable step: closed at the task layer.
- Blockers and unaffected ready work: none.
- Contract/plan/issue/evidence updates required at closure: this plan
  `completed`; owning contracts reconciled 2026-08-24.
- Final revision and verdict: task-layer complete. Adopter effectiveness
  remains `partial` on the owning contract.

- **2026-08-24 — completed at task layer:** landed the domain-neutral
  contract, D8 routing, `ARCHITECTURE.md` runtime prompts, adopter
  templates, and entrypoint projections.
- **2026-08-24 — consumption corrected:** retracted the 15-row
  `ARCHITECTURE.md` §4 sibling register as ceremony. The contract now
  leads with how to read it. Unittest and `check_docs.py --strict` were
  re-run after the correction. Independent adopter exercise remains open.
