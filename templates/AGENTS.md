# Repository Working Agreement

This repository follows the engineering discipline template (`discipline_version`
declared in `docs-policy.toml`). Keep plain language, single-source truth,
explicit module boundaries, real verification, and owner decision authority
intact as the codebase grows.

## 1. Priority Order

1. **Data safety and the requested outcome**: Protect user data, credentials,
   and destructive boundaries, and deliver working results rather than empty
   checklists; never let local checklists, side fixes, or mechanical subtraction
   replace the stated goal.
2. **Shared vocabulary and single source of truth**: Give every concept one
   name and every state value, config threshold, or promise one authoritative
   file.
3. **Clear boundaries, plain language, and isolated styles**: Write direct prose
   in the project's chosen language, put a `# Role:` header in every source and style file claimed by a spec's `owns`, keep
   modules decoupled, and separate style tokens from component styles.
4. **Stage- and mode-matched verification**: Run real end-to-end checks scaled to
   the target domain `stage` (`prototype` 0->0.1, `usable` 0.1->1, `stable` 1->N)
   and `[collaboration]` mode (`interactive` vs `unattended` bounded by `templates/charter.md`).
5. **Lineage sync**: Keep `docs/sources.toml`, `docs/decisions/`, `docs/design/`,
   `docs/specs/`, and `docs/work.toml` synchronized when scope or design changes.

## 2. Three-Perspective Check & Proactive Engineering Before Coding

1. **Executor**: Separate settled requirements (`docs/sources.toml`, current
   specs) from open product choices. Follow settled facts; challenge an
   assumption only with concrete evidence.
2. **Collaborator**: Match structure to design stability. Keep early `0->0.1`
   exploration lightweight; once behavior settles, write explicit boundaries and
   trade-offs into the owning spec.
3. **Senior Architect**: Inspect the domain `stage` (`docs/specs/<domain>/README.md`, default in `docs-policy.toml`). When a
   non-architect owner gives an informal brief, proactively propose clear
   runtime logic, single-owner state, error paths, and forbidden couplings in
   `ARCHITECTURE.md` and specs instead of leaving boundaries vague.

## 3. Required Triggers by Object or Effect

| Object or situation | Required action |
|---|---|
| Human- or AI-readable text (`README.md`, `ARCHITECTURE.md`, specs, CLI, errors, UI) | State plainly what the object is, how it works, and what problem it solves; avoid coined jargon, conflicting numbering, and stacked disclaimers (`docs/README.md#language-standard`). |
| Architecture or module description | Cover positioning/non-goals, end-to-end runtime/control flow (`mermaid`), bounded interfaces and forbidden couplings, single-owner state and hard constraints, and entrypoints/checks (`docs/contracts/architecture-and-modularity.md#decomposition-and-ownership`). |
| Shared value across memory, DB, API, DOM, URL, or config | Assign one authoritative owner and compute derived views mechanically (`docs/contracts/architecture-and-modularity.md#single-source-of-state`). |
| Product direction, interaction flow, or UI layout (`docs/design/`) | Before any product or UI design work, read `python3 scripts/read_rules.py prepare --concern frontend`. Principles and the measurable WCAG 2.2 AA baseline always outrank style preferences (the shipped default is the calm-platter style: light gray canvas, one white content panel), and no UI code is written before the owner records approval of a design option after a pre-code `/grill`. |
| Organizing information for readers (doc structure, navigation, screen content, knowledge or reference content) | Before structuring docs, screens, or knowledge content, read `python3 scripts/read_rules.py prepare --concern information`. Start from the reader's task and put the answer first. |
| Source files and CSS growth | Before adding files or growing one, read `python3 scripts/read_rules.py prepare --concern architecture` (and `--concern css` for styles). Every source and style file claimed by a spec's `owns` starts with a `# Role:` header; split files by responsibility when they grow past the line-budget reminders in `docs-policy.toml`, never by squeezing lines. |
| Substantive owner quote, trade-off, or direction change | Read `python3 scripts/read_rules.py prepare --concern lineage`. Record the owner's exact words in `docs/sources.toml`; a quote behind a cross-module decision goes only into that ADR's `sources` with `affects`, never copied into module specs (`check_docs.py` reports copies). |
| Task execution, review cadence, or unattended mode | Read `python3 scripts/read_rules.py prepare --concern verification`. Finish authorized tasks with real verification scaled to the domain `stage` and `[collaboration]` mode (`unattended` stays inside `templates/charter.md`); the owner decides when to run `/grill`, and agents only remind. |
| Independent review or verification | Load `.agents/skills/grill/SKILL.md` and read `python3 scripts/read_rules.py prepare --concern review`. Reviewers work in a fresh context without the author's explanations and report findings; the owner decides status. |
| Discipline onboarding or version sync | Read `python3 scripts/read_rules.py prepare --concern onboarding`. Upgrade with `python3 <template>/scripts/project.py init --target . --sync`, then apply the release notes for newer versions in `docs/contracts/adoption-and-synchronization.md`. Project-owned files stay intact. |

## 4. Direct Prohibitions Against Corner-Cutting

- **Run real execution paths and behavior checks**: Verify working CLIs,
  servers, or UI states rather than trusting mocked checks alone.
- **Keep independent review open, free of the author's explanations, and closed-loop**: Never
  pre-confine reviewers to narrow code checklists, supply author justifications,
  skip holistic architecture/consistency inspection, or mark a review closed
  without re-verifying fixes with the original critic and a fresh context.
- **Never treat unapproved drafts as owner sign-off**: Block pending design
  tasks in `docs/work.toml` until the owner chooses a direction explicitly.
- **Finish authorized tasks cleanly**: Complete implementation and checks
  end-to-end unless blocked on a real product decision.

## 5. Single-Source Commands & Identity Guard

- Inspect file/module context before editing: `python3 scripts/project.py context <path-or-id>`
- Inspect roadmap, directory layout, and blockers: `python3 scripts/project.py status` (`python3 scripts/project.py serve` shows the same information as a local web page)
- Load review guidance & skill: `docs/guides/grill.md`, `.agents/skills/grill/SKILL.md`, `templates/independent-review.md`
- Ensure `docs-policy.toml` sets `identity = "product"` rather than copying `template` settings unchanged.
- Verify tests and structural rules:

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
python3 scripts/check_docs.py   # add --strict in CI once stable: non-reminder advisories fail the run; reminder checks stay advisory
```
