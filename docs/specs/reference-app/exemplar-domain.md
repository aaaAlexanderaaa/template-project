---
id: exemplar.domain
domain: reference-app
kind: module-spec
summary: "Pure order-ledger calculation example with zero UI, feature, or app imports."
promise: "Order subtotal, discount clamping, and item counts are computed once in a pure function with zero side effects or invalid negative totals."
owns:
  - "examples/reference-app/domain/**"
depends_on: []
sources:
  - SRC-010
  - SRC-011
---

# Reference App — Pure Domain Layer

## 1. Purpose, Public Interface & Non-Goals

- **Public interface**: `compute_order_summary(draft)` and domain dataclasses inside `examples/reference-app/domain/order_ledger.py`.
- **Out of scope**: Persistence, HTTP requests, idempotency caching, or string formatting/CSS.

## 2. Pure Calculation & Validation Flow

```mermaid
flowchart LR
  Draft["OrderDraft (Items + Discount)"] --> Guard{"Valid Quantities & Non-Negative Prices?"}
  Guard -->|Valid| Math["Clamp Discount <= Subtotal & Compute Total Once"]
  Guard -->|Invalid| Err["Raise ValueError (Never Clamp Silent Negative Inputs)"]
```

## 3. State Ownership, Hard Invariants & Forbidden Couplings

- **Single calculation invariant**: Total order value is never recomputed downstream; discounts clamp at subtotal (`total >= 0`).
- **Forbidden couplings**: `depends_on: []` — never imports `shared/`, `features/`, or `app/`.
- **Verification**: Tested by `tests/test_reference_exemplar.py` and import checks in `check_docs.py`.
