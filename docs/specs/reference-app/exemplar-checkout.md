---
id: exemplar.checkout
domain: reference-app
kind: module-spec
summary: "Idempotent checkout feature slice and component-scoped stylesheet."
promise: "Empty idempotency keys are rejected safely, client retries with the same key return the cached receipt without double-charging, and component styles only consume CSS tokens."
owns:
  - "examples/reference-app/features/**"
depends_on:
  - exemplar.domain
  - exemplar.shared
sources:
  - SRC-001
  - SRC-002
  - SRC-013
---

# Reference App — Checkout Feature Slice

## 1. Purpose, Public Interface & Non-Goals

- **Public interface**: Checkout submission handler (`examples/reference-app/features/checkout/service.py`) and component-local stylesheet (`examples/reference-app/features/checkout/CheckoutCard.module.css`).
- **Out of scope**: Top-level application startup (`app/`) or redefining currency tokens (`shared/styles/tokens.css`).

## 2. Runtime Checkout Flow, Retry Cache & Rejection Paths

```mermaid
sequenceDiagram
  participant Caller as Caller / App
  participant Checkout as features/checkout/service.py
  participant Ledger as domain/order_ledger.py
  Caller->>Checkout: submit(idempotency_key, items)
  Checkout-->>Caller: Empty key rejected (ValueError) / Duplicate key returns cached CheckoutReceipt
  Checkout->>Ledger: compute_order_summary(draft) on first valid key
  Ledger-->>Checkout: OrderSummary (computed total >= 0)
  Checkout-->>Caller: Store and return CheckoutReceipt
```

## 3. State Ownership, Hard Invariants & Forbidden Couplings

- **Idempotency & Rejection Invariant**: Blank `idempotency_key` raises an explicit error before any calculation or write; a previously completed key returns its exact stored receipt without calling `Ledger` or charging again.
- **Forbidden couplings**: May depend on `exemplar.domain` and `exemplar.shared`, and must never import upward into `exemplar.app`.
- **Verification**: Tested for empty keys, first-submit receipts, and duplicate-key retry idempotency in `tests/test_reference_exemplar.py`.
