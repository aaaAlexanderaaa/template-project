---
doc_type: evidence
status: historical
authority: evidence
last_reconciled: 2026-09-14
subject: first-party-adoption-feedback
---

# First-party adoption feedback, distilled

This record supports one claim: since 2026-07 this template's discipline has
been exercised by real first-party projects, and their feedback — positive
and negative — has been reconciled into the contracts they exercised. It
supersedes earlier acceptance-evidence notes that said no real project had
exercised the discipline; those dated notes stay as written, because they
were true when written.

## Source and privacy boundary

The source is the maintainer's private cross-project collaboration archive:
distilled preferences, correction chains, and project retrospectives spanning
2025-11 to 2026-09 across several machines and several agent platforms,
covering dozens of real projects, including a subset that adopted this
template's discipline from 2026-07 onward and kept developing under it.

The archive is private. Project identities, credentials, internal topology,
client details, and personal context are deliberately withheld, and lessons
were adopted only in domain-neutral form. This record is the public pointer;
the underlying material cannot be linked.

## Selection method

Selection ran in two passes. The first pass leaned on recurrence across
projects; review against the archive's own weighting rule — recurrence
measures a problem's stubbornness, while institutionalization is the weight
signal — found it under-weighted rules that were stated once and immediately
became standing law. The second pass therefore re-read the archive's
institutionalized-directive inventory in full and re-ranked by weight.

A lesson then qualified for adoption only when all of these held:

1. it was institutionalized by the maintainer (written into a project's
   standing rules or tooling) or recurred across projects in the source;
2. it generalizes beyond its originating project and stack;
3. it has exactly one owner here — an existing invariant it strengthens, or a
   clear new one.

Dumping a catalog of historical incidents was explicitly rejected, per
[project-adoption § authorship-triage](../contracts/project-adoption.md#external-material-is-triaged-by-authorship-before-adoption)
and the template's existing rejection of pit registers as ceremony.

## What confirmed the existing rules

Positive feedback, summarized without private detail:

- Contract-first delivery with the raw/translated dual track survived the
  hardest frontend battles and became the reconciliation mechanism when
  "this is not what I wanted" occurred.
- The bounded option set — options carrying trade-off context, ROI, and risk
  assumptions — became the stable decision interface, answered in compressed
  form; execution after alignment ran uninterrupted to its blockers.
- Independent review gates and fresh-context evaluation caught real defects
  that same-context review missed, including at least one case where a
  deliverable passed the author's checks and failed a context-free consumer.
- The time/calendar and demonstration-data concerns, originally derived from
  late and expensive repairs, recurred in new projects and were handled at
  declaration time rather than at cutover time.

## What corrected or added rules

Negative feedback and incidents, adopted at their existing owners:

- [development § data-fidelity](../contracts/development-discipline.md#real-content-is-never-deleted-or-fabricated-for-presentation):
  presentation must never delete or fabricate real content; reduction happens
  in the display layer, never the storage layer; research keeps its
  intermediate evidence chain and states its measurement basis.
- [development § bidirectional verification](../contracts/development-discipline.md#verify-promised-and-observed-behavior-in-both-directions):
  a failure is attributed to the user's environment only with evidence; a
  fix is verified where the failure was reported; a fresh-context consumer's
  failure is a defect in the deliverable.
- [development § frontend contract](../contracts/development-discipline.md#frontend-development-contract):
  surfaces carry no meta-discourse and no non-functional controls; state
  catalogs include the environment interruptions real usage produces.
- [development § backend contract](../contracts/development-discipline.md#backend-and-service-development-contract):
  an agent-consumable interface treats its error surface as part of the
  contract; validation defines the valid rather than enumerating the invalid.
- [agent-execution § resource spending](../contracts/agent-execution-discipline.md#billed-rate-limited-and-account-bound-resources-are-spent-deliberately):
  billed, rate-limited, and account-bound work declares its volume; a
  rate-limit response circuit-breaks into a mechanism fix; a retry never
  replays a completed effect — adopted after an incident in which repeated
  non-atomic writes suspended a real account.
- [agent-execution § delegation](../contracts/agent-execution-discipline.md#delegated-work-carries-bounded-context-and-returns-to-an-owner):
  when the owner is unavailable, work is shaped to the authorized operation
  set with pre-named pause points; delegated failure is attributed first to
  the assignment's context and contracts, not the worker.
- [agent-execution § evidence classes](../contracts/agent-execution-discipline.md#evidence-classes-remain-explicit):
  a simulation establishes runnability, not real-world outcome; a
  demonstration with invisible manual correction is evidence about the
  correction.
- [governance § decision-envelope](../contracts/governance-decision-boundary.md#delegated-engineering-work-proceeds-by-default):
  the authorization boundary is bidirectional — over-asking is a violation
  symmetric to unauthorized action.
- [governance § advice-preserves-disagreement](../contracts/governance-decision-boundary.md#advice-preserves-disagreement):
  instant agreement without independent judgment is a failure mode.
- [development § durable-recording](../contracts/development-discipline.md#recurring-verbal-rules-are-proposed-for-durable-recording):
  a recorded rule carries its scope and suspension conditions; a rule stated
  under exceptional pressure is not promoted into a standing rule; a new
  rule's proposal names its home and its rank among neighboring rules; and
  what is recorded is the principle, not the incident.
- [development § fix-the-category](../contracts/development-discipline.md#fix-the-category-not-only-the-symptom):
  investigation tooling enriches the raw failure record but never pre-filters
  it.
- [project-adoption § authorship-triage](../contracts/project-adoption.md#external-material-is-triaged-by-authorship-before-adoption):
  recurrence measures a problem's stubbornness, not a preference's weight;
  institutionalization is the weight signal.
- [README](../../README.md): the harness definition and the supremacy of
  the requested observable outcome are now stated on the public face, after
  review found them recorded only inside agent-facing entrypoints.

## What remains unproven

- Adoption by a repository independent of the maintainer. The open promise
  `promise[independent-adoption-review]` in
  [agent-execution](../contracts/agent-execution-discipline.md) stands.
- An end-to-end recorded use of the engineering-judgment comparison
  procedure; only parts of that judgment have been exercised.
- Measured behavioral effectiveness, as opposed to exercised behavior and
  reconciled feedback.

## Limitations

- The source archive is private and cannot be reproduced or audited by a
  reader of this repository; the claims above are maintained by the template
  maintainer and should be weighed accordingly.
- First-party adoption conflates the rule author and the rule consumer in one
  person; feedback may reflect the maintainer's projects' shape rather than
  adopters generally.
- This is a dated snapshot. Later contracts and their reconciliation logs are
  the current authority where they say more.
