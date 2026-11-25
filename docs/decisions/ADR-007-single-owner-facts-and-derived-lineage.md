---
id: ADR-007
kind: decision
status: current
title: "Remove recurring consistency friction at its source: one owner per fact, short trigger rows, one quote-lineage rule, and a checked upgrade path"
sources:
  - SRC-028
  - SRC-029
  - SRC-030
affects:
  - discipline.entry-and-contracts
  - discipline.guides-and-skills
  - discipline.templates
  - graph.model
  - graph.validator
  - perspective.context-pack
  - perspective.server
  - ui.perspective-web
  - exemplar.shared
supersedes: []
---

# ADR-007: One Owner per Fact, Short Trigger Rows, One Quote-Lineage Rule & a Checked Upgrade Path

- **Context & problem**:
  1. **Copied facts went stale.** Every release needed the same cleanup: the
     version string, contract counts ("six contracts"), line budgets (500/300),
     and task states (`T-204` awaiting sign-off) were written into `AGENTS.md`,
     both READMEs, `ARCHITECTURE.md`, guides, specs, templates, and
     `doc_inventory.py`. Each change left some copies wrong.
  2. **Entry rows repeated contracts.** Trigger rows in `AGENTS.md` and
     `templates/AGENTS*.md` restated whole contract paragraphs, so one contract
     edit needed matching edits in three entry files.
  3. **Quotes were hand-copied.** A quote behind a cross-module ADR was copied
     into the `sources` of many module specs (`SRC-010` into nine of them), and
     the scripts did not agree on which quotes belong to a module.
  4. **Some contract sections were never served.** `read_rules.py prepare
     --concern <topic>` hands an agent only the contract sections listed for
     that topic in `CONCERN_MAP` (`scripts/rule_reading.py`). Sections marked as
     required reading but missing from that list never reached agents who used
     the command.
  5. **Upgrades silently kept old facts.** `project.py init --sync` preserves a
     project's own `AGENTS.md`, so a downstream repository could keep the old
     version written in `AGENTS.md` next to the new one in `docs-policy.toml`,
     and nothing reported it. The documents also described the upgrade scope in
     four different ways.
  6. The owner asked whether this friction means the discipline itself is a
     burden or the checks should be relaxed, and chose to fix the root cause
     (`SRC-028`).
- **Chosen approach**:
  1. **One owner per fact**: `discipline_version` and line budgets live only in
     `docs-policy.toml`, task state only in `docs/work.toml`, and the contract
     list only in `docs/contracts/README.md`. A domain's stage lives in its
     `docs/specs/<domain>/README.md`; a module spec may override its own stage.
     Other files point to these owners. `check_docs.py` reports Markdown lines
     that write `discipline_version = "x"` (outside `docs/decisions/` and
     archives, where old versions are history), here and downstream.
  2. **Short trigger rows** (owner choice in `SRC-030`): each row says in one or
     two sentences when it applies, which contract section to read first
     (with the `read_rules.py prepare --concern <topic>` command), and the one
     rule that must never be missed. Numbers and step lists stay only in the
     contracts.
  3. **One quote-lineage rule** (`module_source_refs` in
     `scripts/projectlib/model.py`): a module spec's own `sources` hold only
     quotes about that module and are shown in full; quotes reached through a
     current ADR whose `affects` names the module are shown as one line each
     (ID, the ADR, and the quote's context), with the full text one `trace`
     away (`SRC-029`). `project.py context`, `project.py trace`, the web
     overview, and `check_docs.py` reminders all use this rule. Spec entries
     that duplicate a quote already reached through an ADR were removed, and
     `check_docs.py` reports new duplicates (`SRC-030`). Task `sources` stay on
     tasks.
  4. **Every required-reading section is served**: a test fails when a
     required-reading section in `docs/contracts/*.md` is missing from
     `CONCERN_MAP`.
  5. **Checked upgrade path**: the scope of `init --sync` is written once, in
     `docs/contracts/adoption-and-synchronization.md`; other documents link to
     it. The command prints the full path of the template `AGENTS` file to
     compare and lists lines that still hardcode `discipline_version`.
     Per-release upgrade steps live in a release-notes section outside the
     required-reading span, so agents read only notes newer than their version.
  6. **Web overview accessibility baseline** (last item of the option chosen in
     `SRC-028`): a `--control-border` token with at least 3:1 contrast for
     inputs and controls, a visible `:focus-visible` outline, Enter/Space to
     expand table rows, Esc to close the menu or document drawer with focus
     returned to the button that opened it, and `prefers-reduced-motion`
     handling. Tests measure text and border contrast on every background the
     overview uses.
  7. These changes were released as `discipline_version` `2026.11.2`.
- **Recording option text the owner chose** (`SRC-030`): text the owner
  selected or pasted as an answer counts as the owner's answer and may go into
  a `quote`; the `context` must say which part was written by the agent. Preset
  options picked in the web overview stay on the task (`selected_option`).
- **Is the discipline a burden?** The friction came from the same fact being
  kept in several places, which the discipline's own single-owner rule
  forbids. Removing those copies lowers the cost of every later change, and the
  checks that stay in place now catch drift instead of producing busywork.
  Review effort follows the same idea: fix what matters and accept marginal
  issues (`SRC-030`).
- **Trade-offs & rejected alternatives**:
  - Relaxing `check_docs.py` or the consistency tests was rejected: the
    friction came from duplicated facts, and fewer checks would let them drift
    silently.
  - Keeping concrete numbers (such as 4.5:1 contrast) in every entry row was
    tried and rejected (`SRC-030`): it made the rows longer than before and
    repeated the contracts again.
  - Deriving module quotes from tasks was rejected: it attached unrelated quotes
    to modules (for example a consistency quote to the reference app).
  - Showing every ADR-reached quote in full was rejected (`SRC-029`): it more
    than doubled some module context packs.
  - Keeping hand-copied duplicates as "quotes to show in full" was rejected
    (`SRC-030`): the copies were what made the rule ineffective. A central
    quote shown as one line (for example `SRC-022` on the web overview) is one
    `project.py trace` away.
