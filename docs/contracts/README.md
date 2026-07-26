# Contracts

This directory contains long-lived, normative behavior and invariant
contracts. A current contract answers what must remain true independently of a
particular implementation plan.

Use `templates/contract.md`, `templates/backend-change.md`, or
`templates/cross-stack-change.md` as a starting point.

`agent-execution-discipline.md` is a selectable execution profile for material
or high-risk work performed by coding agents. This template uses it for its own
material agent work; adopted projects confirm their depth during onboarding.
It complements rather than overrides `development-discipline.md`: contracts
still own behavior, while the agent profile governs risk classification,
fixture/test phases, independent review, fresh-context evaluation, and layered
completion.

`governance-decision-boundary.md` keeps product direction, priority, trade-offs,
and risk acceptance with declared human owners while defining the framework's
advisory outputs and narrow execution blockers.

`project-adoption.md` defines AI-guided greenfield and brownfield onboarding,
current-state preservation, managed scope, and staged enforcement.

Contracts that declare `## Source anchors` use dated `source[N]` headings and
adjacent `- from: source[N]` citations. Once the section exists, definitions and
references are bidirectional and mechanically enforced.

Do not put step-by-step execution history here. Do not mark a future design as
current merely because implementation has started.
