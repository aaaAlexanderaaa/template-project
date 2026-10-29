---
doc_type: contract
status: current
authority: normative
contract_role: governance
implementation: implemented
verification_status: partial
last_reconciled: 2026-10-28
supersedes: []
---

<!-- required-reading: analysis -->
# Data analysis discipline

- required-reading: [Execution profiles](agent-execution-discipline.md#vocabulary-and-risk-profiles)

## Purpose

This contract owns the questioning and acceptance discipline for work that
turns a dataset into analytical claims: exploration, metrics, rankings,
mining, and the surfaces that present their results.

The transferable product is a way of interrogating an analysis, not a
catalog of one project's charts. The checklist below produces questions
whose answers change what gets built; the invariants are the acceptance
bar for whatever gets built.

- from: source[1]

## How to read this

1. Take the question checklist. It is ordered by stage; skip the stages the
   current task does not reach. The questions are the method.
2. When a change is activated as Analytical claims under
   [development § activate-concerns](development-discipline.md#activate-concerns-instead-of-expanding-ceremony),
   the invariants here own its acceptance.
3. Source anchors explain why the method exists. They are not adoption work.

## Scope

### In scope

- briefs, exploration, metrics, algorithms, and mining over a dataset;
- surfaces whose primary job is presenting analytical claims;
- evaluation of analyses produced by humans or by agents.

### Out of scope

- storage, pipelines, and non-analytical product surfaces;
- the adopting project's choice of dataset, tooling, and chart library.

## Applicability and output form

Select requirements from the promised reader decision and output form. Shared
obligations are accountable claims, adequate source coverage, stated method and
assumptions, legible evidence, and verification proportional to the consequence
of error. The requested form remains part of the outcome.

| Deliverable | Appropriate application |
|---|---|
| Bounded factual lookup | Check the relevant records and calculation; give the answer, basis and material uncertainty. Follow the ordinary task route. |
| One-off explanation, report or static figure | Retain input identity, method and parameters sufficient to check the result. Link claims or marks to record identifiers, source tables or an appendix in the delivered form. |
| Reusable metric or analytical tool | Supply the re-runnable function, declared parameters and current output. Expose the controls the product promises and verify repeated use. |
| Interactive analytical surface | In addition, verify selectable marks, control/computation correspondence and continuity across views that the surface provides. |

For example, a requested PNG from a fixed CSV can deliver source identity,
denominators, the calculation and a record/table reference. Clickable marks and
parameter widgets belong to an interactive product when that product is part
of the request. Retain the same traceability standard through a suitable form.

Material or high-risk analytical delivery includes independent evaluation of
claim support and presentation, with first judgments preserved separately.
A routine factual lookup uses focused source/calculation verification unless
the brief or another activated owner requires independent review. Apply the
[execution profiles](agent-execution-discipline.md#vocabulary-and-risk-profiles)
and the actual decision impact; a small output can still have serious effects.

## The question checklist

### Framing the brief

- What should the reader understand or decide after seeing this that they
  could not before? An analysis with no reader-side change is decoration.
- Has the brief collapsed into fixed benchmark targets or a fixed chart
  list? Restate it as open questions before accepting any target.
- What are the axes of the domain — the entities, what connects them, and
  time? Name the whole space before choosing what to show, so that an
  omission is a decision rather than an accident.
- What will the analyst show unprompted? A brief that has to ask "what can
  you do?" has not been accepted yet.

### Coverage audit

- What data was fetched, what was available but not fetched, and why?
  Coverage is audited before conclusions, not assumed from them.
- For every claim the analysis intends to make: which records support it,
  and could a reader reach them?

### Exploration

- State each question together with its plausible opposing answers, and
  check that the records can distinguish those answers. A question whose
  answers cannot be told apart from the data is not computable yet.
- Is the granularity a parameter? If the underlying data exists, a fixed
  granularity hides a question the reader was never allowed to ask.
- Ask "what metric survives re-running?" rather than "what did you find?".
  A finding describes this dataset; a metric describes the next one too.
- The counterfactual probe: if this entity left the dataset tomorrow, what
  would change? If nothing changes, the metric was describing an anecdote.
- The overfitting probe: what here is the data speaking, and what is the
  structure of the method speaking?

### Metrics and algorithms

- Where did every constant come from? Who decided it, and what is lost if
  it moves up or down? A threshold with no origin is an assumption wearing
  a result's clothes.
- Why this algorithm, and why not the named alternatives? "The algorithm
  disappeared" into a library default is a finding, not an answer.
- Can the method run again over fresh data and produce a conclusion without
  the analyst in the room? If not, the deliverable is a narrative, not a
  tool.
- Where did the method come from? If the requester supplied it, the
  analyst's own contribution went unexamined. Independent methods, compared,
  are worth more than obedience.

### Presentation review

- Click any mark: does it lead to the records it aggregates? Counts of
  abstract states that open unrelated lists fail this test even when the
  arithmetic is correct.
- Does the surface present mined views, or hand the reader a bag of
  filters? Filter-first assumes the reader already knows which dimension
  combinations carry meaning; most combinations carry none.
- Can the chart be read without mental conversion? Magnitudes, ratios, and
  bases belong on the chart; the reader must not reconstruct them.
- Rehearse the misreading: state the wrong conclusion this display invites,
  out loud, and check whether the display defends itself against it.
- Does the text give a conclusion first, so the reader reads the chart with
  it? A wall of findings without a verdict displaces the analysis onto the
  reader.

### Acceptance

- Which hypotheses were written down before the data answered? Which did
  the data confirm only in part? A hypothesis that cannot lose cannot win.
- Were the claims and the presentation evaluated independently — by
  evaluators without access to each other's context — and were the findings
  classified, translated into fix-or-defer decisions, and converged to the
  few questions that actually remained?

## Normative invariants

### Reusable analyses expose re-runnable functions

A reusable analytical deliverable supplies an algorithm with declared
parameters and its current output. Parameters that shape interpretation are
exposed through its promised interface. A one-off finding retains its input,
calculation or reasoning method and assumptions so another reader can check
that result; a new tool is required when the requested outcome includes reuse.

### Every constant has a stated origin or is an exposed parameter

Every threshold, window, and cutoff either names its origin — who chose it
and what trade-off it encodes — or is exposed for the reader to vary. A
constant with neither is an unexamined assumption baked into the display.

### Measures support fallible judgment and remain open to correction

An operational or quality measure names the decision it informs, the observed
population or sample, artifact and method versions, raw cases, and known limits.
Use repeatable observations to expose missed defects, recurrence, uneven
coverage, unnecessary waiting, or a completion claim contradicted by results.
Several measures can illuminate different parts of a decision without being
collapsed into a single progress score. Choose them for the current question;
this rule does not require a dashboard for every task.

Calibrate detectors against known failures, valuable acceptable cases, and
unfamiliar material. These respectively test detection, excessive rejection,
and blind spots; a fixed regression set serves only the first two. Inspect
false positives and missed cases against the actual quality purpose. Record
coverage and method changes before comparing periods. Deterministic violations
can enforce their contracted boundary; a semantic proxy usually directs
inspection and cannot silently become a ban on useful work.

A zero reading can mean improvement, an unrun or broken check, changed inputs,
or a detector that no longer sees the problem. Distinguish these using execution
evidence and raw cases before declaring success or retiring the detector.
Keep open qualitative review and external evidence capable of challenging the
measurement itself. Correct an instrument that rewards avoidance or hides
useful variation; do not remove observability merely to improve its score.

- from: source[3]

### Statistics precede semantics

Where counts and distributions can answer the question, do not answer it
with semantic inference over sparse material. Semantic reading over
incomplete information manufactures confident error; complete records,
displayed plainly, carry the claim. Semantics may annotate a result; it may
not substitute for one.

### Claims and records remain accountable in both directions

Every claim names the records that support it, and every material pattern
in the records is either addressed or consciously excluded with the
exclusion stated. Do not shrink the data or the claims to make them agree.

### Superseded algorithms remain available as comparisons

When a metric's algorithm changes, retain its prior version and the evidence
needed to compare the resulting claims. A comparative analytical tool keeps
the previous algorithm selectable beside the new one. A static report can
provide a versioned method and side-by-side results. Preserve the ability to
distinguish a data change from a method change through the promised form.

### Every displayed mark resolves to its underlying records

Every point, band, cell or flow in an interactive analytical surface opens
the records it aggregates. Static figures and exports provide stable record
or aggregate-table references through captions, source tables or an appendix.
The reader can trace a displayed claim to the supporting records in either
form, subject to the source's actual access and privacy boundary.

### Reading requires no mental conversion

The display precomputes whatever the claim needs — ratios, magnitudes,
bases, comparisons. If the reader must do arithmetic to learn what the
chart is saying, the chart has delegated its own work.

### Sample size is visible wherever a proportion is shown

A proportion without its base invites confident misreading. The count
behind every rate is drawn on the chart itself, not available on request.

### Small populations survive the chosen encoding

Scale and layout must keep rare-but-important cases legible. An encoding
that flattens a minority into a thin line has deleted exactly the
population that often carries the question.

### The analysis owes the reader a point of view

Presenting mined views is the deliverable; a grid of raw filters is not.
Filter-first design assumes the reader already knows which dimension
combinations matter and displaces the analysis back onto the person it was
meant to serve.

### Control scope equals computation scope

The scope the reader controls is the scope the computation runs over. A
control that narrows the display while the numbers still describe the whole
breaks the correspondence between what is seen and what is meant.

### Depth encodes only what flat layout cannot separate

A third dimension — or any added encoding — is justified only by a
distinction the simpler form cannot show. Depth that restyles separable
data costs reading effort and adds no information.

### The same records stay recognizable across views

When one dataset is shown through several arrangements, the reader must be
able to perceive that the views share records. Transitions that rearrange
without continuity sever that recognition and turn one dataset into many
unrelated pictures.

## Acceptance evidence

- The input identity, coverage, method and assumptions needed to check the
  delivered claim or repeat its promised operation.
- The parameter list: every constant in the deliverable, with its origin or
  its exposed control.
- Traceability for every mark type: a click-through pass for interactive
  surfaces, or checked record/table references for static delivery.
- The misreading rehearsal: the invited wrong conclusion, and the display's
  defense against it.
- A comparison of outputs when an algorithm changed, through the delivered
  form and its retained method versions.
- When independent evaluation is required above: its first findings,
  classification, fix/defer decisions and remaining material questions.

<!-- /required-reading: analysis -->

## Source anchors

### source[1] — 2026-10-04

The maintainer ran an eight-day analysis project over a writing platform's
public records (about 56,000 records, 2026-09-26 to 2026-10-03), working
through brief, coverage audit, five research questions, metric mining,
several rejected presentation forms, and a final narrative surface. The
session exports are unpublished. The reusable result is the questioning
sequence and the acceptance invariants above; the project's own charts are
not the product being transferred.

### source[2] — 2026-10-04

The maintainer asked for the project's experience to be distilled into this
contract and confirmed its shape: question checklist first, invariants
second, fully generic wording. Each adopter still supplies its own dataset,
questions, and surfaces.

### source[3] — 2026-10-10

The maintainer requested that metrics make agent judgment more tolerant of
error and easier to correct, drawing on longitudinal autonomous writing work.
Its feedback distinguished useful measurement from fixed proxies, shared
blind spots, and misleading zero readings. The accepted implementation adds
decision-linked calibration, including valuable cases a detector must preserve.
See [the adoption evidence](../evidence/2026-10-10-experience-and-adaptive-operation.md).

## Reconciliation log

- **2026-10-10 — instruments participate in learning:** added positive uses
  of measurement, calibration against failures and acceptable variation, and
  investigation of zeros and changed methods. This does not make semantic
  quality mechanically decidable or mandate an analytical interface for
  ordinary execution.
  - from: source[3]

- **2026-10-04 — contract created:** distilled from the maintainer's data
  analysis retrospective. The checklist and invariants were exercised in one
  real project; independent effectiveness in an adopting project remains
  open.
  - from: source[1], source[2]
