---
id: example.module
domain: example
kind: module-spec
summary: "{{One sentence stating what this module does}}"
promise: "{{Observable guarantee to users or callers}}"
owns:
  - "src/example/**"
depends_on: []
sources:
  - SRC-001
supersedes: []
---

# {{Module Title}}

## Public Entrypoint & Owned Scope

State what functions or classes external callers may invoke and what stays internal.

## State Ownership, Invariants & Failure Handling

State which state this module owns exclusively, what hard limits hold before any write or side effect, and how invalid input or external failures behave.

## Runtime / State Flow (`mermaid` when non-trivial)

```mermaid
flowchart LR
  Input["Caller Input"] --> Check{"Validate Constraints"}
  Check -->|Pass| Action["Module Operation"]
  Check -->|Fail| Reject["Clean Error Return"]
```
