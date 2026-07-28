---
doc_type: contract
status: current
authority: normative
contract_role: governance
implementation: implemented
verification_status: partial
last_reconciled: 2026-07-28
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

> “赋能而不是阻碍，让 agent 可以清楚自己什么该做和不该做，而不是因为未能
> 理解用户的需求和场景时刻担心犯错。”

### source[2] — 2026-07-28

> “避免只是膨胀……长期治理应该考虑存量管理，考虑文档的退役和沉淀/总结，
> 而不只是增量……文档耦合……很容易出现一个事情在多个文档里出现。”

## Core invariants

### D1 — Contract before material delivery, evidence before certainty

Do not deliver a material feature or behavior change until its contract exists
on disk. The contract must name the behavior, relevant states and triggers,
ownership boundary, failure behavior, non-goals, and acceptance evidence.

When a material fact cannot be learned through read-only investigation, a
bounded experiment may precede the delivery contract. The experiment is
evidence, not product implementation. Before it runs, route the experiment's
own actions through D8. Every activated concern uses an existing normative
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

### D2 — One owner for every invariant

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

### D3 — Coherent end state

Design migrations around one complete end state. Real dependency order may
produce multiple execution checkpoints and explicit transitional states, but
those states have an owner, entry and exit conditions, compatibility behavior,
observation, and removal or promotion criteria. They must not become an
intentionally half-migrated architecture, indefinite compatibility layer, or
placeholder that is merely promised to be corrected later.

If a coherent end state cannot yet be described or verified, do not start the
delivery migration. Use the bounded experiment path in D1 to learn the missing
facts without presenting the experiment as the destination.

### D4 — Outcomes before means

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
are guaranteed; they are not the outcome themselves.

### D5 — Environment over memory

A recurring rule needs an enforcement surface outside human memory. Depending
on the rule, use types, schema validation, static checks, unit tests,
architecture tests, integration tests, runtime assertions, or reproducible
probes.

Prose explains intent and trade-offs. Mechanical guards stop the same class of
mistake from recurring.

### D6 — Fix the category, not only the symptom

Before fixing a defect, name its category and root mechanism. When that
mechanism has repeatable sibling variants, the change includes a class-level
guard capable of catching at least one plausible variant that was not in the
original report.

A symptom-only patch is incomplete when the same mechanism can fail elsewhere.
When evidence shows no repeatable sibling mechanism, a stable guard is not
possible, or the guard would cost more than the bounded risk warrants, record
that fact and keep the change local. D6 is not permission to expand an
authorized fix into an unbounded cleanup.

### D7 — Preserve decisions and evidence

Requirements, translations, implementation plans, issues, and evidence have
different authority. Do not overwrite one with another. Superseded material
keeps an explicit replacement link so later contributors can reconstruct why a
decision changed.

### D8 — Activate concerns instead of expanding ceremony

Governance depth follows the change's observable traits, not the size of its
template or the caution of its implementer. A concern that is not triggered
creates no document, section-filling exercise, review lens, or test obligation.
For every activated concern, an applicable current or target contract is the
sole owner of its boundary, failure policy, and escalation or exception policy.
A plan records only the selected concern, owner link, execution steps, and
proportionate evidence.

If no normative owner exists, material delivery waits for a contract to
establish one. A D1 experiment may proceed only through safety boundaries that
already exist for its own activated actions; it cannot use a plan or scratch
record to invent a temporary quality boundary.

The concern routing table below is the normative owner. Agent instructions,
guides, and templates may link to or project it but must not define competing
trigger semantics.

| Change trait | Activated concern | Minimum questions |
|---|---|---|
| Public interface, event, schema, or consumer-visible meaning | Compatibility | Version, consumers, cutover, deprecation, rollback |
| Durable state, migration, concurrency, or replay | State integrity | Atomicity, idempotency, ordering, recovery, manual intervention |
| Permission, identity, untrusted input, sensitive data, or cross-tenant access | Security and privacy | Trust boundary, least privilege, abuse/failure case, audit, retention |
| Hot path, scale assumption, resource model, or material cost change | Performance, capacity, and cost | Load scenario, response/budget, saturation, backpressure or degradation |
| Availability dependency, timeout, retry, failover, degradation, recovery behavior, or operator workflow | Reliability and operations | Service objective, dependency failure, observability, alert/rollback trigger |
| External package, generated artifact, compiler, build or delivery path | Dependency and build integrity | Owner, provenance, reproducibility, compatibility, unavailable-dependency behavior |
| User-visible surface or interaction | Experience | Reachable states, accessibility, responsive/input behavior, localization where relevant |
| Assumption verifiable only after release | Production learning | Signal, observation window, decision threshold, rollback/reconciliation owner |

- from: source[1]

### D9 — Govern document decisions, not document volume

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

## Change workflow

Every material delivery change follows this order:

1. **Classify and route.** Establish the decision envelope, evidence state, risk
   profile, and concerns activated by D8.
2. **Investigate.** Inspect current contracts, code, state, tests, and existing
   evidence before asking questions that the repository can answer. Use a D1
   bounded experiment only when read-only evidence cannot answer a material fact.
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
- Localization, text expansion, locale, time-zone, and input-method behavior
  when the surface or its data activates those concerns.
- The style layer, value tiers, and published override surface the change
  consumes, plus any value it must define locally and why.

### Style ownership and layering

Style decay is a dependency-direction and precedence problem that happens to
render. The rules below are the frontend instance of D2; they do not create a
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
  and production-learning boundaries from D8.

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
7. Carry every activated D8 concern through its authoritative owner rather than
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

- **2026-07-28 — harness proportionality target landed:** distinguished
  controlled learning from delivery implementation, added positive concern
  routing and cross-cutting quality ownership, bounded D6 expansion, and made
  document subtraction and single-source projection part of the discipline.
  Templates and entrypoints now route through the smallest applicable path;
  fixture-backed projection and lifecycle checks implement the stable syntax.
  Real-project effectiveness remains covered by the existing partial
  verification posture.
