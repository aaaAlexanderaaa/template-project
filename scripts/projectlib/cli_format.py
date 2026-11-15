# Role: Plain-language terminal formatters for `project.py status`, `context`, and `trace`.
# Out of scope: Graph loading, HTTP serving, or TOML file mutations.
# Anchors: spec=perspective.server, ADR-002, SRC-005, SRC-007, SRC-008, SRC-010

from __future__ import annotations

from typing import Any

_STAGE_WORDS_EN = {
    "prototype": "prototype (0->0.1)",
    "usable": "usable (0.1->1)",
    "stable": "stable (1->N)",
}
_STAGE_WORDS_ZH = {
    "prototype": "原型验证期 (0->0.1)",
    "usable": "可用打磨期 (0.1->1)",
    "stable": "稳定维护期 (1->N)",
}
_TASK_STATE_EN = {
    "done": "done",
    "active": "in progress",
    "doing": "in progress",
    "ready_for_check": "ready for sign-off",
    "blocked": "needs decision",
    "todo": "planned",
}
_TASK_STATE_ZH = {
    "done": "已完成",
    "active": "进行中",
    "doing": "进行中",
    "ready_for_check": "待验收签收",
    "blocked": "等待拍板",
    "todo": "已规划",
}
_CHECK_EN = {
    "approved": "approved",
    "pending": "awaiting sign-off",
    "not_required": "no sign-off needed",
    "not_needed": "no sign-off needed",
}
_CHECK_ZH = {
    "approved": "已签收",
    "pending": "待负责人签收",
    "not_required": "无需签收",
    "not_needed": "无需签收",
}
_DEC_STATUS_EN = {"accepted": "active", "active": "active", "current": "active", "superseded": "superseded", "proposed": "proposed"}
_DEC_STATUS_ZH = {"accepted": "有效", "active": "有效", "current": "有效", "superseded": "已被替代", "proposed": "待定"}
_ANCHOR_TYPE_ZH = {"source": "需求原话", "decision": "架构决策"}


def fmt_stage(stage: str, lang: str = "en") -> str:
    """Format a canonical lifecycle stage into plain English or Chinese."""
    tbl = _STAGE_WORDS_ZH if lang == "zh" else _STAGE_WORDS_EN
    return tbl.get(stage, stage)


def _fmt_task_state(state: str, lang: str) -> str:
    return (_TASK_STATE_ZH if lang == "zh" else _TASK_STATE_EN).get(state, state)


def _fmt_check(check: str, lang: str) -> str:
    return (_CHECK_ZH if lang == "zh" else _CHECK_EN).get(check, check)


def _fmt_dec_status(status: str, lang: str) -> str:
    return (_DEC_STATUS_ZH if lang == "zh" else _DEC_STATUS_EN).get(status, status)


def print_status(payload: dict[str, Any], lang: str = "en") -> None:
    """Render concise repository status, blocked decisions, domain progress, and directory map."""
    proj = payload["project"]
    rev = payload["review"]
    eff_lang = str(proj.get("language") or lang).lower()
    is_zh = eff_lang == "zh"
    doc_loc = int(proj.get("doc_loc", 0))

    if is_zh:
        print(
            f"=== {proj['name']} ({fmt_stage(proj['stage'], 'zh')}, 代码={proj['total_loc']}行, "
            f"文档={proj['doc_count']}份/{doc_loc}行, 业务域={proj['domain_count']}个) ==="
        )
    else:
        print(
            f"=== {proj['name']} ({fmt_stage(proj['stage'])}, code={proj['total_loc']} lines, "
            f"docs={proj['doc_count']} ({doc_loc}L), domains={proj['domain_count']}) ==="
        )
    if proj["one_liner"]:
        print(f"  {proj['one_liner']}")

    if payload["blocked_inbox"]:
        hdr = (
            f"\n[待负责人拍板决定 ({len(payload['blocked_inbox'])})]"
            if is_zh
            else f"\n[NEEDS OWNER DECISION ({len(payload['blocked_inbox'])})]"
        )
        print(hdr)
        for b in payload["blocked_inbox"]:
            print(f"  • [{b['domain_name']}] {b['task_id']}: {b['blocker_question']}")
            for idx, opt in enumerate(b.get("blocker_options", []), 1):
                print(f"      {idx}. {opt}")
            if b.get("design_docs"):
                lbl = "设计文档" if is_zh else "Design Docs"
                print(f"      {lbl}: {', '.join(b['design_docs'])}")

    print("\n[各业务域与推进进度]" if is_zh else "\n[Domains & Progress]")
    for d in payload["domains"]:
        done_n = len(d["done_milestones"])
        paused_sfx = " (已暂停等待拍板)" if is_zh else " (paused pending decision)"
        now_parts = [
            f"{m['name']}{paused_sfx if m.get('blocked_tasks', 0) > 0 else ''}"
            for m in d["now_milestones"]
        ]
        now_names = ", ".join(now_parts) or "—"
        next_names = ", ".join(m["name"] for m in d["next_milestones"]) or "—"
        d_docs = int(d.get("doc_count", 0))
        d_dloc = int(d.get("doc_loc", 0))
        if is_zh:
            print(
                f"  • {d['name']} [{fmt_stage(d['stage'], 'zh')}] | 代码={d['loc']}行 | 文档={d_docs}份({d_dloc}行) | "
                f"已归档: {done_n} | 当前: {now_names} | 下一步: {next_names}"
            )
        else:
            print(
                f"  • {d['name']} [{fmt_stage(d['stage'])}] | code={d['loc']}L | docs={d_docs} ({d_dloc}L) | "
                f"Archived: {done_n} | Now: {now_names} | Next: {next_names}"
            )

    dir_map = payload.get("directory_map", [])
    if dir_map:
        print("\n[目录结构总览]" if is_zh else "\n[Directory Overview]")
        for de in dir_map:
            lbl = de.get("label_zh") if is_zh else de.get("label_en")
            sm = de.get("summary_zh") if is_zh else de.get("summary_en")
            if is_zh:
                print(f"  • {de['path']} ({lbl}) — {de['file_count']} 个文件，{de['doc_count']} 份文档：{sm}")
            else:
                print(f"  • {de['path']} ({lbl}) — {de['file_count']} files, {de['doc_count']} docs: {sm}")

    if is_zh:
        tail = " -> 建议触发 `/grill` 质询或独立评审" if rev["grill_suggested"] else " (处于正常评审节奏内)"
        print(
            f"\n[评审累计] 距上次评审基线已累计 +{rev['commits_since_review']} 次提交，涉及 {len(rev['modules_since_review'])} 个模块{tail}"
        )
    else:
        tail = " -> SUGGEST `/grill` or holistic check" if rev["grill_suggested"] else " (within cadence)"
        print(
            f"\n[Review Accumulation] +{rev['commits_since_review']} commits across "
            f"{len(rev['modules_since_review'])} module(s) since last review anchor{tail}"
        )


def print_trace_summary(tr: dict[str, Any], lang: str = "en") -> None:
    """Print bidirectional provenance trace including concrete done and open tasks."""
    is_zh = lang == "zh"
    raw_kind = str(tr.get("anchor_type", ""))
    kind_lbl = _ANCHOR_TYPE_ZH.get(raw_kind, raw_kind) if is_zh else raw_kind
    print(f"=== {'溯源追踪' if is_zh else 'Lineage Trace'} ({kind_lbl}): {tr.get('id')} ===")
    if tr.get("quote"):
        print(f"{'用户原话' if is_zh else 'Quote'}:\n{tr['quote']}\n")
    decs = tr.get("decisions") or []
    if isinstance(decs, list) and decs:
        lbl = "关联决策" if is_zh else "Decisions"
        print(f"{lbl}: ", ", ".join(f"{d['id']} ({_fmt_dec_status(d['status'], lang)})" for d in decs if isinstance(d, dict)))
    srcs = tr.get("sources") or []
    if isinstance(srcs, list) and srcs:
        ids = [s["id"] if isinstance(s, dict) else str(s) for s in srcs]
        print(f"{'来源原话' if is_zh else 'Sources'}:   ", ", ".join(ids))
    mods = tr.get("modules") or []
    if isinstance(mods, list) and mods:
        print(f"{'涉及模块' if is_zh else 'Modules'}:   ", ", ".join(m["id"] for m in mods if isinstance(m, dict)))
    done_list = tr.get("verified_done_tasks") or []
    open_list = tr.get("open_or_pending_tasks") or []
    if is_zh:
        print(f"任务进展: 已验收完成 {tr.get('verified_done_count', 0)} 项，待完成/待签收 {len(open_list)} 项")
    else:
        print(f"Tasks:     {tr.get('verified_done_count', 0)} verified done, {len(open_list)} open/pending")
    if done_list:
        print(f"  {'已完成' if is_zh else 'Verified Done'}:")
        for tk in done_list[:8]:
            print(f"    • {tk['id']}: {tk['title']}")
    if open_list:
        print(f"  {'待推进/待拍板' if is_zh else 'Open / Pending'}:")
        for tk in open_list[:8]:
            print(f"    • {tk['id']} ({_fmt_task_state(tk['state'], lang)}, {_fmt_check(tk['human_check'], lang)}): {tk['title']}")


def print_context_pack(pack: dict[str, Any], target: str, task_obj: Any = None, lang: str = "en") -> None:
    """Render a task, module, document, directory, domain, or trace context pack."""
    is_zh = lang == "zh"
    t_info = pack.get("task")
    if pack.get("focus_kind") == "task" and (t_info or task_obj is not None):
        tid = t_info["id"] if t_info else task_obj.id
        title = t_info["title"] if t_info else task_obj.title
        st_raw = t_info["state"] if t_info else task_obj.state
        chk_raw = t_info["human_check"] if t_info else task_obj.human_check
        ms = t_info["milestone"] if t_info else (task_obj.milestone or "-")
        print(f"=== {'任务上下文' if is_zh else 'Task Context'}: {tid} ({title}) ===")
        print(
            f"{'状态' if is_zh else 'Status'}:  {_fmt_task_state(st_raw, lang)} | "
            f"{'验收' if is_zh else 'Sign-off'}: {_fmt_check(chk_raw, lang)} | "
            f"{'里程碑' if is_zh else 'Milestone'}: {ms or '-'}"
        )
        if t_info:
            if t_info.get("selected_option"):
                print(f"{'已选方案' if is_zh else 'Selected Option'}: {t_info['selected_option']}")
            if t_info.get("blocker_question"):
                print(f"{'待拍板问题' if is_zh else 'Blocker Question'}: {t_info['blocker_question']}")
            if t_info.get("blocker_options"):
                print("可选方案:" if is_zh else "Blocker Options:")
                for idx, opt in enumerate(t_info["blocker_options"], 1):
                    print(f"  {idx}. {opt}")
            if t_info.get("design_docs"):
                print(f"{'设计文档' if is_zh else 'Design Docs'}: {', '.join(t_info['design_docs'])}")
            if t_info.get("specs"):
                print(f"{'关联模块规范' if is_zh else 'Linked Specs'}: {', '.join(t_info['specs'])}")
        print()

    if "module" in pack:
        m = pack["module"]
        d = pack["domain"]
        print(f"=== {'主模块上下文' if is_zh else 'Module Context'}: {m['id']} ({m['title']}) ===")
        print(f"{'业务域' if is_zh else 'Domain'}:  {d['name']} ({fmt_stage(m['stage'], lang)})")
        print(f"{'规范' if is_zh else 'Spec'}:    {m['doc_path']}")
        print(f"{'对外承诺' if is_zh else 'Promise'}: {m['promise'] or m['summary']}")
        print(f"{'负责文件' if is_zh else 'Owns'}:    {', '.join(m['owns'])}")
        print(f"{'依赖模块' if is_zh else 'Depends'}: {', '.join(m['depends_on']) or ('无' if is_zh else '(none)')}")
        if pack.get("verbatim_sources"):
            print("\n用户需求原话:" if is_zh else "\nVerbatim User Quotes:")
            for q in pack["verbatim_sources"]:
                excerpt = " ".join(q["quote"].splitlines())
                print(f"  [{q['id']} · {q['date']}] “{excerpt}”")
        if pack.get("decisions"):
            print("\n架构与约束决策:" if is_zh else "\nGoverning Decisions:")
            for dec in pack["decisions"]:
                print(f"  • {dec['id']} [{_fmt_dec_status(dec['status'], lang)}]: {dec['title']}")
        if pack.get("active_tasks"):
            print("\n活跃任务:" if is_zh else "\nActive Tasks:")
            for tk in pack["active_tasks"]:
                print(f"  • {tk['id']} ({_fmt_task_state(tk['state'], lang)}, {_fmt_check(tk['human_check'], lang)}): {tk['title']}")
    elif pack.get("focus_kind") == "task" and t_info:
        if pack.get("verbatim_sources"):
            print("\n用户需求原话:" if is_zh else "\nVerbatim User Quotes:")
            for q in pack["verbatim_sources"]:
                print(f"  [{q['id']} · {q['date']}] “{' '.join(q['quote'].splitlines())}”")
        if pack.get("decisions"):
            print("\n架构与约束决策:" if is_zh else "\nGoverning Decisions:")
            for dec in pack["decisions"]:
                print(f"  • {dec['id']} [{_fmt_dec_status(dec['status'], lang)}]: {dec['title']}")
    elif pack.get("focus_kind") == "document" and "document" in pack:
        doc = pack["document"]
        print(f"=== {'文档上下文' if is_zh else 'Document Context'}: {doc['path']} ({doc['title']}) ===")
        print(f"{'分类' if is_zh else 'Category'}: {doc['category']} | {'行数' if is_zh else 'Lines'}: {doc['line_count']}")
        if doc["summary"]:
            print(f"{'摘要' if is_zh else 'Summary'}:  {doc['summary']}")
        if pack.get("domain"):
            print(f"{'业务域' if is_zh else 'Domain'}:   {pack['domain'].get('name', '')}")
    elif pack.get("focus_kind") == "directory" and "directory" in pack:
        dr = pack["directory"]
        label = dr["label_zh"] if is_zh else dr["label_en"]
        print(f"=== {'目录上下文' if is_zh else 'Directory Context'}: {dr['path']} ({label}) ===")
        print(f"{'说明' if is_zh else 'Summary'}: {dr['summary_zh'] if is_zh else dr['summary_en']}")
        if is_zh:
            print(f"统计:   {dr['file_count']} 个文件 | {dr['doc_count']} 份文档 | {dr['total_lines']} 行")
        else:
            print(f"Stats:   {dr['file_count']} files | {dr['doc_count']} docs | {dr['total_lines']} lines")
        if dr.get("doc_paths"):
            print(f"{'文档' if is_zh else 'Docs'}:    " + ", ".join(dr["doc_paths"]))
    elif pack.get("focus_kind") == "domain" and "domain" in pack:
        dm = pack["domain"]
        print(f"=== {'业务域上下文' if is_zh else 'Domain Context'}: {dm['id']} ({dm['name']}) ===")
        print(f"{'阶段' if is_zh else 'Stage'}:   {fmt_stage(dm['stage'], lang)} | {'规范' if is_zh else 'Spec'}: {dm['doc_path']}")
        print(f"{'对外承诺' if is_zh else 'Promise'}: {dm['promise'] or dm['summary']}")
        print(f"{'模块列表' if is_zh else 'Modules'}: " + (", ".join(dm.get("modules", [])) or ("无" if is_zh else "(none)")))
    elif pack.get("anchor_type") in ("source", "decision"):
        print_trace_summary(pack, lang=lang)
    else:
        print(f"Context resolved for `{target}` ({pack.get('focus_kind', 'unknown')}).")
