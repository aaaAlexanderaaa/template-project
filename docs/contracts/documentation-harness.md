---
doc_type: contract
status: current
authority: normative
implementation: implemented
verification_status: enforced
last_reconciled: 2026-07-26
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

> “模板自己的招牌特性，却没被强制。”

The review identified that the surface template requires raw-to-translated
citations while the shipped checker does not validate them.

### source[2] — 2026-07-26

> “同意，按你的理解进行优化。”

The operator approved a domain-neutral hardening pass, including the review's
valuable findings with configurable rather than project-specific mechanisms.

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

- from: source[1], source[2]

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
`last_reconciled + target_max_age_days`. An overdue target fails.

Promises use structured records rather than language-specific prose matching:

```text
- promise[example]: due=2026-07-26; status=resolved; owner=template-maintainer; description=syntax example only
```

An open promise past its explicit due date fails. Resolved or cancelled promises
remain as history. `last_reconciled` is not used to expire current contracts
merely because they are old.

- from: source[1], source[2]

### H4 — Templates are checked as first-class deliverables

`docs-policy.toml` declares required template files and required sections. The
checker validates their frontmatter shape, section inventory, standard
raw/source citation examples, structured promise example, placeholders, and
local links without treating them as current product contracts.

- from: source[1]

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

### H8 — Mechanical scope is honest

Every stable syntactic rule above has a checker or test. Rules requiring human
judgment remain explicit review gates and evidence requirements rather than
being represented by a vacuous automated pass.

- from: source[1], source[2]

## Required behaviors

- `python3 scripts/check_docs.py` validates the current repository.
- `python3 -m unittest discover -s tests -p 'test_*.py'` exercises checker
  fixtures without third-party dependencies.
- `--root` allows fixture repositories to be checked.
- `--today` makes aging tests deterministic.
- Failures name the document and concrete violated rule.
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

## Acceptance evidence

| Outcome | Enforcement | Evidence |
|---|---|---|
| Bidirectional UI and contract citations | Fixture tests + repository check | PASS — resolving, orphan, subsection, and layer-boundary cases |
| Configurable target and promise aging | Clock-controlled fixture tests | PASS — default age, override, and overdue promise cases |
| Templates validated as deliverables | Required-file/section/syntax fixtures | PASS — 14 required templates checked |
| Non-vacuous architecture adoption | Manifest and forbidden-pattern fixtures | PASS — adoption, no-match, escape, and literal cases |
| Optional abnormalities remain accountable | Registry/evidence fixtures | PASS — fresh, expired, resolving, and unregistered cases |
| Checker behavior remains stable | Standard-library unittest suite | PASS — 36 tests |
| Repository remains domain-neutral | Scoped forbidden-term, path, and framework audit | PASS — no matches |

Verification run on 2026-07-26:

- `uv run --python 3.11 python -m unittest discover -s tests -p 'test_*.py'`
  → PASS, 36 tests.
- `uv run --python 3.11 python scripts/check_docs.py --today 2026-07-26`
  → PASS, 12 canonical documents and 14 templates valid.
- `git diff --check` → PASS with no output.
- Scoped repository-independence `rg` audits → PASS with no matches.

## Reconciliation log

- **2026-07-26 — contract created:** the original minimal metadata checker is
  retained as a foundation but is insufficient for the template's declared
  reconciliation and environment-over-memory discipline.
- **2026-07-26 — implemented and enforced:** citation reconciliation, aging,
  template self-validation, architecture fitness, abnormality accountability,
  repository-contained references, and 31 fixture cases now form one portable
  documentation harness.
- **2026-07-26 — inventory extended:** registered the agent-governance and
  project-adoption records; 36 fixtures now protect 14 reusable templates.
