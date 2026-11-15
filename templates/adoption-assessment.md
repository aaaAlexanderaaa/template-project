---
doc_type: guide
status: current
authority: guidance
---

# Adoption Assessment

Record concrete repository facts before enabling enforcement in an existing
project:

- **Project purpose & current maturity stage**: `prototype` | `usable` | `stable`
- **Source roots & existing tooling**: `source_roots` and test commands
- **Rule applicability summary**:
  - Satisfied locally (cite existing files/checks)
  - Adopting now (list target domains/specs)
  - Not applicable (cite concrete repository fact)
- **Initial `[adoption].stage`**: `observed` → `scoped_enforcement` → `adopted`
