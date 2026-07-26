"""Fixture tests for the portable documentation governance checker."""

from __future__ import annotations

import ast
import importlib.util
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
CHECKER = REPOSITORY_ROOT / "scripts" / "check_docs.py"
FIXED_TODAY = "2026-07-26"


def load_checker_module():
    specification = importlib.util.spec_from_file_location("check_docs", CHECKER)
    module = importlib.util.module_from_spec(specification)
    # Dataclass resolution looks the defining module up in sys.modules.
    sys.modules["check_docs"] = module
    specification.loader.exec_module(module)
    return module


class DocumentationCheckerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        self.root = Path(self.temporary_directory.name) / "fixture-repository"
        shutil.copytree(
            REPOSITORY_ROOT,
            self.root,
            ignore=shutil.ignore_patterns(
                ".git",
                ".venv",
                "__pycache__",
                "*.pyc",
                "archive",
                "tmp",
            ),
        )

    def path(self, relative: str) -> Path:
        return self.root / relative

    def read(self, relative: str) -> str:
        return self.path(relative).read_text(encoding="utf-8")

    def write(self, relative: str, content: str) -> None:
        target = self.path(relative)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")

    def replace(self, relative: str, old: str, new: str) -> None:
        content = self.read(relative)
        self.assertIn(old, content, f"fixture precondition missing in {relative}")
        self.write(relative, content.replace(old, new, 1))

    def run_checker(
        self,
        *,
        root: Path | None = None,
        today: str = FIXED_TODAY,
        strict: bool = False,
    ) -> subprocess.CompletedProcess[str]:
        command = [
            sys.executable,
            str(CHECKER),
            "--root",
            str(root or self.root),
            "--today",
            today,
        ]
        if strict:
            command.append("--strict")
        return subprocess.run(
            command,
            cwd=REPOSITORY_ROOT,
            check=False,
            capture_output=True,
            text=True,
        )

    def assert_passes(self, *, root: Path | None = None, today: str = FIXED_TODAY) -> str:
        result = self.run_checker(root=root, today=today)
        output = result.stdout + result.stderr
        self.assertEqual(result.returncode, 0, output)
        self.assertIn("check_docs: OK", output)
        return output

    def assert_fails_with(self, *fragments: str, strict: bool = False) -> str:
        result = self.run_checker(strict=strict)
        output = result.stdout + result.stderr
        self.assertNotEqual(result.returncode, 0, output)
        for fragment in fragments:
            self.assertIn(fragment, output)
        return output

    def assert_advises(self, *fragments: str) -> str:
        """A finding is reported, the summary still passes, and --strict blocks."""

        result = self.run_checker()
        output = result.stdout + result.stderr
        self.assertEqual(result.returncode, 0, output)
        self.assertIn("advisory finding(s)", output)
        self.assertIn("check_docs: OK", output)
        for fragment in fragments:
            self.assertIn(fragment, output)
        self.assert_fails_with(*fragments, strict=True)
        return output

    def set_policy(self, old: str, new: str) -> None:
        self.replace("docs-policy.toml", old, new)

    def surface_contract(self, abnormality: str | None = None) -> str:
        abnormality_section = ""
        if abnormality is not None:
            abnormality_section = (
                "\n## Known abnormality classes\n\n" + abnormality + "\n"
            )
        return f"""---
doc_type: surface-contract
surface: sample-surface
status: current
authority: normative
implementation: implemented
contract_scope: current-ui
verification_status: enforced
last_reconciled: 2026-07-26
supersedes: []
---

# Sample surface

## Raw layer

### raw[1] — 2026-07-24

> The primary result must remain visible.

### raw[2] — 2026-07-25

> Keyboard users must reach the action.

## Translated layer

### Outcomes

- Keep the primary result visible and the action keyboard reachable.
- from: raw[1], raw[2]
{abnormality_section}"""

    def source_contract(self, citation: str) -> str:
        return f"""---
doc_type: contract
status: current
authority: normative
implementation: implemented
verification_status: enforced
last_reconciled: 2026-07-26
supersedes: []
---

# Source reconciliation example

## Source anchors

### source[1] — 2026-07-24

> Preserve the first invariant.

### source[2] — 2026-07-25

> Preserve the second invariant.

## Normative invariants

- Both requested invariants are normative.
{citation}
"""

    def basic_contract(
        self,
        *,
        status: str = "current",
        implementation: str = "implemented",
        reconciled: str = "2026-07-26",
        review_due: str | None = None,
        title: str = "Product behavior",
        body: str = "The behavior has one owner.",
    ) -> str:
        due_line = f"review_due: {review_due}\n" if review_due else ""
        return f"""---
doc_type: contract
status: {status}
authority: normative
implementation: {implementation}
verification_status: pending
last_reconciled: {reconciled}
{due_line}supersedes: []
---

# {title}

## Normative invariants

{body}
"""

    def configure_architecture_not_applicable(self, rationale: str) -> None:
        architecture = self.read("ARCHITECTURE.md")
        architecture = architecture.replace(
            "template_state: unconfigured", "template_state: configured", 1
        )
        architecture = re.sub(r"\{\{[^}]+\}\}", "configured-value", architecture)
        self.write("ARCHITECTURE.md", architecture)
        self.write(
            "architecture-rules.toml",
            f'''version = 1
status = "not_applicable"
rationale = "{rationale}"
''',
        )

    def test_template_repository_passes(self) -> None:
        self.assert_passes(root=REPOSITORY_ROOT)

    def test_valid_surface_citations_pass(self) -> None:
        self.write("docs/design/sample-surface.md", self.surface_contract())
        self.assert_passes()

    def test_unresolved_raw_citation_fails(self) -> None:
        content = self.surface_contract().replace(
            "from: raw[1], raw[2]", "from: raw[1], raw[3]"
        )
        self.write("docs/design/sample-surface.md", content)
        self.assert_fails_with(
            "citation does not resolve: raw[3]",
            "raw[2] defined but never cited",
        )

    def test_orphan_raw_anchor_fails(self) -> None:
        content = self.surface_contract().replace(
            "from: raw[1], raw[2]", "from: raw[1]"
        )
        self.write("docs/design/sample-surface.md", content)
        self.assert_fails_with("raw[2] defined but never cited")

    def test_uncited_translated_subsection_fails_even_with_later_citation(self) -> None:
        content = self.surface_contract().replace(
            "- from: raw[1], raw[2]",
            "## Reconciliation log\n\n- from: raw[1], raw[2]",
        )
        self.write("docs/design/sample-surface.md", content)
        self.assert_fails_with(
            "translated subsection lacks raw citation: Outcomes",
            "raw[1] defined but never cited",
            "raw[2] defined but never cited",
        )

    def test_unresolved_source_citation_fails(self) -> None:
        self.write(
            "docs/contracts/source-example.md",
            self.source_contract("- from: source[1], source[3]"),
        )
        self.assert_fails_with(
            "citation does not resolve: source[3]",
            "source[2] defined but never cited",
        )

    def test_orphan_source_anchor_fails(self) -> None:
        self.write(
            "docs/contracts/source-example.md",
            self.source_contract("- from: source[1]"),
        )
        self.assert_fails_with("source[2] defined but never cited")

    def test_overdue_target_is_advisory_by_default(self) -> None:
        self.write(
            "docs/contracts/aging-example.md",
            self.basic_contract(
                status="target",
                implementation="in_progress",
                reconciled="2026-01-01",
            ),
        )
        self.assert_advises("target document review overdue since 2026-04-01")

    def test_aging_severity_is_configurable_to_error(self) -> None:
        self.set_policy('target_aging = "advisory"', 'target_aging = "error"')
        self.write(
            "docs/contracts/aging-example.md",
            self.basic_contract(
                status="target",
                implementation="in_progress",
                reconciled="2026-01-01",
            ),
        )
        self.assert_fails_with("target document review overdue since 2026-04-01")

    def test_aging_severity_is_configurable_to_off(self) -> None:
        self.set_policy('target_aging = "advisory"', 'target_aging = "off"')
        self.write(
            "docs/contracts/aging-example.md",
            self.basic_contract(
                status="target",
                implementation="in_progress",
                reconciled="2026-01-01",
            ),
        )
        output = self.assert_passes()
        self.assertNotIn("review overdue", output)

    def test_strict_does_not_resurrect_a_rule_the_project_switched_off(self) -> None:
        """`off` is an owner decision; the scheduled job must not overturn it."""

        self.set_policy('target_aging = "advisory"', 'target_aging = "off"')
        self.write(
            "docs/contracts/aging-example.md",
            self.basic_contract(
                status="target",
                implementation="in_progress",
                reconciled="2026-01-01",
            ),
        )
        result = self.run_checker(strict=True)
        output = result.stdout + result.stderr
        self.assertEqual(result.returncode, 0, output)
        self.assertNotIn("review overdue", output)

    def test_unknown_severity_rule_is_rejected(self) -> None:
        self.set_policy('target_aging = "advisory"', 'invented_rule = "advisory"')
        self.assert_fails_with("[severity].invented_rule is not a configurable rule")

    def test_invalid_severity_value_is_rejected(self) -> None:
        self.set_policy('target_aging = "advisory"', 'target_aging = "loud"')
        self.assert_fails_with(
            "[severity].target_aging must be error, advisory, or off: loud"
        )

    def test_review_due_overrides_default_target_age(self) -> None:
        self.write(
            "docs/contracts/aging-example.md",
            self.basic_contract(
                status="target",
                implementation="in_progress",
                reconciled="2026-01-01",
                review_due="2026-08-01",
            ),
        )
        self.assert_passes()

    def test_overdue_open_promise_is_advisory_by_default(self) -> None:
        self.write(
            "docs/contracts/promise-example.md",
            self.basic_contract(
                body=(
                    "- promise[finish-cutover]: due=2026-07-25; status=open; "
                    "owner=maintainer; description=finish the declared cutover"
                )
            ),
        )
        self.assert_advises("open promise[finish-cutover] overdue since 2026-07-25")

    def test_shipped_promises_never_break_an_adopter_build(self) -> None:
        """A promise deadline passing must not turn an adopter's CI red."""

        for today in ("2026-12-31", "2027-06-30"):
            with self.subTest(today=today):
                result = self.run_checker(root=REPOSITORY_ROOT, today=today)
                output = result.stdout + result.stderr
                self.assertEqual(result.returncode, 0, output)
                self.assertIn("check_docs: OK", output)

    def test_missing_required_template_file_fails(self) -> None:
        self.path("templates/guide.md").unlink()
        self.assert_fails_with("required template is missing")

    def test_missing_required_template_section_fails(self) -> None:
        self.replace("templates/guide.md", "## Purpose", "## Goal")
        self.assert_fails_with("template missing required section: Purpose")

    def test_missing_agent_execution_template_fails(self) -> None:
        self.path("templates/agent-execution-plan.md").unlink()
        self.assert_fails_with(
            "templates/agent-execution-plan.md",
            "required template is missing",
        )

    def test_agent_execution_template_requires_review_topology(self) -> None:
        self.replace(
            "templates/agent-execution-plan.md",
            "## Review topology",
            "## Review arrangement",
        )
        self.assert_fails_with(
            "template missing required section: Review topology"
        )

    def test_missing_adoption_assessment_template_fails(self) -> None:
        self.path("templates/adoption-assessment.md").unlink()
        self.assert_fails_with(
            "templates/adoption-assessment.md",
            "required template is missing",
        )

    def test_adoption_assessment_requires_stage_decision(self) -> None:
        self.replace(
            "templates/adoption-assessment.md",
            "## Stage decision",
            "## Stage suggestion",
        )
        self.assert_fails_with(
            "template missing required section: Stage decision"
        )

    def test_unsupported_python_versions_get_an_actionable_message(self) -> None:
        guard = load_checker_module().require_supported_python
        for version in ((3, 9, 0), (3, 10, 14), (2, 7, 18)):
            with self.subTest(version=version):
                with self.assertRaises(SystemExit) as raised:
                    guard(version)
                message = str(raised.exception)
                self.assertIn("requires Python 3.11 or newer", message)
                self.assertIn(f"{version[0]}.{version[1]}", message)
        guard((3, 11, 0))
        guard((3, 14, 2))

    def test_version_guard_runs_before_any_version_specific_import(self) -> None:
        """`import tomllib` below the guard is what makes the message reachable."""

        module = ast.parse(CHECKER.read_text(encoding="utf-8"))
        guard_index: int | None = None
        import_index: int | None = None
        for index, node in enumerate(module.body):
            if (
                isinstance(node, ast.Expr)
                and isinstance(node.value, ast.Call)
                and isinstance(node.value.func, ast.Name)
                and node.value.func.id == "require_supported_python"
            ):
                guard_index = index
            if isinstance(node, ast.Import) and any(
                alias.name == "tomllib" for alias in node.names
            ):
                import_index = index
        self.assertIsNotNone(guard_index, "module must call require_supported_python()")
        self.assertIsNotNone(import_index, "module must import tomllib")
        self.assertLess(
            guard_index,
            import_index,
            "the version guard must run before tomllib is imported",
        )

    def test_unsupported_interpreter_reports_cleanly_when_available(self) -> None:
        executable = shutil.which("python3.9")
        if executable is None:
            self.skipTest("Python 3.9 is not installed")
        result = subprocess.run(
            [executable, str(CHECKER), "--help"],
            cwd=REPOSITORY_ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        output = result.stdout + result.stderr
        self.assertNotEqual(result.returncode, 0, output)
        self.assertIn("requires Python 3.11 or newer", output)
        self.assertNotIn("Traceback", output)

    def test_surface_template_subsection_requires_citation(self) -> None:
        content = self.read("templates/frontend-surface.md")
        marker = "### Responsive and browser support"
        start = content.index(marker)
        end = content.index("## Known abnormality classes", start)
        block = content[start:end]
        self.assertIn("- from: raw[{{N}}]", block)
        self.write(
            "templates/frontend-surface.md",
            content[:start]
            + block.replace("- from: raw[{{N}}]", "", 1)
            + content[end:],
        )
        self.assert_fails_with(
            "surface template translated subsection lacks raw citation: "
            "Responsive and browser support"
        )

    def test_contract_template_requires_structured_promise_example(self) -> None:
        self.replace(
            "templates/contract.md",
            "owner={{owner}}",
            "responsible={{owner}}",
        )
        self.assert_fails_with("contract template missing structured promise example")

    def test_product_source_requires_configured_architecture(self) -> None:
        self.write("src/product.py", "VALUE = 1\n")
        self.assert_fails_with(
            "product source exists but architecture template_state is not configured",
            "product source exists but architecture fitness is still template",
        )

    def test_historical_and_not_started_contracts_do_not_satisfy_adoption(self) -> None:
        self.configure_architecture_not_applicable(
            "Literal path rules do not apply; a language-native dependency test is required."
        )
        self.write("src/product.py", "VALUE = 1\n")
        self.write(
            "docs/contracts/historical-product.md",
            self.basic_contract(status="historical", implementation="implemented"),
        )
        self.write(
            "docs/contracts/not-started-product.md",
            self.basic_contract(status="target", implementation="not_started"),
        )
        self.assert_fails_with(
            "product source exists but only 0 live implementation contract(s)"
        )

    def test_contract_in_a_subdirectory_counts_as_a_live_contract(self) -> None:
        self.configure_architecture_not_applicable(
            "Dependency direction is enforced by a language-native architecture test."
        )
        self.write("src/product.py", "VALUE = 1\n")
        self.write(
            "docs/contracts/billing/invoicing.md",
            self.basic_contract(title="Invoicing"),
        )
        self.assert_passes()

    def test_governance_contracts_do_not_satisfy_the_product_minimum(self) -> None:
        self.configure_architecture_not_applicable(
            "Dependency direction is enforced by a language-native architecture test."
        )
        self.write("src/product.py", "VALUE = 1\n")
        content = self.basic_contract(title="House rules").replace(
            "authority: normative",
            "authority: normative\ncontract_role: governance",
            1,
        )
        self.write("docs/contracts/house-rules.md", content)
        self.assert_fails_with(
            "product source exists but only 0 live implementation contract(s)"
        )

    def test_invalid_contract_role_is_rejected(self) -> None:
        content = self.basic_contract().replace(
            "authority: normative",
            "authority: normative\ncontract_role: advisory",
            1,
        )
        self.write("docs/contracts/role-example.md", content)
        self.assert_fails_with("contract_role must be product or governance: advisory")

    def test_source_outside_every_configured_root_is_reported(self) -> None:
        self.write("app/models/invoice.rb", "class Invoice; end\n")
        self.assert_fails_with(
            "source files exist outside every configured source root",
            "app/models/invoice.rb",
        )

    def test_declaring_the_real_source_root_activates_the_adoption_gates(self) -> None:
        self.write("app/models/invoice.rb", "class Invoice; end\n")
        self.set_policy('source_roots = ["src"]', 'source_roots = ["app"]')
        self.assert_fails_with(
            "product source exists but architecture template_state is not configured"
        )

    def test_harness_paths_are_not_mistaken_for_product_source(self) -> None:
        self.write("scripts/release.py", "VALUE = 1\n")
        self.assert_passes()

    def test_harness_paths_accept_glob_patterns(self) -> None:
        self.write("tools/generate/emit.py", "VALUE = 1\n")
        self.set_policy(
            'harness_paths = ["scripts", "tests"]',
            'harness_paths = ["scripts", "tests", "tools/**"]',
        )
        self.assert_passes()

    def test_repository_root_tooling_files_are_never_unclaimed_source(self) -> None:
        """setup.py and friends belong to no source root in any layout."""

        for name in ("setup.py", "conftest.py", "noxfile.py", "vite.config.ts"):
            self.write(name, "VALUE = 1\n")
        self.assert_passes()

    def test_vendored_dependencies_are_not_scanned_for_stray_source(self) -> None:
        self.write("node_modules/left-pad/index.js", "module.exports = 1;\n")
        self.write(".venv/lib/site-packages/thing.py", "VALUE = 1\n")
        self.assert_passes()

    def test_source_root_gap_is_advisory_before_enforcement_begins(self) -> None:
        """An adopter must be able to put the check into CI on day one."""

        self.set_stage("observed")
        self.write("app/models/invoice.rb", "class Invoice; end\n")
        self.assert_advises("source files exist outside every configured source root")

    def test_retired_adoption_key_names_its_replacement(self) -> None:
        self.set_policy(
            "minimum_live_contracts = 1",
            'minimum_live_contracts = 1\ngovernance_contracts = ["x.md"]',
        )
        self.assert_fails_with(
            "[adoption].governance_contracts is no longer read",
            "contract_role: governance",
        )

    def test_unknown_adoption_key_is_rejected(self) -> None:
        self.set_policy(
            "minimum_live_contracts = 1",
            'minimum_live_contracts = 1\nsorce_roots = ["app"]',
        )
        self.assert_fails_with("[adoption].sorce_roots is not a recognised key")

    def set_stage(self, stage: str) -> None:
        content = self.read("docs-policy.toml")
        updated = re.sub(r'^stage = "[a-z_]+"$', f'stage = "{stage}"', content, count=1, flags=re.M)
        self.assertNotEqual(content, updated, "stage assignment not found in policy")
        self.write("docs-policy.toml", updated)

    def test_early_adoption_stages_report_without_blocking(self) -> None:
        self.write("src/product.py", "VALUE = 1\n")
        for stage in ("observed", "baselined"):
            with self.subTest(stage=stage):
                self.set_stage(stage)
                self.assert_advises(
                    "product source exists but architecture template_state is "
                    "not configured"
                )

    def test_scoped_enforcement_gates_only_managed_paths(self) -> None:
        self.set_stage("scoped_enforcement")
        self.write("src/legacy/old.py", "VALUE = 1\n")
        self.assert_fails_with(
            "product source exists but architecture template_state is not configured"
        )
        self.set_policy("managed_paths = []", 'managed_paths = ["src/migrated/**"]')
        self.assert_passes()

    def test_explicit_adoption_gate_severity_overrides_the_stage(self) -> None:
        self.set_stage("observed")
        self.set_policy(
            'pending_abnormality_aging = "advisory"',
            'pending_abnormality_aging = "advisory"\nadoption_gate = "error"',
        )
        self.write("src/product.py", "VALUE = 1\n")
        self.assert_fails_with(
            "product source exists but architecture template_state is not configured"
        )

    def test_unknown_adoption_stage_is_rejected(self) -> None:
        self.set_stage("mostly_adopted")
        self.assert_fails_with("[adoption].stage must be one of")

    def test_minimal_profile_drops_higher_tier_templates(self) -> None:
        self.set_policy('profile = "full"', 'profile = "minimal"')
        for name in (
            "independent-review.md",
            "holistic-evaluation.md",
            "agent-execution-plan.md",
            "evidence-preserving-data.md",
            "adoption-assessment.md",
            "frontend-surface.md",
            "backend-change.md",
            "cross-stack-change.md",
            "verification-report.md",
            "handoff.md",
        ):
            self.path(f"templates/{name}").unlink()
        output = self.assert_passes()
        self.assertIn("4 template(s) (profile: minimal)", output)

    def test_lower_profile_still_requires_its_own_tier(self) -> None:
        self.set_policy('profile = "full"', 'profile = "minimal"')
        self.path("templates/contract.md").unlink()
        self.assert_fails_with("templates/contract.md", "required template is missing")

    def test_unknown_template_profile_is_rejected(self) -> None:
        self.set_policy('profile = "full"', 'profile = "enormous"')
        self.assert_fails_with("[templates].profile must be one of")

    def test_required_template_without_declared_doc_type_fails(self) -> None:
        self.set_policy('"guide.md" = "guide"', "")
        self.assert_fails_with(
            "required template has no declared doc_type in [templates.doc_types]"
        )

    def test_reference_to_a_trimmed_template_is_advisory(self) -> None:
        self.set_policy('profile = "full"', 'profile = "minimal"')
        self.path("templates/adoption-assessment.md").unlink()
        self.assert_advises(
            "broken local Markdown link: ../../templates/adoption-assessment.md"
        )

    def test_reference_to_an_unknown_template_still_fails(self) -> None:
        self.set_policy('profile = "full"', 'profile = "minimal"')
        self.write(
            "docs/guides/onboarding.md",
            self.read("docs/guides/onboarding.md")
            + "\n[Typo](../../templates/no-such-template.md)\n",
        )
        self.assert_fails_with(
            "broken local Markdown link: ../../templates/no-such-template.md"
        )

    def test_configured_architecture_rule_must_match_files(self) -> None:
        self.write(
            "architecture-rules.toml",
            """version = 1
status = "configured"
rationale = "Keep a generic package independent of product dependencies."

[[rules]]
id = "generic-boundary"
description = "The generic package must not reference the product package."
include = ["src/**/*.py"]
exclude = []
forbidden_patterns = ["product_package"]
""",
        )
        self.assert_fails_with("rule generic-boundary matches no files (vacuous rule)")

    def test_configured_architecture_rule_detects_forbidden_literal(self) -> None:
        self.write(
            "architecture-rules.toml",
            """version = 1
status = "configured"
rationale = "Protect the reusable repository entry point."

[[rules]]
id = "entry-boundary"
description = "The entry point must not contain the forbidden marker."
include = ["README.md"]
exclude = []
forbidden_patterns = ["Engineering Discipline Template"]
""",
        )
        self.assert_fails_with(
            "architecture rule entry-boundary forbids 'Engineering Discipline Template'"
        )

    def test_architecture_include_glob_cannot_escape_repository(self) -> None:
        (self.root.parent / "outside.py").write_text("VALUE = 1\n", encoding="utf-8")
        self.write(
            "architecture-rules.toml",
            """version = 1
status = "configured"
rationale = "Architecture checks remain scoped to this repository."

[[rules]]
id = "escaping-boundary"
description = "External files must not satisfy a repository rule."
include = ["../outside.py"]
exclude = []
forbidden_patterns = ["external_dependency"]
""",
        )
        self.assert_fails_with(
            "rule escaping-boundary include glob must stay inside repository: "
            "../outside.py"
        )

    def test_not_applicable_architecture_requires_substantive_rationale(self) -> None:
        self.write(
            "architecture-rules.toml",
            'version = 1\nstatus = "not_applicable"\nrationale = "Too short."\n',
        )
        self.assert_fails_with(
            "not_applicable architecture fitness requires a substantive rationale"
        )

    def test_not_applicable_architecture_rejects_template_rationale(self) -> None:
        self.replace(
            "architecture-rules.toml",
            'status = "template"',
            'status = "not_applicable"',
        )
        self.assert_fails_with(
            "not_applicable architecture fitness requires a substantive rationale"
        )

    def test_substantive_not_applicable_architecture_rationale_passes(self) -> None:
        self.write(
            "architecture-rules.toml",
            (
                'version = 1\nstatus = "not_applicable"\n'
                'rationale = "Dependency direction is enforced by a language-native architecture test."\n'
            ),
        )
        self.assert_passes()

    def test_fresh_pending_abnormality_passes(self) -> None:
        record = (
            "- abnormality[hidden-action]: state=pending; "
            "evidence=pending:2026-07-01; guard=pending; "
            "description=action can be obscured in a narrow container"
        )
        self.write("docs/design/sample-surface.md", self.surface_contract(record))
        self.assert_passes()

    def test_expired_pending_abnormality_is_advisory_by_default(self) -> None:
        record = (
            "- abnormality[hidden-action]: state=pending; "
            "evidence=pending:2026-06-01; guard=pending; "
            "description=action can be obscured in a narrow container"
        )
        self.write("docs/design/sample-surface.md", self.surface_contract(record))
        self.assert_advises(
            "abnormality[hidden-action] evidence pending for more than 30 days"
        )

    def test_abnormality_evidence_reference_resolves(self) -> None:
        record = (
            "- abnormality[hidden-action]: state=active; "
            "evidence=docs/evidence/abnormality-report.md; "
            "guard=test:layout-containment; "
            "description=action can be obscured in a narrow container"
        )
        self.write("docs/design/sample-surface.md", self.surface_contract(record))
        self.write(
            "docs/evidence/abnormality-report.md",
            """---
doc_type: evidence
status: historical
authority: evidence
last_reconciled: 2026-07-26
---

# Abnormality verification

## Anomalies

- abnormality[hidden-action]: result=fail; evidence=observed; issue=none
""",
        )
        self.assert_passes()

    def test_abnormality_evidence_path_cannot_escape_evidence_directory(self) -> None:
        (self.root.parent / "outside.md").write_text("external\n", encoding="utf-8")
        record = (
            "- abnormality[hidden-action]: state=active; "
            "evidence=docs/evidence/../../../outside.md; "
            "guard=test:layout-containment; "
            "description=action can be obscured in a narrow container"
        )
        self.write("docs/design/sample-surface.md", self.surface_contract(record))
        self.assert_fails_with(
            "abnormality[hidden-action] evidence path escapes docs/evidence: "
            "docs/evidence/../../../outside.md"
        )

    def test_unregistered_abnormality_evidence_reference_fails(self) -> None:
        self.write(
            "docs/evidence/abnormality-report.md",
            """---
doc_type: evidence
status: historical
authority: evidence
last_reconciled: 2026-07-26
---

# Abnormality verification

## Anomalies

- abnormality[unknown-class]: result=fail; evidence=observed; issue=none
""",
        )
        self.assert_fails_with(
            "abnormality[unknown-class] is not registered by a surface"
        )

    def test_missing_relationship_target_fails(self) -> None:
        self.replace(
            "docs/plans/2026-07-26-documentation-harness-hardening.md",
            "implements: docs/contracts/documentation-harness.md",
            "implements: docs/contracts/missing-contract.md",
        )
        self.assert_fails_with(
            "implements points to missing path: docs/contracts/missing-contract.md"
        )

    def test_relationship_target_cannot_escape_repository(self) -> None:
        (self.root.parent / "outside.md").write_text("external\n", encoding="utf-8")
        self.replace(
            "docs/plans/2026-07-26-documentation-harness-hardening.md",
            "implements: docs/contracts/documentation-harness.md",
            "implements: ../outside.md",
        )
        self.assert_fails_with("implements path escapes repository: ../outside.md")

    def test_missing_local_link_target_fails(self) -> None:
        self.write(
            "README.md",
            self.read("README.md") + "\n[Missing local reference](docs/missing.md)\n",
        )
        self.assert_fails_with("broken local Markdown link: docs/missing.md")

    def test_local_link_target_cannot_escape_repository(self) -> None:
        (self.root.parent / "outside.md").write_text("external\n", encoding="utf-8")
        self.write(
            "README.md",
            self.read("README.md") + "\n[External local file](../outside.md)\n",
        )
        self.assert_fails_with("local Markdown link escapes repository: ../outside.md")


if __name__ == "__main__":
    unittest.main()
