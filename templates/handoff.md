---
doc_type: evidence
status: historical
authority: evidence
last_reconciled: {{YYYY-MM-DD}}
subject: {{initiative}}
---

# {{Initiative}} cold-start handoff

## Outcome sought

{{Original request/source, accepted interpretation, and the complete end state.}}

Keep an example or chosen artifact distinct from that requested result. State
which original requirement remains when handing off a successful partial step.

## Read first

1. `{{original request/source and accepted outcome}}`
2. `ARCHITECTURE.md` § “{{relevant boundary}}” and
   `docs/contracts/{{contract}}.md` § “{{applicable section and exceptions}}”
3. `{{verified baseline and completion evidence}}`
4. Only if this route needs an active plan:
   `docs/plans/{{plan}}.md` § “{{current executable work}}”

Include only context needed for the next action, plus its original requirements
and governing boundaries. History is linked for investigation, not copied here.
Include relevant accepted trade-offs and their reasons when the next decision
depends on them, plus a locator for applicable reusable experience. Use only
context permitted for this record's audience; retain
personal profiles and private source paths outside public handoffs. Name how
to obtain missing context without exposing it.
Recheck current files; a handoff or agent memory cannot override their authority.
Recover the parent purpose and next action, then obtain the complete applicable
units through [task context](../docs/README.md#task-context). Carry reading
identities and missing evidence as locators; do not substitute a digest list
or this handoff for the source text.
Do not carry `--retained` assertions into a new context; reacquire current rules.
Locate the outcome, facts, decision authority, boundaries, and completion
evidence through these sources. An ordinary handoff requires no new plan or
prior handoff chain.

## Delegated assignment

Delete this section for an ordinary session handoff. For delegated work, record
the parent outcome, expected result, allowed writes/external effects,
baseline/revision, verification, and stop/cancel condition. Return changed
artifacts, checks actually run, unresolved assumptions, and remaining work to
the named integrating owner: {{owner}}. Follow the [delegation owner](../docs/contracts/agent-execution-discipline.md#delegated-work-carries-bounded-context-and-returns-to-an-owner).

## Verified current facts

- {{fact with exact evidence}}
- Working revision, relevant uncommitted changes, and environment: {{identity}}

## Completed work

- {{result, revision, and guard}}

## Remaining work

- {{next dependency-ordered action and completion condition}}
- {{material unresolved assumption and how the next action resolves it, if any}}

This is the current state, not a request to read every earlier handoff. Update
the existing task or plan when resuming; supersede its temporary startup links
at closure while preserving evidence needed for a live claim or recovery.

## Decisions to retain while their conditions hold

- {{confirmed decision, authority, reason, and source; material condition
  that would reopen it, if any}}

Validate these conditions on resume; retain a still-valid commitment. For
ongoing work, carry the selected effort's connection to the parent outcome and
the freedom to revise its approach. A new session alone does not reopen it.

## Reusable experience

- {{relevant successful method or example: locator, observed benefit,
  applicability and invalidation conditions; omit when none is relevant}}
- {{prior failure: locator, symptom and observed conditions, root cause
  or unresolved hypothesis, where to look first, applicability and
  invalidation conditions; omit when none is relevant}}

Follow [experience reuse](../docs/contracts/development-discipline.md#experience-changes-the-next-matching-action).
Link its existing owner; do not paste a growing lesson log into each handoff.
Say whether it was merely saved, incorporated at the matching entrypoint or
observed in a later matching task. Name missing use evidence as unobserved.

## Parallel work in progress

- {{other active sessions or workstreams, their scope, and the shared
  surfaces they touch; write "none known" when working alone}}

## Open conflicts or required operator input

- {{conflict, options, and why it cannot be safely assumed}}

## How to verify

```bash
{{commands}}
```

Expected durable evidence: `{{path}}`.

## Worktree and operational cautions

- Existing unrelated changes: {{paths/none}}
- Services or fixtures required: {{requirements}}
- Destructive or irreversible actions not yet authorized: {{actions/none}}

## Session origin

- Prepared by: {{agent or session identifier}}, {{YYYY-MM-DD}}
- Context state when written: {{fresh / partial / nearly exhausted}}
- Prior handoff, only if needed for provenance or recovery: {{path/none}}
