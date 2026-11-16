# Role: Plain-language, project-language, placeholder, and stable-spec structure checks separated from validator core.
# Out of scope: Ownership globs, AST import scanning, or file-size budget enforcement (kept in validator.py).
# Anchors: spec=graph.validator, ADR-002, ADR-003, SRC-010, SRC-013, SRC-018, SRC-019

from __future__ import annotations

import os
import re
import tomllib
from pathlib import Path
from typing import Any

from .model import ProjectGraph

DISCLAIMER_CHAINS = (
    "does not by itself",
    "alone does not",
    "alone is not",
    "is not proof",
    "cannot establish",
    "proves no",
    "is not a substitute",
    "不能证明",
    "并不等于",
    "不等于",
    "不能替代",
)
BANNED_JARGON = (
    "context capsule",
    "上下文胶囊",
    "3-act",
    "scarce warm-terracotta",
    "技术内生模块",
    "技术内生约束",
    "双层溯源子图",
    "三幕剧",
)
PLACEHOLDER_RE = re.compile(r"\{\{[^{}\n]+\}\}")
CJK_RE = re.compile(r"[\u4e00-\u9fff]")


def scrub_examples(line: str) -> str:
    """Strip inline quoted/code examples before checking plain-language phrase patterns."""
    cleaned = re.sub(r"`[^`]*`|\"[^\"]*\"|'[^']*'|「[^」]*」|（[^）]*）", "", line)
    return cleaned.lower()


def collect_live_markdown_files(root: Path) -> list[Path]:
    """Collect active markdown files across entrypoints, guides, skills, specs, and templates (excluding archive)."""
    results: list[Path] = []
    for top in (
        "AGENTS.md",
        "ARCHITECTURE.md",
        "README.md",
        "README_CN.md",
        "CONTRIBUTING.md",
        "src/README.md",
        "tests/README.md",
        "archive/README.md",
    ):
        tp = root / top
        if tp.is_file():
            results.append(tp)
    ex_dir = root / "examples"
    if ex_dir.is_dir():
        for ex_readme in sorted(ex_dir.glob("*/README.md")):
            if ex_readme.is_file():
                results.append(ex_readme)
    for folder in ("docs", "templates", ".agents"):
        fp = root / folder
        if fp.is_dir():
            for dirpath, dirnames, filenames in os.walk(fp):
                dirnames[:] = [d for d in sorted(dirnames) if d not in {".git", "archive"}]
                for fn in sorted(filenames):
                    if fn.endswith(".md"):
                        results.append(Path(dirpath) / fn)
    return results


def _check_work_toml_language(root: Path, emit: Any) -> None:
    candidates: list[Path] = [root / "docs" / "work.toml"]
    for sub in ("specs", "domains"):
        sub_dir = root / "docs" / sub
        if sub_dir.is_dir():
            candidates.extend(sorted(sub_dir.glob("*/work.toml")))
    for work_path in candidates:
        if not work_path.is_file():
            continue
        rel_work = work_path.relative_to(root).as_posix()
        try:
            data = tomllib.loads(work_path.read_text(encoding="utf-8"))
        except (OSError, tomllib.TOMLDecodeError):
            continue
        for ms in data.get("milestones", []):
            name = str(ms.get("name", "")).strip()
            if name and not CJK_RE.search(name):
                emit(
                    "project_language_mismatch",
                    "startup_disclaimers",
                    rel_work,
                    f'docs-policy.toml sets language = "zh", so milestone `{ms.get("id", "")}` name must be in plain Chinese.',
                    1,
                )
        for task in data.get("tasks", []):
            title = str(task.get("title", "")).strip()
            if title and not CJK_RE.search(title):
                emit(
                    "project_language_mismatch",
                    "startup_disclaimers",
                    rel_work,
                    f'docs-policy.toml sets language = "zh", so task `{task.get("id", "")}` title must be in plain Chinese.',
                    1,
                )


def check_plain_language(
    root: Path,
    md_files: list[Path],
    graph_files: tuple[Any, ...],
    emit: Any,
    policy: dict[str, Any] | None = None,
) -> None:
    """Validate disclaimer chains, banned jargon, unresolved placeholders, and zh language compliance."""
    check_files: list[Path] = list(md_files)
    seen_paths: set[Path] = {p.resolve() for p in md_files}
    ui_exts = {".html", ".js", ".jsx", ".ts", ".tsx", ".vue", ".svelte"}
    for fs in graph_files:
        fp = (root / fs.path).resolve()
        if fp.suffix.lower() in ui_exts and fp.is_file() and fp not in seen_paths:
            seen_paths.add(fp)
            check_files.append(fp)

    docs_dir = root / "docs"
    if docs_dir.is_dir():
        for html_fp in sorted(docs_dir.rglob("*.html")):
            rel_html = html_fp.relative_to(root).as_posix()
            if rel_html.startswith("docs/archive/"):
                continue
            resolved_html = html_fp.resolve()
            if resolved_html not in seen_paths:
                seen_paths.add(resolved_html)
                check_files.append(resolved_html)

    web_dir = root / "scripts" / "projectlib" / "web"
    if web_dir.is_dir():
        for dirpath, _, filenames in os.walk(web_dir):
            for fn in sorted(filenames):
                if fn.endswith((".html", ".js")):
                    fp = (Path(dirpath) / fn).resolve()
                    if fp not in seen_paths:
                        seen_paths.add(fp)
                        check_files.append(fp)

    proj_cfg = (policy or {}).get("project", {})
    identity = str(proj_cfg.get("identity", "product")).strip()
    proj_lang = str(proj_cfg.get("language", "")).strip().lower()

    if identity != "template" and proj_lang == "zh":
        _check_work_toml_language(root, emit)

    for fp in check_files:
        rel = fp.relative_to(root).as_posix()
        is_template = rel.startswith("templates/")
        is_code = fp.suffix.lower() in ui_exts
        raw_text = fp.read_text(encoding="utf-8")
        if (
            identity != "template"
            and proj_lang == "zh"
            and not is_code
            and not is_template
            and (rel in {"AGENTS.md", "ARCHITECTURE.md", "docs/README.md"} or rel.startswith(("docs/specs/", "docs/design/", "docs/decisions/")))
        ):
            prose = re.sub(r"\A---\s*\n.*?\n---\s*(?:\n|\Z)", "", raw_text, flags=re.S)
            prose = re.sub(r"```[\s\S]*?```|~~~[\s\S]*?~~~", "", prose).strip()
            if prose and len(CJK_RE.findall(prose)) < 6:
                emit(
                    "project_language_mismatch",
                    "startup_disclaimers",
                    rel,
                    'docs-policy.toml sets language = "zh", so project documentation must contain substantial plain Chinese prose.',
                    1,
                )
        in_fence = False
        for ln, raw_line in enumerate(raw_text.splitlines(), 1):
            st = raw_line.strip()
            if not is_code and st.startswith(("```", "~~~")):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            scrubbed = raw_line.lower() if is_code else scrub_examples(raw_line)
            for phrase in DISCLAIMER_CHAINS:
                if phrase in scrubbed:
                    emit("startup_disclaimer", "startup_disclaimers", rel, f"Uses defensive disclaimer phrase `{phrase}`; state scope directly.", ln)
            for term in BANNED_JARGON:
                if term in scrubbed:
                    emit("plain_language_jargon", "startup_disclaimers", rel, f"Uses coined buzzword `{term}`; replace with plain ordinary wording.", ln)
            if not is_template and not is_code and PLACEHOLDER_RE.search(re.sub(r"`[^`]*`", "", raw_line)):
                emit("unresolved_placeholder", "broken_links_and_ids", rel, "Unresolved `{{...}}` template placeholder outside `templates/`.", ln)


def check_spec_structure(graph: ProjectGraph, emit: Any) -> None:
    """Enforce baseline structural depth on usable/stable ARCHITECTURE.md and stable domain/module specs."""
    if graph.is_day_zero_synthetic:
        return
    root = Path(graph.root_dir)
    if (root / "ARCHITECTURE.md").is_file() and graph.default_stage in ("usable", "stable") and not graph.system_mermaid:
        emit(
            "incomplete_spec_structure",
            "broken_links_and_ids",
            "ARCHITECTURE.md",
            "Root `ARCHITECTURE.md` at `usable`/`stable` stage should include at least one Mermaid system diagram.",
            1,
            default_sev="advisory",
        )
    for dom in graph.domains.values():
        if dom.stage != "stable" or dom.doc_path == "ARCHITECTURE.md":
            continue
        if not dom.mermaid_blocks:
            emit(
                "incomplete_spec_structure",
                "broken_links_and_ids",
                dom.doc_path,
                f"Stable domain spec `{dom.id}` should include at least one Mermaid diagram.",
                1,
                default_sev="advisory",
            )
        if len(re.findall(r"(?m)^##\s+\S", dom.body_markdown)) < 2:
            emit(
                "incomplete_spec_structure",
                "broken_links_and_ids",
                dom.doc_path,
                f"Stable domain spec `{dom.id}` should document responsibilities, boundaries, and checks across structured `##` sections.",
                1,
                default_sev="advisory",
            )
    for mod in graph.modules.values():
        if mod.stage != "stable":
            continue
        if len(re.findall(r"(?m)^##\s+\S", mod.body_markdown)) < 2:
            emit(
                "incomplete_spec_structure",
                "broken_links_and_ids",
                mod.doc_path,
                f"Stable module spec `{mod.id}` should document runtime logic, boundaries, invariants, and checks across structured `##` sections.",
                1,
                default_sev="advisory",
            )
