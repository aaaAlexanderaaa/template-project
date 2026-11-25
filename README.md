# Engineering Discipline Template (`template-project`)

> **中文说明**：请查看 [README_CN.md](README_CN.md)。

`template-project` is an **Engineering Discipline Template** (`discipline_version` in [docs-policy.toml](docs-policy.toml)) for software repositories built with AI coding agents. Its core product is a transferable set of engineering agreements, architectural contracts, starter templates, and independent review protocols that keep growing codebases readable, modular, honest, and aligned with the project owner's real intent.

The Python scripts in `scripts/` and the optional local web overview (`project.py serve`) are **supporting tools** that validate single-source links, enforce file line budgets, and bootstrap new or existing projects.

## What This Template Gives Any Repository

1. **Clear Entry & Priority Rules ([AGENTS.md](AGENTS.md))**: Defines rule priority, three-perspective pre-code judgment, concrete triggers by object type, and direct prohibitions against corner-cutting.
2. **Modular Contracts & Plain Language ([docs/contracts/](docs/contracts/README.md))**: Enforces single-source state ownership, five-part system architecture (positioning, runtime logic, bounded couplings, constraints/state, module entrypoints), stage-matched verification, and direct plain prose ([docs/README.md](docs/README.md#language-standard)).
3. **Traceable Governance & Design Gate ([docs/sources.toml](docs/sources.toml), [docs/work.toml](docs/work.toml))**: Connects verbatim owner requirements (`SRC-*`), architectural decisions (`ADR-*`), design drafts (`docs/design/`), module specs (`docs/specs/`), and concrete work items (`T-*`). Product direction and UI layouts require explicit owner approval before implementation.
4. **Reader-First Information & Layered Frontend Rules ([information-organization.md](docs/contracts/information-organization.md), [frontend-and-visual-discipline.md](docs/contracts/frontend-and-visual-discipline.md))**: Organizes docs, screens, and knowledge content around the reader's task, and builds interfaces from principles and a measurable best-practice baseline (WCAG 2.2 AA and more) before applying owner preferences and reference products.
5. **Open-Ended, Closed-Loop Independent Review ([docs/guides/grill.md](docs/guides/grill.md), [templates/independent-review.md](templates/independent-review.md))**: Requires fresh reviewer contexts with the author's explanations withheld, open holistic inspection across architecture and consistency, expectation-first checks for coverage, currency settled by dated sources retrieved at review time, and mandatory re-verification with original reviewers after fixes.
6. **Lossless Starter Templates & Skills ([templates/](templates/README.md), [.agents/skills/](.agents/skills/onboard-discipline/SKILL.md))**: Preserves full discipline rules while keeping `template-project` internal domain names out of downstream projects.

## Current State & Pending Owner Decisions

Task state is kept only in [docs/work.toml](docs/work.toml), so this README does not repeat it. Run `python3 scripts/project.py status` to see each domain's progress, the tasks waiting for owner sign-off, and open blockers; the Overview tab of the web overview (`python3 scripts/project.py serve`) shows the same list.

## Quick Start

### Start a new project from this template

```bash
python3 scripts/project.py init --target /path/to/new-repo --name "My Product" --lang en
# Or initialize with Chinese starter docs:
python3 scripts/project.py init --target /path/to/new-repo --name "我的项目" --lang zh
```

### Adopt or upgrade engineering discipline in an existing repository

```bash
python3 scripts/read_rules.py onboard --target /path/to/existing-repo
# Upgrade a repository that already uses the discipline:
python3 scripts/project.py init --target /path/to/existing-repo --sync
```

### Verify this repository cleanly

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
python3 scripts/check_docs.py --strict
python3 scripts/project.py status
```

## Key Entrypoints

| File | Role |
|---|---|
| [AGENTS.md](AGENTS.md) | Top-level working agreement loaded by every human and AI session |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Positioning, core operational logic, constraints, state ownership, subsystems, and downstream transfer |
| [docs-policy.toml](docs-policy.toml) | `discipline_version`, line budgets (`max_source_lines`, `max_style_lines`), and review cadence |
| [docs/README.md](docs/README.md) | Document layout, plain-language rules, and context-reading workflow |
| [docs/design/perspective-web.md](docs/design/perspective-web.md) | Specification of the 4-view web overview and its default calm-platter style (light gray canvas, one white content panel, quiet color) |
| [templates/README.md](templates/README.md) | Starter templates transferred to downstream repositories |
| [.agents/skills/clean-chatgpt-flavor/SKILL.md](.agents/skills/clean-chatgpt-flavor/SKILL.md) | Optional standalone self-contained add-on skill (`Clean ChatGPT Flavor`, also distributed at [clean-chatgpt-flavor](https://github.com/aaaAlexanderaaa/clean-chatgpt-flavor)) for countering overly defensive ChatGPT generation: cleans anxious prose and stacked disclaimers by default, and inventories unasked SHA-256 audit theater, CYA schema/LLM payload fields, and redundant verification pipelines before editing code |
