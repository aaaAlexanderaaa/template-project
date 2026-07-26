# Issues

This directory is the durable ledger for defects, audits, and post-mortem
findings. Use `templates/issue-tracker.md`.

Per-item lifecycle:

- `unverified`: reported but not independently checked;
- `verified`: evidence confirms the claim;
- `disproved`: evidence contradicts the claim;
- `partial`: the claim requires refinement;
- `accepted`: real and intentionally accepted;
- `wontfix`: real but deliberately not addressed;
- `resolved`: fixed with contract impact and class-level guard recorded.

An issue controls its own lifecycle. If resolving it changes intended behavior,
the relevant contract must be updated separately.
