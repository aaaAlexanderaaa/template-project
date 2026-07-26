---
doc_type: contract
status: current
authority: normative
implementation: implemented
verification_status: enforced
last_reconciled: 2026-07-26
review_due: 2026-10-24
supersedes: []
---

# AI agent execution discipline

## Purpose

This contract extends the repository's contract-first discipline with an
execution profile for autonomous or semi-autonomous coding agents. It governs
work selection, fixture- and test-first implementation, independent design
review, fresh-context evaluation, layered completion, and truthful handling of
missing review authority.

It exists because a durable contract does not by itself prevent one agent from
reusing the same assumptions while designing, implementing, and approving its
own work.

## Scope

In scope:

- material feature, migration, cross-stack, and governance work performed by
  coding agents;
- work selection when no explicit executable task is available;
- independence requirements for high-risk design and final evaluation;
- evidence classes and completion claims.

Out of scope:

- prescribing one agent framework, orchestration API, model, or vendor;
- requiring multiple agents for routine, mechanically bounded changes;
- replacing human authority for unresolved product or safety decisions;
- redefining a project's product or architecture contracts.

## Source anchors

### source[1] — 2026-07-26

> “The reusable template should absorb the multi-perspective design
> review, fresh-context evaluation, fixture-first engineering loop, KR sweep,
> and no-idle work-selection protocol.”

### source[2] — 2026-07-26

> “Do not present same-context analysis as independent review evidence; use a
> truthful blocked or governance-exception state when independent review is not
> available.”

### source[3] — 2026-07-26

> “治理框架不应该帮助开发者定义优先级；它可以识别风险和长期异常，但不应
> 在开发者有自己的想法时替他判断这个想法不对。”

## Vocabulary and risk profiles

- **Routine change:** bounded implementation with an existing contract, no new
  semantics, no migration, and a small failure surface.
- **Material change:** changes behavior, a public contract, a durable state,
  more than one consumer, or an operator workflow.
- **High-risk change:** changes architecture, product semantics, authorization,
  irreversible data behavior, cross-process compatibility, or a high-impact UI
  interaction.
- **Independent review:** a review context that did not produce the proposal or
  implementation and receives the governing contract plus evidence rather than
  the implementer's unfiltered reasoning trace.
- **Governance exception:** an explicit human decision that waives or replaces
  a required review step for a named scope and records the residual risk.

- from: source[1], source[2]

## Normative invariants

### A1 — Risk selects the execution depth

Routine work may use the base development discipline. Material work uses the
phased loop below. High-risk work additionally requires independent
multi-perspective design review and fresh-context holistic evaluation.

The classification and rationale are recorded before implementation. A task is
not made routine merely to avoid review.

- from: source[1]

### A2 — Material work uses a fixture- and test-first loop

The default seven phases are:

1. understand the domain and current authority;
2. prepare realistic, sanitized fixtures or controlled boundaries;
3. land the functional contract and design;
4. encode acceptance behavior in tests and confirm the new behavior fails;
5. implement the smallest coherent end state;
6. run affected regression and integration checks;
7. evaluate the result holistically from outside the implementation context.

If a phase is not applicable, the plan records why. Skipping a phase silently
is not allowed.

- from: source[1]

### A3 — High-risk design uses independent lenses

Before implementation, reviewers evaluate the same contract and baseline
evidence through at least these lenses:

- system and contract consistency;
- user or operator experience;
- engineering cost, maintenance, and extensibility.

A separate synthesis identifies agreement, disagreement, residual risk, and
decisions requiring human authority. Projects may add security, privacy,
reliability, or domain-specific lenses.

- from: source[1]

### A4 — Independence is evidence, not a label

The implementer cannot manufacture independence by writing several sections in
the same context. Review records identify the verifier context, inputs,
limitations, and whether independence was required and achieved.

When the required independent context is unavailable, the work remains
`blocked` or `verifying` unless a human grants a documented governance
exception. Passing technical checks does not substitute for missing governance
evidence.

- from: source[2]

### A5 — Work selection has no silent idle state or invented priority

When no explicit executable task exists, an autonomous agent:

1. resumes truthful in-progress work that is already authorized;
2. diagnoses blocked work without treating one blocker as project-wide;
3. consumes the highest-priority ready work from the declared portfolio or
   human owner;
4. if no task is ready, reviews the active portfolio read-only for an uncovered
   user outcome, boundary case, quality gap, or missing regression;
5. records candidate work with facts, risk, dependencies, and evidence limits;
6. when no authoritative priority exists, presents candidates as
   recommendations and requests a human decision before non-trivial
   implementation;
7. verifies completed task groups against their parent acceptance outcome;
8. reports completion only when no roadmap, release-gate, or reconciliation
   work remains within the claimed scope.

The declared portfolio or human owner owns priorities. Work discovery and risk
analysis do not grant the agent authority to rank or execute newly discovered
product work. The output classes and allowed blocker conditions are defined by
`governance-decision-boundary.md`.

- from: source[1], source[3]

### A6 — Completion is layered

- A task is complete when its acceptance evidence and affected regression pass.
- A task group or key result is complete when its integrated outcome is
  independently checked where required.
- An objective is complete when all outcomes pass, holistic evaluation closes,
  and contracts, plans, issues, guides, and evidence have final lifecycle
  states.
- A release gate is complete only when every gate claim has its own reproducible
  evidence.

Lower-level completion does not imply higher-level completion.

- from: source[1], source[2]

### A7 — Evidence classes remain explicit

Verification records name which class they provide, such as:

- unit or class-level guard;
- projection or seeded integration fixture;
- source-shaped or protocol-shaped fixture;
- generated scale evidence;
- built-entrypoint or packaged-artifact evidence;
- real process, HTTP, browser, device, or service evidence;
- operator-started manual diary;
- reviewed real-world sample or archive.

Each report states what it does not prove. Evidence classes may complement one
another but do not silently replace one another.

- from: source[1], source[2]

## Required records

Material agent work records:

- the governing contract and risk profile;
- the priority source or explicit human authorization for the selected work;
- a cold-start-capable implementation plan;
- fixture or controlled-boundary strategy;
- acceptance tests and their pre-implementation result;
- commands, environment, and evidence class for verification;
- independent review or the exact blocked/exception state;
- final contract, plan, issue, and evidence lifecycle updates.

## Forbidden behaviors

- Do not call same-context notes independent reviews.
- Do not mark an objective complete because its implementation tasks are done.
- Do not treat unavailable user-started services or real data as automatically
  passing.
- Do not create untracked corrective implementation from a portfolio review.
- Do not convert an agent-authored recommendation into portfolio priority.
- Do not use a heavyweight review ritual for routine work without a recorded
  risk reason.
- Do not let temporary checkpoints become the undocumented end state.

## Acceptance evidence

This contract is implemented when:

- reusable templates exist for agent execution plans, independent review,
  holistic evaluation, and evidence-preserving data work;
- the documentation harness validates those templates as first-class
  deliverables;
- fixture tests prove missing or malformed required templates fail;
- repository guidance routes agent-driven material changes through this
  contract;
- the correct Python runtime has a canonical, actionable verification path.

Verified on 2026-07-26:

- `uv run --python 3.11 python -m unittest discover -s tests -p 'test_*.py'`
  passed all 36 fixture tests, including missing agent/adoption templates,
  missing-section, and unsupported-runtime cases;
- `uv run --python 3.11 python scripts/check_docs.py` passed against 12 canonical
  documents and 14 required templates;
- `/usr/bin/python3 scripts/check_docs.py --help` under Python 3.9 exited with
  the actionable Python 3.11+ preflight and no traceback.

## Promise register

- promise[independent-adoption-review]: due=2026-10-24; status=open; owner=template-maintainer; description=obtain an independent adoption review after the first real product uses the agent execution profile

## Reconciliation log

- **2026-07-26 — contract created:** combined the template's contract-first
  governance with a risk-based AI execution profile derived from a concrete
  agent-driven product workflow.
- **2026-07-26 — implementation enforced:** registered four reusable templates,
  routed contributor entrypoints through the profile, and added fixture-backed
  template and Python-runtime checks. The real-project independent adoption
  review remains an explicit open promise rather than a completion blocker for
  the reusable harness itself.
- **2026-07-26 — priority authority reconciled:** clarified that the no-idle
  protocol consumes human-owned priority and may discover and recommend work,
  but cannot manufacture product direction or silently authorize execution.
