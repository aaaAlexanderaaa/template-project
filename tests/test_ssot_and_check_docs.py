# Role: Tests single-source graph stitching, boundary/link/budget/adoption checks, and git-diff source quote nudges.
# Out of scope: HTTP server endpoint tests (covered by test_project_cli_and_server.py).
# Anchors: spec=graph.model, spec=graph.indexer, spec=graph.validator, ADR-002, SRC-010, SRC-017, SRC-018

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from projectlib.frontmatter import extract_markdown_structure, parse_frontmatter  # noqa: E402
from projectlib.loader import load_project_graph  # noqa: E402
from projectlib.validator import validate_project_graph  # noqa: E402


def _write(base: Path, rel: str, content: str) -> None:
    p = base / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")


def _build_minimal_repo(base: Path, *, stage: str = "enforced", default_stage: str = "usable") -> None:
    _write(
        base,
        "docs-policy.toml",
        f'''version = 2
discipline_version = "2026.11"

[project]
name = "Fixture App"
identity = "product"
default_stage = "{default_stage}"
source_roots = ["src"]

[adoption]
stage = "{stage}"

[budgets]
max_source_lines = 40
max_style_lines = 25
forbid_catchall_dirs = ["utils", "helpers"]
''',
    )
    _write(
        base,
        "ARCHITECTURE.md",
        """# Fixture App

Single-source fixture architecture for testing mechanical graph stitching.

```mermaid
flowchart LR
  UI --> Core
```
""",
    )
    _write(
        base,
        "docs/sources.toml",
        """[[sources]]
id = "SRC-001"
date = "2026-11-15"
status = "active"
context = "Initial user goal"
quote = '''希望一个事实只在一个地方维护，脚本把它们串联起来。'''
""",
    )
    _write(
        base,
        "docs/specs/core.md",
        """---
id: core.ledger
domain: core
stage: usable
owns: ["src/core/**"]
depends_on: []
sources: [SRC-001]
summary: Core ledger arithmetic.
promise: Order totals never drift across callers.
---

# Core Ledger

See [ARCHITECTURE.md](../../ARCHITECTURE.md#fixture-app).
""",
    )
    _write(
        base,
        "docs/work.toml",
        """[[milestones]]
id = "M-1"
domain = "core"
slot = "now"
name = "Core MVP"

[[tasks]]
id = "T-1"
milestone = "M-1"
title = "Implement core ledger"
state = "done"
human_check = "approved"
specs = ["core.ledger"]
sources = ["SRC-001"]
""",
    )
    _write(
        base,
        "src/core/ledger.py",
        """# Role: Pure ledger total calculation.
# Out of scope: Transport or persistence.
# Anchors: spec=core.ledger, SRC-001

def total(items: list[int]) -> int:
    return sum(items)
""",
    )


class SsotAndCheckDocsTests(unittest.TestCase):
    def test_current_template_repository_passes_strict_validation(self) -> None:
        graph = load_project_graph(ROOT)
        self.assertEqual(len(graph.domains), 4)
        self.assertEqual(len(graph.modules), 13)
        self.assertGreaterEqual(len(graph.sources), 10)
        self.assertIn("SRC-019", graph.sources)
        self.assertGreaterEqual(len(graph.repo_docs), 35)
        self.assertGreaterEqual(len(graph.directory_map), 6)
        self.assertIn("单一事实只在一个地方维护", graph.sources["SRC-018"].quote)
        docs_by_path = {d.path: d for d in graph.repo_docs}
        self.assertTrue(docs_by_path["docs/work.toml"].summary.startswith("Active multi-domain roadmap"))
        self.assertNotIn("id =", docs_by_path["docs/work.toml"].summary)
        self.assertEqual(docs_by_path["docs-policy.toml"].summary, "TOML configuration / ledger (docs-policy.toml)")

        findings, _ = validate_project_graph(graph, strict=True)
        errors = [f for f in findings if f.severity == "error"]
        self.assertEqual(errors, [], f"Unexpected strict errors: {errors}")

    def test_frontmatter_and_markdown_structure_parser(self) -> None:
        doc = """---
id: mod.alpha
owns: ["src/a/**"]
sources:
  - SRC-001
  - SRC-002
---

# Alpha Module

<!-- required-reading: custom-span -->
## Public Contract

Check `[ignored](not-a-real-link.md)` and [real](target.md#frag).

```mermaid
flowchart TD
  A --> B
```
"""
        meta, _, err = parse_frontmatter(doc)
        self.assertIsNone(err)
        self.assertEqual(meta["id"], "mod.alpha")
        self.assertEqual(meta["sources"], ["SRC-001", "SRC-002"])

        h1, slugs, links, mermaids = extract_markdown_structure(doc, "docs/specs/alpha.md")
        self.assertEqual(h1, "Alpha Module")
        self.assertIn("public-contract", slugs)
        self.assertIn("custom-span", slugs)
        self.assertEqual(links, [("target.md#frag", 14)])
        self.assertEqual(len(mermaids), 1)
        self.assertIn("A --> B", mermaids[0].code)

    def test_minimal_single_domain_repo_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _build_minimal_repo(root)
            graph = load_project_graph(root)
            findings, _ = validate_project_graph(graph, strict=True)
            self.assertEqual(findings, [])

    def test_large_multi_domain_sharded_and_archived_scale(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _build_minimal_repo(root)
            # Expand to 6 domains, archived milestones, and sharded per-domain work.toml
            for idx in range(2, 7):
                dom = f"domain-{idx}"
                _write(
                    root,
                    f"docs/specs/{dom}/README.md",
                    (
                        f"---\ndomain: {dom}\nname: Domain {idx}\nstage: stable\npromise: Promise {idx}\n---\n"
                        f"# Domain {idx}\n\n## Positioning\nDomain {idx} boundary.\n\n```mermaid\nflowchart LR\n  A-->B\n```\n\n"
                        f"## Invariants & Checks\nSingle owner for domain {idx}.\n"
                    ),
                )
                _write(
                    root,
                    f"docs/specs/{dom}/service.md",
                    (
                        f"---\nid: {dom}.svc\ndomain: {dom}\nstage: stable\nowns: [\"src/{dom}/**\"]\n"
                        f"depends_on: [core.ledger]\nsources: [SRC-001]\npromise: Svc {idx}\n---\n"
                        f"# Service {idx}\n\n## Logic\nComputes service {idx} total.\n\n## Interfaces & Checks\nCalls core.ledger only.\n"
                    ),
                )
                _write(
                    root,
                    f"docs/specs/{dom}/work.toml",
                    f'[[milestones]]\nid = "M-{idx}"\ndomain = "{dom}"\nslot = "now"\nname = "Active {idx}"\n\n[[tasks]]\nid = "T-{idx}"\nmilestone = "M-{idx}"\ntitle = "Task {idx}"\nstate = "active"\nspecs = ["{dom}.svc"]\n',
                )
                _write(
                    root,
                    f"src/{dom}/svc.py",
                    f"# Role: Domain {idx} service.\nfrom core.ledger import total\n\ndef run() -> int:\n    return total([1, {idx}])\n",
                )
            archived_blocks = []
            for era in range(1, 16):
                archived_blocks.append(
                    f'[[milestones]]\nid = "M-OLD-{era}"\ndomain = "core"\nslot = "done"\nname = "Historical Era {era}"\n'
                )
            _write(root, "docs/archive/work-history.toml", "\n".join(archived_blocks))
            _write(
                root,
                "docs/decisions/ADR-001-old.md",
                "---\nid: ADR-001\nstatus: superseded\naffects: [core.ledger]\n---\n# Old Approach\n",
            )
            _write(
                root,
                "docs/decisions/ADR-002-new.md",
                "---\nid: ADR-002\nstatus: current\nsupersedes: [ADR-001]\nsources: [SRC-001]\naffects: [core.ledger]\n---\n# New Approach\n",
            )

            graph = load_project_graph(root)
            self.assertEqual(len(graph.domains), 6)
            self.assertEqual(len([m for m in graph.milestones.values() if m.archived]), 15)
            self.assertEqual(graph.decisions["ADR-001"].superseded_by, "ADR-002")
            findings, _ = validate_project_graph(graph, strict=True)
            self.assertEqual([f for f in findings if f.severity == "error"], [])

    def test_detects_ownership_import_budget_link_and_disclaimer_violations(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _build_minimal_repo(root)
            # 1. Second module that core.ledger illegally imports
            _write(
                root,
                "docs/specs/ui.md",
                "---\nid: ui.panel\ndomain: core\nowns: [\"src/ui/**\", \"src/core/ledger.py\"]\ndepends_on: [missing.mod]\nsources: [SRC-999]\n---\n# UI [bad](nope.md) and [badfrag](../../ARCHITECTURE.md#missing)\n",
            )
            # 2. Illegal cross-module import from core -> ui + oversized file (> 40 lines)
            long_lines = "\n".join(f"X_{i} = {i}" for i in range(45))
            _write(root, "src/core/ledger.py", f"# Role: Core\nfrom ui.panel import render\n{long_lines}\n")
            _write(root, "src/ui/panel.py", "# Role: UI\ndef render() -> str:\n    return 'ok'\n")
            # 3. Unclaimed file inside banned `utils/` directory
            _write(root, "src/utils/dump.py", "def helper():\n    return 1\n")
            # 4. Architecture rule violation + startup disclaimer stack
            _write(
                root,
                "architecture-rules.toml",
                'status = "configured"\n\n[[rules]]\nid = "no-ui-in-core"\ninclude = ["src/core/**"]\nforbidden_patterns = ["from ui"]\n',
            )
            _write(
                root,
                "AGENTS.md",
                "# Entry\nPassing a check does not by itself establish readiness and is not proof of completion.\n",
            )

            graph = load_project_graph(root)
            findings, _ = validate_project_graph(graph)
            codes = {f.rule_id for f in findings}
            self.assertIn("unknown_source", codes)
            self.assertIn("unknown_dependency", codes)
            self.assertIn("broken_link", codes)
            self.assertIn("broken_fragment", codes)
            self.assertIn("ambiguous_ownership", codes)
            self.assertIn("unclaimed_source", codes)
            self.assertIn("undeclared_import", codes)
            self.assertIn("no-ui-in-core", codes)
            self.assertIn("file_size_budget", codes)
            self.assertIn("catchall_directory", codes)
            self.assertIn("startup_disclaimer", codes)

    def test_observed_adoption_stage_downgrades_legacy_debt_to_advisories(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _build_minimal_repo(root, stage="observed")
            _write(root, "src/legacy_unclaimed.py", "\n".join(f"V_{i} = {i}" for i in range(60)))

            graph = load_project_graph(root)
            findings, _ = validate_project_graph(graph, strict=False)
            errors = [f for f in findings if f.severity == "error"]
            advisories = [f for f in findings if f.severity == "advisory"]
            self.assertEqual(errors, [])
            self.assertTrue(any(f.rule_id == "unclaimed_source" for f in advisories))
            self.assertTrue(any(f.rule_id == "file_size_budget" for f in advisories))

    def test_git_diff_surfaces_verbatim_l1_quotes_and_template_remote_guard(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _build_minimal_repo(root)
            # Mark as un-onboarded template copy with non-template git remote
            policy_txt = (root / "docs-policy.toml").read_text(encoding="utf-8").replace(
                'identity = "product"', 'identity = "template"'
            )
            _write(root, "docs-policy.toml", policy_txt)

            subprocess.run(["git", "init"], cwd=root, check=True, capture_output=True)
            subprocess.run(["git", "remote", "add", "origin", "https://github.com/example/copied-app.git"], cwd=root, check=True, capture_output=True)

            graph = load_project_graph(root)
            findings, nudges = validate_project_graph(graph)
            self.assertTrue(any(f.rule_id == "copied_checkout" for f in findings))
            self.assertEqual(len(nudges["touched_modules"]), 1)
            self.assertEqual(nudges["touched_modules"][0]["module"], "core.ledger")
            self.assertIn("一个事实只在一个地方维护", nudges["touched_modules"][0]["sources"][0]["excerpt"])

    def test_scoped_enforcement_and_missing_role_header(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _build_minimal_repo(root, stage="scoped_enforcement")
            pol = (root / "docs-policy.toml").read_text(encoding="utf-8").replace(
                'stage = "scoped_enforcement"',
                'stage = "scoped_enforcement"\nmanaged_paths = ["src/managed/**"]',
            )
            _write(root, "docs-policy.toml", pol)
            _write(
                root,
                "docs/specs/managed.md",
                '---\nid: managed.mod\ndomain: core\nowns: ["src/managed/**"]\nsources: [SRC-001]\npromise: Managed module.\n---\n# Managed\n',
            )
            _write(root, "src/managed/worker.py", "def work():\n    return 1\n")
            _write(root, "src/legacy/old.py", "def old():\n    return 2\n")

            graph = load_project_graph(root)
            findings, _ = validate_project_graph(graph, strict=False)
            errs = {(f.rule_id, f.path) for f in findings if f.severity == "error"}
            advs = {(f.rule_id, f.path) for f in findings if f.severity == "advisory"}
            self.assertIn(("missing_role_header", "src/managed/worker.py"), errs)
            self.assertIn(("unclaimed_source", "src/legacy/old.py"), advs)

    def test_multiline_js_alias_and_html_script_import_boundaries(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _build_minimal_repo(root)
            _write(root, "docs/specs/secret.md", '---\nid: secret.box\ndomain: core\nowns: ["src/secret/**"]\nsources: [SRC-001]\npromise: Secret.\n---\n# Secret\n')
            _write(root, "docs/specs/web.md", '---\nid: web.app\ndomain: core\nowns: ["src/web/**"]\ndepends_on: []\nsources: [SRC-001]\npromise: Web.\n---\n# Web\n')
            _write(root, "src/secret/hidden.js", "// Role: Secret helper.\nexport const SECRET = 1;\n")
            _write(root, "src/web/view.ts", '// Role: View.\nimport {\n  SECRET,\n} from "@/secret/hidden";\nexport const x = SECRET;\n')
            _write(root, "src/web/index.html", '<!-- Role: Shell. -->\n<script src="../secret/hidden.js"></script>\n')

            graph = load_project_graph(root)
            findings, _ = validate_project_graph(graph)
            vio_files = {f.path for f in findings if f.rule_id == "undeclared_import"}
            self.assertIn("src/web/view.ts", vio_files)
            self.assertIn("src/web/index.html", vio_files)

    def test_banned_jargon_and_unresolved_placeholder_detection(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _build_minimal_repo(root)
            _write(root, "README.md", "# Demo\n使用上下文胶囊管理 {{PROJECT_NAME}}。\n")
            graph = load_project_graph(root)
            findings, _ = validate_project_graph(graph)
            codes = {f.rule_id for f in findings}
            self.assertIn("plain_language_jargon", codes)
            self.assertIn("unresolved_placeholder", codes)

    def test_day_zero_synthetic_modules_fallback(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write(root, "src/billing/calc.py", "# Role: Billing math.\ndef add(a, b):\n    return a + b\n")
            graph = load_project_graph(root)
            self.assertTrue(graph.is_day_zero_synthetic)
            self.assertIn("codebase", graph.domains)
            self.assertIn("codebase.src-billing", graph.modules)
            findings, _ = validate_project_graph(graph)
            self.assertFalse(any(f.rule_id == "unclaimed_source" for f in findings))

        with tempfile.TemporaryDirectory() as tmp2:
            root2 = Path(tmp2)
            _write(root2, "docs-policy.toml", 'version = 2\n[layout]\nsource_roots = ["src", "backend"]\n')
            _write(root2, "backend/api.py", "# Role: API.\ndef ping():\n    return 'ok'\n")
            _write(root2, "examples/demo.py", "# Role: Example.\n")
            g2 = load_project_graph(root2)
            self.assertIn("codebase.backend", g2.modules)
            self.assertNotIn("codebase.examples", g2.modules)

    def test_ui_tsx_vue_plain_language_and_zh_project_lang(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _build_minimal_repo(root)
            pol = (root / "docs-policy.toml").read_text(encoding="utf-8").replace(
                'identity = "product"',
                'identity = "product"\nlanguage = "zh"',
            )
            _write(root, "docs-policy.toml", pol)
            _write(root, "docs/specs/ui.md", '---\nid: ui.view\ndomain: core\nowns: ["src/ui/**"]\nsources: [SRC-001]\npromise: UI view.\n---\n# UI View\nEnglish only body.\n')
            _write(root, "src/ui/App.tsx", '// Role: App.\nexport const label = "使用上下文胶囊";\n')
            _write(root, "src/ui/Widget.vue", '// Role: Widget.\n<template><div>{{ userName }}</div></template>\n')

            subprocess.run(["git", "init"], cwd=root, check=True, capture_output=True)
            graph = load_project_graph(root)
            findings, nudges = validate_project_graph(graph)
            by_file_rule = {(f.rule_id, f.path) for f in findings}
            self.assertIn(("plain_language_jargon", "src/ui/App.tsx"), by_file_rule)
            self.assertNotIn(("unresolved_placeholder", "src/ui/Widget.vue"), by_file_rule)
            self.assertIn(("project_language_mismatch", "docs/specs/ui.md"), by_file_rule)
            self.assertTrue(nudges["touched_docs"])

    def test_html_disclaimer_work_toml_zh_and_strict_spec_structure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _build_minimal_repo(root, default_stage="stable")
            pol = (root / "docs-policy.toml").read_text(encoding="utf-8").replace(
                'identity = "product"',
                'identity = "product"\nlanguage = "zh"',
            )
            _write(root, "docs-policy.toml", pol)
            _write(root, "docs/design/preview.html", "<html><body><p>A不等于B</p></body></html>\n")
            _write(root, "docs/specs/core/README.md", "---\ndomain: core\nname: 核心\nstage: stable\npromise: ok\n---\n# Core\n短\n")
            _write(root, "docs/specs/core/work.toml", '[[tasks]]\nid = "T-SHARD"\nmilestone = "M-1"\ntitle = "English Sharded Task"\nstate = "active"\n')
            graph = load_project_graph(root)
            findings, _ = validate_project_graph(graph, strict=True)
            rules_by_path = {(f.rule_id, f.path) for f in findings}
            self.assertIn(("startup_disclaimer", "docs/design/preview.html"), rules_by_path)
            self.assertIn(("project_language_mismatch", "docs/work.toml"), rules_by_path)
            self.assertIn(("project_language_mismatch", "docs/specs/core/work.toml"), rules_by_path)
            self.assertIn(("project_language_mismatch", "docs/specs/core/README.md"), rules_by_path)
            self.assertIn(("incomplete_spec_structure", "docs/specs/core/README.md"), rules_by_path)


if __name__ == "__main__":
    unittest.main()
