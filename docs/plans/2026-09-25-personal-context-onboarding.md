---
doc_type: plan
status: completed
authority: planning
last_reconciled: 2026-09-25
implements: docs/contracts/project-adoption.md
supersedes: []
---

# Onboarding with separately supplied personal context

## Cold-start summary

The maintainer requested an entry path usable in both new and existing projects:
learn the applicable template discipline, then use separately supplied
collaboration background and decision preferences. Only the general method
belongs in this public repository. Personal profiles and their source material
remain outside it. The public account of the request is
[adoption source 10](../contracts/project-adoption.md#source10--2026-09-25).

Baseline: `203115d1dff37e968def0edce5765b328faa9b86`. The source working tree
was clean. Existing adoption guidance describes a governance migration; it
does not provide an equally clear learning-only route with optional personal
context. Uncertainty routing and bounded delegation already have owners.

## Authority and prerequisites

The maintainer explicitly authorized integrating the general, publishable
method. Adoption owns learning versus migration and privacy during transfer;
governance owns alignment; execution owns delegated context. The documentation
map owns reading routes. Existing project authority and action permissions
remain in force. Personal memory is optional and has no public path dependency.

## Complete end state

An agent can find the entry path from the homepage or working agreement,
orient in a new or running project, resolve only consequential unknowns, and
proceed with authorized work. Personal material stays in its supplied location;
an assignment carries only the context its recipient needs and may receive.

## Current state and gap

Existing contracts already preserve authority, attribute decisions, route
uncertainty, and bound delegation. This change extends those owners and teaches
their use in the existing onboarding guide and handoff template. No new rule
registry, runtime, configuration key, or mandatory template is introduced.

## Execution order within one coherent change

1. Extend adoption, alignment, and delegation at their existing owners.
2. Reconcile the documentation map, onboarding guide, and entrypoints.
3. Update the handoff example; inspect new-project, existing-project, local-fix,
   missing-context, disagreement, and delegation paths.
4. Run repository checks, inspect the public diff for personal material, and
   record the evidence and its limits here.

## Risk register

Material documentation change: several normative owners and their projections
must agree. It changes no runtime authorization or isolation enforcement and
does not migrate any adopting product. Independent high-risk review is not
required. Public disclosure is controlled by transferring only generic methods
and inspecting the entire diff before landing; no personal archive is copied.
Recovery is reverting these documentation edits; no external state is changed.

## Verification matrix

| Claim | Evidence method | Status |
|---|---|---|
| Public routes and citations resolve | Repository tests and documentation checker | Checked on 2026-09-25; see completion record |
| Learning does not force migration or repetitive approvals | Read the entrypoints and follow representative scenarios | Checked on 2026-09-25; see completion record |
| Recipient context preserves relevant intent without copying a profile | Inspect delegation contract and handoff example | Checked on 2026-09-25; see completion record |
| No personal data or private path is introduced | Inspect the complete public diff and targeted scan | Checked on 2026-09-25; see completion record |

Scenario inspection is implementer review, not an independent agent trial or
evidence of long-term adoption effectiveness. Existing partial verification
statuses remain partial.

## Completion record

- Repository suite: 118 tests, 117 passed and one skipped because a command
  named `python3.9` was unavailable to the compatibility probe. The supported
  bundled Python runtime was used. An initial run used the system Python 3.9
  and was rejected by the documented minimum-version guard.
- Updated the fixture clock from 2026-09-17 to 2026-09-25 to match the current
  repository documents. This preserves date validation; no guard was disabled.
- `python3 scripts/check_docs.py --strict`: passed, 34 canonical documents and
  16 templates. Reconciled the project-operation projection after its owning
  contracts changed.
- Public diff: inspected for profiles, private paths, personal quotations,
  resource inventories, and account or health details. Only general methods,
  generic examples, and an English account of the authorized public scope
  were added. A targeted added-line scan found no personal markers.
- Scenario inspection by the implementer: a new project with unknown audience
  resolves that consequential choice; an existing project retains its current
  owners; an authorized local fix proceeds without an interview; a missing
  optional memory does not block unrelated work; a material authority conflict
  follows the existing decision route; parser work and experience review
  receive different context; onboarding alone ends in readiness.
- Handoff inspection: relevant decisions include their reasons, original
  intent remains available for review, and visibility restrictions remain
  attached when context is transferred. A full-session worker is never called
  context-reduced or independent on that basis.
- Independent behavioral trials and long-term adoption were not performed.
  These checks establish structural integration and reviewed instructions.
  Contract verification remains `partial`.
