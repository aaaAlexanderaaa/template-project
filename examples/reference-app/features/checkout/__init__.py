# Role: Public entrypoint for the checkout feature module.
# Out of scope: Internal idempotency table representation in service.py.
# Anchors: spec=exemplar.checkout, SRC-001, SRC-002

from .service import CheckoutReceipt, CheckoutSessionStore

__all__ = ["CheckoutReceipt", "CheckoutSessionStore"]
