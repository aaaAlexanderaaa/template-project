# Test Suite

Run all unit and integration tests (Python 3.11+, or older Python with `tomli` installed):

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
```

Covers:
- Single-source loading, sharded multi-domain scaling, and validation (`test_ssot_and_check_docs.py`);
- `project.py` CLI, context packs, static HTML export, SVG geometry, and HTTP write-back APIs (`test_project_cli_and_server.py`);
- `read_rules.py` rule span preparation and external repository `onboard` inventory (`test_read_rules_and_onboard.py`);
- Engineering discipline transfer fidelity, `init` out-of-the-box checks, and cross-document consistency (`test_discipline_transfer_and_consistency.py`);
- Reference modular code exemplar (`test_reference_exemplar.py`).
