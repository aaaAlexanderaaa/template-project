# Repository Working Agreement

This repository is the engineering discipline template (current `discipline_version`
lives in `docs-policy.toml`). It gives human owners and AI coding agents clear
engineering rules, single-owner documents, and Python scripts that check code
structure and explain the whole project clearly.

## 1. Priority Order

Apply these priorities in order whenever requirements pull against each other:

1. **Data safety and the requested outcome**: Protect user data, credentials,
   and destructive boundaries, and deliver the working result the owner asked
   for rather than extra paperwork.
2. **Shared vocabulary and single source of truth**: Give each concept one name
   and give every fact, state value, or threshold one authoritative owner file.
3. **Module boundaries, file role headers, and isolated styles**: Keep modules
   focused, declare each file's responsibility at the top of the file, and
   split CSS from shared tokens to component-local files.
4. **Stage- and environment-matched verification**: Run real end-to-end checks
   proportional to the domain stage (`prototype`, `usable`, `stable`) and
   collaboration mode (`interactive` vs `unattended`).
5. **Documentation and work-queue synchronization**: Update the owning spec,
   `docs/sources.toml`, or `docs/work.toml` when facts change without duplicating
   descriptions across files.

## 2. Three-Perspective Judgment Before Writing Code

Before choosing how much design or process a task needs, think from three roles
at once:

- **Executor**: Separate what the owner already decided from what remains open.
  Follow settled choices directly; challenge a constraint only when concrete
  evidence shows a clearly better alternative, and explain the trade-off plainly.
- **Collaborator**: Judge how close the request is to a stable design. Keep
  early exploration light so ideas move fast; once the direction settles, write
  clear boundaries into the owning module spec.
- **Senior Architect**: Check the target domain's `stage` (`prototype` 0->0.1,
  `usable` 0.1->1, `stable` 1->N) in `docs-policy.toml` or
  `docs/specs/<domain>/README.md`. Focus effort on what decides success at that
  stage—skip multi-subagent reviews on an unbuilt `0->0.1` prototype, and guard
  public interfaces and migrations strictly on a `stable` core.

## 3. Concrete Triggers (By Object and Effect)

Apply the linked rule whenever your work touches the object below:

| Concrete object or effect | Required action and rule owner |
|---|---|
| Any text read by humans or later AI sessions (`README.md`, `ARCHITECTURE.md`, specs, ADRs, CLI output, error messages, UI copy) | Use plain, direct language matching the project's chosen language: state what the object is, how it works, and what problem it solves; avoid coined jargon, stacked disclaimers, and raw enum tokens. Owner: [docs/README.md](docs/README.md#language-standard) |
| Any value read in more than one place (DB, API, memory, DOM, URL, or config) | Assign one authoritative owner and compute downstream copies mechanically. Owner: [architecture-and-modularity.md](docs/contracts/architecture-and-modularity.md#single-source-of-state) |
| Creating a file, adding a new responsibility, or growing code/CSS | Before adding files or growing one, read `python3 scripts/read_rules.py prepare --concern architecture` (and `--concern css` for styles). Every source and style file claimed by a spec's `owns` starts with a `# Role:` header, and files are split by responsibility before they pass the line budgets in `docs-policy.toml`, never by squeezing lines. Owner: [architecture-and-modularity.md](docs/contracts/architecture-and-modularity.md) |
| Architecture or module boundary description (`ARCHITECTURE.md`, domain/module specs) | Cover all five parts: positioning/non-goals, end-to-end runtime/control logic (`mermaid`), bounded interfaces & forbidden couplings, single-source state & hard invariants, and entrypoints/fitness checks. Owner: [architecture-and-modularity.md](docs/contracts/architecture-and-modularity.md#decomposition-and-ownership) |
| Product direction, interaction flow, or visual UI design (`docs/design/`, web pages) | Before any product or UI design work, read `python3 scripts/read_rules.py prepare --concern frontend`. Principles and the measurable WCAG 2.2 AA baseline always outrank style preferences, and no UI code is written before the owner records approval of a design option after a pre-code `/grill`. Owner: [frontend-and-visual-discipline.md](docs/contracts/frontend-and-visual-discipline.md) and [grill.md](docs/guides/grill.md) |
| Organizing information for readers (doc structure, navigation, screen content, knowledge or reference content) | Before structuring docs, screens, or knowledge content, read `python3 scripts/read_rules.py prepare --concern information`. Start from the reader's task and put the answer first. Owner: [information-organization.md](docs/contracts/information-organization.md) |
| Substantive owner quote, trade-off decision, or direction change | Read `python3 scripts/read_rules.py prepare --concern lineage`. Record the owner's exact words in `docs/sources.toml`; a quote behind a cross-module decision goes only into that ADR's `sources` with `affects`, never copied into module specs (`check_docs.py` reports copies). Owner: [collaboration-and-governance.md](docs/contracts/collaboration-and-governance.md#three-level-bidirectional-lineage) |
| Authorized task execution, review cadence, or unattended loop | Read `python3 scripts/read_rules.py prepare --concern verification`. Finish implementation with real verification scaled to the domain `stage` and `[collaboration]` mode; the owner decides when to run `/grill`, and agents only remind. Owner: [delivery-and-verification.md](docs/contracts/delivery-and-verification.md) |
| Independent review or requested `/grill` check | Load [.agents/skills/grill/SKILL.md](.agents/skills/grill/SKILL.md) and read `python3 scripts/read_rules.py prepare --concern review`. Reviewers work in a fresh context without the author's explanations and report findings; the owner decides status. Owner: [delivery-and-verification.md](docs/contracts/delivery-and-verification.md#independent-review-definition) |
| External learning (`"learn from template-project"`), onboarding, or template transfer | Read `python3 scripts/read_rules.py prepare --concern onboarding`. Inventory with `python3 scripts/read_rules.py onboard --target <path>`, adopt with `python3 scripts/project.py init --target <path>`, upgrade with `python3 scripts/project.py init --target <path> --sync`, and keep `template-project` internal names out of generated output. Owner: [adoption-and-synchronization.md](docs/contracts/adoption-and-synchronization.md) and [onboarding.md](docs/guides/onboarding.md) |

## 4. Direct Prohibitions Against Corner-Cutting

- **Run real execution paths and behavior checks**: Verify changes on real CLI commands, servers, UI screens, and downstream project transfer scenarios rather than relying only on unit tests or doc-extractor checks.
- **Finish authorized tasks cleanly**: Complete implementation, integration, and verification instead of stopping mid-task with a `"Next steps"` list unless a genuine product decision or hard blocker needs the human owner.
- **Keep independent review open, free of the author's explanations, and closed-loop**: Never pre-confine an independent reviewer to code details, feed the author's defense, skip architecture/consistency inspection, or declare a review complete before re-verifying fixes with the original reviewer and a fresh context.
- **Never treat unapproved drafts as owner sign-off**: Wait for explicit owner choice on `docs/design/` alternatives before locking a UI architecture, visual style, or layout.
- **Prevent monoliths and catch-all folders**: Split oversized files before exceeding line budgets, avoid vague `utils / helpers / common` folders, and keep component CSS out of global layout stylesheets.

## 5. Navigation & Verification Commands

Every project fact lives in one file and is linked mechanically by `scripts/`:

- **Load context before editing an unfamiliar file, doc, or module**:
  `python3 scripts/project.py context <path-or-id>`
- **Inspect project roadmap, directory map, and review accumulation**:
  `python3 scripts/project.py status` (`python3 scripts/project.py serve` shows the same information as a local web overview, specified in [docs/design/perspective-web.md](docs/design/perspective-web.md))
- **Run tests and rule checks** (Python 3.11+, or older Python with `tomli` installed):

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
python3 scripts/check_docs.py --strict
```

## 6. Copied Checkout Guard

Onboarding into another repository is incomplete while its `AGENTS.md` or
`docs-policy.toml` still identifies it as this template (`identity = "template"`)
and its git remote is not `https://github.com/aaaAlexanderaaa/template-project`.
