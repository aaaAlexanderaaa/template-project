# Templates

Files in this directory are inert examples. They become authoritative only
after being copied into the appropriate `docs/` directory, all placeholders
are replaced, and lifecycle metadata is set correctly.

| Need | Template | Destination |
|---|---|---|
| Cross-cutting behavior or invariant | `contract.md` | `docs/contracts/<topic>.md` |
| Frontend surface | `frontend-surface.md` | `docs/design/<surface>.md` |
| Style layers, shared visual values, override surface | `style-system.md` | `docs/contracts/<topic>-style-system.md` |
| Backend/service/state change | `backend-change.md` | `docs/contracts/<topic>.md` |
| Frontend + backend change | `cross-stack-change.md` | `docs/contracts/<topic>.md` |
| Implementation or migration | `implementation-plan.md` | `docs/plans/YYYY-MM-DD-<topic>.md` |
| Audit or defect batch | `issue-tracker.md` | `docs/issues/YYYY-MM-DD-<initiative>.md` |
| Durable verification | `verification-report.md` | `docs/evidence/YYYY-MM-DD-<topic>.md` |
| Cross-session continuation | `handoff.md` | `docs/evidence/YYYY-MM-DD-<topic>-handoff.md` |
| Operator or maintainer procedure | `guide.md` | `docs/guides/<topic>.md` |
| Risk-based agent execution | `agent-execution-plan.md` | `docs/plans/YYYY-MM-DD-<topic>.md` |
| Independent multi-perspective review | `independent-review.md` | `docs/evidence/YYYY-MM-DD-<topic>-review.md` |
| Fresh-context completion evaluation | `holistic-evaluation.md` | `docs/evidence/YYYY-MM-DD-<topic>-evaluation.md` |
| Evidence-preserving data boundary | `evidence-preserving-data.md` | `docs/contracts/<topic>-data.md` |
| Greenfield/brownfield adoption baseline | `adoption-assessment.md` | `docs/evidence/YYYY-MM-DD-adoption-assessment.md` |

Clock, calendar, and demonstration-data rules are not a separate copyable
template. They are owned by `docs/contracts/foundational-runtime-discipline.md`
and named in `ARCHITECTURE.md` runtime prompts when [development § activate-concerns](../docs/contracts/development-discipline.md#activate-concerns-instead-of-expanding-ceremony) activates them.
Backend, frontend, and cross-stack templates add delete-unless-activated
sections for those concerns. Do not copy a pit catalog into an adopting
architecture.

Routine work uses existing authority and no plan template. A controlled
experiment uses a disposable scratch record unless its findings support a
durable decision. `agent-execution-plan.md` is for material delivery; retain
its review topology only for high-risk work.

`ci/docs-check.example.yml` is an optional GitHub Actions adapter for the
repository's dependency-free Python 3.11+ documentation check and fixture
suite. Other CI systems should run the same commands in their native format.

The template inventory and required sections are declared in
`docs-policy.toml`; editing a template without reconciling that policy fails the
repository check.
