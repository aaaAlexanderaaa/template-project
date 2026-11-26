---
id: ADR-009
kind: decision
status: current
title: "Anchor work to goals and layer complexity bounds, keep default rules positive and lean, add universal information/research principles, and keep only bounded checker fixes"
sources:
  - SRC-036
  - SRC-037
affects:
  - discipline.entry-and-contracts
  - discipline.guides-and-skills
  - discipline.templates
  - graph.model
  - graph.indexer
  - graph.validator
  - perspective.server
  - ui.perspective-web
supersedes: []
---

# ADR-009: Goal-Anchored Layer Complexity, Positive-First Lean Rules & Bounded Checker Fixes

- **Context & problem**:
  1. **Goal drift under mechanical adherence to local instructions (`SRC-037`).**
     During this release, an early draft packed downstream project details into
     default contracts alongside four opportunistic helper-script additions. A
     pre-release `/grill` then applied `ADR-008` subtraction mechanically by
     reverting the information/research discipline back to zero while expanding
     helper-script edge fixes (including a framework-specific `.astro` parser)
     across 40+ files. Both failures came from the same root cause: following
     local instructions or review loops while losing sight of the stated goal,
     combined with an unbounded `graph-engine` promise that invited helper
     scripts to grow into a multi-framework static analyzer.
  2. **Negative constraints loaded by default cause two-way reinforcement (`SRC-036`).**
     Listing bad writing habits in default-loaded rules primes clean models with
     habits they lacked and reinforces those habits in models that already have
     them. Meanwhile `prose_checks.py` routed `project_language_mismatch` and
     `plain_language_jargon` through the legacy `startup_disclaimers` key,
     failed builds on heuristic jargon terms, and emitted rule ID
     `startup_disclaimer` while `docs-policy.toml` named the key
     `disclaimer_phrases`.
  3. **Universal principles from cross-project knowledge and research work were
     missing from Layer 1**, while detailed research and Chinese prose workflows
     belong in optional on-demand skills (`T-210`).

- **Chosen approach**:
  1. **Anchor execution to goals, bound complexity by layer, and enforce
     promise-implies-non-promise (`SRC-037`)**:
     - Record the observed expectation violation and resolution under `ADR-008`.
     - State in `AGENTS.md`, `templates/AGENTS*.md`, and
       `collaboration-and-governance.md` that local checklists, side fixes, and
       subtraction never replace the stated goal; subtraction means rethinking
       how to meet the goal cleanly without piling up debt; and owner choices
       separate the main goal from opportunistic side fixes.
     - State in `architecture-and-modularity.md` that a module's stated promise
       implies what it does not promise, keeping most of its content and effort
       centered on its primary role.
     - Define the 4-layer complexity and extension model in `ARCHITECTURE.md`
       (core discipline via sharper general abstractions; specialized workflows
       via on-demand skills; `scripts/` capped at universal structural facts
       rather than framework-specific parsers; optional web view kept read-only
       and minimal) and narrow `docs/specs/graph-engine/README.md` accordingly.
  2. **Keep default rules positive-first and add 4 concise universal principles**:
     - Keep positive-first default rules in one home
       (`docs/README.md#language-standard` and starter `templates/docs-readme*.md`),
       removing inline negative buzzword examples.
     - Add four concise, project-agnostic principles: separating stable
       structure from volatile catalogs and declaring reader baselines without
       letting maintenance crowd reader navigation (`information-organization.md`),
       discovering sources through verified practitioners and checking
       counter-arguments (`research-and-access.md`), and separating exact
       engineering facts from multi-definition open-domain data without false
       precision (`delivery-and-verification.md`), plus concise lines on
       avoiding invented approval ceremonies and verifying against expected
       states / real browsers.
     - Keep detailed research and positive-first Chinese writing workflows in
       standalone optional skills under `.agents/skills/` (`T-210`).
  3. **Finish `ADR-008` sync and retain only bounded helper-script fixes**:
     - Downgrade `plain_language_jargon` to `"advisory"` in `REMINDER_KEYS`
       alongside `disclaimer_phrases`, split `project_language_mismatch` into
       its own key, and align `ADR-008` wording across `README*.md`,
       `templates/AGENTS*.md`, `templates/ARCHITECTURE*.md`, `grill.md`,
       `perspective-web.md`, `templates/surface-spec*.md`, `check_docs.py`, and
       `i18n.js`.
     - Retain unified POSIX glob matching (`model.match_path_pattern`) and
       repository-bounded `[layout].doc_roots` (`model.normalize_doc_roots`,
       `prose_checks.py`, `validator.py`, `doc_inventory.py`, `loader.py`,
       `init_repo.py`), plus `init --sync` notices for `docs/README.md` and
       legacy `startup_disclaimers`.
     - **Revert framework-specific `.astro` parsing** (`frontmatter.py`,
       `import_scanner.py`, `prose_checks.py`, `validator.py`, `read_rules.py`)
       as outside the helper-script complexity boundary.
  4. Release as `discipline_version` `2026.11.4`.

- **Trade-offs & rejected alternatives**:
  - Keeping `.astro`-specific frontmatter/`<script>`/`<style>` parsing inside
    `scripts/projectlib/` was rejected under `SRC-037`: every new frontend
    framework would force more regex parsers and edge-case loops into a helper
    that exists to check universal structural facts.
  - Dropping all information/research discipline to zero during `/grill` was
    rejected: mechanical subtraction abandoned the original goal instead of
    distilling the universal principles cleanly.
  - Leaving `plain_language_jargon` as a build-failing error was rejected:
    wording heuristics are judgments, not deterministic facts (`ADR-008`).

- **Expectation**:
  1. Future tasks keep discipline work centered on the stated goal; when a
     draft is bloated, agents distill sharper abstractions or move procedures
     into on-demand skills rather than abandoning the goal or expanding helper
     scripts with framework-specific parsers.
  2. Default-loaded rules stay lean and positive-first, wording heuristics
     remind rather than break builds, and universal glob / `[layout].doc_roots`
     checks work cleanly without custom wrappers.
  *Wrong if* helper scripts accumulate new framework-specific parsers, side
  fixes overtake a discipline task during review loops, or default contracts
  grow back with domain-specific procedures.
