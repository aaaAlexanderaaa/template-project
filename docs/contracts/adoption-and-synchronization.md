---
doc_type: contract
status: current
authority: normative
---

# External Learning, Onboarding & Version Synchronization

<!-- required-reading: read-before-judgment -->
## 1. External Learning (`"Learn From template-project"`)

When asked in another repository to learn or adopt practices from
`template-project`:

1. **Inventory target facts first**: Run
   `python3 <template-path>/scripts/read_rules.py onboard --target <target-repo>`
   to inspect existing instructions, Git cleanliness, directory layout, LOC,
   oversized files, and any prior `discipline_version`.
2. **Read core contracts + fact-triggered rules before judging fit**: Open
   `AGENTS.md`, `docs/README.md`, and the contracts under `docs/contracts/`
   (especially any domain triggered by concrete files in the target repo, such
   as styles/UI or multi-subsystem boundaries) before deciding what applies.
3. **Evaluate by concrete repository facts**: Classify each practice as:
   - *Applies & already covered locally* (cite existing local file/mechanism);
   - *Applies & needs adoption* (adapt to the target's stack and `stage`); or
   - *Not applicable* (cite the concrete repository fact, e.g. headless CLI
     with zero HTML/CSS surfaces).
4. **Write settled judgments to disk**: Learning is incomplete if left only in
   chat. Persist agreed rule updates into the target's `AGENTS.md` / `docs/`
   (or ask for confirmation first before copying governance scripts, enabling
   strict CI gates, or modifying product code). Keep private personal-memory
   paths out of public repository commits.
<!-- /required-reading: read-before-judgment -->

<!-- required-reading: existing-directory-safety -->
## 2. Safe Onboarding for New vs Existing 100k+-Line Repositories

- **Empty directory**: State clearly what the new project is, copy or generate
  minimal starter files (`python3 scripts/project.py init`), set
  `identity = "product"` and `default_stage = "prototype"`, and start building.
- **Existing non-empty directory**:
  1. Ensure Git is initialized and existing files are committed before adding
     governance files; if Git cannot be initialized, stop and report to the owner.
  2. Start at `[adoption] stage = "observed"` so `check_docs.py` reports
     unclaimed directories, catch-all buckets, `# Role:` headers, import boundaries,
     and oversized files as non-blocking advisories without breaking existing CI.
  3. Run `read_rules.py onboard --target <repo>` to measure the repository as it
     is today (lines of code, oversized files, catch-all directories, Git state) and `project.py status`
     for project summary; complete a one-time AI-assisted spec baseline
     (confirmed by the owner) to populate `ARCHITECTURE.md` and
     `docs/specs/<domain>/*.md`, recording `SRC-*` verbatim quotes going forward.
  4. When initialized with `--lang zh`, project-authored entrypoints and
     templates (`AGENTS.md`, `ARCHITECTURE.md`, `docs/README.md`, starter
     templates under `templates/`, `docs/specs/`, `docs/sources.toml`,
     `docs/work.toml`), directory overview labels, and CLI output use plain
     Chinese, while shared normative contracts under `docs/contracts/` and
     playbooks under `docs/guides/` remain canonical English single-source
     references unless locally adapted.
<!-- /required-reading: existing-directory-safety -->

<!-- required-reading: incremental-version-sync -->
## 3. Incremental `discipline_version` Upgrades

Each release of `template-project` declares `discipline_version` in
`docs-policy.toml`; no other file repeats the number. To upgrade an
already-adopted repository:

1. Run `python3 <template>/scripts/read_rules.py onboard --target <repo>` to
   compare the target's `discipline_version` with the template's.
2. Run `python3 <template>/scripts/project.py init --target <repo> --sync`.
   This is the only definition of what the command does:
   - **Replaced with the template's copy**: `scripts/check_docs.py`,
     `scripts/project.py`, `scripts/read_rules.py`, `scripts/rule_reading.py`,
     all of `scripts/projectlib/`, `docs/contracts/*.md`, `docs/guides/*.md`,
     `.agents/skills/grill/` and `.agents/skills/onboard-discipline/`, and the
     starter files under `templates/`.
   - **Changed in `docs-policy.toml`**: only `discipline_version` (set to the
     template's), `identity = "template"` switched to `"product"`, and missing
     tool directories added to `harness_paths`. Stage, budgets, collaboration
     mode, and every other setting stay as they are.
   - **Never touched**: `AGENTS.md`, `README.md`, `ARCHITECTURE.md`,
     `docs/specs/**`, `docs/design/**`, `docs/decisions/**`,
     `docs/sources.toml`, `docs/work.toml`, and `architecture-rules.toml`.
   - **Printed**: the full path of the template's `AGENTS.md` (or
     `AGENTS.zh.md`) to compare with the project's own, and every Markdown line
     that still hardcodes `discipline_version` (outside `docs/decisions/` and archives).
3. Merge new or rewritten trigger rows from the printed template file into the
   project's `AGENTS.md`, and replace any hardcoded version with a pointer to
   `docs-policy.toml` (`check_docs.py` reports remaining copies as errors).
4. Read the release notes in Section 4 for every version newer than the one
   you upgraded from, and apply the ones that fit the project.
<!-- /required-reading: incremental-version-sync -->

## 4. Release Notes for Upgrading Projects

Newest first. Each entry lists only what an upgrading project should check.

- **2026.11.3**
  - When a decision is recorded, also write its expectation: what should
    happen, and what would show it is wrong. When later work contradicts it,
    record the violation and its resolution under that decision (see "Judgments,
    Expectations & Three Resolutions" in `collaboration-and-governance.md`).
  - Line budgets, banned folder names, and hedge phrases now only remind; they
    no longer fail the build, even with `--strict`. Hedge phrases are checked
    only in `AGENTS.md`, `docs/README.md`, contracts, guides, and templates.
  - A `prototype` project or module no longer fails on ownership, imports,
    role headers, or budgets; these become reminders until the stage changes.
  - The scripts run on older Python when `tomli` is installed; Python 3.11+
    needs nothing extra.
- **2026.11.2**
  - Keep each fact in one file: point to `docs-policy.toml` instead of
    repeating `discipline_version` or line budgets, point to `docs/work.toml`
    instead of repeating task states, and drop hard-coded counts such as "six
    contracts".
  - `check_docs.py` now fails on two new errors until they are fixed:
    `hardcoded_version` (a Markdown line that copies `discipline_version`) and
    `duplicate_module_source` (a module spec that re-lists a quote an ADR
    already brings through `affects`). Expect the first run after `--sync` to
    fail; remove the copies it lists.
  - Rewrite each trigger row in `AGENTS.md` as one or two sentences: when it
    applies, which contract section to read first (`read_rules.py prepare
    --concern <topic>`), and the one rule that must never be missed. Keep
    numbers and step lists in the contracts only.
  - Put a quote in a module spec's `sources` only when it is about that
    module. Record a quote behind a cross-module decision once in the ADR's
    `sources` with `affects`; `project.py context` shows it on each affected
    module as a one-line reference.
  - If the project has a web UI: give inputs and other controls a border color
    with at least 3:1 contrast, show a visible `:focus-visible` outline, make
    expandable rows usable with Enter/Space, let Esc close menus and drawers and
    return focus to the button that opened them, and honor
    `prefers-reduced-motion`.
- **2026.11.1**
  - Organize reader-facing docs, screens, and knowledge content with
    `docs/contracts/information-organization.md`.
  - Confirm the frontend meets the mandatory best-practice baseline (measured
    contrast, keyboard, focus, states), and record any owner preferences that
    should replace the default calm-platter style in `docs/design/`.
  - Run coverage or currency reviews with expectation-first lists and dated
    sources retrieved at review time.
