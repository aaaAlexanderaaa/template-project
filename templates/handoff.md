---
doc_type: evidence
status: historical
authority: evidence
last_reconciled: {{YYYY-MM-DD}}
subject: {{initiative}}
---

# {{Initiative}} cold-start handoff

## Outcome sought

{{One paragraph describing the complete end state.}}

## Read first

1. `ARCHITECTURE.md` § “{{section}}”
2. `docs/contracts/{{contract}}.md`
3. `docs/plans/{{plan}}.md`
4. `{{baseline evidence}}`

## Verified current facts

- {{fact with exact evidence}}

## Completed work

- {{result, revision, and guard}}

## Remaining work

- {{next dependency-ordered action and completion condition}}

## Decisions that must not be re-derived

- {{confirmed decision, authority, and source}}

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
