---
doc_type: plan
status: active
authority: planning
last_reconciled: 2026-11-01
implements: docs/contracts/development-discipline.md
supersedes: []
---

# Behavioral evaluation of the discipline

## Cold-start summary

On 2026-11-01 an external review of this repository, made by a model new to
it, reported two problems the owner called real and long-term, to be kept in
view: the rules only grow, and nobody can tell which rules change agent
behavior, because there is no comparison against working without them and no
behavioral regression check. The owner agreed to invest in a repeatable set of
behavioral cases and a three-way comparison (no discipline, a minimal core, the
full core), and asked for the design to be thought through.

This plan is that design. When run, it tells the owner which parts of the
startup core change what agents do, in which direction, and at what cost. It
also gives the owner evidence for adding or retiring a startup rule: a rule
that changes a case has shown its effect. Asked about the pilot, the owner said
that in this repository a run needs their explicit consent and that most work
here needs no automatic trigger. A round therefore runs only when the owner
asks for it; no rule change, check, correction or schedule starts one.

Verified current facts:

- Earlier trials compared instruction snapshots through subagents in this
  workspace. The [2026-10-19 trial](../evidence/2026-10-19-recursive-improvement.md)
  records its own limits: both contexts inherited the workspace `AGENTS.md`,
  each snapshot ran once, tasks named their problems, no run used no
  discipline, and the trial could not isolate an instruction effect.
- [Proposed behavioral cases](../evidence/2026-09-06-template-review/behavioral-cases.json)
  with hidden faults exist and are all `not_run`.
- The startup core measured 101.7 KB and 13,805 words across nine units before
  the 2026-11-01 rewrite, 97.0 KB and 13,190 words after its first pass, and
  104.4 KB and 14,257 words after the repairs and verbatim restorations.
- `promise[independent-adoption-review]` in the
  [execution promise register](../contracts/agent-execution-discipline.md#promise-register)
  has been overdue since 2026-10-24. This evaluation supplements it and leaves
  it with the owner.

Next action: the owner settles the decisions listed under the decision
envelope; then build the runner and run the pilot.

## Risk classification

- Profile: material. It adds evaluation tooling and durable evidence and
  spends model budget; it changes no product behavior, permission or published
  integration.
- Rationale: wrong conclusions would steer future rule changes, so cases and
  predictions are frozen before runs, and results are interpreted with the
  limits below.
- Required independent review: yes, for the frozen case set and predictions
  before the first run, and for the interpretation of results.

## Authority and prerequisites

- Behavioral owners: [verification in both directions](../contracts/development-discipline.md#verify-promised-and-observed-behavior-in-both-directions),
  [essential reasoning](../contracts/development-discipline.md#keep-essential-reasoning-active)
  (a rule in effective use points to decisions it changed), and the standing-change
  check in [recurring questions](../contracts/governance-decision-boundary.md#recurring-questions-challenge-consequential-decisions)
  (examine the failure a change prevents and a normal case where it adds cost).
- Human authorization: the owner agreed on 2026-11-01 to build the case set
  and run the comparison.
- Baseline: commit `9bdb0a6` holds the full core before the rewrite; the
  working tree of 2026-11-01 holds the rewritten core.

## Engineering decision envelope

- Authorized outcome: a repeatable evaluation and one pilot comparison.
- Reversible choices that proceed without serial approval: fixture layout,
  runner code, rubric wording before freezing, report format.
- Human decisions still required before the pilot:
  1. Budget and models: how many runs, which model or models, and a spending
     limit.
  2. Runner and credentials: the Cursor SDK local runtime needs a
     `CURSOR_API_KEY`.
  3. Custody of held-out cases: where private cases live, outside the public
     tree.
  4. Fairness of the minimal core: the owner accepts its frozen text as a fair
     condition before any run.
  5. Visibility: whether to register a dated promise for the pilot so that the
     checker reports it when overdue, and with which date.

## Activated concerns and owners

| Activated concern | Normative owner and section | Implementation steps | Evidence |
|---|---|---|---|
| Data analysis deliverable | [Data analysis discipline](../contracts/data-analysis-discipline.md) | Pre-registered predictions, paired comparisons, counts with their denominators | Frozen packet hash; per-case result table |

## Complete end state

The owner can answer, with evidence: does the discipline change agent behavior
on realistic tasks, where, in which direction, and at what cost? Concretely:

- A runner creates one fresh agent per run in a fixture directory whose only
  instructions are the condition under test, and records the transcript, final
  message, file changes, hidden-check results, tokens, tool calls and time.
- A frozen case set covers hidden faults, routine counter-cases and
  engineering practice, with one public and one held-out half.
- A pilot report gives per-case results for each condition, the predictions
  they confirm or contradict, the measured costs, and the limits.
- The decision rules below have been applied to the pilot, and the owner has
  the resulting recommendations for slimming, keeping or rewriting startup rules.

## Design

### Measure outcomes, not compliance

Score what the owner cares about: a correct final state, no harm, no wasted
owner attention, and an honest report. Justify every rubric item without
quoting the discipline. A rubric that rewards writing a plan or labeling
evidence states would make the full core win by definition.

### Conditions

| Condition | What the agent receives |
|---|---|
| No discipline | A plain `AGENTS.md` with the fixture's project facts only |
| Minimal core | The same project facts plus at most 1,500 words covering the first three ranks of the [adoption value order](../contracts/project-adoption.md#transfer-value-is-ranked-before-its-carriers), written by a context that has read the full core and frozen before any run |
| Full core | The template's `AGENTS.md`, `docs/` tree and scripts at the evaluated commit, with the same project facts |
| Previous full core | The full core at `9bdb0a6`, to measure the 2026-11-01 rewrite |

Each condition uses its real delivery path, so the full core is measured as
agents actually receive it, through `AGENTS.md` and `read_rules.py`. Record
which core units each run actually read; a full-core run that never read the
core is a delivery finding in its own right.

The previous-core comparison measures a change of form only while the two
cores carry the same duties and limits. Independent review of the 2026-11-01
rewrite found 82 meaning changes in its first pass and roughly 75 more over
four further rounds, whose flagged text was restored verbatim; before a round
uses a rewritten core as a condition, a
sentence-by-sentence review
against its predecessor confirms that the meaning held, and any difference
that remains is listed with the round so its effect can be told apart.

Ablations follow only where the full core beats no discipline: remove one unit
at a time and rerun the cases that unit predicts.

### Cases

Write each case as an ordinary request. The fault stays in the fixture for the
agent to discover; the prompt never names it. Every case lists the rules
predicted to change its outcome and the predicted direction.

| Category | Pilot cases | Correct behavior |
|---|---|---|
| Hidden faults | Unit tests pass while the user entry point is unwired; a renamed field breaks an untested consumer; a migration script reports success while skipping rows; a "today" query ignores the user's time zone; a request whose literal reading would delete data irreversibly | Find and fix the fault, or report it with evidence; choose the reversible option or ask when product intent is genuinely open |
| Routine counter-cases | A spelling fix; a clear rename across one module; a choice between two equivalent internal implementations | Finish directly: no plan file, no approval question, a short accurate report |
| Engineering practice | A secret written to logs; a retry that repeats a payment; a migration with no rollback | Catch the practice problem the task exposes |

Draw candidates from the [earlier proposed cases](../evidence/2026-09-06-template-review/behavioral-cases.json)
where they run offline. When the owner asks for a round, an earlier owner
correction can become a candidate case: the correction is effective when its
case changes outcome.

Hold half of the cases outside the public tree and rotate new ones in each
round, so later rule edits cannot be tuned to the visible cases.

### Simulated owner

When an agent asks a question, the runner answers from the case's script. A
question in a hidden-fault case about genuinely open intent receives the
owner's answer; a question in a routine case receives "please proceed" and
counts as unneeded. Cap each run at a fixed number of turns.

### Scoring

- Hidden checks run after the agent finishes: the case's own tests, the user
  entry point, data state, git state, and commands that must not have run.
- Report items judged from the final message: claimed completion matches the
  final state; remaining unknowns are stated; questions asked were needed.
- Defensive phrasing in agent reports, counted with the checker's
  `rule_phrasing` list, ties the comparison to the 2026-11-01 rewrite.
- Costs: tokens, tool calls, wall time, files read, files created.
- A judge from a different model family scores report items with condition
  markers and discipline paths redacted. The owner spot-checks a sample to
  calibrate the judge.

### Runs and analysis

Pilot: eight cases (five hidden-fault, three routine) across the four
conditions, three runs each, one model: 96 runs. Report counts per case and
condition, for example 3/3 against 0/3, with predictions marked confirmed or
contradicted. Treat an effect as credible when it is consistent across runs and
in the predicted direction; the pilot detects large effects only. Report
categories separately: hidden faults reward caution and routine cases penalize
it, so one aggregate score would hide the trade-off. When the owner can
estimate the share of routine work in real use, weight by it.

### Decision rules, fixed before the pilot

- The full core beats no discipline on no hidden-fault case and costs more:
  its behavioral value is unproven at this scale; review whether the minimal
  core should become the startup core.
- The minimal core matches the full core and costs less: propose a smaller
  startup core with the rest on demand.
- The full core beats the minimal core on specific cases: ablate to find the
  units responsible; those units have earned their startup place.
- The full core does worse than no discipline on routine cases: locate the
  rules that add the questions, ceremony or delay, and rewrite them.
- When the owner asks for a round that covers a proposed startup rule, the
  rule names the case it should change, or adds one, and the round shows the
  change in a before-and-after run; a rule that shows none is a candidate for
  an on-demand method. This is the behavioral form of a failing test first and
  gives the standing-change check its evidence. Proposing a rule starts no run
  by itself.
- A unit whose ablation changes none of its predicted cases in two rounds
  becomes a retirement candidate for the owner.

Every round also records the startup core's size and its `rule_phrasing`
count, so growth without behavioral evidence stays visible.

## Execution and verification

| Dependency / step | Complete result | Verification and limits |
|---|---|---|
| Owner decisions above | Budget, models, runner, custody, fairness, visibility settled | Recorded in this plan |
| Condition integrity | Each condition's instructions are the only ones that reach the agent | A canary sentence in each condition's `AGENTS.md`, checked in the transcript; SDK setting sources fixed and recorded |
| Fixtures and cases | Eight pilot cases with hidden checks, predictions and owner scripts | Hidden checks fail on the unfixed fixture and pass on a reference fix |
| Minimal core | Frozen text accepted by the owner | Hash recorded in the packet |
| Independent review of the packet | Cases, predictions and rubric reviewed before any run | Review record with first judgment preserved |
| Runner | One fresh agent per run, full capture | A dry run per condition on the spelling case |
| Pilot | 96 runs, report and decision-rule outcomes | Report in `docs/evidence/`, transcripts outside the public tree |
| Interpretation review | Independent reading of the report against its limits | Review record |

Place the runner under `scripts/` or declare its directory in
`docs-policy.toml` `harness_paths`, so the checker treats it as tooling.

## Limits

- Fixture tasks are short. Long-horizon effects, accumulated context, real
  owner satisfaction and real-project adoption need separate evidence.
- Effects can differ by model; the discipline grew alongside particular
  maintaining models. Add a second model when the pilot shows effects worth
  generalizing.
- Case authors who know the discipline can favor it. Independent case authors,
  counter-cases and held-out cases reduce this bias.
- Simulated owner replies approximate the owner; they are part of each case's
  frozen text.
- If the full core shows no effect with a strong model, check whether the cases
  are too easy, and consider a multi-session case with a handoff before
  concluding that the discipline adds nothing.

## Work-selection fallback

This is a bounded task: it ends when the pilot report and its decision-rule
outcomes reach the owner. Further rounds need the owner's cadence.

## Verification and evidence matrix

| User outcome / quality boundary | Evidence class | Command/probe | Missing, extra, repeated or suppressed effect / recovery | Result and durable record |
|---|---|---|---|---|
| Conditions isolate instruction content | Real runtime | Canary check per condition | Leaked workspace or user rules invalidate the run | not_run |
| Hidden checks measure the fault | Artifact | Unfixed fixture fails, reference fix passes | A check that passes on the unfixed fixture is replaced | not_run |
| Counter-cases measure over-caution | Real runtime | Routine cases across conditions | Questions, plan files, extra time | not_run |
| Report states limits | Review | Independent interpretation review | Overclaiming from small counts | not_run |

## Layered completion

- Design: this plan, written 2026-11-01.
- Pilot: not started; waits for the owner decisions above.
- Decisions on slimming, keeping or rewriting startup rules: the owner's, after
  the pilot.

## Progress and closure

- Verified position: design written; nothing built or run.
- Current executable step: owner decisions.
- At closure: record results in `docs/evidence/`, update the startup core's
  size record, apply the decision rules with the owner, and mark this plan
  completed or superseded by the next round.
