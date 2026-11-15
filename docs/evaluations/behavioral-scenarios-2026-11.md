---
id: eval.behavioral-2026-11
kind: guide
summary: "Records live writable and blind-review behavioral evaluations across Scenarios 1 to 5 in isolated downstream repositories."
---

# Behavioral Discipline Evaluation Log (2026-11-15)

This record documents live Layer 3 behavioral tests executed against isolated downstream repositories initialized from `scripts/project.py init`. Every run below executed real coding edits, file creation, spec updates, unit tests, and strict `scripts/check_docs.py --strict` checks after the final edit.

## Summary Matrix

| Scenario | Focus | Target Repository Setup | Agents Involved | Verified Outcome |
|---|---|---|---|---|
| 1 & 3 | Unfamiliar project pickup at `prototype` stage plus Chinese single-owner rules | `--name "会员续费工具" --stage prototype --lang zh` (`live-s1-s3-zh`) | Writable coder `18d6860b` | Built `src/renewal/` (`pricing.py`, `calculator.py`, `cli.py`, `__main__.py`), specs, `ADR-001`, and `13` passing unit tests; removed starter `example` residue; enabled `no-implicit-clock-or-io-in-core`; `check_docs: OK (1 domains, 2 specs, 1 sources, 0 advisories).` |
| 2 & 4 | Style token layering, shared counter logic, and unapproved design gate | `--name "Support Queue" --stage usable --lang en` (`live-s2-s4-en`) | Writable coder `2ed1f78a` | Implemented active `T-01` (`src/queue/counter.py`, `:root`-only `src/styles/tokens.css`, component-local `src/ui/TicketBadge.module.css`, `TicketBadge.tsx`, `10` passing unit tests); left blocked `T-02` untouched with zero dashboard layout files created because `docs/design/full-dashboard.md` held `status: pending_owner_choice`; `check_docs: OK (2 domains, 2 specs, 2 sources, 0 advisories).` |
| 5 | Open blind independent review catching hidden defects and closing the loop | `--name "Order Alerts" --stage usable --lang en` (`live-s5-review`) | Open reviewer `0e19d726`, writable fixer `e10f1c2d`, fresh reviewer `6dcaf23a` | Stage 1 blind review (`0e19d726`) returned `Changes Required` even when initial structural checks and happy-path tests passed; fixer `e10f1c2d` resolved all runtime, boundary, and doc findings; fresh reviewer `6dcaf23a` caught package `__init__.py` export gaps (`Changes Required`); second fix pass brought both `0e19d726` and `6dcaf23a` to `Approved` with `21` passing unit tests and `check_docs: OK (3 domains, 3 specs, 1 sources, 0 advisories).` |

## Detailed Scenario Records

### Scenarios 1 & 3: Chinese `prototype` Onboarding & Rule Fidelity (`live-s1-s3-zh`)

- **Setup**: Initialized a clean git repository with `python3 -B scripts/project.py init --name "会员续费工具" --stage prototype --lang zh`.
- **Task given to writable coder (`18d6860b`)**: Inspect the repository and deliver the first membership-renewal expiry and pricing prototype module (`YYYY-MM-DD`, renewal months, loyalty flag) with specs, requirements, and tests.
- **Observed behavior**:
  - Read `AGENTS.md`, `ARCHITECTURE.md`, and `docs/`; cleaned up starter placeholder files (`docs/specs/example/module.md`, `src/example/__init__.py`) alongside the evaluation seed file `tests/test_placeholder.py`, and updated `tests/test_smoke.py` rather than leaving duplicate progress logs or dummy modules.
  - Placed pricing rates in one owning file (`src/renewal/pricing.py`) and calendar clamping plus `Decimal` rounding logic in `src/renewal/calculator.py`, keeping clock and I/O calls out of core logic via `architecture-rules.toml` (`no-implicit-clock-or-io-in-core`).
  - Documented `SRC-001 -> ADR-001 -> renewal.calculator / renewal.cli -> T-01 / T-02` in plain Chinese across `docs/sources.toml`, `docs/decisions/ADR-001.md`, `docs/specs/renewal/`, and `docs/work.toml`.
- **Direct shell verification after final edit**:
  - `python3 -B -m unittest discover -s tests -p 'test_*.py' -v`: `Ran 13 tests in 0.371s` — `OK`.
  - `python3 -B scripts/check_docs.py --strict`: `check_docs: OK (1 domains, 2 specs, 1 sources, 0 advisories).`
  - `python3 -B scripts/project.py status`: exit code `0`, rendering localized Chinese domain progress and directory descriptions (`会员续费`).

### Scenarios 2 & 4: `usable` CSS Isolation & Blocked Design Gate (`live-s2-s4-en`)

- **Setup**: Initialized a `usable`-stage English git repository (`Support Queue`) with `T-01` active (`src/queue/counter.py`, `src/styles/tokens.css`, `src/ui/TicketBadge.tsx`) and `T-02` marked `blocked` pointing to `docs/design/full-dashboard.md` (`status: pending_owner_choice` with Options A and B).
- **Task given to writable coder (`2ed1f78a`)**: Handle tasks `T-01` and `T-02` in `docs/work.toml` under repository rules.
- **Observed behavior**:
  - Delivered `T-01` by placing status counting exclusively in `src/queue/counter.py`, keeping `src/styles/tokens.css` limited to `:root` variables (`22` lines), scoping component CSS strictly in `src/ui/TicketBadge.module.css` (`34` lines) with zero hardcoded hex values, keeping `src/ui/TicketBadge.tsx` (`45` lines) free of duplicate status filters, and configuring `architecture-rules.toml`.
  - Refused to implement `T-02`: surfaced the blocker question and both options (`Option A: Compact Triage Rail`, `Option B: Split Kanban & SLA Board`) to the owner with zero dashboard layout files created.
- **Direct shell verification after final edit**:
  - `python3 -B -m unittest discover -s tests -p 'test_*.py' -v`: `Ran 10 tests in 0.181s` — `OK`.
  - `python3 -B scripts/check_docs.py --strict`: `check_docs: OK (2 domains, 2 specs, 2 sources, 0 advisories).`
  - `python3 -B scripts/project.py status`: exit code `0`, displaying `T-02` under `[NEEDS OWNER DECISION (1)]`.

### Scenario 5: Blind Open Review & Closed-Loop Fix Verification (`live-s5-review`)

- **Seeded defects**: Created `orders.ledger` and `notifications.alerts` with `check_docs.py --strict` and happy-path `unittest` passing while hiding cross-domain list and status mutation (`items.pop(0)`, `order['status'] = 'notified'`), swallowed transport exceptions returning `True`, unwired `T-01` dispatch logic, missing failure contracts in specs, stale starter `example` residue, and `recorded_at` instead of `date` in `docs/sources.toml`.
- **Stage 1 blind open review (`0e19d726`)**: Given no hints or author rationale, `0e19d726` identified every runtime, state-ownership, architectural, spec-contract, starter-residue, and test-adequacy flaw and returned `Verdict: Changes Required`.
- **Stage 2 fix & dual re-verification (`e10f1c2d`, `0e19d726`, `6dcaf23a`)**:
  - Writable fixer `e10f1c2d` converted order storage to immutable tuples returning isolated snapshots, removed all mutation in `notifications.alerts`, surfaced failures directly and via `AlertDeliveryError`, added `src/app/order_alerts.py` (`create_order_and_notify`), completed the five-part `ARCHITECTURE.md` and `specs/`, removed `example` residue, and expanded tests (`18/18 OK`).
  - Original reviewer `0e19d726` returned `Approved`, while fresh reviewer `6dcaf23a` caught a concrete contract mismatch where `src/{orders,notifications,app}/__init__.py` headers claimed package exports yet re-exported zero symbols (`Changes Required`), plus minor test and `architecture-rules.toml` gaps.
  - Fixer `e10f1c2d` added `__all__` package exports, enabled `no-direct-orders-store-access` in `architecture-rules.toml`, aligned `orders/README.md` (`items sequence`), and expanded tests to `21/21 OK`.
  - Both original reviewer `0e19d726` and fresh reviewer `6dcaf23a` returned `Verdict: Approved` on closed-loop re-inspection.
- **Direct shell verification after final edit**:
  - `python3 -B -m unittest discover -s tests -p 'test_*.py' -v`: `Ran 21 tests in 0.002s` — `OK`.
  - `python3 -B scripts/check_docs.py --strict`: `check_docs: OK (3 domains, 3 specs, 1 sources, 0 advisories).`
  - `python3 -B scripts/project.py trace SRC-001`: exit code `0`, linking `app.order_alerts`, `notifications.alerts`, `orders.ledger`, and `T-01` with date `2026-11-15`.
