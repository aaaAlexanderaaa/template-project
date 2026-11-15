---
doc_type: plan
status: completed
authority: planning
last_reconciled: 2026-09-26
implements: docs/contracts/development-discipline.md
supersedes: []
---

# Design methods, preference calibration, and onboarding evidence

## Cold-start summary

The maintainer authorized implementing the proposed refinements: qualify
specific design recipes, interpret corrections by their cause, and exercise
onboarding with a fresh agent doing useful work. Public changes contain the
general methods and evidence limits; supplied personal context stays private.

Baseline: commit `203115d1dff37e968def0edce5765b328faa9b86` plus the completed
[personal-context onboarding change](2026-09-25-personal-context-onboarding.md),
which was already present as local edits. Preserve those edits.

## Authority and prerequisites

The current implementation request ratifies these bounded changes. Development
owns design direction and outcomes; autonomous operation owns calibration;
onboarding explains their use without adding authority. No adopting charter,
running schedule, permission mechanism, or product is being changed.

## Complete end state

Design methods support the actual brief without imposing a task or visual
element count. Correction evidence leads to an appropriate local response
without rewarding agreement or treating useful discovery as failure. Templates
teach the same behavior. Onboarding claims distinguish structural checks,
observed fresh-agent work, and untested deployment conditions.

## Baseline and gap

- Development and the surface template require a single job and at most one
  signature element even where the brief supports a different composition.
- Autonomous operation and the charter template make correction rate the
  main health metric and automatically narrow scope when it rises.
- The previous onboarding change has structural checks and implementer
  scenario inspection, but no fresh-agent use evidence.

## Execution order within one coherent change

1. Reconcile the existing normative owners and their source records.
2. Update the surface and charter templates and affected guidance.
3. Run a fresh agent on a bounded, useful existing-project task through the
   supplied onboarding path; obtain a separate review of the changed rules.
4. Resolve findings, run required checks, inspect the public diff, and record
   evidence before applying the verified change to the source working tree.

## Risk register

Material documentation change across two owners and their teaching material.
It does not change authorization or isolation enforcement; high-risk review is
not required. A separate reviewer challenged the interpretation after the
maintainer requested a new attempt with a named model.
Prevent broad preference exceptions from weakening actual product boundaries;
prevent a cause-based calibration rule from excusing recurring mistakes.
Revert this change's patch to recover, preserving earlier local edits.

## Coordination

The implementer alone edited and integrated the public documents. The first
worker failed before reporting work because workspace credits were exhausted;
further calls stopped until the maintainer requested another attempt using
`gpt-6-sol`. One fresh context then performed the bounded existing-project task
and a separate reading-based review, saving its first observations before the
second part. One follow-up checked the corrections. The worker only read source
projects and used disposable copies; it did not inherit the implementation
conversation, write either source repository, use external services, or delegate.

Private reports remain outside the public repository. The public evidence
records findings, actions, and limitations without personal material. No
additional worker or unattended evaluation loop was introduced.

## Verification matrix

| Outcome | Evidence |
|---|---|
| Methods preserve the brief and its real boundaries | Source/template review with contrasting concrete briefs |
| Calibration distinguishes causes and contains actual risk | Independent reading-based review and correction recheck; runtime risk outcomes remain untested |
| Onboarding supports useful work with relevant context | Fresh-agent read-only task completed; observed package defect repaired and independently rechecked |
| Owners, links, and projections agree | Repository suite and strict documentation check |
| Public content contains no personal profile or locator | Full added-diff inspection |

## Completion record

Documentation implementation, bounded independent use, and review are complete:

- Both normative owners, the surface and charter templates, design guidance,
  onboarding verification, and the operating-guide projection are reconciled.
- Python 3.12 suite: 118 tests, 117 passed and one skipped because the optional
  `python3.9` compatibility command was unavailable. Strict documentation check:
  36 canonical documents and 16 templates, all valid.
- The complete added diff was inspected: no personal profile, private locator,
  resource inventory, or private quotation is included. Earlier working-tree
  edits are preserved; no commit or push is part of this change.
- [Evidence and limits](../evidence/2026-09-26-design-and-onboarding-review.md)
  include initial implementer checks, the independent task and its discovered
  packaging defect, four rule clarifications, and the correction recheck.

The independent task closed the previously unperformed check. The portable
package was repaired and rechecked in its private owner. Four public rule
clarifications were independently reviewed; a final persistent-locator wording
adjustment follows that reviewer's recommendation and has structural inspection.
No rendered UI or multi-epoch runtime validation is claimed. Contract verification
remains partial; the separate long-term first-party epoch-evidence promise is
unchanged. No commit or push was made.
