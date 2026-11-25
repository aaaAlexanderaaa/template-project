---
id: ADR-006
kind: decision
status: current
title: "Add an information-organization contract, layer frontend rules from principles to references, and extend independent review for coverage and currency"
sources:
  - SRC-022
  - SRC-024
  - SRC-025
affects:
  - discipline.entry-and-contracts
  - discipline.guides-and-skills
  - discipline.templates
  - ui.perspective-web
  - exemplar.shared
supersedes: []
---

# ADR-006: Information Organization, Four-Layer Frontend Rules & Coverage-Aware Review

- **Context & problem**:
  1. The template said where each fact is stored (`docs/README.md`) but gave no
     practice for how to organize information for readers: grouping, order,
     layering, naming, form, and, for knowledge content, scope and freshness
     (`SRC-024`). An adopting knowledge project showed the cost: content scoped
     to what the author already knew, current-state facts that stopped months
     before their stated as-of date, and coverage claims without evidence.
  2. The frontend contract was essentially the owner's preference specification
     (`SRC-022`): exact tokens, pixel values, and reference products. Agents
     reproduced the look but skipped the principles and best practices behind
     it (`SRC-024`). One preference token, `--ink-tertiary: #868B96`, measured
     3.14:1 on the canvas, below the WCAG AA 4.5:1 text minimum, and nothing in
     the contract caught it.
  3. Independent review was defined around context isolation and open mandates,
     but a reviewer asked a yes/no gate question cannot find missing or outdated
     content: it only audits what the deliverable already contains, and judging
     currency from memory fails for any reviewer, because every model and every
     person has a knowledge horizon (switching reviewers only picks a different
     wrong answer).
- **Chosen approach**:
  1. New contract [information-organization.md](../contracts/information-organization.md)
     covering documents, interface information architecture, and knowledge
     content (owner choice in `SRC-025`: one contract for all three kinds of content): reader task first, answer first,
     organizing schemes per level, layering with context, form chosen from the
     question, document types by reader need (Diátaxis), and coverage, scope,
     and freshness rules for knowledge content.
  2. [frontend-and-visual-discipline.md](../contracts/frontend-and-visual-discipline.md)
     restructured into four ordered layers: principles, a mandatory measurable
     best-practice baseline (WCAG 2.2 AA, typography, Core Web Vitals, states,
     chart perception, honest provenance), owner preferences, and reference
     practices. The calm-platter specification stays intact as the default
     preference layer, shipped to adopting projects and replaceable by their
     owners (owner choice in `SRC-025`: ship as a replaceable default). Conflicts resolve toward the higher layer; the
     tertiary ink became `#6B7079` (4.57:1) in the contract, the web overview,
     and the reference app (owner choice in `SRC-025`: the best practice wins over the preference).
  3. [delivery-and-verification.md](../contracts/delivery-and-verification.md#independent-review-definition)
     adds: verified isolation, no yes/no gate as the opening question,
     expectation-first review for coverage and currency, currency settled by
     dated sources retrieved at review time over an explicit date window (no
     reviewer's memory counts as evidence), findings instead of verdicts with
     owner-confirmed milestone status, and varied review angles. The grill
     guide, grill skill, and review templates follow.
  4. Downstream transfer: `templates/AGENTS*.md` trigger rows, both
     `surface-spec` templates (principles, measured baseline, preferences as
     separate sections), onboarding required reading, and the `frontend` and
     new `information` rule-reading concerns.
- **Trade-offs & rejected alternatives**:
  - Keeping preferences as universal rules and adding principles on top was
    rejected: adopting projects would still copy one owner's palette as if it
    were a standard, and nothing would explain which parts may change.
  - Moving the calm-platter preferences out of the shipped template was
    rejected: they are a good, tested default and the owner wants them carried
    forward.
  - Putting information organization inside the frontend contract was rejected:
    the same rules govern documents and knowledge content that have no UI.
