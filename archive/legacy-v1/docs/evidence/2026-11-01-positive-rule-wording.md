---
doc_type: evidence
status: historical
authority: evidence
last_reconciled: 2026-11-01
subject: positive-rule-wording
---

# Rules written as actions

## Request and dispositions

On 2026-11-01 the owner asked a model new to this repository to review the
discipline by its own rules and report its shortcomings. The review reported
six findings. The owner decided as follows.

| Finding | Owner's decision | Action in this delivery |
|---|---|---|
| The rules only grow | Real and long-term; keep it in view | The [behavioral evaluation plan](../plans/2026-11-01-behavioral-evaluation.md) records the startup core's size each round and lets a proposed startup rule show its effect; a round runs only when the owner asks for it |
| Nobody can tell which rules work | Real and long-term; keep it in view | The same plan: a three-way comparison with routine counter-cases and fixed decision rules |
| The rules mostly say what not to do | Agreed; handle it | Startup core rewritten as actions; language rule and checker advisory added |
| Rules written for single incidents spread into general places | Agreed; fix it | Git stop returned to its adoption owner; named-end rule kept at its owner with cues elsewhere; the entrypoint opens with what the repository is |
| Coverage follows the maintainer's incident history | Acknowledged; matches the owner's planned move into practice | No change now; the plan's engineering-practice cases connect to it |
| Personal collaboration preferences encoded as defaults | Agreed; unchanged until outside feedback arrives | No change to these rules. The named-end rule's full text stays at its execution owner; its copy in the entrypoint became a cue and a pointer under the fourth finding, keeping the moment of failure |

The owner attributed the third finding to the previous maintaining model's
over-caution and habit of disclaimers, and said their own corrective
requirements had not worked well enough.

## Why earlier corrections did not hold

The repository shows three mechanisms.

1. Writers copy the corpus. The owner recorded this on 2026-08-27 in
   [development source[6]](../contracts/development-discipline.md#source6--2026-08-27):
   the wording of descriptive documents guides future language style. Each
   later correction was written into a corpus already full of "is not",
   "alone does not" and "creates no", so the new text took the same form.
2. Corrections were themselves recorded as constraints. The owner's
   2026-10-20 point that accumulating negative constraints does not solve the
   problem, in [development source[18]](../contracts/development-discipline.md#source18--2026-10-20),
   was carried into the rules as further limits.
3. Duties meant for evidence were applied to rules. Attribution and
   uncertainty belong to reports and evidence. Applied to normative text, they
   produced sentences disclaiming what a rule is not, or what the owner did not
   say, in place of the duty itself.

Nothing detected the pattern: the checker covered structure, and the language
rule stated that word lists cannot establish understanding.

## What changed

| Surface | Change |
|---|---|
| Startup core (nine units) and `AGENTS.md` | Reworded toward conditions and actions where an equivalent wording held up under review. The essential-reasoning section and every paragraph or sentence a reviewer found changed in meaning are restored verbatim from the baseline. Headings, anchors, concern triggers and source citations are unchanged; `AGENTS.md` gained a final "In a copied checkout" section |
| Task context | One statement replaces several local disclaimers: a rule creates an approval step, form, record, reviewer or test only when its text requires one, in whatever words |
| Language rule | Rules written so a reader can act on them. A sentence that only repeats that closed list of five may go when, without it, no rule requires that artifact for the same case; any other disclaimer and any limit on what evidence shows stays or is replaced only by wording that passes the check, with one example of each. Rewording keeps reach, conditions, duties and permissions, modal strength, the effect of qualifiers, open example lists, the subjects of merged sentences, presuppositions and placement inside a required-reading unit; a rule moved to its owner leaves the owner holding everything the moved text required. Each limit, condition and permission of a changed sentence is checked against the cases nearest its boundary on both sides, deletions and merges against the text that remains, and the old sentence stays where no equivalent wording passes. Writers copy the form of what they read, including the form of corrections |
| Development core | Attribution is written as plain statements of who decided what, once per record, naming what remains unresolved |
| Checker | An opt-in `rule_phrasing` check for listed disclaimer phrases in the startup rules and the entrypoint, skipping quotes, code and citations, with fixture tests. It is off by default and in this repository |
| Single-incident rules | The git-initialization step lives at [its adoption owner](../contracts/project-adoption.md#an-existing-directory-is-described-before-template-files-are-added); the learning ending links to it and keeps its own stricter stop. That section's git step now applies before any template file is added, before an adoption writes anything else there, and before a learning ending writes a file there, joining its own trigger with the adoption trigger both root entrypoints stated, so the entrypoint's pointer loses nothing. The named-end rule is unchanged at its execution owner, with a cue and a link in the entrypoint, the operation guide and the plan template. The entrypoint's copy-detection sentence moved to its end, with every identity claim the checker reads |
| Plan template | Its disclaimers rewritten as actions, because every new plan copies it |

The `rule_phrasing` check departs from the earlier practice of adding no
keyword checks. The implementer first enabled it as an advisory, because
another written requirement would repeat the remedy the owner reported had not
worked, while a signal in every check run differs in kind. The reviews below
showed that most listed phrases mark limits or permissions that should stay:
with the check enabled, the final startup text produces 26 findings, all on
sentences the final text keeps verbatim from the baseline.
A per-line prompt to reconsider those sentences repeats the move that caused
the drift, so the implementer made the check opt-in and left it off here.
Asked afterwards, the owner chose to keep it off.

## Measurements

A working script split each startup unit, as delivered by
`scripts/read_rules.py prepare`, into sentences of four or more words, after
removing tables, fenced code, reading markers and citation lines. It counted
the sentences containing a negation word (not, no, never, cannot, nor,
neither, none, without and contracted forms) and the occurrences of a working
list of disclaimer phrases: the checker's list plus broader forms such as
"is not a" and "does not prove", counted inside quotes too.

| Measure | Before (`9bdb0a6`) | First rewrite | Final |
|---|---|---|---|
| Startup core size | 101,745 bytes, 13,805 words, 693 sentences | 97,026 bytes, 13,190 words, 632 sentences | 104,418 bytes, 14,257 words, 679 sentences |
| Startup sentences containing a negation word | 38.2% | 14.2% | 30.0% |
| Working-list disclaimer phrases in the startup core | 67 | 2 | 38 |
| `AGENTS.md` sentences containing a negation word | 28.1% | 8.9% | 18.3% |

The first rewrite's shrinkage and most of its change of form came from dropped
limits, which the repairs and verbatim restorations brought back. The final
core is larger than before, by 2.6% in bytes and 3.3% in words: 408 of the 452
added words are the language rule's new paragraphs, and the rest of the core
grew by 27 words net. This delivery therefore adds to the first finding,
one-way growth. What remains is a smaller change of form than the first
rewrite suggested: the share of startup sentences with a negation fell from
38% to 30%, and working-list phrases from 67 to 38. The count misses a phrase
broken across a line on both sides; on whitespace-normalized text it is 70
before and 40 after. All but four of those 40 sit in sentences kept verbatim
from the baseline; three are the language rule's quoted examples and one is a
reworded limit. Of the 679 final sentences, 207 differ from every baseline
sentence after whitespace is normalized, and 472 are unchanged. A negation is
often right, as in a real boundary, and phrases such as "instead of" are not
counted. The numbers show that the wording changed; whether agents act
differently is untested. The [evaluation plan](../plans/2026-11-01-behavioral-evaluation.md)
includes the previous core as a condition to test it.

## Independent review

Two reviewers, each in a fresh context with the baseline commit, compared
every changed sentence with its old form. One covered the development core
and found 52 meaning changes. The other covered the entrypoint, the task
context and language rule, the governance core, the execution units, the
learning ending, two guides and the plan template, and found 30.

| Class | Development core | Other files | Total |
|---|---|---|---|
| Lost | 5 | 2 | 7 |
| Weakened | 14 | 6 | 20 |
| Strengthened | 10 | 5 | 15 |
| New duty | 2 | 1 | 3 |
| Changed meaning | 15 | 8 | 23 |
| Ambiguous | 6 | 8 | 14 |

Most came from one move. A sentence of the form "X does not establish Y" was
treated as a disclaimer and replaced by an action, but such a sentence usually
limits what evidence shows. Replaced, the limit disappeared; a necessary
condition became sufficient ("a conclusion is established when it can be
reproduced"); or a limit on claims became an open-ended duty ("confirm the
change in later use"). The rewrite also turned always-on premises into
narrower triggers, permissions into duties, and two prohibitions into
statements of purpose. Losses that mattered most included the bar on assuming
someone will resolve a known gap, the bar on a universal vocabulary ban in
response to one signal, the stricter git stop for a learning ending, and a
question-ordering rule that, as rewritten, deferred the question others
depend on.

The implementer repaired every item toward the old meaning, keeping positive
form only where it carried the same meaning, for example "shows only what it
exercises".

A third reviewer in a fresh context checked the repairs against both reports
and the baseline. It found 80 items resolved and 2 partly resolved, plus about
a dozen meaning changes that both earlier reviews had missed. Most were limits
rewritten into a sufficiency form: "improvement shows in later behavior" reads
as if later behavior were enough, where the old sentence only said that a
recorded lesson was not. Others dropped a named kind of non-evidence, such as
citation count or an exhausted search budget, or turned a permission to retry
into a duty. The reviewer also found that the language rule still allowed the
same failure: it did not say that a rewrite keeps a rule's reach, that a route
replaces a prohibition only when it excludes the same cases, that small
qualifiers belong to a limit, or which disclaimers the reading rules actually
cover. It noted that most listed advisory phrases mark limits, so each hit
nudges a writer toward the riskiest rewrite.

The implementer repaired those items, again by rewording them, and tightened
the language rule.

A fourth reviewer checked the 22 places changed in that pass and swept the
startup text. Fourteen held. Eight did not, several of them the third round's
own repairs: rewording a limit again changed it again. "More findings show
only more criticism" also discounted confirmed findings, and "shows only where
the search stopped" denied that repetition supports diminishing returns, a
stopping basis the same paragraph allows. The sweep found ten further changes.
They included the always-loaded named-end cue, which had lost the moment of
failure ("writing the next step is not doing it"), and an essential-reasoning
premise that, reworded, described a problem that could never close. The
reviewer also showed that the language rule's own example added a necessary
condition its quoted original lacked.

Repairs by rewording were drifting at about the rate of the first rewrite, so
the implementer changed method. Every paragraph a reviewer had flagged, and
the whole essential-reasoning section, was restored verbatim from the
baseline, which cannot drift. The language rule now gives one example of a
disclaimer that may go and one of a limit that stays, and keeps the old
sentence where no equivalent wording passes the two-case check. The named-end
cue regained its failure moment.

Two final reviewers in fresh contexts then checked every remaining changed
sentence, one in the development core and one in the other startup units and
`AGENTS.md`, with no cap on findings. The first found 11 of 158 changed
sentences still changed in meaning, none severe. The second found 15 of 118.
The most serious was that the risk unit no longer said that unavailable
evidence or an unavailable reviewer cannot justify a lower profile. It also
found that the new reading statement, "a mandatory condition adds only the
work it names", could be read as permission to skip required work, and that
the projection mechanics had left the language-style unit. All flagged text
was restored verbatim, the reading statement was cut to the closed list of
five, and the language rule gained the missing kinds of drift. While checking
that unit, the implementer found one more narrowing that both reviewers had
judged sound: "give precise uncertainty beside the claim it changes" excluded
the separate limits section the old sentence allowed. It was restored.

A second pair of fresh reviewers checked the 223 sentences still changed,
directed at narrowing, which earlier rounds had caught less often than
widening. The development-core reviewer found ten low-severity changes and one
unlisted deletion among 146 items. The other found eight low-severity changes
among 83 and one severe one. Both root entrypoints required a git commit
before an adoption writes anything into a directory that has files and no
repository, but the adoption section the entrypoint now points to required it
only before template files and a learning ending's file. Its review of the
new text found that "only when it names one" let a duty phrased in other
words, such as establishing the owner's authorization or an independent
check, be skipped. It also found that the deletion license could remove an
exception to a nearby rule that names the same artifact. The reading
statement now says "only when its text requires one, in whatever words"; the
deletion license applies only when, without the sentence, no rule requires
that artifact for the same case; and the check covers every limit, condition
and permission of a sentence, and deletions and merges. Every other flagged
sentence was restored verbatim.

The adoption section was first given a trigger of any write. A last fresh
reviewer checked that text, the final language rule and this record. It found
that "any write" also reached writes outside adoption, such as the owner's
task after a learning ending that wrote nothing, which the baseline left
without a commit. The section now joins the baseline triggers instead, as
[adoption source[18]](../contracts/project-adoption.md#source18--2026-11-01)
records. The same review found smaller gaps in the language rule, a
development purpose sentence that repeated the reading statement and
presupposed that every rule names its trigger, and several wrong counts in
this record; all were corrected and the purpose sentence removed.

Every changed startup sentence that existed at the first final round was
judged sound by both final rounds. The reading statement and the language
paragraphs were reviewed twice and tightened as those reviews proposed. The
joined git trigger follows the last review's correction, extended to keep the
baseline's template-file trigger outside adoption, and has not been reviewed
again.

## Verification

| Check | Result |
|---|---|
| `python3 -m unittest discover -s tests -p 'test_*.py'` with Python 3.12.13, after the final restorations | 196 tests ran: 195 passed and one was skipped as before |
| `python3 scripts/check_docs.py`, after the final restorations | Passed for 72 canonical documents and 16 templates with `rule_phrasing` off; the only advisory is the pre-existing overdue `independent-adoption-review` promise |
| The same check on a scratch copy with `rule_phrasing = "advisory"` | 26 findings, all on sentences kept verbatim from the baseline |
| `python3 scripts/check_docs.py --strict` | Fails only on that overdue promise |
| Projection review | The eight guides projecting changed contracts were read against the changes and re-dated; the onboarding guide states the opt-in setting and the joined git trigger |
| `git diff --check` | Passed |

## Limits and remaining work

- Non-startup contracts, guides and the other templates still contain the old
  form. Rewording them carries the drift risk measured here, so each changed
  sentence needs the two-case check and an independent comparison.
- Restoring flagged paragraphs verbatim brought back their negative wording;
  the form change is smaller than the first rewrite's numbers suggested.
- The opt-in check finds only the listed phrases, most of which mark limits
  that stay, and a reworded disclaimer passes it.
- Each review round found changes the earlier rounds missed. The last round
  found mostly low-severity edge cases but still one severe change, so the
  remaining drift is likely small in effect but not shown to be zero.
- Several local disclaimers were deleted because the task-context reading
  rule now says a rule creates an approval step, form, record, reviewer or
  test only when its text requires one. Among them are three development-core
  clauses: "creates no recurring reflection form or additional reviewer
  tier", "routine work needs no new form" and "not an automatic user-approval
  checkpoint". A change to that rule reopens those deletions.
- The adoption section's git step now also applies before an adoption's other
  writes, while its stop when git cannot be initialized still names only
  template files and says other work continues. Read together, the section
  now lets an adoption's non-template writes continue without a commit when
  git cannot be initialized; the old entrypoint row named no behavior for that
  case. Asked about it, the owner kept this behavior.
- No behavioral evidence exists yet for this rewrite; the evaluation plan is
  its route.
- The overdue `independent-adoption-review` promise is unchanged and remains
  the owner's decision.
