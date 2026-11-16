# Role: Zero-dependency parser for thin Markdown YAML frontmatter, links, headings, and Mermaid blocks.
# Out of scope: Repository traversal, Git calls, or cross-file validation.
# Anchors: spec=graph.model, ADR-002, SRC-015, SRC-018

from __future__ import annotations

import re
from typing import Any

from .model import MermaidDiagram

HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")
RULE_SPAN_OPEN_RE = re.compile(r"^<!--\s*required-reading:\s*([a-z0-9][a-z0-9-]*)\s*-->$")
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)\s]+)\)")
FENCE_OPEN_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})\s*([a-zA-Z0-9_-]*)\s*$")


def heading_slug(title: str) -> str:
    cleaned = re.sub(r"[^\w\s-]", "", title.strip().lower())
    return re.sub(r"\s", "-", cleaned)


def _strip_quotes(raw: str) -> str:
    val = raw.strip()
    if len(val) >= 2 and val[0] == val[-1] and val[0] in ("'", '"'):
        return val[1:-1]
    return val


def _parse_inline_list(raw: str) -> list[str]:
    inner = raw.strip()[1:-1].strip()
    if not inner:
        return []
    return [_strip_quotes(part) for part in inner.split(",") if _strip_quotes(part)]


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str, str | None]:
    """Parse flat YAML frontmatter (scalars, inline `[a, b]`, and `- item` lists)."""
    if not text.startswith("---\n") and not text.startswith("---\r\n"):
        return {}, text, None
    lines = text.splitlines(keepends=True)
    end_idx = None
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            end_idx = idx
            break
    if end_idx is None:
        return {}, text, "unterminated `---` frontmatter block"

    meta: dict[str, Any] = {}
    current_list_key: str | None = None
    for raw_line in lines[1:end_idx]:
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("- ") and current_list_key is not None:
            meta[current_list_key].append(_strip_quotes(stripped[2:]))
            continue
        current_list_key = None
        if ":" not in raw_line:
            return meta, "".join(lines[end_idx + 1 :]), f"invalid frontmatter line: {stripped}"
        key, rest = raw_line.split(":", 1)
        key = key.strip()
        val = rest.strip()
        if not key:
            return meta, "".join(lines[end_idx + 1 :]), f"empty key in frontmatter: {stripped}"
        if val == "":
            meta[key] = []
            current_list_key = key
        elif val.startswith("[") and val.endswith("]"):
            meta[key] = _parse_inline_list(val)
        elif val in ("true", "false"):
            meta[key] = val == "true"
        else:
            meta[key] = _strip_quotes(val)

    body = "".join(lines[end_idx + 1 :])
    return meta, body, None


def as_str_tuple(value: Any) -> tuple[str, ...]:
    if value is None or value == "":
        return ()
    if isinstance(value, (list, tuple)):
        return tuple(str(v).strip() for v in value if str(v).strip())
    return (str(value).strip(),)


def extract_markdown_structure(
    text: str, source_path: str
) -> tuple[str, set[str], list[tuple[str, int]], tuple[MermaidDiagram, ...]]:
    """Return `(first_h1_title, heading_slugs, links_with_lines, mermaid_blocks)`."""
    _, body, _ = parse_frontmatter(text)
    lines = text.splitlines()
    fm_skip = 0
    if lines and lines[0].strip() == "---":
        for idx in range(1, len(lines)):
            if lines[idx].strip() == "---":
                fm_skip = idx + 1
                break

    first_h1 = ""
    slugs: set[str] = set()
    links: list[tuple[str, int]] = []
    mermaids: list[MermaidDiagram] = []

    in_fence: tuple[str, int, str, int, list[str]] | None = None
    last_heading = source_path

    for idx in range(fm_skip, len(lines)):
        line_no = idx + 1
        raw = lines[idx]
        m_fence = FENCE_OPEN_RE.match(raw)
        if in_fence is not None:
            char, count, lang, start_ln, buf = in_fence
            if m_fence and m_fence.group(1)[0] == char and len(m_fence.group(1)) >= count and not m_fence.group(2):
                if lang.lower() == "mermaid":
                    mermaids.append(
                        MermaidDiagram(
                            title=last_heading,
                            code="\n".join(buf).strip(),
                            source_path=source_path,
                            line=start_ln,
                        )
                    )
                in_fence = None
            else:
                buf.append(raw)
            continue

        if m_fence:
            in_fence = (m_fence.group(1)[0], len(m_fence.group(1)), m_fence.group(2), line_no, [])
            continue

        m_rule = RULE_SPAN_OPEN_RE.match(raw.strip())
        if m_rule:
            slugs.add(m_rule.group(1))

        m_head = HEADING_RE.match(raw)
        if m_head:
            hashes, h_text = m_head.group(1), m_head.group(2).strip()
            last_heading = h_text
            if len(hashes) == 1 and not first_h1:
                first_h1 = h_text
            slug = heading_slug(h_text)
            if slug:
                slugs.add(slug)

        # Strip inline code spans before scanning Markdown links
        without_code = re.sub(r"`[^`]*`", "", raw)
        for target in LINK_RE.findall(without_code):
            links.append((target, line_no))

    return first_h1, slugs, links, tuple(mermaids)


def has_inline_role_header(text: str) -> bool:
    """Check top 12 lines for a declared Role / responsibility header comment."""
    head = "\n".join(text.splitlines()[:12]).lower()
    return "role:" in head or "responsibility:" in head
