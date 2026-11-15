---
doc_type: plan
status: completed
authority: planning
last_reconciled: 2026-07-26
implements: [docs/contracts/governance-decision-boundary.md, docs/contracts/project-adoption.md]
supersedes: []
---

# Bounded governance and AI-guided onboarding plan

## Cold-start summary

The repository has strong contract-first change execution but does not yet
state a sufficiently narrow governance decision boundary or give greenfield and
brownfield adopters a staged AI-guided onboarding path. The confirmed end state
keeps product direction and priority with humans, limits blockers to truthful
and safe execution conditions, and introduces an adoption assessment plus
guides without building a new project-management or onboarding application.

## Risk classification

- Profile: `material`
- Rationale: changes two public governance contracts and multiple human/agent
  entrypoints, but is reversible documentation-harness work with no product
  runtime, authorization, irreversible data, or cross-process compatibility
  change.
- Required independent review: no; final review will be explicitly labeled
  same-context and non-independent.

## Authority and prerequisites

- Structural authority: `ARCHITECTURE.md` remains an unconfigured template.
- Base discipline: `docs/contracts/development-discipline.md`
- Agent profile: `docs/contracts/agent-execution-discipline.md`
- New targets: `docs/contracts/governance-decision-boundary.md` and
  `docs/contracts/project-adoption.md`
- Confirmed human choice: limited governance authority, AI-guided onboarding,
  and staged brownfield enforcement.
- Baseline evidence: 34 fixture tests and the six-document/thirteen-template
  repository check pass on Python 3.11–3.14.

## Complete end state

An adopter can distinguish decision authority from governance advice, run a
documented greenfield or brownfield onboarding process, preserve current truth
and existing authority, record one structured adoption assessment, choose a
managed scope and stage, and continue project work using human-owned priority.
All repository entrypoints agree, and the template inventory is mechanically
guarded.

## Seven-phase execution loop

| Phase | Required output | Applicability or evidence |
|---|---|---|
| 1. Domain and authority | Confirmed governance boundary and onboarding model | User decisions plus current contracts reviewed |
| 2. Fixture or controlled boundary | Existing repository fixture suite | Repository-copy fixtures remain deterministic |
| 3. Contract and design | Two target contracts and this active plan | Land before entrypoint/template implementation |
| 4. Test first | Adoption-template inventory and section guards | Both targeted tests failed before the template existed, then passed after implementation |
| 5. Implementation | Guides, assessment template, policy/checker wiring, reconciled entrypoints | Complete |
| 6. Regression | Python 3.11 suite, repository checker, Ruff, whitespace, cross-version checks | Complete — 36 tests on Python 3.11–3.14, 12 canonical docs, 14 templates |
| 7. Holistic evaluation | Same-context non-independent adopter review | PASS at task-group layer; real adoption remains unverified |

## Work-selection fallback

Not applicable while the named implementation remains executable. If it
blocks, only already authorized work in this plan may continue; newly
discovered work is recorded as a recommendation for human priority.

## Review topology

| Stage | Required lenses/context | Reviewer identity | Result or blocked reason |
|---|---|---|---|
| Design | system/contract, adopter experience, maintenance | Current implementation context | Confirmed by human direction; non-independent |
| Synthesis | reconcile authority, friction, and enforcement | Current implementation context | Recorded in the two target contracts |
| Final | fresh read of entrypoints and adoption path | Current context after regression | PASS at task-group layer; explicitly non-independent |

Human governance exception: none required because independent review is not a
requirement for the recorded material profile.

## Verification and evidence matrix

| Claim | Evidence class | Command/probe | Expected failure/negative path | Durable record |
|---|---|---|---|---|
| Assessment template is first-class | Fixture guard | `python -m unittest tests.test_check_docs` | Missing file and missing required section fail | Contract acceptance record |
| Canonical docs and links align | Repository integration | `python scripts/check_docs.py` | Broken metadata/link/section fails | Contract acceptance record |
| Existing checker behavior remains stable | Regression | full unittest suite | Existing 34 cases remain green | Plan completion record |
| Onboarding is usable without chat history | Structured cold read | follow README → guide → assessment → plan | Missing authority or stage remains explicit | Final holistic note |

## Layered completion

- Task acceptance: complete; new template guards and affected regression pass.
- Task-group outcome: complete; entrypoints, contracts, guides, template,
  checker inventory, and lifecycle agree.
- Objective outcome: the documented governance/onboarding capability is
  implemented; real-project adoption remains separately verifying.
- Release-gate claims: not applicable to this template-only change.

## Progress and closure

- Current executable step: none within this completed task group.
- Blockers and unaffected ready work: real-project adoption evidence is not a
  blocker for the documented template capability and remains explicitly open.
- Closure updates: both contracts are current/implemented/partial; this plan is
  completed; the holistic record is historical evidence.
- Final revision and verdict: working tree verified; commit intentionally left
  to the repository owner. PASS at task-group layer.

Verification evidence:

- `uv run --python 3.11 python -m unittest discover -s tests -p 'test_*.py'`
  through Python 3.14: PASS, 36 tests on every runtime;
- `uv run --python 3.11 python scripts/check_docs.py --today 2026-07-26`:
  PASS, 12 canonical documents and 14 templates;
- Ruff, Python compileall, and `git diff --check`: PASS;
- [holistic evaluation](../evidence/2026-07-26-bounded-governance-onboarding-evaluation.md):
  PASS, same-context and non-independent, with real adoption limitations.
