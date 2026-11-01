---
doc_type: contract
status: current
authority: normative
contract_role: governance
implementation: implemented
verification_status: enforced
last_reconciled: 2026-11-01
reading_entrypoint: harness
supersedes: []
---

# Documentation harness contract

<!-- required-reading: harness -->
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
- an opt-in lexical signal for disclaimer phrasing in startup rules;
- local references and lifecycle relationship paths;
- fixture-based tests for the checker.

### Out of scope

- product-specific dependency names, roles, services, pages, or runtimes;
- language-specific AST or import analysis;
- visual measurement, browser automation, or product test frameworks;
- executing arbitrary commands declared by repository documentation;
- deciding product intent from prose.

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

### Surface reconciliation is bidirectional

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

### Contract source anchors are conditionally bidirectional

A canonical contract may omit `## Source anchors`. If it declares that section,
it defines unique, dated `### source[N] — YYYY-MM-DD` anchors. Contract text
outside that section must cite every defined anchor through `from:` lines,
and every such `source[N]` citation must resolve. Citations may precede or
follow the source section; citations inside it cannot satisfy coverage.
This permits operative rules before provenance while retaining missing,
unused, duplicate, and invalid-date findings. Surface raw-to-translated
reconciliation retains its separate, layer-specific scope.

Every citation line carries a short human gloss — the anchor's date and topic
in parentheses — so provenance is readable where it is cited rather than only
at the anchor list: `- from: source[2] (2026-09-15 alignment decisions)`.
Raw citations follow the same convention. The checker still validates only the
anchor ids; the gloss is prose, and it states facts that cannot rot: the date
and subject of a dated source. New citations are glossed when written;
existing bare citations are backfilled when their section is next touched, not
in one sweeping edit. `scripts/scan_letter_codes.py` reports letter-number
tokens grouped by document liveness as health-assessment material; it is
deliberately outside the checker's blocking surface, because a code in frozen
history is expected and only accumulation in living prose is a signal.

- from: source[1] (2026-07-26 enforcement-gap review), source[8] (2026-09-15 readable-citation instruction)

### Lifecycle aging is explicit and configurable

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

### Templates are checked as first-class deliverables

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

The retained unit-test command works after an adopter removes templates outside
the selected profile. Tests of unavailable optional templates report explicit
skips; required-template checks and general checker/reader tests still run.
Fixture profile changes do not assume the source checkout uses `full`.

- from: source[1], source[3]

### Architecture fitness is declared without pretending to be universal

`architecture-rules.toml` is machine-readable. In adopted mode it is either:

- `configured`, with at least one non-vacuous path/pattern rule; or
- `not_applicable`, with a substantive rationale.

Configured rules scan declared file globs for forbidden literal dependencies or
references. Globs are repository-relative and cannot traverse into external
directories. Projects needing semantic import analysis add language-native
tests; the generic checker does not simulate an AST with regular expressions.

- from: source[2]

### Frontend abnormality records are optional but structured

When a canonical surface includes `## Known abnormality classes`, each entry
uses a stable `abnormality[slug]` record with state, evidence, guard, and
description. Pending evidence has an explicit date and expires according to
`docs-policy.toml`; durable evidence paths must resolve inside `docs/evidence/`.
Verification reports that cite an abnormality id must resolve it to a
registered surface entry.

Projects without frontend surfaces or accumulated abnormality classes incur no
registry requirement.

- from: source[1], source[2]

### The checker is tested as infrastructure

Lifecycle relationship fields use repository-root-relative paths. Local
Markdown links may be document-relative, but both forms must resolve inside the
repository; an existing external file does not make an escaping reference
portable.

Fixture tests cover valid and invalid citations, aging, promises, templates,
architecture adoption, abnormality records, lifecycle relationships, and local
links. Tests control their clock and write only to temporary directories.

- from: source[1]

### Enforcement stage and managed scope are inputs, not prose

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

Root application files receive the same source-scope check as nested files.
Declare product directories or individual files in `source_roots`; a declared
file activates adoption gates. Declare build and tooling paths through
`harness_paths`, including the shipped root-tooling examples. Location alone
does not establish that a file is tooling. Directory scans prune dependency and
tool caches during the walk, so cost stays proportional to the project rather
than to what it vendors.

- from: source[3]

### Findings carry a severity, and only errors block

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

### Mechanical scope is honest

Every stable syntactic rule above has a checker or test. Rules requiring human
judgment remain explicit review gates and evidence requirements rather than
being represented by a vacuous automated pass.

- from: source[1], source[2]

### Complete rule delivery is a read-only transaction

`scripts/read_rules.py` supplies local source text before task choices depend on
it. `list` displays the current concern table. `prepare` starts at explicit
entrypoint dependencies, adds every selected concern's Required reading links
and supplied owner bindings, resolves their explicit dependencies, and emits
one manifest followed by complete bodies (or explicit same-context retention
labels below) and a final `READING COMPLETE` marker. Each preparation resolves
anew, including when a caller reuses the Python repository object. It snapshots
bytes in memory and checks all source identities again
before emission; a changed source aborts preparation and requires a fresh run.
The manifest names repository path, stable unit identity, heading, authority,
lifecycle, SHA-256 content and file digests, and byte count. Output is UTF-8.
LF and CRLF metadata delimiters are both supported. Source digests, byte counts,
emitted bodies and recovery parts retain the original bytes and line endings.
When a selected whole document covers a selected unit from that same file,
emit only the whole document. Still traverse every explicit dependency and
check cycles before removing covered bodies; external prerequisites remain.

Declared units use paired comments outside fenced examples:

```markdown
<!-- required-reading: frontend -->
## Frontend development contract
The complete operative section and its subsections go here.
<!-- /required-reading: frontend -->
```

An identifier is a lowercase ASCII slug unique within the file; `document` is
reserved for the whole-document fallback. Markers are non-nested and matched.
A unit begins at a heading and ends after its complete operative content;
closing a unit in the middle of a section's prose is invalid. Units can cover
several peer sections, allowing provenance to remain outside an operative unit.
A required heading resolves to its enclosing unit, or the complete document
when no unit encloses it. Ordinary heading navigation and stable unit identity
remain distinct: renaming a heading reconciles incoming navigation links.
An owner may publish `reading_entrypoint: UNIT` in frontmatter. File-only
references then select that declared complete operative unit; `#document`
explicitly requests the whole file. Without that field, whole-file fallback
is unchanged. A missing, malformed or undeclared entrypoint is an error.
Owners review semantic completeness; marker, heading coverage and relationship
checks establish syntax only.

Only an explicit directive creates a dependency:

```markdown
- required-reading: [Concern routing](development-discipline.md#activate-concerns-instead-of-expanding-ceremony)
```

Directives resolve relative to their containing document. CLI references resolve
relative to the repository root. Fenced examples do not declare units or edges.
Ordinary Markdown links do not create edges. Missing anchors, malformed units,
duplicate identifiers, dependency cycles, unsupported lifecycle, and paths
escaping the repository, including through symlinks, fail with a repair location.
Historical or superseded documents are references, not operative reading.
`prepare --target REFERENCE` explicitly includes a target rule for governed
future work and labels it as target; it never silently changes current authority.

The [concern table](development-discipline.md#activate-concerns-instead-of-expanding-ceremony)
is the only trigger registry. Its Required reading cells contain Markdown links
and/or `owner:concern-slug`. The command validates that a supplied concern exists,
its bindings belong to a selected owner slot, and every selected slot is bound.
A bound owner is a canonical normative contract or surface, current or explicitly
selected target. A contract's omitted role defaults to `product`, consistently
with the documentation checker; an explicit role is `product` or `governance`.
Governance contracts identify that role explicitly. Surfaces declare an identity
and compatible UI scope. Multiple bindings for one concern are allowed. The
operator verifies their task/interface identity and source authority against
architecture and accepted intent; type checks alone cannot establish that match.
Experience can bind a command-line or other non-graphical contract. Graphical
surface owners declare the complete frontend reading dependency; the reader
follows that declaration without imposing frontend ownership on other interfaces.

```sh
python3 scripts/read_rules.py list
python3 scripts/read_rules.py prepare --concern analytical-claims
```

`prepare --include REFERENCE` adds an explicitly selected current method or
rule and its complete dependencies. It does not activate authority, choose
priority or waive another applicable concern. Targets still need `--target`.

For repeated preparation within one live reading context, `--context ID`
labels its manifest. `--retained PATH` consumes a previous version-2 manifest
with the same context label. Supplying it asserts that every reused full body
is still available in that context: a manifest or summary alone supplies no
such evidence. Restart, handoff, unknown retention or a different context uses
fresh preparation without that input. The tool cannot inspect model memory;
context labels detect accidental mix-ups rather than certify comprehension.

Preparation always resolves the current selection, owners, lifecycle and full
dependency graph before considering retention. It compares stable identity,
exact body bytes/digest, authority, status and the complete metadata digest.
New or changed units are emitted; matching units are explicitly marked retained.
An edit outside a retained unit can leave its body valid; the current manifest
still refreshes the whole-file digest used for recovery. Changed metadata is
conservatively reacquired. Missing sources, invalid owners, cycles or malformed
receipts fail before output; no old receipt can make invalid current rules pass.

Every manifest states the complete selected units and distinguishes emitted
from caller-asserted retained bodies. The final marker reports those counts
when reuse occurs. It is not proof of new delivery for retained text. Full
preparation and digest-checked recovery remain available. This interface reads
caller-managed task data; it creates no persistent cache, task registry or
authority store and writes no file.

If output is truncated, recover the missing complete unit with
`read --unit PATH#UNIT --digest EXPECTED_SHA256`; the expected digest covers the
entire source file, so a changed boundary or metadata also invalidates recovery.
For output-limited environments, add `--part N --part-size BYTES`. Parts preserve
UTF-8 characters and exact original text, identify part number/total and source
digest, and carry completion markers. Obtain every part before dependent work.
The final aggregate marker or all recovered parts establishes delivered source,
not understanding, correct application, or user success. Those require the
task's artifact and outcome evidence. Memory, manifests and summaries are locators.

The command reads contained local Markdown as data, never executes its contents,
and uses no network or persistent cache. It cannot intercept every agent decision
or force host injection. An optional host adapter needs its own verified boundary.
Where the command is unavailable, directly obtain the same complete units and
their identities. An ordinary file lookup retains the direct route owned by
[task context](../README.md#task-context).

The documentation checker validates declarations and all explicit dependency
closures, including required table targets and owner-slot syntax. It does not
guess concern selection from prose, certify a supplied owner's semantic fit,
or claim that a reader applied the emitted rules.

- from: source[11] (2026-10-28 complete rules and useful delivery), source[12] (2026-10-29 connected operating interfaces)

### A copied template entrypoint is unfinished onboarding

When `AGENTS.md` still contains any identity claim listed in
[the existing-directory rule](project-adoption.md#an-existing-directory-is-described-before-template-files-are-added)
and the directory has a `.git` directory, the checker requires a git remote
for https://github.com/aaaAlexanderaaa/template-project. One remaining claim
is enough. Another remote, or no remote, is unfinished onboarding. A tree
without `.git` is outside this check. The adoption contract still requires
git before template files are added to a directory that already holds files.
The template's own checkout passes because its remote is that repository.

- from: source[9] (2026-10-02 copied entrypoint is unfinished onboarding), source[10] (2026-10-02 any remaining identity claim is enough)

### Style ownership is declared by the project, or not at all

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

### Projection coupling and document stock stay visible

The documentation authority map owns the semantic rules for creating, merging,
summarizing, and retiring documents. The checker does not impose file-count,
line-count, directory-depth, or blanket retention-age budgets as quality or
deletion proxies and does not infer duplication from similar prose. The lifecycle-aging invariant's
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

### Invariant citations resolve to headings

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
New contract templates must expose invariants as plain-language third-level
headings. The checker requires at least one such heading in their Normative
invariants section and rejects letter-number identifiers used as headings or
list labels there. This guard applies to selected contract templates, not to
unmigrated adopter contracts, source quotations, or historical records. It
validates addressable syntax, not the quality or completeness of a rule.
References inside completed plans, dated evidence files, blockquoted source
anchors, and reconciliation-log entries are history: they stay as written,
and a reader resolves an old code through the owning contract's
reconciliation log. Dated verification entries inside a living contract's
acceptance-evidence section are a current status surface, not history.

- from: source[6]

### Startup rules are scanned for disclaimer phrasing

Every agent reads the required-reading closure of `AGENTS.md` and the
entrypoint itself, and later writers copy the form of what they read. The
checker scans that text for a short list of phrases that usually begin a
sentence saying what a rule, record or result is not, such as "does not
establish", "alone does not", "need not" and "creates no". Quoted text, inline
code, fenced examples, `from:` citations and reading markers are mentions and
are skipped; a phrase broken across lines still matches. When a project sets
`rule_phrasing` to `advisory` or `error`, each hit names the line and points
to the [language rule](../README.md#language-style). The rule is off by
default.

The signal is lexical: it finds the stock forms, a reworded disclaimer passes
it, and whether a reader can act on a rule is judged in a concrete task. Most
listed phrases also mark a limit on what evidence shows or a permission, which
the language rule keeps, so rewriting toward fewer hits can drop or strengthen
the rule itself. Each finding therefore asks a writer to keep such a sentence,
and to reword it only when one case it excluded and one it allowed are decided
the same way afterwards. The signal bans no vocabulary and stays within the
startup rules.

- from: source[13] (2026-11-01 positive rule wording)

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
- When `rule_phrasing` is enabled, startup rules that use a listed disclaimer
  phrase outside quotes, code and citations produce a finding naming the line;
  the rule is off by default.

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
| Source identity follows declarations rather than root location | Root-application, declared-file, glob-harness, and vendored-tree fixtures | Explicit tooling exemptions remain; root application files must be claimed |
| Retired and misspelled policy keys are refused | `[adoption]` and `[severity]` key fixtures | PASS — retired key names its replacement, typo is rejected |
| Non-vacuous architecture adoption | Manifest and forbidden-pattern fixtures | PASS — adoption, no-match, escape, and literal cases |
| Optional abnormalities remain accountable | Registry/evidence fixtures | PASS — fresh, expired, resolving, and unregistered cases |
| Optional style ownership stays optional and non-vacuous | Absent-file, partition, and tier-order fixtures | PASS — absent file changes nothing; unclaimed, double-claimed, vacuous corpus, and upward reference all fail |
| Projection coupling stays reviewable without volume quotas | Relationship, lifecycle, and clock-controlled fixtures | PASS — narrow guide/source types, later-date advisory, configurable/off behavior, lifecycle compatibility, and reciprocal canonical supersession |
| Severity is honest about what blocks | Advisory/error/off and `--strict` fixtures | PASS — time-based findings never fail a default run, and `off` survives `--strict` |
| Heading fragments stay resolvable | Fragment fixtures + repository check | PASS — resolving, broken, strict-promoted, and off-under-strict cases |
| Startup rules state actions | Phrasing fixtures + repository check | PASS — listed, wrapped, quoted, entrypoint, out-of-scope, and off-under-strict cases |
| Checker behavior remains stable | Standard-library unittest suite | PASS — full suite green |
| Repository remains domain-neutral | Scoped forbidden-term, path, and framework audit | PASS — no matches |

Counts are deliberately absent from this table: the checker's own summary line
and the fixture suite are the current inventory, and a number copied into prose
goes stale the next time a template is added.

<!-- /required-reading: harness -->

## Verification history

The [September 7 change record](../plans/2026-09-06-proportionate-execution.md#progress-and-closure)
records passing source-order, unresolved-reference, self-citation, and
definition-validation fixtures. Surface translation checks remain unchanged.

The [2026-09-06 completed change](../plans/2026-09-06-outcome-driven-template.md#progress-and-closure)
records the failing-before/passing-after scaffold guard, including coded
heading and list variants and preserved legacy history. The full 114-test
suite and normal/strict checks passed. This establishes the declared syntax
boundary, not semantic quality or agent behavior.


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

### source[7] — 2026-09-07

The maintainer authorized current task rules before historical provenance.
The source checker must preserve bidirectional reconciliation without forcing
the source-anchor block ahead of operative contract text.

### source[8] — 2026-09-15

> English rendering of the maintainer's instruction: internal numbering used
> as a point-of-use reference is a baseline readability defect — citations
> should describe themselves, and a quick repository scan for letter-number
> tokens should exist as health-assessment material, not as a mechanical
> test.

Context: alignment follow-up after the autonomous-operation contract landed;
the maintainer approved the citation-gloss convention and requested the scan.

### source[9] — 2026-10-02

English paraphrase of the maintainer's decision: onboarding is unfinished
while the agent entrypoint still describes the checkout as the documentation
and project-discipline template and the git remote is not this template's
repository. The checker reports that mismatch when the directory is a git
repository.

### source[10] — 2026-10-02

English paraphrase of the maintainer's choice: the checker reports unfinished
onboarding when any listed identity claim remains in the agent entrypoint and
the git remote is not this template's repository. Removing one sentence while
leaving another claim is still unfinished.

### source[11] — 2026-10-28

The owner requested practical rules that preserve purpose and make detailed
requirements reliably available, then authorized implementation of the
[reviewed design](../plans/2026-10-28-rule-reading-and-outcome-design.md).
This is an English account of the current conversation. The implemented
protocol belongs here; the plan records its design rationale and review.

### source[12] — 2026-10-29

The owner described rising foreground attention and ineffective accumulation
as a systems-engineering problem and accepted continuing with the connected
task lifecycle. Publishing operative entrypoints and stateless same-context
preparation are executor-selected interfaces within that accepted design.
They preserve source integrity, current authority and fresh restart; they do
not establish comprehension, sustained savings or real-project adoption.

### source[13] — 2026-11-01

English account of the current conversation. An external review found that
the rules mostly say what not to do. The owner agreed, attributed the pattern
to the previous maintaining model's over-caution and habit of disclaimers,
said earlier corrective requirements had not worked well enough, and asked for
it to be handled. The implementer rewrote the startup rules in action form and
chose this advisory as a detection surface, because another written
requirement would repeat the remedy that had not worked. Independent review of
the rewrite found that phrase-driven rewriting had dropped or changed limits,
and later reviewers noted that most listed phrases mark such limits or
permissions, so each hit nudges a writer toward that failure. The implementer
made the signal opt-in, left it off in this repository, and changed its
message to keep such sentences. Asked whether to keep it off, enable, narrow
or remove it, the owner chose to keep it off.

## Reconciliation log

- **2026-11-01 — startup rules scanned for disclaimer phrasing:** the
  required-reading closure of `AGENTS.md` and the entrypoint itself can be
  scanned by an opt-in `rule_phrasing` rule, off by default, for a short list
  of disclaimer phrases; quoted text, code and citations are mentions and are
  skipped. Each finding asks the writer to keep a sentence that limits or
  permits, and to reword it only when its cases are decided the same way.
  - from: source[13] (2026-11-01 positive rule wording)

- **2026-10-29 — revalidated operating interfaces:** published operative
  entrypoints, explicit method inclusion and caller-asserted same-context
  retention. Preparation resolves current rules anew and remains read-only;
  full source, recovery and fresh acquisition remain available.
  - from: source[12] (2026-10-29 systems-engineering continuation)

- **2026-10-28:** Define contained source resolution, complete units, explicit
  dependencies, owner bindings, digest-checked recovery and honest evidence scope.

- **2026-10-02 — any remaining identity claim fails the checker:** one claim
  that the checkout is this discipline template, with a git remote that is
  not the template repository, is unfinished onboarding.
  - from: source[10]

- **2026-10-02 — copied template entrypoint fails the checker:** an agent
  entrypoint that still describes the checkout as this discipline template
  must have a git remote for the template repository. Another remote, or no
  remote, is unfinished onboarding.
  - from: source[9]

- **2026-09-15 — citations carry glosses; letter codes stay visible:** source
  and raw citation lines now carry a date-and-topic gloss so provenance is
  readable at the point of citation, with bare citations backfilled as
  sections are touched; `scripts/scan_letter_codes.py` reports letter-number
  tokens grouped by document liveness as health-assessment material,
  deliberately outside the checker's blocking surface.
  - from: source[8] (2026-09-15 readable-citation instruction)

- **2026-09-07 — source placement is independent of reconciliation:** contract
  citations count outside the source block regardless of order, permitting
  current rules before provenance without weakening reference integrity or
  changing surface translation checks.
  - from: source[7]

- **2026-09-06 — copied invariant syntax:** extended the existing heading
  convention to a fixture-backed check of new contract scaffolds, which still
  shipped `INV-1` list items after the original migration.
  - from: source[6]

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
- **2026-08-28 — remaining namespaces migrated:** the owner directed the
  cutover of the remaining contracts the same day. D, G, A, O, INV, and this
  contract's own H codes were retired; foundational-runtime's labeled list
  items became `###` headings so every invariant is a linkable target.
  References in completed plans and dated evidence stay as written — they are
  history, and old codes resolve through these log entries. With no unmigrated
  contract left, this repository pins `fragment_resolution` to `error`; the
  advisory default remains for adopters mid-cutover.
  - from: source[6]
