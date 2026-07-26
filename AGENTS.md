# Repository working agreement

This repository uses contract-first development. These instructions apply to
human contributors and automated coding agents.

## Read order

Before changing code or behavior, read in this order:

1. `ARCHITECTURE.md` for structural ownership and dependency direction.
2. `docs/README.md` for document authority and lifecycle.
3. The relevant `status: current` contract under `docs/contracts/`.
4. For UI work, the relevant current surface contract under `docs/design/`.
5. The active implementation plan under `docs/plans/`, if one exists.

Do not infer authority from recency, filename, or document length.
`docs-policy.toml` owns mechanical lifecycle defaults;
`architecture-rules.toml` owns the portable baseline fitness declarations.

## Contract-first gate

- Do not implement a material behavior change without a landed contract.
- If the contract is missing, draft and confirm it first.
- If conversation, code, tests, and contract disagree, stop and surface the
  conflict. Reconcile before editing dependent code.
- Plans describe execution; they do not override current contracts.
- Code comments and commit messages do not replace a normative contract.

The full discipline lives in
`docs/contracts/development-discipline.md`.

## Working safely

- Investigate read-only before asking questions the repository can answer.
- Preserve unrelated and pre-existing work in a dirty worktree.
- Do not perform destructive operations unless the exact target and authority
  are clear.
- Keep changes inside the requested scope; do not infer permission for a
  materially different migration or cleanup.
- A diagnosis request authorizes investigation and explanation, not an
  unrequested implementation.

## Planning and implementation

- Describe one coherent end state. Dependency order is not permission to leave
  temporary architecture behind indefinitely.
- Identify owner, public contract, states, triggers, failure behavior,
  non-goals, risks, and acceptance evidence before implementation.
- Name the defect category before fixing a bug.
- Add a class-level guard that catches sibling variants of the same mechanism.
- Prefer cohesion and a single reason for change over arbitrary file-size
  targets. Split modules that mix bounded contexts.

## Frontend work

- Preserve dated stakeholder language in a raw layer and translate it into
  states, layout, size, interaction, accessibility, and responsive behavior.
- Enumerate relevant reachable states instead of checking one sample.
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
- When changing the documentation harness or templates, run both the fixture
  suite and the repository check with Python 3.11 or newer.
