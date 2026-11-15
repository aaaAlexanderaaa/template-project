---
doc_type: plan
status: completed
authority: planning
last_reconciled: 2026-10-29
implements: docs/contracts/project-adoption.md
supersedes: []
---

# Obtain and understand rules before judging applicability

## Cold-start summary

The owner required external agents to read rules and understand why they exist
before deciding whether to obtain or read them. This follows the question of
how new projects, older adopters and projects with their own discipline learn
from the template. The bounded result is a usable reading order through the
existing entrypoints, with applicability and migration decisions made after
source understanding. A separate universal upgrade tool is outside this task.

Baseline: `8fe18fd`, clean working tree, 189 passing tests. Full learning already
requires every named current rule, but the extraction owner lets an inspection
request select one practice, and README begins with "applicable disciplines."
Those doorways can turn an uninformed selection into permission to omit rules.
The current full-learning list also omits the data-analysis contract by name.

## Risk classification

Material, recoverable documentation and agent-workflow change. It changes how
external consumers obtain and evaluate rules. No product, runtime parser,
permissions, automatic migration or enforcement scope changes. A fresh
nonproducing consumer is required by development's delivery verification rule;
high-risk independent design review is not activated.

## Authority and prerequisites

- [Adoption](../contracts/project-adoption.md) owns external learning, extraction
  and adoption; [task context](../README.md#task-context) routes to it.
- [Development](../contracts/development-discipline.md#verify-promised-and-observed-behavior-in-both-directions)
  owns observed consumer use and evidence limits.
- The owner's October 29 correction supplies the requested ordering. The
  implementer chooses wording, examples and integration at existing owners.

## Engineering decision envelope

Root owns contract, entrypoint and guide edits and final integration. Preserve
target-project authority and the owner's explicit task scope. Reading a source
does not adopt it. Do not change the existing learning endings, require copying
the template, or make every later task repeat a full learning survey.

## Activated concerns and owners

| Concern | Normative owner | Boundary and evidence |
|---|---|---|
| Compatibility and Experience | Adoption: learning and extraction | Existing broad learning cannot become an uninformed optional subset; a fresh consumer uses normal entrypoints. |
| Reliability and operations | Adoption: failure and recovery | Unknown rationale remains unresolved, while current project authority and authorized work remain usable. |

## Complete end state

1. Normal entrypoints direct external learners to the declared full rule set
   and its problem, mechanism and limits before applicability or adoption
   judgments.
2. New, older and independently governed projects use that order; an existing
   discipline or an apparently inactive domain does not excuse unread rules.
3. Narrow practice inquiry obtains complete source and rationale without
   claiming or silently replacing a full survey. An implementer can choose a
   candidate within an authorized concrete task; no owner-naming gate appears.
4. README, onboarding, task context and extraction guidance point to one owner.
5. Consumer observations and repository checks establish the bounded claim;
   actual independent-project adoption remains unobserved.

## Execution and verification

Reconcile adoption first, then its projections. Use no prose-matching test as
proof of comprehension. A fresh read-only consumer receives ordinary public
entrypoints and task inputs, records its reading and first decisions, and
tests the first reading decision for broad learning plus an actual bounded
extraction countercase. This trial does not claim a completed external survey.
Preserve the first result before providing producer rationale. Root verifies findings,
corrects defects, and runs the required suite, documentation and whitespace
checks. An additional rule for a plausible inactive domain tests premature
selection; one explicitly named practice tests preservation of bounded scope.

The actual A/B first report passed its two bounded decisions. An additional
informed C case found that requiring a practice named by the request could
burden ordinary authorized investigation. Root removed that gate while keeping
source understanding before fit. B also observed whole-document method output;
root declared complete operative units and explicit prerequisite edges at the
same owners. A failing-before/passing-after integration test now checks both
direct extraction and its card obtain the reason before the method. This guard
establishes delivery order and scope, not comprehension.

The consumer owns only
`docs/evidence/2026-10-29-external-rule-learning-consumer.json`; all sources
are read-only, with optional disposable probes. No other write workstream is
known. Root remains the integrating owner and preserves the first report.

## Work-selection fallback

Continue through coherent entrypoints, observed consumer use and corrections.
Do not expand this into a full external adoption, new reading command or
ongoing portfolio assignment.

## Verification and evidence matrix

| Claim | Evidence | Current state |
|---|---|---|
| Read and understand before exclusion | [Consumer record](../evidence/2026-10-29-external-rule-learning-consumer.json): actual source acquisition and source-supported explanation in B; informed final recheck | Passed within the recorded trial; target usefulness and a full learning survey remain unobserved. |
| Broad learning keeps its complete scope | A uses the normal entrypoint with supplied independently governed CLI-project facts; final recheck preserves the decision | Passed for the initial reading decision; no completed target survey is claimed. |
| Bounded extraction stays bounded | B examines a named practice; C exposes an unnecessary owner-naming gate, corrected and rechecked | Passed for the current source and supplied task facts; no automatic adoption or target implementation occurred. |
| Complete prerequisites precede the method | Both actual extraction entrypoints, failing-before/passing-after integration guard, consumer's final command observation | Source understanding precedes normative extraction and its guide card; explicit whole-source selection remains available. |
| Relationships remain valid | Python 3.14.2 unit discovery, documentation checker and whitespace check | All 190 tests passed; 66 canonical documents and 16 templates passed checking; diff whitespace check passed. The existing overdue independent-adoption-review advisory remains. |

## Layered completion

Complete for the bounded source-ordering change, its public entrypoints and
observed consumer decisions. The independent first A/B observations, later C
finding and informed correction recheck remain distinguishable in the evidence.
The final record's ten source identities match the integrated sources.
This task makes no claim of universal understanding, completed external
learning, sustained adoption or universal attention savings. The adoption
owner's broader partial verification status and open review promise remain.

## Progress and closure

- Verified position: the reading order and public projections are reconciled;
  complete rationale units are explicit prerequisites of extraction. The
  consumer's informed final recheck passed A/B/C within its stated limits,
  including the corrected owner-naming boundary and actual method delivery.
  All 190 tests and the documentation and whitespace checks passed.
- Next action: none for this bounded task.
- Blocked conditions: none.
- Completion evidence: [consumer observations and correction recheck](../evidence/2026-10-29-external-rule-learning-consumer.json),
  root validation of current source identities, the actual-entrypoint guard
  and repository checks recorded above.
