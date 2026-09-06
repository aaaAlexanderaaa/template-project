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

State the original request/source, accepted outcome, verified current facts, governing contract, and
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

## Execution and verification

List actual dependencies and the smallest coherent implementation. Follow
[outcome-driven delivery](../docs/contracts/agent-execution-discipline.md#material-delivery-follows-the-outcome-and-its-evidence):
record a relevant baseline and select credible evidence for each claim. Use a
failing test first when it can expose the defect or protect the behavior; use
artifact, interaction, or review evidence when that is what the claim needs.

| Dependency / step | Complete result | Verification and relevant baseline |
|---|---|---|
| {{actual dependency}} | {{observable result}} | {{test/probe/review and limits}} |

Once the listed human decisions are settled and delivery is authorized,
continue through implementation, integration, verification, and corrections to
closure. Internal checkpoints do not request user approval. A new material
decision or actual blocker pauses its affected path under the governance owner.

## Work-selection fallback

For a bounded task, stop when its outcome is complete. Only an authorized
ongoing portfolio assignment uses the [work-selection fallback](../docs/contracts/agent-execution-discipline.md#work-selection-has-no-silent-idle-state-or-invented-priority).
If it applies, record the selected action and its authority: {{decision}}.

## Review topology

High-risk only: delete this section for material work.

| Stage | Required lenses/context | Reviewer identity | Result or blocked reason |
|---|---|---|---|
| Design | system/contract, user/operator, engineering/maintenance | {{independent contexts}} | {{result}} |
| Synthesis | agreements, disagreements, residual risk | {{separate synthesizer}} | {{result}} |
| Final | fresh context outside implementation | {{verifier}} | {{result}} |

Human governance exception, if any: {{scope, authority, date, residual risk}}

## Verification and evidence matrix

| User outcome / quality boundary | Evidence class | Command/probe | Missing, extra, repeated or suppressed effect / recovery | Result and durable record |
|---|---|---|---|---|
| {{requirement and source}} | {{unit/integration/artifact/real-runtime/manual}} | `{{command}}` | {{applicable negative check or bounded rationale}} | {{path-or-pending; pass/fail/partial/not_run}} |

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
