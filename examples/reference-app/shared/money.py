# Role: Deterministic integer-cent to display-currency formatting.
# Out of scope: Pricing rules, discounts, or tax calculation (owned by domain).
# Anchors: spec=exemplar.shared, SRC-011

from __future__ import annotations


def format_cents_usd(cents: int) -> str:
    sign = "-" if cents < 0 else ""
    whole, rem = divmod(abs(cents), 100)
    return f"{sign}${whole:,}.{rem:02d}"
