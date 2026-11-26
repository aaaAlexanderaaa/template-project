---
id: graph.model
domain: graph-engine
kind: module-spec
summary: "Pure dataclasses, thin YAML frontmatter parser, Mermaid extractor, and SHA-256 digest-checked rule reader."
promise: "Markdown frontmatter, headings, links, Mermaid blocks, and rule spans parse deterministically using only the Python standard library."
owns:
  - "scripts/projectlib/__init__.py"
  - "scripts/projectlib/model.py"
  - "scripts/projectlib/frontmatter.py"
  - "scripts/rule_reading.py"
depends_on: []
sources:
  - SRC-020
---

# Graph Model, Frontmatter Parser & Rule Reader

## 1. Purpose, Public Interface & Non-Goals

- **Public interface**: Dataclasses (`ProjectGraph`, `DomainSpec`, `ModuleSpec`, `DecisionRecord`, `SourceAnchor`, `Milestone`, `WorkTask`, `ValidationFinding`), `module_source_refs`, `match_path_pattern`, `matches_any_pattern`, `normalize_doc_roots`, `parse_frontmatter`, `extract_markdown_structure`, `has_inline_role_header`, and `RuleRepository`.
- **Out of scope**: Disk filesystem walks, Git subprocess calls, HTTP handling, or TOML writes.

## 2. Parsing & Digest-Verified Rule Flow

```mermaid
flowchart LR
  Raw["Markdown / Span Text"] --> Parse["parse_frontmatter + extract_markdown_structure"]
  Parse --> Slugs["Heading Slugs + required-reading Anchors + Mermaid Blocks"]
  RuleRef["read_rules.py read --unit --digest"] --> Check{"Digest >= 6 Hex Chars & Prefix Match?"}
  Check -->|Match| Emit["Print Full Rule Unit Bytes"]
  Check -->|Empty or Mismatch| Reject["Raise RuleError (Exit 1)"]
```

## 3. State Ownership, Hard Invariants & Forbidden Couplings

- **Pure Base Invariant**: `model.py` and `frontmatter.py` accept text/values only and never import sibling `projectlib` modules or execute shell commands (`depends_on: []`).
- **Digest Integrity Guard**: `RuleRepository.read` rejects empty or short `< 6`-character digests so callers cannot bypass SHA-256 verification.
- **Verification**: Covered by `tests/test_ssot_and_check_docs.py` and `tests/test_read_rules_and_onboard.py`.
