---
id: domain.graph-engine
kind: domain-spec
name: "Document & Code Graph Checker"
stage: stable
summary: "Subordinate repository checker that parses specs, inventories, and TOML ledgers; scans static imports and Git history; and verifies structural and language rules without hardcoding any host domain."
promise: "Any repository using this discipline gets deterministic verification of links, file ownership, cross-module imports, line budgets, plain-language prose, and quote lineage without leaking template-project domain IDs."
---

# Document & Code Graph Checker

> [!NOTE]
> `graph-engine` is a **subordinate verification helper**, not the core product of `template-project`. Its job is mechanical validation and rule loading; qualitative design and architecture review stay with human owners and independent reviewers.

## 1. Execution Pipeline (Files & Code -> Graph -> Checks)

```mermaid
flowchart LR
  Files["Specs, Docs, sources.toml & work.toml"] --> Loader["loader.py + doc_inventory.py"]
  Code["Source Files + Git Log"] --> Scanners["import_scanner.py + git_telemetry.py"]
  Loader --> Validator["validator.py / check_docs.py"]
  Scanners --> Validator
  Validator -->|Error or Advisory| Report["Terminal Findings + Diff Context"]
```

## 2. Actual Module Layering & Explicit Boundaries

Modules under `scripts/` obey strict one-way dependencies (`Base` owns pure data types; `Core` indexes and validates; `Pack` serializes and writes back; `CLI` exposes user commands):

```mermaid
flowchart TD
  CLI["CLI Entrypoints (project.py, check_docs.py, read_rules.py)"] --> Pack["context_pack, briefing_pack, server & toml_writer"]
  Pack --> Core["Core Indexing & Validation (loader, validator, prose_checks, doc_inventory, import_scanner, git_telemetry)"]
  Core --> Base["Data Models, Parsers & Rule Reader (model.py, frontmatter.py, rule_reading.py)"]
  CLI --> Core
```

## 3. State Ownership & Forbidden Couplings

| Constraint or Forbidden Coupling | Rule Summary | Enforced By |
|---|---|---|
| Hardcoded `template-project` domains inside `doc_inventory.py` | Infer directory domain dynamically from target repo specs; keep shared multi-domain directories neutral | `tests/test_discipline_transfer_and_consistency.py` |
| Static AST `import` graphs presented as system architecture | Show module dependencies as structural coupling only; document runtime logic and state separately | `docs/contracts/architecture-and-modularity.md` |
| `validator.py` or `loader.py` mutating tracked project docs | Read-only checks report errors and exit status without altering `sources.toml` or specs | `validator.py` read-only check path |
| `Core` importing `briefing_pack` or `server` | Headless `check_docs.py` runs with zero HTTP server or UI dependencies | Module `depends_on` graph |

## 4. Entrypoints & Fitness Checks

- **CLI entrypoints**: `python3 scripts/check_docs.py [--strict]`, `python3 scripts/read_rules.py {list,prepare,read,overview,onboard}`, and `python3 scripts/project.py {status,context,trace,check}`.
- **Fitness checks**: `tests/test_ssot_and_check_docs.py`, `tests/test_read_rules_and_onboard.py`, and `tests/test_discipline_transfer_and_consistency.py`.
