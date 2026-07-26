# Architecture

> Template status: fill this document before adding product implementation.
> Replace every bracketed prompt. Once adopted, this file is the structural
> authority and must describe the current system rather than an aspirational
> mixture of current and future states.

## 1. System purpose

- Product/system: `[name]`
- Primary users: `[users]`
- Problem boundary: `[what this system owns]`
- Explicit non-goals: `[what it does not own]`

## 2. Bounded contexts and layers

| Context or layer | Owns | Public interface | May depend on | Must not know |
|---|---|---|---|---|
| `[name]` | `[state/behavior]` | `[API/events/types]` | `[owners]` | `[private semantics]` |

State the dependency direction explicitly. A lower-level or generic layer must
not acquire product-specific knowledge through convenience imports, shared
storage reads, or copied status vocabularies.

## 3. Ownership map

| Invariant | Authoritative owner | Consumers | Enforcement surface |
|---|---|---|---|
| `[state transition or rule]` | `[module/service]` | `[clients]` | `[type/test/runtime guard]` |

Every material invariant must have one owner. Consumers may render or compose
the public contract but may not independently redefine it.

## 4. Public contracts

Document interfaces crossing module, service, process, persistence, or team
boundaries:

- version and compatibility policy;
- request/response/event shapes;
- ordering and duplicate behavior;
- validation and error taxonomy;
- authorization and capability boundary;
- deprecation and removal policy.

Link each interface to its normative contract under `docs/contracts/`.

## 5. State and lifecycle

For each durable entity or long-running operation, define:

- identity and state machine;
- legal and illegal transitions;
- persistence owner;
- transaction or atomicity boundary;
- idempotency and concurrency behavior;
- timeout, retry, cancellation, recovery, and manual-intervention states;
- archival and retention behavior.

## 6. Frontend boundary

If the project has a frontend, define:

- which backend contracts are authoritative;
- what state is frontend-owned versus merely projected;
- component or design-system ownership;
- routing and extension points;
- accessibility, browser, input, and responsive support policy.

Per-surface behavior belongs under `docs/design/`, not in this structural map.

## 7. Runtime and deployment

- Runtime topology: `[processes/services/jobs]`
- Configuration sources and precedence: `[sources]`
- Secret ownership: `[mechanism]`
- Health and observability: `[logs/metrics/traces/audit]`
- Deployment and rollback unit: `[unit]`
- Data migration and compatibility window: `[policy]`
- Recovery objectives: `[RTO/RPO or qualitative contract]`

## 8. Hard and soft boundaries

Classify extension points:

- **Hard:** state identity, integrity, protocol shape, geometry, accessibility,
  authorization, or dependency direction. Consumers cannot override it.
- **Soft:** presentation or configuration explicitly exposed through a finite
  public API.
- **Family/group:** a declared owner provides named variants while protecting
  shared behavior.

Anything not explicitly public is private to its owner.

## 9. Structural fitness tests

List the mechanical checks that prove the architecture remains true:

- `[forbidden dependency/import check]`
- `[public contract/schema compatibility check]`
- `[state/recovery lifecycle test]`
- `[permission/capability isolation test]`
- `[frontend ownership or geometry guard]`

## 10. Reconciliation log

Record dated structural changes, superseded decisions, and links to the
contracts and plans that implemented them.
