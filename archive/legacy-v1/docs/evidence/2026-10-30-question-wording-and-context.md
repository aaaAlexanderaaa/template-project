---
doc_type: evidence
status: historical
authority: evidence
last_reconciled: 2026-10-30
subject: question-wording-and-context
---

# Question wording and context in AI assessment

## Claim and scope

The delivered method helps people and question-asking AIs select a question
together with its recipient and context, preserve distinct diagnostic moves,
and interpret the resulting evidence. The
[plan](../plans/2026-10-30-question-wording-and-context.md) records the bounded
outcome. Development's [source 19](../contracts/development-discipline.md#source19--2026-10-30)
records the owner's correction and its attribution.

Baseline: clean `3089af1af089aacb4862c9d1dd4ac2991d289fa0`.
Existing rules already required active comparisons and honest context
independence. The preceding design answer still offered a generic readability
self-check. This is a concrete failure to use available method knowledge,
not evidence that the baseline contained no relevant rule.

## Design choices and source limits

The review guide retains close English translations of the owner's unfamiliar
reviewer complaint, contextual-author complaint and contextual-author
self-assessment. The reported decreasing effectiveness is attributed to the
owner. No original article or controlled comparison was supplied here; neither
the ranking nor equivalence of translated prompts has been experimentally
established by this delivery.

One ChatGPT design discussion challenged a question-only catalog and proposed
retaining context, relationship, wording and first responses. Root integrated
that judgment into the existing analysis owner, review method, task/question/
Grill entrypoints and evidence templates. The implementation avoids a new
protocol registry or a mandatory three-review sequence. Duplicate isolation
advice in the artifact-only card now routes to the shared method.

Primary-source checks inspected the following abstracts and publication pages:

- [Anthropic, Towards understanding sycophancy in language models (2023)](https://www.anthropic.com/research/towards-understanding-sycophancy-in-language-models):
  reported preference for answers matching user views supports treating
  induced agreement as a possible confound. It does not measure these prompts.
- [Tsui, Self-Correction Bench, version 3 (2026)](https://arxiv.org/abs/2507.02778v3):
  reports differing correction of internal and external error attribution
  under controlled conditions in fourteen open-source non-reasoning models.
  Its task/model scope does not establish behavior of this configured ChatGPT
  account, current frontier models generally, or article comprehension.

These sources support investigating the mechanism. The owner feedback,
research results and implementer choices remain different evidence classes.

## Consumer exercise

A separate ChatGPT request receives the actual task-selection doorway, full
review guide and independent-review template as data snapshots. It receives
four fictional situations: a first-time-operator article, an API conformance
review, a spelling correction, and contradictory assessment summaries. It
must use the guidance to choose its next action and prepare any review
assignment. It receives no author's rationale or desired answer list.

The tool uses the configured account's model, instructions and personalization;
those settings are not overridden or fully observable. A separate conversation
can establish separation of the submitted history, not an empty or statistically
independent model environment. This is an instruction-use and dispatch-preparation
exercise, not actual execution of the three reviewer environments or a trial
with real article readers.

The [consumer record](2026-10-30-question-method-consumer.json) retains the exact
request, source manifest, first returned answer, focused follow-up and root's
assessment. Tool metadata confirmed that design discussion, first consumer
request and follow-up used different submitted conversations. This confirms
submitted-history separation only; account-level context remains unknown.

The first attempt was rejected before execution when automatic approval review
could not run because workspace credits were exhausted. After the owner asked
to continue, the identical request completed through the same tool and approval
path. Its first response selected suitable methods, but the returned text had
two assignment headings with no assignment bodies. Their absence could not be
attributed to generation or transport. One follow-up requested ordinary prose
for those missing assignments, using the same cases and guidance. Its complete
returned text is retained separately; it does not replace the first response.

| Case | Observed consumer use | Root verification and limit |
|---|---|---|
| First-time operator article | Chose an unfamiliar reader and a separate inspectable request; the follow-up preserved the guide's complaint wording and supplied only article/title to that reviewer | The proposed dispatch excludes author defense and predicted defects. No actual reviewer was launched; recipient context still needs inspection before a future dispatch. The fictional article supports diagnosis, not a real-reader outcome. |
| API field removal | Chose conformance review with governing contract, policy and original intent; prepared an assignment while naming missing proposal and source revisions | Those sources are absent from the fictional packet. The response correctly withholds a compliance verdict; an artifact-only review would not establish it. |
| Spelling correction | Kept the direct authorized correction without extra independent review | The selected method preserves ordinary low-cost work; this exercise did not edit a product file. |
| Conflicting assessment summaries | Left the verdict unresolved and sought prompts, first answers, context and verified findings instead of counting criticisms | Summaries cannot recover missing observations. The response does not pretend to reproduce the original assessments. |

The consumer also identified absent linked authority, uninspectable inherited
context and the need to verify findings against actual source material. These
are real limits of the supplied packet and future dispatch, not grounds to
copy governance rules into this optional guide. Root verified that the actual
repository routes to existing owners and that those links resolve. The method
does not grant release authority or make isolation observable by declaration.

The first response and labeled follow-up support method selection and dispatch
preparation on these cases. They do not establish the comparative diagnostic
accuracy of the three prompts. No additional guidance correction was required
by a verified consumer finding.

## Verification and completion

| Check | Result |
|---|---|
| `python3 -m unittest discover -s tests -p 'test_*.py'` with Python 3.14.2 | 190 tests passed in 48.780 seconds. The first run had 43 failures because its copied-repository clock was October 28 and today's reconciliation dates exceeded its tolerance. Advancing `FIXED_TODAY` to October 30 follows the existing fixture-baseline rule; no checker behavior or severity was relaxed. |
| `python3 scripts/check_docs.py` | Passed for 68 canonical documents and 16 templates under the existing full profile. The only advisory is the pre-existing overdue `independent-adoption-review` promise in execution discipline. |
| `python3 scripts/read_rules.py prepare --include docs/guides/review-cheatsheet.md` | Completed all ten selected units. The new owner text and the complete method are delivered through the existing reader. |
| Entrypoint and source inspection | General task, question-starter, review, Grill, research and operation routes point to the same method. Consumer source hashes still match the inspected files. Information-access guidance was reviewed against the source change and remains substantively applicable. |
| `git diff --check` | Passed. |

The bounded delivery is complete: the selected question and its operating
conditions are part of the reusable method and evidence, with observed use
through the ordinary task doorway. Long-term uptake, prompt rankings,
real-reader improvement and a sustained reduction in missed problems remain
unverified. The broader project knowledge-catalog proposal was not adopted
or implemented by this correction.
