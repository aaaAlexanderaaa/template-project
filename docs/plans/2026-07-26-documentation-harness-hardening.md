---
doc_type: plan
status: completed
authority: planning
last_reconciled: 2026-07-26
implements: docs/contracts/documentation-harness.md
supersedes: []
---

# Documentation harness hardening plan

## Cold-start summary

At the start of this plan, the template repository validated canonical
metadata, directory routing, local links, unresolved canonical placeholders,
and a minimal product adoption gate. It did not validate its raw/source
reconciliation syntax, age target documents, validate the templates themselves,
require a non-vacuous architecture fitness declaration, structure optional
frontend abnormalities, or test the checker.

This plan implements the complete target defined in
[documentation-harness.md](../contracts/documentation-harness.md) without
introducing product-specific tooling.

## Complete end state

One dependency-free command validates canonical docs, reusable templates,
configured lifecycle policy, source/spec citations, explicit promises,
cross-document paths, optional abnormality records, and architecture adoption.
A standard-library fixture suite proves every failure class. The untouched
template repository passes in template mode; copied repositories fail loudly
when product code appears before contracts and architecture fitness are
configured.

## Execution order within one coherent change

### 1. Standardize machine-readable contracts

- Add `docs-policy.toml` with configurable aging, template inventory, source
  roots, and abnormality policy.
- Add `architecture-rules.toml` with explicit template/configured/not-applicable
  states and a portable forbidden-reference rule schema.
- Update surface, contract, verification, architecture, and guidance templates
  to use the exact syntax in the normative contract.

### 2. Refactor the checker

- Add `--root` and `--today`.
- Load policy and architecture TOML through the Python standard library.
- Validate canonical metadata, relationship paths, citations, aging, promises,
  templates, abnormality records, and adopted-mode architecture rules.
- Keep natural-language judgment and arbitrary command execution out of scope.

### 3. Add class-level fixture tests

- Replace the test placeholder with a standard-library unittest module.
- Cover valid and invalid sibling variants for every new invariant.
- Execute the current repository check as a smoke test.

### 4. Wire verification and close lifecycle

- Update the CI example to run both unittests and repository validation.
- Run whitespace, documentation, unit, independence, and Git checks.
- Update the contract to current/implemented/enforced, attach command-level
  evidence, and mark this plan completed.

## Risk register

| Risk | Prevention |
|---|---|
| Markdown parsing becomes format-fragile | Declare a small exact grammar and test it with fixtures. |
| Fixed aging policy is unsuitable elsewhere | Put thresholds in `docs-policy.toml` and allow per-doc `review_due`. |
| Architecture check pretends to understand every language | Limit the generic rule to declared paths and literal forbidden references. |
| Template placeholders fail canonical checks | Use a separate template-validation mode with explicit allowed placeholders. |
| Optional UI mechanisms burden non-UI projects | Activate abnormality rules only when a surface declares the section. |
| Checker regressions silently weaken discipline | Test each valid/invalid class with a deterministic clock. |

## Verification matrix

| Outcome | Check | Evidence |
|---|---|---|
| Repository docs and templates are structurally valid | `python3 scripts/check_docs.py` | PASS — four canonical documents and nine templates |
| Checker failure classes are guarded | `python3 -m unittest discover -s tests -p 'test_*.py'` | PASS — 31 tests |
| Changed content is whitespace-clean | `git diff --check` | PASS — no output |
| No source-project terms, absolute paths, or framework names leaked | scoped `rg` audit | PASS — no matches |
| Working tree closes cleanly | `git status --short` after commit | final handoff check |

## Explicit non-goals

- No product implementation.
- No browser, CSS, runtime, service, or model-specific check.
- No universal import parser.
- No execution of commands read from documentation.
- No automatic judgment of whether stakeholder intent was translated well.

## Progress log

- **2026-07-26 — in progress:** contract and coherent implementation plan
  landed before checker changes.
- **2026-07-26 — completed:** configurable policies, exact citation syntax,
  template validation, target/promise aging, architecture fitness declarations,
  optional abnormality records, repository-contained references, CI example,
  and 31 clock-controlled fixture tests landed as one coherent harness.
