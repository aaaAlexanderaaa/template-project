---
doc_type: contract
status: current
authority: normative
contract_role: governance
implementation: implemented
verification_status: enforced
last_reconciled: 2026-08-28
supersedes: []
---

# Documentation harness contract

## Purpose

The repository's reusable value depends on its rules being mechanically
checkable where stable syntax can express them. This contract defines the
portable enforcement surface for source-to-spec reconciliation, document
lifecycle, template integrity, architecture fitness declarations, and optional
frontend abnormality records.

The checker validates structure and declared relationships. It does not claim
to judge whether prose, product decisions, or visual quality are semantically
correct.

## Scope

### In scope

- canonical documentation metadata and lifecycle;
- raw/source anchor definitions and bidirectional citations;
- configurable target-document aging and explicit promise deadlines;
- validation of the reusable templates themselves;
- adoption gates for product contracts and architecture fitness declarations;
- optional structured frontend abnormality records;
- an optional style-ownership declaration: layer partition and value-tier
  direction;
- local references and lifecycle relationship paths;
- fixture-based tests for the checker.

### Out of scope

- product-specific dependency names, roles, services, pages, or runtimes;
- language-specific AST or import analysis;
- visual measurement, browser automation, or product test frameworks;
- executing arbitrary commands declared by repository documentation;
- deciding product intent from prose.

## Source anchors

### source[1] — 2026-07-26

> “The template's own signature feature is not actually enforced.”

The review identified that the surface template requires raw-to-translated
citations while the shipped checker does not validate them.

### source[2] — 2026-07-26

> “Agreed. Optimize it according to your understanding.”

The operator approved a domain-neutral hardening pass, including the review's
valuable findings with configurable rather than project-specific mechanisms.

### source[3] — 2026-07-26

> "pls help me optimize this template project to make it suite to different
> scale of projects because sometimes the project is not such big or sometimes
> my project need CI... we need to make the workflow work smoothly instead of
> make agent pay a lot attention to fit it."

The harness described staged, scoped, and profiled adoption in prose while the
checker enforced exactly one profile, at one stage, with every finding blocking.
The operator asked for the mechanism to carry that variation instead of the
reader.

### source[4] — 2026-07-27

> "I noticed that in the front-end discipline of this project, the part about
> CSS modularization doesn't seem to have been emphasized. In fact, this is a
> very common and significant issue."

The frontend discipline specified reachable states, geometry, interaction,
accessibility, and evidence, but never named who owns a shared visual value or
in what order style layers win. The operator asked for that gap to be closed
against how large frontends actually decay.

### source[5] — 2026-07-28

> “Long-term governance should manage the existing stock: retirement,
> distillation, and summary, not only increment. Document coupling makes it
> easy for the same matter to appear in several documents, so that an update
> touches only one of them.”

### source[6] — 2026-08-28

> “How many symbol systems does the project have now? I see different
> encodings like J, D, and G, and it feels off.”

The owner approved the redesign direction: identify invariants by owning
contract and heading slug instead of letter codes, validate citation
fragments mechanically, and migrate contract by contract starting with the
newest.

## Operating modes

### Template mode

The repository contains no product implementation. Architecture and fitness
manifests may remain explicitly `unconfigured` / `template`. Reusable files
under `templates/` are validated for required metadata, sections, and reference
syntax while unresolved double-brace placeholders remain legal.

- from: source[1], source[2]

### Adopted mode

The configured source roots contain at least one product file. The structural
authority must be marked configured, the architecture fitness manifest must be
`configured` with at least one rule or `not_applicable` with a substantive
rationale, and at least one live product contract must be in implementation.

Which files count is a function of `[adoption].source_roots` and, in stage
`scoped_enforcement`, `[adoption].managed_paths`. Whether the gates block is a
function of `[adoption].stage`.

- from: source[1], source[2], source[3]

## Normative invariants

### H1 — Surface reconciliation is bidirectional

Every canonical `surface-contract`:

- contains `## Raw layer` before `## Translated layer`;
- defines at least one unique, dated `### raw[N] — YYYY-MM-DD` anchor;
- defines at least one `###` subsection inside `## Translated layer`;
- contains at least one resolving `- from: raw[N]` citation inside every
  translated subsection;
- cites only defined raw anchors from the translated layer;
- cites every defined raw anchor at least once from the translated layer.

An empty layer, uncited translated subsection, undated anchor, duplicate id,
unresolved citation, or orphan raw anchor fails the check. Citations outside the
translated layer do not satisfy reconciliation.

- from: source[1]

### H2 — Contract source anchors are conditionally bidirectional

A canonical contract may omit `## Source anchors`. If it declares that section,
it defines unique, dated `### source[N] — YYYY-MM-DD` anchors. Material after
the source-anchor section must cite every defined anchor, and every
`source[N]` citation must resolve.

- from: source[1]

### H3 — Lifecycle aging is explicit and configurable

`docs-policy.toml` owns repository-wide aging defaults. A target contract or
surface uses an explicit `review_due` when present; otherwise its deadline is
`last_reconciled + target_max_age_days`. An overdue target produces a
`target_aging` finding; its configured severity decides whether the run blocks.

Promises use structured records rather than language-specific prose matching:

```text
- promise[example]: due=2026-07-26; status=resolved; owner=template-maintainer; description=syntax example only
```

An open promise past its explicit due date produces an `overdue_promise`
finding. Resolved or cancelled promises remain as history. `last_reconciled` is
not used to expire current contracts merely because they are old.

- from: source[1], source[2]

### H4 — Templates are checked as first-class deliverables

`docs-policy.toml` declares the template inventory and required sections. The
checker validates their frontmatter shape, section inventory, standard
raw/source citation examples, structured promise example, placeholders, and
local links without treating them as current product contracts.

The inventory is selected by a cumulative profile — `minimal`, `standard`, or
`full` — rather than one fixed list, so a small project is not required to
carry ceremony it will never fill in. `[templates.doc_types]` owns the expected
`doc_type` of every template; a required template with no declared type fails
rather than silently skipping the assertion. An explicit `required_files` list
overrides the profile.

- from: source[1], source[3]

### H5 — Architecture fitness is declared without pretending to be universal

`architecture-rules.toml` is machine-readable. In adopted mode it is either:

- `configured`, with at least one non-vacuous path/pattern rule; or
- `not_applicable`, with a substantive rationale.

Configured rules scan declared file globs for forbidden literal dependencies or
references. Globs are repository-relative and cannot traverse into external
directories. Projects needing semantic import analysis add language-native
tests; the generic checker does not simulate an AST with regular expressions.

- from: source[2]

### H6 — Frontend abnormality records are optional but structured

When a canonical surface includes `## Known abnormality classes`, each entry
uses a stable `abnormality[slug]` record with state, evidence, guard, and
description. Pending evidence has an explicit date and expires according to
`docs-policy.toml`; durable evidence paths must resolve inside `docs/evidence/`.
Verification reports that cite an abnormality id must resolve it to a
registered surface entry.

Projects without frontend surfaces or accumulated abnormality classes incur no
registry requirement.

- from: source[1], source[2]

### H7 — The checker is tested as infrastructure

Lifecycle relationship fields use repository-root-relative paths. Local
Markdown links may be document-relative, but both forms must resolve inside the
repository; an existing external file does not make an escaping reference
portable.

Fixture tests cover valid and invalid citations, aging, promises, templates,
architecture adoption, abnormality records, lifecycle relationships, and local
links. Tests control their clock and write only to temporary directories.

- from: source[1]

### H8 — Enforcement stage and managed scope are inputs, not prose

`[adoption].stage` carries the enforcement stage from
`docs/contracts/project-adoption.md` into the checker. In `observed` and
`baselined` the adoption gates report without failing the build; from
`scoped_enforcement` onward they block. In `scoped_enforcement`,
`[adoption].managed_paths` narrows the governed file set to the boundaries the
owner has confirmed.

Product mode must not be decidable by one hard-coded directory name. When
source files exist outside every configured source root, the checker names the
offending paths rather than reporting a pass that gates nothing. That report is
itself stage-sensitive: like the adoption gates it advises in `observed` and
`baselined` and blocks from `scoped_enforcement` onward, so declaring an early
stage is enough to run the check in CI before the layout is configured.

Files directly in the repository root are exempt from that report. Build and
tooling configuration — `setup.py`, `conftest.py`, `vite.config.ts`, and their
equivalents — belongs to no source root in any layout, and demanding that an
adopter claim it would fail the first run for something the gates should never
have governed. Directory scans prune dependency and tool caches during the
walk, so cost stays proportional to the project rather than to what it vendors.

- from: source[3]

### H9 — Findings carry a severity, and only errors block

Every finding is an error, an advisory, or off. Structural contradictions —
missing metadata, unresolved citations, broken links, absent templates,
incoherent lifecycle — are errors. Findings caused solely by the passage of
time, by a documented artifact a lower profile legitimately drops, or by a
coupling change whose semantic impact still requires review default to
advisory: they are printed and the summary still passes.

`[severity]` retunes any listed rule; `--strict` promotes advisories to errors
for a scheduled job. A rule set to `off` stays off under `--strict`: switching
one off is a decision the project made, and a hygiene job reports harder rather
than overturning it. A repository that passed yesterday must not fail today
because a calendar date advanced and nothing else changed.

Policy keys are checked against what the checker actually reads. An unknown
`[adoption]` or `[severity]` key fails instead of being ignored, and a key
retired by a later revision names its replacement, so an upgrading adopter is
told how to migrate rather than losing the setting silently.

- from: source[3]

### H10 — Mechanical scope is honest

Every stable syntactic rule above has a checker or test. Rules requiring human
judgment remain explicit review gates and evidence requirements rather than
being represented by a vacuous automated pass.

- from: source[1], source[2]

### H11 — Style ownership is declared by the project, or not at all

`style-ownership.toml` does not ship. A project that owns no style creates no
file, the harness asks nothing of it, and that absence is a decision rather
than an unfinished adoption step.

When the file exists it declares `template`, `configured`, or `not_applicable`
in the same vocabulary as the architecture manifest. A `configured` declaration
names the style corpus and an ordered layer list, and every corpus file resolves
to exactly one layer. An unclaimed file is the failure that matters: where the
realizing mechanism grants undeclared style the highest authority, an omission
escalates rather than defaults. Declared value tiers may reference only tiers at
a lower position, which makes the reference graph one-way by construction rather
than by traversal.

The checker compares paths, array indices, and strings. It does not parse a
stylesheet, compute a specificity, or simulate a cascade. The literal forms a
project forbids its consumers to restate stay in that project's own
`architecture-rules.toml` rules, because the value classes worth governing and
the syntax expressing them differ per stack.

- from: source[4]

### H12 — Projection coupling and document stock stay visible

The documentation authority map owns the semantic rules for creating, merging,
summarizing, and retiring documents. The checker does not impose file-count,
line-count, directory-depth, or blanket retention-age budgets as quality or
deletion proxies and does not infer duplication from similar prose. H3's
target-review, promise, and pending-evidence deadlines remain in force.

Only a canonical current guide may declare `projection_of`, and it may target
only canonical current normative contracts or surface contracts. Paths are
repository-root-relative. A plan, evidence record, root entrypoint, template,
architecture file, non-current guide, or non-current/non-normative source is
outside this field's lifecycle matrix and produces a structural finding. If a
source leaves current authority, recovery reconciles the guide against a
current replacement or removes its projection and restatement; marking the
guide `needs_reconciliation` exposes the interim conflict but does not validate
the relationship.

If a projected source's `last_reconciled` date is later than the guide's, the
checker emits a configurable `projection_staleness` advisory. The advisory asks
for review rather than assuming that every source edit changes the projection.
Day-granularity dates cannot detect a later source edit on the same date, so the
check proves later-dated drift only; same-day ordering remains a review limit.

Lifecycle compatibility keeps retired stock out of false authority: `completed`
is reserved for plans, and a contract or surface with
`implementation: retired` cannot remain `current`. Supersession relationships
join canonical documents and remain bidirectional: a document with
`superseded_by` has status `superseded`, and the replacement names it through
`supersedes`. Both endpoints have the same `doc_type` and `authority`; a plan,
guide, or evidence record cannot become the replacement owner of a normative
contract. These checks govern coherent state, not how many historical records a
project is allowed to retain.

- from: source[5]

### H13 — Invariant citations resolve to headings

A normative invariant is identified by its owning document and its heading,
not by a letter code. New and migrated contracts title their invariants in
plain language without a code prefix. A cross-document citation is a Markdown
link whose fragment is the heading's slug — lowercased, punctuation removed,
spaces replaced by hyphens, the same rule renderers use for heading anchors.
Within a document, an invariant is cited by its short name in plain prose.

A Markdown link whose fragment does not resolve to a heading of the target
document produces a `fragment_resolution` finding. The default is advisory so
an adopting repository can switch the check on before reconciling legacy
links; a project that has completed its cutover may pin the rule to `error`.
Renaming a heading is a reference-breaking change: every fragment pointing at
the old heading is reconciled in the same change, never silently.

Letter-prefixed codes (D, G, A, O, H, INV, J) remain valid in contracts that
have not migrated. A contract migrates wholesale — headings and incoming
references in one change — and records the cutover in its reconciliation log.
Mixed form within one contract is a transition defect, not a style choice.

- from: source[6]

## Required behaviors

- `python3 scripts/check_docs.py` validates the current repository.
- `python3 -m unittest discover -s tests -p 'test_*.py'` exercises checker
  fixtures without third-party dependencies.
- `--root` allows fixture repositories to be checked.
- `--today` makes aging tests deterministic.
- `--strict` promotes advisories to errors and leaves `off` rules off.
- An unsupported interpreter fails with a version message before any
  version-specific import is attempted.
- Failures name the document and concrete violated rule.
- The summary line names the document count, template count, selected profile,
  and adoption stage, so a green check states what it actually enforced.
- Projection relationships resolve to normative sources, and stale projections
  are visible without turning a harmless source-date change into a per-push
  blocker.
- Markdown links carrying a heading fragment resolve to a heading of the
  target document; `fragment_resolution` findings are advisory until a
  project completes its cutover and retunes the rule.
- Template validation permits placeholders only under `templates/` and the
  intentionally unconfigured architecture skeleton.

## Forbidden behaviors

- Do not hard-code product vocabulary or framework-specific import semantics.
- Do not parse free-form promises by matching one natural language.
- Do not allow an empty configured architecture rule set to pass.
- Do not count historical, superseded, or not-started contracts as an adopted
  product's live implementation contract.
- Do not call a missing local evidence file valid because its Markdown is
  syntactically well formed.
- Do not execute arbitrary configured shell commands from the documentation
  checker.
- Do not parse a stylesheet, compute a specificity, simulate a cascade, or ship
  a default layer count, tier count, budget threshold, or forbidden literal.
- Do not enforce universal documentation counts, lengths, folder depths, or
  blanket retention ages as quality or deletion proxies, or use textual
  similarity as proof that two documents conflict.

## Acceptance evidence

| Outcome | Enforcement | Evidence |
|---|---|---|
| Bidirectional UI and contract citations | Fixture tests + repository check | PASS — resolving, orphan, subsection, and layer-boundary cases |
| Configurable target and promise aging | Clock-controlled fixture tests | PASS — default age, override, and overdue promise cases |
| Templates validated as deliverables | Required-file/section/syntax fixtures | PASS — every template the selected profile requires |
| Profiles scale the inventory | Profile-selection and trimmed-reference fixtures | PASS — lower tier still enforced, dropped tier not required, typos still fail |
| Adoption gates read the declared scope | Source-root, managed-path, and stage fixtures | PASS — outside-root detection, scope narrowing, and advisory stages |
| Configuration never fails an adopter for what it cannot own | Root-file, glob-harness, and vendored-tree fixtures | PASS — root tooling, `tools/**`, `node_modules/`, and `.venv/` all exempt |
| Retired and misspelled policy keys are refused | `[adoption]` and `[severity]` key fixtures | PASS — retired key names its replacement, typo is rejected |
| Non-vacuous architecture adoption | Manifest and forbidden-pattern fixtures | PASS — adoption, no-match, escape, and literal cases |
| Optional abnormalities remain accountable | Registry/evidence fixtures | PASS — fresh, expired, resolving, and unregistered cases |
| Optional style ownership stays optional and non-vacuous | Absent-file, partition, and tier-order fixtures | PASS — absent file changes nothing; unclaimed, double-claimed, vacuous corpus, and upward reference all fail |
| Projection coupling stays reviewable without volume quotas | Relationship, lifecycle, and clock-controlled fixtures | PASS — narrow guide/source types, later-date advisory, configurable/off behavior, lifecycle compatibility, and reciprocal canonical supersession |
| Severity is honest about what blocks | Advisory/error/off and `--strict` fixtures | PASS — time-based findings never fail a default run, and `off` survives `--strict` |
| Heading fragments stay resolvable | Fragment fixtures + repository check | PASS — resolving, broken, strict-promoted, and off-under-strict cases |
| Checker behavior remains stable | Standard-library unittest suite | PASS — full suite green |
| Repository remains domain-neutral | Scoped forbidden-term, path, and framework audit | PASS — no matches |

Counts are deliberately absent from this table: the checker's own summary line
and the fixture suite are the current inventory, and a number copied into prose
goes stale the next time a template is added.

Verification run on 2026-07-26:

- `python3 -m unittest discover -s tests -p 'test_*.py'` → PASS, full suite.
- `python3 scripts/check_docs.py --today 2026-07-26` → PASS.
- `python3 scripts/check_docs.py --today 2027-06-30` → PASS, confirming no
  shipped deadline can turn an adopter's build red on a date boundary.
- `git diff --check` → PASS with no output.
- Scoped repository-independence `rg` audits → PASS with no matches.

Verification run on 2026-07-28:

- `uv run --python 3.11 python -m unittest discover -s tests -p 'test_*.py'`
  -> PASS, full suite including projection, lifecycle, reciprocal relationship,
  severity, and template-route variants.
- `uv run --python 3.11 python scripts/check_docs.py --today 2026-07-28` -> PASS.
- The same repository check with `--strict` -> PASS.
- `git diff --check` and scoped trigger-duplication audits -> PASS with no
  findings.

Verification run on 2026-08-28:

- `uv run --python 3.11 python -m unittest discover -s tests -p 'test_*.py'`
  -> PASS, 110 tests including the heading-fragment cases.
- `uv run --python 3.11 python scripts/check_docs.py` -> PASS.
- The same repository check with `--strict` -> PASS, zero fragment findings
  with the pilot contract's slug citations in place.

## Reconciliation log

- **2026-07-26 — contract created:** the original minimal metadata checker is
  retained as a foundation but is insufficient for the template's declared
  reconciliation and environment-over-memory discipline.
- **2026-07-26 — implemented and enforced:** citation reconciliation, aging,
  template self-validation, architecture fitness, abnormality accountability,
  repository-contained references, and 31 fixture cases now form one portable
  documentation harness.
- **2026-07-26 — inventory extended:** registered the agent-governance and
  project-adoption records under the fixture suite.
- **2026-07-26 — scaled to project size:** the harness enforced one profile, at
  one stage, with every finding blocking, while the contracts described tiers,
  stages, and managed scope. Template profiles, `[adoption].stage`,
  `managed_paths`, source-root detection, recursive contract counting, and an
  error/advisory split moved that variation out of prose and into
  `docs-policy.toml`. Prose counts were removed in favour of the checker's own
  summary.
- **2026-07-27 — style ownership added:** the frontend discipline governed
  states, geometry, interaction, and evidence but never named who owns a shared
  visual value or in what order style layers win, so the decay large frontends
  actually suffer had no owner and no guard. Style ownership landed as an
  instance of D2 inside the existing frontend contract rather than as a second
  authority, a `style-system.md` template carried the project-level
  declaration, and an optional `style-ownership.toml` made layer partition and
  tier direction mechanically checkable without parsing a stylesheet. Glob
  safety was extracted into one shared resolver so both manifests reach the
  filesystem through the same escape checks.
- **2026-07-26 — review corrections:** review of that change found the scaling
  mechanisms could still fail an adopter for something they had decided or did
  not own. `--strict` promoted `off` rules to errors, overturning a project's
  own decision; repository-root tooling such as `setup.py` was reported as
  unclaimed product code, failing the first run of a stage that exists to be
  non-blocking; `source_root_configuration` ignored the declared stage;
  retired `[adoption]` keys were dropped silently on upgrade; and directory
  scans filtered dependency trees after walking them. Each is now fixed and
  covered by a fixture.
- **2026-07-28 — stock and coupling target landed:** document volume is not a
  quality metric, but intentional projections and lifecycle states are stable
  syntax. H12 adds a non-blocking projection reconciliation signal and lifecycle
  compatibility checks without textual duplication detection or document
  quotas. The checker and fixture suite now enforce typed projection paths,
  lifecycle coherence, reciprocal supersession, strict/off severity behavior,
  and the date signal's deliberately limited claim.
- **2026-08-20 — publication language:** source anchors originally recorded in
  Chinese are published as English renderings of the original authorizations.
  Meaning is unchanged. Already-English source wording is left as recorded.
- **2026-08-28 — invariant identifiers move to validated heading slugs:** the
  owner found the accumulating letter codes (D, G, A, O, H, INV, J) arbitrary;
  the deeper defect was that invariant references formed the repository's only
  unvalidated reference layer, so a mistyped or orphaned code could rot
  silently. H13 makes the heading the identifier, adds mechanical fragment
  validation (advisory by default, retunable per H9), and migrates contract by
  contract, newest first: the target engineering-judgment contract is the
  pilot. Letter codes remain valid in unmigrated contracts. Plan:
  `docs/plans/2026-08-28-invariant-identifier-redesign.md`.
  - from: source[6]
