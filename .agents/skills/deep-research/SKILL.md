---
name: deep-research
description: >-
  Run structured, primary-source research for unfamiliar technical domains,
  knowledge overviews, fast-moving fields, or contested industry and social
  topics. Covers framing for a named reader, people-centered source discovery,
  dialectical counter-argument checks, multi-caliber open-domain data analysis
  without fabricated scores, and date-anchored coverage and freshness checks.
---

# Deep Research

Use this skill when a task calls for real investigation rather than quick syntax lookup: mapping an unfamiliar domain, surveying a fast-moving field, building a knowledge overview, or evaluating a contested technical, industry, or social question. It is self-contained and works in any repository.

## 1. Frame the Question, Reader, and Boundary First

Before opening tabs or drafting an outline, fix four facts:

1. **Named reader and job**: Who reads the result, what baseline do they already have, and what decision or mental model do they need afterward?
2. **Scope boundary and as-of date**: State what sits inside the boundary, what stays out, and today's date for any current-state claim.
3. **High-value inquiry questions** (use what fits the material; never force a mechanical template):
   - What scattered public facts or conflicting statistical definitions do readers usually miss or fail to cross-check?
   - What angle, affected group, shifted cost, incentive, or historical parallel sits outside the two loudest camps?
   - What 1–2 reusable mechanisms explain why the pattern happens, and where do those mechanisms stop working?
4. **Separate durable structure from volatile catalogs**: When a topic mixes stable mechanisms with a fast-changing list of products, models, tools, or vendors, plan them as two linked layers and define explicit inclusion and retirement criteria for the volatile list.

## 2. People-Centered Source Discovery & Primary Evidence

- **Go to primary sources first**: Prefer official specifications, source code, release notes, laws, court rulings, official statistical communiqués, peer-reviewed papers, and reproducible experiments over secondary summaries.
- **Separate source curation from collection**: Maintaining a list of high-signal people and institutions (and judging where attention belongs) is separate from raw retrieval volume. Do not add noisy channels without weighing their maintenance cost.
- **Follow strong sources through people**: High-signal insight usually comes from specific practitioners and primary communities. Expand outward from verified anchors—an author's references and links, early recommenders of niche work, book prefaces and acknowledgments, and primary citation chains—rather than repeatedly searching names already in memory.
- **Search to discover, not just to confirm**: Recollection from any model or person only seeds searches; it is never evidence. For fast-moving or current-state topics, run date-anchored discovery queries (`"releases since <date>"`, release trackers, latest annual reports) covering the window from the deliverable's latest dated item through today. Record the queries, publication dates, and retrieval date.

## 3. Dialectical Verification & Multi-Caliber Evidence

- **Read the other side and the response layer**: Never stop at a single persuasive essay or famous authority. Check critical reviews, comment threads, replication failures, issue trackers, and later developments to see what held up in practice.
- **Check contested questions sharply**: On topics with strong disagreement, identify who gains, who pays, who is absent from the debate, and which conflicts are factual versus value trade-offs. Stepping past the two loudest camps never means false balance when evidence clearly refutes one side.
- **Keep exact engineering facts separate from multi-definition open data**:
  - **Exact facts** (code metrics, regulatory limits, UI counts, reproducible benchmarks): verify strictly against authoritative inputs and keep numbers internally consistent.
  - **Multi-definition open data** (industry size, historical series, social or policy indicators): agencies naturally differ in definitions, samples, and cutoffs. Treat conflicting figures as analytical evidence rather than a reason to stall or fake precision—lay sources and premises side by side, discard clear errors, keep honest ambiguity where open records stop, and never invent hand-tuned composite scores (such as arbitrary 0–100 weights) without empirical backing.
- **Borrow strong existing explainers cleanly**: Link to authoritative background references instead of rewriting introductory textbook material from scratch, keeping effort on synthesis, new evidence, and real trade-offs.

## 4. Coverage, Freshness & Synthesis

- **Date time-sensitive facts**: Attach an as-of date to fast-changing claims. If retrieval is unavailable for a current-state claim, mark it `currency unverified as of <date>` rather than passing it silently.
- **Expectation-first coverage check** (whenever claiming breadth or completeness):
  1. Before reviewing the draft, list from retrieved sources what a capable reader expects covered within the stated boundary as of today.
  2. Compare the draft against that list and account for every major item as `included`, `merged`, `known gap`, or `excluded (with reason)`.
- **Deliver plain trade-offs**: State directly what each mechanism or option is, how it works, what evidence supports it, where it stops working, and what open questions remain.

## 5. Capability-Preserving Fallbacks

When an external search tool, bridge, or source fails:

- For transient routing or tooling errors, switch to an alternate search or local source with comparable evidence quality.
- For hard permission boundaries, paywalls, or anti-bot gates, never attempt to bypass them—report the exact block and mark the affected area's evidence boundary plainly while completing unaffected research.

## Quick Self-Check

1. Are major claims backed by primary sources with publication and retrieval dates (rather than model memory)?
2. Did discovery reach beyond already-known names via verified authors, citations, or date-anchored searches?
3. Did you check counter-arguments and later developments, and distinguish factual disagreements from value conflicts?
4. Are exact facts verified cleanly while multi-definition open-domain figures appear side by side with premises and zero fabricated composite scores?
5. Does the final output answer the named reader's real question clearly, separating stable mechanisms from volatile instances?
