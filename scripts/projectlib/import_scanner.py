# Role: Static Python AST, JS/TS (multiline + aliases), CSS, HTML/Vue/Svelte, Go, and Rust import scanner.
# Out of scope: Executing user code, Git subprocess calls, or HTTP rendering.
# Anchors: spec=graph.indexer, ADR-002, SRC-010, SRC-018

from __future__ import annotations

import ast
import bisect
import os
import re
from pathlib import Path

from .frontmatter import has_inline_role_header
from .model import FileStat, ImportEdge, ModuleSpec, ModuleTelemetry, matches_any_pattern

IGNORE_DIRS = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    "node_modules",
    ".venv",
    "venv",
    "dist",
    "build",
    ".mypy_cache",
    ".ruff_cache",
    "tmp",
}
SOURCE_EXTS = {".py", ".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".go", ".rs", ".html", ".vue", ".svelte"}
STYLE_EXTS = {".css", ".scss", ".less"}
JS_IMPORT_RE = re.compile(
    r"""(?:import\s+[\s\S]*?\s+from\s+|import\s+|export\s+[\s\S]*?\s+from\s+|require\s*\(\s*|@import\s+)(['"])([^'"]+)\1""",
    re.MULTILINE,
)
HTML_ASSET_RE = re.compile(r"""(?:src|href)\s*=\s*(['"])([^'"]+\.(?:js|jsx|ts|tsx|mjs|css|scss))\1""", re.IGNORECASE)
GO_IMPORT_RE = re.compile(r"""^\s*(?:import\s+)?(?:[a-zA-Z_][a-zA-Z0-9_]*\s+)?"([^"]+)"\s*$""", re.MULTILINE)
RUST_MOD_RE = re.compile(r"""^\s*(?:pub\s+)?(?:mod\s+([a-zA-Z0-9_]+)\s*;|use\s+crate::([a-zA-Z0-9_]+))""", re.MULTILINE)


def _matches_any(rel_path: str, patterns: list[str] | tuple[str, ...]) -> bool:
    return matches_any_pattern(rel_path, patterns)


def discover_governed_files(
    root: Path,
    source_roots: list[str],
    placeholder_names: set[str],
    harness_paths: list[str],
) -> list[str]:
    found: list[str] = []
    for raw_sr in source_roots:
        sr_path = root / raw_sr
        if not sr_path.exists():
            continue
        if sr_path.is_file():
            rel = sr_path.relative_to(root).as_posix()
            if sr_path.name not in placeholder_names:
                found.append(rel)
            continue
        for dirpath, dirnames, filenames in os.walk(sr_path):
            dirnames[:] = [d for d in sorted(dirnames) if d not in IGNORE_DIRS]
            for fname in sorted(filenames):
                if fname in placeholder_names or fname.startswith("."):
                    continue
                full = Path(dirpath) / fname
                if full.suffix.lower() not in (SOURCE_EXTS | STYLE_EXTS):
                    continue
                rel = full.relative_to(root).as_posix()
                matched_hps = [hp.rstrip("/") for hp in harness_paths if _matches_any(rel, [hp])]
                if matched_hps:
                    explicitly_rooted = any(
                        sr.rstrip("/") == rel or any(sr.rstrip("/").startswith(hp + "/") for hp in matched_hps)
                        for sr in source_roots
                        if sr.strip() not in ("", ".")
                    )
                    if not explicitly_rooted:
                        continue
                found.append(rel)
    return sorted(set(found))


def find_claiming_modules(rel_path: str, modules: dict[str, ModuleSpec]) -> list[str]:
    return sorted(mod_id for mod_id, spec in modules.items() if _matches_any(rel_path, spec.owns))


def _line_offsets(text: str) -> list[int]:
    offsets = [0]
    for idx, ch in enumerate(text):
        if ch == "\n":
            offsets.append(idx + 1)
    return offsets


def _offset_to_line(offsets: list[int], pos: int) -> int:
    return bisect.bisect_right(offsets, pos)


def _resolve_python_import(
    root: Path,
    source_file: str,
    module_name: str | None,
    level: int,
    source_roots: list[str],
) -> str | None:
    src_dir = (root / source_file).parent
    candidates: list[Path] = []
    parts = module_name.split(".") if module_name else []

    if level > 0:
        base = src_dir
        for _ in range(level - 1):
            base = base.parent
        target_base = base.joinpath(*parts) if parts else base
        candidates.extend([target_base.with_suffix(".py"), target_base / "__init__.py"])
    else:
        search_bases = [src_dir] + [root / sr for sr in source_roots if (root / sr).is_dir()] + [root]
        for base in search_bases:
            target_base = base.joinpath(*parts)
            candidates.extend([target_base.with_suffix(".py"), target_base / "__init__.py"])

    root_res = root.resolve()
    for cand in candidates:
        try:
            resolved = cand.resolve()
            if resolved.is_file() and resolved.is_relative_to(root_res):
                return resolved.relative_to(root_res).as_posix()
        except OSError:
            continue
    return None


def _resolve_asset_or_alias(root: Path, source_file: str, spec_str: str, source_roots: list[str]) -> str | None:
    bases: list[Path] = []
    if spec_str.startswith("."):
        bases.append((root / source_file).parent / spec_str)
    elif spec_str.startswith(("@/", "~/")):
        sub = spec_str[2:]
        for sr in source_roots:
            sr_dir = root / sr
            if sr_dir.is_dir():
                bases.append(sr_dir / sub)
        bases.append(root / sub)
    elif "/" in spec_str and not spec_str.startswith(("http:", "https:")):
        bases.append((root / source_file).parent / spec_str)
        for sr in source_roots:
            bases.append(root / sr / spec_str)
    else:
        return None

    root_res = root.resolve()
    for base in bases:
        candidates = [base] + [base.with_suffix(ext) for ext in (".ts", ".tsx", ".js", ".jsx", ".mjs", ".css", ".scss", ".vue", ".svelte")]
        candidates.extend([base / "index.ts", base / "index.tsx", base / "index.js"])
        for cand in candidates:
            try:
                res = cand.resolve()
                if res.is_file() and res.is_relative_to(root_res):
                    return res.relative_to(root_res).as_posix()
            except OSError:
                continue
    return None


def _resolve_rust_or_go(root: Path, source_file: str, ref: str, is_go: bool) -> str | None:
    root_res = root.resolve()
    if is_go:
        parts = ref.strip("/").split("/")
        for i in range(len(parts)):
            cand_dir = root.joinpath(*parts[i:])
            if cand_dir.is_dir():
                first_go = next(cand_dir.glob("*.go"), None)
                if first_go and first_go.resolve().is_relative_to(root_res):
                    return first_go.resolve().relative_to(root_res).as_posix()
        return None
    src_dir = (root / source_file).parent
    for cand in (src_dir / f"{ref}.rs", src_dir / ref / "mod.rs", root / "src" / f"{ref}.rs", root / "src" / ref / "mod.rs"):
        if cand.is_file() and cand.resolve().is_relative_to(root_res):
            return cand.resolve().relative_to(root_res).as_posix()
    return None


def scan_files_and_imports(
    root: Path,
    modules: dict[str, ModuleSpec],
    source_roots: list[str],
    placeholder_names: set[str],
    harness_paths: list[str],
    max_source_lines: int,
    max_style_lines: int,
    git_lag_churn: dict[str, tuple[int, int]],
) -> tuple[tuple[FileStat, ...], tuple[ImportEdge, ...], dict[str, ModuleTelemetry], dict[str, list[str]]]:
    """Scan governed files for line counts, role headers, ownership, and import boundaries."""
    rel_files = discover_governed_files(root, source_roots, placeholder_names, harness_paths)
    claims_map: dict[str, list[str]] = {}
    file_stats: list[FileStat] = []
    edges: list[ImportEdge] = []

    for rel in rel_files:
        claims = find_claiming_modules(rel, modules)
        claims_map[rel] = claims
        owner = claims[0] if len(claims) == 1 else None
        full_path = root / rel
        try:
            text = full_path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        line_count = len(text.splitlines())
        suffix = full_path.suffix.lower()
        is_style = suffix in STYLE_EXTS
        file_stats.append(
            FileStat(
                path=rel,
                lines=line_count,
                is_style=is_style,
                has_role_header=has_inline_role_header(text),
                owner_module=owner,
            )
        )

        if suffix == ".py":
            try:
                tree = ast.parse(text, filename=rel)
            except SyntaxError:
                continue
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        target_file = _resolve_python_import(root, rel, alias.name, 0, source_roots)
                        _record_edge(edges, rel, owner, alias.name, target_file, node.lineno, modules)
                elif isinstance(node, ast.ImportFrom):
                    target_file = _resolve_python_import(root, rel, node.module, node.level, source_roots)
                    if node.names:
                        for alias in node.names:
                            sub_mod = f"{node.module}.{alias.name}" if node.module else alias.name
                            sub_target = _resolve_python_import(root, rel, sub_mod, node.level, source_roots)
                            _record_edge(edges, rel, owner, sub_mod, sub_target or target_file, node.lineno, modules)
                    else:
                        _record_edge(edges, rel, owner, node.module or ".", target_file, node.lineno, modules)
            continue

        offsets = _line_offsets(text)
        if suffix == ".go":
            for match in GO_IMPORT_RE.finditer(text):
                ref = match.group(1)
                _record_edge(edges, rel, owner, ref, _resolve_rust_or_go(root, rel, ref, True), _offset_to_line(offsets, match.start()), modules)
        elif suffix == ".rs":
            for match in RUST_MOD_RE.finditer(text):
                ref = match.group(1) or match.group(2)
                _record_edge(edges, rel, owner, ref, _resolve_rust_or_go(root, rel, ref, False), _offset_to_line(offsets, match.start()), modules)
        else:
            for match in JS_IMPORT_RE.finditer(text):
                ref = match.group(2)
                target_file = _resolve_asset_or_alias(root, rel, ref, source_roots)
                _record_edge(edges, rel, owner, ref, target_file, _offset_to_line(offsets, match.start()), modules)
            if suffix in (".html", ".vue", ".svelte"):
                for match in HTML_ASSET_RE.finditer(text):
                    ref = match.group(2)
                    target_file = _resolve_asset_or_alias(root, rel, ref, source_roots)
                    _record_edge(edges, rel, owner, ref, target_file, _offset_to_line(offsets, match.start()), modules)

    telemetry: dict[str, ModuleTelemetry] = {}
    by_mod: dict[str, list[FileStat]] = {m: [] for m in modules}
    for fs in file_stats:
        if fs.owner_module and fs.owner_module in by_mod:
            by_mod[fs.owner_module].append(fs)

    for mod_id in modules:
        owned = by_mod[mod_id]
        total_loc = sum(f.lines for f in owned)
        biggest = max(owned, key=lambda x: x.lines, default=None)
        oversized = tuple(
            (f.path, f.lines)
            for f in owned
            if f.lines > (max_style_lines if f.is_style else max_source_lines)
        )
        lag, churn = git_lag_churn.get(mod_id, (0, 0))
        telemetry[mod_id] = ModuleTelemetry(
            module_id=mod_id,
            file_count=len(owned),
            total_loc=total_loc,
            max_file_path=biggest.path if biggest else "",
            max_file_loc=biggest.lines if biggest else 0,
            oversized_files=oversized,
            git_doc_lag_commits=lag,
            recent_commits=churn,
        )

    return tuple(file_stats), tuple(edges), telemetry, claims_map


def _record_edge(
    edges: list[ImportEdge],
    src_file: str,
    src_mod: str | None,
    raw_ref: str,
    target_file: str | None,
    lineno: int,
    modules: dict[str, ModuleSpec],
) -> None:
    if not target_file:
        return
    target_claims = find_claiming_modules(target_file, modules)
    target_mod = target_claims[0] if len(target_claims) == 1 else None
    if not target_mod or target_mod == src_mod:
        return
    allowed = bool(src_mod and src_mod in modules and target_mod in modules[src_mod].depends_on)
    edges.append(
        ImportEdge(
            source_file=src_file,
            source_module=src_mod,
            target_ref=raw_ref,
            target_module=target_mod,
            line=lineno,
            allowed=allowed,
        )
    )
