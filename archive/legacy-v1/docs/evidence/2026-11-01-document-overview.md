---
doc_type: evidence
status: historical
authority: evidence
last_reconciled: 2026-11-01
subject: on-demand-document-overview
---

# On-demand document overview verification

## Requested outcome and evidence boundary

The owner described recurring loss of permanent constraints, one-time work and
workflow follow-up during agent execution. They asked whether a script could
reorganize existing documents, with hook integration chosen by the executing
agent or adopting project. They accepted the on-demand overview and instructed
implementation on 2026-11-01. This is an English contextual account; the
[harness source and contract](../contracts/documentation-harness.md#document-overviews-expose-sources-before-concern-selection)
retain the decision and behavior.

The delivered boundary is local discovery and navigation through
`python3 scripts/read_rules.py overview`. This work does not establish sustained
attention, semantic priority selection, real article quality or host integration.
The existing behavioral-evaluation plan remains outside this authorization.

## Environment and baseline

macOS arm64, Python 3.14.2; baseline revision
`5a9303cb408af80de9bd4202c55a5c7445ee6138` plus this task's uncommitted changes.
The initial working tree was clean. The baseline suite passed 196 tests in
59.536 seconds. The existing checker passed with the overdue
`independent-adoption-review` advisory.

The previous reader exposed concern routes through `list` and delivered
selected full rules through `prepare` and `read`. It correctly rejected active
plans and issue records as operative rules. On the same controlled article
sources, `list` exposes the concern and owner slot but not the editorial
promise, issue dispositions, follow-up plan or unclassified note. The overview
locates those candidates before concern selection and preserves the reader's
lifecycle restriction.

[Process observations](2026-11-01-document-overview-observations.json) retain the
source-shaped files, exact CLI arguments, stdout/stderr, exits, environment and
implementation digests. [Peer review inputs and responses](2026-11-01-document-overview-review.json)
retain actual prompts and first judgments. Neither evidence source is a
longitudinal agent execution study.

## Observed results

| Scenario | Observation and supported result |
|---|---|
| Discover an unfamiliar article project | Actual CLI output identifies current editorial rules, target proposal, active follow-up, unresolved citation concern, accepted checker limitation and an unclassified local note. Source paths lead back to the originals. |
| Preserve permanent standards after a one-time repair | Source-shaped fixtures keep the current writing standard while completed plans, superseded rules and resolved/disproved findings leave the default live list. Accepted and wontfix dispositions remain distinct. |
| Expand only when useful | Default text maps documents and commitments. `--outline` exposes every operative heading, including H1 and closed-item navigation, outside frontmatter, examples and provenance. Mixed headings, findings and commitments follow source-line order. |
| Encounter unknown or contradictory data | Missing/unrecognized metadata remains visible; malformed records, bad UTF-8, unclosed examples and conflicting frontmatter keys produce explicit partial coverage. Unknown finding states are counted even when their document is on another page. |
| Reconcile a tracker | An issue tracker needing reconciliation still exposes declared item states. A mismatched authority becomes unclassified rather than promoting its content. |
| Audit omissions | JSON lists inactive paths and states; default text names that route. Scope, exclusions, all-category counts, shown/total/next offset and diagnostics remain visible. |
| Continue after a source change | File mutation or membership changes before output abort the read. A changed snapshot rejects continuation before stdout; matching source selection and calendar reference continue successfully. |
| Recover from failed access | Controlled read failures produce an unknown digest and partial view; a changed failure or recovery before output requires a rerun. Native denied file and root access return incomplete JSON and exit 2. A missing selected scope exits 2; a nonexistent/non-directory root is an invalid argument without a view. |
| Preserve source identity | Extra promise fields cannot replace the actual record id, kind or source line. Duplicate metadata keys fail both the overview and complete-rule reader. |
| Preserve date meaning | Dates stay calendar strings. Without `--today`, timing is unassessed; explicit dates label past/due/future without expiring current authority. Empty review dates remain invalid declarations instead of disappearing. |
| Keep access contained | Real escaping file and directory symlinks reveal no external content. Selected sources replace the defaults; a broken unselected entrypoint does not block a narrow scan. |
| Avoid tool side effects | A before/after fixture filesystem comparison is unchanged after text/JSON CLI calls. Source audit finds standard-library reads and output only; invocation installs no hook, task, cache or background process. |
| Browse a larger collection | Generated scale guard enumerates 1,000 documents through pages of 137, with one snapshot and no loss or duplicate. This is collection/paging evidence, not a universal latency or memory budget. |

An implementation self-check reproduced promise payload fields overwriting the
public source id/kind/line. The correction preserves source-derived locators
after copying fields; a sibling guard includes an attempted timing override.
A read-failure test initially failed to inject its fault because macOS resolved
the temporary path through a different canonical prefix. Resolving the fixture
path made the intended failure observable; it was not evidence of a product
access failure.

## Fresh-context consumer and implementation review

The configured ChatGPT Web tool creates isolated conversations. The first
review received the accepted scope, normal usage, contract, captured CLI
surfaces, complete new CLI source and relevant parser/lifecycle context. It
received no producer reasoning trace. The model name was not reported; the
account's model and thinking settings were left unchanged. Context separation
is achieved, while implementation and observation origins remain shared.

The first consumer identified current editorial rules, E-3 citation uncertainty,
E-2's accepted limitation, active follow-up and the unknown note. It kept the
target proposal separate and required explicit calendar assessment. Its
suggested `prepare --concern experience` omitted the owner binding. The actual
process failed without stdout and named `--owner experience=PATH`; following
that message with the editorial owner succeeded, delivering two complete units
and the final marker. The producer ran these commands; the peer inspected
their captured surfaces and did not operate the local filesystem.

The review also found missing text outline entries, conflated wontfix/accepted
dispositions, missing items in a tracker needing reconciliation, skipped empty
review dates, incomplete read-failure revalidation, incomplete calendar paging
instructions and source-order concerns. These were corrected and guarded.
The navigation exception for metadata-free README/AGENTS files and the invalid
root boundary are now explicit at the contract. Compact text keeps an explicit
route to JSON's exclusion inventory instead of duplicating every inactive path.

A second isolated review received the corrected contract and source, full
controlled fixture inputs and current process results. It judged the accepted
discovery/navigation outcome supported, while retaining the producer-executed
evidence limit. It identified one remaining root-access risk: a permission error
during root resolution could return 1 instead of an incomplete view and exit 2.
Root initialization is now inside the overview's partial-scan boundary and
rechecks a failed root access before emission. Native denied parent-directory
access returned incomplete JSON, a root diagnostic, exit 2 and empty stderr;
permissions were restored and the temporary directory removed. A sibling guard
checks changed root access. This final mechanical correction was verified
locally after the second review rather than claimed to have received another
peer review.

Additional actual CLI probes changed an issue tracker's lifecycle to
`needs_reconciliation` and retained its accepted/unverified items; changed
source bytes and observed stale continuation fail before stdout; and denied
read access to a selected source and observed an unknown digest with exit 2.
Each fixture's bytes and permissions were restored. The observation JSON
retains these process results separately from unit-level fault injection.

## Checks and reproduction

- Focused overview guards: 23 tests; the focused run passes in 3.576 seconds.
- Required full suite after the final correction: 219 tests pass in 62.140 seconds.
- Final documentation checker: passes with 74 canonical documents, 16 templates,
  full profile and adopted stage, with the same existing overdue-promise advisory.
- `git diff --check`: passes.

Run the delivered entrypoints from the checkout:

```sh
python3 scripts/read_rules.py overview
python3 scripts/read_rules.py overview --source docs/contracts --outline
python3 scripts/read_rules.py overview --format json --today 2026-11-01 --limit 5
python3 -m unittest discover -s tests -p 'test_*.py'
python3 scripts/check_docs.py
```

Recreate the consumer fixture by writing each `fixture_sources` key/value from
the process-observation JSON into an empty temporary directory. Run the same
`command_observations[].args` after `--root <directory>`. Snapshot hashes are
derived from source bytes and calendar reference; changed fixture inputs
require a new first page. Dispose of the temporary directory after the trial.

The actual repository scan before closure found 80 Markdown files, with 29
live/navigation documents and 51 inactive records, no unclassified documents or
scan diagnostics. Compact text was 8,160 bytes and took 0.1288 seconds; JSON
was 31,516 bytes and took 0.1466 seconds in that one observation. Earlier full
heading JSON was 121,840 bytes, motivating optional outline expansion. These
measurements describe those versions and sources, not a repeated speed study.

After lifecycle reconciliation, the actual scan finds 81 Markdown files, with
28 live/navigation documents and 53 inactive records. This completed plan leaves
the live view and appears in the exclusion inventory with status completed.
The consumer fixture was removed after comparing its restored bytes with the
retained fixture sources; native permission-probe directories were also removed.

## Limits and completion state

Controlled fixtures cover declared syntax and metadata, not semantic completeness
or obedience. Unit fault injection and native file/root permission failures are
recorded as distinct observations. Filesystem identity rechecks detect observed changes but
provide no lease against a later writer. Source reading and discovery remain
different results from applying the rules successfully in a real task.

The accepted local script outcome is complete: consumers can discover candidate
rules and working state, navigate to their originals, and recover complete
rules through the existing reader. Required checks pass and peer findings are
reconciled. Manual invocation and host integration remain choices of the using
project; behavioral benefit needs evidence from later real tasks.
