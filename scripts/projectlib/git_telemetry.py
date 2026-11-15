# Role: Read-only Git history, commit lag, review-accumulation, and ref-diff telemetry.
# Out of scope: Modifying Git state, parsing Markdown specs, or serving HTTP endpoints.
# Anchors: spec=graph.indexer, ADR-002, ADR-003, SRC-004, SRC-006

from __future__ import annotations

import hashlib
import re
import subprocess
from fnmatch import fnmatch
from pathlib import Path
from typing import Any

from .model import ModuleSpec


def _run_git(root: Path, args: list[str]) -> tuple[int, str]:
    try:
        proc = subprocess.run(
            ["git", "--no-optional-locks", *args],
            cwd=root,
            capture_output=True,
            text=True,
            timeout=8,
            check=False,
        )
        return proc.returncode, proc.stdout.rstrip("\r\n")
    except (OSError, subprocess.SubprocessError):
        return 1, ""


def is_git_repo(root: Path) -> bool:
    rc, out = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    return rc == 0 and out == "true"


def get_remote_url(root: Path) -> str:
    rc, out = _run_git(root, ["remote", "get-url", "origin"])
    return out if rc == 0 else ""


def get_head_sha(root: Path) -> str:
    rc, out = _run_git(root, ["rev-parse", "--short=12", "HEAD"])
    return out if rc == 0 else ""


def get_working_changed_files(root: Path, diff_base: str | None = None) -> list[str]:
    changed: set[str] = set()
    if diff_base:
        rc, out = _run_git(root, ["diff", "--name-only", diff_base])
        if rc == 0 and out:
            changed.update(line.strip() for line in out.splitlines() if line.strip())
    rc, out = _run_git(root, ["status", "--porcelain", "-uall"])
    if rc == 0 and out:
        for line in out.splitlines():
            if len(line) > 3:
                raw_path = line[3:].strip()
                if " -> " in raw_path:
                    raw_path = raw_path.split(" -> ", 1)[1].strip()
                changed.add(raw_path.strip('"'))
    return sorted(changed)


def get_working_tree_digest(root: Path) -> str:
    """Hash working-tree changed paths and bytes so `mark-reviewed` recognizes unchanged working trees."""
    changed = [p for p in get_working_changed_files(root) if p != "tmp" and not p.startswith("tmp/")]
    if not changed:
        return ""
    h = hashlib.sha256()
    for rel in changed:
        h.update(rel.encode("utf-8", errors="replace"))
        h.update(b"\0")
        fp = root / rel
        if fp.is_file():
            try:
                h.update(fp.read_bytes())
            except OSError:
                h.update(b"__unreadable__")
        else:
            h.update(b"__missing__")
        h.update(b"\0")
    return h.hexdigest()[:16]


def match_path_to_module(rel_path: str, modules: dict[str, ModuleSpec]) -> str | None:
    for mod_id, spec in modules.items():
        for pattern in spec.owns:
            norm = pattern.rstrip("/")
            if rel_path == norm or fnmatch(rel_path, pattern):
                return mod_id
            if pattern.endswith("/**") and rel_path.startswith(pattern[:-3] + "/"):
                return mod_id
    return None


def collect_git_telemetry(
    root: Path,
    modules: dict[str, ModuleSpec],
    last_review_sha: str = "",
    last_review_wt_digest: str = "",
) -> tuple[dict[str, tuple[int, int]], dict[str, Any]]:
    """Return `(per_module_lag_and_churn, git_summary_dict)`."""
    per_mod: dict[str, tuple[int, int]] = {m: (0, 0) for m in modules}
    if not is_git_repo(root):
        return per_mod, {
            "is_git_repo": False,
            "head_sha": "",
            "remote_url": "",
            "changed_files": [],
            "commits_since_review": 0,
            "modules_since_review": [],
            "stale_domains": [],
            "recent_refs": [],
            "recent_commits": [],
        }

    head_sha = get_head_sha(root)
    remote_url = get_remote_url(root)
    changed_files = get_working_changed_files(root)

    # Recent commit file touches (up to last 40 commits) for churn & lag estimation
    rc, log_out = _run_git(root, ["log", "-n", "40", "--name-only", "--pretty=format:__COMMIT__%h\t%s"])
    commits: list[tuple[str, list[str]]] = []
    commit_subjects: dict[str, str] = {}
    if rc == 0 and log_out:
        cur_sha = ""
        cur_files: list[str] = []
        for line in log_out.splitlines():
            if line.startswith("__COMMIT__"):
                if cur_sha:
                    commits.append((cur_sha, cur_files))
                raw_head = line[len("__COMMIT__") :]
                cur_sha, _, cur_subj = raw_head.partition("\t")
                cur_sha = cur_sha.strip()
                if cur_sha:
                    commit_subjects[cur_sha] = cur_subj.strip()
                cur_files = []
            elif line.strip():
                cur_files.append(line.strip())
        if cur_sha:
            commits.append((cur_sha, cur_files))

    churn_counts: dict[str, int] = {m: 0 for m in modules}
    lag_counts: dict[str, int] = {m: 0 for m in modules}
    changed_set = set(changed_files)
    doc_seen: set[str] = {
        mod_id for mod_id, spec in modules.items() if spec.doc_path in changed_set
    }

    for _, c_files in commits:
        touched_mods: set[str] = set()
        for f in c_files:
            for mod_id, spec in modules.items():
                if f == spec.doc_path:
                    doc_seen.add(mod_id)
            owner = match_path_to_module(f, modules)
            if owner:
                touched_mods.add(owner)
        for mod_id in touched_mods:
            churn_counts[mod_id] += 1
            if mod_id not in doc_seen:
                lag_counts[mod_id] += 1

    for mod_id in modules:
        per_mod[mod_id] = (lag_counts[mod_id], churn_counts[mod_id])

    # Commits and modules touched since last_review_sha
    commits_since = 0
    mods_since: set[str] = set()
    if last_review_sha and last_review_sha != "working-tree":
        rc_rev, rev_out = _run_git(
            root, ["log", f"{last_review_sha}..HEAD", "--name-only", "--pretty=format:__C__"]
        )
        if rc_rev == 0 and rev_out:
            for line in rev_out.splitlines():
                if line == "__C__":
                    commits_since += 1
                elif line.strip():
                    ow = match_path_to_module(line.strip(), modules)
                    if ow:
                        mods_since.add(ow)
    else:
        commits_since = len(commits)
        for _, c_files in commits:
            for f in c_files:
                ow = match_path_to_module(f, modules)
                if ow:
                    mods_since.add(ow)

    # Include uncommitted working-tree module touches unless already marked reviewed at exact digest
    wt_digest = get_working_tree_digest(root)
    current_anchor = head_sha or "working-tree"
    wt_already_reviewed = bool(
        last_review_wt_digest
        and last_review_wt_digest == wt_digest
        and last_review_sha == current_anchor
    )
    if not wt_already_reviewed:
        for f in changed_files:
            ow = match_path_to_module(f, modules)
            if ow:
                mods_since.add(ow)

    stale_domains = sorted(
        {modules[m].domain for m, (lag, _) in per_mod.items() if lag >= 2 and m in modules}
    )

    rc_tags, tags_out = _run_git(root, ["tag", "--sort=-creatordate"])
    refs = [t.strip() for t in tags_out.splitlines() if t.strip()][:12] if rc_tags == 0 else []
    for sha, _ in commits[:8]:
        if sha not in refs:
            refs.append(sha)

    return per_mod, {
        "is_git_repo": True,
        "head_sha": head_sha,
        "remote_url": remote_url,
        "changed_files": changed_files,
        "commits_since_review": commits_since,
        "modules_since_review": sorted(mods_since),
        "stale_domains": stale_domains,
        "recent_refs": refs,
        "recent_commits": [{"sha": s, "subject": commit_subjects.get(s, "")} for s, _ in commits[:8]],
    }


def _normalize_numstat_path(raw_path: str) -> str:
    s = raw_path.strip()
    if "{" in s and " => " in s:
        s = re.sub(r"\{[^{}]*? => ([^{}]*?)\}", r"\1", s)
        return re.sub(r"//+", "/", s).strip("/")
    if " => " in s:
        return s.split(" => ", 1)[1].strip()
    return s


def compare_git_refs(
    root: Path,
    modules: dict[str, ModuleSpec],
    base_ref: str,
    target_ref: str = "HEAD",
) -> dict[str, Any]:
    """Group `git diff` (`ref..ref` or working-tree vs HEAD) by domain and module with exact file statuses."""
    if not is_git_repo(root):
        return {"base": base_ref, "target": target_ref, "domains": [], "total_files": 0}
    norm_base = "" if base_ref in ("", "working-tree") else base_ref
    if not norm_base:
        if get_head_sha(root):
            eff_base, eff_target, diff_args = "HEAD", "working-tree", ["HEAD"]
        else:
            eff_base, eff_target, diff_args = "EMPTY", "working-tree", ["--cached"]
    elif target_ref == "working-tree":
        eff_base, eff_target, diff_args = norm_base, "working-tree", [norm_base]
    else:
        eff_base, eff_target, diff_args = norm_base, target_ref, [f"{norm_base}..{target_ref}"]

    rc, out = _run_git(root, ["diff", "--numstat", *diff_args])
    if rc != 0:
        return {"base": eff_base, "target": eff_target, "error": "unable to diff refs", "domains": []}

    status_map: dict[str, str] = {}
    rc_st, st_name_out = _run_git(root, ["diff", "--name-status", *diff_args])
    if rc_st == 0 and st_name_out:
        for st_ln in st_name_out.splitlines():
            cols = st_ln.split("\t")
            if len(cols) < 2:
                continue
            code = cols[0].strip()
            path_key = (cols[2] if code.startswith(("R", "C")) and len(cols) >= 3 else cols[1]).strip()
            if code.startswith("A"):
                status_map[path_key] = "added"
            elif code.startswith("D"):
                status_map[path_key] = "deleted"
            elif code.startswith("R"):
                status_map[path_key] = "renamed"
            else:
                status_map[path_key] = "modified"

    by_domain: dict[str, dict[str, Any]] = {}
    total_files = 0
    seen_paths: set[str] = set()

    def _record_path(path: str, added: int, deleted: int, status: str = "modified") -> None:
        nonlocal total_files
        seen_paths.add(path)
        total_files += 1
        mod_id = match_path_to_module(path, modules)
        dom_id = modules[mod_id].domain if mod_id and mod_id in modules else "Shared Docs & Config"
        bucket = by_domain.setdefault(
            dom_id, {"domain": dom_id, "files": 0, "added": 0, "deleted": 0, "modules": set(), "changed_files": []}
        )
        bucket["files"] += 1
        bucket["added"] += added
        bucket["deleted"] += deleted
        bucket["changed_files"].append(
            {"path": path, "added": added, "deleted": deleted, "status": status, "module": mod_id or ""}
        )
        if mod_id:
            bucket["modules"].add(mod_id)

    for line in out.splitlines():
        parts = line.split("\t")
        if len(parts) != 3:
            continue
        added = int(parts[0]) if parts[0].isdigit() else 0
        deleted = int(parts[1]) if parts[1].isdigit() else 0
        rel_path = _normalize_numstat_path(parts[2])
        _record_path(rel_path, added, deleted, status_map.get(rel_path, "modified"))

    if not norm_base or target_ref == "working-tree":
        st_rc, st_out = _run_git(root, ["status", "--porcelain", "-uall"])
        if st_rc == 0:
            for st_line in st_out.splitlines():
                if not st_line.startswith("?? "):
                    continue
                untracked_rel = st_line[3:].strip().rstrip("/")
                if not untracked_rel or untracked_rel.startswith("tmp/") or untracked_rel in seen_paths:
                    continue
                fp = root / untracked_rel
                if fp.is_file():
                    try:
                        line_cnt = len(fp.read_text(encoding="utf-8", errors="ignore").splitlines())
                    except OSError:
                        line_cnt = 0
                    _record_path(untracked_rel, line_cnt, 0, "untracked")

    summary = [
        {
            "domain": d["domain"],
            "files": d["files"],
            "added": d["added"],
            "deleted": d["deleted"],
            "modules": sorted(d["modules"]),
            "changed_files": d["changed_files"],
        }
        for d in sorted(by_domain.values(), key=lambda x: -(x["added"] + x["deleted"]))
    ]
    return {"base": eff_base, "target": eff_target, "total_files": total_files, "domains": summary}
