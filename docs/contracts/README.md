# Contracts

This directory contains long-lived, normative behavior and invariant
contracts. A current contract answers what must remain true independently of a
particular implementation plan.

Use `templates/contract.md`, `templates/backend-change.md`, or
`templates/cross-stack-change.md` as a starting point.

Contracts that declare `## Source anchors` use dated `source[N]` headings and
adjacent `- from: source[N]` citations. Once the section exists, definitions and
references are bidirectional and mechanically enforced.

Do not put step-by-step execution history here. Do not mark a future design as
current merely because implementation has started.
