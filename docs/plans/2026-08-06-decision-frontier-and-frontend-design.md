---
doc_type: plan
status: completed
authority: planning
last_reconciled: 2026-09-17
implements: [docs/contracts/development-discipline.md, docs/contracts/governance-decision-boundary.md]
supersedes: []
---

# Decision sequencing and frontend design adoption

## Cold-start summary

On August 6, the maintainer accepted selected practices from visual-design and
structured-questioning material. The portable outcome was a method for asking
human-owned decisions in dependency order and carrying visual choices through
existing surface and style contracts. Personal tool installation was performed
in the original task but is not part of the template's requirements or public
verification surface.

This public account was revised on September 17 to remove private installation
fingerprints and machine-inventory instructions. It retains the repository
change, its rationale, and the limits of the recorded verification. Historical
invariant codes below describe the names used at the time; current rules use
linked heading titles.

## Risk classification

Material documentation work changed collaboration and frontend guidance. It
changed no product runtime, durable state, or authorization boundary. The
August 6 execution profile did not require independent design review for this
scope. The recorded audit is not independent consumer-effectiveness evidence.

## Authority and prerequisites

The maintainer accepted the repository-level extraction of useful practices.
[Governance](../contracts/governance-decision-boundary.md#missing-knowledge-is-routed-not-automatically-escalated)
owns genuine human decisions and their prerequisite context.
[Development](../contracts/development-discipline.md#frontend-development-contract)
owns frontend design direction and its verification.
`ARCHITECTURE.md` remained an unconfigured product template.

The source assessment and personal installation inventory were not published.
The resulting rules, template fields, and repository history are the available
outputs. The task did not establish those external tools as dependencies for
adopters or certify their current behavior.

## Engineering decision envelope

The authorized repository scope covered collaboration/frontend contracts,
current guides, compact entrypoints, and the frontend-surface template.
Naming, placement, and examples were implementation choices. The change could
not create another glossary, design master, or decision authority alongside
existing surface and style owners.

## Activated concerns and owners

The repository had no product UI or dependency on a personal tool installation.
The change concerned documentation lifecycle, ownership, and reusable design
instructions. Product-specific experience concerns activate in the adopter
when it implements a surface.

## Complete end state

The governance contract routes technical facts to investigation, reversible
local choices to the implementer, and unresolved material preferences to the
owner. A decision is asked after its prerequisites are understood; this does
not require approval at every internal stage.

The frontend contract requires a direction grounded in the brief, deliberate
type/layout/content choices, bounded visual exploration when useful, and
review of the result. Accepted choices belong in the existing surface and
style owners. Guides, entrypoints, and the frontend template expose the method
without defining competing authority.

## Recorded execution and verification

These are recorded August 6 outcomes, not results of a new tool-installation
or product trial. The dated checker commands apply to that historical state;
run the current commands without the historical date on today's checkout.

| Claim | Recorded evidence | Limit |
|---|---|---|
| Frontend template contains design-direction prompts | Declaring the required section first produced `template missing required section: Design direction and content`; adding it passed | Structural fixture, not visual quality |
| Harness regressions remain covered | Python 3.11 fixture suite: 106 tests passed | Repository fixtures only |
| Canonical links, templates, and projections reconcile | Normal and strict documentation checks passed at the August 6 baseline | Does not establish adoption effectiveness |
| One owner remains for each decision | Source audit found no competing decision trigger or visual authority | Same-context review |
| Personal tool replacement | Reported by the original task; machine records are not supplied | Excluded from public reproduction and adopter requirements |

Current structural checks use Python 3.11 or newer:

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
python3 scripts/check_docs.py
python3 scripts/check_docs.py --strict
```

## Work-selection fallback

A source or evidence conflict pauses only the affected projection until its
owner is reconciled. It does not authorize unrelated portfolio work.

## Layered completion

The repository task was recorded complete on August 6: the contract changes,
projections, template guard, and structural checks were delivered. This does
not certify real-adopter design quality, commercial tool compatibility, or an
outside reader's personal environment.

## Progress and closure

- Completed on 2026-08-06; no active execution remains in this plan.
- Publication editing on 2026-08-20 removed absolute machine paths.
- Publication editing on 2026-09-17 also removed inaccessible installation
  fingerprints and instructions that assumed the reader had that machine.
  The portable decision and design methods remain unchanged.
