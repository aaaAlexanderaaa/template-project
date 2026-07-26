# Contributing

The portable documentation checker and its fixture suite require Python 3.11
or newer and have no third-party package dependencies.

## Before starting

1. Classify the request: explanation, diagnosis, feature, defect, migration,
   or operation.
2. Locate the current authority using `docs/README.md`.
3. Confirm the behavior owner and dependency boundary in `ARCHITECTURE.md`.
4. Check for contradictory contracts, active plans, or unresolved issues.
5. For a material change, copy the appropriate file from `templates/` and land
   the contract before implementation.

## During the change

- Keep an active plan current enough that a fresh contributor can continue
  without conversation history.
- Record decisions and changed requirements in the relevant contract, not only
  in chat or commits.
- Preserve unrelated changes.
- Add class-level guards while implementing, rather than scheduling them as
  unspecified future cleanup.
- Keep verification evidence tied to the claim it supports.

## Review questions

- Is there exactly one authoritative owner for every changed invariant?
- Can a future contributor distinguish current, target, historical, and
  superseded documents?
- Does the implementation match the contract's states, triggers, errors, and
  non-goals?
- Does the test suite guard the failure category, not only the reported input?
- Are frontend and backend projections self-consistent?
- Are failure, recovery, observability, migration, and rollback addressed where
  relevant?
- Can the evidence be reproduced in the declared environment?

## Definition of done

A material change is done only when:

- the normative contract is current and reconciled;
- the complete intended behavior is implemented;
- relevant class-level, integration, lifecycle, and user-visible checks pass;
- durable evidence is stored at the appropriate level;
- the implementation plan and related issues have final lifecycle states;
- operational guidance is updated if users or maintainers must act differently.

Run the documentation check before handoff:

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
python3 scripts/check_docs.py
```
