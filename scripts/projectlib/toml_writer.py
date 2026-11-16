# Role: Safe TOML serializers and write-back mutators for sources.toml, work.toml, and archives.
# Out of scope: HTTP serving, AST import scanning, or HTML template assembly.
# Anchors: spec=perspective.server, ADR-002, SRC-014, SRC-015, SRC-019

from __future__ import annotations

import datetime
import re
import tomllib
from pathlib import Path
from typing import Any

from .loader import load_project_graph


def format_toml_basic_str(val: str) -> str:
    """Escape backslashes, quotes, tabs, newlines, and control characters for a single-line TOML string."""
    escaped = (
        val.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\r", "\\r")
        .replace("\n", "\\n")
        .replace("\t", "\\t")
    )
    return f'"{escaped}"'


def format_toml_multiline_quote(val: str) -> str:
    """Safely encode a verbatim multi-line quote using literal ''' when possible or escaped \"\"\" otherwise."""
    normalized = val.replace("\r\n", "\n").replace("\r", "\n").strip()
    if "'''" not in normalized:
        return f"'''\n{normalized}\n'''"
    escaped = normalized.replace("\\", "\\\\").replace('"""', '\\"\\"\\"')
    return f'"""\n{escaped}\n"""'


def format_toml_list(items: list[str] | tuple[str, ...]) -> str:
    return "[" + ", ".join(format_toml_basic_str(str(x)) for x in items) + "]"


def _extract_leading_comments(text: str) -> str:
    kept: list[str] = []
    for line in text.splitlines():
        st = line.strip()
        if st.startswith("#") or st == "":
            kept.append(line)
        else:
            break
    return "\n".join(kept).strip()


_MILESTONE_KNOWN = {"id", "domain", "name", "slot", "era", "depends_on"}
_TASK_KNOWN = {
    "id",
    "milestone",
    "title",
    "state",
    "human_check",
    "specs",
    "decisions",
    "sources",
    "blocker_question",
    "blocker_options",
}


def _format_toml_value(val: Any) -> str:
    if isinstance(val, bool):
        return "true" if val else "false"
    if isinstance(val, int):
        return str(val)
    if isinstance(val, float):
        return repr(val)
    if isinstance(val, (list, tuple)):
        return format_toml_list(list(val))
    return format_toml_basic_str(str(val))


def serialize_work_toml(
    milestones: list[dict[str, Any]],
    tasks: list[dict[str, Any]],
    header: str = "",
) -> str:
    lines: list[str] = []
    if header.strip():
        lines.append(header.strip())
        lines.append("")
    for m in milestones:
        lines.append("[[milestones]]")
        lines.append(f"id = {format_toml_basic_str(m['id'])}")
        lines.append(f"domain = {format_toml_basic_str(m.get('domain', 'core'))}")
        lines.append(f"name = {format_toml_basic_str(m.get('name', m['id']))}")
        lines.append(f"slot = {format_toml_basic_str(m.get('slot', 'now'))}")
        if m.get("era"):
            lines.append(f"era = {format_toml_basic_str(m['era'])}")
        lines.append(f"depends_on = {format_toml_list(m.get('depends_on', []))}")
        for extra_k in sorted(k for k in m if k not in _MILESTONE_KNOWN and not isinstance(m[k], dict)):
            lines.append(f"{extra_k} = {_format_toml_value(m[extra_k])}")
        lines.append("")
    for t in tasks:
        lines.append("[[tasks]]")
        lines.append(f"id = {format_toml_basic_str(t['id'])}")
        lines.append(f"milestone = {format_toml_basic_str(t.get('milestone', ''))}")
        lines.append(f"title = {format_toml_basic_str(t.get('title', t['id']))}")
        lines.append(f"state = {format_toml_basic_str(t.get('state', 'todo'))}")
        lines.append(f"human_check = {format_toml_basic_str(t.get('human_check', 'pending'))}")
        lines.append(f"specs = {format_toml_list(t.get('specs', []))}")
        lines.append(f"decisions = {format_toml_list(t.get('decisions', []))}")
        lines.append(f"sources = {format_toml_list(t.get('sources', []))}")
        if t.get("blocker_question"):
            lines.append(f"blocker_question = {format_toml_basic_str(t['blocker_question'])}")
        if t.get("blocker_options"):
            lines.append(f"blocker_options = {format_toml_list(t['blocker_options'])}")
        for extra_k in sorted(k for k in t if k not in _TASK_KNOWN and not isinstance(t[k], dict)):
            lines.append(f"{extra_k} = {_format_toml_value(t[extra_k])}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def append_verbatim_source(root: Path, quote: str, context: str) -> str:
    sources_path = root / "docs" / "sources.toml"
    sources_path.parent.mkdir(parents=True, exist_ok=True)
    existing_text = sources_path.read_text(encoding="utf-8") if sources_path.is_file() else ""
    nums = [int(m) for m in re.findall(r'id\s*=\s*"SRC-(\d+)"', existing_text)]
    next_id = f"SRC-{(max(nums) + 1) if nums else 1:03d}"
    today = datetime.date.today().isoformat()
    entry = (
        f"\n[[sources]]\n"
        f'id = "{next_id}"\n'
        f'date = "{today}"\n'
        f'status = "active"\n'
        f"context = {format_toml_basic_str(context)}\n"
        f"quote = {format_toml_multiline_quote(quote)}\n"
    )
    sources_path.write_text(existing_text.rstrip() + "\n" + entry, encoding="utf-8")
    return next_id


def mutate_task_in_work_toml(
    root: Path,
    task_id: str,
    *,
    new_state: str | None = None,
    human_check: str | None = None,
    resolution_quote: str = "",
) -> bool:
    graph = load_project_graph(root)
    if task_id not in graph.tasks:
        return False
    origin_rel = graph.tasks[task_id].origin_path or "docs/work.toml"
    work_path = root / origin_rel
    if not work_path.is_file():
        return False

    orig_text = work_path.read_text(encoding="utf-8")
    header = _extract_leading_comments(orig_text)
    data = tomllib.loads(orig_text)
    milestones = list(data.get("milestones", []))
    tasks = list(data.get("tasks", []))

    target_task = next((t for t in tasks if str(t.get("id")) == task_id), None)
    if target_task is None:
        return False

    quote_val = resolution_quote.strip()
    preset_opts = [str(opt).strip() for opt in target_task.get("blocker_options", [])]
    matched_preset = quote_val if (quote_val and quote_val in preset_opts) else ""

    new_src_id = ""
    if quote_val and not matched_preset:
        new_src_id = append_verbatim_source(root, quote_val, f"Blocker decision for task {task_id}")

    if new_state:
        target_task["state"] = new_state
    if human_check:
        target_task["human_check"] = human_check
        if human_check == "approved" and target_task.get("state") == "ready_for_check":
            target_task["state"] = "done"
    if matched_preset:
        target_task["selected_option"] = matched_preset
        target_task["blocker_question"] = ""
        target_task["blocker_options"] = []
    elif quote_val:
        target_task["blocker_question"] = ""
        target_task["blocker_options"] = []
        srcs = list(target_task.get("sources", []))
        if new_src_id and new_src_id not in srcs:
            srcs.append(new_src_id)
        target_task["sources"] = srcs
    updated = True

    if updated:
        work_path.write_text(serialize_work_toml(milestones, tasks, header=header), encoding="utf-8")
    return updated


def archive_completed_milestone(root: Path, milestone_id: str) -> Path:
    graph = load_project_graph(root)
    if milestone_id not in graph.milestones:
        raise ValueError(f"Unknown milestone `{milestone_id}`")
    ms_obj = graph.milestones[milestone_id]
    if ms_obj.archived:
        raise ValueError(f"Milestone `{milestone_id}` is already archived in `{ms_obj.origin_path}`")
    origin_rel = ms_obj.origin_path
    work_path = root / origin_rel
    orig_text = work_path.read_text(encoding="utf-8")
    header = _extract_leading_comments(orig_text)
    data = tomllib.loads(orig_text)

    keep_ms, move_ms = [], []
    for m in data.get("milestones", []):
        m_copy = dict(m)
        if str(m_copy.get("id")) == milestone_id:
            m_copy["slot"] = "done"
            move_ms.append(m_copy)
        else:
            keep_ms.append(m_copy)

    keep_tasks, move_tasks = [], []
    for t in data.get("tasks", []):
        t_copy = dict(t)
        if str(t_copy.get("milestone")) == milestone_id:
            t_copy["state"] = "done"
            move_tasks.append(t_copy)
        else:
            keep_tasks.append(t_copy)

    slug = re.sub(r"[^a-zA-Z0-9_-]+", "-", milestone_id.lower()).strip("-") or "milestone"
    arch_path = root / "docs" / "archive" / f"work-{slug}.toml"
    arch_path.parent.mkdir(parents=True, exist_ok=True)
    arch_header = f"# Archived milestone {milestone_id}"
    if arch_path.is_file():
        old_arch_text = arch_path.read_text(encoding="utf-8")
        arch_header = _extract_leading_comments(old_arch_text) or arch_header
        try:
            old_data = tomllib.loads(old_arch_text)
        except tomllib.TOMLDecodeError:
            old_data = {}
        new_m_ids = {str(x.get("id")) for x in move_ms}
        new_t_ids = {str(x.get("id")) for x in move_tasks}
        move_ms = [dict(x) for x in old_data.get("milestones", []) if str(x.get("id")) not in new_m_ids] + move_ms
        move_tasks = [dict(x) for x in old_data.get("tasks", []) if str(x.get("id")) not in new_t_ids] + move_tasks
    arch_path.write_text(
        serialize_work_toml(move_ms, move_tasks, arch_header),
        encoding="utf-8",
    )
    work_path.write_text(serialize_work_toml(keep_ms, keep_tasks, header=header), encoding="utf-8")
    return arch_path
