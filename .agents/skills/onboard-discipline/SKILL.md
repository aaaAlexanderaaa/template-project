---
name: onboard-discipline
description: Inventory a new or existing repository, compare its facts against template-project contracts, and adopt or upgrade single-source-of-truth engineering discipline safely.
---

# Onboard Discipline Skill

1. Run `python3 scripts/read_rules.py onboard --target <target-path>` to inspect
   existing instructions, Git state, directory layout, LOC, oversized files, and
   `discipline_version`.
2. Read `AGENTS.md`, `docs/README.md`, [docs/contracts/adoption-and-synchronization.md](../../../docs/contracts/adoption-and-synchronization.md),
   and [docs/guides/onboarding.md](../../../docs/guides/onboarding.md) plus any
   domain contract triggered by the target repository's files.
3. Classify every contract rule against concrete target facts (*covered*,
   *adopt*, or *not applicable with concrete fact*), and select the appropriate
   path (`Path A` new prototype, `Path B` existing codebase starting at
   `stage = "observed"`, or `Path C` incremental version sync).
4. Persist settled applicability decisions to disk in the target repository
   (asking first before copying governance scripts into a non-empty repo or
   enabling blocking CI gates).
