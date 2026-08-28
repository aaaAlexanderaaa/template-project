# Contributing

The portable documentation checker and its fixture suite require Python 3.11
or newer and have no third-party package dependencies.

## Before starting

1. Classify the request: explanation, diagnosis, feature, defect, migration,
   or operation.
2. Locate the current authority using `docs/README.md`.
3. Confirm the behavior owner and dependency boundary in `ARCHITECTURE.md`.
4. Check for contradictory contracts, active plans, or unresolved issues.
5. For agent-driven work, select the smallest route in the agent execution
   contract. Routine work uses existing authority and no plan; a controlled
   experiment answers an unknown technical fact without becoming delivery.
6. For material delivery, land the contract. Human contributors normally use
   `templates/implementation-plan.md`; agent-driven material work uses
   `templates/agent-execution-plan.md`, with its independent review sections
   retained only for high-risk work.
7. For template adoption, follow `docs/guides/onboarding.md`, preserve existing
   authority, and record the human-confirmed profile, managed scope, priority
   source, and adoption stage before enabling broad gates.
8. Resolve uncertainty through development D10-D12 and governance G7: research
   unfamiliar references, seek a capability-preserving tool fallback, and ask
   for a bounded human choice only when the decision belongs outside the
   reversible engineering envelope. When several such decisions depend on one
   another, use the decision-frontier procedure in
   `docs/guides/project-operation.md`.

## During the change

- Keep an active plan current enough that a fresh contributor can continue
  without conversation history.
- Record decisions and changed requirements in the relevant contract, not only
  in chat or commits.
- Preserve unrelated changes.
- When a defect mechanism has repeatable siblings, add a proportionate
  class-level guard while implementing; record why a local fix is sufficient
  when it does not.
- Keep verification evidence tied to the claim it supports.
- Keep product direction and priority with the declared human owner. Separate
  facts, risks, recommendations, required decisions, and execution blockers.
- Answer the stated question while surfacing any evidence-backed premise or
  risk that is materially more consequential. Explain its causal mechanism;
  do not turn it into unrequested implementation.
- For material work, preserve fixture identity and the observed failing
  acceptance check before implementation.
- Link every activated concern to the current/target contract that owns its
  boundary and failure/escalation policy. Plans carry steps and evidence, not
  duplicate policy.
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
- If the change displays, stores, or schedules time, does it consume the
  Time and calendar owner rather than the host or browser zone?
- If operators or customers will see seed or demo data, is it relative to
  that clock, environment-gated, and free of hardcoded live calendar dates?
- Does every visual value the change introduces resolve to a declared owner, or
  to a registered exception with an owner and a removal condition?
- Does each frontend direction trace to a concrete subject, audience, user job,
  and raw brief; were generic defaults, interface language, and any signature
  element deliberately reviewed before implementation?
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
- Were unfamiliar external claims verified against primary or official sources
  rather than reconstructed from memory?
- When a tool failed, was the required capability attempted through a fallback
  with equivalent semantics and evidence, or was the remaining limitation made
  explicit?
- Does the analysis explain the causal mechanism and its boundary, and does any
  requested human choice represent a genuine product, trade-off, authority, or
  risk decision rather than a resolvable fact or reversible local choice?
- When human decisions depended on one another, did the inquiry work only the
  prerequisite-safe frontier and obtain shared-understanding confirmation
  before dependent material work?

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
