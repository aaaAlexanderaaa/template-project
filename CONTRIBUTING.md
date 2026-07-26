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
6. For agent-driven work, classify the risk using
   `docs/contracts/agent-execution-discipline.md`; use
   `templates/agent-execution-plan.md` for material or high-risk execution.
7. For template adoption, follow `docs/guides/onboarding.md`, preserve existing
   authority, and record the human-confirmed profile, managed scope, priority
   source, and adoption stage before enabling broad gates.

## During the change

- Keep an active plan current enough that a fresh contributor can continue
  without conversation history.
- Record decisions and changed requirements in the relevant contract, not only
  in chat or commits.
- Preserve unrelated changes.
- Add class-level guards while implementing, rather than scheduling them as
  unspecified future cleanup.
- Keep verification evidence tied to the claim it supports.
- Keep product direction and priority with the declared human owner. Separate
  facts, risks, recommendations, required decisions, and execution blockers.
- For material work, preserve fixture identity and the observed failing
  acceptance check before implementation.
- For high-risk work, commission the required independent perspectives and
  fresh-context evaluation, or record the exact blocked/governance-exception
  state. Do not self-attest independence.

## Review questions

- Is there exactly one authoritative owner for every changed invariant?
- Can a future contributor distinguish current, target, historical, and
  superseded documents?
- Does the implementation match the contract's states, triggers, errors, and
  non-goals?
- Does the test suite guard the failure category, not only the reported input?
- Are frontend and backend projections self-consistent?
- Does every visual value the change introduces resolve to a declared owner, or
  to a registered exception with an owner and a removal condition?
- Are failure, recovery, observability, migration, and rollback addressed where
  relevant?
- Can the evidence be reproduced in the declared environment?
- Is the risk profile honest, and is claimed review independence demonstrated
  by the review context rather than by labels?
- Does the completion claim name the correct layer instead of promoting task
  completion into objective or release completion?
- Does selected work trace to a declared priority source or explicit human
  choice, rather than an agent-authored ranking?
- If governance blocks execution, is the blocker class allowed, evidence-backed,
  scoped to one path, and paired with recovery or a human decision?

## Definition of done

A material change is done only when:

- the normative contract is current and reconciled;
- the complete intended behavior is implemented;
- relevant class-level, integration, lifecycle, and user-visible checks pass;
- durable evidence is stored at the appropriate level;
- the implementation plan and related issues have final lifecycle states;
- operational guidance is updated if users or maintainers must act differently.
- independent design and holistic review evidence exists where the recorded
  risk requires it, or the work remains truthfully open under a documented
  human governance exception.

Run the documentation check before handoff:

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
python3 scripts/check_docs.py
```
