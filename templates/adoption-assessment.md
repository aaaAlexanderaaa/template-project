---
doc_type: evidence
status: historical
authority: evidence
last_reconciled: {{YYYY-MM-DD}}
subject: {{project-or-adoption-initiative}}
---

# {{Project}} adoption assessment

## Adoption context

- Project classification: `{{greenfield / brownfield}}`
- Assessment date and assessor/context: {{identity}}
- Requested outcome: {{why the project is adopting the framework}}
- Current delivery obligations: {{active releases, incidents, or commitments}}
- Governing adoption contract:
  `docs/contracts/project-adoption.md`

This assessment is read-only evidence. It does not itself authorize product
rewrites, priority changes, or project-wide enforcement.

## Existing authority inventory

| Concern | Current source/owner | Status | Conflict or uncertainty |
|---|---|---|---|
| Product direction and priority | {{person, tracker, or document}} | {{verified/unknown}} | {{finding}} |
| Architecture and boundaries | {{path/owner}} | {{verified/partial/absent}} | {{finding}} |
| Product behavior/contracts | {{paths/owners}} | {{verified/partial/absent}} | {{finding}} |
| Delivery, CI, and release | {{paths/systems/owners}} | {{verified/partial/absent}} | {{finding}} |
| Agent/contributor instructions | {{paths/owners}} | {{verified/partial/absent}} | {{finding}} |

Preserve existing authority until it is explicitly reconciled or superseded.

## Current-state baseline

- Product source roots: {{repository-relative paths}}
- Runtime and deployable units: {{facts}}
- Test and verification entrypoints: {{commands}}
- CI/release/rollback path: {{facts}}
- Current documentation topology: {{facts}}
- Known debt and historical exceptions: {{bounded inventory or links}}
- Implicit clock, timezone, or live demo/seed dataset, if any:
  {{fact / absent / unknown}}
- Facts that could not be verified: {{unknowns}}

Record current truth separately from desired architecture or governance.

## Governance profile and scope

- Selected profile: `{{project-defined profile name and meaning}}`
- Managed paths and boundaries: {{scope}}
- Explicit exclusions: {{scope and reason}}
- Rules immediately enforced: {{rules}}
- Rules initially advisory: {{rules and promotion condition}}
- Existing instructions to preserve or reconcile: {{paths}}

The adopting human owner confirms profile and scope; the assessor recommends
but does not select them.

## Priority and decision authority

- Product/direction owner: {{identity}}
- Authoritative priority source: {{tracker, document, owner, or not yet declared}}
- Risk-acceptance authority: {{identity and limits}}
- Declared engineering risk budget: {{budget or none; absence uses governance
  G6's locally reversible, no-uncontracted-durable-effect default}}
- Governance-exception authority: {{identity and limits}}
- Decisions still required: {{decision, options, and requested owner}}

If no priority source is declared, discovered work remains a recommendation.

## Risk and conflict register

| Classification | Finding and evidence | Affected scope | Options/recovery | Owner |
|---|---|---|---|---|
| `{{fact / risk / recommendation / human_decision_required / execution_blocker}}` | {{finding}} | {{scope}} | {{options}} | {{owner}} |

Only the blocker classes permitted by the governance decision-boundary
contract may use `execution_blocker`.

## Stage decision

- Current stage: `{{observed / baselined / scoped_enforcement / adopted}}`
- Entry evidence: {{evidence}}
- Exit criteria for the next stage: {{outcomes}}
- Human confirmation: {{owner, decision, date}}
- Residual baseline debt and disposition: {{links/owners}}
- Recovery stage if evidence is disproved: {{stage and procedure}}

## Migration plan link

- Implementation plan: `docs/plans/{{YYYY-MM-DD-topic}}.md`
- First managed boundary: {{boundary and reason}}
- Sequencing constraints: {{dependencies}}
- Work explicitly not authorized by onboarding: {{non-goals}}

Use the normal implementation-plan template; do not turn this assessment into
an execution history.

## Verification and completion

| Adoption claim | Evidence/probe | Result | Limitation |
|---|---|---|---|
| {{claim}} | `{{command-or-path}}` | {{pass/fail/partial}} | {{what it does not prove}} |

- Stage allowed to close: {{stage}}
- Higher stage still open: {{stage and gap}}
- Contract/guide/plan updates required: {{paths}}
- Final human adoption decision: {{decision, owner, date}}

## Limitations

- {{Missing access, environment, stakeholder authority, evidence, or scope}}
