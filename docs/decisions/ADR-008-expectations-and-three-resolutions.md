---
id: ADR-008
kind: decision
status: current
title: "Every judgment states an expectation; an observed violation ends in one of three recorded resolutions"
sources:
  - SRC-031
  - SRC-032
  - SRC-033
  - SRC-034
  - SRC-035
affects:
  - discipline.entry-and-contracts
  - discipline.templates
  - graph.validator
supersedes: []
---

# ADR-008: Judgments, Expectations & Three Resolutions

- **Context & problem**:
  1. **The discipline only grows.** Version 1 was archived after its rules
     piled up faster than anyone removed them. Version 2 still has no regular
     way to remove a rule.
  2. **Judgments are recorded without a way to test them later.** An ADR says
     why a choice was made, not what the choice should cause. A later session
     revisiting it has nothing to compare against.
  3. **Models have no memory.** A model knows only the context it is given,
     from project documents or the harness, and the harness changes with agent
     products. Project documents are the memory the owner controls
     (`SRC-032`).
  4. **The reader is a capable agent** (`SRC-031`). Rules state the essence
     and leave the details to its judgment; fine-grained fixed limits need a
     reason to exist (`SRC-034`).

- **Chosen approach**:
  1. **A judgment states its expectation**: what should happen because of it,
     and what would show it is wrong. Judgments are ADRs, module `promise`s,
     checks that can fail the build, and a project's health constraints.
  2. **An expectation violation is recorded under the judgment it
     contradicts**, when it is seen, so a later session finds it there.
  3. **Each violation ends in one of three resolutions** (`SRC-033`), written
     under the same judgment:
     - **Revise the expectation**: the expectation was wrong. The judgment
       changes or is retired. This is the regular way to remove rules.
     - **Correct the phenomenon**: the expectation is right and what is
       happening is wrong. Code or documents change; the judgment stays.
     - **Accept with a stronger description**: the old expectation described
       only part of the picture. The new description covers both and can still
       be contradicted by a future observation. Attaching an exception to the
       old text is not a stronger description. Accepting a minor violation is
       a stronger description too, and is written down so later sessions do
       not argue it again.
  4. **The project's goal and the owner quotes decide which resolution
     applies**; the current observation and the old expectation cannot judge
     each other. Who may decide follows the existing decision authority
     boundary in `collaboration-and-governance.md`.
  5. **Health constraints live in `ARCHITECTURE.md`, next to the goal they
     serve.** That is where an agent reads the project's purpose. The project
     chooses a few and adjusts them sparingly against the goal.
  6. **Numbers may trigger reminders; only facts fail the build.** A check
     fails the build only when a script can decide right or wrong (a broken
     link, a copied fact, a file no module owns). A number that stands in for
     a judgment, such as a line count meaning "too big", only reminds; the
     agent decides.
  7. **This loop replaces the self-supervision section** of
     `collaboration-and-governance.md`; it does not stand beside it.
  8. In a holistic review, judgments with open violations come first, and
     removing something is the first option considered.

- **First cases** (implemented in `2026.11.3` together with the contract change):

  | Judgment | Expectation | Observed | Resolution |
  |---|---|---|---|
  | `prototype` stage | A `prototype` project defers ownership, import, and budget checks. | A fresh `init --stage prototype` writes `adopted`; the first source file fails with `unclaimed_source`. | Correct the phenomenon: the validator reads the `stage`. |
  | Disclaimer phrases | A listed phrase marks a defensive disclaimer. | `相关性不等于因果性` fails the build in a downstream note. | Stronger description: a defensive disclaimer is a chain of hedges that protects the author, not a single negation. The check becomes a reminder. |
  | "Python 3.11+" | The scripts run wherever the project is used. | The macOS default `python3` stops every command. The only reason for 3.11 is the standard TOML reader `tomllib`. | Revise the expectation: the need is a TOML reader, not a Python version. |
  | Line budgets and banned folder names | They prevent oversized files and catch-all folders. | Files sat just under the limit; whether a file is too big is a judgment. | Revise the expectation (owner choice, `SRC-035`): they remind, never fail the build (item 6). |
  | Hand-kept list of template ADR IDs in `checkout_sanitizer.py` | — | It went stale when this ADR was added. | Accepted: a test already catches it. |

- **Expectation for this decision**: holistic reviews start ending in removed
  or loosened rules, and the discipline text does not grow because of this
  ADR. *Wrong if* reviews keep producing only additions.
- **Observed violation & resolution (2026-11-26, `SRC-037`)**:
  - *Observed*: During a release meant to distill cross-project lessons into
    discipline, subtraction was applied mechanically by dropping the core
    discipline edits to zero while an opportunistic helper-script side task
    (including framework-specific `.astro` parsing) grew to 40+ files across
    three review loops.
  - *Resolution (Stronger description & revise expectation)*: Subtraction means
    rethinking how to meet the goal cleanly without piling up debt, never
    abandoning the goal; before reworking a side task or review finding, check
    whether it serves the original goal or should be cut. Helper scripts stay
    capped at universal structural facts, and a module's stated promise also
    implies what it does not promise (applied in `ADR-009`).

- **Rejected alternatives**:
  - A total size cap for the discipline: a fixed number is what `SRC-032`
    asks to avoid.
  - Keeping the loop in model or harness memory (`SRC-032`).
  - The first draft of this ADR, which added a decision table, a fixed review
    order, a target count of health constraints, sentence limits, and script
    checks for the loop's structure. A capable agent works these out itself;
    writing them down added rules to a decision meant to stop rules from
    piling up (`SRC-034`).
  - Health constraints in `docs-policy.toml`: scripts read that file, and a
    script cannot judge health.
