# Role: Thin application entrypoint wiring feature public facades together.
# Out of scope: Business calculations (owned by domain) or feature internals.
# Anchors: spec=exemplar.app, SRC-011

from __future__ import annotations

from features.checkout import CheckoutReceipt, CheckoutSessionStore


def run_demo_checkout() -> CheckoutReceipt:
    store = CheckoutSessionStore()
    return store.submit(
        idempotency_key="req-001",
        order_id="ord-100",
        raw_items=[("book-arch", 3200, 1), ("notebook", 900, 2)],
        discount_cents=500,
    )
