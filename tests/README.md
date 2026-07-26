# Tests

`test_check_docs.py` is the template repository's own infrastructure suite. It
copies the repository into temporary directories, introduces one controlled
contract violation at a time, and verifies that `scripts/check_docs.py` fails
with an actionable message. It also keeps valid variants and the untouched
template repository green.

Run it with Python 3.11 or newer:

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
```

Adopted projects should keep this suite and add their own unit, integration,
architecture, lifecycle, and user-visible checks. Organize those tests around
contracts and failure categories rather than mirroring implementation files
mechanically.
