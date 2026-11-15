---
id: domain.reference-app
kind: domain-spec
name: "Reference Modular App Example"
stage: stable
summary: "Compact runnable Python and CSS exemplar under `examples/reference-app/` showing pure domain math, named shared utilities, idempotent checkout, and layered CSS tokens."
promise: "Demonstrates downstream developers how to partition a real application cleanly across `domain/`, `shared/`, `features/`, and `app/` with zero upward imports."
non_goals: "Does not define repository governance rules or run doc/code validation; serves purely as a runnable modular code and CSS token example."
---

# Reference Modular App Example (`examples/reference-app/`)

## 1. Positioning & Non-Goals

This domain is a **live teaching example** verified by automated tests (`tests/test_reference_exemplar.py`)—distinct from `template-project`'s governance rules (`discipline`) and helper validator scripts (`graph-engine`).

## 2. Layer Flow & Failure Boundaries

```mermaid
flowchart LR
  App["app/ (Composition Root)"] --> Checkout["features/checkout/ (Use Case + Scoped CSS)"]
  Checkout --> Domain["domain/ (Pure Order Math)"]
  Checkout --> Shared["shared/ (Money Formatter + styles/tokens.css + styles/layout.css)"]
  Checkout -->|Invalid Key| Reject["ValueError (No Charge or Receipt Stored)"]
```

## 3. Bounded Coupling & Single-Source Rules

| Constraint or Forbidden Coupling | Rule Summary | Enforced By |
|---|---|---|
| Upward imports from `domain/` or `shared/` into `features/` or `app/` | Inner layers stay reusable and side-effect free | `depends_on: []`, `check_docs.py` |
| Catch-all `utils/` or `helpers/` buckets | Shared formatting lives in named value modules (`shared/money.py`) | `validator.py` catch-all ban |
| Duplicate fee calculation or hardcoded CSS hex colors | Order math lives once in `domain/`; colors live in `shared/styles/tokens.css` | `exemplar.domain`, `exemplar.shared` |

## 4. Entrypoints & Fitness Checks

- **Entrypoint**: [main.py](../../../examples/reference-app/app/main.py) (`render_checkout_preview`).
- **Fitness checks**: Run `python3 -m unittest tests/test_reference_exemplar.py` for end-to-end checkout, math, and CSS layer ownership checks, plus `python3 scripts/check_docs.py --strict` for boundary verification.
