# Plans

Plans describe how one coherent change reaches its end state. They carry
`authority: planning` and never override current contracts.

Use `templates/implementation-plan.md`. A useful plan includes:

- authoritative contracts;
- current facts and baseline evidence;
- complete end state;
- dependency-ordered execution within that change;
- affected files or systems;
- risks, failure handling, migration and rollback;
- verification and completion evidence;
- explicit non-goals.

When finished, mark the plan `completed`; when replaced, mark it `superseded`
and link its successor.

`2026-08-24-foundational-runtime-discipline.md` completed the task-layer
landing of the recognition rule plus the time/calendar and
demonstration-data invariants activated through [development § activate-concerns](../contracts/development-discipline.md#activate-concerns-instead-of-expanding-ceremony).
A sibling-incident register was retracted.
Adopter effectiveness remains partial on the owning contract.

`2026-08-27-collaboration-constraints-adoption.md` lands five constraints
selected from an external archive review: written parallel-work coordination
([agent-execution § written-coordination](../contracts/agent-execution-discipline.md#parallel-work-is-coordinated-in-writing)), durable recording of recurring verbal rules ([development § durable-recording](../contracts/development-discipline.md#recurring-verbal-rules-are-proposed-for-durable-recording)), handoff template
fields, authorship triage for external material ([adoption § authorship-triage](../contracts/project-adoption.md#external-material-is-triaged-by-authorship-before-adoption)), and a plain-wording
language style in the documentation authority map.

`2026-08-28-engineering-judgment-discipline.md` lands the mined
engineering-judgment material: [governance § advice-preserves-disagreement](../contracts/governance-decision-boundary.md#advice-preserves-disagreement) problem-report fields, extended [development § activate-concerns](../contracts/development-discipline.md#activate-concerns-instead-of-expanding-ceremony) minimum
questions, [development § fix-the-category](../contracts/development-discipline.md#fix-the-category-not-only-the-symptom) postmortem feed, a new target contract for judgment method,
and the engineering reading list.

`2026-08-28-invariant-identifier-redesign.md` replaces letter-coded
invariant identifiers with validated heading-slug citations: documentation
[harness § invariant-citations](../contracts/documentation-harness.md#invariant-citations-resolve-to-headings) owns the convention and transition, the checker resolves link
fragments (advisory first), and the engineering-judgment contract is the
pilot cutover.
