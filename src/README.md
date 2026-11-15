# Product Source Root Placeholder

In `template-project` itself, this directory is an empty starter placeholder (`[project].identity = "template"`).
To start a new product repository cleanly with initialized rules, ledgers, tests, and `src/`, run:

```bash
python3 scripts/project.py init --target /path/to/new-repo --name "My Product" --lang en
```

Follow the layered modular pattern shown in [../examples/reference-app/](../examples/reference-app/), keep `[project].identity = "product"` and `[layout].source_roots = ["src"]` in [../docs-policy.toml](../docs-policy.toml), and claim each module's directory in `docs/specs/`.
