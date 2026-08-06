# Repository working agreement

This repository uses contract-first development. These instructions apply to
human contributors and automated coding agents.

## Read order

Before changing code or behavior, read in this order:

1. `ARCHITECTURE.md` for structural ownership and dependency direction.
2. `docs/README.md` for document authority and lifecycle.
3. The relevant `status: current` contract and any applicable accepted
   `status: target` contract under `docs/contracts/`.
4. For UI work, the relevant current and accepted target surface contracts
   under `docs/design/`.
5. The active implementation plan under `docs/plans/`, if one exists.
6. For material agent-driven work, the risk and review requirements in
   `docs/contracts/agent-execution-discipline.md`.

For greenfield or brownfield adoption, read
`docs/contracts/project-adoption.md` and `docs/guides/onboarding.md` before
rewriting existing authority or enabling project-wide gates.

Do not infer authority from recency, filename, or document length.
`docs-policy.toml` owns mechanical lifecycle defaults;
`architecture-rules.toml` owns the portable baseline fitness declarations.

Governance depth is declared, not assumed. `[adoption].stage`,
`[adoption].source_roots`, `[adoption].managed_paths`, and
`[templates].profile` in `docs-policy.toml` state which scope is governed and
how strictly. Read them before reporting a gap: at an early stage the checker
reports adoption work without blocking, and that is the intended state, not a
finding. Change the declared scope by proposing it to the owner, never by
weakening a rule to make a check pass.

## Contract-first gate

- Do not deliver a material behavior change without a landed contract.
- When a material technical fact is unknown, use the controlled experiment
  path in development D1; the experiment is disposable evidence, not delivery.
- Routine work may consume an applicable current contract without creating a
  standalone contract or plan.
- If a material delivery contract is missing, draft and confirm it first.
- If conversation, code, tests, and contract disagree, stop and surface the
  conflict. Reconcile before editing dependent code.
- Plans describe execution; they do not override current contracts.
- Code comments and commit messages do not replace a normative contract.

The full discipline lives in
`docs/contracts/development-discipline.md`.

## Governance decision boundary

- Product direction, priority, trade-offs, and risk acceptance remain with the
  declared human owner. The framework supplies decision evidence; it does not
  replace that authority.
- Classify material governance output as `fact`, `risk`, `recommendation`,
  `human_decision_required`, or `execution_blocker`.
- Use `execution_blocker` only for the bounded conflict, authorization,
  configuration/dependency, adopted evidence/review, and coherent-end-state
  conditions in `docs/contracts/governance-decision-boundary.md`.
- A blocker pauses one execution path, not the product idea. Name its evidence,
  exact scope, recovery options, and available human decision.
- When priority is missing, present candidates and request direction; do not
  silently promote an agent recommendation into project priority.
- Inside an authorized outcome, proceed with locally reversible engineering
  choices in the G6 decision envelope. Investigate technical uncertainty before
  escalating it as a product or risk decision.

## Working safely

- Investigate read-only before asking questions the repository can answer.
- Preserve unrelated and pre-existing work in a dirty worktree.
- Do not perform destructive operations unless the exact target and authority
  are clear.
- Keep changes inside the requested scope; do not infer permission for a
  materially different migration or cleanup.
- A diagnosis request authorizes investigation and explanation, not an
  unrequested implementation.

## Inquiry and collaboration

Follow development D10-D12 and governance G7 rather than guessing or seeking
approval indiscriminately:

- Research unfamiliar terms, named references, publications, and other
  checkable external facts with available network or retrieval tools; prefer
  primary and official sources, and distinguish sourced fact from inference.
- If a tool is unavailable, identify the capability it provided and try a
  semantics- and evidence-preserving fallback before reporting a blocker. Do
  not silently weaken the claim or switch product behavior.
- Route uncertainty by kind: investigate facts, make and verify locally
  reversible engineering choices, and present bounded options when product
  intent, material trade-offs, expensive-to-reverse preferences, authority, or
  risk acceptance belong to the user.
- Answer the explicit question and point out an evidence-backed unasked issue
  when it is materially more consequential to the user's goal. Explain the
  causal connection without expanding implementation scope silently.
- Judge analytical depth by whether the causal mechanism, conditions,
  boundaries, and distinguishing evidence are clear, not by the number of
  headings or abstraction layers.

## Planning and implementation

- Describe one coherent end state. Dependency order is not permission to leave
  temporary architecture behind indefinitely.
- For material delivery, identify owner, public contract, states, triggers,
  failure behavior, non-goals, risks, and acceptance evidence first.
- Name the defect category before fixing a bug.
- Add a sibling-variant guard when the root mechanism is repeatable and the
  guard is proportionate to the bounded risk; otherwise record why the fix stays
  local.
- Prefer cohesion and a single reason for change over arbitrary file-size
  targets. Split modules that mix bounded contexts.

## Agent execution profile

Choose the smallest route in
`docs/contracts/agent-execution-discipline.md` A8:

- **Routine:** use existing authority, make the bounded reversible change, and
  run focused guards without a new plan.
- **Controlled experiment:** when read-only investigation cannot answer a
  technical fact, use development D1's disposable, contained evidence path.
- **Material delivery:** land the contract, link only D8-activated concern
  owners, and use the seven-phase fixture- and test-first loop.
- **High-risk delivery:** add A3/A4 independent design review and fresh-context
  completion evaluation to the material route.

Record the rationale for material/high-risk work; do not downgrade risk to
bypass a missing reviewer. If required independent context is unavailable, keep
only the affected completion layer open unless a human records a scoped
exception. When no named task is executable, follow A5 and consume human-owned
portfolio priority rather than inventing it.

## Frontend work

- Preserve dated stakeholder language in a raw layer and translate it into
  states, layout, size, interaction, style, accessibility, and responsive
  behavior.
- Enumerate relevant reachable states instead of checking one sample.
- Consume the declared style layer and value tiers; do not introduce a second
  source of visual truth. A value restated where it is used has no owner.
- Change another unit's appearance only through the surface that unit
  published. Being able to select something is not permission to style it.
- When the shared layer publishes no suitable value, record the exception with
  an owner and a removal condition instead of overriding privately.
- For layout work, combine perceptual review with rendered structural evidence.
- Check repeated instances, both axes, intermediate responsive ranges, and
  actual usability.
- Use an independent verifier for high-risk visual or interaction changes.

## Backend and service work

- Keep domain truth and mutation authorization with one declared owner.
- Version interfaces that cross module or process boundaries.
- Specify invalid transitions, idempotency, concurrency, persistence,
  timeouts, retry eligibility, recovery, observability, and permissions.
- Fail loudly on invalid configuration or unavailable dependencies.
- Test lifecycle and failure behavior with controlled boundaries.

## Cross-stack work

- Define the shared state and interface contract before producer or consumer
  code changes.
- Backend owns domain truth; frontend owns its user-visible projection.
- Do not duplicate hidden business rules in the client.
- Cut over all required participants under one explicit compatibility decision.

## Verification and handoff

- Lead with observable outcomes: functionality, presentation, interaction,
  design/domain logic, and failure/recovery behavior.
- Run checks in proportion to the affected risk and boundary surface.
- Record durable evidence for durable claims; keep scratch artifacts in `tmp/`.
- Update contract implementation/verification status, plan status, issue
  status, and supersession links before declaring work complete.
- State which layer is complete: task, task group/key result, objective, or
  release gate. Completion at one layer does not close the next.
- When changing the documentation harness or templates, run both the fixture
  suite and the repository check with Python 3.11 or newer.
