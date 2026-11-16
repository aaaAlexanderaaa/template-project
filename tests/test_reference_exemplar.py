# Role: End-to-end unit and boundary tests for the modular reference exemplar under examples/reference-app/.
# Out of scope: Repository governance validation (covered by test_ssot_and_check_docs.py).
# Anchors: spec=exemplar.domain, spec=exemplar.shared, spec=exemplar.checkout, SRC-010, SRC-011

from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXEMPLAR_ROOT = ROOT / "examples" / "reference-app"
if str(EXEMPLAR_ROOT) not in sys.path:
    sys.path.insert(0, str(EXEMPLAR_ROOT))

from app.main import run_demo_checkout  # noqa: E402
from domain import LineItem, OrderDraft, compute_order_summary  # noqa: E402
from features.checkout import CheckoutReceipt, CheckoutSessionStore  # noqa: E402
from shared import format_cents_usd  # noqa: E402


class ReferenceExemplarTests(unittest.TestCase):
    def test_order_ledger_single_source_computation_and_clamping(self) -> None:
        items = (
            LineItem(sku="plan-team", unit_cents=4900, quantity=2),
            LineItem(sku="addon-audit", unit_cents=1500, quantity=1),
        )
        summary = compute_order_summary(OrderDraft(order_id="ord-1", items=items, discount_cents=2000))
        self.assertEqual(summary.subtotal_cents, 11300)
        self.assertEqual(summary.payable_cents, 9300)
        self.assertEqual(summary.item_count, 3)

        clamped = compute_order_summary(OrderDraft(order_id="ord-2", items=items, discount_cents=99999))
        self.assertEqual(clamped.payable_cents, 0)

    def test_order_ledger_rejects_invalid_inputs(self) -> None:
        with self.assertRaises(ValueError):
            compute_order_summary(OrderDraft(order_id="  ", items=(LineItem(sku="a", unit_cents=100, quantity=1),)))
        with self.assertRaises(ValueError):
            compute_order_summary(OrderDraft(order_id="o1", items=(LineItem(sku="a", unit_cents=-1, quantity=1),)))
        with self.assertRaises(ValueError):
            compute_order_summary(OrderDraft(order_id="o1", items=(LineItem(sku="a", unit_cents=100, quantity=0),)))

    def test_money_formatting(self) -> None:
        self.assertEqual(format_cents_usd(0), "$0.00")
        self.assertEqual(format_cents_usd(9305), "$93.05")
        self.assertEqual(format_cents_usd(-250), "-$2.50")

    def test_idempotent_checkout_prevents_duplicate_charges(self) -> None:
        store = CheckoutSessionStore()
        first = store.submit(
            idempotency_key="idem-key-42",
            order_id="ord-42",
            raw_items=[("seat", 2500, 2)],
            discount_cents=500,
        )
        retry = store.submit(
            idempotency_key="idem-key-42",
            order_id="ord-42",
            raw_items=[("seat", 2500, 2)],
            discount_cents=500,
        )
        self.assertIs(first, retry)
        self.assertIsInstance(first, CheckoutReceipt)
        self.assertEqual(first.payable_display, "$45.00")
        self.assertEqual(first.item_count, 2)

        second = store.submit(
            idempotency_key="idem-key-43",
            order_id="ord-43",
            raw_items=[("seat", 2500, 1)],
        )
        self.assertEqual(second.payable_display, "$25.00")

        with self.assertRaises(ValueError):
            store.submit(idempotency_key="  ", order_id="ord-err", raw_items=[("seat", 100, 1)])

    def test_demo_entrypoint_and_layered_css_ownership(self) -> None:
        demo = run_demo_checkout()
        self.assertEqual(demo.order_id, "ord-100")
        self.assertEqual(demo.payable_display, "$45.00")
        self.assertEqual(demo.item_count, 3)

        tokens_css = (EXEMPLAR_ROOT / "shared" / "styles" / "tokens.css").read_text(encoding="utf-8")
        layout_css = (EXEMPLAR_ROOT / "shared" / "styles" / "layout.css").read_text(encoding="utf-8")
        card_css = (EXEMPLAR_ROOT / "features" / "checkout" / "CheckoutCard.module.css").read_text(encoding="utf-8")

        self.assertIn("--surface-paper:", tokens_css)
        self.assertIn("var(--", layout_css)
        self.assertIn("var(--", card_css)
        self.assertIsNone(re.search(r"#[0-9a-fA-F]{3,6}", layout_css))
        self.assertIsNone(re.search(r"#[0-9a-fA-F]{3,6}", card_css))


if __name__ == "__main__":
    unittest.main()
