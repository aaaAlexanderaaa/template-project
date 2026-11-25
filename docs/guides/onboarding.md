---
doc_type: guide
status: current
authority: guidance
---

# Onboarding & Incremental Synchronization Guide

Use this playbook when starting a new project from `template-project`, adopting
the discipline into an existing repository, or upgrading an older checkout to
the current `discipline_version` declared in `docs-policy.toml`.

## 1. Copyable Prompt for External Projects

```text
Learn the engineering discipline from /path/to/template-project:
1. Run `python3 /path/to/template-project/scripts/read_rules.py onboard --target .`
   to inventory this repository's current layout, LOC, instructions, and git state.
2. Read `AGENTS.md`, `docs/README.md`, and the contracts in `docs/contracts/`
   before judging what applies here.
3. Compare each practice against this repository's concrete facts and current
   maturity stage (`prototype`, `usable`, or `stable`), and check any supplied
   personal user-memory onboarding file (keeping private paths out of git).
4. Write settled applicability updates to disk (or present options first before
   copying scripts, enabling blocking CI gates, or editing product code).
```

## 2. Three Adoption Paths

### Path A — Brand-New Project (`0 → 0.1` Prototype)

1. Ensure Git is initialized in your new repository directory.
2. From `template-project`, run `python3 scripts/project.py init --target /path/to/new-repo --name "<Project Name>" --stage prototype --lang en`
   (or `--lang zh`, or edit `docs-policy.toml` to set `identity = "product"` and `default_stage = "prototype"`).
3. Fill `ARCHITECTURE.md` with the system one-liner and an initial end-to-end
   `mermaid` flow, record the owner's initial verbatim request as `SRC-001` in
   `docs/sources.toml`, and create `docs/work.toml` with the first milestone.
4. Keep ceremony light: skip multi-agent reviews while validating `0 → 0.1`.

### Path B — Existing Codebase (Including 100k+ LOC Multi-Subsystem Repos)

1. Verify `git status` is clean (or commit baseline files before adding
   governance files).
2. Before copying any governance files, run `python3 <template>/scripts/read_rules.py onboard --target .`
   and read the listed required contracts to inspect Day-0 directory LOC,
   oversized monolith files, and catch-all buckets on your actual codebase.
3. Run `python3 <template>/scripts/project.py init --target . --name "<Project Name>" --lang en`
   (or `--lang zh`) from `<template>`. On existing codebases, `init`
   automatically sets `[adoption] stage = "observed"` and populates
   `source_roots` from detected non-tooling directories or root source files
   (edit `docs-policy.toml` only if you need to add extra custom roots); it
   also sanitizes cloned template checkouts by removing template-only domains,
   ADRs, and example stubs while copying clean `templates/` starters,
   `scripts/projectlib/`, and the web overview assets (`web/`). If
   copying manually instead, copy the starter entry files from
   `<template>/templates/` (`AGENTS.md`, `ARCHITECTURE.md`, `docs-readme.md` ->
   `docs/README.md`, `architecture-rules.toml`, `sources.toml`, `work.toml`) plus
   `<template>/docs-policy.toml` rather than `template-project`'s root docs,
   along with `docs/contracts/`, `docs/guides/`, `.agents/skills/`, `templates/`,
   and `scripts/`, leaving Day-0 task `specs = []` (in `observed` stage,
   `check_docs.py` reports unresolved task `specs` as advisories rather than
   failing). Then run `python3 scripts/project.py status` to view synthesized
   codebase modules and blocker status.
4. Group directories into bounded domains (`docs/specs/<domain>/README.md` +
   `docs/specs/<domain>/<module>.md`), confirm domain stages and promises with
   the owner, and tighten `[adoption] stage` to `"adopted"` once ownership globs
   cover active source roots.

### Path C — Upgrading an Older `template-project` Checkout

1. Run `python3 <template>/scripts/read_rules.py onboard --target <repo>` to see
   the `discipline_version` delta.
2. Run `python3 <template>/scripts/project.py init --target <repo> --sync`.
   What it replaces, changes, preserves, and prints is defined once in
   [adoption-and-synchronization.md](../contracts/adoption-and-synchronization.md#3-incremental-discipline_version-upgrades).
3. Merge new trigger rows from the template `AGENTS` file whose path the
   command prints, fix any hardcoded `discipline_version` lines it lists, and
   apply the release notes for every newer version.
4. If the repository still has the old long-form document templates (the
   single-file layout with twelve fixed sections that this discipline replaced
   with thin module specs), move them to `archive/` instead of deleting them.
