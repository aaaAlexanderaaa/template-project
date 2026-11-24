# Repository Working Agreement

This repository follows the engineering discipline template (`discipline_version = "2026.11.1"`).
Keep plain language, single-source truth, explicit module boundaries, real
verification, and owner decision authority intact as the codebase grows.

## 1. Priority Order

1. **Data safety and the requested outcome**: Protect user data, credentials,
   and destructive boundaries, and deliver working results rather than empty
   checklists.
2. **Shared vocabulary and single source of truth**: Give every concept one
   name and every state value, config threshold, or promise one authoritative
   file.
3. **Clear boundaries, plain language, and isolated styles**: Write direct prose
   in the project's chosen language, declare each core file's `# Role:`, keep
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
3. **Senior Architect**: Inspect the domain `stage` (`docs-policy.toml`). When a
   non-architect owner gives an informal brief, proactively propose clear
   runtime logic, single-owner state, error paths, and forbidden couplings in
   `ARCHITECTURE.md` and specs instead of leaving boundaries vague.

## 3. Required Triggers by Object or Effect

| Object or situation | Required action |
|---|---|
| Human- or AI-readable text (`README.md`, `ARCHITECTURE.md`, specs, CLI, errors, UI) | State plainly what the object is, how it works, and what problem it solves; follow `docs/README.md#language-standard`. |
| Architecture or module description | Cover positioning/non-goals, end-to-end runtime/control flow (`mermaid`), bounded interfaces and forbidden couplings, single-owner state and hard constraints, and entrypoints/checks (`docs/contracts/architecture-and-modularity.md#decomposition-and-ownership`). |
| Shared value across memory, DB, API, DOM, URL, or config | Assign one authoritative owner and compute derived views mechanically (`docs/contracts/architecture-and-modularity.md#single-source-of-state`). |
| Product direction, interaction flow, or UI layout (`docs/design/`) | Apply the four frontend layers in order: principles, the measurable best-practice baseline (WCAG 2.2 AA contrast, keyboard, focus, states), this project's owner preferences (the shipped calm-platter defaults until the owner records others), then reference practices. Draft explicit options, run pre-code `/grill`, and obtain recorded owner approval before UI implementation; unapproved drafts never count as consent (`docs/contracts/frontend-and-visual-discipline.md`). |
| Organizing information for readers (doc structure, navigation, screen content, knowledge or reference content) | Start from the reader and task, answer first, one organizing scheme per level, layered detail with context attached, form chosen from the question; for knowledge content scope by real-world impact, date current-state facts, and prove coverage claims (`docs/contracts/information-organization.md`). |
| Source files and CSS growth | Verify `owns` globs, keep `# Role:` headers on claimed files, stay within `max_source_lines` (`500`) / `max_style_lines` (`300`), and avoid catch-all `utils/` folders. |
| Substantive owner quote, trade-off, or direction change | Append exact unedited words to `docs/sources.toml` (`SRC-*`, chronological order, only quotes that substantively affect project direction), update owning spec or ADR, and link IDs in `docs/work.toml`. |
| Task execution, review cadence, or unattended mode | Complete authorized tasks cleanly, respect `[collaboration]` in `docs-policy.toml`, follow `templates/charter.md` when `unattended`, and load `.agents/skills/grill/SKILL.md` for `/grill` (`docs/contracts/delivery-and-verification.md`). |
| Independent review or verification | Run reviewers in a fresh context with author rationales withheld, start with an open holistic mandate across architecture, consistency, and user outcome, verify fixes back with original + fresh reviewers, and test real runtime behavior. For coverage or currency, reviewers list expectations before reading the deliverable and settle currency with dated sources retrieved during the review, never with any model's or person's memory; reviewers report findings and the owner confirms milestone status (`docs/contracts/delivery-and-verification.md#independent-review-definition`). |
| Discipline onboarding or version sync | Use `python3 scripts/read_rules.py onboard --target <path>` and follow `docs/contracts/adoption-and-synchronization.md` while keeping project-owned files intact. |

## 4. Direct Prohibitions Against Corner-Cutting

- **Run real execution paths and behavior checks**: Verify working CLIs,
  servers, or UI states rather than trusting mocked checks alone.
- **Keep independent review open, rationale-blind, and closed-loop**: Never
  pre-confine reviewers to narrow code checklists, supply author justifications,
  skip holistic architecture/consistency inspection, or mark a review closed
  without re-verifying fixes with the original critic and a fresh context.
- **Never treat unapproved drafts as owner sign-off**: Block pending design
  tasks in `docs/work.toml` until the owner chooses a direction explicitly.
- **Finish authorized tasks cleanly**: Complete implementation and checks
  end-to-end unless blocked on a real product decision.

## 5. Single-Source Commands & Identity Guard

- Inspect file/module context before editing: `python3 scripts/project.py context <path-or-id>`
- Inspect roadmap, directory layout, and blockers: `python3 scripts/project.py status` (use `project.py serve` only when inspecting approved web surfaces)
- Load review guidance & skill: `docs/guides/grill.md`, `.agents/skills/grill/SKILL.md`, `templates/independent-review.md`
- Ensure `docs-policy.toml` sets `identity = "product"` rather than copying `template` settings unchanged.
- Verify tests and structural rules:

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
python3 scripts/check_docs.py
```
