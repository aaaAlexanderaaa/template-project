---
doc_type: plan
status: completed
authority: planning
last_reconciled: 2026-08-27
implements: [docs/contracts/development-discipline.md, docs/contracts/agent-execution-discipline.md, docs/contracts/project-adoption.md]
supersedes: []
---

# Collaboration constraints adoption plan

## Cold-start summary

The owner reviewed an external project archive (a long agent-driven build with
its session records) and selected five constraints to deposit into this
template. Four come from the archive's dated human instruction stream; the
fifth is a language-style rule the owner stated during the review. The change
edits three governance contracts, the documentation authority map, the handoff
template, the policy manifest, both guides, and the agent entrypoint. No
product code exists in this repository; the governed surface is the
documentation system itself.

The five constraints, in the owner's wording as translated:

1. multiple parallel sessions need a written coordination method;
2. when a verbal rule recurs, proactively propose writing it as a durable
   rule;
3. handoffs at context exhaustion have mature practices to follow (the
   handoff record was missing fields the archive's practice showed were
   needed);
4. when adopting external material, triage it by authorship before deciding
   how much to trust it;
5. keep document wording in plain style, because the wording of descriptive
   documents guides future language style.

## Authority and prerequisites

- Behavioral contracts: `docs/contracts/development-discipline.md`,
  `docs/contracts/agent-execution-discipline.md`,
  `docs/contracts/project-adoption.md`
- Documentation authority: `docs/README.md`
- Carrier policy: `docs-policy.toml` (handoff required sections)
- Baseline evidence: the archive review conversation of 2026-08-27; the
  archive itself remains outside the repository as scratch material
- Decisions already confirmed: the owner selected exactly these five
  constraints and asked for placement, ordering, and system-impact analysis

## Complete end state

Each constraint has exactly one normative owner, entrypoints route to it, and
the documentation check plus fixture suite pass:

- parallel-work coordination is invariant A9 in the agent execution contract,
  with scope, records, and forbidden-behavior entries;
- verbal-rule persistence is invariant D13 in the development contract;
- authorship triage is invariant O8 in the adoption contract, and the O7
  transfer-value first tier names it;
- the handoff template carries known-pitfalls, parallel-work, and
  session-origin fields, enforced through `docs-policy.toml`;
- plain wording is a language-style section in the documentation authority
  map;
- `AGENTS.md` and both current guides route to the new rules without
  restating them;
- this plan records the placement and ordering rationale.

## Current state and gap

| Activated concern or dependency | Current verified fact | Normative owner | Plan step/evidence gap |
|---|---|---|---|
| Parallel sessions | No invariant covered concurrent agents; collisions were handled ad hoc | `agent-execution-discipline.md` | A9 added |
| Verbal rules | The discipline objective names moving intent out of chat history, but no trigger told an agent when to propose recording | `development-discipline.md` | D13 added |
| Handoff content | Template lacked pitfall, parallel-work, and origin fields | `templates/handoff.md` + `docs-policy.toml` | fields added and registered |
| External material | O7 ranked transfer value but said nothing about evidence strength by author | `project-adoption.md` | O8 added, O7 first tier mentions it |
| Document wording | No language-style norm existed | `docs/README.md` | language-style section added |

## Execution order within one coherent change

### 1. Language style (documentation authority map)

- Files/systems: `docs/README.md`, `AGENTS.md` read order
- Change: add the plain-wording section; route the entrypoint to it
- Guard added: none mechanical — prose style is human judgment (harness H10);
  the rule is a review gate, not a checker rule
- Checkpoint outcome: section present; repository check passes

### 2. Authorship triage (adoption contract)

- Files/systems: `docs/contracts/project-adoption.md`, onboarding guide,
  `AGENTS.md` transfer-value order
- Change: O8 plus the O7 first-tier mention, with source anchor
- Guard added: H2 source-anchor citation checks apply to the edited contract
- Checkpoint outcome: citations resolve bidirectionally

### 3. Verbal-rule persistence (development contract)

- Files/systems: `docs/contracts/development-discipline.md`,
  project-operation guide, `AGENTS.md` contract-first gate
- Change: D13 with source anchor
- Guard added: H2 citation checks
- Checkpoint outcome: citations resolve bidirectionally

### 4. Parallel coordination (agent execution contract)

- Files/systems: `docs/contracts/agent-execution-discipline.md`,
  project-operation guide, `AGENTS.md` execution profile
- Change: A9, scope line, required-record line, two forbidden behaviors
- Guard added: H2 citation checks
- Checkpoint outcome: citations resolve bidirectionally

### 5. Handoff fields (carrier)

- Files/systems: `templates/handoff.md`, `docs-policy.toml`
- Change: three sections added to the template and to the enforced required
  sections
- Guard added: H4 template validation now fails if the sections disappear
- Checkpoint outcome: fixture suite passes against the copied repository

### 6. Dates, fixtures, and verification

- Files/systems: `tests/test_check_docs.py`, frontmatter dates, both guides
- Change: fixture clock and date-sensitive fixtures move to 2026-08-27;
  guides re-dated after projection review
- Commands/probes: `python3 scripts/check_docs.py`, `--strict`, and
  `python3 -m unittest discover -s tests -p 'test_*.py'` under Python 3.11
- Independent verification: not required; governance-documentation change at
  material depth, no high-risk trait activated
- Status updates: contract reconciliation logs, plan status, guide dates

## Risk register

| Risk | Trigger | Impact | Prevention/detection | Recovery |
|---|---|---|---|---|
| New rules read as ceremony | Agents follow A9/D13 mechanically | Noise records | Rules are scoped to their triggers; routine solo work creates nothing | Narrow wording at next reconciliation |
| Fixture clock drift | New canonical dates ahead of FIXED_TODAY | Suite fails on future dates | Bump FIXED_TODAY with the dated docs | Reconcile dates in one commit |
| Projection drift | Guides restate changed contract text | Stale guidance | H12 staleness advisory; guides re-dated only after review | Reconcile projection or remove it |
| Over-attribution to the archive | Treating one project's practice as universal | Miscalibrated rules | O8 applied to the source itself: only human-instruction-grounded lessons adopted; verification stays partial | Revisit after real multi-session use |

## Verification matrix

| Outcome | Unit/class guard | Integration/lifecycle | User-visible/probe | Evidence path |
|---|---|---|---|---|
| Contracts cite new anchors bidirectionally | fixture suite | repository check | checker output | this plan |
| Handoff template carries new sections | H4 template validation | fixture suite | checker output | this plan |
| Entrypoints route without restating | scoped read | strict check | link audit | this plan |
| Dates coherent under fixed clock | fixture suite | repository check | checker output | this plan |

## Explicit non-goals

- No checker rule for prose style; language quality stays a human review gate.
- No new contract document; the five constraints extend existing owners.
- No adoption-assessment template change; the assessment inventories the
  target project, not source material.
- No import of the archive's generated vocabulary; per O8 it is not adopted.

## Progress log

- **2026-08-27 — done:** all edits landed. `python3 scripts/check_docs.py`
  and `--strict` pass; the full fixture suite (107 tests, Python 3.11)
  passes, including the re-dated projection fixtures.

## Completion record

- Final revision/commit: this working tree, 2026-08-27
- Contract implementation status: implemented (three contracts amended)
- Contract verification status: partial (structural checks only; no real
  multi-session project has exercised A9, D13, or O8 yet)
- Issues resolved/superseded: none
- Durable evidence: this plan
