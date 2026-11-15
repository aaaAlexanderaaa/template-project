# Role: Indexes all active repository documents and explains directory layout for CLI and web newcomers.
# Out of scope: Mutating files, running Git commands, or static import boundary validation.
# Anchors: spec=graph.indexer, ADR-002, SRC-007, SRC-010

from __future__ import annotations

import html
import os
import re
from pathlib import Path

from .frontmatter import extract_markdown_structure, parse_frontmatter
from .git_telemetry import match_path_to_module
from .model import DirectoryEntry, ModuleSpec, RepoDoc

IGNORE_WALK = {".git", "__pycache__", ".pytest_cache", "node_modules", ".venv", "venv", "dist", "build", "tmp"}
TEXT_DOC_EXTS = {".md", ".toml", ".yml", ".yaml", ".html"}

# Generic directory descriptions for common discipline layouts; domain mapping is inferred dynamically.
KNOWN_DIRS: tuple[tuple[str, str, str, str, str], ...] = (
    (
        "(root)",
        "根目录入口与配置",
        "Root Entry & Config",
        "放置 AI 与人类协作者入口约定（AGENTS.md）、系统架构总览（ARCHITECTURE.md）、规则开关与文件上限配置（docs-policy.toml）。",
        "Entry agreement (AGENTS.md), system overview (ARCHITECTURE.md), and rule/budget config (docs-policy.toml).",
    ),
    (
        "docs/contracts",
        "工程规范契约",
        "Engineering Contracts",
        "五份核心工程契约：团队分工与需求留痕、架构与 CSS 分层、按阶段匹配的测试策略、界面呈现规范、外部项目接入方式。",
        "Five core normative contracts covering governance, architecture and CSS modularity, stage-matched verification, UI clarity, and repo onboarding.",
    ),
    (
        "docs/guides",
        "操作指南",
        "Operational Guides",
        "日常实操手册：新旧项目接入步骤、设计质询与开放闭环评审指南（Grill）、一手资料查证与工具兜底做法。",
        "Step-by-step playbooks for onboarding, design grill, open closed-loop review, and primary-source research fallbacks.",
    ),
    (
        ".agents/skills",
        "可调用 Agent 技能",
        "Agent Skills",
        "按需触发的技能说明书，告诉 AI 何时以及如何执行项目接入评估、设计质询或独立评审。",
        "On-demand skill instructions defining when and how an AI agent runs onboarding inventory, design grill, or independent review.",
    ),
    (
        "templates",
        "下游项目起步模板",
        "Starter Templates",
        "新项目初始化或老项目接入时复制使用的最小骨架（含下游 AGENTS.md、五要素架构、规格、评审单与台账模板）。",
        "Minimal starter files copied into new or adopting repos (downstream AGENTS.md, five-part architecture, specs, review records, ledgers).",
    ),
    (
        "docs/specs",
        "业务域与模块设计规格",
        "Domain & Module Specs",
        "按业务域分目录存放的单一真源规格：每个模块明确声明功能承诺、管辖代码路径与允许依赖的下游模块。",
        "Single-source specs organized by domain declaring module promises, owned source paths, and allowed dependencies.",
    ),
    (
        "docs/design",
        "前端界面设计规格",
        "UI Surface Specs",
        "说明界面服务谁、负责人设计批准状态、主次信息如何组织，以及 CSS 分层与交互状态约定。",
        "Design specs defining target readers, owner design approval status, visual hierarchy, CSS layering, and interaction states.",
    ),
    (
        "docs/decisions",
        "跨模块架构决策 (ADR)",
        "Architecture Decisions",
        "记录推翻旧方案或跨模块权衡的原因、影响范围与被替代关系。",
        "Cross-module trade-offs and direction changes with links to upstream requests and superseded ADRs.",
    ),
    (
        "docs",
        "文档索引、原话与工作台账",
        "Docs Index, Quotes & Work Queue",
        "文档地图与平实语言规范（README.md）、一字不改的用户原话（sources.toml）、路线图与任务队列（work.toml）及历史归档。",
        "Single-source map and plain-language rule (README.md), verbatim quotes (sources.toml), roadmap/tasks (work.toml), and archive/.",
    ),
    (
        "scripts",
        "检查与辅助命令行脚本",
        "Checker & Helper Scripts",
        "纯 Python 3.11+ 标准库编写的规则检查器（check_docs.py）、项目命令行（project.py）、规则读取器与本地预览服务。",
        "Zero-dependency Python 3.11+ helper scripts powering check_docs.py, read_rules.py, project.py CLI, and local overview server.",
    ),
    (
        "examples/reference-app",
        "参考代码示例（非主系统）",
        "Reference Code Example",
        "可运行的小示例，用来演示分层边界、单一真源状态与 CSS Token 用法。",
        "Compact runnable example demonstrating layered import boundaries, single-owner state, and CSS tokens.",
    ),
    (
        "tests",
        "自动化测试套件",
        "Automated Tests",
        "验证工程规则、文档图谱、边界拦截、平实语言、命令行与下游迁移一致性的端到端测试。",
        "End-to-end unittest suite covering discipline rules, single-source graph checks, import boundaries, plain language, CLI, and downstream transfer.",
    ),
    (
        "src",
        "产品源代码目录",
        "Product Source Tree",
        "按能力划分子目录存放产品实现代码，每个源码文件声明顶行角色注释并归属单个模块规范。",
        "Product implementation packages organized by capability, with top-of-file role headers and single-module spec ownership.",
    ),
    (
        "docs/evaluations",
        "行为规则实测记录",
        "Behavioral Evaluation Records",
        "记录新鲜 AI 会话在真实初始化仓库中的实际执行与规范遵守结果（由 check_docs.py 持续校验）。",
        "Empirical records of fresh AI coding and review sessions running on initialized repositories (validated live by check_docs.py).",
    ),
    (
        "archive/legacy-v1",
        "已淘汰的 v1 历史归档",
        "Archived Legacy v1 Docs",
        "保留早期 2026.07–10 版本的旧模板与迁移证据（只作历史备查，当前规则不再生效）。",
        "Historical 2026.07-10 v1 templates and evidence preserved read-only for reference; superseded by 2026.11.",
    ),
)


_CAT_ORDER = {
    "entry": 0,
    "contract": 1,
    "guide": 2,
    "spec": 3,
    "design": 4,
    "decision": 5,
    "skill": 6,
    "template": 7,
    "config": 8,
}


def _classify_doc(rel: str) -> str:
    if rel in ("README.md", "README_CN.md", "AGENTS.md", "ARCHITECTURE.md", "CONTRIBUTING.md", "docs/README.md"):
        return "entry"
    if rel.startswith("docs/contracts/"):
        return "contract"
    if rel.startswith(("docs/guides/", "docs/evaluations/")) or rel.endswith("/README.md") and rel.startswith(("tests/", "examples/")):
        return "guide"
    if rel.startswith(".agents/"):
        return "skill"
    if rel.startswith("docs/specs/") or rel.startswith("docs/domains/"):
        return "spec"
    if rel.startswith("docs/design/"):
        return "design"
    if rel.startswith("docs/decisions/"):
        return "decision"
    if rel.startswith("templates/"):
        return "template"
    return "config"


def _clip_plain_summary(text: str, limit: int = 180) -> str:
    if len(text) <= limit:
        return text
    cut = text[: limit - 1]
    sp = cut.rfind(" ")
    return (cut[:sp] if sp > 90 else cut).rstrip(" ,;:.，；、") + "…"


def _extract_plain_summary(text: str, meta: dict, body: str) -> str:
    for key in ("summary", "one_liner", "promise", "description"):
        val = str(meta.get(key, "")).strip()
        if val:
            return val
    in_fence = False
    pending_label = ""
    para_parts: list[str] = []
    para_from_bullet = False
    for line in (body or text).splitlines():
        raw_st = line.strip()
        if raw_st.startswith(("```", "~~~")):
            in_fence = not in_fence
            if para_parts:
                break
            continue
        if in_fence:
            continue
        is_struct_break = not raw_st or raw_st.startswith(("#", "<!--", "|", "---", "[["))
        if is_struct_break:
            if para_parts and sum(len(p) for p in para_parts) > 12:
                break
            if not raw_st:
                para_parts = []
                para_from_bullet = False
            continue
        is_bullet = raw_st.startswith(("- ", "* "))
        if is_bullet and para_parts and (para_from_bullet or sum(len(p) for p in para_parts) > 12):
            break
        st = re.sub(r"^>+\s*", "", raw_st)
        st = re.sub(r"^\[!(?:NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]\s*", "", st, flags=re.I).strip()
        if is_bullet:
            st = st[2:].strip()
        st = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", st)
        st = st.replace("`", "").replace("**", "").strip()
        if not st or re.match(r"^(?:English version|中文说明|中文版)\s*[:：]", st, re.I):
            continue
        if st.endswith((":", "：")) and len(st) <= 36 and not pending_label and not para_parts:
            pending_label = st
            continue
        if pending_label:
            st = f"{pending_label} {st}"
            pending_label = ""
        para_parts.append(st)
        para_from_bullet = para_from_bullet or is_bullet
        if sum(len(p) for p in para_parts) >= 180:
            break
    joined = " ".join(para_parts).strip()
    if len(joined) > 12:
        return _clip_plain_summary(joined)
    return pending_label or joined


def _build_repo_doc(root: Path, fp: Path, modules: dict[str, ModuleSpec]) -> RepoDoc | None:
    try:
        text = fp.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None
    rel = fp.relative_to(root).as_posix()
    meta: dict = {}
    body = text
    h1 = fp.name
    mermaids: tuple = ()
    if fp.suffix.lower() == ".md":
        meta, body, _ = parse_frontmatter(text)
        h1_found, _, _, mermaids = extract_markdown_structure(text, rel)
        if h1_found:
            h1 = h1_found
    elif fp.suffix.lower() == ".html":
        title_m = re.search(r"<h1[^>]*>(.*?)</h1>|<title[^>]*>(.*?)</title>", text, flags=re.I | re.S)
        if title_m:
            raw_t = title_m.group(1) or title_m.group(2) or ""
            cleaned_t = " ".join(html.unescape(re.sub(r"<[^>]+>", " ", raw_t)).split())
            if cleaned_t:
                h1 = cleaned_t
    title = str(meta.get("title") or meta.get("name") or h1 or fp.name).replace("`", "").strip()
    if fp.suffix.lower() == ".html":
        summary = ""
        for p_m in re.finditer(r"<p\b[^>]*>(.*?)</p>", text, flags=re.I | re.S):
            p_txt = " ".join(html.unescape(re.sub(r"<[^>]+>", " ", p_m.group(1))).split())
            if len(p_txt) > 8:
                summary = p_txt[:180] + ("…" if len(p_txt) > 180 else "")
                break
        if not summary:
            summary = f"HTML design document ({rel})"
        stripped = re.sub(r"<(script|style)\b[^>]*>.*?</\1>", "", text, flags=re.I | re.S)
        stripped = html.unescape(re.sub(r"<[^>]+>", " ", stripped))
        body = "\n".join(" ".join(ln.split()) for ln in stripped.splitlines() if ln.strip())
    elif fp.suffix.lower() == ".toml":
        top_comments: list[str] = []
        for ln in text.splitlines():
            st = ln.strip()
            if not st:
                if top_comments:
                    break
                continue
            if st.startswith("#"):
                c = st.lstrip("# ").strip()
                if c and not set(c) <= {"-", "=", "*"}:
                    top_comments.append(c)
                continue
            break
        summary = _clip_plain_summary(" ".join(top_comments)) if top_comments else f"TOML configuration / ledger ({rel})"
    else:
        summary = _extract_plain_summary(text, meta, body)
    meta_id = str(meta.get("id", "")).strip()
    owner = meta_id if meta_id in modules else (match_path_to_module(rel, modules) or "")
    domain = str(meta.get("domain", "")).strip()
    if not domain and owner and owner in modules:
        domain = modules[owner].domain
    elif not domain and rel.startswith("docs/specs/"):
        parts = rel.split("/")
        if len(parts) >= 3 and parts[2] != "README.md":
            domain = parts[2]
    return RepoDoc(
        path=rel,
        title=title,
        category=_classify_doc(rel),
        summary=summary,
        body_markdown=(body if fp.suffix.lower() in (".md", ".html") else text).strip(),
        line_count=len(text.splitlines()),
        domain=domain,
        owner_module=owner,
        mermaid_blocks=mermaids,
    )


def _infer_dir_domain(
    dir_rel: str,
    doc_paths: tuple[str, ...],
    doc_by_path: dict[str, RepoDoc],
    modules: dict[str, ModuleSpec],
) -> str:
    """Derive directory domain strictly from the host repo's own docs and module `owns` globs."""
    if dir_rel.startswith("archive"):
        return ""
    counts: dict[str, int] = {}
    for dp in doc_paths:
        doc = doc_by_path.get(dp)
        if doc and doc.domain:
            counts[doc.domain] = counts.get(doc.domain, 0) + 1
    if dir_rel != "(root)":
        for mod in modules.values():
            for pat in mod.owns:
                base = pat.split("*", 1)[0].rstrip("/")
                if not base:
                    continue
                if base == dir_rel or base.startswith(dir_rel + "/") or dir_rel.startswith(base + "/"):
                    counts[mod.domain] = counts.get(mod.domain, 0) + 1
    if not counts:
        return ""
    return next(iter(counts)) if len(counts) == 1 else ""


def _dir_stats(root: Path, dir_rel: str, all_docs: dict[str, RepoDoc]) -> tuple[int, int, tuple[str, ...]]:
    if dir_rel == "(root)":
        files = [p for p in sorted(root.iterdir()) if p.is_file() and not p.name.startswith(".")]
        doc_paths = tuple(p.name for p in files if p.name in all_docs)
        lines = sum(len(p.read_text(encoding="utf-8", errors="ignore").splitlines()) for p in files if p.suffix.lower() in TEXT_DOC_EXTS)
        return len(files), lines, doc_paths

    target = root / dir_rel
    if not target.is_dir():
        return 0, 0, ()
    file_count = 0
    total_lines = 0
    doc_paths: list[str] = []
    skip_docs_children = dir_rel == "docs"
    for dirpath, dirnames, filenames in os.walk(target):
        dirnames[:] = [d for d in sorted(dirnames) if d not in IGNORE_WALK]
        dp = Path(dirpath)
        if skip_docs_children and dp != target and dp.relative_to(target).parts[0] in {
            "contracts", "guides", "specs", "design", "decisions", "evaluations"
        }:
            dirnames[:] = []
            continue
        for fn in sorted(filenames):
            if fn.startswith("."):
                continue
            fp = dp / fn
            rel = fp.relative_to(root).as_posix()
            file_count += 1
            if rel in all_docs:
                doc_paths.append(rel)
            if fp.suffix.lower() in (TEXT_DOC_EXTS | {".py", ".js", ".ts", ".tsx", ".css", ".html"}):
                try:
                    total_lines += len(fp.read_text(encoding="utf-8", errors="ignore").splitlines())
                except OSError:
                    pass
    return file_count, total_lines, tuple(doc_paths)


def index_repository_docs_and_dirs(
    root: Path,
    modules: dict[str, ModuleSpec],
) -> tuple[tuple[RepoDoc, ...], tuple[DirectoryEntry, ...]]:
    """Collect active repository documents and bilingual directory map entries."""
    docs_list: list[RepoDoc] = []
    seen: set[str] = set()

    def _add_file(p: Path) -> None:
        if not p.is_file():
            return
        rel = p.relative_to(root).as_posix()
        if rel in seen:
            return
        seen.add(rel)
        doc = _build_repo_doc(root, p, modules)
        if doc is not None:
            docs_list.append(doc)

    for top_name in (
        "AGENTS.md", "README.md", "README_CN.md", "ARCHITECTURE.md", "CONTRIBUTING.md",
        "docs-policy.toml", "architecture-rules.toml",
    ):
        _add_file(root / top_name)
    _add_file(root / "archive" / "README.md")

    for folder in ("docs", "templates", ".agents", "tests", "examples"):
        base = root / folder
        if not base.is_dir():
            continue
        for dirpath, dirnames, filenames in os.walk(base):
            dirnames[:] = [d for d in sorted(dirnames) if d not in IGNORE_WALK]
            for fn in sorted(filenames):
                fp = Path(dirpath) / fn
                if fp.suffix.lower() in TEXT_DOC_EXTS:
                    _add_file(fp)

    for child in sorted(root.iterdir()):
        if not child.is_dir() or child.name.startswith(".") or child.name in IGNORE_WALK:
            continue
        if child.name in ("docs", "templates", "tests", "examples", "archive", "scripts"):
            continue
        for dirpath, dirnames, filenames in os.walk(child):
            dirnames[:] = [d for d in sorted(dirnames) if d not in IGNORE_WALK]
            for fn in sorted(filenames):
                if fn.lower().endswith(".md"):
                    _add_file(Path(dirpath) / fn)

    doc_by_path = {d.path: d for d in docs_list}
    entries: list[DirectoryEntry] = []
    recorded_dirs: set[str] = set()

    for dpath, lzh, len_, szh, sen in KNOWN_DIRS:
        if dpath != "(root)" and not (root / dpath).is_dir():
            continue
        fcount, tlines, dpaths = _dir_stats(root, dpath, doc_by_path)
        entries.append(
            DirectoryEntry(
                path=dpath,
                label_zh=lzh,
                label_en=len_,
                summary_zh=szh,
                summary_en=sen,
                file_count=fcount,
                doc_count=len(dpaths),
                total_lines=tlines,
                domain=_infer_dir_domain(dpath, dpaths, doc_by_path, modules),
                doc_paths=dpaths,
            )
        )
        recorded_dirs.add(dpath)

    # Also capture any custom top-level source/doc directories in adopting repos
    for child in sorted(root.iterdir()):
        if not child.is_dir() or child.name.startswith(".") or child.name in IGNORE_WALK:
            continue
        rel = child.name
        if rel in recorded_dirs or rel == "archive" or any(r.startswith(rel + "/") for r in recorded_dirs):
            continue
        fcount, tlines, dpaths = _dir_stats(root, rel, doc_by_path)
        if fcount == 0:
            continue
        entries.append(
            DirectoryEntry(
                path=rel,
                label_zh=f"目录 {rel}/",
                label_en=f"Directory {rel}/",
                summary_zh=f"项目顶层目录 `{rel}/`，包含 {fcount} 个文件（共 {tlines} 行）。",
                summary_en=f"Project top-level directory `{rel}/` containing {fcount} file(s) ({tlines} lines).",
                file_count=fcount,
                doc_count=len(dpaths),
                total_lines=tlines,
                domain=_infer_dir_domain(rel, dpaths, doc_by_path, modules),
                doc_paths=dpaths,
            )
        )

    return tuple(sorted(docs_list, key=lambda d: (_CAT_ORDER.get(d.category, 99), d.path))), tuple(entries)
