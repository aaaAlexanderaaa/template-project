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
  risk, or expose an external blocker.
- **Proactively supply engineering best practices**: Never assume the owner is a
  career software architect or frontend specialist. When the owner states a
  symptom or rough example, research mature engineering patterns and present
  concrete options with plain trade-offs instead of merely echoing the owner's
  example back.
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

- **1. Verbatim User Quotes (`docs/sources.toml`)**: Store the owner's exact
  words in their original language (`quote = '''...'''`) with `id = "SRC-NNN"`,
  `date`, `status = "active" | "deferred" | "retired"`, and brief `context`.
  Never translate or paraphrase `quote` into abstract summaries.
- **2. Architectural & Module Specs (`docs/specs/**/*.md` & `docs/decisions/ADR-*.md`)**:
  Record how requirements and technical constraints translate into boundaries
  and trade-offs. Link upstream `sources: [SRC-...]` and, when overturning an
  earlier choice, link `supersedes: [ADR-...]` so future sessions can see *why*
  the old approach was abandoned. Purely technical decisions state their
  technical rationale directly without inventing forced links to user quotes.
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

<!-- required-reading: self-supervision -->
## Self-Supervision Against Goodhart Drift

A vision narrowed into a target and then reduced to a proxy metric invites
Goodhart's Law—agents optimize the metric while degrading the real goal (for
example, compressing clear rules into cryptic slogans to pass a hard line-count
cap, or touching timestamps to satisfy a 90-day calendar rule).

Whenever a rule is skipped, gamed, or creates friction during real work,
diagnose which of four causes occurred before editing governance:

1. **Delivery gap**: The rule mattered, but nothing surfaced it when editing the
   affected files → wire it into `check_docs.py` diff nudges or file headers.
2. **Vague trigger**: The rule used broad labels (`"content"`, `"architecture"`)
   → rewrite the trigger around concrete objects and observable effects.
3. **Habitual corner-cutting**: Models repeatedly take a shortcut → enforce via
   a deterministic script check or copyable code exemplar in `examples/`.
4. **Faulty or Goodhart metric**: The rule itself slows healthy work or rewards
   performative compliance → revise or delete the rule against verbatim user quotes (`SRC-*`)
   instead of stacking extra reminders on top.
<!-- /required-reading: self-supervision -->
