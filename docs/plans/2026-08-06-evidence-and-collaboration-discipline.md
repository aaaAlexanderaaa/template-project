---
doc_type: plan
status: completed
authority: planning
last_reconciled: 2026-09-17
implements: [docs/contracts/development-discipline.md, docs/contracts/governance-decision-boundary.md]
supersedes: []
---

# Evidence and collaboration discipline implementation plan

## Cold-start summary

The template owner selected five collaboration defaults for this template: research unfamiliar references instead of guessing, seek fallbacks
when a tool is unavailable, return material preference and trade-off decisions
as bounded choices, surface more consequential unasked issues, and explain
causal mechanisms instead of manufacturing abstract depth. The normative
translations are now in development D10-D12 and governance G7. The remaining
work is to project them through contributor and agent entrypoints, reconcile
the current operating and onboarding guides, verify the documentation graph,
and close this plan.

## Risk classification

- Profile: `material`
- Rationale: the change alters repository-wide collaboration and decision
  semantics consumed by every adopter, but changes no architecture,
  authorization, irreversible state, cross-process compatibility, or
  high-impact user interaction.
- Required independent review: no; A1 reserves it for the high-risk profile.

## Authority and prerequisites

- Structural authority: `ARCHITECTURE.md` declares this repository an
  unconfigured product template, so no product boundary is changed.
- Behavioral contracts:
  `docs/contracts/development-discipline.md` D10-D12 and
  `docs/contracts/governance-decision-boundary.md` G6-G7.
- Human authorization: the template owner confirmed on 2026-08-06 that these
  collaboration defaults apply within this template and accepted the proposed
  uncertainty routing. An adopter chooses its own scope and authority.
- Baseline evidence: repository inspection found existing technical-unknown
  and reversible-choice routing but no explicit external-reference,
  tool-fallback, latent-question, or causal-explanation rules.

## Engineering decision envelope

- Authorized outcome and managed scope: collaboration contracts and their
  compact projections in root entrypoints and current operating guidance.
- Applicable boundary: one normative rule keeps one owner; entrypoints route or
  project without redefining trigger semantics.
- Reversible choices: wording, section placement, and concise cross-references.
- Human decisions still required: none.

## Activated concerns and owners

No product-facing D8 quality concern is activated. Documentation lifecycle and
single-owner integrity remain governed by `docs/README.md` and development D9;
the plan records only reconciliation and verification steps.

## Complete end state

Dated English accounts of the accepted decisions remain in the two contracts. Those
contracts define one uncertainty route: research checkable facts, use
capability-preserving fallbacks, investigate technical unknowns, decide
reversible internal mechanics, and offer bounded options for human-owned
material decisions. Agent, contributor, README, and operation entrypoints make
the route discoverable without becoming competing owners; the onboarding guide
is reconciled against its updated governance source. All canonical dates,
implementation states, verification notes, and this plan's lifecycle are
reconciled.

## Seven-phase execution loop

| Phase | Required output | Applicability or evidence |
|---|---|---|
| 1. Domain and authority | Existing D1/D4/D6/D9, G2/G6/G7, A8 and authority-map boundaries inspected | Completed through the repository read set |
| 2. Fixture or controlled boundary | Existing repository is the documentation fixture | `rg` baseline and current entrypoint reads |
| 3. Contract and design | D10-D12 and expanded G7 land before projections | Completed on 2026-08-06 |
| 4. Test first | Stable semantic behavior is not mechanically decidable | No new syntax is introduced; pre-change search established the missing projections |
| 5. Implementation | Reconcile agent, contributor, README, operating-guide, and onboarding projections | Completed on 2026-08-06 |
| 6. Regression | Run fixture suite and repository checker with Python 3.11+ | 106 tests and strict repository check pass under Python 3.11 |
| 7. Holistic evaluation | Audit owner uniqueness, route completeness, and conflict with G6 | Complete: D10-D12 own inquiry mechanics; G7 owns routing; projections add no competing trigger |

## Work-selection fallback

If a verification tool is unavailable, apply development D11: identify the
required evidence, try a semantics-preserving alternative, and report any
remaining limitation. No unrelated portfolio work is authorized by this plan.

## Verification and evidence matrix

| Claim | Evidence class | Command/probe | Expected failure/negative path | Durable record |
|---|---|---|---|---|
| Canonical documentation remains structurally valid | fixture suite | `python3 -m unittest discover -s tests -p 'test_*.py'` | malformed lifecycle or template relationships fail | Contract acceptance notes |
| Repository lifecycle and projections reconcile | repository check | `python3 scripts/check_docs.py` | stale or invalid canonical records fail | Contract acceptance notes |
| The five preferences have one complete route | source audit | `rg -n "D10|D11|D12|G7|fallback|causal|option" AGENTS.md CONTRIBUTING.md README.md docs` | missing owner or competing trigger semantics keeps the plan active | Plan completion record |

## Layered completion

- Task acceptance: complete; all requested preference translations and
  projections are present and verified.
- Task-group outcome: complete; the source audit found one normative owner per
  rule and no conflict with G6's reversible engineering discretion.
- Objective outcome: outside this plan; this closes only the requested
  collaboration-discipline change.
- Release gate: not applicable.

## Progress and closure

- Current executable step: none; plan complete.
- Blockers and unaffected ready work: none.
- Closure updates: contract implementation and verification metadata,
  acceptance notes, guide reconciliation dates, fixture date, and this plan
  status are complete.
- Final revision and verdict: completed on 2026-08-06. The task layer is
  complete; real-adopter behavioral effectiveness remains covered by the
  contracts' existing partial verification posture.
