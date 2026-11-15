"""Read-only document discovery; applicability and authority stay with callers."""

from __future__ import annotations

import hashlib
import json
import os
import re
import stat
from collections import Counter
from datetime import date
from pathlib import Path

if __package__:
    from .check_docs import (IGNORED_DIRECTORY_NAMES, PROMISE_RE, VALID_AUTHORITIES,
                             VALID_DOC_TYPES, VALID_PROMISE_STATUSES, VALID_STATUSES,
                             parse_record_fields)
    from .rule_reading import HEADING, RuleError, RuleRepository, heading_slug, parse_frontmatter_text, visible_lines
else:
    from check_docs import (IGNORED_DIRECTORY_NAMES, PROMISE_RE, VALID_AUTHORITIES,
                            VALID_DOC_TYPES, VALID_PROMISE_STATUSES, VALID_STATUSES,
                            parse_record_fields)
    from rule_reading import HEADING, RuleError, RuleRepository, heading_slug, parse_frontmatter_text, visible_lines


LIVE = {"current", "target", "active", "needs_reconciliation"}
CLOSED_FINDINGS = {"resolved", "disproved"}
FINDING_STATES = {"unverified", "verified", "partial", "accepted", "wontfix"} | CLOSED_FINDINGS
STATUS_FIELD = re.compile(r"^\s*-\s+\*\*Status:\*\*\s*(.*?)\s*$")
PROVENANCE_HEADINGS = {"source anchors", "reconciliation log"}


def calendar_date(value: str) -> date:
    try:
        parsed = date.fromisoformat(value)
        if parsed.isoformat() == value:
            return parsed
    except ValueError:
        pass
    raise ValueError("use a calendar date in YYYY-MM-DD form")


def timing(value: str, today: date | None) -> str:
    deadline = calendar_date(value)
    if today is None:
        return "unassessed"
    return "past" if deadline < today else "due" if deadline == today else "future"


def outline(lines: list[str], visible: tuple[bool, ...]) -> list[dict]:
    headings = []
    for index, line in operative_lines(lines, visible):
        if match := HEADING.match(line.rstrip("\r\n")):
            headings.append({"title": match[1], "level": len(line) - len(line.lstrip("#")), "line": index})
    return headings


def operative_lines(lines: list[str], visible: tuple[bool, ...]):
    """Ignore canonical provenance sections as well as fenced examples."""
    provenance_level = None
    in_metadata = bool(lines and lines[0].rstrip("\r\n") == "---")
    for index, (line, shown) in enumerate(zip(lines, visible), 1):
        if in_metadata:
            if index > 1 and line.rstrip("\r\n") == "---":
                in_metadata = False
            continue
        if not shown:
            continue
        match = HEADING.match(line.rstrip("\r\n"))
        if match:
            level = len(line) - len(line.lstrip("#"))
            if provenance_level is not None and level <= provenance_level:
                provenance_level = None
            if match[1].strip().lower() in PROVENANCE_HEADINGS:
                provenance_level = level
        if provenance_level is None:
            yield index, line


def category(path: str, metadata: dict, error: str | None) -> tuple[str, list[str]]:
    if error == "missing frontmatter" and Path(path).name in {"AGENTS.md", "README.md"}:
        return "navigation", []
    gaps = []
    if error:
        gaps.append(error)
    for key, allowed in [("doc_type", VALID_DOC_TYPES), ("authority", VALID_AUTHORITIES),
                         ("status", VALID_STATUSES)]:
        if metadata.get(key) not in allowed:
            gaps.append(f"unrecognized or missing {key}: {metadata.get(key, '(absent)')}")
    if gaps:
        return "unclassified", gaps
    state, kind, authority = (metadata[k] for k in ("status", "doc_type", "authority"))
    if state not in LIVE:
        return "excluded", []
    expected = {"contract": "normative", "surface-contract": "normative",
                "authority-map": "normative", "plan": "planning",
                "issue-tracker": "normative", "guide": "guidance", "evidence": "evidence"}
    if authority != expected[kind]:
        return "unclassified", [f"{kind} declares {authority}; expected {expected[kind]}"]
    if state == "needs_reconciliation":
        return "needs_reconciliation", []
    if kind in {"contract", "surface-contract", "authority-map"}:
        return ("current_rules" if state == "current" else "target_rules" if state == "target"
                else "unclassified"), ([] if state in {"current", "target"} else ["rule lifecycle needs judgment"])
    if kind == "plan":
        return ("active_plans", []) if state == "active" else ("unclassified", ["plan lifecycle needs judgment"])
    if kind == "issue-tracker":
        return ("findings", []) if state == "active" else ("unclassified", ["finding lifecycle needs judgment"])
    if state != "current":
        return "unclassified", [f"{kind} lifecycle needs judgment"]
    return ("guidance" if kind == "guide" else "evidence"), []


class DocumentOverview:
    def __init__(self, root: Path):
        self.root = root
        self.reader = None

    def open_root(self):
        try:
            root = self.root.resolve()
            mode = root.stat().st_mode
        except (FileNotFoundError, NotADirectoryError) as exc:
            raise RuleError("overview root must be an existing directory") from exc
        if not stat.S_ISDIR(mode):
            raise RuleError("overview root must be an existing directory")
        return root, RuleRepository(root)

    def discover(self, sources: list[str]) -> tuple[list[str], list[dict]]:
        found = set()
        diagnostics = []

        def problem(path, message):
            diagnostics.append({"path": str(path), "message": message})

        def add(path):
            try:
                relative, _ = self.reader.reference(path.relative_to(self.root).as_posix())
                found.add(relative)
            except (OSError, RuleError, ValueError) as exc:
                problem(path.relative_to(self.root).as_posix(), str(exc))

        for raw in sources:
            path = self.root / raw
            try:
                resolved = path.resolve()
                if not resolved.is_relative_to(self.root):
                    raise RuleError("source escapes the repository")
                if resolved.is_file():
                    add(resolved)
                elif resolved.is_dir():
                    def onerror(error):
                        problem(raw, f"cannot enumerate source: {error}")
                    for current, directories, files in os.walk(resolved, followlinks=False, onerror=onerror):
                        base = Path(current)
                        for name in sorted(directories):
                            if name not in IGNORED_DIRECTORY_NAMES and (base / name).is_symlink():
                                problem((base / name).relative_to(self.root).as_posix(),
                                        "directory symlink not traversed; select its contained target explicitly")
                        directories[:] = sorted(name for name in directories
                            if name not in IGNORED_DIRECTORY_NAMES and not (base / name).is_symlink())
                        for name in sorted(files):
                            if Path(name).suffix == ".md":
                                add(base / name)
                else:
                    problem(raw, "source is missing or is not a regular Markdown file/directory")
            except (OSError, ValueError, RuntimeError, RuleError) as exc:
                problem(raw, str(exc))
        return sorted(found), sorted(diagnostics, key=lambda item: (item["path"], item["message"]))

    def recheck(self, sources, discovered, discovery_diagnostics, identities, failed_reads):
        current, diagnostics = self.discover(sources)
        if current != discovered or diagnostics != discovery_diagnostics:
            raise RuleError("overview source membership changed; rerun overview")
        for path, digest in identities.items():
            try:
                relative, _ = self.reader.reference(path)
                data = (self.root / relative).read_bytes()
            except (OSError, RuleError, RuntimeError) as exc:
                raise RuleError(f"{path}: source changed or became unavailable; rerun overview") from exc
            if relative != path or hashlib.sha256(data).hexdigest() != digest:
                raise RuleError(f"{path}: source changed; rerun overview")
        for path, failure in failed_reads.items():
            try:
                relative, _ = self.reader.reference(path)
                (self.root / relative).read_bytes()
            except (OSError, RuleError, RuntimeError) as exc:
                if (type(exc).__name__, str(exc)) == failure:
                    continue
            raise RuleError(f"{path}: source read failure changed or recovered; rerun overview")

    def build(self, sources=(), *, today=None, offset=0, limit=None, snapshot=None, include_outline=False):
        if offset < 0 or (limit is not None and limit <= 0):
            raise RuleError("offset must be nonnegative and limit must be positive")
        sources = list(dict.fromkeys(sources or ["AGENTS.md", "docs"]))
        if any(not raw or "\\" in raw or "://" in raw or "#" in raw or "?" in raw for raw in sources):
            raise RuleError("overview sources must be local paths without fragments, queries or backslashes")
        if any(Path(raw).is_absolute() for raw in sources):
            raise RuleError("overview sources must be repository-relative paths")
        root_failure = None
        try:
            self.root, self.reader = self.open_root()
        except (OSError, RuntimeError) as exc:
            root_failure = (type(exc).__name__, str(exc))
        if root_failure is None:
            discovered, discovery_diagnostics = self.discover(sources)
        else:
            discovered = []
            discovery_diagnostics = [{"path": ".", "message": f"cannot access overview root: {root_failure[1]}"}]
        diagnostics = list(discovery_diagnostics)
        documents, excluded, identities, failed_reads = [], [], {}, {}
        for path in discovered:
            try:
                relative, _ = self.reader.reference(path)
                if relative != path:
                    raise RuleError("source identity changed during discovery; rerun overview")
                data = (self.root / relative).read_bytes()
                identities[path] = hashlib.sha256(data).hexdigest()
                text = data.decode("utf-8")
                lines = text.splitlines(keepends=True)
                shown = visible_lines(lines)
                metadata, error = parse_frontmatter_text(text)
            except (OSError, UnicodeError, RuleError, RuntimeError) as exc:
                if path not in identities:
                    failed_reads[path] = (type(exc).__name__, str(exc))
                diagnostics.append({"path": path, "message": str(exc)})
                documents.append({"path": path, "sha256": identities.get(path), "title": Path(path).name,
                                  "category": "unclassified", "metadata": {}, "gaps": [str(exc)],
                                  "headings": [], "findings": [], "commitments": [], "closed_findings": 0})
                continue
            group, gaps = category(path, metadata, error)
            if error and error != "missing frontmatter":
                diagnostics.append({"path": path, "message": error})
            if group == "excluded":
                excluded.append({"path": path, "sha256": identities[path], "status": metadata["status"]})
                continue
            headings = outline(lines, shown)
            slugs = Counter(heading_slug(match[1]) for line, visible in zip(lines, shown)
                            if visible and (match := HEADING.match(line.rstrip("\r\n"))))
            for item in headings:
                slug = heading_slug(item["title"])
                item["reference"] = f"{path}#{slug}" if slug and slugs[slug] == 1 else path
            record = {"path": path, "sha256": identities[path],
                      "title": next((h["title"] for h in headings if h["level"] == 1), Path(path).name),
                      "category": group, "metadata": metadata, "gaps": gaps,
                      "headings": headings, "findings": [], "commitments": [], "closed_findings": 0}
            # Unclassified sources remain locators; ambiguous metadata cannot
            # promote their contents into obligations or active work.
            if group not in {"unclassified", "navigation"}:
                review_line = next((i for i, line in enumerate(lines, 1)
                                    if ":" in line and line.split(":", 1)[0].strip() == "review_due"), 1)
                self.commitments(record, list(operative_lines(lines, shown)), today, diagnostics, review_line)
                if metadata["doc_type"] == "issue-tracker":
                    self.findings(record, list(operative_lines(lines, shown)))
            documents.append(record)

        basis = {"schema_version": 1, "sources": sources, "calendar_reference": today.isoformat() if today else None,
                 "documents": documents, "excluded": excluded, "diagnostics": diagnostics}
        identity = hashlib.sha256(json.dumps(basis, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()
        if snapshot is not None and snapshot != identity:
            raise RuleError("overview snapshot changed; restart at offset 0 without --snapshot")
        total = len(documents)
        selected = documents[offset:offset + limit if limit is not None else None]
        page = [{**item, "heading_count": len(item["headings"]),
                 "headings": item["headings"] if include_outline else []} for item in selected]
        result = {"schema_version": 1, "snapshot": identity, "sources": sources,
                  "detail": "headings" if include_outline else "documents",
                  "calendar_reference": basis["calendar_reference"],
                  "coverage": {"scan_complete": not diagnostics, "files_discovered": len(discovered),
                               "directory_exclusions": sorted(IGNORED_DIRECTORY_NAMES),
                               "categories": dict(sorted(Counter(d["category"] for d in documents).items())),
                               "unclassified": [d["path"] for d in documents if d["category"] == "unclassified"],
                               "uncertain_findings": [{"path": d["path"], "line": f["line"]}
                                                      for d in documents for f in d["findings"] if f["status"] == "unknown"],
                               "excluded": excluded, "diagnostics": diagnostics},
                  "page": {"offset": offset, "limit": limit, "total": total, "shown": len(page),
                           "next_offset": offset + len(page) if offset + len(page) < total else None},
                  "documents": page}
        if root_failure is None:
            self.recheck(sources, discovered, discovery_diagnostics, identities, failed_reads)
        else:
            try:
                self.open_root()
            except (OSError, RuntimeError) as exc:
                if (type(exc).__name__, str(exc)) == root_failure:
                    return result
            except RuleError:
                pass
            raise RuleError("overview root access changed; rerun overview")
        return result

    @staticmethod
    def commitments(record, lines, today, diagnostics, review_line):
        def add(kind, identifier, fields, line):
            entry = {**fields, "kind": kind, "id": identifier, "line": line}
            try:
                entry["timing"] = timing(fields["due"], today)
            except (ValueError, KeyError):
                entry["timing"] = "invalid"
                diagnostics.append({"path": record["path"], "message": f"line {line}: invalid calendar date in {identifier}"})
            record["commitments"].append(entry)

        if "review_due" in record["metadata"]:
            add("review", "review_due", {"due": record["metadata"]["review_due"], "status": "declared"}, review_line)
        seen = set()
        for number, text in lines:
            match = PROMISE_RE.match(text)
            if not match:
                continue
            identifier, payload = match.groups()
            fields, errors = parse_record_fields(payload)
            required = {"due", "status", "owner", "description"}
            if required - fields.keys():
                errors.append("missing " + ", ".join(sorted(required - fields.keys())))
            if fields.get("status") not in VALID_PROMISE_STATUSES:
                errors.append("unknown promise status")
            if identifier in seen:
                errors.append("duplicate promise id")
            seen.add(identifier)
            if errors:
                diagnostics.append({"path": record["path"], "message": f"line {number}: promise[{identifier}]: " + "; ".join(errors)})
                record["commitments"].append({"kind": "promise", "id": identifier, "line": number,
                                              "status": "unknown", "raw": payload, "timing": "unassessed"})
            elif fields["status"] == "open":
                add("promise", identifier, fields, number)

    @staticmethod
    def findings(record, lines):
        sections = []
        for number, text in lines:
            if text.startswith("## "):
                sections.append({"title": text[3:].strip(), "line": number, "states": []})
            if match := STATUS_FIELD.match(text):
                if not sections:
                    sections.append({"title": record["title"], "line": number, "states": []})
                sections[-1]["states"].append(match[1].strip().strip("`"))
        if not sections:
            sections.append({"title": record["title"], "line": 1, "states": []})
        for section in sections:
            states = section.pop("states")
            state = states[0] if len(states) == 1 and states[0] in FINDING_STATES else "unknown"
            if state in CLOSED_FINDINGS:
                record["closed_findings"] += 1
            else:
                record["findings"].append({**section, "status": state,
                    "disposition": state if state in {"accepted", "wontfix"} else "unresolved" if state != "unknown" else "unknown"})


def render_text(view: dict) -> str:
    coverage, page = view["coverage"], view["page"]
    lines = ["DOCUMENT OVERVIEW", "Source metadata and navigation; read sources before judging applicability.",
             f"Scope: {', '.join(view['sources'])}", f"Snapshot: {view['snapshot']}",
             f"Scan: {'complete' if coverage['scan_complete'] else 'INCOMPLETE'}; {coverage['files_discovered']} Markdown files; "
             f"{len(coverage['excluded'])} inactive; {len(coverage['unclassified'])} unclassified; "
             f"{len(coverage['uncertain_findings'])} unknown finding states",
             "Categories: " + ", ".join(f"{k}={v}" for k, v in coverage["categories"].items()),
             f"Detail: {view['detail']}; use --outline --source PATH to expand document headings",
             f"Calendar reference: {view['calendar_reference'] or 'unassessed (pass --today YYYY-MM-DD)'}",
             f"Documents: offset {page['offset']}; shown {page['shown']} of {page['total']}"]
    if coverage["excluded"]:
        lines.append("Inactive paths and states: use --format json and inspect coverage.excluded")
    for item in view["documents"]:
        metadata = item["metadata"]
        lines.extend(["", f"[{item['category']}] {item['title']}",
                      f"  {item['path']} — {metadata.get('status', 'undeclared')}; {metadata.get('authority', 'undeclared')} authority",
                      f"  sha256: {item['sha256'] or 'unavailable'}"])
        if view["detail"] == "documents":
            lines.append(f"  {item['heading_count']} headings available with --outline")
        if item["gaps"]:
            lines.append("  Needs judgment: " + "; ".join(item["gaps"]))
        details = []
        for heading in item["headings"]:
            details.append((heading["line"], 0,
                            f"  L{heading['line']}: heading H{heading['level']}: {heading['title']}"))
        for finding in item["findings"]:
            details.append((finding["line"], 1,
                            f"  L{finding['line']}: [{finding['status']}; {finding['disposition']}] {finding['title']}"))
        for entry in item["commitments"]:
            detail = entry.get("description", entry.get("raw", "source-declared review date"))
            details.append((entry["line"], 2,
                            f"  L{entry['line']}: {entry['kind']}[{entry['id']}] {entry['status']}; "
                            f"due={entry.get('due', 'unknown')}; {entry['timing']}; {detail}"))
        lines.extend(text for _, _, text in sorted(details))
        if item["closed_findings"]:
            lines.append(f"  {item['closed_findings']} resolved/disproved finding(s) outside attention")
    for problem in coverage["diagnostics"]:
        lines.append(f"DIAGNOSTIC {problem['path']}: {problem['message']}")
    if page["next_offset"] is not None:
        reference = f" --today {view['calendar_reference']}" if view["calendar_reference"] else ""
        lines.append(f"More documents: --offset {page['next_offset']} --snapshot {view['snapshot']}{reference}; reuse source selection")
    lines.append("OVERVIEW COMPLETE" if coverage["scan_complete"] else "OVERVIEW INCOMPLETE — repair diagnostics and rerun")
    return "\n".join(lines) + "\n"
