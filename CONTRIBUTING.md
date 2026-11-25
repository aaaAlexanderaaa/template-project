# Contributing

All scripts and tests use only the Python standard library. They need a TOML
reader: Python 3.11+ includes one; on older Python, install `tomli`.

## Workflow

1. **Read context first**: Run `python3 scripts/project.py context <path-or-id>`
   to inspect the owning spec, linked user quotes, decisions, and open tasks
   before editing unfamiliar files.
2. **Write plainly**: Follow [docs/README.md](docs/README.md#language-standard)
   in every document, CLI message, and UI string.
3. **Keep one home per fact**:
   - Store verbatim user quotes in `docs/sources.toml`;
   - Store module responsibilities, `owns` patterns, `depends_on`, and `mermaid`
     diagrams in the owning `docs/specs/<domain>/<module>.md` or
     `docs/design/<surface>.md`;
   - Record cross-module trade-offs in `docs/decisions/ADR-*.md`;
   - Update milestone and task state in `docs/work.toml` by ID;
   - Keep a 2–3 line `# Role:` header at the top of source files and entrypoints.
4. **Verify end-to-end**:

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
python3 scripts/check_docs.py
```
