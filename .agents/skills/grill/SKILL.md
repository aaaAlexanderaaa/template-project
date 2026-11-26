---
name: grill
description: Challenge project direction, architecture, boundaries, UX, or Goodhart drift from first principles before building unapproved designs or after change accumulation, and run open closed-loop independent reviews.
---

# Grill Skill

1. Run `python3 scripts/project.py status` and `python3 scripts/check_docs.py`
   to collect objective Git, import-boundary, file-size, and blocker facts.
2. Read `docs/sources.toml` (`SRC-*` verbatim quotes),
   [delivery-and-verification.md](../../../docs/contracts/delivery-and-verification.md#independent-review-definition),
   and [grill.md](../../../docs/guides/grill.md).
3. Challenge the design or repository against first principles:
   - Before coding unapproved UX/product flows, grill the draft openly, present
     genuinely distinct architectural options, and pause (`blocked`) for owner
     approval instead of assuming consent.
   - In holistic reviews, inspect judgments with open expectation violations
     first and consider removing or simplifying rules before proposing additions.
   - Audit whether the repo centers on real operational logic, state ownership,
     hard constraints, forbidden couplings, downstream transfer fidelity, and
     plain unfamiliar-reader comprehension.
4. When running Independent Review, spawn fresh subagent context(s) **withholding
   author rationales**, use an **open-ended holistic mandate** (never a narrow
   code checklist), cover holistic architecture/consistency/transfer plus
   unfamiliar-reader clarity, and **close the loop** by re-verifying fixes with
   both original reviewers and a fresh pass when structure changed. For
   coverage or currency questions, have the reviewer **list expectations before
   reading the deliverable**, and settle currency with **dated sources retrieved
   during the review** that cover the window from the deliverable's latest dated
   item to today; no model's or person's memory counts as evidence.
   Reviewers report findings, never pass verdicts; milestone status changes only
   after owner confirmation.
5. Report evidence-backed findings plainly using
   [templates/independent-review.md](../../../templates/independent-review.md)
   when recording durable reviews, and run `python3 scripts/project.py mark-reviewed`
   only after owner acceptance.
