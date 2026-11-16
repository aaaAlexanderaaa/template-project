# Role: Boundary validation and idempotent checkout submission orchestration.
# Out of scope: Order math (delegated to domain.order_ledger) and HTTP server routing.
# Anchors: spec=exemplar.checkout, SRC-011

from __future__ import annotations

from dataclasses import dataclass

from domain import LineItem, OrderDraft, compute_order_summary
from shared import format_cents_usd


@dataclass(frozen=True)
class CheckoutReceipt:
    idempotency_key: str
    order_id: str
    payable_display: str
    item_count: int


class CheckoutSessionStore:
    """Guarantees duplicate client retries return the original receipt."""

    def __init__(self) -> None:
        self._committed: dict[str, CheckoutReceipt] = {}

    def submit(
        self,
        idempotency_key: str,
        order_id: str,
        raw_items: list[tuple[str, int, int]],
        discount_cents: int = 0,
    ) -> CheckoutReceipt:
        key = idempotency_key.strip()
        if not key:
            raise ValueError("idempotency_key is required at feature boundary")
        if key in self._committed:
            return self._committed[key]
        draft = OrderDraft(
            order_id=order_id,
            items=tuple(LineItem(sku=s, unit_cents=u, quantity=q) for s, u, q in raw_items),
            discount_cents=discount_cents,
        )
        summary = compute_order_summary(draft)
        receipt = CheckoutReceipt(
            idempotency_key=key,
            order_id=summary.order_id,
            payable_display=format_cents_usd(summary.payable_cents),
            item_count=summary.item_count,
        )
        self._committed[key] = receipt
        return receipt
