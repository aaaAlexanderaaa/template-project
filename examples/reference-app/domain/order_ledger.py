# Role: Authoritative single-owner calculation of order totals and idempotency keys.
# Out of scope: Currency string formatting (owned by shared.money) and IO/UI state.
# Anchors: spec=exemplar.domain, SRC-002

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LineItem:
    sku: str
    unit_cents: int
    quantity: int


@dataclass(frozen=True)
class OrderDraft:
    order_id: str
    items: tuple[LineItem, ...]
    discount_cents: int = 0


@dataclass(frozen=True)
class OrderSummary:
    order_id: str
    subtotal_cents: int
    payable_cents: int
    item_count: int


def compute_order_summary(draft: OrderDraft) -> OrderSummary:
    """Single authoritative calculation for order totals across backend and UI."""
    if not draft.order_id.strip():
        raise ValueError("order_id is required")
    for item in draft.items:
        if item.unit_cents < 0 or item.quantity <= 0:
            raise ValueError(f"invalid line item for sku={item.sku}")
    subtotal = sum(item.unit_cents * item.quantity for item in draft.items)
    payable = max(0, subtotal - max(0, draft.discount_cents))
    total_qty = sum(item.quantity for item in draft.items)
    return OrderSummary(
        order_id=draft.order_id,
        subtotal_cents=subtotal,
        payable_cents=payable,
        item_count=total_qty,
    )
