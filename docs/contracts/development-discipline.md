---
doc_type: contract
status: current
authority: normative
contract_role: governance
implementation: implemented
verification_status: partial
last_reconciled: 2026-07-26
supersedes: []
---

# Development and collaboration discipline

## Purpose

This contract defines how work is understood, specified, implemented,
verified, and handed off. It is domain-neutral: it governs collaboration and
change quality, not any particular product, framework, runtime, or deployment.

The objective is to move project intent out of chat history and individual
memory into durable, reviewable contracts and reproducible evidence.

## Core invariants

### D1 — Contract before material implementation

Do not implement a material feature or behavior change until its contract
exists on disk. The contract must name the behavior, relevant states and
triggers, ownership boundary, failure behavior, non-goals, and acceptance
evidence.

Routine corrections and mechanically bounded refactors may rely on an existing
current contract when they introduce no new semantics, state, boundary, or
failure behavior. They do not require a standalone contract solely to satisfy a
ritual. If no applicable contract exists for a material change, write one
first. If current discussion conflicts with a landed contract, stop dependent
implementation, record the conflict, reconcile it, and only then continue.

Comments, tickets, commit messages, and conversation summaries are supporting
context; they are not substitutes for the normative contract.

### D2 — One owner for every invariant

Every state transition, data rule, API shape, layout rule, and operational
decision has one authoritative owner. Consumers may use the owner's public
contract but must not silently reproduce or override its private rules.

Cross-layer behavior must identify:

- the authoritative state owner;
- the public interface used by consumers;
- what consumers may display or configure;
- what consumers must never infer independently.

### D3 — Coherent end state

Design migrations around one complete end state. Real dependency order may
produce multiple execution checkpoints, but those checkpoints must not create
an intentionally half-migrated architecture, indefinite compatibility layer,
or placeholder that is promised to be corrected later.

If a coherent end state cannot yet be described or verified, do not start the
migration.

### D4 — Outcomes before means

Define success in terms of observable outcomes before listing implementation
or test mechanics. The default quality outcomes are:

1. functionality is correct;
2. presentation is correct;
3. interaction is correct;
4. the result follows the product's design and domain logic;
5. failure and recovery behavior are understandable.

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

Before fixing a defect, name its category and root mechanism. The change must
include a class-level guard capable of catching at least one plausible sibling
variant that was not in the original report.

A symptom-only patch is incomplete when the same mechanism can fail elsewhere.

### D7 — Preserve decisions and evidence

Requirements, translations, implementation plans, issues, and evidence have
different authority. Do not overwrite one with another. Superseded material
keeps an explicit replacement link so later contributors can reconstruct why a
decision changed.

## Change workflow

Every material change follows this order:

1. **Investigate read-only.** Inspect current contracts, code, state, tests,
   and existing evidence before asking questions that the repository can answer.
2. **Resolve authority.** Identify the current normative document and the code
   or service that owns the behavior.
3. **Reconcile intent.** Record ambiguity, contradiction, or changed
   requirements. Do not silently choose between conflicting sources.
4. **Land or update the contract.** Define states, triggers, boundaries,
   failure behavior, non-goals, and acceptance outcomes.
5. **Write the execution plan.** Describe one coherent end state, dependency
   order, affected files or surfaces, risks, and verification.
6. **Implement with guards.** Preserve unrelated work and add the smallest
   class-level enforcement surface that protects the intended behavior.
7. **Verify proportionally to risk.** Cover the changed unit, its integration
   boundary, affected user-visible states, and failure/recovery paths.
8. **Close the loop.** Update implementation and verification status, attach
   durable evidence, resolve or supersede the plan, and update issue state.

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
the relevant mechanical guards pass; and the production-like surface has been
verified.

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

## Documentation lifecycle

Documents must declare their type, status, authority, and reconciliation date.
Contracts additionally declare implementation and verification status.

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
