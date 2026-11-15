"""Source-shaped discovery, authority, coverage and CLI recovery scenarios."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path
from unittest.mock import patch

from scripts.document_overview import DocumentOverview, render_text
from scripts.rule_reading import RuleError, RuleRepository, parse_frontmatter_text

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts/read_rules.py"


def document(body, *, kind="contract", authority="normative", status="current", extra=""):
    return (f"---\ndoc_type: {kind}\nauthority: {authority}\nstatus: {status}\n"
            f"last_reconciled: 2026-11-01\n{extra}---\n\n{body}")


class DocumentOverviewTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.write("AGENTS.md", "# Project entry\nOpen current owners before changing work.\n")
        self.write("docs/contracts/writing.md", document(
            "# Writing standard\n## Reader-facing quality\n### Avoid mechanical phrasing\n"
            "Retain the agreed voice.\n## Facts\nVerify factual claims.\n"))
        self.write("docs/plans/review.md", document(
            "# Improve the workflow\n## Next action\nReview whether the repair was used.\n",
            kind="plan", authority="planning", status="active"))

    def write(self, path, text):
        file = self.root / path
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(text, encoding="utf-8")
        return file

    def build(self, **kwargs):
        return DocumentOverview(self.root).build(**kwargs)

    def by_path(self, view):
        return {d["path"]: d for d in view["documents"]}

    def cli(self, *args):
        return subprocess.run([sys.executable, str(CLI), "--root", str(self.root), "overview", *args],
                              capture_output=True, text=True, encoding="utf-8")

    def test_discovery_precedes_concern_selection_and_preserves_roles(self):
        self.write("docs/contracts/future.md", document("# Future standard\n", status="target"))
        self.write("docs/guides/voice.md", document("# Voice examples\n", kind="guide", authority="guidance"))
        self.write("docs/evidence/sample.md", document("# Observed sample\n", kind="evidence", authority="evidence"))
        self.write("docs/contracts/conflict.md", document("# Conflicting standards\n", status="needs_reconciliation"))
        view = self.build(include_outline=True)
        records = self.by_path(view)
        self.assertTrue(view["coverage"]["scan_complete"])
        self.assertEqual(records["AGENTS.md"]["category"], "navigation")
        self.assertEqual(records["docs/contracts/writing.md"]["category"], "current_rules")
        self.assertEqual(records["docs/contracts/future.md"]["category"], "target_rules")
        self.assertEqual(records["docs/plans/review.md"]["category"], "active_plans")
        self.assertEqual(records["docs/guides/voice.md"]["category"], "guidance")
        self.assertEqual(records["docs/evidence/sample.md"]["category"], "evidence")
        self.assertEqual(records["docs/contracts/conflict.md"]["category"], "needs_reconciliation")
        standard = records["docs/contracts/writing.md"]
        phrasing = next(h for h in standard["headings"] if h["title"] == "Avoid mechanical phrasing")
        self.assertEqual(phrasing["reference"], "docs/contracts/writing.md#avoid-mechanical-phrasing")
        self.assertEqual((self.root / standard["path"]).read_text().splitlines()[phrasing["line"] - 1],
                         "### Avoid mechanical phrasing")
        self.assertEqual(standard["sha256"], hashlib.sha256((self.root / standard["path"]).read_bytes()).hexdigest())

    def test_closed_work_exits_attention_while_permanent_rules_and_accepted_findings_remain(self):
        self.write("docs/plans/old.md", document("# Finished repair\n", kind="plan", authority="planning", status="completed"))
        self.write("docs/contracts/old.md", document("# Superseded standard\n", status="superseded"))
        self.write("docs/issues/writing.md", document(
            "# Writing findings\n"
            "## W-1 — Fixed typo\n- **Status:** `resolved`\n### Verification\nCorrected.\n"
            "## W-2 — Bad premise\n- **Status:** `disproved`\n"
            "## W-3 — Repeated voice drift\n- **Status:** `verified`\n"
            "## W-4 — Accepted limitation\n- **Status:** `accepted`\n"
            "## W-5 — Deferred repair\n- **Status:** `wontfix`\n"
            "## W-6 — Unknown state\n- **Status:** `maybe`\n"
            "## W-7 — Missing state\n"
            "## W-8 — Contradiction\n- **Status:** `resolved`\n- **Status:** `verified`\n",
            kind="issue-tracker", status="active"))
        view = self.build()
        records = self.by_path(view)
        self.assertIn("docs/contracts/writing.md", records)
        self.assertNotIn("docs/plans/old.md", records)
        self.assertNotIn("docs/contracts/old.md", records)
        self.assertEqual({e["status"] for e in view["coverage"]["excluded"]}, {"completed", "superseded"})
        issues = records["docs/issues/writing.md"]
        self.assertEqual(issues["closed_findings"], 2)
        self.assertEqual([f["status"] for f in issues["findings"]],
                         ["verified", "accepted", "wontfix", "unknown", "unknown", "unknown"])
        self.assertEqual([f["disposition"] for f in issues["findings"][:3]],
                         ["unresolved", "accepted", "wontfix"])
        with self.assertRaisesRegex(RuleError, "lifecycle"):
            RuleRepository(self.root).resolve("docs/issues/writing.md")

    def test_promises_and_dates_keep_source_meaning_and_ignore_examples_and_provenance(self):
        self.write("docs/contracts/writing.md", document(
            "# Writing standard\n## Review commitments\n"
            "- promise[voice]: due=2026-11-01; status=open; owner=editor; description=Check later writing\n"
            "- promise[finished]: due=2020-01-01; status=resolved; owner=editor; description=Finished\n"
            "```text\n- promise[example]: due=2020-01-01; status=open; owner=x; description=Example\n```\n"
            "## Source anchors\n### source[1] — 2020-01-01\n"
            "- promise[history]: due=2020-01-01; status=open; owner=x; description=History\n"
            "## Acceptance evidence\nRelevant current evidence.\n"
            "## Reconciliation log\n- promise[chronology]: due=2020-01-01; status=open; owner=x; description=Chronology\n",
            extra="review_due: 2026-10-24\n"))
        original = self.by_path(self.build())["docs/contracts/writing.md"]
        self.assertEqual([c["timing"] for c in original["commitments"]], ["unassessed", "unassessed"])
        timed = self.by_path(self.build(today=date(2026, 11, 1), include_outline=True))["docs/contracts/writing.md"]
        self.assertEqual([(c["id"], c["timing"]) for c in timed["commitments"]],
                         [("review_due", "past"), ("voice", "due")])
        self.assertEqual(timed["category"], "current_rules")
        source_lines = (self.root / timed["path"]).read_text().splitlines()
        self.assertEqual(source_lines[timed["commitments"][0]["line"] - 1], "review_due: 2026-10-24")
        titles = [h["title"] for h in timed["headings"]]
        self.assertIn("Acceptance evidence", titles)
        self.assertNotIn("Source anchors", titles)
        self.assertFalse(any("source[1]" in t for t in titles))

    def test_unknown_metadata_and_invalid_records_cannot_become_empty_success(self):
        self.write("docs/local-note.md", "# Remember the earlier failure\nApplicability is not declared.\n")
        self.write("docs/bad-role.md", document("# Mismatched role\n", authority="guidance"))
        self.write("docs/bad-promise.md", document(
            "# Commitment\n- promise[uncertain]: status=resolved; status=open; due=2026-11-01\n"))
        result = self.cli("--format", "json")
        self.assertEqual(result.returncode, 2)
        view = json.loads(result.stdout)
        self.assertFalse(view["coverage"]["scan_complete"])
        self.assertIn("docs/local-note.md", view["coverage"]["unclassified"])
        self.assertIn("docs/bad-role.md", view["coverage"]["unclassified"])
        commitment = self.by_path(view)["docs/bad-promise.md"]["commitments"][0]
        self.assertEqual(commitment["status"], "unknown")
        self.assertTrue(view["coverage"]["diagnostics"])

    def test_record_fields_cannot_replace_source_identity_and_empty_review_dates_stay_visible(self):
        self.write("docs/contracts/writing.md", document(
            "# Writing\n"
            "- promise[real]: due=2026-11-01; status=open; owner=editor; description=Review voice; "
            "id=other; line=999; kind=review; timing=future\n", extra="review_due: \n"))
        view = self.build()
        record = self.by_path(view)["docs/contracts/writing.md"]
        review, promise = record["commitments"]
        self.assertEqual((review["id"], review["timing"]), ("review_due", "invalid"))
        source = (self.root / record["path"]).read_text().splitlines()
        self.assertTrue(source[promise["line"] - 1].startswith("- promise[real]:"))
        self.assertEqual((promise["id"], promise["kind"], promise["timing"]),
                         ("real", "promise", "unassessed"))
        self.assertFalse(view["coverage"]["scan_complete"])

    def test_reconciliation_keeps_declared_finding_states_without_promoting_mismatched_roles(self):
        self.write("docs/issues/reconcile.md", document(
            "# Review findings\n## I-1 — Unresolved\n- **Status:** `verified`\n"
            "## I-2 — Chosen disposition\n- **Status:** `wontfix`\n",
            kind="issue-tracker", status="needs_reconciliation"))
        self.write("docs/issues/wrong-role.md", document(
            "# Not an issue owner\n## I-3\n- **Status:** `verified`\n",
            kind="issue-tracker", authority="guidance", status="needs_reconciliation"))
        records = self.by_path(self.build())
        pending = records["docs/issues/reconcile.md"]
        self.assertEqual(pending["category"], "needs_reconciliation")
        self.assertEqual([f["status"] for f in pending["findings"]], ["verified", "wontfix"])
        self.assertEqual(records["docs/issues/wrong-role.md"]["category"], "unclassified")
        self.assertFalse(records["docs/issues/wrong-role.md"]["findings"])

    def test_expanded_text_delivers_every_heading_and_source_line_order(self):
        self.write("docs/issues/review.md", document(
            "# Findings\n## I-1 — Closed\n- **Status:** `resolved`\n"
            "## I-2 — Open\n- **Status:** `verified`\n"
            "- promise[observe]: due=2026-11-01; status=open; owner=editor; description=Observe next use\n"
            "### Detail\nMore information.\n", kind="issue-tracker", status="active"))
        view = self.build(sources=["docs/issues"], include_outline=True)
        text = render_text(view)
        record = view["documents"][0]
        for heading in record["headings"]:
            self.assertIn(f"L{heading['line']}: heading H{heading['level']}: {heading['title']}", text)
        self.assertEqual([f["title"] for f in record["findings"]], ["I-2 — Open"])
        numbers = [int(n) for n in re.findall(r"^  L(\d+):", text, re.M)]
        self.assertEqual(numbers, sorted(numbers))
        compact = render_text(self.build(sources=["docs/issues"]))
        self.assertNotIn("I-1 — Closed", compact)

    def test_date_bound_pagination_carries_its_calendar_reference(self):
        first = self.cli("--today", "2026-11-01", "--limit", "1", "--format", "json")
        view = json.loads(first.stdout)
        hint = render_text(view).split("More documents: ", 1)[1]
        self.assertIn("--today 2026-11-01", hint)
        follow = ("--offset", "1", "--snapshot", view["snapshot"], "--limit", "1")
        self.assertEqual(self.cli(*follow, "--today", "2026-11-01").returncode, 0)
        missing_date = self.cli(*follow)
        self.assertNotEqual(missing_date.returncode, 0)
        self.assertEqual(missing_date.stdout, "")

    def test_unreadable_sources_are_partial_and_recovery_requires_a_new_scan(self):
        target = (self.root / "docs/contracts/writing.md").resolve()
        real_read = Path.read_bytes
        calls = 0
        def denied(path):
            if path == target:
                raise PermissionError("controlled unreadable source")
            return real_read(path)
        with patch.object(Path, "read_bytes", denied):
            view = self.build()
        self.assertFalse(view["coverage"]["scan_complete"])
        self.assertIsNone(self.by_path(view)["docs/contracts/writing.md"]["sha256"])
        def recovers(path):
            nonlocal calls
            if path == target:
                calls += 1
                if calls == 1:
                    raise PermissionError("controlled unreadable source")
            return real_read(path)
        with patch.object(Path, "read_bytes", recovers):
            with self.assertRaisesRegex(RuleError, "recovered"):
                self.build()

    def test_narrow_scope_ignores_broken_unselected_entrypoint_and_invalid_root_emits_no_view(self):
        self.write("AGENTS.md", "# Entry\n```\nUnclosed example\n")
        selected = self.cli("--source", "docs/contracts", "--format", "json")
        self.assertEqual(selected.returncode, 0, selected.stderr)
        self.assertTrue(json.loads(selected.stdout)["coverage"]["scan_complete"])
        invalid = subprocess.run([sys.executable, str(CLI), "--root", str(self.root / "missing"), "overview"],
                                 capture_output=True, text=True)
        self.assertEqual(invalid.returncode, 1)
        self.assertEqual(invalid.stdout, "")
        self.assertIn("root must be an existing directory", invalid.stderr)

    def test_root_access_failures_produce_partial_coverage_and_changed_access_requires_rerun(self):
        overview = DocumentOverview(self.root)
        with patch.object(overview, "open_root", side_effect=PermissionError("controlled root access failure")):
            view = overview.build()
        self.assertFalse(view["coverage"]["scan_complete"])
        self.assertEqual(view["documents"], [])
        self.assertEqual(view["coverage"]["diagnostics"][0]["path"], ".")
        with patch.object(overview, "open_root", side_effect=[PermissionError("controlled root access failure"),
                                                            (self.root, RuleRepository(self.root))]):
            with self.assertRaisesRegex(RuleError, "root access changed"):
                overview.build()

    def test_duplicate_metadata_is_ambiguous_in_both_overview_and_reader(self):
        body = document("# Conflicting lifecycle\n").replace("status: current", "status: current\nstatus: historical")
        self.write("docs/contracts/ambiguous.md", body)
        self.assertIn("duplicate", parse_frontmatter_text(body)[1])
        view = self.build()
        self.assertFalse(view["coverage"]["scan_complete"])
        self.assertEqual(self.by_path(view)["docs/contracts/ambiguous.md"]["category"], "unclassified")
        with self.assertRaisesRegex(RuleError, "duplicate"):
            RuleRepository(self.root).resolve("docs/contracts/ambiguous.md")

    def test_paging_has_explicit_coverage_and_stale_continuation_fails_before_output(self):
        first = self.cli("--format", "json", "--limit", "1")
        self.assertEqual(first.returncode, 0, first.stderr)
        view = json.loads(first.stdout)
        self.assertEqual(view["page"], {"offset": 0, "limit": 1, "total": 3, "shown": 1, "next_offset": 1})
        second = self.cli("--format", "json", "--offset", "1", "--limit", "1", "--snapshot", view["snapshot"])
        next_view = json.loads(second.stdout)
        self.assertNotEqual(view["documents"][0]["path"], next_view["documents"][0]["path"])
        self.assertEqual(next_view["snapshot"], view["snapshot"])
        self.write("docs/contracts/writing.md", document("# Revised standard\n"))
        stale = self.cli("--offset", "1", "--snapshot", view["snapshot"])
        self.assertNotEqual(stale.returncode, 0)
        self.assertEqual(stale.stdout, "")
        self.assertIn("snapshot changed", stale.stderr)

    def test_selected_scope_and_inactive_inventory_are_explicit(self):
        self.write("notes/voice.md", document("# Local note standard\n"))
        self.write("notes/node_modules/ignored.md", document("# Dependency content\n"))
        view = self.build(sources=["notes", "notes/voice.md"])
        self.assertEqual(list(self.by_path(view)), ["notes/voice.md"])
        self.assertEqual(view["coverage"]["files_discovered"], 1)
        self.assertIn("node_modules", view["coverage"]["directory_exclusions"])
        self.assertEqual(view["sources"], ["notes", "notes/voice.md"])

    def test_empty_scope_and_missing_scope_are_distinguishable(self):
        (self.root / "empty").mkdir()
        empty = self.cli("--source", "empty", "--format", "json")
        self.assertEqual(empty.returncode, 0)
        self.assertTrue(json.loads(empty.stdout)["coverage"]["scan_complete"])
        missing = self.cli("--source", "missing", "--format", "json")
        self.assertEqual(missing.returncode, 2)
        self.assertFalse(json.loads(missing.stdout)["coverage"]["scan_complete"])

    def test_escaping_files_and_directory_symlinks_never_expose_external_content(self):
        outside = tempfile.TemporaryDirectory()
        self.addCleanup(outside.cleanup)
        secret = Path(outside.name) / "outside.md"
        secret.write_text("# PRIVATE-CONTENT-MUST-NOT-APPEAR\n")
        (self.root / "docs/escape.md").symlink_to(secret)
        (self.root / "docs/linked-directory").symlink_to(outside.name, target_is_directory=True)
        result = self.cli("--format", "json")
        self.assertEqual(result.returncode, 2)
        self.assertNotIn("PRIVATE-CONTENT-MUST-NOT-APPEAR", result.stdout)
        self.assertEqual(len(json.loads(result.stdout)["coverage"]["diagnostics"]), 2)

    def test_source_mutation_and_membership_change_abort_the_read(self):
        for change in ["contents", "membership"]:
            with self.subTest(change=change):
                overview = DocumentOverview(self.root)
                recheck = overview.recheck
                def mutate(*args):
                    self.write("docs/contracts/writing.md" if change == "contents" else "docs/new.md",
                               document("# Changed during discovery\n"))
                    recheck(*args)
                with patch.object(overview, "recheck", side_effect=mutate):
                    with self.assertRaisesRegex(RuleError, "changed"):
                        overview.build()

    def test_non_utf8_and_unclosed_examples_are_reported_with_partial_coverage(self):
        (self.root / "docs/binary.md").write_bytes(b"\xff\xfe")
        self.write("docs/open-fence.md", document("# Rule\n```\nExample never ends\n"))
        view = self.build()
        self.assertFalse(view["coverage"]["scan_complete"])
        self.assertEqual(len(view["coverage"]["diagnostics"]), 2)
        self.assertIn("docs/binary.md", view["coverage"]["unclassified"])

    def test_invalid_arguments_are_actionable_and_leave_stdout_empty(self):
        for args in [("--offset", "-1"), ("--limit", "0"), ("--today", "20261101"),
                     ("--today", "2026-02-30"), ("--source", "docs#section")]:
            with self.subTest(args=args):
                result = self.cli(*args)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(result.stdout, "")
                self.assertTrue(result.stderr)

    def test_cli_outputs_text_and_json_without_changing_the_source_tree(self):
        def snapshot():
            return {p.relative_to(self.root).as_posix(): p.read_bytes()
                    for p in self.root.rglob("*") if p.is_file()}
        before = snapshot()
        text = self.cli("--outline")
        structured = self.cli("--format", "json")
        self.assertEqual(text.returncode, 0, text.stderr)
        self.assertEqual(structured.returncode, 0, structured.stderr)
        self.assertIn("Avoid mechanical phrasing", text.stdout)
        self.assertIn("Improve the workflow", text.stdout)
        self.assertTrue(text.stdout.endswith("OVERVIEW COMPLETE\n"))
        self.assertEqual(json.loads(structured.stdout)["schema_version"], 1)
        self.assertEqual(snapshot(), before)

    def test_compact_view_keeps_all_document_categories_and_explicit_heading_expansion(self):
        view = self.build(limit=1)
        self.assertEqual(view["detail"], "documents")
        self.assertEqual(view["documents"][0]["headings"], [])
        self.assertGreater(view["documents"][0]["heading_count"], 0)
        self.assertEqual(view["coverage"]["categories"]["active_plans"], 1)
        full = self.build(limit=1, include_outline=True, snapshot=view["snapshot"])
        self.assertEqual(full["detail"], "headings")
        self.assertTrue(full["documents"][0]["headings"])

    def test_frontmatter_is_data_and_ambiguous_anchors_fall_back_to_the_file(self):
        self.write("docs/contracts/writing.md", document(
            "# Writing\n## Facts\nCheck facts.\n## Source anchors\n### Facts\nHistorical use.\n",
            extra="- promise[metadata-example]: due=2020-01-01; status=open; owner=x; description=Header data\n"))
        record = self.by_path(self.build(include_outline=True))["docs/contracts/writing.md"]
        self.assertFalse(record["commitments"])
        facts = next(h for h in record["headings"] if h["title"] == "Facts")
        self.assertEqual(facts["reference"], record["path"])

    def test_large_collection_can_be_browsed_without_losing_a_document(self):
        for number in range(1000):
            self.write(f"collection/{number:04}.md", document(f"# Standard {number}\n## Boundary\nKeep it.\n"))
        first = self.build(sources=["collection"], limit=137)
        seen = []
        current = first
        while True:
            seen.extend(d["path"] for d in current["documents"])
            if current["page"]["next_offset"] is None:
                break
            current = self.build(sources=["collection"], limit=137,
                                 offset=current["page"]["next_offset"], snapshot=first["snapshot"])
        self.assertEqual(first["coverage"]["files_discovered"], 1000)
        self.assertEqual(len(seen), 1000)
        self.assertEqual(len(set(seen)), 1000)


if __name__ == "__main__":
    unittest.main()
