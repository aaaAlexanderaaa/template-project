# Role: Validates single-source graph links, code ownership, import boundaries, plain language, budgets, and git-diff context nudges.
# Out of scope: Modifying repository files or running HTTP servers.
# Anchors: spec=graph.validator, ADR-002, ADR-003, SRC-010, SRC-013, SRC-018, SRC-019

from __future__ import annotations

import re
import tomllib
from fnmatch import fnmatch
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlsplit

from .frontmatter import extract_markdown_structure
from .git_telemetry import get_working_changed_files, match_path_to_module
from .model import ProjectGraph, ValidationFinding, module_source_refs
from .prose_checks import (
    BANNED_JARGON,
    DISCLAIMER_CHAINS,
    PLACEHOLDER_RE,
    check_plain_language,
    check_spec_structure,
    collect_live_markdown_files,
    scrub_examples,
)

TEMPLATE_REMOTE_SLUG = "github.com/aaaalexanderaaa/template-project"


# `discipline_version = "x.y.z"` copied into Markdown. The value lives only in `docs-policy.toml`.
HARDCODED_VERSION_RE = re.compile(r'discipline_version\s*=\s*"(\d+(?:\.\d+)+)"')


def find_hardcoded_versions(root: Path, md_files: list[Path] | None = None) -> list[tuple[str, int, str]]:
    """Return `(relative path, line number, version)` for every Markdown line that copies `discipline_version`."""
    hits: list[tuple[str, int, str]] = []
    for mp in md_files if md_files is not None else collect_live_markdown_files(root):
        rel_md = mp.relative_to(root).as_posix()
        if rel_md.startswith("docs/decisions/"):
            continue  # decision records may name the version that was current back then
        for ln, line in enumerate(mp.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
            for m in HARDCODED_VERSION_RE.finditer(line):
                hits.append((rel_md, ln, m.group(1)))
    return hits


def _normalize_remote(url: str) -> str:
    val = url.strip().rstrip("/")
    if val.endswith(".git"):
        val = val[:-4]
    val = re.sub(r"^(?:https?://|ssh://|git@)", "", val)
    val = re.sub(r"^[^@/]+@", "", val).replace(":", "/")
    return val.lower()


def _matches_managed(path: str, managed_paths: list[str]) -> bool:
    for pat in managed_paths:
        norm = pat.rstrip("/")
        if path == norm or path.startswith(norm + "/") or fnmatch(path, pat):
            return True
        if pat.endswith("/**") and path.startswith(pat[:-3] + "/"):
            return True
    return False


def _effective_severity(graph: ProjectGraph, key: str, path: str, default: str = "error") -> str:
    sev = str(graph.policy.get("severity", {}).get(key, default))
    adoption_cfg = graph.policy.get("adoption", {})
    adoption_stage = str(adoption_cfg.get("stage", "adopted"))
    enforce_keys = (
        "source_ownership",
        "import_boundaries",
        "file_size_budget",
        "missing_role_header",
        "catchall_directories",
        "unknown_task_specs",
    )
    if adoption_stage == "observed" and sev == "error" and key in enforce_keys:
        return "advisory"
    if adoption_stage == "scoped_enforcement" and sev == "error" and key in enforce_keys:
        managed = [str(p) for p in adoption_cfg.get("managed_paths", [])]
        if managed and not _matches_managed(path, managed):
            return "advisory"
    return sev


def validate_project_graph(
    graph: ProjectGraph,
    strict: bool = False,
    diff_base: str | None = None,
) -> tuple[list[ValidationFinding], dict[str, Any]]:
    """Run all deterministic single-source, boundary, plain-language, budget, and contextual checks."""
    root = Path(graph.root_dir)
    findings: list[ValidationFinding] = list(graph.parse_errors)

    def emit(
        rule_id: str,
        sev_key: str,
        path: str,
        msg: str,
        line: int = 0,
        default_sev: str = "error",
        *,
        strict_exempt: bool = False,
    ) -> None:
        sev = _effective_severity(graph, sev_key, path, default_sev)
        if sev == "off":
            return
        if strict and sev == "advisory" and not strict_exempt:
            sev = "error"
        findings.append(ValidationFinding(rule_id, sev, path, msg, line))

    # 1. Copied checkout guard
    remote_norm = _normalize_remote(str(graph.git_summary.get("remote_url", "")))
    if graph.identity == "template" and (
        (remote_norm and remote_norm != TEMPLATE_REMOTE_SLUG)
        or (not remote_norm and not (root / "docs" / "specs" / "discipline").exists())
    ):
        emit(
            "copied_checkout",
            "broken_links_and_ids",
            "docs-policy.toml",
            f"Repository uses `[project].identity = \"template\"` outside `{TEMPLATE_REMOTE_SLUG}`; run onboarding to set product identity.",
        )
    agents_file = root / "AGENTS.md"
    if graph.identity != "template" and agents_file.is_file():
        agents_txt = agents_file.read_text(encoding="utf-8", errors="ignore").lower()
        if TEMPLATE_REMOTE_SLUG in agents_txt:
            emit(
                "copied_checkout",
                "broken_links_and_ids",
                "AGENTS.md",
                "Root `AGENTS.md` still carries the `template-project` Copied Checkout Guard; run `project.py init` to install product instructions.",
            )

    # 2. ID reference integrity across specs, ADRs, and work queues
    referenced_sources: set[str] = set()
    for mod in graph.modules.values():
        _, via_refs = module_source_refs(graph, mod)
        via_adr = {sid: did for sid, did in via_refs}
        for dec in graph.decisions.values():
            if dec.status != "superseded" and (mod.id in dec.affects or mod.domain in dec.affects):
                for sid in dec.sources:
                    via_adr.setdefault(sid, dec.id)
        for sid in mod.sources:
            referenced_sources.add(sid)
            if sid not in graph.sources:
                emit("unknown_source", "broken_links_and_ids", mod.doc_path, f"Module `{mod.id}` references unknown source `{sid}`.")
            elif sid in via_adr:
                emit(
                    "duplicate_module_source",
                    "duplicate_module_source",
                    mod.doc_path,
                    f"Module `{mod.id}` re-lists `{sid}`, which `{via_adr[sid]}` already brings through `affects`; remove it from the spec's `sources`.",
                )
        for dep in mod.depends_on:
            if dep not in graph.modules:
                emit("unknown_dependency", "broken_links_and_ids", mod.doc_path, f"Module `{mod.id}` depends_on unknown module `{dep}`.")
        for sup in mod.supersedes:
            if sup not in graph.modules and sup not in graph.decisions:
                emit("unknown_supersedes", "broken_links_and_ids", mod.doc_path, f"Module `{mod.id}` supersedes unknown id `{sup}`.")

    for dec in graph.decisions.values():
        for sid in dec.sources:
            referenced_sources.add(sid)
            if sid not in graph.sources:
                emit("unknown_source", "broken_links_and_ids", dec.doc_path, f"Decision `{dec.id}` references unknown source `{sid}`.")
        for aff in dec.affects:
            if aff not in graph.modules and aff not in graph.domains:
                emit("unknown_affect", "broken_links_and_ids", dec.doc_path, f"Decision `{dec.id}` affects unknown module/domain `{aff}`.")
        for sup in dec.supersedes:
            if sup not in graph.decisions:
                emit("unknown_supersedes", "broken_links_and_ids", dec.doc_path, f"Decision `{dec.id}` supersedes unknown decision `{sup}`.")
        if dec.superseded_by and dec.superseded_by not in graph.decisions:
            emit("unknown_superseded_by", "broken_links_and_ids", dec.doc_path, f"Decision `{dec.id}` superseded_by unknown decision `{dec.superseded_by}`.")

    for ms in graph.milestones.values():
        for dep_m in ms.depends_on:
            if dep_m not in graph.milestones:
                emit("unknown_milestone_dep", "broken_links_and_ids", ms.origin_path, f"Milestone `{ms.id}` depends_on unknown milestone `{dep_m}`.")

    for task in graph.tasks.values():
        if task.milestone and task.milestone not in graph.milestones:
            emit("unknown_milestone", "broken_links_and_ids", task.origin_path, f"Task `{task.id}` references unknown milestone `{task.milestone}`.")
        for sp in task.specs:
            if sp not in graph.modules:
                if graph.is_day_zero_synthetic:
                    emit(
                        "unknown_spec",
                        "unknown_task_specs",
                        task.origin_path,
                        f"Task `{task.id}` references placeholder spec `{sp}` not yet matched to synthesized Day-0 modules.",
                        default_sev="advisory",
                    )
                else:
                    emit("unknown_spec", "unknown_task_specs", task.origin_path, f"Task `{task.id}` references unknown module spec `{sp}`.")
        for did in task.decisions:
            if did not in graph.decisions:
                emit("unknown_decision", "broken_links_and_ids", task.origin_path, f"Task `{task.id}` references unknown decision `{did}`.")
        for sid in task.sources:
            referenced_sources.add(sid)
            if sid not in graph.sources:
                emit("unknown_source", "broken_links_and_ids", task.origin_path, f"Task `{task.id}` references unknown source `{sid}`.")

    # 3. Orphan active sources check
    for sid, src in graph.sources.items():
        if src.status == "active" and sid not in referenced_sources:
            emit(
                "orphan_source",
                "orphan_active_sources",
                src.origin_path,
                f"Active user source `{sid}` is not yet linked to any module spec, ADR, or work task.",
                default_sev="advisory",
            )

    # 4. Markdown relative link & heading fragment resolution (excluding archive/)
    md_files = collect_live_markdown_files(root)
    for rel_md, ln_md, ver in find_hardcoded_versions(root, md_files):
        emit(
            "hardcoded_version",
            "hardcoded_version",
            rel_md,
            f"Copies `discipline_version = \"{ver}\"`; the value lives only in `docs-policy.toml`, so point to that file instead.",
            ln_md,
        )
    slug_cache: dict[Path, set[str]] = {}
    links_cache: dict[Path, list[tuple[str, int]]] = {}
    for mp in md_files:
        txt = mp.read_text(encoding="utf-8")
        _, slugs, links, _ = extract_markdown_structure(txt, mp.relative_to(root).as_posix())
        slug_cache[mp.resolve()] = slugs
        links_cache[mp.resolve()] = links

    for mp, links in links_cache.items():
        rel_mp = mp.relative_to(root).as_posix()
        for raw_target, ln in links:
            if "{{" in raw_target or raw_target.startswith(("http://", "https://", "mailto:", "conversation://", "file://")):
                continue
            parsed = urlsplit(unquote(raw_target))
            target_file = (mp.parent / parsed.path).resolve() if parsed.path else mp
            if not target_file.exists():
                emit("broken_link", "broken_links_and_ids", rel_mp, f"Broken link target `{raw_target}`.", ln)
                continue
            if parsed.fragment and target_file.is_file() and target_file.suffix.lower() == ".md":
                target_slugs = slug_cache.get(target_file)
                if target_slugs is None:
                    _, target_slugs, _, _ = extract_markdown_structure(target_file.read_text(encoding="utf-8"), "")
                if parsed.fragment.lower() not in target_slugs:
                    emit(
                        "broken_fragment",
                        "broken_links_and_ids",
                        rel_mp,
                        f"Heading fragment `#{parsed.fragment}` not found in `{target_file.relative_to(root).as_posix()}`.",
                        ln,
                    )

    # 5. Exclusive code ownership across `source_roots` (skip only raw unconfigured dirs without docs-policy adoption)
    claims_map: dict[str, list[str]] = graph.git_summary.get("file_claims", {})
    adoption_stage = str(graph.policy.get("adoption", {}).get("stage", "")) if "adoption" in graph.policy else ""
    if graph.modules and not graph.is_day_zero_synthetic:
        for f_path, claimants in sorted(claims_map.items()):
            if len(claimants) == 0:
                emit(
                    "unclaimed_source",
                    "source_ownership",
                    f_path,
                    "Governed source file is not claimed by any module spec `owns` pattern in `docs/specs/`.",
                )
            elif len(claimants) > 1:
                emit(
                    "ambiguous_ownership",
                    "source_ownership",
                    f_path,
                    f"Source file is claimed by multiple module specs: {', '.join(claimants)}.",
                )
    elif graph.is_day_zero_synthetic and graph.files and adoption_stage in ("observed", "scoped_enforcement", "adopted"):
        emit(
            "unclaimed_source",
            "source_ownership",
            "docs/specs",
            "Governed source files exist with zero formal module specs in `docs/specs/`; add module specs before switching `[adoption].stage` to `\"adopted\"`.",
        )

    # 6. Static import boundaries + `architecture-rules.toml`
    if not graph.is_day_zero_synthetic:
        for edge in graph.import_edges:
            if not edge.allowed:
                allowed_list = list(graph.modules[edge.source_module].depends_on) if edge.source_module in graph.modules else []
                emit(
                    "undeclared_import",
                    "import_boundaries",
                    edge.source_file,
                    f"Module `{edge.source_module}` imports `{edge.target_module}` (`{edge.target_ref}`), outside declared `depends_on={allowed_list}`.",
                    edge.line,
                )
    _check_architecture_rules_manifest(root, graph.files, emit)

    # 7. File/style size budgets, role headers on claimed files, & catch-all directory ban
    budgets = graph.policy.get("budgets", {})
    max_src = int(budgets.get("max_source_lines", 500))
    max_css = int(budgets.get("max_style_lines", 300))
    banned_dirs = {str(d).lower() for d in budgets.get("forbid_catchall_dirs", ["utils", "helpers", "common", "misc"])}

    for fs in graph.files:
        limit = max_css if fs.is_style else max_src
        if fs.lines > limit:
            emit("file_size_budget", "file_size_budget", fs.path, f"File has {fs.lines} lines (budget {limit}); split by cohesive responsibility.")
        if fs.owner_module and not graph.is_day_zero_synthetic and not fs.has_role_header:
            emit(
                "missing_role_header",
                "missing_role_header",
                fs.path,
                "Claimed source/style file is missing a top-of-file Role header comment.",
                default_sev="error",
            )
        dir_parts = {p.lower() for p in Path(fs.path).parts[:-1]}
        hit_banned = sorted(dir_parts & banned_dirs)
        if hit_banned:
            emit("catchall_directory", "catchall_directories", fs.path, f"Catch-all directory name `{hit_banned[0]}` is disallowed; name packages by capability.")

    # 8. Plain-language, coined-jargon, disclaimer-chain, project-language, placeholder & spec structure checks
    check_plain_language(root, md_files, graph.files, emit, graph.policy)
    check_spec_structure(graph, emit)

    # 9. Git commit lag advisory (remains non-blocking under --strict unless policy explicitly sets error)
    configured_lag_sev = str(graph.policy.get("severity", {}).get("git_doc_lag", "advisory"))
    for mod_id, tel in graph.module_telemetry.items():
        if tel.git_doc_lag_commits >= 3:
            spec = graph.modules[mod_id]
            emit(
                "git_doc_lag",
                "git_doc_lag",
                spec.doc_path,
                f"Source files owned by `{mod_id}` have {tel.git_doc_lag_commits} commits since `{spec.doc_path}` was last updated.",
                default_sev="advisory",
                strict_exempt=(configured_lag_sev != "error"),
            )

    nudges = build_diff_context_nudges(graph, diff_base=diff_base)
    return findings, nudges


def _check_architecture_rules_manifest(root: Path, files: tuple[Any, ...], emit: Any) -> None:
    manifest_path = root / "architecture-rules.toml"
    if not manifest_path.is_file():
        return
    try:
        manifest = tomllib.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError) as exc:
        emit("arch_manifest", "import_boundaries", "architecture-rules.toml", f"Invalid TOML: {exc}")
        return
    if manifest.get("status") != "configured":
        return
    for rule in manifest.get("rules", []):
        rid = str(rule.get("id", "arch-rule"))
        includes = [str(p) for p in rule.get("include", [])]
        excludes = [str(p) for p in rule.get("exclude", [])]
        forbidden = [str(p) for p in rule.get("forbidden_patterns", [])]
        for fs in files:
            if not any(fnmatch(fs.path, pat) for pat in includes):
                continue
            if any(fnmatch(fs.path, pat) for pat in excludes):
                continue
            try:
                text = (root / fs.path).read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue
            for ln, raw_line in enumerate(text.splitlines(), 1):
                if raw_line.lstrip().startswith("#"):
                    continue
                for pat in forbidden:
                    if pat in raw_line:
                        emit(rid, "import_boundaries", fs.path, f"Forbidden pattern `{pat}` violates architecture rule `{rid}`.", ln)


def build_diff_context_nudges(graph: ProjectGraph, diff_base: str | None = None) -> dict[str, Any]:
    """Build active context reminders (verbatim quotes + promises + review counter) from current git changes."""
    root = Path(graph.root_dir)
    changed = get_working_changed_files(root, diff_base=diff_base)
    touched_mods: set[str] = set()
    touched_docs = False
    for path in changed:
        if Path(path).suffix.lower() in {".md", ".html", ".js", ".jsx", ".ts", ".tsx", ".vue", ".svelte"}:
            touched_docs = True
        mod_id = match_path_to_module(path, graph.modules)
        if mod_id:
            touched_mods.add(mod_id)

    module_reminders: list[dict[str, Any]] = []
    for mod_id in sorted(touched_mods):
        spec = graph.modules[mod_id]
        direct_ids, via_refs = module_source_refs(graph, spec)
        quotes = []
        for sid in direct_ids[:3]:
            if sid in graph.sources:
                excerpt = " ".join(graph.sources[sid].quote.splitlines()).strip()
                quotes.append({"id": sid, "excerpt": excerpt[:120] + ("…" if len(excerpt) > 120 else "")})
        module_reminders.append(
            {
                "module": mod_id,
                "stage": spec.stage,
                "spec_path": spec.doc_path,
                "promise": spec.promise,
                "sources": quotes,
                "more_direct_sources": [sid for sid in direct_ids[3:] if sid in graph.sources],
                "decision_sources": [{"id": sid, "decision": did} for sid, did in via_refs if sid in graph.sources],
            }
        )

    collab = graph.policy.get("collaboration", {})
    cadence_c = int(collab.get("grill_cadence_commits", 12))
    cadence_m = int(collab.get("grill_cadence_modules", 4))
    commits_since = int(graph.git_summary.get("commits_since_review", 0))
    mods_since = list(graph.git_summary.get("modules_since_review", []))
    grill_due = commits_since >= cadence_c or len(mods_since) >= cadence_m

    return {
        "changed_files_count": len(changed),
        "touched_docs": touched_docs,
        "touched_modules": module_reminders,
        "commits_since_review": commits_since,
        "modules_since_review": mods_since,
        "grill_suggested": grill_due,
        "grill_thresholds": {"commits": cadence_c, "modules": cadence_m},
    }
