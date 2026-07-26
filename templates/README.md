# Templates

Files in this directory are inert examples. They become authoritative only
after being copied into the appropriate `docs/` directory, all placeholders
are replaced, and lifecycle metadata is set correctly.

| Need | Template | Destination |
|---|---|---|
| Cross-cutting behavior or invariant | `contract.md` | `docs/contracts/<topic>.md` |
| Frontend surface | `frontend-surface.md` | `docs/design/<surface>.md` |
| Backend/service/state change | `backend-change.md` | `docs/contracts/<topic>.md` |
| Frontend + backend change | `cross-stack-change.md` | `docs/contracts/<topic>.md` |
| Implementation or migration | `implementation-plan.md` | `docs/plans/YYYY-MM-DD-<topic>.md` |
| Audit or defect batch | `issue-tracker.md` | `docs/issues/YYYY-MM-DD-<initiative>.md` |
| Durable verification | `verification-report.md` | `docs/evidence/YYYY-MM-DD-<topic>.md` |
| Cross-session continuation | `handoff.md` | `docs/evidence/YYYY-MM-DD-<topic>-handoff.md` |
| Operator or maintainer procedure | `guide.md` | `docs/guides/<topic>.md` |

`ci/docs-check.example.yml` is an optional GitHub Actions adapter for the
repository's dependency-free Python 3.11+ documentation check and fixture
suite. Other CI systems should run the same commands in their native format.

The template inventory and required sections are declared in
`docs-policy.toml`; editing a template without reconciling that policy fails the
repository check.
