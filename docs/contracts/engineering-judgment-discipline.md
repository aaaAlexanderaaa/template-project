---
doc_type: contract
status: target
authority: normative
contract_role: governance
implementation: not_started
verification_status: pending
last_reconciled: 2026-09-14
review_due: 2026-11-26
supersedes: []
---

# Engineering judgment discipline

## Purpose

The repository's other contracts govern process truthfulness: authority,
evidence, verification, and lifecycle. This contract governs engineering
judgment itself: how complexity is named and when it triggers intervention,
how solutions are compared inside the engineering decision envelope, how
build-vs-reuse is decided, and from whose standpoint a judgment is made.

It exists because a change can follow every process rule and still be the
wrong change: correctly implemented, correctly verified, and more complex,
redundant, or unusable than the alternative nobody looked for.

## Scope

In scope:

- naming complexity by symptom and weighting it by contact frequency;
- checkable triggers for refactoring and rewriting;
- the comparison procedure for non-trivial choices inside [governance § decision-envelope](governance-decision-boundary.md#delegated-engineering-work-proceeds-by-default)'s
  engineering decision envelope;
- build-vs-reuse accounting;
- standpoint declaration in material analysis;
- the writing format for scenario-specific disciplines.

Out of scope:

- product direction, priority, and risk acceptance ([governance § human-direction](governance-decision-boundary.md#humans-own-direction-and-priority));
- the reporting fields for risks and recommendations ([governance § advice-preserves-disagreement](governance-decision-boundary.md#advice-preserves-disagreement) owns
  those; this contract's standpoint vocabulary informs them);
- universal numeric targets, coverage gates, or file-size limits
  ([development § decisions-not-volume](development-discipline.md#govern-document-decisions-not-document-volume) rejects them);
- a catalog of scenario rules. Specific problems get specific analysis, but
  the scenario has usually been trodden before: the rule-format invariant
  below defines how such knowledge is written down, not what it must say.

## Source anchors

### source[1] — 2026-08-28

> “Many of our disciplines are collaboration disciplines, and many are
> AI-facing or documentation disciplines, but we have neglected the
> disciplines of engineering practice itself: how to define and evaluate
> user experience — a good engineering implementation is not necessarily
> good user experience; how to manage project complexity and what should
> trigger refactoring; how to avoid reinventing the wheel; how to decide
> between solutions. Reference settled industry practice such as the Google
> SRE books while avoiding over-design, and mind the standpoint: the user,
> the product manager, and the architect each cut into the same problem
> differently.”

### source[2] — 2026-08-28

> “Specific problems need specific analysis, but the scenarios have been
> trodden by many before. Keep enough text to remind an agent to consider
> what it has not considered — to avoid drilling into a dead end,
> over-optimizing, or over-designing.”

### source[3] — 2026-08-28

> “How many symbol systems does the project have now? I see different
> encodings like J, D, and G, and it feels off.”

The owner approved the citation redesign in [documentation-harness § invariant-citations](documentation-harness.md#invariant-citations-resolve-to-headings)
and named this contract — one day old, target status, fourteen references —
as the pilot cutover.

## Source materials

The invariants below were mined from an archived reading set, triaged by
authorship per [adoption § authorship-triage](project-adoption.md#external-material-is-triaged-by-authorship-before-adoption): *A Philosophy of Software Design* (Ousterhout;
named human author), the Google SRE book and workbook (named organization),
TigerBeetle's TIGER_STYLE (named engineering organization), the Grug Brained
Developer essay (pseudonymous practitioner essay), *97 Things Every Software
Architect Should Know* (multi-author book, consumed through a second-hand
summary), hacker-laws (curated compilation; each law traces to its own
origin), and an unattributed agent-rules gist (treated as unverified leads).
`docs/guides/engineering-reading.md` holds the full list, what each source
is for, and what was deliberately rejected. The raw archive is local under
`archive/external/` and is not project authority.

## Normative invariants

### Complexity is named by symptom before it is managed

A claim that code is "too complex" names the symptom: change amplification
(one logical change forces edits in many places), cognitive load (how much
must be learned before a safe change), or unknown unknowns (it is not clear
what must change, or that a problem exists). The claim also names whether
the source is dependency or obscurity, and weights the cost by contact
frequency: complexity in code nobody touches is nearly harmless, while
complexity on a hot path compounds.

*Taking it too far:* the symptoms are a vocabulary for judgment, not a
counting metric. One-off scripts and disposable [development § contract-first](development-discipline.md#contract-before-material-delivery-evidence-before-certainty) experiments are exempt.
A low-traffic region that is a failure source is still a defect, not a
complexity bargain.

- from: source[1]

### Refactoring and rewriting have checkable triggers

Intervention is triggered by evidence, not by age, size, or taste:

1. a design red flag appears in code being changed anyway — shallow module,
   information leakage, pass-through method, repeated mechanism, a name that
   resists naming — and the change pauses to compare one alternative;
2. a narrow-interface cut point has visibly emerged in code that has
   stabilized, so complexity can be hidden behind it;
3. the reason an existing structure exists can be stated, and that reason is
   gone — or cannot be stated, in which case the structure is investigated
   before it is touched;
4. a rewrite is proposed: it lists the real problems the current version
   demonstrably has, and designs only for those; capabilities beyond the
   list are argued individually;
5. the same manual, repetitive, automatable operation is being done a third
   time.

Every change leaves the design no worse than it was. Complexity is added
incrementally by well-meaning changes, so the defense runs per change: name
what new concept, abstraction, or moving part this change introduces and
what it buys.

*Taking it too far:* triggers are pause-and-compare signals, not mandates
and not CI counters. [development § fix-the-category](development-discipline.md#fix-the-category-not-only-the-symptom) still bounds expansion: a trigger is not permission
for unbounded cleanup, and scope discipline still applies.

- from: source[1], source[2]

### Non-trivial choices inside the envelope use a comparison procedure

[governance § decision-envelope](governance-decision-boundary.md#delegated-engineering-work-proceeds-by-default) lets reversible engineering choices proceed without serial
approval. When such a choice is non-trivial — several defensible shapes,
different long-term costs — the implementer:

1. sketches two genuinely different candidates, even if one looks bad, and
   lists each one's interface simplicity, generality, and implementation
   cost; a class-level decision is time-boxed to an hour or two;
2. where performance or capacity matters, adds a back-of-the-envelope
   resource sketch (network, disk, memory, CPU against bandwidth and
   latency) and aims for roughly right rather than optimal;
3. states the conditions under which the choice does not matter, and stops
   there when they hold;
4. records the assumption that would change the answer, so a later failure
   can trace back to it;
5. when only one solution seems to exist for a material choice, seeks a
   second opinion or records why no alternative exists.

*Taking it too far:* routine [agent-execution § smallest-route](agent-execution-discipline.md#the-harness-selects-the-smallest-executable-route) work uses none of this. The procedure
produces decision evidence, not approval requests; [governance § decision-envelope](governance-decision-boundary.md#delegated-engineering-work-proceeds-by-default)'s default still
stands. When every candidate is bad, the findings drive a third candidate —
they do not license endless divergence.

- from: source[1]

### Search before building; reuse is accounted, not mandated

Before building a capability, search in order: the project's own ownership
map, then the existing dependency set, then the ecosystem. Record why each
plausible existing solution was rejected — and check whether the reason is
fit or merely familiarity.

Adopting a dependency accounts for its cost categories: supply-chain and
provenance risk, security and performance exposure, install and build time,
and the team's tool-count budget. Providing a reusable unit carries the
obligation to keep adoption cost below self-build; reuse is sold, not
commanded. Generality is grown from real repeated use, not designed in
advance.

*Taking it too far:* reuse introduces coupling, so this is not "always
reuse", and it is not a zero-dependency ideology — both extremes manufacture
the wheel or the coupling they claim to avoid. One-off scripts are exempt.

- from: source[1]

### Judgment declares its standpoint

Material analysis names the standpoint it speaks from — user, operator,
product, engineering, or budget — and keeps per-standpoint conclusions
separate instead of averaging them into one verdict. The same fact can be a
defect from one standpoint and immaterial from another; naming the
standpoint is what makes "impact" and "does not matter under these
conditions" decidable in [governance § advice-preserves-disagreement](governance-decision-boundary.md#advice-preserves-disagreement)'s reports. A project may declare its
own goal ordering (for example safety above performance above developer
experience) as the referee when standpoints conflict; the ordering is the
owner's declaration, not this contract's default.

The quality of an interface is judged by its consumer: if the reader or
caller finds it hard, it is hard, and the response is to find where
understanding broke, not to argue.

*Taking it too far:* standpoints are limited to actual stakeholders;
inventing dimensions to look thorough is the ceremony this contract exists
to avoid. Routine work declares nothing.

- from: source[1]

### Every discipline entry carries its own boundary

A rule worth writing down states: the mechanism it addresses, a checkable
instruction, the reason, the constraint that grounds it, and the conditions
under which it does not apply. Scenario-specific knowledge — CSS
architecture, container build caching, memory-exhaustion behavior, schema
evolution, distributed-system assumptions — is written in this format and
mounted as an activated concern in the sense of
[development § activate-concerns](development-discipline.md#activate-concerns-instead-of-expanding-ceremony): present when the scenario is
triggered, absent when it is not, never a universal questionnaire.

Before writing a new scenario rule, look for the existing map: the scenario
has usually been trodden, and the trodden map — with its authorship triaged
per [adoption § authorship-triage](project-adoption.md#external-material-is-triaged-by-authorship-before-adoption) — beats a freshly invented one.

*Taking it too far:* a rule without a boundary is incomplete, but a boundary
without a rule is not a deliverable; this format serves real rules, it does
not manufacture them.

- from: source[2]

## Forbidden behaviors

- Do not convert red flags, symptom counts, or assertion densities into
  mechanical targets; [development § decisions-not-volume](development-discipline.md#govern-document-decisions-not-document-volume) rejects numeric proxies for judgment.
- Do not manufacture options, standpoints, or complexity claims to look
  thorough.
- Do not import vocabulary, metaphors, or slogans from source materials into
  project documents; [adoption § authorship-triage](project-adoption.md#external-material-is-triaged-by-authorship-before-adoption)'s pollution rule applies.
- Do not use the refactor triggers to expand an authorized change beyond its
  scope.
- Do not average conflicting standpoints into a single false consensus.

## Acceptance evidence

This contract is implemented when:

- the [development § activate-concerns](development-discipline.md#activate-concerns-instead-of-expanding-ceremony) rows strengthened on 2026-08-28 route to this contract where the
  judgment method is needed, and entrypoints expose it without restating it;
- at least one real material change has used the comparison procedure and
  recorded its outcome as decision evidence;
- at least one real problem report has used the [governance § advice-preserves-disagreement](governance-decision-boundary.md#advice-preserves-disagreement) fields informed by
  declared standpoints.

Verification stays `pending` for the full procedure: first-party projects
applying this template's discipline since 2026-07 have exercised parts of
this judgment — complexity-cost rejection of over-engineered proposals and
impact-surface triage of review findings — but no material change has yet
run the comparison procedure end to end and recorded its outcome as decision
evidence.

## Reconciliation log

- **2026-08-28 — target created:** drafted from the owner direction of
  2026-08-28 and seven parallel mining passes over the archived reading set.
  Convergent findings across independent sources were preferred: complexity
  enters through well-meaning change and is fought by naming, not counting
  (all sources); refactor triggers are checkable events, not thresholds
  (APOSD, Grug, hacker-laws, SRE toil); in-envelope decisions needed a
  comparison procedure (APOSD design-twice, TigerBeetle resource sketches,
  architecture-decision ROI); problem reports needed immateriality
  conditions and risk-acceptance assumptions (SRE error budgets, G3). Known
  gap: user-experience evaluation has the thinnest source base — Tesler's
  law, Fitts/Hick, and Goodhart give foundations but no full method; a
  dedicated source (HEART-class) is a candidate for a later mining pass.
  - from: source[1], source[2]
- **2026-08-28 — pilot cutover to heading-slug identifiers:** the J1–J6
  codes were retired before they could spread; headings are now the
  identifiers per documentation-harness H13, internal references use short
  names, and incoming references use slug links. This contract is the first
  migrated namespace.
  - from: source[3]
