---
id: discipline.guides-and-skills
domain: discipline
kind: module-spec
summary: "Operational playbooks for onboarding, pre-code design grill, open closed-loop independent review, behavioral discipline scenarios, and portable agent skills."
promise: "Guides and skills ensure agents run pre-implementation design challenges with explicit owner choices, open holistic reviews with the author's explanations withheld, and closed-loop re-verification back to original reviewers."
owns:
  - "docs/guides/**"
  - ".agents/skills/**"
depends_on:
  - discipline.entry-and-contracts
sources:
  - SRC-026
  - SRC-027
  - SRC-002
  - SRC-005
  - SRC-007
---

# Operational Guides & Agent Skills

## 1. Purpose, Narrow Interface & Non-Goals

- **Public interface**: Procedural playbooks (`docs/guides/{onboarding,grill,research-and-access}.md`), core portable skills (`.agents/skills/{grill,onboard-discipline}/SKILL.md`) transferred on `init` / `onboard`, and optional standalone self-contained add-on skills (`.agents/skills/clean-chatgpt-flavor/SKILL.md`, `.agents/skills/deep-research/SKILL.md`, `.agents/skills/plain-chinese-writing/SKILL.md`) invoked on demand or copied independently without expanding default context.
- **Out of scope**: Setting standalone policy rules outside `AGENTS.md` / `docs/contracts/` or modifying product code without target-repo confirmation during external onboarding.

## 2. Operational Procedure & Escalation Flow

```mermaid
flowchart LR
  Trigger["Trigger (/grill, Independent Review, or Onboard)"] --> Mode{"Check Stage & Mode"}
  Mode -->|Pre-Code UI or Direction| Options["Challenge Premises + Present Options to Owner"]
  Options -->|Awaiting Choice| Stop["Mark Task Blocked in docs/work.toml"]
  Mode -->|Completed Change| Blind["Spawn Fresh Reviewer (No Author Rationale, Open Prompt)"]
  Blind -->|Findings Reported| Fix["Fix & Send Back to Original + Fresh Reviewer"]
```

## 3. Constraints, State Ownership & Forbidden Couplings

- **Single authoritative owners**: Review protocol steps live in `docs/guides/grill.md`; onboarding inventory protocol lives in `docs/guides/onboarding.md`.
- **Forbidden couplings**: Skills MUST NOT hardcode `template-project` internal domain assumptions or skip `read_rules.py onboard` when assessing an external codebase; pre-fix rationales MUST NOT leak into independent reviewer prompts.
- **Verification**: Anchor resolution (`#behavioral-discipline-evaluation-scenarios`), `test_read_rules_and_onboard.py`, and `test_discipline_transfer_and_consistency.py`.
