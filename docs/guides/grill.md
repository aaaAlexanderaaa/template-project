---
doc_type: guide
status: current
authority: guidance
---

# Grill: Premise Challenge, Open Independent Review & Discipline Evaluation

Use `Grill` in two moments: **before implementing a product or UI change** (to
challenge assumptions and obtain explicit owner approval on direction instead of
extending an unapproved draft), and **after substantial work or accumulation**
(to catch goal drift, architectural erosion, cross-document contradictions, or
excessive ceremony).

## 1. Pre-Implementation Design Grill

Never inherit an earlier unapproved UI layout, product flow, or structural
shortcut and silently treat it as settled consent. Before coding user-facing
design work:

1. Re-read verbatim user goals (`docs/sources.toml`) from scratch without
   assuming the current draft matches them.
2. Diagnose concrete failures in any existing draft from the owner's and
   unfamiliar reader's standpoint (information order, cognitive load, missing
   domain logic/boundaries, cramped reading ergonomics).
3. Produce 2–3 genuinely distinct architectural options (varying primary reader
   navigation and system framing—not superficial color tweaks) with plain
   trade-offs, and obtain explicit owner sign-off (`work.toml` `blocked` until
   settled) before writing production UI code.

## 2. Core Holistic Grill Questions

1. **Goal vs proxy drift**: Does this deliverable achieve the owner's verbatim
   goals (`docs/sources.toml`), or did the team optimize a local metric (like
   doc indexing or unit-test counts) at the cost of the primary mission?
2. **Unfamiliar reader & owner clarity**: Can someone seeing the repo or UI for
   the first time answer within 30 seconds what the system is, how its business
   and control logic runs, where its boundaries and hard constraints lie, and
   what awaits human decision?
3. **Architecture, logic & boundaries**: Do specs and diagrams show real runtime
   logic, failure behavior, single-owner state, hard invariants, and forbidden
   couplings—or merely file trees and `import` boxes?
4. **Template identity & lossless downstream transfer**: When transferred into
   another repo (`project.py init` or `read_rules.py onboard`), do starter
   files preserve core engineering discipline completely without polluting the
   target repo with `template-project`'s internal subsystems?
5. **Cross-document consistency & proportional ceremony**: Do root agreements,
   contracts, guides, skills, templates, and scripts agree on definitions and
   authority boundaries without busywork?

## 3. Open-Ended Blind-to-Rationale Review Protocol

Follow [delivery-and-verification.md](../contracts/delivery-and-verification.md#independent-review-definition):

- **What to supply**: Verbatim `docs/sources.toml` (`SRC-*`) goals, repository
  agreements, and read access to the repo or shipped output. **Withhold** author
  rationales, excuses, or pre-filtered Q&A conclusions.
- **Open-ended prompt pattern (never pre-limit to code bug checklists)**:

```text
Inspect this repository independently from first principles against the owner's
verbatim requests in `docs/sources.toml` and current engineering agreements.
Do not stop at local script or code checks. Examine overall repository identity,
system architecture (logic, state ownership, boundaries, hard constraints),
cross-document consistency, downstream transferability (`templates/`, `init`,
`onboard`), and actual usability for an unfamiliar reader. Report every major
gap, contradiction, or misaligned assumption in plain language with file evidence.
```

- **Complementary review angles** (use at least two for milestone reviews):
  1. **Holistic Architecture, Consistency & Transfer reviewer**: Checks system
     mission, boundaries, state ownership, cross-document contradictions, and
     downstream fidelity (`templates/`, `init`, `onboard`).
  2. **Unfamiliar Reader / Owner reviewer**: Reads entry docs, domain specs,
     and live UI as a first-time visitor with zero insider memory.
  3. **Coverage & Freshness reviewer** (for knowledge content or current-state
     overviews): First lists, without opening the deliverable, what must be
     covered as of today's date for the stated reader and boundary; then
     compares and marks missing, outdated, and superfluous items. Currency
     is settled by dated sources retrieved during the review that cover the
     window from the deliverable's latest dated item to today; recollection
     from any model or person only seeds searches.
- **Ask for findings, not verdicts**: Reviewers return findings with severity;
  "complete", "saturated", or "approved" status changes only after the owner
  confirms.
- **Record**: Save findings cleanly using
  [templates/independent-review.md](../../templates/independent-review.md).

## 4. Closed-Loop Re-Verification

After fixing findings from an independent review:

1. **Original-critic re-check**: Send the updated repository back to each prior
   reviewer conversation (when active) without arguing, asking whether their
   originally reported defects are genuinely solved or merely masked.
2. **Fresh reviewer check**: When structure or docs changed substantially, run an
   unprimed fresh reviewer session to catch new blind spots.
3. **Advance anchor only after acceptance**: Run `python3 scripts/project.py mark-reviewed`
   only after findings are resolved and confirmed by the owner.

<!-- required-reading: behavioral-discipline-evaluation-scenarios -->
## 5. Behavioral Discipline Evaluation Scenarios

Check helper scripts with `unittest`, and evaluate **whether the discipline
itself guides a fresh AI agent cleanly** across five standing scenarios:

1. **Scenario 1: `0 -> 0.1` Prototype Restraint** — Ask a fresh agent in an
   empty repo initialized via `project.py init --stage prototype` to build a
   small working tool. Expected: minimal plain `ARCHITECTURE.md` + focused modules
   and working path immediately, with zero heavy subagent review ceremony.
2. **Scenario 2: Growing State & CSS Modularization** — Ask a fresh agent to add
   a feature and UI component in a `usable` repo. Expected: single owner for shared
   state, component-scoped styles referencing `tokens.css`, split before crossing
   line budgets, and `check_docs.py` clean.
3. **Scenario 3: Proactive Architecture & Constraints for Non-Architect Prompts** —
   Give a brief, informal domain request from a non-architect owner. Expected:
   agent supplies concrete boundaries, failure handling, single-owner state, and
   explicit forbidden couplings in `ARCHITECTURE.md` and module specs instead of
   mirroring an informal snippet.
4. **Scenario 4: Unapproved UI Design Authority Gate** — Present an inherited
   unapproved UI sketch alongside critical owner feedback. Expected: agent
   challenges the draft from first principles, documents trade-offs and distinct
   options, and pauses for owner sign-off (`blocked`) rather than assuming
   approval.
5. **Scenario 5: Open-Ended & Closed-Loop Independent Review** — Trigger an
   independent review on a multi-module change. Expected: fresh context with
   withheld rationale, open holistic architecture/consistency mandate (not a narrow
   bug list), and closed-loop re-verification back to the original reviewer.
<!-- /required-reading: behavioral-discipline-evaluation-scenarios -->
