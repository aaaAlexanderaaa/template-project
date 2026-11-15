---
id: domain.example
kind: domain-spec
name: "{{Domain Name}}"
stage: usable
summary: "{{What bounded subsystem responsibility this domain owns}}"
promise: "{{What observable guarantee this domain provides to users or sibling domains}}"
---

# {{Domain Name}}

## Domain Role & Runtime Flow

State what enters this subsystem, what stays outside it, and how work runs
from entry to output (including failure paths):

```mermaid
flowchart LR
  API["Public Entrypoint"] --> Service["Domain Logic"]
  Service --> Store["Single Authoritative Store"]
  Service -->|Invalid or Failed| Error["Explicit Failure Path"]
```

## Narrow Interfaces & Forbidden Couplings

- **Public Interface**: {{Functions, routes, or CLI entrypoints exposed to sibling domains}}
- **Forbidden Couplings**: {{Cross-domain imports or direct state mutations banned here}}
- **Hard Invariants & Constraints**: {{Data limits, idempotency, authorization, or compatibility guards}}
