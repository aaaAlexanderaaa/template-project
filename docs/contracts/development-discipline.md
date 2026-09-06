---
doc_type: contract
status: current
authority: normative
contract_role: governance
implementation: implemented
verification_status: partial
last_reconciled: 2026-09-06
supersedes: []
---

# Development and collaboration discipline

## Purpose

This contract defines how work is understood, specified, implemented,
verified, and handed off. It is domain-neutral: it governs collaboration and
change quality, not any particular product, framework, runtime, or deployment.

The objective is to move project intent out of chat history and individual
memory into durable, reviewable contracts and reproducible evidence while
preserving a clear, low-friction path for reversible engineering work and
controlled learning.

## Source anchors

### source[1] — 2026-07-28

> “Enable rather than obstruct. An agent should know clearly what it should
> and should not do, instead of constantly fearing mistakes because it has
> not understood the user's needs and situation.”

### source[2] — 2026-07-28

> “Avoid mere expansion. Long-term governance should manage the existing
> stock: retirement, distillation, and summary, not only increment. Document
> coupling makes it easy for the same matter to appear in several documents.”

### source[3] — 2026-08-06

> “When you encounter an unfamiliar named reference, publication, or anything
> else you do not know, use network tools to look it up; do not guess. If a
> tool is unavailable, do not give up; find a fallback. When the user asks a
> question, identify the unasked issue that may be more important and point it
> out. Break problems down to make the causal mechanism clear, not to add
> layers, and not to pile empty abstraction for an appearance of depth.”

### source[4] — 2026-08-06

> “Agreed with your understanding: adopt frontend-design, uninstall
> ui-ux-pro-max, and learn what is worth learning.”

### source[5] — 2026-08-24

> “This should not remain only in the current project; it also needs to be
> exported, for example by updating the Template Project.”

### source[6] — 2026-08-27

> “When a rule stated in conversation recurs, propose recording it as a
> durable rule in the document that owns its topic. Keep document wording in
> plain style, because the wording of descriptive documents guides future
> language style.”

### source[7] — 2026-08-28

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
>
> “Specific problems need specific analysis, but the scenarios have been
> trodden by many before. Keep enough text to remind an agent to consider
> what it has not considered — to avoid drilling into a dead end,
> over-optimizing, or over-designing.”

### source[8] — 2026-09-06

Original maintainer wording in this task:

> “仍然不够目标驱动”
>
> “声明应该发生，但实现不存在”；“实现产生了未声明的效果”；
> “效果发生次数过多”；“效果被错误压制，发生次数过少”。

Maintainer feedback in the template review task, rendered in English: delivery
must serve the user's goal, not merely pass tests. Check for promised effects
that are absent, undeclared effects, and effects that occur too often or too
rarely. Include functional and nonfunctional requirements, user costs, boundary
cases, and what the user can do after a result. Improve recurring mistakes in
the harness instead of accumulating reminders and startup reading.

## Core invariants

### Contract before material delivery, evidence before certainty

Do not deliver a material feature or behavior change until its contract exists
on disk. The contract must name the behavior, relevant states and triggers,
ownership boundary, failure behavior, non-goals, and acceptance evidence.

When a material fact cannot be learned through read-only investigation, a
bounded experiment may precede the delivery contract. The experiment is
evidence, not product implementation. Before it runs, route the experiment's
own actions through the activate-concerns invariant. Every activated concern uses an existing normative
owner and safety boundary; an experiment record cannot create either one.

The experiment records its question, disposable path, expiry, abort trigger,
containment and cleanup actions, cleanup evidence, and the escalation path for
boundary escape or failed cleanup. It cannot become a public interface or
production dependency. Privileged or irreversible actions still require
separate prior authorization and remain subject to the owning contract; the
experiment creates no such authority. Useful findings may move into durable
evidence and inform a later contract, but scratch implementation is discarded
at expiry or conclusion even when its findings are adopted.

Routine corrections and mechanically bounded refactors may rely on an existing
current contract when they introduce no new semantics, state, boundary, or
failure behavior. They do not require a standalone contract solely to satisfy a
ritual. If no applicable contract exists for a material change, write one
first. If current discussion conflicts with a landed contract, stop dependent
implementation, record the conflict, reconcile it, and only then continue.

Comments, tickets, commit messages, and conversation summaries are supporting
context; they are not substitutes for the normative contract.

- from: source[1]

### One owner for every invariant

Every state transition, data rule, API shape, layout rule, shared visual value,
cross-cutting quality attribute, and operational decision has one authoritative
owner. Consumers may use the owner's public contract but must not silently
reproduce or override its private rules.

Cross-layer behavior must identify:

- the authoritative state owner;
- the public interface used by consumers;
- what consumers may display or configure;
- what consumers must never infer independently.

Performance, capacity, resource cost, security, privacy, reliability, build and
dependency integrity, and production-observation policy are governed when the
change can affect them. They use the same ownership model as functional state:
one owner, a scenario and measurable response or explicit qualitative
boundary, a guard or observation surface, and an escalation and exception
policy. The owner may declare a boundary non-waivable; the existence of an
escalation path does not imply that an exception is available.

- from: source[1]

### Coherent end state

Design migrations around one complete end state. Real dependency order may
produce multiple execution checkpoints and explicit transitional states, but
those states have an owner, entry and exit conditions, compatibility behavior,
observation, and removal or promotion criteria. They must not become an
intentionally half-migrated architecture, indefinite compatibility layer, or
placeholder that is merely promised to be corrected later.

If a coherent end state cannot yet be described or verified, do not start the
delivery migration. Use the bounded experiment path in the contract-first invariant to learn the missing
facts without presenting the experiment as the destination.

### Outcomes before means

Define success in terms of observable outcomes before listing implementation
or test mechanics. The default quality outcomes are:

1. functionality is correct;
2. presentation is correct;
3. interaction is correct;
4. the result follows the product's design and domain logic;
5. failure and recovery behavior are understandable;
6. every activated quality attribute stays within its declared boundary;
7. production-only assumptions have an observation and rollback decision.

Tests, probes, selectors, thresholds, and scripts explain how those outcomes
are checked; they are not the outcome themselves. Preserve the original request
or its source alongside the accepted interpretation. Before closing delivery,
compare the observed result with both. A correct implementation of a mistaken
interpretation still needs reconciliation; passing its tests does not close
the requested outcome.

### Verify promised and observed behavior in both directions

The owning contract's acceptance matrix lists functional outcomes and activated
nonfunctional requirements by user or operator scenario. Each names a trigger,
starting state, observable response, and applicable boundary. Link an existing
quality owner instead of duplicating its threshold. Do not derive this list
solely from the tests or the implementation. The future reconciliation
`promise[...]` register is not a product feature inventory.

For effects such as requests, writes, events, notifications, or repeated user
actions, define the affected identity and scope, allowed count or bound per
logical operation, and relevant timing/order. Where repetition matters, also
define which triggers create an operation, any cadence or bound across an
observation window, and the freshness or maximum silence the outcome permits.
Include concurrency, retries, cache reuse, and suppression when they can
change those effects. State what is unknown; do not invent a safe request rate
or claim exactly-once behavior from
an idempotency key alone. User cost includes unnecessary requests, account
exposure, latency, attention, and recovery effort when applicable.

Verification runs in both directions:

- For each promised result, observe whether it occurs under its trigger and
  meets its functional and quality boundaries.
- Inspect actual externally visible effects at the affected boundary, including
  effects absent from the expected-result list. Map each to an authorized
  requirement or report it for reconciliation. Evidence drawn only from a
  helper's return value cannot establish effects at another boundary.
- Distinguish missing, undeclared, excessive, and wrongly suppressed effects.
  Also inspect wrong identity/scope, premature or stale effects, partial
  completion, and misleading success when applicable. These are prompts for
  analysis, not an exhaustive taxonomy or a mandatory test count.
- Exercise failure and recovery from the user's position: what is known, what
  remains unresolved, what was changed, and what action is available next.

Use the smallest credible evidence for each claim. A failing regression test,
an instrumented process, a packaged artifact, a browser observation, or a
bounded manual review may be appropriate. Record the relevant conditions and
limits. Missing observations remain unknown or not run, never a pass. Required
evidence for a completion claim cannot be replaced by a cheaper unrelated check.

- from: source[8]

### Environment over memory

A recurring rule needs an enforcement surface outside human memory. Depending
on the rule, use types, schema validation, static checks, unit tests,
architecture tests, integration tests, runtime assertions, or reproducible
probes.

Prose explains intent and trade-offs. Mechanical guards stop the same class of
mistake from recurring.

Agent memory and summaries may help locate evidence; they do not create
authority. Recheck their source, scope, and current applicability before using
them for a material decision. Reconcile conflict with current authority rather
than treating confident recall as a new instruction.

- from: source[8]

### Fix the category, not only the symptom

Before fixing a defect, name its category and root mechanism. When that
mechanism has repeatable sibling variants, the change includes a class-level
guard capable of catching at least one plausible variant that was not in the
original report.

A symptom-only patch is incomplete when the same mechanism can fail elsewhere.
When evidence shows no repeatable sibling mechanism, a stable guard is not
possible, or the guard would cost more than the bounded risk warrants, record
that fact and keep the change local. This invariant is not permission to
expand an authorized fix into an unbounded cleanup.

When the project operates incidents or postmortems, their output feeds this
invariant: a postmortem names the root-cause category — possibly several —
and the class-level action for each, and a monitoring failure (a user noticed
before the system did) is itself a defect category. A postmortem that ends in
a local fix without a named category is incomplete.

When the harness contributed to a repeated error, correct the smallest owner
that caused it: a default, interface, example, context route, check, or rule.
Verify a plausible sibling case and remove any reminder made redundant by the
fix. Keep the useful mechanism and its limits, not the whole incident in the
startup context. If no proportionate guard exists, keep a short example or
review cue at the relevant owner and say what it cannot prevent. More recorded
lessons alone are not evidence of improvement.

- from: source[7], source[8]

### Preserve decisions and evidence

Requirements, translations, implementation plans, issues, and evidence have
different authority. Do not overwrite one with another. Superseded material
keeps an explicit replacement link so later contributors can reconstruct why a
decision changed.

### Activate concerns instead of expanding ceremony

Governance depth follows the change's observable traits, not the size of its
template or the caution of its implementer. A concern that is not triggered
creates no document, section-filling exercise, review lens, or test obligation.
For every activated concern, an applicable current or target contract is the
sole owner of its boundary, failure policy, and escalation or exception policy.
A plan records only the selected concern, owner link, execution steps, and
proportionate evidence.

If no normative owner exists, material delivery waits for a contract to
establish one. An experiment under the contract-first invariant may proceed only through safety boundaries that
already exist for its own activated actions; it cannot use a plan or scratch
record to invent a temporary quality boundary.

The concern routing table below is the normative owner. Agent instructions,
guides, and templates may link to or project it but must not define competing
trigger semantics.

| Change trait | Activated concern | Minimum questions |
|---|---|---|
| Public interface, event, schema, or consumer-visible meaning | Compatibility | Version, consumers, cutover, deprecation, rollback |
| Durable state, migration, concurrency, or replay | State integrity | Atomicity, idempotency, ordering, recovery, manual intervention, schema evolution and extensibility |
| Permission, identity, untrusted input, sensitive data, or cross-tenant access | Security and privacy | Trust boundary, least privilege, abuse/failure case, audit, retention |
| Hot path, scale assumption, resource model, or material cost change | Performance, capacity, and cost | Load scenario, response/budget, saturation, backpressure or degradation, named resource bounds and chosen exhaustion behavior |
| Availability dependency, timeout, retry, failover, degradation, recovery behavior, or operator workflow | Reliability and operations | Service objective and its error budget, dependency failure, observability, actionable-alert test, postmortem trigger, alert/rollback trigger |
| External package, generated artifact, compiler, build or delivery path | Dependency and build integrity | Existing-solution search before building, owner, provenance, reproducibility, compatibility, cost categories, unavailable-dependency behavior |
| User-visible surface or interaction | Experience | Reachable states, accessibility, responsive/input behavior, locale and copy where relevant, complexity displaced onto the user, task success and time signals |
| Persisted, scheduled, displayed, or exchanged date/time; calendar-day; duration; or clock | Time and calendar | Unique zone, instant vs calendar vs duration, naive-input policy, public representation, injectable clock, fail-loud drift |
| Demo, seed, synthetic, fixture, or sample data that operators or customers will see | Demonstration data | Clock-relative validity, environment gate, idempotent refresh, production isolation, labeled demo |
| Assumption verifiable only after release | Production learning | Signal, observation window, decision threshold, rollback/reconciliation owner |

- from: source[1], source[5], source[7]

### Govern document decisions, not document volume

Document count and length are consequences of bounded contexts, risk, and the
number of durable decisions; they are not quality targets. Long-term governance
includes update, merge, historical synthesis, supersession, retirement, and
disposal, without universal file-count, line-count, directory-depth, or blanket
retention-age limits as quality or deletion proxies. This does not remove the
target-review, promise, or pending-evidence deadlines owned by the
documentation harness.

One normative rule is defined in one authoritative document. Other documents
route, project, explain, or provide evidence without adding conditions. The
documentation authority map owns the creation, active-read-set, projection, and
subtraction mechanics; this invariant does not redefine them.

- from: source[2]

### Unknown references are researched, not reconstructed

When a request, contract, source, or discussion relies on an unfamiliar term,
named reference, publication, external system, or other checkable fact, do not
complete it from resemblance or memory. Inspect available local evidence
first; when that is insufficient, use available network or retrieval tools to
consult authoritative external sources. Prefer the original publication,
official documentation, standard, or owning institution over a secondary
summary, and preserve enough source identity for another contributor to check
the claim.

Separate what the source states from inference and recommendation. If neither
local nor external evidence can establish the fact, name the unknown and its
effect instead of inventing a plausible answer. Research is still bounded by
the request's permissions, privacy boundary, and activated security or cost
concerns.

- from: source[3]

### Tool failure triggers capability-preserving fallback

Failure or absence of one tool is not by itself failure of the task. Identify
the capability and evidence the step requires, then try an available fallback
that preserves the intended semantics, safety boundary, and strength of
evidence. Examples include another repository search mechanism, a primary
source reached through a different retrieval path, a language-native check in
place of a convenience wrapper, or a controlled manual inspection when its
limitations are explicit.

Do not silently substitute a path that changes product behavior, mutates a
different system, weakens an adopted guard, or supports a weaker completion
claim. If no permitted fallback can preserve a required capability, report the
attempts, exact missing capability, affected claim, and recovery options; only
then may the condition enter the blocker routing owned by [governance § narrow-blockers](governance-decision-boundary.md#blockers-are-narrow-and-evidence-backed).

- from: source[3]

### Analysis exposes the decisive causal mechanism

Analysis and explanation are complete when they identify the relevant
conditions, the mechanism by which those conditions produce the observed or
expected outcome, the boundary where that explanation stops holding, and the
evidence that could distinguish it from alternatives. More headings, layers,
or abstract categories are not evidence of deeper understanding.

Answer the user's explicit question, and also surface an unasked premise,
constraint, outcome, or risk when evidence shows it is materially more
consequential to the user's goal. State the causal connection and classify the
observation through the governance vocabulary. Do not use this obligation to
speculate without evidence, replace the requested task, manufacture priority,
or expand implementation scope without authorization.

- from: source[3]

### Recurring verbal rules are proposed for durable recording

A rule the owner states in conversation binds from the moment it is stated,
but conversation is not durable storage. When a general rule is stated — and
especially when the same rule is stated again, or is phrased as something to
remember — propose recording it in the document that owns the topic: a
contract invariant, a guide procedure, a template field, or an agent
entrypoint. The proposal states the rule in plain wording, its reason, how it
applies, and its source and date. The owner confirms before it lands.

An explicit instruction to adopt or implement the rule supplies that
confirmation for its stated scope. Do not request the same confirmation again.

A rule that lives only in chat history or agent memory decays with the context
that carries it. Recording is proposed, not assumed: the decision to adopt
remains with the human owner, and a rejected proposal stays as history rather
than returning as an unwritten rule.

- from: source[6]

## Change workflow

Material delivery satisfies the following obligations in dependency order.
Contract reconciliation precedes dependent implementation; required design
review precedes implementation and completion review precedes closure.
Investigation, implementation, and verification may iterate. This list does
not prescribe user approval checkpoints or require a record for every item.

1. **Classify and route.** Establish the decision envelope, evidence state, risk
   profile, and concerns activated by the activate-concerns invariant.
2. **Investigate.** Inspect current contracts, code, state, tests, and existing
   evidence before asking questions that the repository can answer. Apply the research-unknowns invariant
   to unfamiliar external references and the capability-fallback invariant when an investigation tool is
   unavailable. Use a bounded experiment under the contract-first invariant
   only when read-only evidence cannot answer a material technical fact.
3. **Resolve authority.** Identify the current normative document and the code
   or service that owns the behavior.
4. **Reconcile intent.** Record ambiguity, contradiction, or changed
   requirements. Do not silently choose between conflicting sources.
5. **Land or update the contract.** Define states, triggers, boundaries,
   failure behavior, non-goals, and acceptance outcomes.
6. **Write the execution plan.** Describe one coherent end state, dependency
   order, affected files or surfaces, risks, and verification.
7. **Implement with guards.** Preserve unrelated work and add the smallest
   class-level enforcement surface that protects the intended behavior.
8. **Verify proportionally to risk.** Cover the changed unit, its integration
   boundary, affected user-visible states, and failure/recovery paths.
9. **Observe when activated.** Evaluate production-only assumptions and apply
   the declared continue, rollback, or reconcile decision.
10. **Close the loop.** Update implementation and verification status, attach
    durable evidence, resolve or supersede the plan, retire redundant working
    material, and update issue state.

## Frontend development contract

Frontend work translates product intent into observable states and geometry.

### Required before implementation

- A current surface contract containing dated raw stakeholder language and an
  engineering translation.
- An explicit state catalog: empty, loading, populated, error, disabled,
  selected, expanded, or other reachable variants relevant to the surface.
- Layout and size expectations, including narrow, intermediate, and wide
  containers where applicable.
- Interaction expectations: trigger, state transition, focus behavior,
  reachability, and failure/empty response.
- Browser, input, accessibility, and responsive support targets.
- Locale, text expansion, and input-method behavior when the surface
  activates those concerns.
- If the surface displays or accepts date/time, consume the Time and
  calendar owner from the activate-concerns invariant: business timezone, instant vs calendar-day vs
  duration, naive-input interpretation, and the injectable clock. If it
  does not, the activate-concerns invariant creates no extra obligation. Omission is not UTC and not
  the device timezone.
- If the surface shows seed, synthetic, or sample data to an operator or
  customer, consume the Demonstration data owner. Hardcoded live-demo
  calendar dates are a defect.
- The style layer, value tiers, and published override surface the change
  consumes, plus any value it must define locally and why.

### Design direction and content

Visual direction translates authorized product intent; it does not create
missing product intent. Ground each surface in a concrete subject, audience,
and single user job found in its raw layer. Use the subject's real materials,
instruments, artifacts, language, and workflows where they improve recognition
or use. When a missing subject, audience, job, or expensive-to-reverse
preference would materially change the result, use [governance § route-uncertainty](governance-decision-boundary.md#missing-knowledge-is-routed-not-automatically-escalated) rather than
silently choosing a plausible theme.

Before implementation, work in two design passes:

1. propose a compact candidate direction covering named color roles,
   typography roles, layout concept, content voice, motion intent, and at most
   one signature element that serves the user job;
2. critique that direction against the raw brief, the product's own world, and
   the generic defaults likely to recur across unrelated products, then revise
   any choice that cannot be justified specifically.

Candidate directions are decision evidence, not a new source of visual truth.
Only the accepted translation enters the surface contract and consumes or
extends the declared style owner. A generated palette, token file, design
master, mockup, or skill output cannot override those owners. Concentrate
visual emphasis in the signature element, match execution complexity to the
accepted direction, and remove decoration that communicates nothing true about
the subject or hierarchy.

Interface language is part of the design contract. Use the user's vocabulary
and active, specific action names; keep an action's name consistent from
control through result feedback; let labels, examples, and supporting text each
do one job; and make empty and failure states explain the available recovery or
next action without vague apology or promotional filler.

When a human-owned visual preference cannot be decided usefully from prose,
prepare a bounded set of low-cost alternatives or a disposable visual probe in
`tmp/`. State the question it resolves, keep it out of production and public
interfaces, record the owner's reaction as dated raw surface input, and remove
the probe when it supports no live evidence. The probe informs the contract; it
does not authorize delivery or become the accepted design by survival.

- from: source[4]

### Style ownership and layering

Style decay is a dependency-direction and precedence problem that happens to
render. The rules below are the frontend instance of the one-owner invariant; they do not create a
second authority for frontend work.

- **Precedence is declared, not emergent.** The project declares one ordered
  list of style layers, lowest to highest authority, and every file in its
  style corpus resolves to exactly one of them. Which owner wins is a
  declaration, not a consequence of selector weight, source order, or the
  order in which build artifacts happened to be concatenated.
- **An omission is not a low-priority default.** Where the realizing mechanism
  grants undeclared style the *highest* authority rather than the lowest,
  forgetting to declare a layer is an escalation. Declaring the corpus is what
  prevents it. A project whose mechanism resolves conflicts by artifact or
  load order records that dependency and the risk it accepts.
- **Shared values are tiered and reference one way.** Named visual values are
  declared in ordered tiers — raw values, the roles they serve, and any
  unit-scoped names — each with one owner. A tier may reference only tiers
  below it. Consumers bind to roles rather than to raw values, because a name
  that describes an appearance cannot be re-pointed when the appearance
  changes.
- **A literal at a use site is an unowned decision.** A recurring visual value
  restated where it is used forks its owner, including when it is restated as
  a fallback beside the reference. The project declares which classes of value
  are governed and which literals remain legal.
- **The override surface is published, and everything else is private.** A
  unit others may restyle enumerates what they may set: named values, named
  regions, named variants. That enumeration is the soft boundary of
  `ARCHITECTURE.md` §8; everything not enumerated is hard. Reachability is not
  publication.
- **Escalation is recorded debt, not technique.** Winning by outranking rather
  than by owning — forced priority, inflated selector weight, or reaching
  across a declared boundary — is legitimate only as a declared permanent part
  of a layer's contract, or as a registered exception carrying one owner, a
  reason, and a removal condition. An exception with no owner is not an
  exception.
- **Responsive authority names its measurement basis.** Each adaptive band
  states what is measured and who owns it: the space the unit was given, or
  the display. A unit that adapts to the display is correct only where it was
  measured.
- **Style is deletable or it is permanent.** A unit's style is owned in one
  declared place, so removing the unit removes its style. Where reachability
  cannot be established mechanically, the project records that blindness
  rather than treating an unproven rule as live.

### Verification discipline

- Verify every relevant reachable state, not one convenient sample.
- Use both perceptual evidence and structural evidence for layout-affecting
  work. A screenshot can reveal hierarchy; rendered measurements establish
  geometry.
- Perceptual review checks fidelity to the subject, audience, user job, accepted
  design thesis, hierarchy, content voice, and deliberate restraint. It names
  any generic default or decoration that survived without a brief-specific
  reason; a screenshot remains evidence, not a style owner.
- Measure all repeated instances and both axes when investigating containment
  or clipping. Do not generalize from the first match.
- Exercise intermediate responsive ranges, not only the smallest and largest
  viewports.
- Verify usability, not merely DOM existence: focus, scrolling, hit targets,
  discoverability, keyboard/touch access, and error feedback matter.
- High-risk visual or interaction changes require an independent verifier who
  reads the contract and evidence without inheriting the implementer's
  assumptions.

### Frontend completion criteria

A frontend change is complete when functionality, display, interaction,
accessibility, responsive behavior, and visual logic meet the surface contract;
the presentation and interface language remain specific to its subject,
audience, user job, and accepted design direction rather than an unexamined
generic default;
every visual value it introduces resolves to a declared owner or to a
registered exception with an owner and a removal condition; the relevant
mechanical guards pass; and the production-like surface has been verified.

## Backend and service development contract

Backend work owns domain truth, state transitions, reliability, and public
interfaces.

### Required before implementation

- The authoritative owner of each state and invariant.
- Versioned request, response, event, and error contracts where consumers cross
  a process or module boundary.
- State-machine transitions, including invalid transitions.
- Idempotency, concurrency, ordering, and duplicate-delivery behavior.
- Failure classification, retry eligibility, timeout behavior, recovery, and
  operator intervention points.
- Persistence, transaction, migration, and rollback expectations.
- Observability: logs, events, metrics, audit fields, and diagnostic identity.
- Permission boundaries and the minimum capabilities each caller needs.
- Activated performance/capacity, reliability, security/privacy, dependency,
  production-learning, time/calendar, and demonstration-data boundaries
  from the activate-concerns invariant.
- When Time and calendar is activated: the unique business timezone,
  instant vs calendar-day vs duration, naive-input policy, public
  representation, injectable clock, and fail-loud drift check.
- When Demonstration data is activated: clock-relative validity,
  environment gate, same-day idempotent refresh, and production isolation.

### Verification discipline

- Test invariants and state transitions, not only helper functions.
- Include restart, retry, timeout, stale ownership, partial write, duplicate
  request, and invalid input cases when relevant.
- Use controlled fakes at external boundaries so end-to-end tests validate the
  system's institution and lifecycle rather than the quality of an external
  dependency.
- Assert API self-consistency: payload, counts, cursors, status, persisted state,
  and replay must describe the same reality.
- Fail loudly on invalid configuration or missing dependencies; never silently
  switch to a different behavior.

### Backend completion criteria

A backend change is complete when ownership remains clear, public contracts are
versioned or reconciled, state survives the declared failure model, permissions
remain least-privilege, behavior is observable, and class-level lifecycle tests
pass.

## Cross-stack coordination

For a change spanning frontend and backend:

1. Define the shared state and interface contract first.
2. Keep business truth and mutation authorization in the backend owner.
3. Let the frontend project that truth into interaction and presentation; do
   not make it reconstruct hidden domain rules.
4. Enumerate loading, empty, stale, partial, unauthorized, conflict, retryable,
   and terminal error states as applicable.
5. Cut over producer and consumers within one coherent compatibility decision.
6. Verify both API consistency and the user-visible projection.
7. Carry every concern activated under the activate-concerns invariant
   through its authoritative owner rather than
   duplicating hidden thresholds or policy in both stacks.

## Documentation lifecycle

Documents must declare their type, status, authority, and reconciliation date.
Contracts additionally declare implementation and verification status.

Lifecycle is also a read-path control. `current`, `target`, `active`, and
`needs_reconciliation` material remains visible to normal work selection;
completed, historical, and superseded material leaves that active path. Retain
the latter only for a decision, evidence, audit, or recovery reason. The
detailed stock and projection rules live in `docs/README.md`, which owns the
documentation authority map.

- `current`: normative for present behavior.
- `target`: accepted future behavior; not evidence that current code is wrong.
- `active`: execution work in progress.
- `completed`: plan finished; retained as history.
- `historical`: context or evidence only.
- `superseded`: replaced, with `superseded_by` set.
- `needs_reconciliation`: known conflict; dependent implementation pauses.

Plans never override current contracts. Guides describe procedures but do not
define product behavior. Issues own defect lifecycle but do not silently change
contracts. Evidence supports a claim but does not become normative merely
because it is recent.

## Reconciliation protocol

When intent and implementation disagree, classify the mismatch:

1. **Source ambiguity:** add a dated clarification and update its translation.
2. **Translation error:** correct the engineering contract and record why.
3. **Requirement change:** add a superseding source statement and replacement
   link.
4. **Implementation regression:** keep the contract and repair code plus guard.
5. **Evidence conflict:** repeat or improve the measurement; do not rewrite the
   contract to fit weak evidence.

No side may resolve a conflict silently.

## Reconciliation log

- **2026-09-06 — outcome and effect verification:** separated original intent,
  accepted requirements, and observed delivery; added bidirectional acceptance
  and bounded learning at the existing owners. The maintainer's request to
  improve this template authorizes this adoption. Structural checks cannot
  prove that future agents apply these rules effectively.
  - from: source[8]

- **2026-08-28 — D8 minimum questions extended to settled engineering
  scenarios:** five rows gained the questions industry practice has already
  settled for their scenario: schema evolution and extensibility (state
  integrity), named resource bounds and chosen exhaustion behavior
  (performance/capacity), error budget, actionable-alert test, and
  postmortem trigger (reliability/operations), existing-solution search and
  cost categories (dependency), displaced complexity and task success/time
  signals (experience). D6 now names postmortem output and monitoring
  failure as category sources. The deeper judgment method — complexity
  vocabulary, refactor triggers, the in-envelope comparison procedure,
  build-vs-reuse accounting, standpoint declaration — is drafted in the
  target contract `docs/contracts/engineering-judgment-discipline.md`.
  Sources: owner direction of 2026-08-28; external materials mined from the
  local archive under `archive/external/`, authorship-triaged per O8.
  Verification remains partial until a real change answers these questions.
  Plan: `docs/plans/2026-08-28-engineering-judgment-discipline.md`.
  - from: source[7]
- **2026-08-27 — recurring verbal rules proposed for recording:** D13 added.
  A general rule stated in conversation is proposed for durable recording in
  its owning document, with plain wording, reason, application, source, and
  date; adoption remains the owner's decision. Document language style is
  owned by the documentation authority map. The fixture clock moved to
  2026-08-27 with the new canonical dates; the full suite and both checker
  modes pass. Verification remains partial until a real project exercises
  the proposal loop.
  - from: source[6]
- **2026-08-24 — foundational runtime concerns routed:** D8 now activates
  Time and calendar and Demonstration data and routes them to
  `docs/contracts/foundational-runtime-discipline.md`. Frontend and backend
  required-before-implementation lists no longer treat timezone as an
  optional localization footnote. A sibling-incident questionnaire was
  rejected; untriggered concerns still create no section-filling. The
  method is domain-neutral. Verification remains partial until a real
  adopter activates one of the two concerns.
  - from: source[5]
- **2026-08-06 — subject-grounded frontend direction adopted:** the owner
  selected the reviewed `frontend-design` approach over the database-driven
  alternative. The frontend contract now requires brief-specific design
  direction, two-pass generic-default critique, consistent interface language,
  and bounded visual decision evidence while keeping accepted values in the
  existing surface/style owners. Disposable probes remain evidence, not
  delivery or parallel design authority; verification remains partial until a
  real adopter exercises the method. The template-required direction section
  first produced the expected missing-section failure, then the full 106-test
  Python 3.11 fixture suite and strict repository check passed after the
  projection landed.
- **2026-08-06 — evidence and causal inquiry added:** made authoritative-source
  research, capability-preserving tool fallback, and causal analysis with
  bounded surfacing of more consequential unasked questions part of the
  collaboration discipline. Governance G7 separately owns which uncertainty
  is investigated, decided locally, or returned to the human owner. Agent,
  contributor, README, and operating-guide projections were reconciled; the
  Python 3.11 fixture suite and strict repository check pass. Verification
  remains partial because structural reachability does not prove behavior in a
  real adopting project.
- **2026-08-20 — publication language:** source anchors are published as
  English renderings of the original authorizations. Contracts that cite the
  same statement use the same wording; meaning is unchanged.
- **2026-07-28 — harness proportionality target landed:** distinguished
  controlled learning from delivery implementation, added positive concern
  routing and cross-cutting quality ownership, bounded D6 expansion, and made
  document subtraction and single-source projection part of the discipline.
  Templates and entrypoints now route through the smallest applicable path;
  fixture-backed projection and lifecycle checks implement the stable syntax.
  Real-project effectiveness remains covered by the existing partial
  verification posture.
- **2026-08-28 — cutover to heading-slug identifiers:** the D1–D13 codes were
  retired; headings are now the identifiers per [documentation-harness § invariant-citations](documentation-harness.md#invariant-citations-resolve-to-headings).
  Incoming references across living documents were rewritten to slug links in
  the same change. Earlier entries in this log, completed plans, and dated
  evidence keep the codes as written.
