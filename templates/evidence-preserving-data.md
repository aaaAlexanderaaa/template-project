---
doc_type: contract
status: target
authority: normative
implementation: not_started
verification_status: pending
last_reconciled: {{YYYY-MM-DD}}
supersedes: []
---

# {{Data boundary}} evidence-preserving data contract

## Purpose

Define which inputs are authoritative, which representations are derived, and
how ingestion, migration, compaction, and garbage collection preserve the
ability to reinterpret valuable source evidence.

## Scope

- In scope: {{capture, parse, storage, migration, export, or deletion boundary}}
- Out of scope: {{explicit non-goal}}

## Source anchors

### source[1] — {{YYYY-MM-DD}}

> “{{Stakeholder, incident, legal, or product-value statement about data preservation.}}”

Context: {{source context}}

## Value hierarchy

| Tier | Data/value | Loss policy | Rationale |
|---|---|---|---|
| 1 | {{irreplaceable user/source input}} | {{lossless or explicit human approval}} | {{why}} |
| 2 | {{interaction/process/statistical context}} | {{policy}} | {{why}} |
| 3 | {{derived optimization or architectural mechanism}} | {{rebuild/evict policy}} | {{why}} |

- from: source[{{N}}]

## Authoritative input and derived output

- Authoritative parser/transform input: {{bytes, records, protocol frames}}
- Integrity identity: {{checksum/content address/other}}
- Derived outputs: {{indexes, normalized rows, summaries, caches}}
- Rebuild path and required version identity: {{procedure}}
- Explicitly irreversible operations: {{none or human-approved operation}}

## Activated quality attributes

| Concern | Normative owner | Boundary and failure policy | Evidence |
|---|---|---|---|
| {{security/privacy/capacity/reliability/dependency or none}} | `{{contract and section}}` | {{owned rule or link}} | {{guard/observation}} |

## Preservation invariants

- **DATA-1 — {{name}}.** {{losslessness or recoverability rule}}
- **DATA-2 — {{name}}.** {{bounded-field rule for high-value content}}
- **DATA-3 — {{name}}.** {{prohibition on fixing projections by deleting evidence}}

## Reference inventory and garbage collection

| Referencing owner/field | Target identity | Create/update path | Prune/retire path | Class-level guard |
|---|---|---|---|---|
| `{{owner.field}}` | `{{content identity}}` | `{{path}}` | `{{path}}` | `{{test}}` |

Every new reference site must update all liveness, prune, export, import, and
retirement paths before it can ship.

## Migration and rollback

- Preflight capacity and safety check: {{check}}
- Snapshot/backup identity and cleanup owner: {{plan}}
- Idempotency and resumability: {{contract}}
- Integrity comparison: {{method}}
- Rollback and point-of-no-return: {{procedure}}

## Acceptance evidence

| Claim | Failure-category guard | Migration/integration check | Durable evidence |
|---|---|---|---|
| {{preservation claim}} | {{proportionate sibling-variant test or local-only rationale}} | {{round-trip or fault injection}} | {{path}} |

## Reconciliation log

- **{{YYYY-MM-DD}}:** {{source ambiguity, requirement change, implementation
  regression, translation error, or evidence conflict}}
