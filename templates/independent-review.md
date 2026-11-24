---
id: review.record
kind: independent-review
status: draft
reviewer_role: "{{Open-Ended Holistic / Unfamiliar Reader}}"
inputs_supplied:
  - "docs/sources.toml (verbatim owner goals)"
  - "Repository files and live outputs (author rationale withheld until first judgment)"
---

# Independent Review Record

## 1. Review Scope & Independence Declaration

- **Target reviewed**: {{Deliverable, commit range, or repo state}}
- **Fresh context confirmation**: Fresh session/subagent that did not author the implementation; author rationales withheld prior to first judgment.
- **Mandate supplied**: Open-ended first-principles evaluation covering goal alignment, architecture/boundaries/constraints/logic, cross-document consistency, downstream transferability, and unfamiliar-reader comprehension (no yes/no gate question).
- **Isolation check**: {{How context isolation was verified, e.g. no build-session instructions injected}}
- **Currency evidence**: {{Retrieved dated sources, queries used, retrieval date, and the covered window (deliverable's latest dated item -> today); memory from any model or person is not evidence}}

## 2. Expectation List (coverage or currency reviews only)

Before opening the deliverable, list what must be covered as of {{YYYY-MM-DD}} for the stated reader and boundary, built from sources retrieved during the review (recalled items only seed searches). Then mark each item: present / missing / outdated.

## 3. Open-Ended First Judgment

State the reviewer's unprompted initial impression directly before examining any author explanation.

## 4. Architecture, Boundary, Consistency & Usability Findings

| Finding | Category (Goal / Architecture / Consistency / Transfer / Clarity) | Concrete file or runtime evidence | Impact if unfixed |
|---|---|---|---|
| {{Plain finding summary}} | {{Category}} | `{{path:line or command output}}` | {{Why it matters}} |

## 5. Owner Decisions & Scope Boundaries

List any product, UX, or priority question that requires explicit human owner decision rather than agent guesswork.

## 6. Closed-Loop Re-Verification

- **Fixes applied**: {{Commit or file changes resolving each finding}}
- **Original reviewer re-check**: {{Confirmed resolved / remaining gaps in original reviewer context}}
- **Fresh blind check (when structural)**: {{Outcome of unprimed follow-up check}}
- **Owner confirmation**: {{Owner accepted on <date> / still open — reviewers report findings only; status changes after owner sign-off and `mark-reviewed`}}
