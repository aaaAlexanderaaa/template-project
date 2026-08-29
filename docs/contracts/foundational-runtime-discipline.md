---
doc_type: contract
status: current
authority: normative
contract_role: governance
implementation: implemented
verification_status: partial
last_reconciled: 2026-08-28
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

1. Take the recognition rule. That is the P2 method.
2. When [development § activate-concerns](development-discipline.md#activate-concerns-instead-of-expanding-ceremony) activates Time and calendar or Demonstration data,
   use the matching invariants as the method owner. Project values (zone
   name, representation, demo gate) live in the adopting project's
   `ARCHITECTURE.md` runtime section, not in this file.
3. When some other change has the same shape, use the [development § activate-concerns](development-discipline.md#activate-concerns-instead-of-expanding-ceremony) concern it already
   belongs to. Do not open a parallel register of scars.
4. Source anchors explain why the method exists. They are not adoption work.

A library, batch job, or project with no user-visible date/time and no
operator-visible seed owes this contract nothing beyond [development § activate-concerns](development-discipline.md#activate-concerns-instead-of-expanding-ceremony)'s default: an
untriggered concern creates no section-filling exercise.

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

## Source anchors

### source[1] — 2026-08-24

> “What I care about is the engineering-implementation issues that were not
> taken seriously at first but later become expensive to change, for example
> time zone. At the start nobody declared using UTC+8, and now we have to make
> a full-system adjustment. That is a fairly bad outcome.”

Context: the owner named timezone as an exemplar of late, system-wide
repair, not as a zone to copy.

### source[2] — 2026-08-24

> “Demo data times should be generated relative to now. At the start there was
> also no policy about demo-data validity and time, so they became hardcoded,
> and it became impossible to run an effective demo.”

Context: hardcoded calendar dates fought the product's own “today”
language after a civil-day rollover.

### source[3] — 2026-08-24

> “There are many other changes made for project health, completeness, and
> viability. Those changes were repairing debt created, left behind, or
> unnoticed earlier. That experience is real engineering experience, and it is
> worth depositing into a Template Project.”

Context: the portable deposit is the recognition rule those repairs share.
It is not a requirement to restate each repair as an adopter row.

### source[4] — 2026-08-24

> “This should not remain only in the current project; it also needs to be
> exported, for example by updating the Template Project.”

Context: export the method into this template; do not copy the source
product's numbers.

### source[5] — 2026-08-24

> “I agree that you should make the change in the Template project. But you
> also need to think about whether that change matches that project's own
> expectations, and you need to evaluate the value of this backfilled
> information. You cannot simply put down the historical pits you stepped in.
> How much value do those pits have? And how should a user look at them?”

Context: a mandatory register of sibling incidents was rejected as
ceremony. Consumption follows [development § activate-concerns](development-discipline.md#activate-concerns-instead-of-expanding-ceremony)
and the transfer-value order.

## Vocabulary

| Term | Meaning | Excluded meaning |
|---|---|---|
| Business timezone | The single IANA zone that owns civil dates and business-local clock time | Host, browser, device, or operator-laptop locale |
| Instant | A timezone-aware absolute moment | A naive datetime, a date string, or a displayed clock |
| Calendar day | A civil date in the business timezone | A 24-hour duration or an instant truncated in another zone |
| Duration | An elapsed length independent of civil midnight | “Tomorrow”, “day 3”, or “today” |
| Clock | The time source production and tests share, injectable in tests | `now()` called independently in each layer |
| Naive input | Date or time text without an offset or zone | A well-formed timestamp that already names its offset |
| Demonstration data | Seed, synthetic, fixture, or sample data operators or customers will see | Disposable unit-test rows that never leave CI |
| Relative business day | Demo dates expressed from the clock's current civil date | Hardcoded calendar dates in a live demo dataset |

## Ownership and boundary

- Recognition rule and the two [development § activate-concerns](development-discipline.md#activate-concerns-instead-of-expanding-ceremony) method bodies: this contract.
- Trigger table: [development § activate-concerns](development-discipline.md#activate-concerns-instead-of-expanding-ceremony). Do not invent a second list.
- Project values: the adopting `ARCHITECTURE.md` runtime section and the
  product contracts that consume them.
- Consumers format, parse, and refresh through that owner. They must not
  invent a second zone, a second “today”, or a second demo dataset.

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

Applies only when [development § activate-concerns](development-discipline.md#activate-concerns-instead-of-expanding-ceremony) activates Time and calendar. Splitting “API is UTC”,
“UI is local”, “jobs use the server”, and “the database session is
something else” is the defect this section exists to prevent.

### One business timezone

All business runtime units use one
IANA timezone. Host, browser, device, and container defaults do not
select it.

- from: source[1]

Enforcement: one named setting; startup fails when a subsystem zone
differs.

### Instants stay instants

Durable datetime values are stored
as timezone-aware absolute moments. Changing session, display, or public
text does not rewrite history or add hours.

- from: source[1]

Enforcement: round-trip tests that the instant is unchanged when
representation changes.

### Calendar is not duration

“Today”, grouping by day, and
“day N after an anchor” use the business timezone's civil date. TTL,
locks, age, retry delay, ordering, and expiry use instants.

- from: source[1]

Enforcement: a civil-midnight case and a duration-crossing case in the
same suite.

### Public representation is declared

System-generated
date-times that leave the process use one declared text form. Mixing
offset-less text, `Z`, and numeric offsets in the same public contract is
a compatibility defect. Dependents must not match a suffix character as
a substitute for parsing.

- from: source[1]

Enforcement: shared formatter/parser; production projections do not
hand-write offset suffixes.

### Naive input is interpreted or rejected, never guessed per device

Offset-less controls and payloads have one declared rule:
attach the business timezone, reject, or accept only a date. A device
timezone must not silently interpret business input.

- from: source[1]

Enforcement: the same naive string yields the same instant under at
least two process timezones, including UTC.

### External timestamps keep their source offset

A record with
a declared offset is stored as that instant. A record with neither
offset nor a protocol-declared zone is rejected or held unknown.

- from: source[1]

Enforcement: a foreign-offset fixture and a naive-reject case.

### One injectable clock

Production and tests obtain “now” and
“today” from the same clock and business timezone.

- from: source[1]

Enforcement: clock injection; a civil-date test that would fail if tests
used UTC while production used another zone.

### Drift fails loudly

Notification, reporting, database
session, job, and container timezone settings either equal the business
timezone or prevent startup.

- from: source[1]

Enforcement: boot or config check with a mismatched subsystem zone.

## Demonstration data

Applies only when [development § activate-concerns](development-discipline.md#activate-concerns-instead-of-expanding-ceremony) activates Demonstration data. Unit-test rows that
never reach an operator or customer are not this concern.

### Demo data is a runtime

Visible seed or sample data has an
owner, an environment gate, and a refresh path. Leftover fixture files
are not a demo strategy.

- from: source[2]

Enforcement: a named command; unknown environments refuse it.

### Live demo dates are relative to the clock

In-progress items
fall on the current business day, upcoming items on later business days,
and completed items on recent ones, using the same civil-date rules as
production. Hardcoded calendar dates in a live demo dataset are a
defect: after one midnight they fight the product's “today” language.

- from: source[2]

Enforcement: refresh anchored at an injected civil date; UI “today”
labels derived from that same date.

### Same-day refresh is idempotent; cross-day refresh replaces the allowlist

Repeating the refresh on the same business day yields the
same natural keys. Crossing a civil date replaces the previous
allowlisted scenes rather than accumulating expired rows.

- from: source[2]

Enforcement: same-day identity assertion; next-day rebuild drops
yesterday's expired allowlisted scenes.

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
| Subsystem timezone drift | Boot/config check | Refuse startup; do not pick a winner silently |
| Naive or unzoned external time | Parser/guard | Reject or hold unknown |
| Demo refresh outside a demo environment | Environment gate | No write; a deployment that required refresh is incomplete |
| Hardcoded live-demo calendar dates | Dataset vs clock | Rebuild relative to the injected civil date |
| Partial scene apply | Transaction/audit | Roll back |

Changing a public timestamp representation is a compatibility cutover of
text, not a data migration of instants, unless the instants-stay-instants invariant was already
violated. If stored values were naive or were rewritten by a zone change,
stop and obtain a human data-risk decision.

## What not to copy

Migrate the method. Do not copy a specific IANA timezone or offset, a demo
host or port, allowlisted fixture identities, a framework setting key, or
a claim that “UTC everywhere” is universally right.

- from: source[4]

## Acceptance evidence

| Outcome | Guard or verification | Durable evidence |
|---|---|---|
| Readers are told how to use this, and a pit catalog is not the interface | This contract's reading section; no adopter register of sibling incidents | this file; `ARCHITECTURE.md` runtime prompts only |
| [development § activate-concerns](development-discipline.md#activate-concerns-instead-of-expanding-ceremony) routes Time and calendar and Demonstration data here | Repository wiring test | `tests/test_check_docs.py` |
| Time and demo invariants are testable as a class | Clock injection, naive-input stability, relative seed, environment gate | adopting project's tests when the concern is activated |
| Product numbers were not copied | Domain-neutral wording | this contract |

Verification remains `partial` until a real adopter activates one of the
two concerns and exercises the method. Structural presence in this
template is not evidence that a product timezone or demo runtime is
correct.

## Reconciliation log

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
