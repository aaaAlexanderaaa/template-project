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
from datetime import date
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
CHECKER = REPOSITORY_ROOT / "scripts" / "check_docs.py"
# The copied repository and this clock form one reviewed fixture baseline.
# Advance together when repository reconciliation dates move forward.
FIXED_TODAY = "2026-11-01"


def load_checker_module():
    specification = importlib.util.spec_from_file_location("scripts.check_docs", CHECKER)
    module = importlib.util.module_from_spec(specification)
    # Dataclass resolution looks the defining module up in sys.modules.
    sys.modules["scripts.check_docs"] = module
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
        # Each scenario controls the promises it exercises. Keep inherited
        # commitments neutral in the copied baseline; checks against the real
        # repository retain its actual dates and overdue findings.
        for document in (self.root / "docs").rglob("*.md"):
            content = document.read_text(encoding="utf-8")
            fixture_content = re.sub(
                r"(?m)^(- promise\[[^\]\n]+\]: due=)\d{4}-\d{2}-\d{2}(; status=open;)",
                lambda match: f"{match[1]}{FIXED_TODAY}{match[2]}",
                content,
            )
            if fixture_content != content:
                document.write_text(fixture_content, encoding="utf-8")
        # A lower profile can legitimately retain links to deleted optional
        # templates. Isolate those inherited advisories from strict tests of
        # other rules; the trimmed-link scenario explicitly re-enables them.
        policy = self.read("docs-policy.toml")
        setting = 'trimmed_template_link = "off"'
        if re.search(r"(?m)^trimmed_template_link\s*=", policy):
            policy = re.sub(r"(?m)^trimmed_template_link\s*=.*$", setting, policy)
        else:
            policy = policy.replace("[severity]\n", f"[severity]\n{setting}\n", 1)
        self.write("docs-policy.toml", policy)

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

    def template_inventory(self):
        checker = load_checker_module().DocumentationChecker(self.root, date.fromisoformat(FIXED_TODAY))
        checker.policy = checker.load_toml(self.path("docs-policy.toml"), "docs policy")
        return checker

    def require_template(self, name: str) -> None:
        if name not in self.template_inventory().required_template_files():
            self.skipTest(f"{name} is outside the selected template profile")
        self.assertTrue(self.path(f"templates/{name}").is_file(), f"required template missing: {name}")

    def set_template_profile(self, profile: str) -> None:
        content = self.read("docs-policy.toml")
        updated, count = re.subn(r'^profile = "[^"]+"$', f'profile = "{profile}"',
                                content, count=1, flags=re.M)
        self.assertEqual(count, 1, "fixture has no template profile")
        self.write("docs-policy.toml", updated)

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

    def canonical_guide(
        self,
        *,
        projection_of: str | None = None,
        status: str = "current",
        reconciled: str = "2026-07-28",
    ) -> str:
        projection_line = (
            f"projection_of: {projection_of}\n" if projection_of else ""
        )
        return f"""---
doc_type: guide
status: {status}
authority: guidance
last_reconciled: {reconciled}
{projection_line}---

# Projection guide

## Purpose

Explain the contributor procedure without owning normative behavior.
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

    def test_activated_concerns_route_foundational_runtime(self) -> None:
        """Time and demo stay activated concerns with a method owner.

        The wiring protects declared time and demo policy without choosing
        the adopter's timezone scope or temporal promise. Product correctness
        requires scenario evidence beyond these structural routes.
        """

        development = (REPOSITORY_ROOT / "docs/contracts/development-discipline.md").read_text(
            encoding="utf-8"
        )
        for concern, section in (
            ("Time and calendar", "time-and-calendar"),
            ("Demonstration data", "demonstration-data"),
        ):
            row = next(
                line for line in development.splitlines()
                if f"| {concern} |" in line
            )
            self.assertIn(f"foundational-runtime-discipline.md#{section}", row)
        contract = (
            REPOSITORY_ROOT / "docs/contracts/foundational-runtime-discipline.md"
        ).read_text(encoding="utf-8")
        self.assertIn("contract_role: governance", contract)
        self.assertIn("## How to read this", contract)
        self.assertNotIn("Asia/Shanghai", contract)
        self.assertNotIn("Sibling retrofit classes", contract)
        architecture = (REPOSITORY_ROOT / "ARCHITECTURE.md").read_text(encoding="utf-8")
        self.assertNotIn("## 4. Early implementation declarations", architecture)
        self.assertIn("docs/contracts/foundational-runtime-discipline.md", architecture)

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

    def test_source_reconciliation_accepts_front_middle_and_end_placement(self) -> None:
        original = self.source_contract("- from: source[1], source[2]")
        prefix, remainder = original.split("## Source anchors\n", 1)
        anchors, invariants = remainder.split("## Normative invariants\n", 1)
        sources = "## Source anchors\n" + anchors
        placements = {
            "front": original,
            "middle": (
                prefix + "## Normative invariants\n\n- from: source[1]\n\n"
                + sources + "## Acceptance evidence\n\n- from: source[2]\n"
            ),
            "end": prefix + "## Normative invariants\n" + invariants + "\n" + sources,
        }
        for placement, content in placements.items():
            with self.subTest(placement=placement):
                self.write("docs/contracts/source-example.md", content)
                self.assert_passes()

    def test_unresolved_source_before_definitions_fails(self) -> None:
        content = self.source_contract("- from: source[1], source[2]").replace(
            "## Source anchors", "- from: source[3]\n\n## Source anchors", 1
        )
        self.write("docs/contracts/source-example.md", content)
        self.assert_fails_with("citation does not resolve: source[3]")

    def test_source_block_cannot_cite_itself_into_coverage(self) -> None:
        content = self.source_contract("- from: source[1]").replace(
            "> Preserve the second invariant.",
            "> Preserve the second invariant.\n\n- from: source[2]",
            1,
        )
        self.write("docs/contracts/source-example.md", content)
        self.assert_fails_with("source[2] defined but never cited")

    def test_reordered_sources_retain_definition_validation(self) -> None:
        original = self.source_contract("- from: source[1], source[2]")
        prefix, remainder = original.split("## Source anchors\n", 1)
        anchors, invariants = remainder.split("## Normative invariants\n", 1)
        content = (
            prefix + "## Normative invariants\n" + invariants
            + "\n## Source anchors\n" + anchors
        )
        for invalid, finding in (
            ("### source[1] — 2026-07-25", "duplicate source[1]"),
            ("### source[2] — 2026-02-30", "source[2] date must be YYYY-MM-DD"),
        ):
            with self.subTest(definition=invalid):
                self.write(
                    "docs/contracts/source-example.md",
                    content.replace("### source[2] — 2026-07-25", invalid, 1),
                )
                self.assert_fails_with(finding)

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
                review_due="2026-09-01",
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

    def test_contract_scaffold_requires_addressable_invariant_heading(self) -> None:
        relative = "templates/contract.md"
        content = self.read(relative)
        start = content.index("## Normative invariants\n")
        end = content.index("## Required behaviors\n", start)
        self.write(relative, content[:start] + (
            "## Normative invariants\n\n"
            "- A plain but unaddressable rule.\n"
            "  - from: source[{{N}}]\n\n"
        ) + content[end:])
        self.assert_fails_with("contract template needs a plain-language ### invariant")

    def test_contract_scaffolds_reject_coded_invariant_variants(self) -> None:
        for relative in ("templates/contract.md", "templates/backend-change.md"):
            with self.subTest(template=relative):
                self.require_template(Path(relative).name)
                original = self.read(relative)
                start = original.index("## Normative invariants\n")
                end = original.index("\n## ", start + 1)
                for coded_rule in (
                    "- **INV-1 — Retry identity.** Use one identity.",
                    "### D8 — Retry identity",
                    "### INV-2: Retry identity",
                ):
                    with self.subTest(rule=coded_rule):
                        self.write(relative, original[:start] + (
                            "## Normative invariants\n\n"
                            "### Retry uses the same identity\n\n"
                            "- from: source[{{N}}]\n\n" + coded_rule + "\n"
                        ) + original[end:])
                        self.assert_fails_with("contract template invariant uses a retired code")
                self.write(relative, original)

    def test_plain_invariant_template_keeps_historical_codes_outside_guard(self) -> None:
        self.write("templates/contract.md", self.read("templates/contract.md") + (
            "\n## Historical example\n\n"
            "A prior contract used INV-1; its source remains historical.\n"
            "- **D8 — Prior wording.** Preserved as history.\n"
        ))
        self.write("docs/contracts/legacy-fixture.md", self.basic_contract(
            body="- **INV-1 — Legacy rule.** This unmigrated contract stays valid."
        ))
        self.assert_passes()

    def test_missing_agent_execution_template_fails(self) -> None:
        self.require_template("agent-execution-plan.md")
        self.path("templates/agent-execution-plan.md").unlink()
        self.assert_fails_with(
            "templates/agent-execution-plan.md",
            "required template is missing",
        )

    def test_agent_execution_template_marks_review_topology_high_risk_only(self) -> None:
        self.require_template("agent-execution-plan.md")
        content = self.read("templates/agent-execution-plan.md").replace(
            "High-risk only: delete this section for material work.",
            "Review notes.",
            1,
        )
        self.write("templates/agent-execution-plan.md", content)
        self.assert_fails_with(
            "Review topology must be marked high-risk-only and removable"
        )

    def test_agent_execution_template_rejects_routine_plan_profile(self) -> None:
        self.require_template("agent-execution-plan.md")
        self.write(
            "templates/agent-execution-plan.md",
            self.read("templates/agent-execution-plan.md")
            + "\n- Invalid profile example: `{{routine / material / high-risk}}`\n",
        )
        self.assert_fails_with(
            "agent execution plan is only for material or high-risk work"
        )

    def test_material_agent_plan_does_not_require_review_topology(self) -> None:
        self.require_template("agent-execution-plan.md")
        content = self.read("templates/agent-execution-plan.md")
        start = content.index("## Review topology")
        end = content.index("## Verification and evidence matrix", start)
        self.write(
            "templates/agent-execution-plan.md", content[:start] + content[end:]
        )
        self.assert_passes()

    def test_agent_execution_template_requires_decision_envelope(self) -> None:
        self.require_template("agent-execution-plan.md")
        content = self.read("templates/agent-execution-plan.md")
        content = content.replace(
            "## Engineering decision envelope", "## Decision notes", 1
        )
        self.write("templates/agent-execution-plan.md", content)
        self.assert_fails_with(
            "template missing required section: Engineering decision envelope"
        )

    def test_agent_execution_template_requires_activated_concern_owners(self) -> None:
        self.require_template("agent-execution-plan.md")
        content = self.read("templates/agent-execution-plan.md")
        content = content.replace(
            "## Activated concerns and owners", "## General risks", 1
        )
        self.write("templates/agent-execution-plan.md", content)
        self.assert_fails_with(
            "template missing required section: Activated concerns and owners"
        )

    def test_backend_permission_test_is_security_concern_conditional(self) -> None:
        self.require_template("backend-change.md")
        content = self.read("templates/backend-change.md").replace(
            "{{permission denial when security/privacy is activated}}",
            "{{permission denial}}",
            1,
        )
        self.write("templates/backend-change.md", content)
        self.assert_fails_with(
            "backend permission-denial test must be conditional on security/privacy"
        )

    def test_missing_adoption_assessment_template_fails(self) -> None:
        self.require_template("adoption-assessment.md")
        self.path("templates/adoption-assessment.md").unlink()
        self.assert_fails_with(
            "templates/adoption-assessment.md",
            "required template is missing",
        )

    def test_adoption_assessment_requires_stage_decision(self) -> None:
        self.require_template("adoption-assessment.md")
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
        self.require_template("frontend-surface.md")
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
            'harness_paths = [',
            'harness_paths = ["tools/**", ',
        )
        self.assert_passes()

    def test_declared_repository_root_tooling_files_are_exempt(self) -> None:
        """The shipped tooling declarations protect normal build files."""

        for name in ("setup.py", "conftest.py", "noxfile.py", "vite.config.ts"):
            self.write(name, "VALUE = 1\n")
        self.assert_passes()

    def test_root_application_files_must_be_claimed(self) -> None:
        for name in ("main.py", "server.ts", "worker.rb"):
            with self.subTest(name=name):
                self.write(name, "APPLICATION = 1\n")
                self.assert_fails_with("source files exist outside every configured source root", name)

    def test_declared_root_application_file_activates_adoption(self) -> None:
        self.write("main.py", "APPLICATION = 1\n")
        self.set_policy('source_roots = ["src"]', 'source_roots = ["main.py"]')
        output = self.assert_fails_with(
            "product source exists but architecture template_state is not configured")
        self.assertNotIn("source files exist outside every configured source root", output)

    def test_root_source_gap_respects_early_adoption_and_explicit_tooling(self) -> None:
        self.set_stage("observed")
        self.write("release.py", "TOOLING = 1\n")
        self.assert_advises("source files exist outside every configured source root", "release.py")
        self.set_policy('harness_paths = [', 'harness_paths = ["release.py", ')
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
        self.set_template_profile("minimal")
        inventory = self.template_inventory()
        for name in inventory.known_template_files() - set(inventory.required_template_files()):
            self.path(f"templates/{name}").unlink(missing_ok=True)
        output = self.assert_passes()
        self.assertIn("4 template(s) (profile: minimal)", output)

    def test_lower_profile_still_requires_its_own_tier(self) -> None:
        self.set_template_profile("minimal")
        self.path("templates/contract.md").unlink()
        self.assert_fails_with("templates/contract.md", "required template is missing")

    def test_unknown_template_profile_is_rejected(self) -> None:
        self.set_template_profile("enormous")
        self.assert_fails_with("[templates].profile must be one of")

    def test_required_template_without_declared_doc_type_fails(self) -> None:
        self.set_policy('"guide.md" = "guide"', "")
        self.assert_fails_with(
            "required template has no declared doc_type in [templates.doc_types]"
        )

    def test_reference_to_a_trimmed_template_is_advisory(self) -> None:
        self.set_template_profile("minimal")
        self.set_policy('trimmed_template_link = "off"', 'trimmed_template_link = "advisory"')
        self.path("templates/adoption-assessment.md").unlink(missing_ok=True)
        self.assert_advises(
            "broken local Markdown link: ../../templates/adoption-assessment.md"
        )

    def test_reference_to_an_unknown_template_still_fails(self) -> None:
        self.set_template_profile("minimal")
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

    def test_current_guide_may_project_current_normative_contract(self) -> None:
        self.write(
            "docs/guides/projection.md",
            self.canonical_guide(
                projection_of="docs/contracts/development-discipline.md"
            ),
        )
        self.assert_passes()

    def test_projection_target_must_exist(self) -> None:
        self.write(
            "docs/guides/projection.md",
            self.canonical_guide(
                projection_of="docs/contracts/missing-contract.md"
            ),
        )
        self.assert_fails_with(
            "projection_of points to missing path: docs/contracts/missing-contract.md"
        )

    def test_projection_path_cannot_escape_repository(self) -> None:
        (self.root.parent / "outside.md").write_text("external\n", encoding="utf-8")
        self.write(
            "docs/guides/projection.md",
            self.canonical_guide(projection_of="../outside.md"),
        )
        self.assert_fails_with("projection_of path escapes repository: ../outside.md")

    def test_only_current_guides_may_declare_projection(self) -> None:
        self.replace(
            "docs/plans/2026-07-28-engineering-harness-enablement.md",
            "supersedes: []",
            "supersedes: []\nprojection_of: docs/contracts/development-discipline.md",
        )
        self.assert_fails_with(
            "projection_of is allowed only on a current canonical guide"
        )

    def test_non_current_guide_cannot_keep_projection(self) -> None:
        self.write(
            "docs/guides/reconciling.md",
            self.canonical_guide(
                projection_of="docs/contracts/development-discipline.md",
                status="needs_reconciliation",
            ),
        )
        self.assert_fails_with(
            "projection_of is allowed only on a current canonical guide"
        )

    def test_projection_source_must_be_contract_or_surface(self) -> None:
        self.write(
            "docs/guides/projection.md",
            self.canonical_guide(projection_of="docs/README.md"),
        )
        self.assert_fails_with(
            "projection_of source must be a current normative contract or surface-contract"
        )

    def test_projection_source_must_be_current(self) -> None:
        self.write(
            "docs/contracts/future.md",
            self.basic_contract(status="target", implementation="in_progress"),
        )
        self.write(
            "docs/guides/projection.md",
            self.canonical_guide(projection_of="docs/contracts/future.md"),
        )
        self.assert_fails_with(
            "projection_of source must be a current normative contract or surface-contract"
        )

    def test_later_dated_projection_source_is_advisory(self) -> None:
        self.write("docs/contracts/projection-source.md", self.basic_contract(
            reconciled="2026-08-28"
        ))
        self.write(
            "docs/guides/projection.md",
            self.canonical_guide(
                projection_of="docs/contracts/projection-source.md",
                reconciled="2026-07-27",
            ),
        )
        self.assert_advises(
            "projection review is stale: source reconciled 2026-08-28 after guide 2026-07-27"
        )

    def test_projection_staleness_can_be_switched_off(self) -> None:
        self.set_policy(
            'projection_staleness = "advisory"',
            'projection_staleness = "off"',
        )
        self.write(
            "docs/guides/projection.md",
            self.canonical_guide(
                projection_of="docs/contracts/development-discipline.md",
                reconciled="2026-07-27",
            ),
        )
        result = self.run_checker(strict=True)
        output = result.stdout + result.stderr
        self.assertEqual(result.returncode, 0, output)
        self.assertNotIn("projection review is stale", output)

    def test_same_day_projection_dates_do_not_claim_drift(self) -> None:
        self.write("docs/contracts/projection-source.md", self.basic_contract(
            reconciled="2026-08-28"
        ))
        self.write(
            "docs/guides/projection.md",
            self.canonical_guide(
                projection_of="docs/contracts/projection-source.md",
                reconciled="2026-08-28",
            ),
        )
        output = self.assert_passes()
        self.assertNotIn("projection review is stale", output)

    def assert_no_phrasing_finding(self) -> None:
        result = self.run_checker(strict=True)
        output = result.stdout + result.stderr
        self.assertEqual(result.returncode, 0, output)
        self.assertNotIn("says what something is not", output)

    def enable_rule_phrasing(self) -> None:
        self.set_policy('rule_phrasing = "off"', 'rule_phrasing = "advisory"')

    def phrasing_finding_count(self) -> int:
        result = self.run_checker()
        output = result.stdout + result.stderr
        return output.count("says what something is not")

    def add_task_context_paragraph(self, paragraph: str) -> None:
        self.replace(
            "docs/README.md",
            "#completion-is-layered)\n\n",
            f"#completion-is-layered)\n\n{paragraph}\n\n",
        )

    def test_rule_phrasing_is_off_by_default(self) -> None:
        policy = self.read("docs-policy.toml")
        self.write(
            "docs-policy.toml",
            re.sub(r"(?m)^rule_phrasing\s*=.*\n", "", policy),
        )
        self.add_task_context_paragraph("A manifest alone does not prove reading.")
        self.assert_no_phrasing_finding()

    def test_startup_rule_disclaimer_phrase_is_advisory(self) -> None:
        self.enable_rule_phrasing()
        self.add_task_context_paragraph("A manifest alone does not prove reading.")
        self.assert_advises('"alone does not" says what something is not')

    def test_wrapped_entrypoint_phrase_reports_its_first_line(self) -> None:
        self.enable_rule_phrasing()
        content = self.read("AGENTS.md").rstrip("\n") + "\n"
        self.write("AGENTS.md", content + "\nDelivery of a rule alone\ndoes not apply it.\n")
        line = len(content.splitlines()) + 2
        self.assert_advises(f'line {line}: "alone does not"')

    def test_quoted_and_code_phrases_are_mentions(self) -> None:
        self.enable_rule_phrasing()
        before = self.phrasing_finding_count()
        self.add_task_context_paragraph(
            'Rewrite "a manifest alone does not prove reading" and `need not` as actions.'
        )
        self.assertEqual(self.phrasing_finding_count(), before)

    def test_rules_outside_startup_reading_are_not_scanned(self) -> None:
        self.enable_rule_phrasing()
        before = self.phrasing_finding_count()
        self.replace(
            "docs/README.md",
            "## Conflict rule\n\n",
            "## Conflict rule\n\nA manifest alone does not prove reading.\n\n",
        )
        self.assertEqual(self.phrasing_finding_count(), before)

    def test_rule_phrasing_can_be_switched_off(self) -> None:
        self.enable_rule_phrasing()
        self.set_policy('rule_phrasing = "advisory"', 'rule_phrasing = "off"')
        self.add_task_context_paragraph("A manifest alone does not prove reading.")
        self.assert_no_phrasing_finding()

    def test_heading_fragment_resolves(self) -> None:
        self.write(
            "docs/contracts/frag-target.md",
            self.basic_contract(
                body="## Purpose\n\nOwned behavior.\n\n## Named section\n\nDetails.\n"
            ),
        )
        self.write(
            "docs/guides/linker.md",
            self.canonical_guide()
            + "\nSee [the named section](../contracts/frag-target.md#named-section).\n",
        )
        output = self.assert_passes()
        self.assertNotIn("heading fragment", output)

    def test_broken_heading_fragment_is_advisory_when_retuned(self) -> None:
        self.set_policy(
            'fragment_resolution = "error"', 'fragment_resolution = "advisory"'
        )
        self.write(
            "docs/contracts/frag-target.md",
            self.basic_contract(body="## Purpose\n\nOwned behavior.\n"),
        )
        self.write(
            "docs/guides/linker.md",
            self.canonical_guide()
            + "\nSee [gone](../contracts/frag-target.md#removed-section).\n",
        )
        self.assert_advises("heading fragment does not resolve")

    def test_broken_heading_fragment_blocks_by_default(self) -> None:
        self.write(
            "docs/contracts/frag-target.md",
            self.basic_contract(body="## Purpose\n\nOwned behavior.\n"),
        )
        self.write(
            "docs/guides/linker.md",
            self.canonical_guide()
            + "\nSee [gone](../contracts/frag-target.md#removed-section).\n",
        )
        self.assert_fails_with("heading fragment does not resolve")

    def test_fragment_resolution_off_survives_strict(self) -> None:
        self.set_policy(
            'fragment_resolution = "error"', 'fragment_resolution = "off"'
        )
        self.write(
            "docs/contracts/frag-target.md",
            self.basic_contract(body="## Purpose\n\nOwned behavior.\n"),
        )
        self.write(
            "docs/guides/linker.md",
            self.canonical_guide()
            + "\nSee [gone](../contracts/frag-target.md#removed-section).\n",
        )
        result = self.run_checker(strict=True)
        output = result.stdout + result.stderr
        self.assertEqual(result.returncode, 0, output)
        self.assertNotIn("heading fragment", output)

    def test_completed_status_is_reserved_for_plans(self) -> None:
        self.write(
            "docs/guides/completed.md",
            self.canonical_guide(status="completed"),
        )
        self.assert_fails_with("status completed is reserved for plans")

    def test_current_contract_cannot_be_retired(self) -> None:
        self.write(
            "docs/contracts/retired.md",
            self.basic_contract(implementation="retired"),
        )
        self.assert_fails_with("current contract cannot be implementation: retired")

    def test_supersession_relationships_must_be_bidirectional(self) -> None:
        old = self.basic_contract(
            status="superseded", implementation="retired", title="Old behavior"
        ).replace(
            "supersedes: []",
            "supersedes: []\nsuperseded_by: docs/contracts/new.md",
        )
        self.write("docs/contracts/old.md", old)
        self.write(
            "docs/contracts/new.md", self.basic_contract(title="New behavior")
        )
        self.assert_fails_with(
            "superseded_by relationship is not reciprocated by supersedes"
        )

    def test_supersession_target_must_be_canonical(self) -> None:
        new = self.basic_contract(title="New behavior").replace(
            "supersedes: []", "supersedes: README.md"
        )
        self.write("docs/contracts/new.md", new)
        self.assert_fails_with(
            "supersedes must target a canonical document: README.md"
        )

    def test_supersession_cannot_cross_authority_or_document_type(self) -> None:
        old = self.basic_contract(
            status="superseded", implementation="retired", title="Old behavior"
        ).replace(
            "supersedes: []",
            "supersedes: []\nsuperseded_by: docs/evidence/replacement.md",
        )
        replacement = """---
doc_type: evidence
status: historical
authority: evidence
last_reconciled: 2026-07-28
supersedes: docs/contracts/old.md
---

# Replacement evidence

This evidence cannot replace normative authority.
"""
        self.write("docs/contracts/old.md", old)
        self.write("docs/evidence/replacement.md", replacement)
        self.assert_fails_with(
            "supersession endpoints must have the same doc_type and authority"
        )

    def test_document_with_superseded_by_cannot_remain_current(self) -> None:
        old = self.basic_contract(title="Old behavior").replace(
            "supersedes: []",
            "supersedes: []\nsuperseded_by: docs/contracts/new.md",
        )
        new = self.basic_contract(title="New behavior").replace(
            "supersedes: []", "supersedes: docs/contracts/old.md"
        )
        self.write("docs/contracts/old.md", old)
        self.write("docs/contracts/new.md", new)
        self.assert_fails_with(
            "document with superseded_by must be status: superseded"
        )

    def test_bidirectional_supersession_relationship_passes(self) -> None:
        old = self.basic_contract(
            status="superseded", implementation="retired", title="Old behavior"
        ).replace(
            "supersedes: []",
            "supersedes: []\nsuperseded_by: docs/contracts/new.md",
        )
        new = self.basic_contract(title="New behavior").replace(
            "supersedes: []", "supersedes: docs/contracts/old.md"
        )
        self.write("docs/contracts/old.md", old)
        self.write("docs/contracts/new.md", new)
        self.assert_passes()

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

    def style_manifest(self, body: str) -> None:
        self.write("style-ownership.toml", "version = 1\n" + body)

    def adopt_fixture(self) -> None:
        """Satisfy the adoption gates so product source is legal in the fixture."""

        self.configure_architecture_not_applicable(
            "Structural fitness is enforced by language-native tests in this project."
        )
        self.write(
            "docs/contracts/product-behavior.md",
            self.basic_contract(body="Card appearance has one owner."),
        )

    def configured_style_corpus(self) -> None:
        """Two corpus files, one per layer: the shape a passing project has."""

        self.adopt_fixture()
        self.write("src/styles/base/reset.css", "/* base */\n")
        self.write("src/styles/parts/card.css", "/* card */\n")

    def test_absent_style_manifest_changes_nothing(self) -> None:
        """The opt-in property the whole design rests on."""

        self.configured_style_corpus()
        self.assertFalse(self.path("style-ownership.toml").exists())
        output = self.assert_passes()
        self.assertNotIn("style corpus", output)
        self.assertNotIn("style manifest", output)

    def test_template_style_manifest_gates_nothing(self) -> None:
        self.configured_style_corpus()
        self.style_manifest('status = "template"\n')
        self.assert_passes()

    def test_declared_style_layers_partition_the_corpus(self) -> None:
        self.configured_style_corpus()
        self.style_manifest(
            'status = "configured"\n'
            'scan = ["src/styles/**/*.css"]\n\n'
            "[[layers]]\n"
            'name = "base"\n'
            'owner = "design-system"\n'
            'include = ["src/styles/base/**/*.css"]\n\n'
            "[[layers]]\n"
            'name = "parts"\n'
            'owner = "design-system"\n'
            'include = ["src/styles/parts/**/*.css"]\n'
        )
        self.assert_passes()

    def test_style_corpus_file_claimed_by_no_layer_fails(self) -> None:
        self.configured_style_corpus()
        self.write("src/styles/stray.css", "/* nobody owns this */\n")
        self.style_manifest(
            'status = "configured"\n'
            'scan = ["src/styles/**/*.css"]\n\n'
            "[[layers]]\n"
            'name = "base"\n'
            'owner = "design-system"\n'
            'include = ["src/styles/base/**/*.css"]\n\n'
            "[[layers]]\n"
            'name = "parts"\n'
            'owner = "design-system"\n'
            'include = ["src/styles/parts/**/*.css"]\n'
        )
        self.assert_fails_with(
            "style corpus file resolves to no declared layer: src/styles/stray.css"
        )

    def test_style_corpus_file_claimed_by_two_layers_fails(self) -> None:
        self.configured_style_corpus()
        self.style_manifest(
            'status = "configured"\n'
            'scan = ["src/styles/**/*.css"]\n\n'
            "[[layers]]\n"
            'name = "base"\n'
            'owner = "design-system"\n'
            'include = ["src/styles/**/*.css"]\n\n'
            "[[layers]]\n"
            'name = "parts"\n'
            'owner = "design-system"\n'
            'include = ["src/styles/parts/**/*.css"]\n'
        )
        self.assert_fails_with(
            "style corpus file resolves to more than one layer (base, parts): "
            "src/styles/parts/card.css"
        )

    def test_vacuous_style_corpus_fails(self) -> None:
        self.style_manifest(
            'status = "configured"\n'
            'scan = ["src/styles/**/*.css"]\n\n'
            "[[layers]]\n"
            'name = "base"\n'
            'owner = "design-system"\n'
            'include = ["src/styles/base/**/*.css"]\n'
        )
        self.assert_fails_with("style manifest scan matches no files (vacuous corpus)")

    def test_configured_style_manifest_needs_a_layer(self) -> None:
        self.configured_style_corpus()
        self.style_manifest('status = "configured"\nscan = ["src/styles/**/*.css"]\n')
        self.assert_fails_with("configured style manifest needs at least one layer")

    def test_style_layer_requires_an_owner(self) -> None:
        self.configured_style_corpus()
        self.style_manifest(
            'status = "configured"\n'
            'scan = ["src/styles/**/*.css"]\n\n'
            "[[layers]]\n"
            'name = "everything"\n'
            'include = ["src/styles/**/*.css"]\n'
        )
        self.assert_fails_with("style layer everything missing owner")

    def test_style_manifest_glob_cannot_escape_repository(self) -> None:
        (self.root.parent / "outside.css").write_text("/* x */\n", encoding="utf-8")
        self.configured_style_corpus()
        self.style_manifest(
            'status = "configured"\n'
            'scan = ["src/styles/**/*.css"]\n\n'
            "[[layers]]\n"
            'name = "base"\n'
            'owner = "design-system"\n'
            'include = ["../outside.css"]\n'
        )
        self.assert_fails_with(
            "style layer base include glob must stay inside repository: ../outside.css"
        )

    def test_style_tiers_reference_only_lower_tiers(self) -> None:
        self.configured_style_corpus()
        self.style_manifest(
            'status = "configured"\n'
            'scan = ["src/styles/**/*.css"]\n\n'
            "[[layers]]\n"
            'name = "everything"\n'
            'owner = "design-system"\n'
            'include = ["src/styles/**/*.css"]\n\n'
            "[[tiers]]\n"
            'name = "raw"\n'
            'owner = "design-system"\n'
            "may_reference = []\n\n"
            "[[tiers]]\n"
            'name = "role"\n'
            'owner = "design-system"\n'
            'may_reference = ["raw"]\n'
        )
        self.assert_passes()

    def test_style_tier_cannot_reference_upward(self) -> None:
        self.configured_style_corpus()
        self.style_manifest(
            'status = "configured"\n'
            'scan = ["src/styles/**/*.css"]\n\n'
            "[[layers]]\n"
            'name = "everything"\n'
            'owner = "design-system"\n'
            'include = ["src/styles/**/*.css"]\n\n'
            "[[tiers]]\n"
            'name = "raw"\n'
            'owner = "design-system"\n'
            'may_reference = ["role"]\n\n'
            "[[tiers]]\n"
            'name = "role"\n'
            'owner = "design-system"\n'
            "may_reference = []\n"
        )
        self.assert_fails_with("style tier raw may reference only lower tiers: role")

    def test_style_tier_reference_must_resolve(self) -> None:
        self.configured_style_corpus()
        self.style_manifest(
            'status = "configured"\n'
            'scan = ["src/styles/**/*.css"]\n\n'
            "[[layers]]\n"
            'name = "everything"\n'
            'owner = "design-system"\n'
            'include = ["src/styles/**/*.css"]\n\n'
            "[[tiers]]\n"
            'name = "role"\n'
            'owner = "design-system"\n'
            'may_reference = ["no-such-tier"]\n'
        )
        self.assert_fails_with(
            "style tier role references undeclared tier: no-such-tier"
        )

    def test_not_applicable_style_ownership_needs_a_substantive_rationale(self) -> None:
        self.style_manifest('status = "not_applicable"\nrationale = "n/a"\n')
        self.assert_fails_with(
            "not_applicable style ownership requires a substantive rationale"
        )

    def test_substantive_not_applicable_style_ownership_passes(self) -> None:
        self.style_manifest(
            'status = "not_applicable"\n'
            'rationale = "This service renders no user interface and ships no '
            'stylesheet of any kind."\n'
        )
        self.assert_passes()

    def test_unknown_style_manifest_key_is_rejected(self) -> None:
        self.style_manifest('status = "template"\nlayer_count = 7\n')
        self.assert_fails_with("unknown style manifest key: layer_count")

    def test_invalid_style_manifest_status_is_rejected(self) -> None:
        self.style_manifest('status = "enforced"\n')
        self.assert_fails_with("style manifest status must be template, configured")

    def test_missing_style_system_template_fails(self) -> None:
        self.require_template("style-system.md")
        self.path("templates/style-system.md").unlink()
        self.assert_fails_with(
            "templates/style-system.md", "required template is missing"
        )

    def test_style_system_template_requires_layer_ownership_section(self) -> None:
        self.require_template("style-system.md")
        self.replace(
            "templates/style-system.md",
            "## Layer order and ownership",
            "## Layer notes",
        )
        self.assert_fails_with(
            "template missing required section: Layer order and ownership"
        )

    def git(self, *args: str) -> None:
        subprocess.run(
            ["git", *args],
            cwd=self.root,
            check=True,
            capture_output=True,
            text=True,
        )

    def test_copied_template_entrypoint_without_the_template_remote_is_unfinished(self) -> None:
        self.git("init")
        self.assert_fails_with("onboarding is unfinished")

    def test_template_entrypoint_accepts_the_template_remote(self) -> None:
        self.git("init")
        self.git(
            "remote",
            "add",
            "origin",
            "git@github.com:aaaAlexanderaaa/template-project.git",
        )
        self.assert_passes()

    def test_one_remaining_identity_claim_is_still_unfinished(self) -> None:
        self.replace(
            "AGENTS.md",
            "This repository is the engineering discipline template. ",
            "",
        )
        self.git("init")
        self.assert_fails_with("onboarding is unfinished")

    def test_local_entrypoint_does_not_require_the_template_remote(self) -> None:
        text = self.read("AGENTS.md")
        for claim in (
            "This repository is the engineering discipline template. Its work is\n"
            "documentation and project discipline.\n",
            "Onboarding into any other checkout is unfinished while that checkout's agent\n"
            "entrypoint still describes it as this template and its git remote is not\n"
            "https://github.com/aaaAlexanderaaa/template-project.\n",
            "For a request to learn this template",
            "Adoption into another project",
        ):
            self.assertIn(claim, text)
            text = text.replace(claim, "Local project work", 1)
        self.write("AGENTS.md", text)
        self.git("init")
        self.assert_passes()


    def test_required_reading_unit_must_close(self) -> None:
        self.replace("docs/README.md", "<!-- /required-reading: task-context -->", "")
        self.assert_fails_with("required reading", "unclosed unit", "task-context")

    def test_required_reading_dependency_must_resolve(self) -> None:
        self.replace("docs/README.md", "- required-reading: [Authority order](#authority-order)",
                     "- required-reading: [Authority order](#missing-authority)")
        self.assert_fails_with("required reading", "missing-authority")

    def test_required_reading_table_slot_must_match_concern(self) -> None:
        self.replace("docs/contracts/development-discipline.md", "owner:experience |", "owner:wrong |")
        self.assert_fails_with("required reading", "invalid Required reading declaration")


if __name__ == "__main__":
    unittest.main()
