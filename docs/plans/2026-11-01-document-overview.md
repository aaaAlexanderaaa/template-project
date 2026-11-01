---
doc_type: plan
status: completed
authority: planning
last_reconciled: 2026-11-01
implements: docs/contracts/documentation-harness.md
supersedes: []
---

# Discover project concerns through an on-demand document overview

## Cold-start summary

The owner asked for a script that reorganizes existing documents into a usable
view. This project supplies the tool; the executing agent and adopting project
decide whether to call it manually or integrate it with a host hook. On
2026-11-01 the owner accepted that design and instructed implementation.

The bounded outcome is a working text/JSON overview through `read_rules.py`,
with traceable current rules, working state, review commitments and unknown
classification. Existing documents retain ownership and lifecycle; complete
rule preparation remains unchanged. This delivery does not install hooks,
build a scheduler or establish that future agents will reliably obey rules.

Baseline: the working tree was clean; 196 tests passed. The documentation
checker passed with the existing overdue independent-adoption-review advisory.
The reader currently provides list, prepare and read. Its concern selection
comes from the caller, and its source resolver correctly rejects active work
records as operative rules. There is no overview command.

## Risk classification

Material: a new local CLI and versioned output interface. The operation is
read-only and contained within explicitly selected repository sources. It adds
no privileges, dependency, persistent state or autonomous execution. A fresh
consumer review covers usability, authority distinctions and recovery before
closure; the high-risk design-review route is not activated.

## Authority and prerequisites

- [Harness owner](../contracts/documentation-harness.md#document-overviews-expose-sources-before-concern-selection): CLI, projection, source integrity and integration boundary.
- [Task context](../README.md#task-context): applicability and complete reading.
- [Delivery](../contracts/agent-execution-discipline.md#material-delivery-follows-the-outcome-and-its-evidence): material work and evidence.
- [Time](../contracts/foundational-runtime-discipline.md#time-and-calendar): calendar-date meaning and explicit reference injection.
- Human authority: the owner's acceptance and instruction to implement on 2026-11-01.

## Engineering decision envelope

Implement the overview, shared parsing where useful, regression tests, usage
documentation and verification records. Keep source documents authoritative,
preserve existing reader commands, and report discovery limits. No additional
human decision is required for these reversible choices. The unrelated
behavioral-evaluation pilot keeps its own authorization and pending decisions.

## Activated concerns and owners

Compatibility, state integrity, security/privacy, performance/cost,
reliability/operations, dependency/build integrity and command-line experience
use the harness owner. They cover schema identity, source/membership rechecks,
contained paths, explicit coverage and paging, failure recovery, standard-library
portability and readable output. Time/calendar uses the foundational owner and
the overview's explicit date projection policy. No clock-based scheduling or
semantic ranking is introduced.

## Complete end state

- One optional command exposes declared current/target rules, working records,
  guidance, explicit commitments and unclassified sources before concern selection.
- Each item leads to original text and source identity. Unknown states remain
  visible; closed one-time records leave attention without erasing permanent rules.
- Text and versioned JSON convey incomplete scans, exclusions and pagination.
- Changing a source invalidates snapshot continuation; existing full reading,
  lifecycle restrictions and recovery remain available.
- Usage documentation enables manual use and explains caller-owned host integration.

## Execution and verification

1. Reconcile the harness contract before implementation; reuse parser and record
   semantics rather than adding a second tracker or trigger registry.
2. Add the overview CLI and contained, stateless document projection. Guard
   authority/lifecycle distinctions, source changes and unknown data with fixtures.
3. Exercise the actual command on this repository and on source-shaped fixtures:
   new-context discovery, closed/accepted findings, stale sources, malformed
   records, unrelated/historical material and a non-default source layout.
4. Obtain a fresh consumer judgment from a self-contained artifact packet,
   resolve material findings, then run the required suite and checker.

The comparison holds source documents fixed while contrasting the existing
concern list with the new overview. It tests discovery and navigation, not
longitudinal model behavior. Generated scale coverage tests enumeration and
paging only; elapsed time is observed rather than given an invented budget.

## Work-selection fallback

Continue through the bounded implementation and verification above. Stop at its
observed completion; unrelated active plans remain with their own owners.

## Verification and evidence matrix

| Outcome | Evidence | Status |
|---|---|---|
| Declared roles and unknowns are discoverable | Source-shaped fixtures and actual CLI output | passed |
| One-time closure preserves lasting constraints | Mixed lifecycle/finding/promise fixtures | passed |
| Source identity and incomplete coverage are honest | Mutation, escaping path, native denied access, malformed input and paging guards | passed |
| Tool has no installation or source-write effects | CLI filesystem comparison and source audit | passed |
| Operator can find and open the required source | Fresh artifact consumer review and producer-executed entrypoint probes | passed within that evidence boundary |
| Existing preparation and checker behavior remain valid | 219 unit tests and documentation checker | passed; existing overdue-promise advisory retained |

## Layered completion

The bounded script delivery is complete. The tool discovers source roles and
working state, preserves unknowns and source identity, and provides manual
text/JSON entrypoints with recovery. Improved sustained attention and automatic
host integration remain unclaimed. The [verification record](../evidence/2026-11-01-document-overview.md)
identifies the observations, peer findings, corrections and limits.

## Progress and closure

Implemented and verified on 2026-11-01. Fresh ChatGPT artifact review found a
usable discovery path and exposed several state/recovery defects, which were
corrected. The final root-permission finding was reproduced with native denied
directory access, fixed and verified. All 219 tests pass. Contract, usage,
evidence and plan lifecycle are reconciled; no task-specific blocker remains.
The bounded end is reached, with host integration left to its using owner.
