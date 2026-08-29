---
doc_type: plan
status: active
authority: planning
last_reconciled: {{YYYY-MM-DD}}
implements: docs/contracts/{{contract}}.md
supersedes: []
---

# {{Initiative}} agent execution plan

## Cold-start summary

State the requested outcome, verified current facts, governing contract, and
the next executable action so another context can continue without chat
history. Routine work and disposable experiments do not use this delivery-plan
template solely to prove their classification.

## Risk classification

- Profile: `{{material / high-risk}}`
- Rationale: {{changed semantics, boundaries, data, users, or failure surface}}
- Required independent review: {{yes/no and governing reason}}

Do not downgrade risk merely because an independent reviewer is unavailable.

## Authority and prerequisites

- Structural authority: `ARCHITECTURE.md` § “{{section}}”
- Behavioral contract: `docs/contracts/{{contract}}.md`
- Surface contract, if applicable: `docs/design/{{surface}}.md`
- Active issue or objective: `{{path-or-id}}`
- Priority source or human authorization: `{{tracker/path/owner and decision}}`
- Baseline evidence: `{{path-or-command}}`

## Engineering decision envelope

- Authorized outcome and managed scope: {{owner/source and boundary}}
- Applicable public contracts and permission boundaries: {{links}}
- Declared risk budget, if any: {{budget or none}}
- Reversible engineering choices that proceed without serial approval:
  {{choices}}
- Human decisions still required: {{product intent, authority, or risk
  acceptance; none if absent}}

## Activated concerns and owners

List only concerns activated through [development § activate-concerns](../docs/contracts/development-discipline.md#activate-concerns-instead-of-expanding-ceremony). The linked current or
target contract owns each boundary, failure policy, and escalation/exception
policy; this plan owns only steps and evidence. Do not copy the [development § activate-concerns](../docs/contracts/development-discipline.md#activate-concerns-instead-of-expanding-ceremony) trigger table.

| Activated concern | Normative owner and section | Implementation steps | Evidence |
|---|---|---|---|
| {{concern or none}} | `{{contract and section}}` | {{steps}} | {{guard/probe}} |

## Complete end state

Describe the coherent final behavior. Temporary sequencing is not permission
to leave an undocumented coexistence state behind.

## Seven-phase execution loop

| Phase | Required output | Applicability or evidence |
|---|---|---|
| 1. Domain and authority | Terms, owners, current behavior, conflicts | {{record}} |
| 2. Fixture or controlled boundary | Realistic sanitized input or deterministic seam | {{record}} |
| 3. Contract and design | Landed normative behavior and boundaries | {{record}} |
| 4. Test first | Acceptance guard and observed pre-implementation failure | {{record}} |
| 5. Implementation | Smallest coherent complete change | {{record}} |
| 6. Regression | Affected class, integration, and compatibility checks | {{record}} |
| 7. Holistic evaluation | Result against the contract and activated quality outcomes | {{record}} |

For any non-applicable phase, record the concrete reason.

## Work-selection fallback

When the named task cannot proceed, record which step selected the next work:

1. resume truthful in-progress work that is already authorized;
2. diagnose the blocker without treating it as project-wide;
3. consume the highest-priority ready work from the declared priority source;
4. review the active portfolio read-only for uncovered outcomes or quality gaps;
5. record candidate work with facts, risk, dependencies, and limitations;
6. when priority is absent, request a human decision before non-trivial work;
7. verify completed task groups against their parent outcome.

Selected action and authority: {{decision}}

## Review topology

High-risk only: delete this section for material work.

| Stage | Required lenses/context | Reviewer identity | Result or blocked reason |
|---|---|---|---|
| Design | system/contract, user/operator, engineering/maintenance | {{independent contexts}} | {{result}} |
| Synthesis | agreements, disagreements, residual risk | {{separate synthesizer}} | {{result}} |
| Final | fresh context outside implementation | {{verifier}} | {{result}} |

Human governance exception, if any: {{scope, authority, date, residual risk}}

## Verification and evidence matrix

| Claim | Evidence class | Command/probe | Expected failure/negative path | Durable record |
|---|---|---|---|---|
| {{observable claim}} | {{unit/integration/artifact/real-runtime/manual}} | `{{command}}` | {{negative check}} | {{path-or-pending}} |

## Layered completion

- Task acceptance: {{state and evidence}}
- Task-group or key-result outcome: {{state and evidence}}
- Objective outcome and holistic review: {{state and evidence}}
- Release-gate claims, if applicable: {{state and evidence}}

Lower layers do not imply that higher layers are complete.

## Progress and closure

- Current executable step: {{step}}
- Blockers and unaffected ready work: {{facts}}
- Contract/plan/issue/evidence updates required at closure: {{paths}}
- Final revision and verdict: {{pending or result}}
