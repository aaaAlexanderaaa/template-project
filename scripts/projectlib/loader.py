# Role: Loads all Single-Source-of-Truth Markdown specs, TOML ledgers, doc inventory, and Git/AST telemetry into ProjectGraph.
# Out of scope: Modifying repository files or serving HTTP traffic.
# Anchors: spec=graph.indexer, ADR-002, SRC-015, SRC-017, SRC-018, SRC-019

from __future__ import annotations

import json
import re
import tomllib
from dataclasses import replace
from pathlib import Path
from typing import Any

from .doc_inventory import index_repository_docs_and_dirs
from .frontmatter import as_str_tuple, extract_markdown_structure, parse_frontmatter
from .git_telemetry import collect_git_telemetry
from .import_scanner import discover_governed_files, scan_files_and_imports
from .model import (
    DecisionRecord,
    DomainSpec,
    Milestone,
    ModuleSpec,
    ProjectGraph,
    SourceAnchor,
    ValidationFinding,
    WorkTask,
)

STATE_REL_PATH = "tmp/project-state.json"


def load_runtime_state(root: Path) -> dict[str, Any]:
    state_file = root / STATE_REL_PATH
    if not state_file.is_file():
        return {}
    try:
        data = json.loads(state_file.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except (OSError, json.JSONDecodeError):
        return {}


def save_runtime_state(root: Path, updates: dict[str, Any]) -> dict[str, Any]:
    current = load_runtime_state(root)
    current.update(updates)
    state_file = root / STATE_REL_PATH
    state_file.parent.mkdir(parents=True, exist_ok=True)
    state_file.write_text(json.dumps(current, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return current


def _clip_clause(text: str, limit: int = 240) -> str:
    if len(text) <= limit:
        return text
    cut = text[: limit - 1]
    for sep in (". ", "。", "; ", "；"):
        idx = cut.rfind(sep)
        if idx >= limit // 2:
            return cut[: idx + (1 if sep in (". ", "; ") else 1)].strip()
    sp = cut.rfind(" ")
    if sp > limit // 2:
        cut = cut[:sp]
    return cut.rstrip(" ,;:.，；、") + "…"


def _extract_domain_non_goals(meta: dict[str, Any], body: str) -> str:
    raw = meta.get("non_goals")
    if raw:
        return raw.strip() if isinstance(raw, str) else "; ".join(as_str_tuple(raw))
    in_scope_sec = True
    fallback = ""
    for line in body.splitlines():
        s = line.strip()
        if s.startswith("##"):
            in_scope_sec = bool(re.search(r"non-goals?|out of scope|positioning|boundary|role|不做什么|边界|定位", s, re.I))
            continue
        if s.startswith("#"):
            continue
        if not s or s.startswith("```"):
            continue
        s_clean = re.sub(r"^>+\s*", "", s)
        s_clean = re.sub(r"^\[!(?:NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]\s*", "", s_clean, flags=re.I).strip()
        if not s_clean:
            continue
        m_lbl = re.match(r"^[-*]?\s*\*\*(Out of scope|Non-goals?|Explicit Scope Boundary|Forbidden coupling|Positioning|不做什么|明确不做)\*\*\s*[:：]\s*(.+)$", s_clean, re.I)
        if m_lbl:
            clean = re.sub(r"[`*_]", "", m_lbl.group(2)).strip()
            if re.search(r"out of scope|non-goal|explicit|不做什么|明确不做", m_lbl.group(1), re.I):
                return _clip_clause(clean)
            fallback = fallback or _clip_clause(clean)
        elif in_scope_sec and not fallback and len(s_clean) > 20 and not s_clean.startswith("|"):
            clean = re.sub(r"[`*]", "", s_clean).lstrip("- ").strip()
            if re.search(r"leaves\b|distinct from|subordinate|helper|rather than|not the core|不承担|不做|而非", clean, re.I):
                fallback = _clip_clause(clean)
    return fallback


def _load_toml(path: Path, errors: list[ValidationFinding], root: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        return tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError) as exc:
        rel = path.relative_to(root).as_posix()
        errors.append(ValidationFinding("toml_syntax", "error", rel, f"TOML parse error: {exc}"))
        return {}


def _synthesize_day_zero_modules(
    root: Path,
    source_roots: list[str],
    placeholders: set[str],
    harness_paths: list[str],
    default_stage: str,
    proj_lang: str = "en",
) -> tuple[dict[str, DomainSpec], dict[str, ModuleSpec]]:
    """Build directory preview containers when `docs/specs/` has zero modules on Day 0."""
    rel_files = discover_governed_files(root, source_roots, placeholders, harness_paths)
    has_subdirs = {Path(rel).parts[0] for rel in rel_files if len(Path(rel).parts) >= 3}
    buckets: dict[str, list[str]] = {}
    for rel in rel_files:
        parts = Path(rel).parts
        if len(parts) >= 3:
            pat = f"{parts[0]}/{parts[1]}/**"
            mod_slug = f"{parts[0]}-{parts[1]}".lower().replace("_", "-")
        elif len(parts) == 2:
            mod_slug = parts[0].lower().replace("_", "-")
            pat = rel if parts[0] in has_subdirs else f"{parts[0]}/**"
        else:
            mod_slug = "root-files"
            pat = rel
        items = buckets.setdefault(mod_slug, [])
        if pat not in items:
            items.append(pat)

    is_zh = proj_lang == "zh"
    domains: dict[str, DomainSpec] = {}
    modules: dict[str, ModuleSpec] = {}
    if buckets:
        domains["codebase"] = DomainSpec(
            id="codebase",
            name="未接入规范的现有代码概览" if is_zh else "Unadopted Codebase Overview",
            stage=default_stage,
            summary="尚未建立模块规格前，按源码目录自动汇总的预览视图。" if is_zh else "Day-0 directory view inferred automatically from source files before writing specs.",
            promise="展示顶层目录、代码行数与导入关系，供逐步补齐模块边界规格。" if is_zh else "Maps top-level directories, file sizes, and existing import edges without waiting for manual specs.",
            doc_path="ARCHITECTURE.md",
        )
        for mod_slug, pats in sorted(buckets.items()):
            pats_tuple = tuple(sorted(pats))
            mod_id = f"codebase.{mod_slug}"
            label = pats_tuple[0].rstrip("/*") if len(pats_tuple) == 1 else mod_slug
            modules[mod_id] = ModuleSpec(
                id=mod_id,
                domain="codebase",
                kind="module-spec",
                stage=default_stage,
                title=f"目录 {label}" if is_zh else f"Directory {label}",
                summary=(
                    f"自动识别的代码目录分组，对应 `{', '.join(pats_tuple[:3])}`。"
                    if is_zh
                    else f"Auto-discovered directory group matching `{', '.join(pats_tuple[:3])}`."
                ),
                promise=(
                    "检查文件数量、行数与导入边界后，再拆分或正式认领为模块规格。"
                    if is_zh
                    else "Inspect files, line counts, and imports before assigning formal module specs."
                ),
                owns=pats_tuple,
                depends_on=(),
                sources=(),
                supersedes=(),
                doc_path="ARCHITECTURE.md",
            )
    return domains, modules


def load_project_graph(root: Path) -> ProjectGraph:
    root = root.resolve()
    errors: list[ValidationFinding] = []
    policy = _load_toml(root / "docs-policy.toml", errors, root)

    proj_cfg = policy.get("project", {})
    default_stage = str(proj_cfg.get("default_stage", "usable"))
    discipline_version = str(policy.get("discipline_version", "unknown"))
    identity = str(proj_cfg.get("identity", "product"))

    # 1. Load ARCHITECTURE.md
    arch_path = root / "ARCHITECTURE.md"
    sys_id = "system.root"
    proj_name = str(proj_cfg.get("name", "")) or root.name
    one_liner = ""
    arch_body = ""
    sys_mermaids = ()
    if arch_path.is_file():
        arch_text = arch_path.read_text(encoding="utf-8")
        arch_meta, arch_body, fm_err = parse_frontmatter(arch_text)
        if fm_err:
            errors.append(ValidationFinding("frontmatter", "error", "ARCHITECTURE.md", fm_err))
        h1, _, _, sys_mermaids = extract_markdown_structure(arch_text, "ARCHITECTURE.md")
        sys_id = str(arch_meta.get("id", sys_id))
        proj_name = str(arch_meta.get("name", proj_name or h1 or root.name))
        one_liner = str(arch_meta.get("one_liner", ""))
        default_stage = str(arch_meta.get("stage", default_stage))

    graph = ProjectGraph(
        root_dir=str(root),
        system_id=sys_id,
        project_name=proj_name,
        one_liner=one_liner,
        default_stage=default_stage,
        discipline_version=discipline_version,
        identity=identity,
        policy=policy,
        system_mermaid=sys_mermaids,
        architecture_markdown=arch_body.strip(),
        parse_errors=errors,
    )

    # 2. Load verbatim sources (`docs/sources.toml` + optional domain shards)
    source_files = [root / "docs" / "sources.toml"]
    specs_root = root / "docs" / "specs"
    if specs_root.is_dir():
        source_files.extend(sorted(specs_root.glob("*/sources.toml")))
    domains_alt = root / "docs" / "domains"
    if domains_alt.is_dir():
        source_files.extend(sorted(domains_alt.glob("*/sources.toml")))

    for sf in source_files:
        if not sf.is_file():
            continue
        rel = sf.relative_to(root).as_posix()
        data = _load_toml(sf, errors, root)
        for item in data.get("sources", []):
            sid = str(item.get("id", "")).strip()
            if not sid:
                errors.append(ValidationFinding("source_id", "error", rel, "Source entry missing `id`"))
                continue
            if sid in graph.sources:
                errors.append(ValidationFinding("duplicate_id", "error", rel, f"Duplicate source id `{sid}`"))
                continue
            graph.sources[sid] = SourceAnchor(
                id=sid,
                date=str(item.get("date", "")),
                status=str(item.get("status", "active")),
                context=str(item.get("context", "")),
                quote=str(item.get("quote", "")).strip(),
                origin_path=rel,
            )

    # 3. Two-pass loading of domain specs and module specs (load-order independent)
    spec_candidates: list[Path] = []
    if specs_root.is_dir():
        spec_candidates.extend(sorted(specs_root.rglob("*.md")))
    design_root = root / "docs" / "design"
    if design_root.is_dir():
        spec_candidates.extend(sorted(design_root.rglob("*.md")))
    if domains_alt.is_dir():
        spec_candidates.extend(sorted(domains_alt.rglob("*.md")))

    parsed_mods: list[tuple[str, str, dict[str, Any], str, str, tuple, str]] = []
    for md_path in spec_candidates:
        rel = md_path.relative_to(root).as_posix()
        text = md_path.read_text(encoding="utf-8")
        meta, body, fm_err = parse_frontmatter(text)
        if fm_err:
            errors.append(ValidationFinding("frontmatter", "error", rel, fm_err))
            continue
        if not meta or ("id" not in meta and "domain" not in meta):
            continue
        h1, _, _, mermaids = extract_markdown_structure(text, rel)
        kind = str(meta.get("kind", "domain-spec" if md_path.name == "README.md" else "module-spec"))
        raw_id = str(meta.get("id", f"domain.{md_path.parent.name}")).strip()

        if kind == "domain-spec" or (md_path.name == "README.md" and raw_id.startswith("domain.")):
            dom_slug = str(meta.get("domain", "")).strip() or raw_id.removeprefix("domain.")
            graph.domains[dom_slug] = DomainSpec(
                id=dom_slug,
                name=str(meta.get("name", h1 or dom_slug)),
                stage=str(meta.get("stage", default_stage)),
                summary=str(meta.get("summary", "")),
                promise=str(meta.get("promise", "")),
                doc_path=rel,
                non_goals=_extract_domain_non_goals(meta, body),
                mermaid_blocks=mermaids,
                body_markdown=body.strip(),
            )
        elif kind in ("module-spec", "surface-spec"):
            parsed_mods.append((rel, md_path.parent.name, meta, raw_id, h1, mermaids, body))

    for rel, parent_name, meta, raw_id, h1, mermaids, body in parsed_mods:
        dom_slug = str(meta.get("domain", "")).strip()
        if not dom_slug:
            dom_slug = parent_name if parent_name not in ("specs", "design", "domains") else "core"
        if raw_id in graph.modules:
            errors.append(ValidationFinding("duplicate_id", "error", rel, f"Duplicate module spec id `{raw_id}`"))
            continue
        dom_stage = graph.domains[dom_slug].stage if dom_slug in graph.domains else default_stage
        graph.modules[raw_id] = ModuleSpec(
            id=raw_id,
            domain=dom_slug,
            kind=str(meta.get("kind", "module-spec")),
            stage=str(meta.get("stage", dom_stage)),
            title=h1 or raw_id,
            summary=str(meta.get("summary", "")),
            promise=str(meta.get("promise", "")),
            owns=as_str_tuple(meta.get("owns")),
            depends_on=as_str_tuple(meta.get("depends_on")),
            sources=as_str_tuple(meta.get("sources")),
            supersedes=as_str_tuple(meta.get("supersedes")),
            doc_path=rel,
            mermaid_blocks=mermaids,
            body_markdown=body.strip(),
        )

    proj_lang = str(policy.get("project", {}).get("language", "en")).strip().lower()
    for spec in graph.modules.values():
        if spec.domain not in graph.domains:
            dom_title = (
                "示例业务域"
                if proj_lang == "zh" and spec.domain == "example"
                else spec.domain.replace("-", " ").title()
            )
            graph.domains[spec.domain] = DomainSpec(
                id=spec.domain,
                name=dom_title,
                stage=default_stage,
                summary=one_liner or f"Modules in domain `{spec.domain}`",
                promise="",
                doc_path="ARCHITECTURE.md",
            )

    # 4. Load cross-module decisions (`docs/decisions/*.md`)
    dec_root = root / "docs" / "decisions"
    if dec_root.is_dir():
        for md_path in sorted(dec_root.glob("*.md")):
            rel = md_path.relative_to(root).as_posix()
            text = md_path.read_text(encoding="utf-8")
            meta, body, fm_err = parse_frontmatter(text)
            if fm_err:
                errors.append(ValidationFinding("frontmatter", "error", rel, fm_err))
                continue
            if not meta or "id" not in meta:
                continue
            did = str(meta["id"]).strip()
            h1, _, _, _ = extract_markdown_structure(text, rel)
            graph.decisions[did] = DecisionRecord(
                id=did,
                status=str(meta.get("status", "current")),
                title=str(meta.get("title", h1 or did)),
                sources=as_str_tuple(meta.get("sources")),
                affects=as_str_tuple(meta.get("affects")),
                supersedes=as_str_tuple(meta.get("supersedes")),
                superseded_by=str(meta.get("superseded_by", "")).strip(),
                doc_path=rel,
                body_markdown=body.strip(),
            )
        for did, dec in list(graph.decisions.items()):
            for old_id in dec.supersedes:
                if old_id in graph.decisions:
                    old_dec = graph.decisions[old_id]
                    graph.decisions[old_id] = replace(
                        old_dec,
                        superseded_by=old_dec.superseded_by or did,
                        status="superseded",
                    )

    # 5. Load active & archived work queues
    work_files: list[tuple[Path, bool]] = [(root / "docs" / "work.toml", False)]
    if specs_root.is_dir():
        work_files.extend((p, False) for p in sorted(specs_root.glob("*/work.toml")))
    if domains_alt.is_dir():
        work_files.extend((p, False) for p in sorted(domains_alt.glob("*/work.toml")))
    arch_work_dir = root / "docs" / "archive"
    if arch_work_dir.is_dir():
        work_files.extend((p, True) for p in sorted(arch_work_dir.glob("work*.toml")))

    for wf, is_archived in work_files:
        if not wf.is_file():
            continue
        rel = wf.relative_to(root).as_posix()
        data = _load_toml(wf, errors, root)
        for m in data.get("milestones", []):
            mid = str(m.get("id", "")).strip()
            if not mid:
                continue
            dom = str(m.get("domain", "")).strip() or next(iter(graph.domains), "core")
            if dom not in graph.domains:
                graph.domains[dom] = DomainSpec(
                    id=dom, name=dom.replace("-", " ").title(), stage=default_stage, summary="", promise="", doc_path="ARCHITECTURE.md"
                )
            graph.milestones[mid] = Milestone(
                id=mid,
                domain=dom,
                name=str(m.get("name", mid)),
                slot="done" if is_archived else str(m.get("slot", "now")),
                depends_on=as_str_tuple(m.get("depends_on")),
                era=str(m.get("era", "Archived" if is_archived else "")),
                origin_path=rel,
                archived=is_archived,
            )
        for t in data.get("tasks", []):
            tid = str(t.get("id", "")).strip()
            if not tid:
                continue
            graph.tasks[tid] = WorkTask(
                id=tid,
                milestone=str(t.get("milestone", "")).strip(),
                title=str(t.get("title", tid)),
                state="done" if is_archived else str(t.get("state", "todo")),
                human_check=str(t.get("human_check", "pending")),
                specs=as_str_tuple(t.get("specs")),
                decisions=as_str_tuple(t.get("decisions")),
                sources=as_str_tuple(t.get("sources")),
                blocker_question=str(t.get("blocker_question", "")),
                blocker_options=as_str_tuple(t.get("blocker_options")),
                selected_option=str(t.get("selected_option", "")).strip(),
                parent=str(t.get("parent", "")).strip(),
                origin_path=rel,
                archived=is_archived,
            )

    # 6. Policy layout, Day-0 preview synthesis, runtime state & telemetry
    layout_cfg = policy.get("layout", {})
    budgets_cfg = policy.get("budgets", {})
    source_roots = [str(s) for s in (layout_cfg.get("source_roots") or proj_cfg.get("source_roots") or ["src"])]
    placeholders = {str(s) for s in layout_cfg.get("placeholder_names", ["README.md", ".gitkeep"])}
    harness_paths = [str(s) for s in layout_cfg.get("harness_paths", ["tests", "archive", "tmp"])]
    if identity != "template" and (root / "scripts" / "projectlib").is_dir() and not (root / "docs" / "specs" / "discipline").is_dir():
        for tool_hp in ("scripts/projectlib", "scripts/project.py", "scripts/check_docs.py", "scripts/read_rules.py", "scripts/rule_reading.py"):
            if tool_hp not in harness_paths:
                harness_paths.append(tool_hp)
    if not graph.modules and not any((root / s).exists() for s in source_roots):
        skip_dirs = {"docs", "tmp", "archive", "tests", "templates", "examples", "node_modules", "__pycache__", "build", "dist", "venv"} | {
            h.rstrip("/").split("/")[0] for h in harness_paths if "/" not in h.rstrip("/")
        }
        if (root / "scripts" / "projectlib").is_dir():
            skip_dirs.add("scripts")
        auto_roots = [d.name for d in sorted(root.iterdir()) if d.is_dir() and not d.name.startswith(".") and d.name not in skip_dirs]
        if auto_roots:
            source_roots = auto_roots
    max_src = int(budgets_cfg.get("max_source_lines", 500))
    max_css = int(budgets_cfg.get("max_style_lines", 300))

    scan_modules = dict(graph.modules)
    if not graph.modules:
        syn_doms, syn_mods = _synthesize_day_zero_modules(root, source_roots, placeholders, harness_paths, default_stage, proj_lang=proj_lang)
        if syn_mods:
            graph.domains.update(syn_doms)
            graph.modules.update(syn_mods)
            scan_modules = syn_mods
            graph.is_day_zero_synthetic = True

    graph.runtime_state = load_runtime_state(root)
    policy_anchor = str(policy.get("collaboration", {}).get("review_anchor_sha", "")).strip()
    last_review_sha = str(graph.runtime_state.get("last_review_sha", "") or policy_anchor)
    last_review_wt_digest = str(graph.runtime_state.get("last_review_wt_digest", "")).strip()
    lag_churn, git_summary = collect_git_telemetry(
        root,
        scan_modules,
        last_review_sha=last_review_sha,
        last_review_wt_digest=last_review_wt_digest,
    )
    graph.git_summary = git_summary

    files, edges, telemetry, claims_map = scan_files_and_imports(
        root=root,
        modules=scan_modules,
        source_roots=source_roots,
        placeholder_names=placeholders,
        harness_paths=harness_paths,
        max_source_lines=max_src,
        max_style_lines=max_css,
        git_lag_churn=lag_churn,
    )
    graph.files = files
    graph.import_edges = edges
    graph.module_telemetry = telemetry
    graph.git_summary["file_claims"] = claims_map

    graph.repo_docs, graph.directory_map = index_repository_docs_and_dirs(root, graph.modules)
    return graph
