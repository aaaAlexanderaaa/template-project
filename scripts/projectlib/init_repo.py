# Role: Clean repository bootstrap (`project.py init`), cloned-checkout sanitization, and `discipline_version` sync (`--sync`).
# Out of scope: HTTP serving (server.py), TOML write-back mutations (toml_writer.py), or codebase validation.
# Anchors: spec=perspective.server, ADR-002, SRC-014, SRC-020

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tomllib
from pathlib import Path

from .cli_format import fmt_stage
from .import_scanner import SOURCE_EXTS, STYLE_EXTS
from .validator import TEMPLATE_REMOTE_SLUG, _normalize_remote

CODE_EXTS = SOURCE_EXTS | STYLE_EXTS | {".java", ".rb", ".c", ".cpp", ".cs", ".swift", ".kt"}
NON_CODE_DIRS = {".git", "docs", "templates", "tests", "archive", "tmp", ".agents", "node_modules", "__pycache__", ".venv", "venv", "dist", "build"}
COPIED_TOOL_FILES = {"scripts/project.py", "scripts/check_docs.py", "scripts/read_rules.py", "scripts/rule_reading.py"}
DOWNSTREAM_TOOL_HARNESS = (
    "scripts/projectlib",
    "scripts/project.py",
    "scripts/check_docs.py",
    "scripts/read_rules.py",
    "scripts/rule_reading.py",
)
TEMPLATE_INTERNAL_DOMAINS = ("discipline", "graph-engine", "perspective-ui", "reference-app")
TEMPLATE_INTERNAL_TESTS = (
    "test_discipline_transfer_and_consistency.py",
    "test_project_cli_and_server.py",
    "test_read_rules_and_onboard.py",
    "test_reference_exemplar.py",
    "test_ssot_and_check_docs.py",
    "test_web_workbench.py",
    "test_chrome_geometry.py",
)


def _run_git(target: Path, *args: str) -> str:
    try:
        proc = subprocess.run(
            ["git", "--no-optional-locks", *args],
            cwd=target,
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
        return proc.stdout.strip() if proc.returncode == 0 else ""
    except OSError:
        return ""


def _is_origin_template_repo(target: Path, template_root: Path) -> bool:
    url = _run_git(target, "remote", "get-url", "origin")
    return _normalize_remote(url) == TEMPLATE_REMOTE_SLUG if url else False


def _insert_after_section(txt: str, section: str, block: str) -> str | None:
    m = re.search(rf"^\[{re.escape(section)}\][ \t]*(?:#[^\r\n]*)?(?:\r?\n|$)", txt, flags=re.M)
    if not m:
        return None
    hdr = m.group(0) if m.group(0).endswith("\n") else m.group(0) + "\n"
    return txt[: m.start()] + hdr + block + txt[m.end() :]


def _anchor_review_sha_in_policy(txt: str, head_sha: str) -> str:
    cleaned = re.sub(r'^\s*review_anchor_sha\s*=\s*(?:"[^"]*"|\'[^\']*\')\r?\n?', "", txt, flags=re.MULTILINE)
    if not head_sha:
        return cleaned
    return _insert_after_section(cleaned, "collaboration", f'review_anchor_sha = "{head_sha}"\n') or cleaned


def _detect_existing_code(target: Path) -> tuple[list[str], list[str], bool]:
    has_copied_scripts = (target / "scripts" / "projectlib").is_dir()
    src_dirs: list[str] = []
    for entry in sorted(target.iterdir()):
        if not entry.is_dir() or entry.name.startswith(".") or entry.name in NON_CODE_DIRS:
            continue
        for fp in entry.rglob("*"):
            if not fp.is_file() or fp.suffix.lower() not in CODE_EXTS:
                continue
            rel = fp.relative_to(target).as_posix()
            if has_copied_scripts and (rel in COPIED_TOOL_FILES or rel.startswith("scripts/projectlib/")):
                continue
            src_dirs.append(entry.name)
            break
    root_files = sorted(
        p.name for p in target.iterdir() if p.is_file() and p.suffix.lower() in CODE_EXTS
    )
    return src_dirs, root_files, bool(src_dirs or root_files)


def _find_toml_array_end(txt: str, open_idx: int) -> tuple[int, int, str | None] | None:
    i, n, depth, last_sig_ch, last_token_end = open_idx, len(txt), 0, None, open_idx
    while i < n:
        ch = txt[i]
        if ch == "#":
            nl = txt.find("\n", i)
            i = n if nl < 0 else nl + 1
            continue
        if ch in ('"', "'"):
            delim = txt[i : i + 3] if txt[i : i + 3] in ('"""', "'''") else ch
            i += len(delim)
            while i < n:
                if delim[0] == '"' and txt[i] == "\\":
                    i += 2
                    continue
                if txt.startswith(delim, i):
                    i += len(delim)
                    break
                i += 1
            if depth == 0:
                last_sig_ch, last_token_end = delim[-1], i
            continue
        if ch in " \t\r\n":
            i += 1
            continue
        if ch == "[":
            depth += 1
        elif ch == "]":
            if depth == 0:
                return i, last_token_end, last_sig_ch
            depth -= 1
        if depth == 0:
            last_sig_ch, last_token_end = ch, i + 1
        i += 1
    return None


def _ensure_harness_paths_in_toml(txt: str) -> str:
    m = re.search(r"^[ \t]*harness_paths[ \t]*=[ \t]*\[", txt, flags=re.M)
    if not m or (span := _find_toml_array_end(txt, m.end())) is None:
        all_hps = ("tests", "templates", "archive", "docs", ".agents", "tmp", *DOWNSTREAM_TOOL_HARNESS)
        hp_block = "harness_paths = [\n" + "".join(f'  "{hp}",\n' for hp in all_hps) + "]\n"
        updated = _insert_after_section(txt, "layout", hp_block)
        if updated is not None:
            return updated
        sep = "" if (not txt or txt.endswith("\n")) else "\n"
        return txt + f"{sep}\n[layout]\n{hp_block}"
    close_idx, last_token_end, last_sig_ch = span
    open_idx = m.end()
    body = txt[open_idx:close_idx]
    missing = [hp for hp in DOWNSTREAM_TOOL_HARNESS if f'"{hp}"' not in body and f"'{hp}'" not in body]
    if not missing:
        return txt
    if last_sig_ch is not None and last_sig_ch != ",":
        rel_cut = last_token_end - open_idx
        body = body[:rel_cut] + "," + body[rel_cut:]
    body_trimmed = body.rstrip(" \t")
    close_indent = body[len(body_trimmed) :]
    if not body_trimmed.endswith("\n"):
        body_trimmed += "\n"
    ins = "".join(f'  "{hp}",\n' for hp in missing)
    return txt[:open_idx] + body_trimmed + ins + close_indent + txt[close_idx:]


def _sanitize_copied_checkout(target: Path) -> None:
    specs_dir = target / "docs" / "specs"
    if specs_dir.is_dir():
        for dom in TEMPLATE_INTERNAL_DOMAINS:
            if (specs_dir / dom).is_dir():
                shutil.rmtree(specs_dir / dom)
        if not any(specs_dir.iterdir()):
            specs_dir.rmdir()
    dec_dir = target / "docs" / "decisions"
    if dec_dir.is_dir():
        for adr in dec_dir.glob("ADR-00[1-5]-*.md"):
            adr.unlink(missing_ok=True)
        if not any(dec_dir.iterdir()):
            dec_dir.rmdir()
    for folder in ("docs/archive", "docs/evaluations", "archive/legacy-v1"):
        p = target / folder
        if p.is_dir():
            shutil.rmtree(p)
    arch_readme = target / "archive" / "README.md"
    if arch_readme.is_file() and "legacy-v1" in arch_readme.read_text(encoding="utf-8", errors="ignore"):
        arch_readme.unlink(missing_ok=True)
    if (target / "archive").is_dir() and not any((target / "archive").iterdir()):
        (target / "archive").rmdir()
    design_dir = target / "docs" / "design"
    if design_dir.is_dir():
        for df in ("perspective-web.md", "frontend-design-options.html"):
            (design_dir / df).unlink(missing_ok=True)
        des_readme = design_dir / "README.md"
        if des_readme.is_file() and "perspective-web.md" in des_readme.read_text(encoding="utf-8", errors="ignore"):
            des_readme.unlink(missing_ok=True)
        if not any(design_dir.iterdir()):
            design_dir.rmdir()
    ex_app = target / "examples" / "reference-app"
    if any((ex_app / p).is_file() for p in ("features/checkout/service.py", "domain/order_ledger.py", "src/checkout.py")):
        shutil.rmtree(ex_app)
        if (target / "examples").is_dir() and not any((target / "examples").iterdir()):
            (target / "examples").rmdir()
    tests_dir = target / "tests"
    if tests_dir.is_dir():
        for tf in TEMPLATE_INTERNAL_TESTS:
            (tests_dir / tf).unlink(missing_ok=True)
        t_readme = tests_dir / "README.md"
        if t_readme.is_file() and "test_reference_exemplar.py" in t_readme.read_text(encoding="utf-8", errors="ignore"):
            t_readme.unlink(missing_ok=True)
        if not any(tests_dir.iterdir()):
            tests_dir.rmdir()
    src_readme = target / "src" / "README.md"
    if src_readme.is_file() and "template-project" in src_readme.read_text(encoding="utf-8", errors="ignore"):
        src_readme.unlink(missing_ok=True)
        if (target / "src").is_dir() and not any((target / "src").iterdir()):
            (target / "src").rmdir()
    for rel in ("README_CN.md", "tmp/project-state.json"):
        (target / rel).unlink(missing_ok=True)


def _strip_internal_anchors(text: str, suffix: str) -> str:
    if suffix == ".css":
        return re.sub(r"\n\s*\*\s*Anchors:.*?\*/", " */", text)
    if suffix == ".html":
        return re.sub(r"^\s*<!--\s*Anchors:.*?-->\r?\n?", "", text, flags=re.MULTILINE)
    return re.sub(r"^\s*(?:#|//)\s*Anchors:.*\r?\n?", "", text, flags=re.MULTILINE)


def run_init_command(
    template_root: Path,
    target: Path,
    name: str,
    stage: str,
    lang: str = "en",
    sync: bool = False,
) -> int:
    target = target.resolve()
    policy_file = target / "docs-policy.toml"
    is_template_checkout = _is_origin_template_repo(target, template_root)
    existing_cfg: dict = {}
    if policy_file.is_file():
        try:
            existing_cfg = tomllib.loads(policy_file.read_text(encoding="utf-8"))
        except (OSError, tomllib.TOMLDecodeError):
            existing_cfg = {}
        if existing_cfg.get("project", {}).get("identity") == "template" and is_template_checkout:
            print(
                f"Refusing to overwrite template repository at {target}. Pass `--target /path/to/product-repo`.",
                file=sys.stderr,
            )
            return 1

    target.mkdir(parents=True, exist_ok=True)
    if sync and policy_file.is_file():
        proj_sec = existing_cfg.get("project", {})
        lang = str(proj_sec.get("language", lang)).strip().lower() or lang
        stage = str(proj_sec.get("default_stage", stage)).strip() or stage

    agents_dst = target / "AGENTS.md"
    replace_template_agents = (
        agents_dst.is_file()
        and TEMPLATE_REMOTE_SLUG in agents_dst.read_text(encoding="utf-8", errors="ignore").lower()
    )
    is_copied_checkout = (not is_template_checkout) and (
        existing_cfg.get("project", {}).get("identity") == "template" or replace_template_agents
    )
    if is_copied_checkout and not sync:
        _sanitize_copied_checkout(target)

    tpl_dir = template_root / "templates"
    existing_src_dirs, root_files, has_existing_code = _detect_existing_code(target)
    if existing_src_dirs and root_files:
        det_roots = [*existing_src_dirs, *root_files]
    elif existing_src_dirs:
        det_roots = existing_src_dirs
    elif root_files:
        det_roots = root_files
    else:
        det_roots = ["src"]

    tpl_policy = tomllib.loads((template_root / "docs-policy.toml").read_text(encoding="utf-8"))
    tpl_version = str(tpl_policy.get("discipline_version", "2026.11"))
    head_sha = _run_git(target, "rev-parse", "--short", "HEAD") if not sync else ""

    if policy_file.is_file():
        txt = policy_file.read_text(encoding="utf-8")
        txt = re.sub(r'identity\s*=\s*"template"', 'identity = "product"', txt)
        if not sync:
            txt = re.sub(r'default_stage\s*=\s*"[^"]+"', f'default_stage = "{stage}"', txt)
            txt = _anchor_review_sha_in_policy(txt, head_sha)
        else:
            if re.search(r"^\s*discipline_version\s*=", txt, flags=re.MULTILINE):
                txt = re.sub(r'^\s*discipline_version\s*=\s*"[^"]*"', f'discipline_version = "{tpl_version}"', txt, flags=re.MULTILINE)
            elif re.search(r"^\s*version\s*=", txt, flags=re.MULTILINE):
                txt = re.sub(r"(^\s*version\s*=\s*[^\r\n]+\r?\n)", rf'\1discipline_version = "{tpl_version}"\n', txt, count=1, flags=re.MULTILINE)
            else:
                txt = f'discipline_version = "{tpl_version}"\n' + txt
        if (is_copied_checkout and not sync) or (re.search(r'source_roots\s*=\s*\[[^\]]*"examples"', txt) and not (target / "examples").is_dir()):
            txt = re.sub(r"source_roots\s*=\s*\[[^\]]*\]", f"source_roots = {json.dumps(det_roots)}", txt, flags=re.S)
        if not sync:
            if re.search(r"^\s*language\s*=", txt, flags=re.MULTILINE):
                txt = re.sub(r'^\s*language\s*=\s*"[^"]+"', f'language = "{lang}"', txt, flags=re.MULTILINE)
            else:
                txt = _insert_after_section(txt, "project", f'language = "{lang}"\n') or txt
        if has_existing_code and not (target / "docs" / "specs").exists():
            txt = re.sub(r'(\[adoption\][^\[]*?^\s*stage\s*=\s*)"adopted"', r'\1"observed"', txt, flags=re.MULTILINE | re.DOTALL)
        policy_file.write_text(_ensure_harness_paths_in_toml(txt), encoding="utf-8")
    else:
        base_policy = (template_root / "docs-policy.toml").read_text(encoding="utf-8")
        base_policy = base_policy.replace('identity = "template"', f'identity = "product"\nlanguage = "{lang}"')
        base_policy = base_policy.replace('default_stage = "stable"', f'default_stage = "{stage}"')
        base_policy = re.sub(r"source_roots\s*=\s*\[[^\]]*\]", f"source_roots = {json.dumps(det_roots)}", base_policy, flags=re.S)
        base_policy = _anchor_review_sha_in_policy(base_policy, head_sha)
        if has_existing_code:
            base_policy = re.sub(r'(\[adoption\][^\[]*?^\s*stage\s*=\s*)"adopted"', r'\1"observed"', base_policy, flags=re.MULTILINE | re.DOTALL)
        policy_file.write_text(_ensure_harness_paths_in_toml(base_policy), encoding="utf-8")

    overwrite_starters = is_copied_checkout and not sync
    copy_map = (
        ("AGENTS.zh.md" if lang == "zh" else "AGENTS.md", "AGENTS.md"),
        ("docs-readme.zh.md" if lang == "zh" else "docs-readme.md", "docs/README.md"),
        ("sources.toml", "docs/sources.toml"),
        ("work.toml", "docs/work.toml"),
    )
    for tpl_name, dst_rel in copy_map:
        dst = target / dst_rel
        src_tpl = tpl_dir / tpl_name
        if not src_tpl.is_file() and tpl_name.endswith(".zh.md"):
            src_tpl = tpl_dir / tpl_name.replace(".zh.md", ".md")
        should_write = (not dst.is_file()) or overwrite_starters or (dst_rel == "AGENTS.md" and replace_template_agents)
        if should_write and src_tpl.is_file():
            dst.parent.mkdir(parents=True, exist_ok=True)
            content = src_tpl.read_text(encoding="utf-8")
            if lang == "zh" and dst_rel == "docs/sources.toml":
                content = content.replace('context = "Initial project goal"', 'context = "初始项目目标"')
                content = content.replace("Replace with the owner's exact verbatim request.", "请替换为项目负责人的真实需求原话。")
            elif dst_rel == "docs/work.toml":
                if lang == "zh":
                    content = content.replace('name = "Initial Usable Slice"', 'name = "首个可用版本"')
                    content = content.replace('title = "Deliver core module vertical slice"', 'title = "完成核心模块端到端功能"')
                if has_existing_code:
                    content = content.replace('domain = "example"', 'domain = "codebase"')
                    content = content.replace('specs = ["example.module"]', 'specs = []')
            dst.write_text(content, encoding="utf-8")

    one_liner = f"{name} 系统说明。" if lang == "zh" else f"{name} application."
    readme_dst = target / "README.md"
    if not sync and ((not readme_dst.is_file() and not has_existing_code) or overwrite_starters):
        readme_body = (
            f"# {name}\n\n{one_liner}\n\n- 架构说明：[ARCHITECTURE.md](ARCHITECTURE.md)\n- 文档索引：[docs/README.md](docs/README.md)\n"
            if lang == "zh"
            else f"# {name}\n\n{one_liner}\n\n- Architecture: [ARCHITECTURE.md](ARCHITECTURE.md)\n- Docs index: [docs/README.md](docs/README.md)\n"
        )
        readme_dst.write_text(readme_body, encoding="utf-8")

    arch_target = target / "ARCHITECTURE.md"
    if not sync and (not arch_target.is_file() or overwrite_starters):
        arch_tpl_name = "ARCHITECTURE.zh.md" if lang == "zh" and (tpl_dir / "ARCHITECTURE.zh.md").is_file() else "ARCHITECTURE.md"
        arch_tpl = (
            (tpl_dir / arch_tpl_name)
            .read_text(encoding="utf-8")
            .replace("{{Project Name}}", name)
            .replace("{{项目名称}}", name)
            .replace("{{One-sentence plain description of who uses this system and what core outcome it delivers}}", one_liner)
            .replace("{{用一句话说明系统服务谁、交付什么核心结果}}", one_liner)
            .replace("stage: prototype", f"stage: {stage}")
        )
        arch_target.write_text(arch_tpl, encoding="utf-8")

    spec_dst = target / "docs" / "specs" / "example" / "module.md"
    if not sync and not has_existing_code and not spec_dst.is_file() and not (target / "docs" / "specs").exists():
        spec_dst.parent.mkdir(parents=True, exist_ok=True)
        mod_tpl_name = "module-spec.zh.md" if lang == "zh" and (tpl_dir / "module-spec.zh.md").is_file() else "module-spec.md"
        mod_summary = "核心示例模块起步说明。" if lang == "zh" else "Core module starter placeholder."
        mod_promise = "实现具体功能时替换为真实对外承诺。" if lang == "zh" else "Replace with the real promise once built."
        mod_title = "示例模块" if lang == "zh" else "Example Module"
        mod_tpl = (
            (tpl_dir / mod_tpl_name)
            .read_text(encoding="utf-8")
            .replace("{{One sentence stating what this module does}}", mod_summary)
            .replace("{{用一句话说明本模块做什么}}", mod_summary)
            .replace("{{Observable guarantee to users or callers}}", mod_promise)
            .replace("{{对用户或调用方可验证的结果承诺}}", mod_promise)
            .replace("{{Module Title}}", mod_title)
            .replace("{{模块名称}}", mod_title)
        )
        spec_dst.write_text(mod_tpl, encoding="utf-8")

    src_dir = target / "src"
    if not sync and not has_existing_code and (not src_dir.exists() or not any(src_dir.iterdir())):
        ex_init = src_dir / "example" / "__init__.py"
        ex_init.parent.mkdir(parents=True, exist_ok=True)
        ex_init.write_text(
            "# Role: Starter example package entry point matching docs/specs/example/module.md.\n"
            "# Out of scope: Business persistence or CLI parsing until replaced by real product code.\n"
            '"""Example starter package."""\n',
            encoding="utf-8",
        )

    tests_dir = target / "tests"
    if not sync and not has_existing_code and not any(tests_dir.glob("test_*.py")):
        smoke_test = tests_dir / "test_smoke.py"
        smoke_test.parent.mkdir(parents=True, exist_ok=True)
        smoke_test.write_text(
            "# Role: Starter end-to-end smoke test verifying initialized repository layout and example package.\n"
            "from __future__ import annotations\n\n"
            "import unittest\n"
            "from pathlib import Path\n\n"
            "ROOT = Path(__file__).resolve().parents[1]\n\n\n"
            "class StarterRepoSmokeTests(unittest.TestCase):\n"
            "    def test_starter_files_present(self) -> None:\n"
            "        for rel in (\n"
            '            "AGENTS.md",\n'
            '            "ARCHITECTURE.md",\n'
            '            "docs-policy.toml",\n'
            '            "docs/README.md",\n'
            '            "docs/sources.toml",\n'
            '            "docs/work.toml",\n'
            '            "src/example/__init__.py",\n'
            "        ):\n"
            '            self.assertTrue((ROOT / rel).is_file(), f"missing {rel}")\n\n\n'
            'if __name__ == "__main__":\n'
            "    unittest.main()\n",
            encoding="utf-8",
        )

    same_tree = target == template_root.resolve()
    if not same_tree:
        scripts_dst = target / "scripts"
        scripts_dst.mkdir(parents=True, exist_ok=True)
        for sname in ("check_docs.py", "project.py", "read_rules.py", "rule_reading.py"):
            src_f, dst_f = template_root / "scripts" / sname, scripts_dst / sname
            if src_f.is_file() and (sync or overwrite_starters or not dst_f.exists()):
                shutil.copy2(src_f, dst_f)
                dst_f.write_text(_strip_internal_anchors(dst_f.read_text(encoding="utf-8"), ".py"), encoding="utf-8")
        projlib_dst = scripts_dst / "projectlib"
        if (sync or overwrite_starters) and projlib_dst.exists():
            shutil.rmtree(projlib_dst)
        if not projlib_dst.exists():
            shutil.copytree(
                template_root / "scripts" / "projectlib",
                projlib_dst,
                ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store"),
            )
            for copied in projlib_dst.rglob("*"):
                if copied.is_file() and copied.suffix in (".py", ".js", ".css", ".html"):
                    copied.write_text(_strip_internal_anchors(copied.read_text(encoding="utf-8"), copied.suffix), encoding="utf-8")
        for folder in ("contracts", "guides"):
            src_dir, dst_dir = template_root / "docs" / folder, target / "docs" / folder
            if src_dir.is_dir():
                dst_dir.mkdir(parents=True, exist_ok=True)
                for fp in src_dir.glob("*.md"):
                    if sync or overwrite_starters or not (dst_dir / fp.name).exists():
                        shutil.copy2(fp, dst_dir / fp.name)
        for skill_name in ("grill", "onboard-discipline"):
            sk_src, sk_dst = template_root / ".agents" / "skills" / skill_name / "SKILL.md", target / ".agents" / "skills" / skill_name / "SKILL.md"
            if sk_src.is_file() and (sync or overwrite_starters or not sk_dst.exists()):
                sk_dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(sk_src, sk_dst)
    elif overwrite_starters:
        for script_file in (target / "scripts").rglob("*"):
            if script_file.is_file() and script_file.suffix in (".py", ".js", ".css", ".html"):
                script_file.write_text(_strip_internal_anchors(script_file.read_text(encoding="utf-8"), script_file.suffix), encoding="utf-8")

    for stem in ("adr", "domain-readme", "module-spec", "surface-spec", "charter", "adoption-assessment", "independent-review"):
        src_name = f"{stem}.zh.md" if lang == "zh" and (tpl_dir / f"{stem}.zh.md").is_file() else f"{stem}.md"
        t_src, t_dst = tpl_dir / src_name, target / "templates" / f"{stem}.md"
        if t_src.is_file() and (sync or overwrite_starters or not t_dst.exists()):
            t_dst.parent.mkdir(parents=True, exist_ok=True)
            if t_src.resolve() != t_dst.resolve():
                shutil.copy2(t_src, t_dst)
    for raw_tpl in ("architecture-rules.toml", "ci/docs-check.example.yml"):
        t_src, t_dst = tpl_dir / raw_tpl, target / "templates" / raw_tpl
        if t_src.is_file() and (sync or overwrite_starters or not t_dst.exists()):
            t_dst.parent.mkdir(parents=True, exist_ok=True)
            if t_src.resolve() != t_dst.resolve():
                shutil.copy2(t_src, t_dst)
    arch_rules_dst = target / "architecture-rules.toml"
    if (tpl_dir / "architecture-rules.toml").is_file() and (overwrite_starters or not arch_rules_dst.exists()):
        shutil.copy2(tpl_dir / "architecture-rules.toml", arch_rules_dst)
    if same_tree and overwrite_starters and (target / "templates").is_dir():
        for extra_tpl in ("AGENTS.md", "ARCHITECTURE.md", "docs-readme.md", "sources.toml", "work.toml", "README.md"):
            (target / "templates" / extra_tpl).unlink(missing_ok=True)
        for zh_tpl in (target / "templates").glob("*.zh.md"):
            zh_tpl.unlink(missing_ok=True)

    if sync:
        if lang == "zh":
            print(f"已同步工程纪律：{target}（版本={tpl_version}，阶段={fmt_stage(stage, 'zh')}）。")
        else:
            print(f"Synced engineering discipline in {target} (discipline_version={tpl_version}, {fmt_stage(stage, lang)}).")
    elif lang == "zh":
        print(f"已初始化产品仓库：{target}（名称={name}，阶段={fmt_stage(stage, 'zh')}）。")
    else:
        print(f"Initialized product repository in {target} (name={name}, {fmt_stage(stage, lang)}).")
    return 0
