---
doc_type: contract
status: current
authority: normative
contract_role: governance
implementation: implemented
verification_status: partial
last_reconciled: 2026-09-17
review_due: 2026-11-22
supersedes: []
---

# Foundational runtime discipline

## Purpose

This contract owns two [development § activate-concerns](development-discipline.md#activate-concerns-instead-of-expanding-ceremony) concerns — Time and calendar, and Demonstration
data — and the recognition rule that decides whether a fact belongs with
them.

The transferable product is a way of seeing, not a list of incidents. A
historical retrofit has value here only when it teaches a portable test:
the omitted decision is assumed independently in more than one place, and
naming it later is a cutover rather than a local fix. Incidents that fail
that test stay in the source project.

- from: source[1], source[2], source[3], source[5]

## How to read this

This is not a backlog of pits to audit, and it is not a questionnaire that
every adopter must complete.

1. Take the recognition rule. That is the delivery-discipline method — the
   [transfer-value order](project-adoption.md#transfer-value-is-ranked-before-its-carriers)
   tier the README table abbreviates as P2.
2. When [development § activate-concerns](development-discipline.md#activate-concerns-instead-of-expanding-ceremony) activates Time and calendar or Demonstration data,
   use the matching invariants as the method owner. Project policy (scope,
   zone resolution, representation, temporal promise, demo gate) lives in the
   adopting project's `ARCHITECTURE.md` runtime section, not in this file.
3. When some other change has the same shape, use the [development § activate-concerns](development-discipline.md#activate-concerns-instead-of-expanding-ceremony) concern it already
   belongs to. Do not open a parallel register of scars.
4. Source anchors explain why the method exists. They are not adoption work.

A project owes this contract work only for concerns activated by
[development's trigger table](development-discipline.md#activate-concerns-instead-of-expanding-ceremony).
Libraries and batch jobs can activate time concerns through persistence,
scheduling, or exchange without a user interface. An untriggered concern
creates no section-filling exercise.

- from: source[4], source[5]

## Scope

### In scope

- the recognition rule for leak-across-the-system facts;
- Time and calendar when [development § activate-concerns](development-discipline.md#activate-concerns-instead-of-expanding-ceremony) activates it;
- Demonstration data when [development § activate-concerns](development-discipline.md#activate-concerns-instead-of-expanding-ceremony) activates it.

### Out of scope

- a mandatory catalog of other health or viability incidents;
- choosing a product's IANA zone, offset text, demo dataset, or seed
  identities;
- copying another project's framework, port, or compose profile;
- replacing [development § one-owner](development-discipline.md#one-owner-for-every-invariant), [development § environment-over-memory](development-discipline.md#environment-over-memory), or [development § activate-concerns](development-discipline.md#activate-concerns-instead-of-expanding-ceremony); this contract is the owner those
  two [development § activate-concerns](development-discipline.md#activate-concerns-instead-of-expanding-ceremony) rows route to;
- treating a completed demo as a production release gate.

## Vocabulary

| Term | Meaning | Excluded meaning |
|---|---|---|
| Business timezone | The IANA zone selected by the declared scope for a business calendar operation | A zone silently inferred from host or device settings |
| Instant | A timezone-aware absolute moment | A naive datetime, a date string, or a displayed clock |
| Calendar day | A civil date interpreted under the applicable calendar policy | A 24-hour duration or an instant truncated in an unrelated zone |
| Duration | An elapsed length independent of civil midnight | “Tomorrow”, “day 3”, or “today” |
| Clock | The declared time-source interface used by runtime consumers and controlled in tests | Unowned calls that bypass the applicable time policy |
| Naive input | Date or time text without an offset or zone | A well-formed timestamp that already names its offset |
| Demonstration data | Seed, synthetic, fixture, or sample data operators or customers will see | Disposable unit-test rows that never leave CI |
| Temporal promise | The present, fixed reference date, or historical period a demonstration represents | Stale data presented as current activity |
| Relative business day | Demo dates derived from the applicable clock and calendar for a current-day scene | A requirement to move every historical example to today |

## Ownership and boundary

- Recognition rule and the two [development § activate-concerns](development-discipline.md#activate-concerns-instead-of-expanding-ceremony) method bodies: this contract.
- Trigger table: [development § activate-concerns](development-discipline.md#activate-concerns-instead-of-expanding-ceremony). Do not invent a second list.
- Project values: the adopting `ARCHITECTURE.md` runtime section and the
  product contracts that consume them.
- Consumers resolve scope, interpret time, and refresh through the declared
  owners. Different roles may intentionally use different zones or
  representations; consumers must not invent an undeclared resolution rule.

## Recognition rule

A fact is worth declaring before the first durable write, the first
user-visible date/time, or the first operator-visible demo when all of
these hold:

1. if unnamed, more than one producer, consumer, job, or test will assume
   it independently;
2. changing it later is a compatibility cutover, not a local fix;
3. it configures meaning (what “now” is, what “today” is, whether a seed
   remains true tomorrow), not a feature to build.

Timezone and live demo dates are the teaching cases because they fail the
“decide later” test hardest. Other health repairs in a source project are
useful only as evidence that this shape recurs. If the repair already has a
[development § activate-concerns](development-discipline.md#activate-concerns-instead-of-expanding-ceremony) owner — state integrity, security, compatibility, capacity, experience —
use that owner. Listing the repair again here would make volume look like
coverage.

- from: source[1], source[2], source[3], source[5]

## Time and calendar

Applies only when [development § activate-concerns](development-discipline.md#activate-concerns-instead-of-expanding-ceremony) activates Time and calendar. Declare how storage,
calendar calculation, input interpretation, and display obtain their meaning.
Intentional differences between these roles are valid when they conform to
the same declared policy.

### Timezone policy has a declared scope

The owner declares the scope of business calendar rules: system, tenant,
business object, or another explicit scope. Each operation resolves the
applicable zone through that policy. Declare the roles of storage, calendar
calculation, input, and display, including allowed user-local presentation and
how a missing or conflicting scope is handled. Host, browser, device, and
container defaults cannot silently select business meaning.

- from: source[1], source[6]

Enforcement: trace scope resolution through producer and consumer. For example,
tenant-local settlement can coexist with UTC instant storage when that mapping
is declared. Exercise at least two scopes when the product supports them and
an absent-scope case; an undeclared fallback must not pass.

### Instants stay instants

Persisted values representing instants retain an unambiguous absolute moment.
Calendar dates and civil schedules retain their declared semantic types rather
than being silently treated as instants. Changing session, display, or public
text does not rewrite the stored instant.

- from: source[1]

Enforcement: round-trip tests that the instant is unchanged when
representation changes.

### Calendar is not duration

“Today”, grouping by day, and
“day N after an anchor” use the applicable scope's civil date. TTL,
locks, age, retry delay, ordering, and expiry use instants.

- from: source[1]

Enforcement: a civil-midnight case and a duration-crossing case in the
same suite.

### Public representation is declared

Each public contract declares its accepted and emitted time representations
and their meaning. Different interfaces may publish different forms. Values
outside that contract, including undeclared offset-less timestamps, are
compatibility defects. Dependents parse the declared representation rather
than infer meaning from a suffix character.

- from: source[1]

Enforcement: shared formatter/parser; production projections do not
hand-write offset suffixes.

### Naive input is interpreted or rejected, never guessed per device

Offset-less controls and payloads have one declared rule:
resolve the zone from the input's scope with a declared disambiguation policy,
reject, or accept only a date. A device timezone may be used when the input
contract explicitly selects user-local interpretation; it must not silently
interpret business-scoped input.

- from: source[1]

Enforcement: the same input and declared scope retain their meaning under
different process/device zones. Exercise missing scope and ambiguous input
according to the declared resolution or rejection policy.

### External timestamps preserve their declared meaning

A record with a declared offset is interpreted as that instant. Preserving
its original offset text is required only when the owning contract promises it.
A record with neither offset nor a protocol-declared zone is rejected or held unknown.

- from: source[1]

Enforcement: a foreign-offset fixture and a naive-reject case.

### Clock access has an injectable owner

Runtime consumers obtain “now” through the declared clock interface and derive
“today” through the applicable scope's calendar policy. Tests control that
same path through clock injection. Multiple processes need not share a physical
clock object; they must preserve the declared sampling and consistency policy.

- from: source[1]

Enforcement: injected time reaches the actual consumer path; calendar-boundary
tests resolve the intended scope rather than rely on the test host's zone.

### Drift fails loudly

Validate consumers against their declared roles and scope, not against global
timezone equality. Reject invalid static policy at configuration/startup where
it can be checked. If scope is selected dynamically, reject the affected
operation before calculation or mutation when required policy is missing or
inconsistent. Report the scope and recovery action; do not silently pick a zone.

- from: source[1], source[6]

Enforcement: accept intentionally different role settings; reject undeclared
fallbacks and absent dynamic scope without emitting a success or partial write.

## Demonstration data

Applies only when [development § activate-concerns](development-discipline.md#activate-concerns-instead-of-expanding-ceremony) activates Demonstration data. Unit-test rows that
never reach an operator or customer are not this concern.

### Demo data is a runtime

Visible seed or sample data has an owner, a temporal promise, and a delivery
strategy. Static examples need no artificial daily refresh command. Mutating
generation, refresh, and reset operations require the write safeguards below,
including when regenerating historical scenes.

- from: source[2]

Enforcement: identify the dataset's time reference and rendering path; any
mutating command refuses an unknown environment.

### Demo dates and labels meet the temporal promise

Declare whether the scene represents the present, a fixed reference date, or
a historical period, and how the viewer recognizes that reference. Current-day
scenes derive dates and freshness from the applicable clock and calendar;
“today”, “upcoming”, and similar labels must remain true across their validity
boundary. Historical or fixed-reference scenes may retain dates when their
labels and behavior preserve that meaning. A historical label alone does not
excuse stale records still presented as today's activity.

- from: source[2], source[6]

Enforcement: inspect actual dates, labels, and user-visible states together.
Advance the clock across the declared validity boundary for current-day scenes;
verify that fixed-reference scenes preserve their stated reference. A fixed
clock uses the existing injectable path and does not create new business rules.

### Refresh and retention follow the declared strategy

For a mutating scene operation, declare its logical identity/reference, repeat
behavior, and retention or replacement policy. Repeating the same operation
must not create unintended duplicates or extra effects. Crossing the validity
boundary must apply that policy rather than accumulate expired scenes without
a bound. Same-day stable keys with next-day replacement is one strategy;
historical replay can instead retain its fixed reference and declared keys.

- from: source[2], source[6]

Enforcement: repeat the same logical operation and cross its declared validity
or reference boundary. Inspect identities, count, retention, and recovery;
static examples need no mutating probe solely to fill this section.

### Production cannot inherit demo rewrite

Refresh and scene
reset run only in an explicit demo or synthetic environment. Missing
flags fail closed before any write. Refresh is not a generic boot hook.

- from: source[2]

Enforcement: production and unset-flag cases refuse the command with no
mutation.

### Scope is allowlisted and atomic

A refresh names the
identities it may rewrite. Failure leaves no half-applied scene.

- from: source[2]

Enforcement: unknown scenario id and mid-reset failure cases.

### Demo does not impersonate production

Where a viewer could
mistake the dataset for production evidence, the surface says it is a
demo. A successful demo does not close a production gate.

- from: source[2]

Enforcement: the completion claim names the demo layer.

### Standard and demo share one runtime authority

Demo is not a
second client-side state machine or a build flag that ships different
business rules.

- from: source[2]

Enforcement: build or import scan for a second authority path.

## Failure, recovery, and intervention

| Failure class | Detection | Response |
|---|---|---|
| Time or demo activated but unnamed | Missing runtime owner in architecture or product contract | Stop that concern's material delivery; declare or record why [development § activate-concerns](development-discipline.md#activate-concerns-instead-of-expanding-ceremony) does not apply |
| Time policy drift or absent scope | Configuration check or operation guard | Reject the affected configuration/operation before effects; report the missing policy and recovery action |
| Unresolvable naive or external time | Scoped parser/guard | Follow the declared reject/unknown policy; do not guess |
| Demo refresh outside a demo environment | Environment gate | No write; a deployment that required refresh is incomplete |
| Demo dates or labels contradict the temporal promise | Dataset and rendered states vs declared reference | Refresh current scenes or correct the representation; preserve intentional historical dates |
| Partial scene apply | Transaction/audit | Roll back |

Changing a public timestamp representation is a compatibility cutover of
text, not a data migration of instants, unless the instants-stay-instants invariant was already
violated. If stored values were naive or were rewritten by a zone change,
stop and obtain a human data-risk decision.

## What not to copy

Migrate the method. Do not copy a specific IANA timezone or offset, a demo
host or port, allowlisted fixture identities, a framework setting key, or
a claim that one global zone or one daily-refresh strategy fits every project.

- from: source[4]

## Acceptance evidence

| Outcome | Guard or verification | Durable evidence |
|---|---|---|
| Readers are told how to use this, and a pit catalog is not the interface | This contract's reading section; no adopter register of sibling incidents | this file; `ARCHITECTURE.md` runtime prompts only |
| [development § activate-concerns](development-discipline.md#activate-concerns-instead-of-expanding-ceremony) routes Time and calendar and Demonstration data here | Repository wiring test | `tests/test_check_docs.py` |
| Time and demo invariants are testable as a class | Scoped policy conformance, clock injection, input stability, temporal promises, repeat safety, environment gate | adopting project's tests when the concern is activated |
| Product numbers were not copied | Domain-neutral wording | this contract |

Verification remains `partial` until a real adopter activates one of the
two concerns and exercises the method. Structural presence in this
template is not evidence that a product timezone or demo runtime is
correct.

The [September 7 change record](../plans/2026-09-06-proportionate-execution.md#progress-and-closure)
records review of scoped time resolution, demo temporal promises, and their
negative cases. No product runtime was deployed or certified by that review.

## Source anchors

### source[1] — 2026-08-24

The maintainer reported a project where components assumed different time
policies because no policy had been declared early. Aligning them later
required system-wide changes. The example motivates explicit time-policy
ownership; the original project's chosen UTC offset is not an adopter default.

### source[2] — 2026-08-24

The maintainer reported demonstration data with fixed dates while the UI
promised current-day activity. After time passed, the displayed scenes no
longer met that promise. This motivates choosing an explicit temporal promise
and an appropriate refresh strategy; intentionally historical scenes need not
be rewritten to the present.

### source[3] — 2026-08-24

The maintainer asked the template to learn from expensive repairs to omitted
engineering decisions. The reusable result is a way to recognize a decision
that will spread across components, not a catalog of another project's debt.

### source[4] — 2026-08-24

The maintainer authorized applying the time-policy and demonstration-data
lessons to this template. Each adopter still selects its own product policies
under the template's concern-activation method.

### source[5] — 2026-08-24

A proposed mandatory register of past incidents was rejected because it
created work even when the adopter had no corresponding concern. The accepted
method routes applicable time and demonstration-data work through
[development's concern triggers](development-discipline.md#activate-concerns-instead-of-expanding-ceremony)
and the transfer-value order. These source entries summarize maintainer-reported
experience; the original incident records are not supplied as public evidence.

### source[6] — 2026-09-07

English rendering of the maintainer's accepted proposal: replace a universal
single-business-timezone rule with declared scope and role resolution. Check
related demonstration-data assumptions so current-day and clearly labeled
historical scenes can use different temporal policies while retaining write
safety and truthful outcomes.

## Reconciliation log

- **2026-09-15 — P2 reference made self-describing:** the "How to read this"
  pointer now names the delivery-discipline tier and links its owning
  contract instead of relying on the README table's bare P2 label. Flagged by
  the letter-code health scan; the label remains defined in the README table
  itself.

- **2026-09-07 — scoped time and demo policies:** replaced global zone equality
  with declared role/scope resolution and checks at configuration or operation
  boundaries. Demo dates, labels, refresh, and retention follow the temporal
  promise; current-day freshness and mutating-operation safeguards remain.
  Historical source statements describe the incident that motivated the
  method, not universal product settings.
  - from: source[6]

- **2026-08-24 — consumption corrected:** a mandatory `ARCHITECTURE.md`
  register of sibling retrofit rows was retracted. It treated historical
  pits as adoption work and violated development D8 (untriggered concerns
  create no questionnaire) and D9 (volume is not coverage). The contract
  now leads with how to read it: recognition rule as P2 method; time and
  demo as D8-activated worked examples; other source-project repairs stay
  evidence of the shape, not extra rows.
  - from: source[5]
- **2026-08-24 — method exported:** D8 gained Time and calendar and
  Demonstration data rows routed here, so undeclared clocks and hardcoded
  live-demo dates are a named class rather than an unstated surprise.
  Independent effectiveness in an adopting product remains open.
  - from: source[1], source[2], source[4]
- **2026-08-28 — cutover to heading-slug identifiers:** the INV-T/INV-D codes
  were retired and the labeled list items were restructured into `###`
  headings so every invariant is a linkable target, per [documentation-harness § invariant-citations](documentation-harness.md#invariant-citations-resolve-to-headings).
  Incoming references across living documents were rewritten to slug links in
  the same change. Earlier entries in this log, completed plans, and dated
  evidence keep the codes as written.
