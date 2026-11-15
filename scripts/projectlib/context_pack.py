# Role: Builds progressive context packs for files, docs, modules, directories, and exact bidirectional traces.
# Out of scope: HTTP socket handling, TOML mutation, or direct subprocess calls.
# Anchors: spec=perspective.context-pack, ADR-002, SRC-004, SRC-005, SRC-007, SRC-010

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .git_telemetry import match_path_to_module
from .model import ProjectGraph, WorkTask

_DESIGN_HTML_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)#\s]+\.html)(?:#[^)]*)?\)|`?(docs/design/[A-Za-z0-9_./-]+\.html)`?")


def select_primary_task_spec(graph: ProjectGraph, task: WorkTask) -> str | None:
    """Choose the primary module spec for a task, preferring pending surface-specs on blocked UI work."""
    known = [sp for sp in task.specs if sp in graph.modules]
    if not known:
        return None
    if task.state == "blocked":
        for sp in known:
            mod = graph.modules[sp]
            if mod.kind == "surface-spec" or mod.doc_path.startswith("docs/design/"):
                return sp
    ms = graph.milestones.get(task.milestone)
    if ms and ms.domain:
        for sp in known:
            if graph.modules[sp].domain == ms.domain:
                return sp
    return known[0]


def collect_task_design_docs(graph: ProjectGraph, task: WorkTask) -> list[str]:
    """Collect surface/design spec docs and linked interactive HTML drafts for a task."""
    root = Path(graph.root_dir)
    docs_out: list[str] = []

    def _add(rel_p: str) -> None:
        if rel_p and rel_p not in docs_out and (root / rel_p).is_file():
            docs_out.append(rel_p)

    for sp in task.specs:
        mod = graph.modules.get(sp)
        if not mod:
            continue
        is_design = mod.kind == "surface-spec" or mod.doc_path.startswith("docs/design/")
        if is_design:
            _add(mod.doc_path)
            doc_dir = (root / mod.doc_path).parent
            for m in _DESIGN_HTML_LINK_RE.finditer(mod.body_markdown):
                link_ref = m.group(1) or m.group(2) or ""
                if not link_ref or link_ref.startswith(("http://", "https://")):
                    continue
                cand = (root / link_ref).resolve() if link_ref.startswith("docs/") else (doc_dir / link_ref).resolve()
                if cand.is_file() and cand.is_relative_to(root.resolve()):
                    _add(cand.relative_to(root).as_posix())
    return docs_out


def build_context_pack(graph: ProjectGraph, target: str) -> dict[str, Any]:
    """Resolve a path, doc, dir, module ID, domain ID, SRC-*, ADR-*, or task ID."""
    target = target.strip()
    clean_path = target.lstrip("./").rstrip("/")
    mod_id: str | None = None
    dom_id: str | None = None
    focus_kind = "module"
    matched_doc = next((d for d in graph.repo_docs if d.path == clean_path), None)
    matched_dir = next((de for de in graph.directory_map if de.path == (clean_path or "(root)")), None)
    t_obj = graph.tasks.get(target)

    if target in graph.modules:
        mod_id = target
        dom_id = graph.modules[mod_id].domain
    elif target in graph.domains:
        dom_id = target
        focus_kind = "domain"
    elif target in graph.sources:
        focus_kind = "source"
    elif target in graph.decisions:
        focus_kind = "decision"
    elif t_obj is not None:
        focus_kind = "task"
        mod_id = select_primary_task_spec(graph, t_obj)
        dom_id = graph.modules[mod_id].domain if mod_id and mod_id in graph.modules else None
        if not dom_id and t_obj.milestone in graph.milestones:
            dom_id = graph.milestones[t_obj.milestone].domain
    else:
        matched = match_path_to_module(clean_path, graph.modules)
        if matched:
            mod_id = matched
            dom_id = graph.modules[mod_id].domain
            focus_kind = "document" if matched_doc else "file"
        elif matched_doc:
            focus_kind = "document"
        elif matched_dir:
            focus_kind = "directory"

    if focus_kind in ("source", "decision"):
        return build_lineage_trace(graph, target)

    doc_payload = (
        {
            "path": matched_doc.path,
            "title": matched_doc.title,
            "category": matched_doc.category,
            "summary": matched_doc.summary,
            "line_count": matched_doc.line_count,
            "body_markdown": matched_doc.body_markdown,
        }
        if matched_doc
        else None
    )
    task_payload = (
        {
            "id": t_obj.id,
            "title": t_obj.title,
            "milestone": t_obj.milestone,
            "state": t_obj.state,
            "human_check": t_obj.human_check,
            "specs": list(t_obj.specs),
            "sources": list(t_obj.sources),
            "decisions": list(t_obj.decisions),
            "blocker_question": t_obj.blocker_question,
            "blocker_options": list(t_obj.blocker_options),
            "selected_option": t_obj.selected_option,
            "design_docs": collect_task_design_docs(graph, t_obj),
        }
        if focus_kind == "task" and t_obj is not None
        else None
    )

    if mod_id and mod_id in graph.modules:
        spec = graph.modules[mod_id]
        dom = graph.domains.get(spec.domain)
        tel = graph.module_telemetry.get(mod_id)
        if task_payload and t_obj is not None:
            src_ids = list(t_obj.sources)
            for sid in spec.sources:
                if sid not in src_ids:
                    src_ids.append(sid)
        else:
            src_ids = list(spec.sources)
        quotes = [
            {"id": sid, "date": graph.sources[sid].date, "context": graph.sources[sid].context, "quote": graph.sources[sid].quote}
            for sid in src_ids
            if sid in graph.sources
        ]
        dec_ids_task = set(t_obj.decisions) if task_payload and t_obj is not None else set()
        adrs = [
            {
                "id": d.id,
                "status": d.status,
                "title": d.title,
                "supersedes": list(d.supersedes),
                "superseded_by": d.superseded_by,
                "doc_path": d.doc_path,
            }
            for d in graph.decisions.values()
            if mod_id in d.affects or spec.domain in d.affects or d.id in dec_ids_task
        ]
        tasks = [
            {
                "id": t.id,
                "milestone": t.milestone,
                "title": t.title,
                "state": t.state,
                "human_check": t.human_check,
                "blocker_question": t.blocker_question,
            }
            for t in graph.tasks.values()
            if mod_id in t.specs and not t.archived
        ]
        owned_files = [
            {"path": f.path, "lines": f.lines, "has_role_header": f.has_role_header}
            for f in graph.files
            if f.owner_module == mod_id
        ]
        violations = [
            {"file": e.source_file, "line": e.line, "target_module": e.target_module, "ref": e.target_ref}
            for e in graph.import_edges
            if e.source_module == mod_id and not e.allowed
        ]
        used_by = sorted(m.id for m in graph.modules.values() if mod_id in m.depends_on)
        result: dict[str, Any] = {
            "found": True,
            "query": target,
            "focus_kind": focus_kind,
            "domain": {
                "id": spec.domain,
                "name": dom.name if dom else spec.domain,
                "stage": dom.stage if dom else spec.stage,
                "promise": dom.promise if dom else "",
            },
            "module": {
                "id": spec.id,
                "title": spec.title,
                "stage": spec.stage,
                "summary": spec.summary,
                "promise": spec.promise,
                "doc_path": spec.doc_path,
                "owns": list(spec.owns),
                "depends_on": list(spec.depends_on),
                "used_by": used_by,
                "body_markdown": spec.body_markdown,
            },
            "verbatim_sources": quotes,
            "decisions": adrs,
            "active_tasks": tasks,
            "telemetry": {
                "file_count": tel.file_count if tel else 0,
                "total_loc": tel.total_loc if tel else 0,
                "max_file_path": tel.max_file_path if tel else "",
                "max_file_loc": tel.max_file_loc if tel else 0,
                "git_doc_lag_commits": tel.git_doc_lag_commits if tel else 0,
                "recent_commits": tel.recent_commits if tel else 0,
                "import_violations": violations,
                "files": owned_files,
            },
        }
        if doc_payload:
            result["document"] = doc_payload
        if task_payload:
            result["task"] = task_payload
        return result

    if task_payload:
        task_quotes = [
            {"id": sid, "date": graph.sources[sid].date, "context": graph.sources[sid].context, "quote": graph.sources[sid].quote}
            for sid in task_payload["sources"]
            if sid in graph.sources
        ]
        task_decs = [
            {
                "id": did,
                "status": graph.decisions[did].status,
                "title": graph.decisions[did].title,
                "supersedes": list(graph.decisions[did].supersedes),
                "superseded_by": graph.decisions[did].superseded_by,
                "doc_path": graph.decisions[did].doc_path,
            }
            for did in task_payload["decisions"]
            if did in graph.decisions
        ]
        return {
            "found": True,
            "query": target,
            "focus_kind": focus_kind,
            "task": task_payload,
            "domain": {"id": dom_id, "name": graph.domains[dom_id].name} if dom_id and dom_id in graph.domains else {},
            "verbatim_sources": task_quotes,
            "decisions": task_decs,
        }

    if matched_doc:
        return {
            "found": True,
            "query": target,
            "focus_kind": "document",
            "document": doc_payload,
            "domain": {"id": matched_doc.domain, "name": graph.domains[matched_doc.domain].name} if matched_doc.domain in graph.domains else {},
        }

    if matched_dir:
        return {
            "found": True,
            "query": target,
            "focus_kind": "directory",
            "directory": {
                "path": matched_dir.path,
                "label_en": matched_dir.label_en,
                "label_zh": matched_dir.label_zh,
                "summary_en": matched_dir.summary_en,
                "summary_zh": matched_dir.summary_zh,
                "file_count": matched_dir.file_count,
                "doc_count": matched_dir.doc_count,
                "total_lines": matched_dir.total_lines,
                "doc_paths": list(matched_dir.doc_paths),
            },
        }

    if dom_id and dom_id in graph.domains:
        dom = graph.domains[dom_id]
        mods = [m.id for m in graph.modules.values() if m.domain == dom_id]
        return {
            "found": True,
            "query": target,
            "focus_kind": "domain",
            "domain": {
                "id": dom.id,
                "name": dom.name,
                "stage": dom.stage,
                "summary": dom.summary,
                "promise": dom.promise,
                "doc_path": dom.doc_path,
                "modules": mods,
            },
        }

    return {"found": False, "query": target, "message": f"No module, domain, document, source, decision, or task matched `{target}`."}


build_context_capsule = build_context_pack


def build_lineage_trace(graph: ProjectGraph, node_id: str) -> dict[str, Any]:
    """Compute bidirectional traceability (`Source <-> Decision/Spec <-> Tasks/Code`)."""
    node_id = node_id.strip()
    if node_id in graph.sources:
        src = graph.sources[node_id]
        specs = [m for m in graph.modules.values() if node_id in m.sources]
        decs = [d for d in graph.decisions.values() if node_id in d.sources]
        tasks = [
            t
            for t in graph.tasks.values()
            if node_id in t.sources
        ]
        done_tasks = [t for t in tasks if t.state == "done" and t.human_check in ("approved", "not_required")]
        open_tasks = [t for t in tasks if t not in done_tasks]
        return {
            "found": True,
            "anchor_type": "source",
            "id": src.id,
            "title": src.context or src.id,
            "date": src.date,
            "status": src.status,
            "quote": src.quote,
            "decisions": [
                {"id": d.id, "title": d.title, "status": d.status, "supersedes": list(d.supersedes), "superseded_by": d.superseded_by, "doc_path": d.doc_path}
                for d in decs
            ],
            "modules": [
                {"id": m.id, "domain": m.domain, "stage": m.stage, "title": m.title, "promise": m.promise, "doc_path": m.doc_path}
                for m in specs
            ],
            "verified_done_count": len(done_tasks),
            "verified_done_tasks": [
                {"id": t.id, "title": t.title, "milestone": t.milestone, "specs": list(t.specs)}
                for t in done_tasks
            ],
            "open_or_pending_tasks": [
                {
                    "id": t.id,
                    "title": t.title,
                    "milestone": t.milestone,
                    "state": t.state,
                    "human_check": t.human_check,
                    "blocker_question": t.blocker_question,
                    "specs": list(t.specs),
                }
                for t in open_tasks
            ],
        }

    if node_id in graph.decisions:
        dec = graph.decisions[node_id]
        upstream = [
            {"id": s, "date": graph.sources[s].date, "context": graph.sources[s].context, "quote": graph.sources[s].quote}
            for s in dec.sources
            if s in graph.sources
        ]
        affected_mods = [
            m for m in graph.modules.values() if m.id in dec.affects or m.domain in dec.affects
        ]
        affected_ids = {m.id for m in affected_mods} | set(dec.affects)
        tasks = [
            t
            for t in graph.tasks.values()
            if node_id in t.decisions
            or (
                dec.status != "superseded"
                and not t.archived
                and not t.decisions
                and bool(affected_ids & set(t.specs))
            )
        ]
        done_tasks = [t for t in tasks if t.state == "done" and t.human_check in ("approved", "not_required")]
        open_tasks = [t for t in tasks if t not in done_tasks]
        return {
            "found": True,
            "anchor_type": "decision",
            "id": dec.id,
            "title": dec.title,
            "status": dec.status,
            "supersedes": list(dec.supersedes),
            "superseded_by": dec.superseded_by,
            "doc_path": dec.doc_path,
            "body_markdown": dec.body_markdown,
            "sources": upstream,
            "affects": list(dec.affects),
            "modules": [
                {"id": m.id, "domain": m.domain, "stage": m.stage, "title": m.title, "promise": m.promise, "doc_path": m.doc_path}
                for m in affected_mods
            ],
            "verified_done_count": len(done_tasks),
            "verified_done_tasks": [
                {"id": t.id, "title": t.title, "milestone": t.milestone, "specs": list(t.specs)}
                for t in done_tasks
            ],
            "open_or_pending_tasks": [
                {
                    "id": t.id,
                    "title": t.title,
                    "milestone": t.milestone,
                    "state": t.state,
                    "human_check": t.human_check,
                    "specs": list(t.specs),
                }
                for t in open_tasks
            ],
        }

    if node_id in graph.modules:
        pack = build_context_pack(graph, node_id)
        pack["anchor_type"] = "module"
        return pack

    return {"found": False, "id": node_id, "message": f"Unknown lineage node `{node_id}`."}
