---
id: exemplar.shared
domain: reference-app
kind: module-spec
summary: "Named shared currency formatter and design-token / layout CSS foundation."
promise: "Shared formatting and CSS custom properties (`tokens.css`, `layout.css`) stay reusable and free of feature-specific selectors."
owns:
  - "examples/reference-app/shared/**"
depends_on: []
sources:
  - SRC-010
  - SRC-011
  - SRC-022
---

# Reference App — Shared Formatters & Design Tokens

## 1. Purpose, Public Interface & Non-Goals

- **Public interface**: `shared/money.py` formatting helpers plus base CSS sheets `shared/styles/tokens.css` and `shared/styles/layout.css`.
- **Out of scope**: Order math (`exemplar.domain`), feature-specific DOM selectors, or generic `utils/` catch-all files.

## 2. Asset & Formatting Flow

```mermaid
flowchart LR
  Tokens["shared/styles/tokens.css (Colors, Spacing, Type)"] --> Layout["shared/styles/layout.css (Page Shell)"]
  Tokens --> FeatureCSS["features/checkout/CheckoutCard.module.css (Component Styles Only)"]
  Money["shared/money.py"] --> Display["Consistent Cents-to-Currency Text"]
```

## 3. State Ownership, Constraints & Forbidden Couplings

- **Layered CSS Invariant**: Color hex values live only in `shared/styles/tokens.css`; component styles under `features/` reference CSS custom properties (`var(--...)`) rather than duplicating palette literals.
- **Forbidden couplings**: `depends_on: []` — never imports `domain/`, `features/`, or `app/`, and never uses `utils/`/`helpers/` directory names.
- **Verification**: Checked by `tests/test_reference_exemplar.py` and CSS size/ownership checks in `check_docs.py`.
