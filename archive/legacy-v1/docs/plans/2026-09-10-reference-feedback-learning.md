---
doc_type: plan
status: completed
authority: planning
last_reconciled: 2026-09-17
implements: [docs/contracts/development-discipline.md, docs/contracts/project-adoption.md]
supersedes: []
---

# Learn from reported requirement and feedback failures

## Cold-start summary

On September 10, the maintainer requested that this template learn from
changes and feedback in another assistant-assisted project. The selected
refinements preserve decision attribution, prevent examples from becoming
unintended scope limits, and require analysis of the actual input.

On September 17, the maintainer clarified the publication requirement: explain
those mechanisms in English with enough context for an outside reader.
Private checkout paths, unavailable commit identities, and isolated dialogue
fragments do not make the incidents publicly reproducible. The public account
below replaces those details while preserving the lessons and evidence limits.

The original template baseline was `5a7a5e6c98d7da0ad1e8f3875550760896ad484f`.
Current owners are [decision preservation](../contracts/development-discipline.md#preserve-decisions-and-evidence),
[outcome verification](../contracts/development-discipline.md#verify-promised-and-observed-behavior-in-both-directions),
and [adoption triage](../contracts/project-adoption.md#external-material-is-triaged-by-authorship-before-adoption).

## Risk classification and authority

Material documentation work reconciles existing contracts and their template
consumers. The maintainer authorized this bounded learning task. It changes no
runtime, isolation, privilege, or destructive data path. The current execution
profile does not require independent design review for this scope.
The scenario review is same-context evidence, not independent evaluation.

The selected rules are the implementer's synthesis of the reported problems.
They are not a list dictated by the maintainer, and another project's local
approval practices are not adopted by implication.

## Source evidence and selection

The motivating project and its original conversations are not supplied with
this repository. The September 10 work record reported inspecting its records
and changes; public readers cannot repeat that inspection here. This account
explains why the rules were selected. It does not prove the incidents, their
frequency, or improved user outcomes. The September 17 clarification directly
explains the attribution error in the first row.

| Reported situation and evidence limit | Failure mechanism | Selected refinement and boundary |
|---|---|---|
| An assistant organized feedback into four categories. It later referred to that classification as though the maintainer had supplied the wording and required that structure. The maintainer corrected the attribution. The original project records are not public. | An interpretive label became a purported owner requirement through repeated summaries. Acceptance of a proposal was also confused with authorship of its wording. | Distinguish owner statements, accepted proposals, and implementer interpretations. Acceptance still authorizes its agreed scope; it does not make the proposal owner-authored or immutable. |
| A broad product goal was reduced to an initial sample workflow. The prior work record reports that the restriction spread into task inventory and an executable guard. That implementation is unavailable here. | A convenient example became an exhaustive requirement without an owner decision. | Trace narrowing through the plan, implementation, and tests. Preserve explicitly authorized narrow work; a broad parent goal does not authorize unlimited expansion. |
| In a language-feedback tool, a valid reusable rule or library example was returned instead of explaining the problem in the submitted text and checking the proposed correction in context. | Correct general information displaced the analysis needed to complete the user's actual task. | Apply the causal explanation to the input and review the whole corrected result. No language-teaching schema or private library is required by this template. |
| The prior work record reports unmatched catalog findings and rejected parser output being treated as an empty, successful result. The implementation and outcome data are unavailable. | Missing coverage or discarded information was presented as absence of a problem. | Inspect omitted, unmatched, and rejected results under bidirectional verification. The owning product decides how unknown and partial results are presented. |
| The maintainer reported being asked to perform analysis and verification that the assistant could complete within already authorized work. | Verification labor and settled decisions were returned to the user. | Existing execution and uncertainty rules cover this; strengthen concrete analysis without adding another approval loop or duplicate rule. |

The repository rules and examples can be inspected and tested here. A later
citation of this account is not independent corroboration of the private
incidents. Evidence of a code change, where available, also does not establish
who originated a requirement or whether users benefited.

## Complete end state

- Development owns attribution, outcome scope, concrete analysis, and the
  negative-result verification example at existing sections.
- Adoption triage distinguishes original evidence from reported statements
  and routes attribution to development rather than defining it twice.
- Contract, frontend-surface, verification, and independent-review templates
  expose the relevant questions at the point of use. Current guides agree.
- The public explanation is self-contained. No new metadata schema, task
  registry, mandatory review role, or text detector attempts to infer agreement.

## Execution and verification

The contracts were amended first, followed by their templates and guide
projections. The public-language review retains the substantive amendments and
replaces their inaccessible supporting detail. Checks cover this repository's
structure and the scenarios below, not a new experiment in the source project.

| Scenario | Required result | Evidence/status |
|---|---|---|
| Owner accepts proposal A, then questions its wording | Preserve the proposal and acceptance scope; proceed with authorized work; do not call its wording owner-authored | Pass — decision preservation separates acceptance scope from authorship and retains authorized work. |
| A summary attributes acceptance without a supporting decision | Keep the attribution unverified; silence is not assent; unrelated authorization remains valid | Pass — decision preservation keeps missing source material an evidence limit; silence does not authorize. |
| One sample workflow becomes the only supported task | Trace the introducing record and supporting decision through documentation and guards | Pass — outcomes before means traces narrowing into plans, implementation, and guards. |
| Owner explicitly requests only one workflow | Preserve that scope rather than expanding it merely because examples are often non-exhaustive | Pass — outcomes before means explicitly protects an authorized narrow scope. |
| A library rule is correct but its suggested replacement breaks the input | Verify the explanation and the complete corrected artifact in context | Pass — causal analysis requires application to the input and review of the whole correction. |
| Every candidate is discarded or the catalog has no match | Distinguish unknown coverage from a valid clean result and preserve the failure policy | Pass — bidirectional verification inspects unmatched, rejected, and omitted results. |
| A bounded task is complete but a broader ambition remains | Close the authorized task without treating its samples as the whole ambition or authorizing further work | Pass — the existing execution boundary ends bounded work without inventing portfolio authority. |
| A polished report cites unavailable original records | Preserve the evidence limit; do not inherit claims of user success or public reproducibility | Pass — adoption triage and this public account distinguish reported experience from inspectable evidence. |

## Risks and recovery

Over-correction could require verbatim approval for every engineering choice,
make accepted proposals optional, or turn every sample into a demand for full
domain coverage. The paired scenarios guard those boundaries. The existing
[governance owner](../contracts/governance-decision-boundary.md#delegated-engineering-work-proceeds-by-default)
still determines authority. Semantic review cannot be replaced by phrase
presence tests. Revert or narrow an amendment that conflicts with these limits.

## Progress and closure

- The September 10 amendments are present in the working tree. Their earlier
  closure record was unfinished and is not treated as proof of completed tests.
- The September 17 publication reconciliation replaced private paths and
  isolated quotations with the contextual account above.
- All eight scenarios were reviewed against the current text on September 17.
  Results above are same-context document review, not executed adopter trials.
- Python 3.14.2: all 118 fixture tests passed; normal and strict documentation
  checks passed. Those checks establish repository structure, not effectiveness
  of the rules in another project.
- The bounded refinement and publication work is complete. Behavioral
  effectiveness remains partial at the contracts; no private incident or user
  outcome is claimed as newly reproduced.
