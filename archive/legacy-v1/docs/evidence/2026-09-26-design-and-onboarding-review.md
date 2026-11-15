---
doc_type: evidence
status: historical
authority: evidence
last_reconciled: 2026-09-26
subject: design-methods-calibration-and-onboarding
---

# Design methods, calibration, and onboarding verification

## Claim being verified

The [development owner](../contracts/development-discipline.md#design-direction-and-content)
and its surface template support the actual brief without universal task or
visual-element counts. The [autonomy owner](../contracts/autonomous-operation-discipline.md#taste-lives-in-a-corpus-the-model-is-a-hypothesis)
and its charter template interpret corrections by cause and contain affected
decisions. The [onboarding guide](../guides/onboarding.md#verification) provides
an entry path from which a fresh agent can start useful authorized work.

The [implementation plan](../plans/2026-09-26-design-methods-and-calibration.md)
records the approved scope. This record covers local documentation delivery,
one real read-only onboarding task, and independent reading-based review. It
does not establish long-term autonomy or adoption across all project types.

## Environment and independence

Baseline: `203115d1dff37e968def0edce5765b328faa9b86` plus the local onboarding
and design/calibration changes. The original implementer checks passed before
independent review. No commit or push was made.

The first independent worker failed for lack of workspace credits before
returning a read trace or result. The maintainer then explicitly requested a
new worker using `gpt-6-sol`. That worker started with no inherited conversation
and did not produce the implementation. Its assignment had two ordered parts:

1. Learn the template and a separately supplied private entrypoint, then check
   whether an existing portable memory package works after relocation. Save
   its actual-use observations before reading implementation plans, evidence,
   or the two rule groups being reviewed.
2. Read the current design and calibration owners and teaching material;
   assess concrete contrasting situations against the authorized scope.

The same reviewer later checked the corrections in one bounded follow-up.
These are one independent context and one recheck, not multiple independent
votes. The implementer preserved the original reports unchanged and recorded
hashes of the initial public inputs; those inputs remained unchanged throughout
initial review. Private profiles, reports, and locators remain outside this
repository. Findings below contain the general mechanisms and evidence limits.

## Actual onboarding and artifact use

The reviewer reported reading the working agreement, homepage entry route,
documentation authority/task-context sections, onboarding collaboration path,
and applicable adoption boundary. It then read the private package's short
entrypoint, README, manifest, and packaging script. It did not load the deep
personal reference, request a new interview, or initiate governance migration.
The task had enough information for read-only execution with temporary copies.

In a fresh temporary location, the reviewer extracted the archive into a
separate directory and checked files, hashes, entrypoints, and relative links.
Five document hashes and both entrypoints passed. Twenty links resolved; the
README's link to the archive itself failed when the archive was outside the
extracted directory. The packager explicitly exempted that link. The original
implementer probe had extracted beside the ZIP, so it missed this use case.
The implementer separately reproduced the failure before changing the package.

The private package README now names the archive as plain text and explains
that it can be removed after extraction. The packager no longer exempts its
self-link. In the independent follow-up, the reviewer extracted into a nested
directory, deleted the copied archive, and verified all six entries, five
hashes, two entrypoints, and 20 relative links. No relocation blocker remained.
An implementer negative check reintroduced the archive hyperlink in a disposable
fixture and confirmed that packaging rejected it.

This is evidence of actual onboarding decisions and artifact use for one
bounded existing-project task. No comparison group, new-product adoption,
other Markdown renderer, or long-term collaboration was tested.

## Independent rule findings and resolution

The following findings came from rule reading and scenario reasoning, not
rendered UI tests or autonomous epochs.

| Finding | Correction and recheck |
|---|---|
| An absolute ban on demo wording could hide sample or sandbox state needed for correct use | Development separates development commentary from necessary product-state information. The reviewer found this sufficient without expanding product-direction authority. |
| A required rejected-alternative field could invite invented owner feedback | The surface template permits none or not tested, labels implementer inference, and requires a raw anchor for a rejection attributed to the owner. The reviewer found this sufficient. |
| Corpus/model/prediction fields invited private locations into a public charter | The autonomy owner routes all three through the existing personal-context boundary; the charter records permitted audience and safe references. The reviewer found the disclosure boundary sufficient. |
| Local calibration pauses could be confused with formal halted state | The autonomy owner and charter distinguish them; formal halted recovery still requires the owner's answer. The reviewer found no self-unlocking path in the revised wording. |

The follow-up also noted that session-only source resolution might fail across
unattended wakes. The implementer adopted the reviewer's proposed wording:
approved private context or a persistent locator, still subject to the same
privacy and access boundary. This final wording adjustment received structural
inspection; cross-wake runtime availability was not tested or independently
rechecked. It introduces no public private-location field.

The reviewer found the conditional design method usable for local repairs,
comparison surfaces, and materially new directions, and found no automatic
upgrade from learning to governance migration. This supports the reviewed
interpretation; it is not proof of real visual or autonomous-operation quality.

## Repository checks

- Python 3.12 suite: 118 tests, 117 passed, one skipped because the optional
  `python3.9` executable was absent.
- Strict documentation check: 36 canonical documents and 16 templates passed.
- Complete added public diff inspected for private profiles, paths, raw quotes,
  and resource inventories. Earlier working-tree edits were preserved.
- No live charter, permission mechanism, schedule, or external system changed.

Reproduce structural checks with Python 3.11 or newer from the repository root:

```sh
python3 -m unittest discover -s tests -p 'test_*.py'
python3 scripts/check_docs.py --strict
```

## Limitations and verdict

The bounded independent task and rule review are complete, including repair
and recheck of the observed packaging defect. Both normative contracts remain
`verification_status: partial`: no greenfield adoption, rendered interface
trial, or multi-epoch autonomy observation was completed. The separate
first-party epoch-evidence promise remains open.
