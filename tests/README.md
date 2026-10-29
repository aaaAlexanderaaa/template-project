# Tests

`test_check_docs.py` is the template repository's own infrastructure suite. It
copies the repository into temporary directories, introduces one controlled
contract violation at a time, and verifies that `scripts/check_docs.py` fails
with an actionable message. It also keeps valid variants and the untouched
template repository green.

`test_read_rules.py` exercises complete reading units, explicit dependencies,
owner and lifecycle selection, contained local paths, changed sources and
UTF-8 recovery. Fixtures exercise overlapping concerns and an analytical
surface whose dependencies recover a missed selection. Repository cases check
the actual global core, non-graphical Experience and complete service detail.
These checks establish the source-delivery boundary; the task procedure and
its independently reviewed scope cases evaluate the separate claim that the
right project outcome is selected and completed.

Published operative entrypoints keep whole-source access explicit. Same-context
tests revalidate current closure and metadata, distinguish retained and newly
delivered bodies, and reject malformed or cross-context receipts before output.
Reusing the Python repository object also starts a fresh transaction; an earlier
target selection cannot authorize a later current-only preparation.

Actual-template adoption cases use the repository's generic, backend,
cross-stack and frontend sources with the documented destination relocation.
They cover the established product-role default, required domain closure and
complete risk definitions, rather than only hand-authored fixture metadata.
Time preparation also obtains the shared intervention rules. CRLF and mixed
metadata fixtures check byte-preserving preparation and recovery. Root-file
cases distinguish declared tooling from unclaimed or declared application code.

The same suite runs after trimming templates to `minimal` or `standard`.
Template-specific tests report skips outside the selected profile or when an
optional source is absent; missing required templates still fail. General
checker and reader cases continue to run without restoring deleted templates.

Run it with Python 3.11 or newer:

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
```

Adopted projects should keep this suite and add their own unit, integration,
architecture, lifecycle, and user-visible checks. Organize those tests around
contracts and failure categories rather than mirroring implementation files
mechanically.
