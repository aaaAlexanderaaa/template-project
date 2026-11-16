# Role: Tests digest-verified rule reading (`read_rules.py`) and external repository onboarding (`onboard`).
# Out of scope: HTTP server and static AST import scanning.
# Anchors: spec=graph.validator, ADR-002, SRC-010, SRC-013

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
READ_RULES = ROOT / "scripts" / "read_rules.py"


class ReadRulesAndOnboardTests(unittest.TestCase):
    def _run_cli(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(READ_RULES), *args],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_list_prepare_and_digest_verified_read(self) -> None:
        listed = self._run_cli("list")
        self.assertEqual(listed.returncode, 0, listed.stderr)
        catalog = json.loads(listed.stdout)
        self.assertIn("architecture", catalog["concerns"])
        self.assertIn("css", catalog["concerns"])

        prepared = self._run_cli("prepare", "--concern", "architecture", "--concern", "css", "--owner", "state=ARCHITECTURE.md")
        self.assertEqual(prepared.returncode, 0, prepared.stderr)
        json_head = prepared.stdout.split("\n=== UNIT ", 1)[0]
        manifest = json.loads(json_head)
        units = {u["identity"]: u["sha256"] for u in manifest["units"]}
        self.assertIn("AGENTS.md", units)
        self.assertIn("ARCHITECTURE.md", units)
        self.assertIn("docs/README.md#language-standard", units)
        self.assertIn("docs/contracts/architecture-and-modularity.md#css-modularity", units)

        # Valid digest read succeeds (including section fragment resolution)
        target_unit = "docs/contracts/architecture-and-modularity.md#css-modularity"
        ok_read = self._run_cli("read", "--unit", target_unit, "--digest", units[target_unit])
        self.assertEqual(ok_read.returncode, 0, ok_read.stderr)
        self.assertIn("tokens.css", ok_read.stdout)

        ok_lang = self._run_cli("read", "--unit", "docs/README.md#language-standard", "--digest", units["docs/README.md#language-standard"])
        self.assertEqual(ok_lang.returncode, 0, ok_lang.stderr)
        self.assertIn("plain", ok_lang.stdout.lower())

        # Nonexistent section fragment fails loudly instead of falling back silently
        bad_frag = self._run_cli("read", "--unit", "docs/README.md#nonexistent-section", "--digest", "0" * 64)
        self.assertNotEqual(bad_frag.returncode, 0)

        # Tampered digest fails closed
        bad_read = self._run_cli("read", "--unit", target_unit, "--digest", "0" * 64)
        self.assertNotEqual(bad_read.returncode, 0)
        self.assertIn("digest mismatch", bad_read.stderr)

    def test_onboard_empty_unadopted_and_adopted_targets(self) -> None:
        # 1. Empty directory
        with tempfile.TemporaryDirectory() as empty_dir:
            res_empty = self._run_cli("onboard", "--target", empty_dir, "--json")
            self.assertEqual(res_empty.returncode, 0, res_empty.stderr)
            info_empty = json.loads(res_empty.stdout)
            self.assertEqual(info_empty["total_files"], 0)
            self.assertIn("Path A", info_empty["recommended_adoption_path"])

        # 2. Existing unadopted repo with CSS and an oversized source file
        with tempfile.TemporaryDirectory() as existing_dir:
            p = Path(existing_dir)
            (p / "src").mkdir()
            (p / "src" / "monolith.ts").write_text("\n".join(f"export const x{i} = {i};" for i in range(520)), encoding="utf-8")
            (p / "src" / "app.css").write_text(".btn { color: red; }\n", encoding="utf-8")

            res_exist = self._run_cli("onboard", "--target", existing_dir, "--json")
            self.assertEqual(res_exist.returncode, 0, res_exist.stderr)
            info_exist = json.loads(res_exist.stdout)
            self.assertIn("Path B", info_exist["recommended_adoption_path"])
            self.assertTrue(info_exist["has_ui_or_style_files"])
            self.assertEqual(len(info_exist["oversized_files"]), 1)
            self.assertTrue(
                any(p.endswith("docs/contracts/frontend-and-visual-discipline.md") for p in info_exist["required_reading_before_judgment"]),
                info_exist["required_reading_before_judgment"],
            )

        # 3. Already-adopted repo on an older discipline_version
        with tempfile.TemporaryDirectory() as old_adopted_dir:
            p = Path(old_adopted_dir)
            (p / "docs-policy.toml").write_text('version = 2\ndiscipline_version = "2026.01"\n', encoding="utf-8")
            res_old = self._run_cli("onboard", "--target", old_adopted_dir, "--json")
            self.assertEqual(res_old.returncode, 0, res_old.stderr)
            info_old = json.loads(res_old.stdout)
            self.assertEqual(info_old["target_discipline_version"], "2026.01")
            self.assertIn("Path C", info_old["recommended_adoption_path"])

        # 4. General concern passes prepare cleanly, and onboard honors harness_paths while scanning non-discipline scripts/
        gen = self._run_cli("prepare", "--concern", "general")
        self.assertEqual(gen.returncode, 0, gen.stderr)
        with tempfile.TemporaryDirectory() as custom_dir:
            p = Path(custom_dir)
            (p / "docs-policy.toml").write_text('[layout]\nharness_paths = ["legacy_vendor"]\n', encoding="utf-8")
            (p / "legacy_vendor").mkdir()
            (p / "legacy_vendor" / "big.py").write_text("x = 1\n" * 520, encoding="utf-8")
            (p / "scripts").mkdir()
            (p / "scripts" / "tool_big.py").write_text("y = 1\n" * 520, encoding="utf-8")
            info_c = json.loads(self._run_cli("onboard", "--target", custom_dir, "--json").stdout)
            oversized = {x["path"] for x in info_c["oversized_files"]}
            self.assertIn("scripts/tool_big.py", oversized)
            self.assertNotIn("legacy_vendor/big.py", oversized)

    def test_init_on_existing_codebase_sets_observed_and_strips_internal_anchors(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / "src" / "billing").mkdir(parents=True, exist_ok=True)
            (repo / "src" / "billing" / "calc.py").write_text(
                "# Role: Legacy billing calculator.\ndef calc(x: int) -> int:\n    return x + 1\n",
                encoding="utf-8",
            )
            init_proc = subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "project.py"), "init", "--target", str(repo), "--name", "Existing Billing", "--lang", "en", "--stage", "usable"],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(init_proc.returncode, 0, init_proc.stderr)

            policy_path = repo / "docs-policy.toml"
            policy_txt = policy_path.read_text(encoding="utf-8")
            self.assertIn('stage = "observed"', policy_txt)

            for py_file in (repo / "scripts").rglob("*.py"):
                for ln in py_file.read_text(encoding="utf-8").splitlines():
                    self.assertFalse(ln.lstrip().startswith("# Anchors:"), f"Anchor header leaked into {py_file}: {ln}")

            chk_obs = subprocess.run([sys.executable, "-B", str(repo / "scripts" / "check_docs.py")], cwd=repo, capture_output=True, text=True, check=False)
            self.assertEqual(chk_obs.returncode, 0, chk_obs.stdout + chk_obs.stderr)
            chk_strict = subprocess.run([sys.executable, "-B", str(repo / "scripts" / "check_docs.py"), "--strict"], cwd=repo, capture_output=True, text=True, check=False)
            self.assertNotEqual(chk_strict.returncode, 0)
            self.assertIn("unclaimed_source", chk_strict.stdout)

            policy_path.write_text(policy_txt.replace('stage = "observed"', 'stage = "adopted"'), encoding="utf-8")
            chk_adopted = subprocess.run([sys.executable, "-B", str(repo / "scripts" / "check_docs.py")], cwd=repo, capture_output=True, text=True, check=False)
            self.assertNotEqual(chk_adopted.returncode, 0)
            self.assertIn("unclaimed_source", chk_adopted.stdout)

            # Self-run copied read_rules.py onboard inside adopter repo excludes copied governance tools while counting user scripts
            (repo / "scripts" / "deploy.py").write_text("x = 1\n" * 10, encoding="utf-8")
            self_onboard = subprocess.run(
                [sys.executable, "-B", "scripts/read_rules.py", "onboard", "--target", ".", "--json"],
                cwd=repo, capture_output=True, text=True, check=False,
            )
            self.assertEqual(self_onboard.returncode, 0, self_onboard.stderr)
            self_info = json.loads(self_onboard.stdout)
            self.assertLess(self_info["code_and_style_loc"], 200, f"Copied governance scripts leaked into LOC: {self_info}")


if __name__ == "__main__":
    unittest.main()
