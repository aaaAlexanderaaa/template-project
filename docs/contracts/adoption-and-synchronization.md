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
   `AGENTS.md`, `docs/README.md`, and the six contracts under `docs/contracts/`
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
  3. Run `read_rules.py onboard --target <repo>` for Day-0 physical telemetry
     (LOC, oversized files, catch-all directory scan, Git state) and `project.py status`
     for project summary; complete a one-time AI-assisted spec baseline
     (confirmed by the owner) to populate `ARCHITECTURE.md` and
     `docs/specs/<domain>/*.md`, recording `SRC-*` verbatim quotes going forward.
  4. When initialized with `--lang zh`, project-authored entrypoints and
     templates (`AGENTS.md`, `ARCHITECTURE.md`, `docs/README.md`, starter
     templates under `templates/`, `docs/specs/`, `docs/sources.toml`,
     `docs/work.toml`), directory overview labels, and CLI output use plain
     Chinese, while shared normative contracts under `docs/contracts/` and
     playbooks under `docs/guides/` remain canonical English single-source
     references unless locally adapted (`SRC-021`).
<!-- /required-reading: existing-directory-safety -->

<!-- required-reading: incremental-version-sync -->
## 3. Incremental `discipline_version` Upgrades

Each release of `template-project` declares `discipline_version` in
`docs-policy.toml`. When upgrading an already-adopted repository:

- Compare the target's `discipline_version` with this template's version via
  `read_rules.py onboard --target <target-repo>`.
- Update mechanical tooling (`scripts/`) and general engineering contracts while
  **preserving all target-owned files** (`ARCHITECTURE.md`, `docs/specs/**`,
  `docs/design/**`, `docs/decisions/**`, `docs/sources.toml`, `docs/work.toml`,
  and local `architecture-rules.toml` rules).
<!-- /required-reading: incremental-version-sync -->
