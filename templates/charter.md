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

- Taste corpus (the issuer's corrections and decisions) lives at: {{path}}
- The agent's derivative taste model lives at: {{path}}, labeled as a
  hypothesis wherever used
- Predictions of pending issuer decisions are recorded before each sync at:
  {{path}}
- The per-epoch override rate is reviewed at every sync; a rising rate shrinks
  autonomous scope until calibration
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

- Objective: {{high-level goal}}
- In scope: {{boundaries}}
- Out of scope: {{exclusions}}

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
- Reviewer pass — given the governing contract and evidence, never the
  executor's reasoning trace — fires at: {{milestones or triggers}}
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
