---
doc_type: contract
status: target
authority: normative
contract_role: governance
implementation: not_started
verification_status: pending
last_reconciled: {{YYYY-MM-DD}}
supersedes: []
---

# {{Project}} autonomous operation charter — {{objective name, or "base layer only"}}

Governing discipline:
[autonomous operation](../docs/contracts/autonomous-operation-discipline.md).
A charter authorizes standing work under current contracts; it never overrides
them, and it never transfers direction, priority, or risk acceptance.

## Purpose and objective

The high-level goal handed to unattended operation, in the issuer's words:
{{goal}}. What the issuer expects to observe on return: {{observable end
state}}.

## Issuer and authority

- Issuer (direction authority): {{owner}}
- This charter is a standing form of declared authorization under
  [governance § work-selection](../docs/contracts/governance-decision-boundary.md#work-selection-consumes-authority).
- Only the issuer may amend or renew this document. The agent may propose
  amendments with motivating evidence; it never edits its own authorization.
- from: source[{{N}}] ({{source date and topic}})

## Base layer

Project-wide; filled once per project.

### Taste corpus and calibration

- Taste corpus (the issuer's corrections and decisions): {{reference}}
- The agent's derivative taste model: {{reference}}, labeled as a hypothesis
  wherever used
- Predictions of pending issuer decisions are recorded before each sync at:
  {{reference}}
- Permitted audience and use of these sources: {{who may read and write them}}

Use references safe for this document's audience under the [personal-context
boundary](../docs/contracts/project-adoption.md#learning-and-personal-context-have-a-bounded-entry-path).
Resolve private locations through approved private context or a persistent locator. Public charters
contain neither private paths nor raw personal material; only project-relevant
decisions authorized for their readers enter public records.

- At sync, review corrections and their causes alongside objective progress,
  result quality, and owner intervention cost under [preference calibration](../docs/contracts/autonomous-operation-discipline.md#taste-lives-in-a-corpus-the-model-is-a-hypothesis).
  Workflow forecasts remain separate; only actual issuer decisions calibrate
  preference predictions. A rising correction rate prompts investigation; pause affected decisions
  when unresolved interpretation or repeated failure risks another material
  error. Continue unaffected work within this charter. This local pause does
  not release a formal `halted` state, which retains its owner-answer recovery
  requirement.
- Taste-dense domains excluded from autonomy entirely: {{domains or "none"}}

### Forbidden zones and resource ceilings

- Never autonomous: {{actions, paths, or systems}}
- Billed, rate-limited, or account-bound ceilings and their stop conditions:
  {{limits}}

### Sync cadence and halt conditions

- Sync schedule and channel: {{cadence}}
- Earliest contact channel for escalations between syncs: {{channel}}
- Any of these halts the affected scope immediately: {{halt conditions}}

## Objective layer

One per objective; copy this section when adding an objective.

### Goal and scope

- Objective: {{high-level goal and the value it should create}}
- Delegated work-selection criteria within the issuer's priorities: {{criteria}}
- Active checkpoint and durable evidence owner: {{existing task/state location}}
- Execution-state update authority: {{who may update that record within the
  delegated criteria and ceilings}}
- In scope: {{boundaries}}
- Out of scope: {{exclusions}}

Keep changing execution state at that checkpoint, outside this issuer-only
authorization: selected effort and baseline, strongest alternative and why it
loses, significant candidate gaps, expected result or learning by review, next
step, and evidence. The executor may revise its approach within this charter;
updates do not amend the goal, priorities, ceilings, expiry, or review bounds.
A missed progress horizon needs fresh review before the same approach continues
or its budget grows. Preserve the original horizon and review decision rather
than silently resetting it in the checkpoint.

### Stop conditions and expiry

- Stop when: {{conditions}}
- Expiry: {{YYYY-MM-DD}} — after this date the agent is dormant or read-only
  for this objective. Renewal is an explicit issuer act; silence is not
  renewal.
- Trigger thresholds are mechanical (dates, counts, check results) wherever
  possible: {{thresholds}}

### Deferral and escalation

- Deferring a fired trigger requires a written record naming the changed
  condition that will allow it to fire.
- The same trigger deferred at two consecutive evaluations escalates through
  the earliest contact channel, and the trigger's action does not run
  autonomously meanwhile.
- Role conflicts that cannot be resolved under this charter go to the issuer
  at the next sync — immediately when high-risk.

## Role and review triggers

- Planner pass: at epoch boundaries and whenever direction is in doubt.
- Fresh direction reviewer: {{separate context, inputs and access; who dispatches it}}
- Maximum review interval and limit on unreviewed work/exposure: {{finite bounds}}
- Dispatch and due-state owner outside executor self-approval: {{harness mechanism}}
- Bring review forward on: {{consequential new assumptions, repeated corrections,
  missing progress, or project-specific signs that judgment is degrading}}
- Review asks openly whether actual results serve the agreed high-level purpose,
  what important problems or alternatives have been missed, and what would change
  that judgment. Give the original intent, relevant accepted taste and trade-offs,
  baseline and artifacts; record first findings before supplying execution rationale.
- A due review waits for a real fresh context; affected expansion pauses until
  reviewed or explicitly excepted by the issuer. Unaffected maintenance can continue.
- Consequential findings are resolved with fresh verification or an issuer decision.
- Before unattended expansion: {{evidence that fresh dispatch works and a missing
  reviewer cannot be replaced by executor approval, including after restart}}
- High-risk here means: {{local high-risk definition}}; it additionally
  requires fresh-context independent review per
  [agent execution](../docs/contracts/agent-execution-discipline.md#independence-is-evidence-not-a-label).

## Renewal and amendment

- Renewal extends an expiry date by issuer edit, with a dated note in the
  reconciliation log.
- Agent amendment proposals name the observed failure that motivates them and
  wait for issuer ratification.

## Source anchors

### source[1] — {{YYYY-MM-DD}}

> "{{the issuer's words authorizing this charter}}"

Context: {{where the authorization was given}}

## Reconciliation log

- **{{YYYY-MM-DD}}:** {{issuance, renewal, amendment, or expiry decision,
  with its reason}}
