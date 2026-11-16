# Role: Public entrypoint for shared cross-feature value formatters.
# Out of scope: Feature-specific business rules or catch-all miscellaneous helpers.
# Anchors: spec=exemplar.shared, SRC-011

from .money import format_cents_usd

__all__ = ["format_cents_usd"]
