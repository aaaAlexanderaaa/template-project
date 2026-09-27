---
doc_type: evidence
status: historical
authority: evidence
last_reconciled: 2026-09-27
subject: recurring-grill-role
---

# Grill role delivery evidence

## Claim and scope

The [delivery plan](../plans/2026-09-27-recurring-grill-questions.md) implements
the maintainer's request for stronger recurring questions and their selected
form: a separately invocable Grill role focused on goals, assumptions, and
proposals. The [guide](../guides/grill.md) supplies a short invocation and a
full assignment; [governance](../contracts/governance-decision-boundary.md#recurring-questions-challenge-consequential-decisions)
owns the recurring questions and decision boundaries.

This delivery adds portable role instructions and routes from existing
entrypoints. It does not install a runtime agent, schedule a recurring review,
or establish measured gains in real-project decisions.

The accepted revision extends this role to important problems under the current
owner's high-level goals and supported standards, including taste. It reuses
existing personal-context and independent-review boundaries. The initial review
below tested questioning mechanics; the revision has separate evidence below.

## Environment and repository checks

Baseline: clean repository at `898fcf0`, with this delivery in the working tree.
Python 3.12.13 on macOS; the repository requires Python 3.11 or newer.

Observed commands:

```sh
python3 -m unittest discover -s tests -p 'test_*.py'
python3 scripts/check_docs.py
python3 scripts/check_docs.py --strict
git diff --check
```

The test run used the installed Python 3.12 interpreter explicitly. It ran 118
tests in 15.511 seconds: 117 passed and one skipped. The skipped optional
unsupported-interpreter test looks for a command named `python3.9`, which was
unavailable. Normal and strict documentation checks passed. The whitespace
check passed. These observations verify repository integrity, not the quality
of future Grill judgments.

## Initial fresh consumer review

The independently dispatched context `/root/grill_consumer_review` received
the original request and the user's selected invocation form, the delivered
guide, entrypoint, and relevant governing contracts. It did not receive the
implementer's conversation, reasoning history, or delivery plan. Its assignment
was read-only and required actual first questions and answer-dependent next
steps for self-chosen cases outside the guide's worked examples, plus authority
and stopping checks. No input files changed during its initial evaluation.

The first returned judgment found no actionable defect. No correction or
second review was needed. The reviewer applied the instructions to these
self-chosen hypothetical cases; the answers are scenario branches, not actual
user decisions or measured product observations.

| Case | First consequential question and divergent next actions |
|---|---|
| A mandatory onboarding tour intended to improve useful first imports | Ask whether users cannot find the import action or cannot supply usable data; investigate sessions/failure evidence instead of asking the owner to guess. A discovery failure leads to comparing a direct entry point with a tour. A data-readiness failure instead raises whether the goal requires real imports or permits a clearly limited sample experience. Sample success cannot silently replace the original outcome. |
| A standing instruction requiring a second agent review for every task | Ask what additional defects review detects by task class and what repeated dispatch/context/review cost it adds. Benefits concentrated at behavior boundaries support a targeted trigger. Evidence of meaningful failures in minor work calls for further investigation and, where unresolved, the owner's assurance/cost trade-off. Neither branch authorizes changing instructions or launching workers during the investigation. |

The reviewer also exercised these boundaries:

- A settled ordinary task reuses purpose and scope and can finish without an
  interview or question ledger when no consequential gap remains.
- An unavailable owner leaves a bounded unresolved decision; hypothetical
  answers and silence do not become assent. Unaffected authorized investigation
  may continue.
- Existing implementation authorization returns to the execution owner after
  Grill. The role adds no approval gate or write authority; a newly material
  decision still follows the existing boundary.

The reviewer confirmed the entrypoint, guide, question owner, guide index,
contribution guidance, operation guide, and existing review/plan templates
provide a reachable, conditionally selected role. It found usable follow-up,
closure, and revisit instructions and correctly identified the deliverable as
portable guidance rather than a runtime agent.

## Maintainer-side reconciliation

The delivery owner inspected the role, governing questions, projections, and
review outputs against the original request and selected standalone form. The
recurring questions are defined once; the guide supplies execution rather than
a competing question bank. The original integrated-flow draft was replaced
before review and is not a second available default. The guide's later-session
procedure compares earlier reasoning with new observations, retaining both
supported answers and consequential changes. No behavioral runtime or
independent quality improvement is inferred from this inspection.

## Approved revision: goals, standards, and confidence

The revision's review packet contained the guide and governing section,
the original request and accepted scope, without executor rationale or the
earlier review verdict. Inputs included the public entrypoint and independent
review template, relevant governance, personal-context, delegation and
independence sections, and the existing onboarding route. Autonomous-operation
excerpts retained their standing-work scope. No private source, derived
personal details, or private locator was supplied.

All review cases were fictional. They test the delivered instructions, not
fidelity to any real person's private taste:

| Case and supplied evidence | Review assignment |
|---|---|
| A greenhouse bulletin at 08:00 reports temperature 22 C within 18–26 C and humidity 59% within 45–70%, current authorized readings, no sensor fault, and no immediate intervention indicated by these readings. The local checklist is complete. | Owner A needs an immediate visit decision under this temperature/humidity policy, accepts concise text, and excludes other hazards. Owner B needs to choose a trial response to recurring afternoon overheating and has accepted causal explanation over time, rejecting snapshots. No afternoon evidence is supplied. Judge the same artifact for each owner. |
| A migration report says the readiness envelope is fully harmonized, all ten datasets pass, verification can close, and the endpoint uses TLS 1.3. Logs show datasets 1–8 pass, 9–10 were not run because fixtures were unavailable, and TLS 1.3 negotiation succeeded. | Owner C requires all ten checks for readiness, treats unexplained status labels as a confidence concern, and accepts precise technical terms. Inspect claims and their scope; no release or implementation authority is given. |
| The artifact lists changed keys `retry_limit` and `request_timeout`; the diff changes exactly those two keys. | Owner D requested a correct key list. No taste source is supplied and the owner is unavailable. Judge the supported purpose and state limits. |
| A factually checked feature announcement says: "Good news! Saved views are here. Keep your favorite filters and get back to what matters. Available to every account today." | Both owners need to announce feature availability. Owner E selected a warm celebratory voice for a hobby newsletter and accepted openings such as "Good news!". Owner F selected a restrained technical changelog voice and rejected promotional openings and vague benefits. Neither requires more detail. Judge each accepted standard proportionately. |

### Review execution and limits

The first fresh subagent `/root/grill_standards_review` returned only a
workspace-credit error, with no substantive judgment. A configured gateway
fallback returned HTTP 401 / invalid API key, also without a judgment. Neither
was retried or counted as completed review.

The next fallback used a local reviewer client whose authentication status
reported logged in. It requested a fresh nonpersistent session with
customizations and tools disabled and only the supplied public packet. The
resource bound was one review call with a USD 3 client budget cap and a
180-second process deadline; a correction recheck was allowed only for an
actionable finding. That process timed out with empty result and error files
and was terminated. The cause is unknown; login status alone does not prove
that a request reached the model. No retry or correction recheck was made.

Actual dispatches: one native subagent, one gateway request using
`claude-sonnet-4-6`, and one local client invocation using its `sonnet` alias.
None returned a substantive first judgment. No token or billing report was
returned, so actual billed spend and the local alias's resolved model are
unknown. Failed dispatches are not review passes, and no independence claim is
made for the parent's own inspection. The required fresh consumer verification
remains incomplete; restore a usable independent reviewer and apply the packet
before closing this revision.

The post-revision Python 3.12 suite ran 118 tests in 16.041 seconds: 117 passed
and the same optional interpreter test skipped. Normal and strict documentation
checks passed after evidence reconciliation, covering 41 canonical documents
and 16 templates; whitespace passed. These checks do not substitute for the
missing independent judgment.

## Limitations and verdict

Repository checks and fresh consumer verification support completion of the
initial role-guidance delivery. The approved revision is still verifying until
its fresh consumer judgment is available. The contract remains behaviorally partial.
Scenario use can establish instruction usability and expose a defect; it
cannot establish sustained effectiveness across models, adopters, or projects.
