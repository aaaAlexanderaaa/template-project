---
doc_type: guide
status: current
authority: guidance
last_reconciled: 2026-09-14
---

# Engineering reading list

## Purpose

This guide records the external engineering-practice sources this template
has mined, what each is for, and what was deliberately rejected. It exists
so a future contributor or agent can re-mine originals instead of trusting
someone's summary — including this one.

Nothing here is normative. A lesson enters the repository only through the
normal contract-first gate; [adoption § authorship-triage](../contracts/project-adoption.md#external-material-is-triaged-by-authorship-before-adoption) owns the
authorship triage, and the engineering-judgment contract's
[rule-format invariant](../contracts/engineering-judgment-discipline.md#every-discipline-entry-carries-its-own-boundary)
owns the writing format for anything adopted.

## How to mine

1. Read the original, not a summary. If a local raw archive exists under
   `archive/external/`, use it; otherwise fetch the URL below. The archive
   is gitignored local material, so its absence means re-fetch, not loss.
2. Triage authorship before trusting: dated human decisions and named
   authors are primary; curated compilations are leads whose items must
   trace to their own origins; unattributed or machine-polished narrative
   is unverified.
3. Extract candidates as checkable judgment with provenance and an
   over-design boundary — not as summaries. Record what you rejected and
   why, so it is not re-proposed.
4. Migrate the method, not the numbers: thresholds calibrated to another
   organization's scale stay behind.

## Sources

| Source | Authorship ([adoption § authorship-triage](../contracts/project-adoption.md#external-material-is-triaged-by-authorship-before-adoption)) | Mine it for |
|---|---|---|
| [A Philosophy of Software Design, 2e (Chinese translation)](https://yingang.github.io/aposd2e-zh/) | Primary: named author (Ousterhout) | Complexity symptoms (change amplification, cognitive load, unknown unknowns), contact-frequency weighting, red-flag list, design-twice, "taking it too far" as a rule section |
| [Google SRE book](https://sre.google/sre-book/table-of-contents/) and [Workbook](https://sre.google/workbook/table-of-contents/) | Primary: named organization | Error budgets as quantified risk acceptance, actionable-alert tests, blameless postmortems feeding defect categories, toil definition, per-system-type SLI selection |
| [TIGER_STYLE](https://github.com/tigerbeetle/tigerbeetle/blob/main/docs/TIGER_STYLE.md) | Primary: named engineering organization | How to write scenario rules as mechanism + checkable instruction + reason + grounded constraint; bounds on everything and chosen exhaustion behavior; back-of-envelope decision sketches |
| [hacker-laws](https://github.com/dwmkerr/hacker-laws) | Second-hand compilation; cite each law's own origin | Tesler's law (simplification displaces complexity onto someone — often the user), Fitts/Hick (interaction cost is measurable), Goodhart (a metric turned target distorts), Hyrum (observable behavior is the contract), Postel-vs-strict as a worked contradiction pair, Chesterton's fence, second-system effect, Amdahl for comparing options |
| [The Grug Brained Developer](https://grugbrain.dev/) | Practitioner essay, pseudonymous | Anti-over-design judgment: complexity enters through well-meaning change, refactor when a narrow-interface cut point has emerged, "I cannot explain this" is a legitimate review signal |
| [97 Things Every Software Architect Should Know (summary)](https://medium.com/@iankaga/97-things-every-software-architect-should-know-672f2accf109) | Second-hand summary of a multi-author book | Standpoint discipline (business vs engineering), architecture decisions as investments with ROI, use-before-reuse, data-model change-cost asymmetry |
| [Agent-rules gist](https://gist.github.com/sanchez314c/a767997b030d2904c0d0f08fabae2d42) | Unverified lead | Peer comparison for agent discipline; restart-vs-patch judgment and rule retirement triggers were the only candidates that survived triage |

## Deliberately rejected

These were considered on 2026-08-28 and rejected; do not re-propose without
new evidence:

- numeric targets from any source (10–20% design-investment ratios, 50% toil
  caps, 80% coverage gates, function-length limits) — [development § decisions-not-volume](../contracts/development-discipline.md#govern-document-decisions-not-document-volume) rejects numeric
  proxies for judgment, and the numbers are calibrated to other scales;
- zero-dependency and static-allocation policies — infrastructure-specific
  answers; the template adopts cost accounting and named bounds instead;
- on-call rotation design, multi-window burn-rate alerting, and other
  Google-scale operating rituals — the [development § activate-concerns](../contracts/development-discipline.md#activate-concerns-instead-of-expanding-ceremony) activation model already keeps
  untriggered concerns free of ceremony;
- blanket approval gates ("confirm before coding beyond N steps") — [governance § decision-envelope](../contracts/governance-decision-boundary.md#delegated-engineering-work-proceeds-by-default)
  deliberately removed them;
- aphorisms without a checkable instruction (most of the 97-things list,
  most of hacker-laws) — they stay here as reading, not rules.

## Known gap

User-experience evaluation has the thinnest base in this set: Tesler,
Fitts/Hick, and Goodhart give foundations, and the frontend contract's
perceptual review gives a procedure, but no mined source provides a full
evaluation method. First-party projects activated that need after 2026-07;
the adopted partial answer is the fresh-context consumer in
[development § bidirectional-verification](../contracts/development-discipline.md#verify-promised-and-observed-behavior-in-both-directions) —
acceptance by an independent consumer with none of the author's assumptions.
A dedicated source (Google's HEART framework or Nielsen's usability
engineering) remains the candidate for a future mining pass.
