---
id: discipline.entry-and-contracts
domain: discipline
kind: module-spec
summary: "Root working agreement, single-source map, plain-language standard, five-part architecture rule, UI design gate, and open closed-loop independent review contract."
promise: "Every agent session follows plain direct rules covering five-part architecture, explicit owner approval on UI/product drafts, and closed-loop review."
owns:
  - "AGENTS.md"
  - "CONTRIBUTING.md"
  - "docs/README.md"
  - "docs/contracts/**"
depends_on: []
sources:
  - SRC-001
  - SRC-006
  - SRC-007
  - SRC-008
  - SRC-009
  - SRC-023
---

# Entry Rules & Engineering Contracts

## 1. Purpose, Narrow Interface & Non-Goals

- **Public interface**: Human/AI reading entry (`AGENTS.md`, `docs/README.md`) and topical contracts under `docs/contracts/` fetched selectively via `read_rules.py prepare --concern <slug>` or trigger table in `AGENTS.md`.
- **Out of scope**: Runtime Python execution (owned by `graph-engine`) and starter file copies transferred verbatim without adaptation (owned by `discipline.templates`).

## 2. Runtime Governance Loop & Failure Paths

```mermaid
flowchart LR
  Task["Incoming Task + User Request"] --> Triage["3-Perspective Check + Trigger Table (AGENTS.md)"]
  Triage -->|Touches UI or Direction| DesignGate["Draft Options + /grill in docs/design/ (Block Until Owner Picks)"]
  Triage -->|Clear Requirements| Execute["Implement + Sync Authoritative Owner Files"]
  DesignGate -->|Approved| Execute
  Execute --> Verify["Run Stage-Matched Checks & Behavioral Scenarios"]
  Verify -->|Review Required| Indep["Open Review (Author Explanations Withheld)"]
  Indep -->|Defects Found| Execute
```

## 3. State Ownership, Hard Invariants & Forbidden Couplings

- **Single authoritative owners**: Normative rules live only in `AGENTS.md` and `docs/contracts/*.md`; language rules live only in `docs/README.md#language-standard`.
- **Forbidden couplings**: Unapproved drafts in `docs/design/` or older UI code MUST NOT count as approval to implement a design; reviewers MUST NOT receive author justifications or narrow code-only checklists before holistic inspection.
- **Verification**: Enforced mechanically by `read_rules.py` span integrity checks, `check_docs.py --strict`, and downstream sync checks in `tests/test_discipline_transfer_and_consistency.py`.
