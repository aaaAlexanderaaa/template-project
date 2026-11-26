---
doc_type: contract
status: current
authority: normative
---

# Collaboration, Governance & Bidirectional Lineage

<!-- required-reading: governance-boundary -->
## Decision Authority Boundary

Product direction, scope priority, irreversible external side effects, and risk
acceptance belong to the human owner. Local technical structure, reversible
implementation choices, and factual investigation belong to the engineering
agent:

- **Investigate before asking**: Resolve checkable technical facts from code,
  Git history, local tests, and primary documentation before asking the owner.
- **Ask only at genuine forks**: Escalate to the human owner (and record a
  `blocked` task with `blocker_question` in `work.toml` when asynchronous) only
  when new facts alter product intent, user-visible promises, security/data
  risk, or expose an external blocker; never invent extra approval ceremonies
  on your own.
- **Proactively supply engineering best practices**: Never assume the owner is a
  career software architect or frontend specialist. When the owner states a
  symptom or rough example, research mature engineering patterns and present
  concrete options with plain trade-offs instead of merely echoing the owner's
  example back.
- **Separate primary goals from side fixes in owner choices**: When presenting
  options, keep the owner's requested goal separate from opportunistic script
  fixes or legacy cleanup instead of bundling both into one recommended option,
  and state the real change footprint plainly.
<!-- /required-reading: governance-boundary -->

<!-- required-reading: three-perspectives -->
## Three-Perspective Pre-Code Judgment

Replace rigid pre-code forms with three simultaneous questions before touching
implementation:

1. **Executor**: Which constraints are already settled by the owner (`SRC-*`
   and current `ADR-*`), and which choices remain open? Follow settled choices;
   propose an alternative only when concrete evidence shows a substantially
   better result.
2. **Collaborator**: How close is the owner's current statement to a stable
   design? During early exploration, build small working slices and avoid
   locking premature ceremony; once direction settles, write clear boundaries
   into the owning module spec.
3. **Senior Architect**: What `stage` (`prototype`, `usable`, `stable`) governs
   this domain, and what single engineering property (speed of validation,
   clean module seams, or backward-compatible reliability) determines success
   right now?
<!-- /required-reading: three-perspectives -->

<!-- required-reading: three-level-bidirectional-lineage -->
## Three-Level Bidirectional Lineage

Preserve intent across sessions and design pivots without duplicating prose:

- **1. Verbatim User Quotes (`docs/sources.toml`)**: Record only owner quotes
  that **substantively shape or redirect project direction, boundaries, or
  design choices** (not routine chat or minor wording tweaks). Order entries
  chronologically (earliest first) and store the owner's exact unedited words
  in their original language (`quote = '''...'''`) with `id = "SRC-NNN"`,
  `date`, `status = "active" | "deferred" | "retired"`, and brief `context`.
  Never translate, condense, or paraphrase `quote` into processed summaries.
  Text the owner selects or pastes as an answer (for example an option the
  agent proposed) counts as the owner's answer and may be recorded in `quote`;
  `context` must then say which part the agent wrote. Preset options picked in
  the web overview stay on the task as `selected_option`.
- **2. Architectural & Module Specs (`docs/specs/**/*.md` & `docs/decisions/ADR-*.md`)**:
  Record how requirements and technical constraints translate into boundaries
  and trade-offs. Link upstream `sources: [SRC-...]` and, when overturning an
  earlier choice, link `supersedes: [ADR-...]` so future sessions can see *why*
  the old approach was abandoned. A module spec's `sources` list only quotes
  about that module. A quote behind a cross-module decision is recorded once in
  the ADR's `sources` with `affects`; `project.py context` shows it on each
  affected module as a one-line reference and `project.py trace` shows the full
  text. `check_docs.py` reports a spec that re-lists a quote an ADR already
  brings. Purely technical decisions state
  their technical rationale directly without inventing forced links to user quotes.
- **3. Implementation & Work Queue (`owns` globs & `docs/work.toml`)**: Module
  specs claim concrete source paths via `owns`, and `work.toml` links tasks and
  milestones to module/ADR/source IDs.

Both directions stay mechanically queryable via `python3 scripts/project.py trace <id>`:
- **Downstream (`Quotes → Specs → Tasks & Code`)**: Check which specs, modules,
  and tasks fulfill a user quote—and surface active quotes that have zero
  coverage or open gaps.
- **Upstream (`Code → Specs → Quotes`)**: Starting from any source file or
  oversized module, trace why it exists, what user promise it serves, and which
  original quote anchored it.
<!-- /required-reading: three-level-bidirectional-lineage -->

<!-- required-reading: inquiry-and-fallback -->
## Research & Capability-Preserving Fallback

- Verify unfamiliar APIs, standards, and external claims against primary
  sources rather than reconstructing from memory; cross-check non-trivial
  design questions across more than one angle or pass.
- When a tool or integration is unavailable (for example, an offline bridge or
  sandbox restriction), switch to a capability-preserving fallback with
  comparable evidence quality or report the exact remaining boundary plainly.
<!-- /required-reading: inquiry-and-fallback -->

<!-- required-reading: expectations-and-resolutions -->
## Judgments, Expectations & Three Resolutions

A model remembers nothing between sessions; it knows what the project documents
tell it. So the discipline corrects itself through its documents:

- **A judgment states its expectation**: what should happen because of it, and
  what would show it is wrong. Judgments are ADRs, module `promise`s, checks
  that can fail the build, and the project's health constraints.
- **An expectation violation is recorded under the judgment it contradicts**,
  when it is seen, and ends in one of three resolutions:
  - **Revise the expectation**: the expectation was wrong; change or retire the
    judgment. This is how rules are removed.
  - **Correct the phenomenon**: the expectation is right; fix the code or
    documents.
  - **Accept with a stronger description**: the old expectation described part
    of the picture; write one description that covers both and can still be
    contradicted. An exception attached to the old text does not count.
    Accepting a minor violation is recorded the same way, so later sessions do
    not argue it again.
- **The project's goal and the owner quotes decide which resolution applies**;
  who decides follows the authority boundary above.
- **Health constraints live in `ARCHITECTURE.md`, next to the goal they
  serve**. The project chooses a few and adjusts them sparingly against the
  goal.
- **Numbers remind; only facts fail the build.** A check fails the build only
  when a script can decide right or wrong. A number that stands in for a
  judgment (a line count meaning "too big") only reminds.
- **In a holistic review**, judgments with open violations come first, and
  removing something is the first option considered. Subtraction means
  rethinking how to achieve the goal cleanly without piling up debt, never
  abandoning the goal; before reworking a side task or review finding, verify
  that it still serves the main goal or drop it.
<!-- /required-reading: expectations-and-resolutions -->
