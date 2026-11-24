---
id: system.root
name: "template-project"
one_liner: "Engineering discipline template providing plain-language agreements, five-part architecture contracts, starter templates, and open closed-loop independent review."
stage: stable
---

# Architecture Overview

## 1. Purpose, Promises & Non-Goals

`template-project` is an **Engineering Discipline Template** (`discipline_version = "2026.11.1"`). Its job is to help human owners and AI coding agents build, evolve, and review software repositories with shared terminology, clear boundaries, plain language, and verifiable accountability.

- **Core Promises**:
  1. **Transferable Engineering Discipline**: Package practical rules (`AGENTS.md`, `docs/contracts/`, `docs/guides/`, `.agents/skills/`) and starter scaffolding (`templates/`) so new (`project.py init`) and existing (`read_rules.py onboard`) repositories adopt the discipline cleanly without carrying `template-project` internal domains.
  2. **Traceable Decisions & Design Gate**: Anchor user quotes in `docs/sources.toml` (`SRC-*`), record design trade-offs in `docs/decisions/ADR-*.md`, and hold major product or UI choices at an explicit owner approval gate before writing implementation code.
  3. **Real Verification & Closed-Loop Review**: Verify both deterministic repository integrity and agent behavioral discipline, using blind-to-rationale, open-ended independent review that loops back until original findings are verified solved.
- **Explicit Scope Boundary**: This repository delivers reusable engineering discipline, governance workflows, and starter templates; the Python tools in `scripts/` and the optional browser overview serve strictly as generic helpers rather than a commercial web application or a dedicated document-extraction framework.

## 2. Core Operational Logic & Failure Loop

```mermaid
flowchart LR
  Owner["Owner Goal & Verbatim Quotes (docs/sources.toml)"] --> Gate["Pre-Code Gate: 3 Perspectives + Design Sign-Off"]
  Gate --> Build["Single-Source Implementation (Contracts, Specs, Templates, Code)"]
  Build --> Verify["Deterministic Checks + Behavioral Discipline Scenarios"]
  Verify --> Review["Open-Ended Independent Review (Fresh Context, No Rationale)"]
  Review -->|Defects Found: Fix & Re-Verify| Gate
  Review -->|Needs Product Choice| Owner
  Verify -->|Structural Error| Build
```

- **When a check fails**: Automated structure errors return directly to `Build` for cleanup; holistic or consistency defects found during independent review return to `Gate`/`Build` and must be re-verified by the original reviewer before advancing the review baseline.
- **When owner approval is missing**: Product direction or UI architecture drafts stop in `docs/design/` and `docs/work.toml` (`blocked` / `human_check = "pending"`) until the owner explicitly approves an option.

## 3. Hard Constraints, State Ownership & Forbidden Couplings

### Authoritative State Owners

| Fact or State | Single Authoritative Owner | Downstream Derived Consumers |
|---|---|---|
| Verbatim owner requirements & critiques | [docs/sources.toml](docs/sources.toml) (`SRC-*`) | Specs, ADRs, `work.toml` links |
| Non-negotiable engineering rules | [AGENTS.md](AGENTS.md) & [docs/contracts/](docs/contracts/README.md) | `templates/AGENTS*.md`, `scripts/read_rules.py` |
| Approved & pending UI surface designs | [docs/design/perspective-web.md](docs/design/perspective-web.md) & [docs/decisions/ADR-005-calm-platter-frontend-specification-and-perspective-web.md](docs/decisions/ADR-005-calm-platter-frontend-specification-and-perspective-web.md) | `scripts/projectlib/web/` and `T-204`; prior unapproved drafts never unlock code |
| Architectural decisions & rationales | [docs/decisions/](docs/decisions/ADR-004-discipline-first-architecture-and-open-closed-loop-review.md) (`ADR-*`) | Module specs & review baselines |
| Module bounds (`owns`, `promise`, `depends_on`) | [docs/specs/discipline/README.md](docs/specs/discipline/README.md) & sibling domains (`docs/specs/*/`) | Validator, import checks, onboarding |
| Milestones, tasks & review baseline | [docs/work.toml](docs/work.toml) & [docs-policy.toml](docs-policy.toml) (`review_anchor_sha` updated on clean `mark-reviewed`, dirty-worktree state in `tmp/project-state.json`) | `project.py status`, CLI progress summary |

### Hard Constraints & Explicitly Forbidden Couplings

| Constraint or Forbidden Coupling | Rule Summary | Where Enforced |
|---|---|---|
| **No assumed UI approval** | Never treat inherited web code or unapproved sketches in `docs/design/` as owner sign-off (`T-204` unlocked only after explicit `SRC-022` / `ADR-005`). | [frontend-and-visual-discipline.md](docs/contracts/frontend-and-visual-discipline.md), [delivery-and-verification.md](docs/contracts/delivery-and-verification.md) |
| **No template domain leakage** | `scripts/projectlib/doc_inventory.py`, `templates/`, and `project.py init` must never stamp `graph-engine`, `perspective-ui`, or `reference-app` into downstream repos. | [adoption-and-synchronization.md](docs/contracts/adoption-and-synchronization.md), [tests/test_discipline_transfer_and_consistency.py](tests/test_discipline_transfer_and_consistency.py) |
| **Open, rationale-blind, closed-loop review** | Independent reviewers receive only owner sources and repository files (with author explanations removed), evaluate architecture and consistency openly, and re-verify fixes directly. | [delivery-and-verification.md](docs/contracts/delivery-and-verification.md#independent-review-definition), [grill.md](docs/guides/grill.md) |
| **Architecture beyond static `import` boxes** | Static module import graphs never substitute for runtime control flow, state ownership, forbidden couplings, and failure handling. | [architecture-and-modularity.md](docs/contracts/architecture-and-modularity.md#decomposition-and-ownership) |
| **Hard file & prose limits** | `max_source_lines = 500`, `max_style_lines = 300`, `# Role:` header on claimed source files, zero jargon or stacked disclaimers in human/AI text. | [docs-policy.toml](docs-policy.toml), [docs/README.md](docs/README.md#language-standard) |

## 4. Subsystems Ordered by Product Role

| Role Priority | Domain ID | Authoritative Stage | Responsibility |
|---|---|---|---|
| **1. Primary Product** | `discipline` | `stable` | Owns entry agreements, contracts, `/grill` & independent review protocols, plain-language rules, skills, and starter templates transferred to downstream projects. Spec: [docs/specs/discipline/README.md](docs/specs/discipline/README.md) |
| **2. Live Example** | `reference-app` | `stable` | Minimal working checkout/CLI exemplar proving how a real product module applies `owns`, single-source state, sequence flows, and plain copy. Spec: [docs/specs/reference-app/README.md](docs/specs/reference-app/README.md) |
| **3. Subordinate Checker** | `graph-engine` | `stable` | Generic TOML/Markdown/AST/Git validator (`check_docs.py`, `read_rules.py`, `project.py` CLI) enforcing structural consistency without host domain assumptions. Spec & internal layer diagram: [docs/specs/graph-engine/README.md](docs/specs/graph-engine/README.md) |
| **4. Optional Visual Browser** | `perspective-ui` | `usable` (`ui.perspective-web` `usable`, `T-204` ready for check) | Local HTTP API & calm-platter 4-view web workbench (`project.py serve`). Rebuilt in `scripts/projectlib/web/` under `SRC-022` and `ADR-005` ([perspective-web.md](docs/design/perspective-web.md)). Spec: [docs/specs/perspective-ui/README.md](docs/specs/perspective-ui/README.md) |

## 5. Downstream Transfer Path (`init` & `onboard`)

```mermaid
flowchart LR
  Core["template-project Core (AGENTS + Contracts + Guides + Skills + Templates + Generic Scripts)"] -->|project.py init| NewRepo["New Repository (Clean Architecture + Starter Module Spec)"]
  Core -->|read_rules.py onboard| ExistingRepo["Existing Repository (Gap Inventory + Tailored Adoption Plan)"]
```
