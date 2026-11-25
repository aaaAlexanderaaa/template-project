# Role: Tests behavioral engineering-discipline rules, downstream init transfer fidelity, and cross-document consistency.
# Out of scope: Testing browser pixel rendering or low-level TOML parser edge cases (covered in sibling test suites).
# Anchors: ADR-004, SRC-020

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from projectlib.context_pack import build_lineage_trace  # noqa: E402
from projectlib.doc_inventory import index_repository_docs_and_dirs  # noqa: E402
from projectlib.git_telemetry import compare_git_refs  # noqa: E402
from projectlib.loader import load_project_graph  # noqa: E402
from projectlib.server import mark_review_anchor  # noqa: E402
from projectlib.toml_writer import archive_completed_milestone, mutate_task_in_work_toml, serialize_work_toml  # noqa: E402
from projectlib.validator import validate_project_graph  # noqa: E402
from read_rules import inspect_external_target  # noqa: E402
from rule_reading import RuleRepository  # noqa: E402

TEMPLATE_INTERNAL_DOMAINS = {"discipline", "graph-engine", "perspective-ui", "reference-app"}


class DisciplineTransferAndConsistencyTests(unittest.TestCase):
    def _init_repo(self, target: Path, name: str, lang: str, stage: str = "prototype") -> None:
        proc = subprocess.run(
            [sys.executable, "-B", str(SCRIPTS_DIR / "project.py"), "init", "--target", str(target), "--name", name, "--lang", lang, "--stage", stage],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)

    def test_init_en_and_zh_transfer_core_rules_without_leaking_template_domains(self) -> None:
        for lang, name in (("en", "Billing Core"), ("zh", "计费核心")):
            with tempfile.TemporaryDirectory() as tmp:
                repo = Path(tmp)
                self._init_repo(repo, name, lang)

                for rel in (
                    "AGENTS.md",
                    "ARCHITECTURE.md",
                    "architecture-rules.toml",
                    "docs/README.md",
                    "docs/contracts/architecture-and-modularity.md",
                    "docs/contracts/delivery-and-verification.md",
                    "docs/guides/grill.md",
                    ".agents/skills/grill/SKILL.md",
                    ".agents/skills/onboard-discipline/SKILL.md",
                    "templates/adr.md",
                    "templates/domain-readme.md",
                    "templates/module-spec.md",
                    "templates/surface-spec.md",
                    "templates/charter.md",
                    "templates/adoption-assessment.md",
                    "templates/independent-review.md",
                    "templates/architecture-rules.toml",
                    "templates/ci/docs-check.example.yml",
                    "src/example/__init__.py",
                    "tests/test_smoke.py",
                ):
                    self.assertTrue((repo / rel).is_file(), f"Missing transferred file {rel} for lang={lang}")
                for web_rel in (
                    "scripts/projectlib/web/index.html",
                    "scripts/projectlib/web/styles/tokens.css",
                    "scripts/projectlib/web/js/views.js",
                ):
                    self.assertTrue((repo / web_rel).is_file(), f"Missing transferred web asset {web_rel} for lang={lang}")

                agents_txt = (repo / "AGENTS.md").read_text(encoding="utf-8")
                docs_readme_txt = (repo / "docs" / "README.md").read_text(encoding="utf-8")
                arch_txt = (repo / "ARCHITECTURE.md").read_text(encoding="utf-8")
                adr_tpl_txt = (repo / "templates" / "adr.md").read_text(encoding="utf-8")
                spec_tpl_txt = (repo / "templates" / "module-spec.md").read_text(encoding="utf-8")
                self.assertTrue("closed-loop" in agents_txt or "闭环" in agents_txt)
                self.assertTrue("unapproved drafts" in agents_txt or "未批准设计" in agents_txt)
                self.assertIn("charter.md", agents_txt)
                self.assertIn("task-context", docs_readme_txt)
                self.assertIn("```mermaid", arch_txt)
                if lang == "zh":
                    self.assertIn("先用平实直接的中文", agents_txt)
                    self.assertIn("禁止", arch_txt)
                    self.assertRegex(adr_tpl_txt, r"[\u4e00-\u9fff]")
                    self.assertRegex(spec_tpl_txt, r"[\u4e00-\u9fff]")
                    self.assertNotIn("{{One sentence", spec_tpl_txt)
                    self.assertFalse((repo / "templates" / "adr.zh.md").exists())
                    self.assertFalse((repo / "templates" / "module-spec.zh.md").exists())
                else:
                    self.assertIn("Forbidden", arch_txt)

                # Verify downstream copied CLI (status, context, export-html) and web-omitted server in subprocess
                out_html = repo / "tmp-overview.html"
                exp_proc = subprocess.run(
                    [sys.executable, "-B", str(repo / "scripts" / "project.py"), "export-html", "--output", str(out_html)],
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(exp_proc.returncode, 0, exp_proc.stdout + exp_proc.stderr)
                out_html_txt = out_html.read_text(encoding="utf-8")
                self.assertIn("__PERSPECTIVE_DATA__", out_html_txt)
                self.assertIn("--bg-canvas", out_html_txt)
                self.assertIn('data-view="overview"', out_html_txt)
                self.assertNotIn('style="', out_html_txt)

                st_proc = subprocess.run(
                    [sys.executable, "-B", str(repo / "scripts" / "project.py"), "status"],
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(st_proc.returncode, 0, st_proc.stdout + st_proc.stderr)
                if lang == "zh":
                    self.assertIn("示例业务域", st_proc.stdout)
                    self.assertIn("个文件", st_proc.stdout)
                    self.assertNotIn(" files,", st_proc.stdout)
                    ctx_proc = subprocess.run(
                        [sys.executable, "-B", str(repo / "scripts" / "project.py"), "context", "src"],
                        capture_output=True,
                        text=True,
                        check=False,
                    )
                    self.assertEqual(ctx_proc.returncode, 0, ctx_proc.stdout + ctx_proc.stderr)
                    self.assertIn("个文件 |", ctx_proc.stdout)
                    self.assertNotIn(" files |", ctx_proc.stdout)

                srv_script = (
                    "import json, socket, sys, threading\n"
                    f"sys.path.insert(0, {str(repo / 'scripts')!r})\n"
                    "from pathlib import Path\n"
                    "from projectlib.server import create_perspective_server\n"
                    f"repo_p = Path({str(repo)!r})\n"
                    "srv = create_perspective_server(repo_p, port=0)\n"
                    "try:\n"
                    "  for p in ('/', '/api/graph', '/api/overview'):\n"
                    "    c, s = socket.socketpair()\n"
                    "    t = threading.Thread(target=lambda: (srv.RequestHandlerClass(s, ('127.0.0.1', 0), srv), s.close()), daemon=True)\n"
                    "    t.start(); c.sendall(f'GET {p} HTTP/1.1\\r\\nHost: localhost\\r\\nConnection: close\\r\\n\\r\\n'.encode())\n"
                    "    chunks = []\n"
                    "    while (d := c.recv(65536)): chunks.append(d)\n"
                    "    t.join(5); c.close()\n"
                    "    h, _, b = b''.join(chunks).partition(b'\\r\\n\\r\\n')\n"
                    "    assert h.splitlines()[0].split()[1] == b'200', (p, h)\n"
                    "    if p == '/':\n"
                    "      assert b'data-view=\"overview\"' in b, p\n"
                    "    else:\n"
                    "      d = json.loads(b.decode())\n"
                    "      assert 'domains' in d and 'project' in d and 'directory_map' in d, (p, sorted(d))\n"
                    "finally:\n"
                    "  srv.server_close()\n"
                    "web_dir = repo_p / 'scripts' / 'projectlib' / 'web'\n"
                    "bak_dir = repo_p / 'scripts' / 'projectlib' / 'web_omitted'\n"
                    "web_dir.rename(bak_dir)\n"
                    "srv2 = create_perspective_server(repo_p, port=0)\n"
                    "try:\n"
                    "  c, s = socket.socketpair()\n"
                    "  t = threading.Thread(target=lambda: (srv2.RequestHandlerClass(s, ('127.0.0.1', 0), srv2), s.close()), daemon=True)\n"
                    "  t.start(); c.sendall(b'GET / HTTP/1.1\\r\\nHost: localhost\\r\\nConnection: close\\r\\n\\r\\n')\n"
                    "  chunks = []\n"
                    "  while (d := c.recv(65536)): chunks.append(d)\n"
                    "  t.join(5); c.close()\n"
                    "  h, _, b = b''.join(chunks).partition(b'\\r\\n\\r\\n')\n"
                    "  assert h.splitlines()[0].split()[1] == b'200', h\n"
                    "  assert b'Project Overview API Running' in b, b[:200]\n"
                    "finally:\n"
                    "  srv2.server_close()\n"
                    "  bak_dir.rename(web_dir)\n"
                )
                srv_proc = subprocess.run([sys.executable, "-B", "-c", srv_script], capture_output=True, text=True, check=False)
                self.assertEqual(srv_proc.returncode, 0, srv_proc.stdout + srv_proc.stderr)

        for lang, name in (("en", "Stable Core"), ("zh", "稳定核心")):
            with tempfile.TemporaryDirectory() as tmp:
                repo = Path(tmp)
                self._init_repo(repo, name, lang, stage="stable")
                chk = subprocess.run(
                    [sys.executable, "-B", str(repo / "scripts" / "check_docs.py"), "--strict"],
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(chk.returncode, 0, chk.stdout + chk.stderr)

                chk = subprocess.run(
                    [sys.executable, str(repo / "scripts" / "check_docs.py"), "--strict"],
                    cwd=repo,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(chk.returncode, 0, chk.stdout + chk.stderr)

                smk = subprocess.run(
                    [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"],
                    cwd=repo,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(smk.returncode, 0, smk.stdout + smk.stderr)

                (repo / "src" / "example" / "billing.py").write_text(
                    "# Role: Billing domain entrypoint.\n# Out of scope: Web UI.\n# Anchors: SRC-001\n\ndef bill() -> int:\n    return 1\n",
                    encoding="utf-8",
                )
                graph = load_project_graph(repo)
                _, dir_entries = index_repository_docs_and_dirs(repo, graph.modules)
                self.assertEqual(set(graph.domains.keys()), {"example"})
                leaked = [d.domain for d in dir_entries if d.domain in TEMPLATE_INTERNAL_DOMAINS]
                self.assertEqual(leaked, [], f"Leaked template-project domains into initialized repo: {leaked}")
                src_entry = next((d for d in dir_entries if d.path == "src"), None)
                self.assertIsNotNone(src_entry)
                self.assertEqual(src_entry.domain, "example")

    def test_cross_document_consistency_across_contracts_guides_and_work_ledger(self) -> None:
        graph = load_project_graph(ROOT)
        self.assertIn("T-204", graph.tasks)
        t204 = graph.tasks["T-204"]
        self.assertEqual(t204.state, "ready_for_check")
        self.assertEqual(t204.human_check, "pending")
        self.assertIn("SRC-022", t204.selected_option)
        self.assertIn("SRC-022", graph.sources)
        self.assertIn("ADR-005", graph.decisions)

        repo = RuleRepository(ROOT)
        verification_targets = set(repo.CONCERN_MAP["verification"]) | set(repo.CONCERN_MAP["review"])
        self.assertIn("docs/contracts/delivery-and-verification.md#independent-review-definition", verification_targets)
        self.assertIn("docs/contracts/delivery-and-verification.md#discipline-and-transfer-verification", verification_targets)
        self.assertIn("docs/guides/grill.md#behavioral-discipline-evaluation-scenarios", verification_targets)
        frontend_targets = set(repo.CONCERN_MAP["frontend"])
        for span in (
            "docs/contracts/frontend-and-visual-discipline.md#frontend-layers",
            "docs/contracts/frontend-and-visual-discipline.md#frontend-principles",
            "docs/contracts/frontend-and-visual-discipline.md#frontend-best-practices",
            "docs/contracts/frontend-and-visual-discipline.md#owner-preferences",
            "docs/contracts/frontend-and-visual-discipline.md#reference-practices",
            "docs/contracts/frontend-and-visual-discipline.md#pre-delivery-ui-self-check",
        ):
            self.assertIn(span, frontend_targets)
            self.assertIn(span, repo.units)
        from projectlib.checkout_sanitizer import TEMPLATE_INTERNAL_ADRS

        shipped_adrs = {fp.name.split("-")[0] + "-" + fp.name.split("-")[1] for fp in (ROOT / "docs" / "decisions").glob("ADR-*.md")}
        self.assertEqual(shipped_adrs, set(TEMPLATE_INTERNAL_ADRS), "Copied-checkout sanitizer must list every template ADR")
        information_targets = set(repo.CONCERN_MAP["information"])
        for slug in (
            "reader-task-first",
            "organizing-schemes",
            "layering-and-disclosure",
            "form-follows-content",
            "document-types",
            "coverage-scope-freshness",
            "information-self-check",
        ):
            span = f"docs/contracts/information-organization.md#{slug}"
            self.assertIn(span, information_targets)
            self.assertIn(span, repo.units)
        # Every required-reading span declared in docs/contracts/*.md must be registered in CONCERN_MAP
        from rule_reading import MARKER
        mapped_spans = {u for vs in repo.CONCERN_MAP.values() for u in vs}
        for cpath in sorted((ROOT / "docs" / "contracts").glob("*.md")):
            rel_c = cpath.relative_to(ROOT).as_posix()
            for line in cpath.read_text(encoding="utf-8").splitlines():
                mm = MARKER.match(line)
                if mm and not mm.group(1):
                    self.assertIn(f"{rel_c}#{mm.group(2)}", mapped_spans, f"Unmapped contract span: {rel_c}#{mm.group(2)}")
        # Mechanical single-owner derivation: ADR-006 sources flow to affected modules and back without hand-copying
        from projectlib.context_pack import build_context_pack
        info_ctx = build_context_pack(graph, "docs/contracts/information-organization.md")
        info_src_ids = {s["id"] for s in info_ctx["verbatim_sources"]} | {s["id"] for s in info_ctx["decision_sources"]}
        self.assertTrue({"SRC-024", "SRC-025"}.issubset(info_src_ids), info_src_ids)
        src24_trace = build_lineage_trace(graph, "SRC-024")
        src24_mods = {m["id"] for m in src24_trace["modules"]}
        self.assertIn("discipline.entry-and-contracts", src24_mods)
        self.assertIn("ui.perspective-web", src24_mods)
        # Forward (module -> SRC) and reverse (SRC -> module) lineage must agree for every pair
        from projectlib.model import derive_module_source_ids
        reverse = {(m["id"], sid) for sid in graph.sources for m in build_lineage_trace(graph, sid)["modules"]}
        self.assertEqual({(m.id, sid) for m in graph.modules.values() for sid in derive_module_source_ids(graph, m)}, reverse)
        # Computed from raw spec/ADR data (not through module_source_refs): no spec re-lists a quote an ADR already brings
        for m in graph.modules.values():
            via_adr = {sid for d in graph.decisions.values() if d.status != "superseded" and (m.id in d.affects or m.domain in d.affects) for sid in d.sources}
            self.assertEqual(set(m.sources) & via_adr, set(), f"{m.id} hand-copies quotes already reached through an ADR")
        # discipline_version lives authoritatively in docs-policy.toml; check_docs flags any Markdown copy of it
        from projectlib.validator import find_hardcoded_versions
        self.assertEqual(find_hardcoded_versions(ROOT), [])
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_root = Path(tmp_dir)
            (tmp_root / "AGENTS.md").write_text('# Agreement\n\nTemplate (`discipline_version = "2026.11.1"`).\n', encoding="utf-8")
            self.assertEqual(find_hardcoded_versions(tmp_root), [("AGENTS.md", 3, "2026.11.1")])
        # Module context: own sources in full, ADR-reached sources as one-line references naming the ADR
        app_ctx = build_context_pack(graph, "exemplar.app")
        self.assertEqual([s["id"] for s in app_ctx["verbatim_sources"]], list(graph.modules["exemplar.app"].sources))
        via_ids = {s["id"]: s["decision"] for s in app_ctx["decision_sources"]}
        self.assertEqual(via_ids.get("SRC-013"), "ADR-003")
        self.assertTrue(all(s["summary"] and "quote" not in s for s in app_ctx["decision_sources"]))
        for uid in verification_targets:
            self.assertIn(uid, repo.units)

        grill_txt = (ROOT / "docs" / "guides" / "grill.md").read_text(encoding="utf-8")
        for n in range(1, 6):
            self.assertIn(f"Scenario {n}:", grill_txt)

        agents_txt = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        design_txt = (ROOT / "docs" / "design" / "perspective-web.md").read_text(encoding="utf-8")
        self.assertIn("Never treat unapproved drafts as owner sign-off", agents_txt)
        self.assertIn("approved", design_txt)
        self.assertIn("SRC-022", design_txt)
        self.assertIn("Option A:", design_txt)
        self.assertIn("Option B:", design_txt)
        self.assertIn("Option C:", design_txt)

        # Shared multi-domain directories in host repo stay domain-neutral ("")
        dir_by_path = {d.path: d for d in graph.directory_map}
        self.assertEqual(dir_by_path["docs/specs"].domain, "")
        self.assertEqual(dir_by_path["scripts"].domain, "")

        # Superseded ADR-001 must not pull current tasks into its lineage trace
        adr1_trace = build_lineage_trace(graph, "ADR-001")
        adr1_task_ids = {t["id"] for t in adr1_trace["verified_done_tasks"] + adr1_trace["open_or_pending_tasks"]}
        self.assertNotIn("T-201", adr1_task_ids)
        self.assertNotIn("T-203", adr1_task_ids)

    def test_empty_digest_rejected_and_observed_catchall_downgraded(self) -> None:
        bad = subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / "read_rules.py"), "read", "--unit", "AGENTS.md", "--digest", ""],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertNotEqual(bad.returncode, 0)

        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / "src" / "utils").mkdir(parents=True, exist_ok=True)
            (repo / "src" / "utils" / "legacy.py").write_text("x = 1\n", encoding="utf-8")
            inv_unadopted = inspect_external_target(ROOT, repo)
            self.assertIn("src/utils", inv_unadopted["catchall_directories"])
            self.assertEqual(inv_unadopted["budgets_used"]["max_source_lines"], 500)
            self.assertIn(str((ROOT / "AGENTS.md").resolve()), inv_unadopted["required_reading_before_judgment"])

            self._init_repo(repo, "Legacy App", "en")
            self.assertFalse((repo / "docs" / "specs" / "example" / "module.md").exists())
            self.assertFalse((repo / "src" / "example").exists())
            self.assertFalse((repo / "tests" / "test_smoke.py").exists())
            policy = repo / "docs-policy.toml"
            policy.write_text(
                policy.read_text(encoding="utf-8").replace('stage = "adopted"', 'stage = "observed"', 1),
                encoding="utf-8",
            )
            (repo / "src" / "billing").mkdir(parents=True, exist_ok=True)
            (repo / "src" / "billing" / "charge.py").write_text("import utils.legacy\n", encoding="utf-8")

            inv = inspect_external_target(ROOT, repo)
            self.assertLess(inv["code_and_style_loc"], 50)
            self.assertIn("src/utils", inv["catchall_directories"])
            self.assertIn("AGENTS.md", inv["required_reading_before_judgment"])

            graph = load_project_graph(repo)
            self.assertTrue(graph.is_day_zero_synthetic)
            self.assertIn("codebase.src-utils", graph.modules)
            self.assertIn("codebase.src-billing", graph.modules)
            findings, _ = validate_project_graph(graph)
            errors = [f for f in findings if f.severity == "error"]
            advisories = [f for f in findings if f.severity == "advisory"]
            self.assertEqual(errors, [], f"Observed mode should not fail on catchall dir or Path B day0: {errors}")
            self.assertTrue(any(f.rule_id == "catchall_directory" for f in advisories))

            # Unresolved task specs also downgrade to advisory in observed mode after specs start being authored
            (repo / "docs" / "specs" / "billing").mkdir(parents=True, exist_ok=True)
            (repo / "docs" / "specs" / "billing" / "charge.md").write_text(
                '---\nid: billing.charge\ndomain: billing\nowns: ["src/billing/**"]\nsources: [SRC-001]\npromise: ok\n---\n# Billing\n',
                encoding="utf-8",
            )
            work_path = repo / "docs" / "work.toml"
            work_path.write_text(
                work_path.read_text(encoding="utf-8").replace('specs = []', 'specs = ["unwritten.spec"]', 1),
                encoding="utf-8",
            )
            partial = load_project_graph(repo)
            self.assertFalse(partial.is_day_zero_synthetic)
            partial_findings, _ = validate_project_graph(partial)
            self.assertEqual([f for f in partial_findings if f.rule_id == "unknown_spec" and f.severity == "error"], [])
            self.assertTrue(any(f.rule_id == "unknown_spec" and f.severity == "advisory" for f in partial_findings))

    def test_toml_writer_guards_and_git_review_telemetry(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            self._init_repo(repo, "Git Flow App", "en")
            # Preserve unknown keys, guard missing tasks, and record preset blocker_options without SRC duplication
            before_sources = (repo / "docs" / "sources.toml").read_text(encoding="utf-8")
            self.assertFalse(mutate_task_in_work_toml(repo, "T-NOPE", resolution_quote="Must not leak"))
            self.assertEqual((repo / "docs" / "sources.toml").read_text(encoding="utf-8"), before_sources)

            (repo / "docs" / "work.toml").write_text(
                serialize_work_toml(
                    [{"id": "M-1", "domain": "example", "name": "M-1", "slot": "now", "priority": "high"}],
                    [
                        {
                            "id": "T1",
                            "milestone": "M-1",
                            "title": "Choose UI",
                            "state": "blocked",
                            "specs": ["example.module"],
                            "blocker_question": "Pick option?",
                            "blocker_options": ["Option A", "Option B"],
                            "owner_note": "keep-me",
                        }
                    ],
                ),
                encoding="utf-8",
            )
            self.assertTrue(mutate_task_in_work_toml(repo, "T1", new_state="done", resolution_quote="Option A"))
            self.assertEqual((repo / "docs" / "sources.toml").read_text(encoding="utf-8"), before_sources)
            work_after = (repo / "docs" / "work.toml").read_text(encoding="utf-8")
            self.assertIn('selected_option = "Option A"', work_after)
            self.assertIn('priority = "high"', work_after)
            self.assertIn('owner_note = "keep-me"', work_after)

            # Archive distinct milestones whose slug (`work-m-1.toml`) collides without losing T1
            arch_path = archive_completed_milestone(repo, "M-1")
            (repo / "docs" / "work.toml").write_text(
                serialize_work_toml(
                    [{"id": "M/1", "domain": "example", "name": "M1b", "slot": "done"}],
                    [{"id": "T2", "milestone": "M/1", "title": "Second", "state": "done"}],
                ),
                encoding="utf-8",
            )
            archive_completed_milestone(repo, "M/1")
            arch_txt = arch_path.read_text(encoding="utf-8")
            self.assertIn('id = "T1"', arch_txt)
            self.assertIn('id = "T2"', arch_txt)

            # Git diff includes untracked files, Shared Docs & Config domain, and mark-reviewed persists clean anchor
            for cmd in (
                ["git", "init"],
                ["git", "config", "user.email", "test@example.com"],
                ["git", "config", "user.name", "Test"],
                ["git", "add", "."],
                ["git", "commit", "-m", "init"],
            ):
                subprocess.run(cmd, cwd=repo, check=True, capture_output=True)

            target_py = repo / "src" / "example" / "__init__.py"
            target_py.write_text("# Role: Example.\nval = 42\n", encoding="utf-8")
            (repo / "notes-untracked.txt").write_text("line1\nline2\n", encoding="utf-8")
            (repo / "newdir").mkdir(exist_ok=True)
            (repo / "newdir" / "sub.py").write_text("# Role: Untracked subdir file.\n", encoding="utf-8")
            g1 = load_project_graph(repo)
            self.assertIn("src/example/__init__.py", g1.git_summary["changed_files"])
            self.assertIn("example.module", g1.git_summary["modules_since_review"])
            diff_wt = compare_git_refs(repo, g1.modules, "")
            dom_names = {d["domain"] for d in diff_wt["domains"]}
            self.assertIn("Shared Docs & Config", dom_names)
            self.assertNotIn("unclaimed_or_docs", dom_names)
            self.assertGreaterEqual(diff_wt["total_files"], 3)

            (repo / "notes-untracked.txt").unlink()
            (repo / "newdir" / "sub.py").unlink()
            (repo / "newdir").rmdir()
            subprocess.run(["git", "add", "src/example/__init__.py"], cwd=repo, check=True, capture_output=True)
            subprocess.run(["git", "commit", "-m", "clean-commit"], cwd=repo, check=True, capture_output=True)
            mark_review_anchor(repo)
            policy_txt = (repo / "docs-policy.toml").read_text(encoding="utf-8")
            self.assertIn("review_anchor_sha =", policy_txt)
            g2 = load_project_graph(repo)
            self.assertEqual(g2.git_summary["modules_since_review"], [])

    def test_host_task_context_design_html_and_adr_trace_scoping(self) -> None:
        graph = load_project_graph(ROOT)
        adr4_trace = build_lineage_trace(graph, "ADR-004")
        adr4_tasks = {t["id"] for t in adr4_trace["verified_done_tasks"] + adr4_trace["open_or_pending_tasks"]}
        self.assertIn("T-204", adr4_tasks)
        adr3_trace = build_lineage_trace(graph, "ADR-003")
        adr3_tasks = {t["id"] for t in adr3_trace["verified_done_tasks"] + adr3_trace["open_or_pending_tasks"]}
        self.assertNotIn("T-204", adr3_tasks)

        adr5_trace = build_lineage_trace(graph, "ADR-005")
        adr5_tasks = {t["id"] for t in adr5_trace["verified_done_tasks"] + adr5_trace["open_or_pending_tasks"]}
        self.assertIn("T-204", adr5_tasks)

        ctx_t204 = subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / "project.py"), "context", "T-204"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(ctx_t204.returncode, 0, ctx_t204.stderr)
        self.assertIn("ui.perspective-web", ctx_t204.stdout)
        self.assertIn("Selected Option: SRC-022", ctx_t204.stdout)
        self.assertIn("docs/design/frontend-design-options.html", ctx_t204.stdout)

        ctx_html = subprocess.run(
            [sys.executable, "-B", str(SCRIPTS_DIR / "project.py"), "context", "docs/design/frontend-design-options.html"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(ctx_html.returncode, 0, ctx_html.stderr)
        self.assertIn("Document Context", ctx_html.stdout)

        _, dir_entries = index_repository_docs_and_dirs(ROOT, graph.modules)
        dir_map = {d.path: d for d in dir_entries}
        self.assertIn("docs/evaluations/behavioral-scenarios-2026-11.md", dir_map["docs/evaluations"].doc_paths)
        self.assertNotIn("docs/evaluations/behavioral-scenarios-2026-11.md", dir_map["docs"].doc_paths)


if __name__ == "__main__":
    unittest.main()
