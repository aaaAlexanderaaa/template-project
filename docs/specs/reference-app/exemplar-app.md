---
id: exemplar.app
domain: reference-app
kind: module-spec
summary: "Thin application entrypoint wiring the checkout feature module together."
promise: "Wires feature slices at the top boundary without placing business logic, duplicate totals, or CSS definitions in the entrypoint."
owns:
  - "examples/reference-app/app/**"
depends_on:
  - exemplar.checkout
  - exemplar.domain
  - exemplar.shared
sources:
  - SRC-010
  - SRC-011
---

# Reference App — Application Entrypoint

## 1. Purpose, Public Interface & Non-Goals

- **Public interface**: `examples/reference-app/app/main.py` composition entrypoint (`run_demo_checkout()`).
- **Out of scope**: Order pricing math, idempotency storage, or direct DOM/CSS styling definitions.

## 2. Wiring Flow & Boundaries

```mermaid
flowchart LR
  Input["User Order Payload"] --> App["app/main.py (Build Dependencies Once)"]
  App --> Feature["features/checkout/ (Run Checkout)"]
  Feature -->|Validation or Domain Error| Surface["Return Clean Error Without Side Effects"]
```

## 3. State Ownership & Forbidden Couplings

- **State**: Holds composition wiring references only; delegates transactional order state to `exemplar.checkout`.
- **Forbidden couplings**: Lower layers (`features/`, `domain/`, `shared/`) MUST NOT import `app/`; business rules belong in `domain/`, never in `main.py`.
- **Verification**: Exercised end-to-end by `tests/test_reference_exemplar.py` and `check_docs.py`.
