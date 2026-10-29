"""Behavioral fixtures for complete rule delivery and bounded recovery."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

from scripts.rule_reading import RuleError, RuleRepository, utf8_parts
from scripts.check_docs import DocumentationChecker

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts/read_rules.py"


def document(body, kind="contract", **fields):
    metadata = {"doc_type": kind, "authority": "normative", "status": "current"}
    if kind == "contract":
        metadata["contract_role"] = "governance"
    metadata.update(fields)
    return "---\n" + "".join(f"{k}: {v}\n" for k, v in metadata.items()) + "---\n\n" + body


class RuleReadingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.write("AGENTS.md", "# Entry\n\n- required-reading: [Context](docs/README.md#context)\n")
        self.write("docs/README.md", document(
            "<!-- required-reading: core -->\n## Context\nKeep purpose.\n"
            "<!-- /required-reading: core -->\n\n## History\nUnneeded chronology.\n",
            kind="authority-map"))
        self.write("docs/contracts/development-discipline.md", document(
            "# Development\n\n### Activate concerns instead of expanding ceremony\n\n"
            "| Change trait | Activated concern | Minimum questions | Required reading |\n"
            "|---|---|---|---|\n"
            "| User interaction | Experience | Usability | owner:experience |\n"
            "| Analytical explanation | Analytical claims | Evidence | [Analysis](analysis.md) |\n"))
        self.write("docs/contracts/frontend.md", document(
            "<!-- required-reading: frontend -->\n## Frontend\nEvery reachable state.\n"
            "### Keyboard\nKeyboard works.\n<!-- /required-reading: frontend -->\n\n"
            "## Source anchors\nHistorical explanation.\n"))
        self.write("docs/contracts/analysis.md", document("# Analysis\nEvery claim reaches evidence.\n"))
        self.write("docs/design/map.md", document(
            "# Project map\n- required-reading: [Frontend](../contracts/frontend.md#frontend)\n"
            "Explain the project.\n",
            kind="surface-contract", surface="project-map", contract_scope="current-ui"))

    def write(self, relative, text):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def repo(self):
        return RuleRepository(self.root)

    def prepare_visual(self, **kwargs):
        return self.repo().prepare(["experience", "analytical-claims"],
                                   ["experience=docs/design/map.md"], **kwargs)

    def adopt_template(self, name, destination):
        """Use actual source templates and the relocation documented for adopters."""
        source = ROOT / "templates" / name
        if not source.is_file():
            checker = DocumentationChecker(ROOT, date(2026, 10, 29))
            checker.policy = checker.load_toml(ROOT / "docs-policy.toml", "docs policy")
            self.assertNotIn(name, checker.required_template_files(), f"required template missing: {name}")
            self.skipTest(f"optional template {name} is not supplied")
        for path in ["AGENTS.md", "docs/README.md",
                     "docs/contracts/development-discipline.md",
                     "docs/contracts/governance-decision-boundary.md",
                     "docs/contracts/agent-execution-discipline.md"]:
            self.write(path, (ROOT / path).read_text())
        text = source.read_text()
        prefix = "../contracts/" if destination.startswith("docs/design/") else ""
        text = text.replace("../docs/contracts/", prefix)
        text = text.replace("{{surface-slug}}", "trial").replace("{{YYYY-MM-DD}}", "2026-10-28")
        self.write(destination, text)

    def test_complete_units_exclude_unselected_history(self):
        repo = self.repo()
        prepared = repo.prepare(["experience"], ["experience=docs/design/map.md"])
        output = repo.transcript(prepared)
        self.assertIn("Every reachable state.\n### Keyboard\nKeyboard works.", output)
        self.assertNotIn("Historical explanation.", output)
        self.assertNotIn("Unneeded chronology.", output)
        self.assertTrue(output.endswith("READING COMPLETE units=3\n"))
        self.assertEqual(prepared.units[1].identity, "docs/contracts/frontend.md#frontend")

    def test_unmarked_heading_reads_entire_document(self):
        unit = self.repo().resolve("docs/contracts/analysis.md#analysis")
        self.assertEqual(unit.data, (self.root / "docs/contracts/analysis.md").read_bytes())
        self.assertEqual(unit.identifier, "document")

    def test_published_entrypoint_selects_operative_rules_and_keeps_whole_source_available(self):
        path = self.root / "docs/contracts/frontend.md"
        path.write_text(path.read_text().replace("status: current", "status: current\nreading_entrypoint: frontend"))
        repo = self.repo()
        unit = repo.resolve("docs/contracts/frontend.md")
        self.assertEqual(unit.identifier, "frontend")
        self.assertIn(b"Keyboard works.", unit.data)
        self.assertNotIn(b"Historical explanation.", unit.data)
        whole = repo.resolve("docs/contracts/frontend.md#document")
        self.assertEqual(whole.data, path.read_bytes())
        self.assertEqual(repo.resolve("docs/contracts/frontend.md#source-anchors").data, whole.data)

    def test_invalid_published_entrypoints_fail_before_source_delivery(self):
        for entrypoint in ["missing", "document", "#frontend", ""]:
            with self.subTest(entrypoint=entrypoint):
                self.write("docs/contracts/analysis.md", document("# Analysis\nComplete rule.\n",
                           reading_entrypoint=entrypoint))
                with self.assertRaisesRegex(RuleError, "reading_entrypoint"):
                    self.repo().prepare(["analytical-claims"])

    def test_explicit_current_method_gets_complete_dependencies(self):
        self.write("docs/contracts/method.md", document(
            "# Method\n- required-reading: [Keyboard](frontend.md#keyboard)\n"))
        prepared = self.repo().prepare(includes=["docs/contracts/method.md#method"])
        self.assertIn("docs/contracts/frontend.md#frontend", {u.identity for u in prepared.units})
        self.assertEqual(prepared.units[-1].identity, "docs/contracts/method.md#document")

    def test_retained_core_is_revalidated_while_new_domain_bodies_are_delivered(self):
        first_repo = self.repo()
        first = first_repo.prepare(context="live-task")
        self.assertIn("Keep purpose.", first_repo.transcript(first))
        repo = self.repo()
        extended = repo.prepare(["experience"], ["experience=docs/design/map.md"],
                                context="live-task", retained=first.manifest)
        self.assertEqual(len(extended.units), 3)
        self.assertEqual(len(extended.delivered), 2)
        output = repo.transcript(extended)
        self.assertNotIn("Keep purpose.", output)
        self.assertIn("Every reachable state.", output)
        self.assertIn("RETAINED UNIT docs/README.md#core", output)
        self.assertTrue(output.endswith("READING COMPLETE units=3 delivered=2 retained=1\n"))

    def test_retention_rechecks_changed_units_and_all_current_dependencies(self):
        first = self.repo().prepare(context="live-task")
        path = self.root / "docs/README.md"
        path.write_text(path.read_text().replace("Keep purpose.", "Keep revised purpose."))
        repo = self.repo()
        changed = repo.prepare(context="live-task", retained=first.manifest)
        self.assertEqual(len(changed.delivered), 1)
        self.assertIn("Keep revised purpose.", repo.transcript(changed))
        path.write_text(path.read_text().replace("Keep revised purpose.",
            "Keep revised purpose.\n- required-reading: [Missing](missing.md)"))
        with self.assertRaisesRegex(RuleError, "missing"):
            self.repo().prepare(context="live-task", retained=changed.manifest)

    def test_unrelated_source_edit_refreshes_file_identity_without_repeating_valid_unit(self):
        first = self.repo().prepare(context="live-task")
        path = self.root / "docs/README.md"
        path.write_text(path.read_text().replace("Unneeded chronology.", "Later chronology."))
        later = self.repo().prepare(context="live-task", retained=first.manifest)
        self.assertEqual(later.delivered, ())
        self.assertEqual(first.manifest["units"][0]["sha256"], later.manifest["units"][0]["sha256"])
        self.assertNotEqual(first.manifest["units"][0]["file_sha256"], later.manifest["units"][0]["file_sha256"])

    def test_metadata_or_owner_change_cannot_hide_behind_retained_body(self):
        first = self.repo().prepare(context="live-task")
        path = self.root / "docs/README.md"
        path.write_text(path.read_text().replace("authority: normative", "authority: guidance"))
        changed = self.repo().prepare(context="live-task", retained=first.manifest)
        self.assertEqual(len(changed.delivered), 1)
        self.assertEqual(changed.manifest["units"][0]["authority"], "guidance")
        path.write_text(path.read_text().replace("status: current", "status: historical"))
        with self.assertRaisesRegex(RuleError, "lifecycle"):
            self.repo().prepare(context="live-task", retained=changed.manifest)

    def test_retention_needs_matching_live_context_and_valid_unambiguous_receipt(self):
        first = self.repo().prepare(context="live-task")
        for context, receipt in [(None, first.manifest), ("new-session", first.manifest),
                                 ("live-task", {"version": 1}), ("live-task", []),
                                 ("live-task", dict(first.manifest, units=first.manifest["units"] * 2))]:
            with self.subTest(context=context, receipt=type(receipt).__name__):
                with self.assertRaises(RuleError):
                    self.repo().prepare(context=context, retained=receipt)
        fresh = self.repo().prepare(context="new-session")
        self.assertEqual(len(fresh.delivered), len(fresh.units))

    def test_cli_retention_and_context_mismatch_are_explicit(self):
        first = subprocess.run([sys.executable, str(CLI), "--root", str(self.root), "prepare",
                                "--context", "live-task"], capture_output=True)
        self.assertEqual(first.returncode, 0, first.stderr.decode())
        receipt = self.root / "receipt.json"
        receipt.write_text(first.stdout.decode().splitlines()[1])
        command = [sys.executable, str(CLI), "--root", str(self.root), "prepare",
                   "--retained", str(receipt), "--context", "live-task"]
        reused = subprocess.run(command, capture_output=True)
        self.assertEqual(reused.returncode, 0, reused.stderr.decode())
        self.assertNotIn(b"Keep purpose.", reused.stdout)
        self.assertIn(b"retained=1", reused.stdout)
        command[-1] = "new-session"
        rejected = subprocess.run(command, capture_output=True)
        self.assertNotEqual(rejected.returncode, 0)
        self.assertEqual(rejected.stdout, b"")
        self.assertIn(b"context", rejected.stderr)

    def test_cli_malformed_receipt_never_becomes_fresh_success(self):
        receipt = self.root / "receipt.json"
        for content in ["null", "[]", "{broken"]:
            with self.subTest(content=content):
                receipt.write_text(content)
                result = subprocess.run([sys.executable, str(CLI), "--root", str(self.root),
                    "prepare", "--context", "live-task", "--retained", str(receipt)], capture_output=True)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(result.stdout, b"")
                self.assertIn(b"manifest", result.stderr)

    def test_prepare_revalidates_sources_and_target_authority_on_reused_repository(self):
        repo = self.repo()
        first = repo.prepare(context="live-task")
        path = self.root / "docs/README.md"
        path.write_text(path.read_text().replace("Keep purpose.", "Changed current purpose."))
        changed = repo.prepare(context="live-task", retained=first.manifest)
        self.assertIn("Changed current purpose.", repo.transcript(changed))
        self.write("docs/contracts/future.md", document("# Future\nAccepted future rule.\n", status="target"))
        repo.prepare(targets=["docs/contracts/future.md"])
        with self.assertRaisesRegex(RuleError, "lifecycle"):
            repo.prepare(includes=["docs/contracts/future.md"])

    def test_malformed_retention_labels_and_multiline_contexts_have_actionable_errors(self):
        first = self.repo().prepare(context="live-task")
        receipt = json.loads(json.dumps(first.manifest))
        receipt["units"][0]["delivery"] = []
        with self.assertRaisesRegex(RuleError, "delivery"):
            self.repo().prepare(context="live-task", retained=receipt)
        for context in ["", "\n", "a\nb", "a\u0085b", "a\u2028b",
                        "live\u0085", "live\u2028", "live\u2029"]:
            with self.subTest(context=repr(context)), self.assertRaisesRegex(RuleError, "context"):
                self.repo().prepare(context=context)
        self.repo().prepare(context="caf\u00e9-task")

    def test_subheading_resolves_to_enclosing_unit(self):
        unit = self.repo().resolve("docs/contracts/frontend.md#keyboard")
        self.assertEqual(unit.identifier, "frontend")
        self.assertIn(b"Every reachable state.", unit.data)

    def test_unit_cannot_drop_a_subsection(self):
        self.write("docs/contracts/analysis.md", document(
            "<!-- required-reading: a -->\n## A\nFirst half.\n"
            "<!-- /required-reading: a -->\n### More requirements\nSecond half.\n"))
        with self.assertRaisesRegex(RuleError, "subordinate heading"):
            self.repo().resolve("docs/contracts/analysis.md")

    def test_adjacent_unit_cannot_hide_an_omitted_child(self):
        self.write("docs/contracts/analysis.md", document(
            "<!-- required-reading: a -->\n## A\nFirst half.\n"
            "<!-- /required-reading: a -->\n<!-- required-reading: b -->\n"
            "### Child\nSecond half.\n<!-- /required-reading: b -->\n"))
        with self.assertRaisesRegex(RuleError, "subordinate heading"):
            self.repo().resolve("docs/contracts/analysis.md")

    def test_stable_recovery_id_survives_navigation_name_collision(self):
        self.write("docs/contracts/analysis.md", document(
            "<!-- required-reading: stable -->\n## Renamed\nKeep this unit.\n"
            "<!-- /required-reading: stable -->\n\n## Stable\nOther section.\n"))
        repo = self.repo()
        unit = repo.resolve("docs/contracts/analysis.md#renamed")
        self.assertEqual(repo.read(unit.identity, unit.file_digest).data, unit.data)

    def test_entrypoint_cannot_bypass_path_containment(self):
        outside = self.root.parent / (self.root.name + "-entry.md")
        outside.write_text("# Outside\n")
        self.addCleanup(outside.unlink)
        (self.root / "AGENTS.md").unlink()
        (self.root / "AGENTS.md").symlink_to(outside)
        with self.assertRaisesRegex(RuleError, "escape"):
            self.repo().prepare([], [])

    def test_dependency_closure_is_ordered_and_deduplicated(self):
        self.write("docs/contracts/analysis.md", document(
            "# Analysis\n- required-reading: [Keyboard](frontend.md#keyboard)\n"))
        prepared = self.prepare_visual()
        self.assertEqual(len(prepared.units), 4)
        self.assertEqual(len({u.identity for u in prepared.units}), 4)

    def test_ordinary_links_do_not_create_reading_dependencies(self):
        self.write("docs/contracts/analysis.md", document("# Analysis\n[Background](absent.md)\n"))
        self.prepare_visual()

    def test_whole_document_covers_units_without_losing_external_dependencies(self):
        path = self.root / "docs/contracts/frontend.md"
        path.write_text(path.read_text().replace("Every reachable state.",
            "Every reachable state.\n- required-reading: [Guard](guard.md)"))
        self.write("docs/contracts/guard.md", document("# Guard\nExternal prerequisite.\n"))
        self.write("docs/contracts/analysis.md", document(
            "# Analysis\n- required-reading: [Keyboard](frontend.md#keyboard)\n"))
        repo = self.repo()
        prepared = repo.prepare(["experience", "analytical-claims"],
                                ["experience=docs/contracts/frontend.md"])
        identities = [unit.identity for unit in prepared.units]
        self.assertIn("docs/contracts/frontend.md#document", identities)
        self.assertNotIn("docs/contracts/frontend.md#frontend", identities)
        self.assertIn("docs/contracts/guard.md#document", identities)
        self.assertLess(identities.index("docs/contracts/guard.md#document"),
                        identities.index("docs/contracts/frontend.md#document"))
        self.assertEqual(repo.transcript(prepared).count("Every reachable state."), 1)

    def test_whole_document_coverage_does_not_hide_a_dependency_cycle(self):
        path = self.root / "docs/contracts/frontend.md"
        path.write_text(path.read_text().replace("Every reachable state.",
            "Every reachable state.\n- required-reading: [Self](#frontend)"))
        with self.assertRaisesRegex(RuleError, "dependency cycle"):
            self.repo().prepare(["experience"], ["experience=docs/contracts/frontend.md"])

    def test_fenced_examples_do_not_declare_units_edges_or_headings(self):
        self.write("docs/contracts/analysis.md", document(
            "# Analysis\n~~~markdown\n<!-- required-reading: broken -->\n"
            "- required-reading: [Missing](absent.md)\n## Imaginary\n~~~\n"))
        self.prepare_visual()
        with self.assertRaisesRegex(RuleError, "anchor"):
            self.repo().resolve("docs/contracts/analysis.md#imaginary")

    def test_missing_unclosed_duplicate_and_nested_markers_fail(self):
        bodies = [
            "<!-- /required-reading: absent -->\n",
            "<!-- required-reading: a -->\n## A\n",
            "<!-- required-reading: a -->\n## A\n<!-- /required-reading: a -->\n"
            "<!-- required-reading: a -->\n## B\n<!-- /required-reading: a -->\n",
            "<!-- required-reading: a -->\n## A\n<!-- required-reading: b -->\n## B\n",
        ]
        for body in bodies:
            with self.subTest(body=body):
                self.write("docs/contracts/analysis.md", document(body))
                with self.assertRaises(RuleError):
                    self.repo().resolve("docs/contracts/analysis.md")

    def test_unit_cannot_start_mid_prose_or_end_before_remaining_prose(self):
        for body in [
            "<!-- required-reading: a -->\nRemaining prose.\n<!-- /required-reading: a -->\n",
            "<!-- required-reading: a -->\n## A\nFirst half.\n"
            "<!-- /required-reading: a -->\nSecond half.\n",
        ]:
            with self.subTest(body=body):
                self.write("docs/contracts/analysis.md", document(body))
                with self.assertRaisesRegex(RuleError, "heading|prose"):
                    self.repo().resolve("docs/contracts/analysis.md")

    def test_malformed_directive_and_missing_anchor_fail(self):
        for line in ["- required-reading: missing.md", "- required-reading: [Bad](frontend.md#absent)"]:
            self.write("docs/contracts/analysis.md", document("# Analysis\n" + line + "\n"))
            with self.assertRaisesRegex(RuleError, "directive|anchor"):
                self.prepare_visual()

    def test_dependency_cycle_fails_with_path(self):
        self.write("docs/contracts/analysis.md", document(
            "# Analysis\n- required-reading: [Self](analysis.md)\n"))
        with self.assertRaisesRegex(RuleError, "cycle.*analysis.md"):
            self.prepare_visual()

    def test_file_and_symlink_escape_fail(self):
        with self.assertRaisesRegex(RuleError, "escape"):
            self.repo().resolve("../outside.md")
        outside = self.root.parent / (self.root.name + "-outside.md")
        outside.write_text(document("# Outside\n"))
        self.addCleanup(outside.unlink)
        (self.root / "outside.md").symlink_to(outside)
        with self.assertRaisesRegex(RuleError, "escape"):
            self.repo().resolve("outside.md")

    def test_nonlocal_and_missing_sources_fail(self):
        for ref in ["https://example.org/rules.md", "absent.md"]:
            with self.subTest(ref=ref), self.assertRaises(RuleError):
                self.repo().resolve(ref)

    def test_unknown_concern_fails(self):
        with self.assertRaisesRegex(RuleError, "unknown concern"):
            self.repo().prepare(["experince"], [])

    def test_missing_owner_and_owner_for_unselected_concern_fail(self):
        with self.assertRaisesRegex(RuleError, "missing owner"):
            self.repo().prepare(["experience"], [])
        with self.assertRaisesRegex(RuleError, "unselected|slot"):
            self.repo().prepare([], ["experience=docs/design/map.md"])

    def test_owner_must_be_normative_and_role_correct(self):
        for fields in [{"authority": "guidance"}, {"doc_type": "guide"},
                       {"contract_role": "invented"}]:
            self.write("docs/contracts/wrong.md", document("# Wrong\n", **fields))
            with self.subTest(fields=fields), self.assertRaisesRegex(RuleError, "owner|normative|role"):
                self.repo().prepare(["experience"], ["experience=docs/contracts/wrong.md"])

    def test_non_graphical_experience_uses_its_contract_without_frontend(self):
        self.write("docs/contracts/cli.md", document(
            "# Rule reader CLI\nA stale digest names the changed source and asks for prepare.\n"))
        prepared = self.repo().prepare(["experience"], ["experience=docs/contracts/cli.md"])
        output = self.repo().transcript(prepared)
        self.assertIn("A stale digest names the changed source and asks for prepare.", output)
        self.assertNotIn("Every reachable state.", output)
        self.assertEqual({u.identity for u in prepared.units},
                         {"docs/README.md#core", "docs/contracts/cli.md#document"})

    def test_surface_identity_and_scope_required(self):
        for fields in [{"contract_scope": "current-ui"},
                       {"surface": "map", "contract_scope": "future-ui"}]:
            self.write("docs/design/wrong.md", document("# Wrong\n", kind="surface-contract", **fields))
            with self.subTest(fields=fields), self.assertRaisesRegex(RuleError, "surface|scope"):
                self.repo().prepare(["experience"], ["experience=docs/design/wrong.md"])

    def test_multiple_surface_bindings_and_duplicate_dedup(self):
        self.write("docs/design/other.md", document("# Other\n", kind="surface-contract",
                   surface="other", contract_scope="current-ui"))
        prepared = self.repo().prepare(["experience", "experience"], [
            "experience=docs/design/map.md", "experience=docs/design/map.md",
            "experience=docs/design/other.md"])
        self.assertEqual(len(prepared.units), 4)

    def test_historical_and_unselected_target_fail(self):
        for status in ["historical", "superseded", "needs_reconciliation", "target"]:
            self.write("docs/contracts/analysis.md", document("# Analysis\n", status=status))
            with self.subTest(status=status), self.assertRaisesRegex(RuleError, "lifecycle|target"):
                self.prepare_visual()

    def test_explicit_target_is_labeled_and_can_bind(self):
        self.write("docs/design/map.md", document("# Project map\n", kind="surface-contract",
                   surface="project-map", status="target", contract_scope="future-ui"))
        prepared = self.prepare_visual(targets=["docs/design/map.md"])
        self.assertEqual(next(u for u in prepared.units if u.path == "docs/design/map.md").status, "target")

    def test_changed_source_aborts_entire_output(self):
        repo = self.repo(); prepared = repo.prepare([], [])
        self.write("docs/README.md", document("# Changed\n", kind="authority-map"))
        with self.assertRaisesRegex(RuleError, "changed.*prepare"):
            repo.transcript(prepared)

    def test_changed_routing_source_also_invalidates_snapshot(self):
        repo = self.repo(); prepared = repo.prepare([], [])
        with (self.root / "docs/contracts/development-discipline.md").open("a") as f:
            f.write("\nA later decision.\n")
        with self.assertRaisesRegex(RuleError, "changed"):
            repo.transcript(prepared)

    def test_recovery_requires_entire_file_digest(self):
        repo = self.repo(); unit = repo.resolve("docs/contracts/frontend.md#keyboard")
        recovered = repo.read(unit.identity, unit.file_digest)
        self.assertEqual(recovered.data, unit.data)
        path = self.root / unit.path
        path.write_text(path.read_text() + "\nMetadata outside unit changed.\n")
        with self.assertRaisesRegex(RuleError, "digest.*prepare"):
            self.repo().read(unit.identity, unit.file_digest)

    def test_utf8_recovery_parts_reassemble_exact_original_bytes(self):
        original = "## 阅读\nEvery boundary 😀\r\nEnds without newline".encode()
        for size in [4, 5, 13, 1000]:
            parts = utf8_parts(original, size)
            self.assertEqual(b"".join(parts), original)
            self.assertTrue(all(len(p) <= size for p in parts))
            for part in parts:
                part.decode("utf-8")
        with self.assertRaisesRegex(RuleError, "at least 4"):
            utf8_parts(original, 1)

    def test_manifest_has_exact_byte_count_and_source_identities(self):
        prepared = self.prepare_visual()
        for unit, entry in zip(prepared.units, prepared.manifest["units"]):
            self.assertEqual(entry["bytes"], len(unit.data))
            self.assertEqual(entry["sha256"], hashlib.sha256(unit.data).hexdigest())
            self.assertEqual(entry["file_sha256"], hashlib.sha256((self.root / unit.path).read_bytes()).hexdigest())

    def test_crlf_and_mixed_metadata_preserve_exact_source_bytes(self):
        for opening, closing, body in [("\r\n", "\r\n", "\r\n"),
                                       ("\n", "\r\n", "\n"),
                                       ("\r\n", "\n", "\r\n")]:
            with self.subTest(opening=opening, closing=closing, body=body):
                data = (f"---{opening}doc_type: contract{opening}"
                        f"authority: normative{opening}status: current{opening}"
                        f"---{closing}# Analysis{body}Exact source 😀{body}").encode()
                (self.root / "docs/contracts/analysis.md").write_bytes(data)
                repo = self.repo()
                prepared = repo.prepare(["analytical-claims"])
                unit = next(u for u in prepared.units if u.path.endswith("analysis.md"))
                self.assertEqual(unit.data, data)
                self.assertEqual(unit.file_digest, hashlib.sha256(data).hexdigest())
                self.assertEqual(repo.read(unit.identity, unit.file_digest).data, data)
                self.assertEqual(b"".join(utf8_parts(unit.data, 13)), data)

    def test_cli_accepts_crlf_checkout_without_rewriting_sources(self):
        for path in self.root.rglob("*.md"):
            path.write_bytes(path.read_bytes().replace(b"\n", b"\r\n"))
        before = {p: p.read_bytes() for p in self.root.rglob("*.md")}
        result = subprocess.run([sys.executable, str(CLI), "--root", str(self.root), "prepare"],
                                capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        self.assertIn(b"## Context\r\nKeep purpose.\r\n", result.stdout)
        self.assertTrue(result.stdout.endswith(b"READING COMPLETE units=1\n"))
        unit = self.repo().resolve("docs/README.md#core")
        recovered = subprocess.run([sys.executable, str(CLI), "--root", str(self.root), "read",
            "--unit", unit.identity, "--digest", unit.file_digest], capture_output=True)
        self.assertEqual(recovered.returncode, 0, recovered.stderr.decode())
        self.assertIn(b"BEGIN CONTENT\n" + unit.data + b"\nEND CONTENT\nUNIT COMPLETE\n",
                      recovered.stdout)
        self.assertEqual({p: p.read_bytes() for p in before}, before)

    def test_cli_whole_transaction_and_digest_recovery(self):
        result = subprocess.run([sys.executable, str(CLI), "--root", str(self.root), "prepare"],
                                capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        self.assertIn(b"Keep purpose.", result.stdout)
        self.assertTrue(result.stdout.endswith(b"READING COMPLETE units=1\n"))
        unit = self.repo().resolve("docs/README.md#context")
        result = subprocess.run([sys.executable, str(CLI), "--root", str(self.root), "read",
            "--unit", unit.identity, "--digest", unit.file_digest, "--part", "1", "--part-size", "8"],
            capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        self.assertIn(b"PART COMPLETE", result.stdout)

    def test_cli_rejects_part_zero_without_emitting_a_body(self):
        unit = self.repo().resolve("docs/README.md#context")
        result = subprocess.run([sys.executable, str(CLI), "--root", str(self.root), "read",
            "--unit", unit.identity, "--digest", unit.file_digest, "--part", "0"], capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, b"")

    def test_checker_detects_declarations_without_executing_them(self):
        path = "docs/contracts/analysis.md"
        self.write(path, document("# Analysis\n- required-reading: [Bad](frontend.md#absent)\n"))
        errors = self.repo().validate_declarations([path])
        self.assertTrue(any("anchor" in message for _, message in errors))

    def test_checker_rejects_mismatched_owner_slot_in_trigger_table(self):
        path = self.root / "docs/contracts/development-discipline.md"
        path.write_text(path.read_text().replace("owner:experience", "owner:wrong"))
        self.assertTrue(any("Required reading" in msg for _, msg in self.repo().validate_declarations([])))

    def test_direct_lookup_retains_core_only(self):
        prepared = self.repo().prepare([], [])
        self.assertEqual([u.identity for u in prepared.units], ["docs/README.md#core"])

    def test_repository_core_contains_outcome_authority_and_completion(self):
        prepared = RuleRepository(ROOT).prepare([], [])
        identities = {unit.identity for unit in prepared.units}
        self.assertIn("docs/contracts/development-discipline.md#development-core", identities)
        self.assertIn("docs/contracts/governance-decision-boundary.md#governance-core", identities)
        for unit in ["risk", "route", "completion"]:
            self.assertIn("docs/contracts/agent-execution-discipline.md#" + unit, identities)
        output = RuleRepository(ROOT).transcript(prepared)
        self.assertIn("### Preserve decisions and evidence", output)
        self.assertIn("### Outcomes before means", output)

    def test_core_delivers_the_actual_risk_classification_boundaries(self):
        repo = RuleRepository(ROOT)
        output = repo.transcript(repo.prepare())
        for profile in ["Routine", "Material", "High-risk"]:
            self.assertIn("**" + profile + " change:**", output)
        self.assertIn("including compatible additions", output)
        self.assertIn("requires a new normative owner", output)

    def test_actual_product_templates_bind_with_the_established_default_role(self):
        for name in ["contract.md", "backend-change.md", "cross-stack-change.md"]:
            with self.subTest(template=name):
                destination = "docs/contracts/trial.md"
                self.adopt_template(name, destination)
                prepared = self.repo().prepare(["compatibility"],
                    ["compatibility=" + destination], targets=[destination])
                self.assertIn(destination + "#document", {u.identity for u in prepared.units})

    def test_actual_service_template_prepares_its_complete_domain(self):
        destination = "docs/contracts/service.md"
        self.adopt_template("backend-change.md", destination)
        prepared = self.repo().prepare(["reliability-and-operations"],
            ["reliability-and-operations=" + destination], targets=[destination])
        backend = next(u for u in prepared.units if u.identifier == "backend")
        self.assertIn(b"### Backend completion criteria", backend.data)
        self.assertIn(b"restart, retry, timeout", backend.data)
        self.assertNotIn("frontend", {u.identifier for u in prepared.units})

    def test_actual_cross_stack_template_prepares_both_domains(self):
        destination = "docs/contracts/shared.md"
        self.adopt_template("cross-stack-change.md", destination)
        prepared = self.repo().prepare(["compatibility", "state-integrity", "reliability-and-operations"],
            [concern + "=" + destination for concern in
             ["compatibility", "state-integrity", "reliability-and-operations"]], targets=[destination])
        identities = {u.identifier for u in prepared.units}
        self.assertTrue({"backend", "cross-stack"} <= identities)
        self.assertEqual(len(prepared.units), len({u.identity for u in prepared.units}))

    def test_actual_frontend_template_keeps_its_domain_after_documented_relocation(self):
        destination = "docs/design/trial.md"
        self.adopt_template("frontend-surface.md", destination)
        prepared = self.repo().prepare(["experience"], ["experience=" + destination], targets=[destination])
        frontend = next(u for u in prepared.units if u.identifier == "frontend")
        self.assertIn(b"### Frontend completion criteria", frontend.data)
        self.assertNotIn("backend", {u.identifier for u in prepared.units})

    def test_analytical_owner_dependency_recovers_a_missed_selection(self):
        self.write("docs/design/map.md", document(
            "# Project map\n- required-reading: [Analysis](../contracts/analysis.md)\n",
            kind="surface-contract", surface="project-map", contract_scope="current-ui"))
        prepared = self.repo().prepare(["experience"], ["experience=docs/design/map.md"])
        self.assertIn("docs/contracts/analysis.md#document", {u.identity for u in prepared.units})

    def test_time_and_demo_deliver_shared_failure_and_recovery(self):
        for concerns in [["time-and-calendar"], ["demonstration-data"],
                         ["time-and-calendar", "demonstration-data"]]:
            with self.subTest(concerns=concerns):
                repo = RuleRepository(ROOT)
                output = repo.transcript(repo.prepare(concerns))
                self.assertIn("## Failure, recovery, and intervention", output)
                self.assertIn("stop and obtain a human data-risk decision.", output)
                self.assertEqual(output.count("stop and obtain a human data-risk decision."), 1)
                self.assertIn("Follow the declared reject/unknown policy; do not guess", output)
                self.assertTrue(output.rstrip().splitlines()[-1].startswith("READING COMPLETE"))

    def test_repository_domain_detail_adds_to_core_without_a_product_surface(self):
        prepared = RuleRepository(ROOT).prepare(["analytical-claims"], [])
        self.assertIn("docs/contracts/data-analysis-discipline.md#analysis", {u.identity for u in prepared.units})

    def test_repository_cli_experience_accepts_its_actual_harness_owner(self):
        result = subprocess.run([sys.executable, str(CLI), "prepare", "--concern", "experience",
            "--owner", "experience=docs/contracts/documentation-harness.md"],
            cwd=ROOT, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        self.assertIn(b"Complete rule delivery is a read-only transaction", result.stdout)
        self.assertNotIn(b"BEGIN UNIT docs/contracts/development-discipline.md#frontend", result.stdout)
        self.assertIn(b"READING COMPLETE units=", result.stdout)

    def test_backend_heading_delivers_its_complete_domain_without_other_domains(self):
        unit = RuleRepository(ROOT).resolve(
            "docs/contracts/development-discipline.md#backend-and-service-development-contract")
        self.assertEqual(unit.identifier, "backend")
        self.assertIn(b"### Backend completion criteria", unit.data)
        self.assertIn(b"restart, retry, timeout", unit.data)
        self.assertNotIn(b"### Frontend completion criteria", unit.data)
        self.assertNotIn(b"## Source anchors", unit.data)


if __name__ == "__main__":
    unittest.main()
