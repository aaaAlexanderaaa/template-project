---
doc_type: plan
status: completed
authority: planning
last_reconciled: 2026-08-06
implements: [docs/contracts/development-discipline.md, docs/contracts/governance-decision-boundary.md]
supersedes: []
---

# Decision frontier and frontend design adoption plan

## Cold-start summary

The template owner approved the prior evaluation: adopt Anthropic's
`frontend-design` skill, uninstall `ui-ux-pro-max`, extract the dependency-aware
decision-frontier method from the reviewed grilling skills, and absorb only the
frontend practices that fit this repository's existing authority model. The
normative owners remain development's frontend contract and governance G7;
guides, entrypoints, and templates will project those rules without introducing
`CONTEXT.md`, ADRs, or a second design-system authority.

## Risk classification

- Profile: `material`
- Rationale: the change alters reusable collaboration and frontend-delivery
  behavior consumed by adopters, but changes no product architecture,
  authorization, durable state, cross-process compatibility, or high-impact
  user interaction.
- Required independent review: no; A1 reserves independent design and
  fresh-context completion review for high-risk work.

## Authority and prerequisites

- Structural authority: `ARCHITECTURE.md` remains an unconfigured product
  template; no product boundary changes.
- Behavioral contracts: `docs/contracts/development-discipline.md` owns
  frontend delivery and document ownership; `docs/contracts/governance-decision-boundary.md`
  G7 owns uncertainty routing and human-decision triggers.
- Human authorization: on 2026-08-06 the template owner approved the evaluated
  adoption, uninstall, and project-level learning scope.
- External source baseline: Anthropic `frontend-design` at commit
  `2235be7c60b551f5de82ade908fd3816455afcda`, Matt Pocock `grilling` at
  `1495d014303e041c51c29f9e442485ba06f5878d`, and `domain-modeling` at
  `ee8bae40062cd6b435073368ed0c540f48c35862`. The installed Anthropic
  `SKILL.md` and `LICENSE.txt` SHA-256 values are respectively
  `1608ea77fbb6fc30d13a97d12cfa8ebf31358d40f0dd97beed24829d6b3f45dd`
  and `0d542e0c8804e39aa7f37eb00da5a762149dc682d7829451287e11b938e94594`,
  matching the upstream `main` content retrieved during installation.
- Repository baseline: no active target contract or plan conflicts with this
  work; the worktree was clean before edits.

## Engineering decision envelope

- Authorized outcome and managed scope: personal Codex skill installation and
  the repository's collaboration/frontend contracts, current operation guide,
  compact entrypoints, and frontend surface template.
- Applicable boundaries: one normative rule keeps one owner; design candidates
  must resolve into existing surface/style owners and cannot become a parallel
  `MASTER.md`, glossary, or ADR authority.
- Reversible choices: wording, section placement, guide examples, template
  prompts, and a recoverable archive location for the uninstalled skill.
- Human decisions still required: none; the owner selected the skill and
  approved the previously described extraction boundary.

## Activated concerns and owners

No product-facing D8 concern is activated because this repository contains no
product UI and will not depend on either personal skill at runtime. Document
lifecycle and owner uniqueness remain governed by `docs/README.md` and
development D9. The external skill operation is verified separately as local
tool configuration rather than represented as a product dependency.

## Complete end state

`frontend-design` is installed under the Codex skills directory with its
upstream license and instructions intact; `ui-ux-pro-max` no longer appears in
the active skills directory and remains recoverable outside it. G7 defines a
dependency-aware frontier only for genuine human decisions and retains its
fact/local-choice routing. The frontend contract requires brief-specific,
subject-grounded direction, intentional type/layout/content, bounded visual
exploration, and self-critique while preserving surface/style ownership.
Current guidance, root entrypoints, and the reusable surface template expose
the adopted method without becoming competing authorities. All fixture,
repository, source-audit, and skill-installation checks pass.

## Seven-phase execution loop

| Phase | Required output | Applicability or evidence |
|---|---|---|
| 1. Domain and authority | Current architecture, documentation map, D1-D12, G1-G7, A1-A8, design README, and active plan set inspected | Completed before edits |
| 2. Fixture or controlled boundary | Current repository plus exact local skill directories form the controlled boundary | Clean worktree and resolved paths recorded |
| 3. Contract and design | G7 decision-frontier boundary and frontend design-direction contract land before projections | Completed before guide, entrypoint, and template edits |
| 4. Test first | Template-required design-direction section is declared before the template supplies it, and the focused repository check must fail for that absence | Completed: Python 3.11 check failed only with `template missing required section: Design direction and content`, then passed after the template change |
| 5. Implementation | Install/archive skills; update guide, entrypoints, design README, and frontend template | Completed; old skill archived in the local Codex skill-backup directory as `ui-ux-pro-max-2026-08-06` |
| 6. Regression | Run Python 3.11+ fixture suite, normal/strict repository checks, source audits, and skill inventory checks | Completed: 106 tests and both repository modes pass; diff and inventory audits are clean |
| 7. Holistic evaluation | Audit owner uniqueness, G6 proportionality, brief fidelity, second-authority absence, and recovery path | Completed: G7 owns the frontier trigger, development owns frontend direction, and projections introduce no glossary, ADR, or design master |

## Work-selection fallback

If the GitHub installation helper fails, use the skill installer's documented
download-to-git fallback and preserve the same repository/path/ref identity. If
contract or checker evidence conflicts, stop only the affected projection,
reconcile its owner, and do not substitute unrelated portfolio work.

## Verification and evidence matrix

| Claim | Evidence class | Command/probe | Expected failure/negative path | Durable record |
|---|---|---|---|---|
| Frontend template exposes the adopted design-direction owner | fixture/repository structure | `uv run --python 3.11 python scripts/check_docs.py --today 2026-08-06` | missing required template section produced the expected pre-implementation failure | Plan completion record |
| Documentation harness remains stable | fixture suite | `uv run --python 3.11 python -m unittest discover -s tests -p 'test_*.py'` | malformed templates or lifecycle records fail | 106 tests pass |
| Canonical graph and projections reconcile | repository checks | `uv run --python 3.11 python scripts/check_docs.py --today 2026-08-06` and the same command with `--strict` | invalid source/projection/template relationships fail | Both modes pass |
| Frontier and frontend rules retain one owner | source audit | `rg -n "decision frontier|design thesis|generic default|second.*authority" AGENTS.md CONTRIBUTING.md README.md docs templates` | competing triggers or unowned design sources keep the plan active | Plan completion record |
| Skill replacement is complete and recoverable | local inventory | inspect the local Codex skills directory and the dated backup | both active skills or missing replacement fails handoff | Plan completion record |

## Layered completion

- Task acceptance: complete; contract, skill replacement, projections, template
  guard, and verification all match the authorized outcome.
- Task-group outcome: complete; the owner-uniqueness and coherent-end-state
  audit found no competing decision trigger or visual authority.
- Objective outcome: outside this plan; this closes only the approved skill and
  discipline adoption.
- Release gate: not applicable.

## Progress and closure

- Current executable step: none; plan complete.
- Blockers and unaffected ready work: none.
- Closure updates: contract source/reconciliation notes, guide and design
  projections, template guard, skill inventory, and this plan status are
  reconciled.
- Final revision and verdict: completed on 2026-08-06. The task and task-group
  layers are complete; real-adopter design and decision effectiveness remains
  covered by the contracts' existing partial verification posture.
- **2026-08-20 — publication redaction:** local skill-directory paths were
  replaced with host-independent descriptions; the recorded skill names and
  backup date are unchanged.
