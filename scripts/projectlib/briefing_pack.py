# Role: Serializes the full stitched ProjectGraph into the JSON payload for CLI status and the local Web UI.
# Out of scope: HTTP socket serving, TOML mutation, or direct subprocess calls.
# Anchors: spec=perspective.context-pack, ADR-002, SRC-005, SRC-007, SRC-008, SRC-010

from __future__ import annotations

from pathlib import Path
from typing import Any

from .context_pack import build_context_pack, build_lineage_trace, collect_task_design_docs, select_primary_task_spec
from .git_telemetry import compare_git_refs, match_path_to_module
from .model import ProjectGraph
from .validator import validate_project_graph


def serialize_perspective_payload(graph: ProjectGraph, *, csrf_token: str = "") -> dict[str, Any]:
    """Build the complete JSON model consumed by `project.py status` and `scripts/projectlib/web/`."""
    findings, nudges = validate_project_graph(graph)
    total_loc = sum(f.lines for f in graph.files)
    total_doc_loc = sum(d.line_count for d in graph.repo_docs)

    # Blocked decisions & awaiting human verification inboxes
    blocked_inbox: list[dict[str, Any]] = []
    ready_inbox: list[dict[str, Any]] = []
    for t in graph.tasks.values():
        if t.archived:
            continue
        ms = graph.milestones.get(t.milestone)
        primary_spec_id = select_primary_task_spec(graph, t)
        mod = graph.modules.get(primary_spec_id) if primary_spec_id else None
        dom_id = ms.domain if ms else (mod.domain if mod else "core")
        dom = graph.domains.get(dom_id)
        src = graph.sources.get(t.sources[0]) if t.sources else None
        design_docs = collect_task_design_docs(graph, t)
        base_entry = {
            "task_id": t.id,
            "milestone_id": t.milestone,
            "title": t.title,
            "domain_id": dom_id,
            "domain_name": dom.name if dom else dom_id,
            "module_id": mod.id if mod else "",
            "specs": list(t.specs),
            "sources": list(t.sources),
            "design_docs": design_docs,
            "promise": (mod.promise if mod and mod.promise else (dom.promise if dom else "")),
            "source_id": src.id if src else "",
            "source_date": src.date if src else "",
            "source_quote": src.quote if src else "",
        }
        if t.state == "blocked":
            blocked_inbox.append(
                {
                    **base_entry,
                    "blocker_question": t.blocker_question or t.title,
                    "blocker_options": list(t.blocker_options),
                }
            )
        elif t.state == "ready_for_check" and t.human_check == "pending":
            ready_inbox.append(base_entry)

    # Cross-domain edges (declared `depends_on` + static import violations)
    dom_declared_pairs: dict[tuple[str, str], list[str]] = {}
    dom_violation_pairs: dict[tuple[str, str], list[str]] = {}

    for m in graph.modules.values():
        for dep in m.depends_on:
            if dep in graph.modules:
                target_dom = graph.modules[dep].domain
                if target_dom != m.domain:
                    dom_declared_pairs.setdefault((m.domain, target_dom), []).append(f"{m.id} -> {dep}")

    for e in graph.import_edges:
        if not e.allowed and e.source_module in graph.modules and e.target_module in graph.modules:
            s_dom = graph.modules[e.source_module].domain
            t_dom = graph.modules[e.target_module].domain
            dom_violation_pairs.setdefault((s_dom, t_dom), []).append(f"{e.source_file}:{e.line}")

    domain_edges: list[dict[str, Any]] = [
        {"from": src_d, "to": dst_d, "kind": "declared", "count": len(items), "examples": items[:3]}
        for (src_d, dst_d), items in sorted(dom_declared_pairs.items())
    ] + [
        {"from": src_d, "to": dst_d, "kind": "violation", "count": len(items), "examples": items[:3]}
        for (src_d, dst_d), items in sorted(dom_violation_pairs.items())
    ]

    # Per-domain views & intra-domain module edges
    domains_out: list[dict[str, Any]] = []
    warn_domains: set[str] = set()

    for dom_id, dom in graph.domains.items():
        dom_mods = [m for m in graph.modules.values() if m.domain == dom_id]
        dom_ms = [m for m in graph.milestones.values() if m.domain == dom_id]
        done_ms = [m for m in dom_ms if m.slot == "done"]
        now_ms = [m for m in dom_ms if m.slot == "now"]
        next_ms = [m for m in dom_ms if m.slot == "next"]
        later_ms = [m for m in dom_ms if m.slot == "later"]

        dom_loc = sum(graph.module_telemetry[m.id].total_loc for m in dom_mods if m.id in graph.module_telemetry)
        oversized_n = sum(len(graph.module_telemetry[m.id].oversized_files) for m in dom_mods if m.id in graph.module_telemetry)
        dom_mod_ids = {m.id for m in dom_mods}
        illegal_out = [
            {
                "source_file": e.source_file,
                "source_module": e.source_module,
                "target_module": e.target_module,
                "target_domain": graph.modules[e.target_module].domain if e.target_module in graph.modules else "",
                "line": e.line,
                "ref": e.target_ref,
            }
            for e in graph.import_edges
            if e.source_module in dom_mod_ids and not e.allowed
        ]
        legal_target_domains = sorted(
            {
                graph.modules[dep].domain
                for m in dom_mods
                for dep in m.depends_on
                if dep in graph.modules and graph.modules[dep].domain != dom_id
            }
        )
        if oversized_n > 0 or illegal_out:
            warn_domains.add(dom_id)

        module_edges: list[dict[str, Any]] = []
        for m in dom_mods:
            for dep in m.depends_on:
                module_edges.append(
                    {
                        "from": m.id,
                        "to": dep,
                        "kind": "declared",
                        "external": bool(dep in graph.modules and graph.modules[dep].domain != dom_id),
                    }
                )
        for v in illegal_out:
            module_edges.append(
                {
                    "from": v["source_module"],
                    "to": v["target_module"],
                    "kind": "violation",
                    "external": bool(v["target_domain"] and v["target_domain"] != dom_id),
                    "file": v["source_file"],
                    "line": v["line"],
                }
            )

        def _ms_card(m_obj: Any) -> dict[str, Any]:
            m_tasks = [tk for tk in graph.tasks.values() if tk.milestone == m_obj.id]
            done_c = sum(1 for tk in m_tasks if tk.state == "done")
            blocked_c = sum(1 for tk in m_tasks if tk.state == "blocked")
            ready_c = sum(1 for tk in m_tasks if tk.state == "ready_for_check")
            active_c = sum(1 for tk in m_tasks if tk.state == "active")
            todo_c = sum(1 for tk in m_tasks if tk.state == "todo")
            task_ids = {tk.id for tk in m_tasks}
            children_map: dict[str, list[Any]] = {}
            roots: list[Any] = []
            for tk in m_tasks:
                if tk.parent and tk.parent in task_ids and tk.parent != tk.id:
                    children_map.setdefault(tk.parent, []).append(tk)
                else:
                    roots.append(tk)
            ordered_tasks: list[tuple[Any, int]] = []
            visited_tids: set[str] = set()

            def _walk_task(node: Any, depth: int) -> None:
                if node.id in visited_tids:
                    return
                visited_tids.add(node.id)
                ordered_tasks.append((node, depth))
                for child in children_map.get(node.id, []):
                    _walk_task(child, min(4, depth + 1))

            for root_tk in roots:
                _walk_task(root_tk, 2)
            for tk in m_tasks:
                if tk.id not in visited_tids:
                    _walk_task(tk, 2)

            cross_deps = [
                {"id": dep_id, "name": graph.milestones[dep_id].name, "domain": graph.milestones[dep_id].domain}
                for dep_id in m_obj.depends_on
                if dep_id in graph.milestones and graph.milestones[dep_id].slot != "done"
            ]

            def _task_card(tk: Any, depth: int) -> dict[str, Any]:
                return {
                    "id": tk.id,
                    "title": tk.title,
                    "state": tk.state,
                    "human_check": tk.human_check,
                    "parent": tk.parent,
                    "depth": depth,
                    "specs": list(tk.specs),
                    "sources": list(tk.sources),
                    "decisions": list(tk.decisions),
                    "design_docs": collect_task_design_docs(graph, tk),
                    "blocker_question": tk.blocker_question,
                    "blocker_options": list(tk.blocker_options),
                    "selected_option": tk.selected_option,
                    "archived": tk.archived,
                }

            return {
                "id": m_obj.id,
                "name": m_obj.name,
                "era": m_obj.era,
                "slot": m_obj.slot,
                "archived": m_obj.archived,
                "done_tasks": done_c,
                "ready_tasks": ready_c,
                "blocked_tasks": blocked_c,
                "active_tasks": active_c,
                "todo_tasks": todo_c,
                "total_tasks": len(m_tasks),
                "cross_deps": cross_deps,
                "tasks": [_task_card(tk, depth) for tk, depth in ordered_tasks],
            }

        budgets_cfg = graph.policy.get("budgets", {})
        max_src_cap = int(budgets_cfg.get("max_source_lines", 500))
        modules_cards = []
        for m in dom_mods:
            tel = graph.module_telemetry.get(m.id)
            m_tasks = [tk for tk in graph.tasks.values() if m.id in tk.specs and not tk.archived]
            m_viols = [v for v in illegal_out if v["source_module"] == m.id]
            m_docs = [d for d in graph.repo_docs if d.owner_module == m.id]
            modules_cards.append(
                {
                    "id": m.id,
                    "kind": m.kind,
                    "title": m.title,
                    "stage": m.stage,
                    "summary": m.summary,
                    "promise": m.promise,
                    "doc_path": m.doc_path,
                    "depends_on": list(m.depends_on),
                    "sources": list(m.sources),
                    "loc": tel.total_loc if tel else 0,
                    "max_loc": max_src_cap,
                    "file_count": tel.file_count if tel else 0,
                    "doc_count": len(m_docs),
                    "doc_loc": sum(d.line_count for d in m_docs),
                    "max_file_path": tel.max_file_path if tel else "",
                    "max_file_loc": tel.max_file_loc if tel else 0,
                    "oversized_count": len(tel.oversized_files) if tel else 0,
                    "violation_count": len(m_viols),
                    "git_lag": tel.git_doc_lag_commits if tel else 0,
                    "recent_commits": tel.recent_commits if tel else 0,
                    "tasks": [
                        {
                            "id": tk.id,
                            "title": tk.title,
                            "state": tk.state,
                            "human_check": tk.human_check,
                            "specs": list(tk.specs),
                            "sources": list(tk.sources),
                            "decisions": list(tk.decisions),
                            "design_docs": collect_task_design_docs(graph, tk),
                            "blocker_question": tk.blocker_question,
                            "blocker_options": list(tk.blocker_options),
                            "selected_option": tk.selected_option,
                        }
                        for tk in m_tasks
                    ],
                }
            )

        is_calm = oversized_n == 0 and len(illegal_out) == 0
        dom_mod_ids = {m.id for m in dom_mods}
        dom_docs = [d for d in graph.repo_docs if d.domain == dom_id or d.owner_module in dom_mod_ids]
        dom_ms_ids = {m.id for m in dom_ms}
        dom_tasks = [tk for tk in graph.tasks.values() if tk.milestone in dom_ms_ids]
        dom_sources = sorted(
            {sid for m in dom_mods for sid in m.sources}
            | {sid for tk in dom_tasks for sid in tk.sources}
        )
        dom_decisions = sorted(
            {d.id for d in graph.decisions.values() if any(aid in dom_mod_ids for aid in d.affects)}
            | {did for tk in dom_tasks for did in tk.decisions}
        )
        domains_out.append(
            {
                "id": dom_id,
                "name": dom.name,
                "stage": dom.stage,
                "summary": dom.summary,
                "promise": dom.promise,
                "non_goals": dom.non_goals,
                "sources": dom_sources,
                "decisions": dom_decisions,
                "doc_path": dom.doc_path,
                "body_markdown": dom.body_markdown,
                "is_exemplar": any(p.startswith("examples/") for m in dom_mods for p in m.owns),
                "loc": dom_loc,
                "doc_count": len(dom_docs),
                "doc_loc": sum(d.line_count for d in dom_docs),
                "module_count": len(dom_mods),
                "oversized_count": oversized_n,
                "violations": illegal_out,
                "depends_on_domains": legal_target_domains,
                "module_edges": module_edges,
                "is_calm": is_calm,
                "done_milestones": [_ms_card(x) for x in done_ms],
                "now_milestones": [_ms_card(x) for x in now_ms],
                "next_milestones": [_ms_card(x) for x in next_ms],
                "later_milestones": [_ms_card(x) for x in later_ms],
                "modules": modules_cards,
                "mermaids": [
                    {"title": d.title, "code": d.code, "source": d.source_path}
                    for d in (list(dom.mermaid_blocks) + [blk for m in dom_mods for blk in m.mermaid_blocks])
                ],
            }
        )

    archived_ms = [m for m in graph.milestones.values() if m.slot == "done"]
    pivots = [
        {
            "id": d.id,
            "title": d.title,
            "status": d.status,
            "supersedes": list(d.supersedes),
            "superseded_by": d.superseded_by,
            "affects": list(d.affects),
            "sources": list(d.sources),
        }
        for d in sorted(graph.decisions.values(), key=lambda x: x.id)
    ]

    provenance_nodes = [
        {
            "id": s.id,
            "kind": "source",
            "label": f"{s.id} · {s.context or s.quote[:36]}",
            "trace": build_lineage_trace(graph, s.id),
        }
        for s in graph.sources.values()
    ] + [
        {
            "id": d.id,
            "kind": "decision",
            "label": f"{d.id} · {d.title}",
            "trace": build_lineage_trace(graph, d.id),
        }
        for d in sorted(graph.decisions.values(), key=lambda x: x.id)
    ]

    capsules = {m_id: build_context_pack(graph, m_id) for m_id in graph.modules}
    policy_anchor = str(graph.policy.get("collaboration", {}).get("review_anchor_sha", "")).strip()
    effective_anchor = str(graph.runtime_state.get("last_review_sha", "") or policy_anchor)

    proj_cfg = graph.policy.get("project", {})
    raw_lang = str(proj_cfg.get("language", "en")).strip().lower() or "en"
    web_default_lang = "zh" if (graph.identity == "template" and "language" not in proj_cfg) else raw_lang
    top_budgets = graph.policy.get("budgets", {})
    doc_owner_dom = {d.path: (d.domain, d.owner_module) for d in graph.repo_docs}

    def _finding_row(f: Any) -> dict[str, Any]:
        f_mod = match_path_to_module(f.path, graph.modules) or doc_owner_dom.get(f.path, ("", ""))[1]
        f_dom = graph.modules[f_mod].domain if f_mod in graph.modules else doc_owner_dom.get(f.path, ("", ""))[0]
        return {
            "rule_id": f.rule_id,
            "severity": f.severity,
            "path": f.path,
            "line": f.line,
            "message": f.message,
            "module": f_mod,
            "domain": f_dom,
        }

    return {
        "csrf_token": csrf_token,
        "project": {
            "id": graph.system_id,
            "name": graph.project_name,
            "identity": graph.identity,
            "language": raw_lang,
            "web_default_lang": web_default_lang,
            "is_day_zero": graph.is_day_zero_synthetic,
            "one_liner": graph.one_liner,
            "architecture_markdown": graph.architecture_markdown,
            "stage": graph.default_stage,
            "discipline_version": graph.discipline_version,
            "max_source_lines": int(top_budgets.get("max_source_lines", 500)),
            "max_style_lines": int(top_budgets.get("max_style_lines", 300)),
            "total_loc": total_loc,
            "total_files": len(graph.files),
            "doc_count": len(graph.repo_docs),
            "doc_loc": total_doc_loc,
            "dir_count": len(graph.directory_map),
            "domain_count": len(domains_out),
            "milestone_count": len(graph.milestones),
            "warn_domain_count": len(warn_domains),
            "stale_domains": graph.git_summary.get("stale_domains", []),
            "head_sha": graph.git_summary.get("head_sha", ""),
            "recent_refs": graph.git_summary.get("recent_refs", []),
            "recent_commits": graph.git_summary.get("recent_commits", []),
        },
        "review": {
            "mode": graph.policy.get("collaboration", {}).get("mode", "interactive"),
            "commits_since_review": nudges["commits_since_review"],
            "modules_since_review": nudges["modules_since_review"],
            "grill_suggested": nudges["grill_suggested"],
            "last_review_sha": effective_anchor,
        },
        "test_run": graph.runtime_state.get("last_test_run", {}),
        "blocked_inbox": blocked_inbox,
        "ready_inbox": ready_inbox,
        "directory_map": [
            {
                "path": de.path,
                "label_zh": de.label_zh,
                "label_en": de.label_en,
                "summary_zh": de.summary_zh,
                "summary_en": de.summary_en,
                "file_count": de.file_count,
                "doc_count": de.doc_count,
                "total_lines": de.total_lines,
                "domain": de.domain,
                "doc_paths": list(de.doc_paths),
            }
            for de in graph.directory_map
        ],
        "repo_docs": [
            {
                "path": doc.path,
                "title": doc.title,
                "category": doc.category,
                "summary": doc.summary,
                "body_markdown": doc.body_markdown,
                "line_count": doc.line_count,
                "domain": doc.domain,
                "owner_module": doc.owner_module,
                "mermaids": [{"title": d.title, "code": d.code, "source": d.source_path} for d in doc.mermaid_blocks],
            }
            for doc in graph.repo_docs
        ],
        "domains": domains_out,
        "domain_edges": domain_edges,
        "timeline": {
            "archived_milestones": [
                {"id": m.id, "name": m.name, "domain": m.domain, "era": m.era}
                for m in archived_ms
            ],
            "pivots": pivots,
        },
        "provenance_nodes": provenance_nodes,
        "system_mermaids": [{"title": d.title, "code": d.code, "source": d.source_path} for d in graph.system_mermaid],
        "capsules": capsules,
        "context_packs": capsules,
        "initial_diff": compare_git_refs(Path(graph.root_dir), graph.modules, ""),
        "findings": [_finding_row(f) for f in findings],
    }
