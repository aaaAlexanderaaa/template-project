---
doc_type: plan
status: completed
authority: planning
last_reconciled: 2026-07-27
implements: [docs/contracts/development-discipline.md, docs/contracts/documentation-harness.md]
supersedes: []
---

# Style ownership discipline plan

## Cold-start summary

The frontend discipline specified reachable states, layout and size contracts,
interaction maps, accessibility, responsive bands, and the evidence classes
that prove them. It never named who owns a shared visual value, in what order
style layers win when they disagree, or what a consumer may change on somebody
else's unit. The words describing that failure class appeared nowhere in the
repository.

That is the gap where large frontends actually decay. The documented mechanisms
are consistent across stacks and decades: override strength escalates because
precedence was never declared; the same value acquires several owners because
none was named; consumers reach into internals because no finite override
surface was published; escape hatches normalize because they carry no owner or
expiry; and style volume grows with feature count rather than decision count
because nobody can prove a rule is dead.

## Authority and prerequisites

- [development-discipline.md](../contracts/development-discipline.md) owns
  frontend discipline and is the only place this may land. A separate style
  contract would give frontend work two owners and commit the D2 violation the
  change exists to prevent.
- [documentation-harness.md](../contracts/documentation-harness.md) owns the
  mechanical enforcement surface and its limits.
- `ARCHITECTURE.md` §8 already classifies hard, soft, and family boundaries.
  Style ownership is expressed in that existing vocabulary rather than a new
  axis.

## Complete end state

Style ownership is an instance of D2, stated once in the frontend contract,
carried into a project by a copyable declaration, and checked by structure the
harness can actually validate. A project that owns no style is asked for
nothing. A project that opts in has its layer partition and value-tier
direction proved mechanically, and its remaining rules enforced by literals it
supplies itself.

## Current state and gap

| Concern | Before | After |
|---|---|---|
| Shared visual value ownership | unnamed | named in D2 and in the frontend contract |
| Layer precedence | undeclared | declared and partition-checked when opted in |
| Value tiers | absent | declared, direction enforced by array index |
| Override surface | implicit | published surface is soft, everything else hard |
| Escalation debt | untracked | registered with owner and removal condition |
| Style corpus coverage | invisible | every corpus file resolves to exactly one layer |

## Execution order within one coherent change

1. Extend D2's enumeration to include shared visual values, so style ownership
   is an instance of an existing invariant rather than a new peer.
2. Add the `Style ownership and layering` subsection to the frontend contract
   and require the style layer, tiers, and override surface as inputs.
3. Add `templates/style-system.md` and register it in `docs-policy.toml` under
   the `full` tier, its declared `doc_type`, and its required sections.
4. Add the optional `style-ownership.toml` validation to the checker, gated on
   file existence, and extract glob safety into one shared resolver so both
   manifests reach the filesystem through the same escape checks.
5. Carry the vocabulary into `AGENTS.md`, `ARCHITECTURE.md`, `CONTRIBUTING.md`,
   the surface and cross-stack templates, `docs/design/README.md`, the
   onboarding inventory, and the Chinese `README.md`.
6. Record H11 in the harness contract against a real dated source anchor, and
   add fixture tests for every new failure class.

## Risk register

| Risk | Prevention |
|---|---|
| The discipline prescribes a tool or a methodology | No framework, preprocessor, naming convention, or delivery mechanism is named anywhere in the change. |
| Another project's measured numbers leak in as defaults | No layer count, tier count, budget threshold, or forbidden literal ships. Every number is the adopting project's own. |
| A non-frontend project inherits new burden | The manifest does not ship; absence is a decision. The template sits in the `full` tier and is deletable at lower profiles. |
| The checker drifts toward parsing stylesheets | H11 and the forbidden-behavior list state the limit; the implementation compares paths, array indices, and strings only. |
| A green check implies more than it proves | The acceptance table names what each guard establishes, and the surface template states that style ownership is proved structurally rather than perceptually. |
| Glob safety is re-derived and diverges | One resolver owns include/exclude handling and escape prevention for every manifest. |

## Verification matrix

| Outcome | Check | Evidence |
|---|---|---|
| Repository remains structurally valid | `python3 scripts/check_docs.py --today 2026-07-27` | PASS — 12 documents, 15 templates, profile `full` |
| No shipped deadline turns an adopter red later | `python3 scripts/check_docs.py --today 2027-06-30` | PASS — only the pre-existing advisory promise, still non-blocking |
| A hygiene run stays green | `python3 scripts/check_docs.py --strict` | PASS |
| Every new failure class is guarded | `python3 -m unittest discover -s tests -p 'test_*.py'` | PASS — 84 tests, 18 of them new |
| Opting out costs nothing | absent-manifest fixture | PASS — corpus present, no manifest, no style findings |
| Changed content is whitespace-clean | `git diff --check` | PASS — no output |

## Rollout, migration, and rollback

- Adopters upgrading the harness inherit no new obligation until they create
  `style-ownership.toml`. Deleting that file disables every style check.
- A project already carrying filled-in surface contracts keeps them valid: the
  new surface subsection is added to the template, and existing copies under
  `docs/design/` are not rewritten by the template change. Adding the
  subsection to a live surface is a normal reconciliation, not a migration.
- A brownfield project whose stylesheets do not yet partition cleanly declares
  `status = "template"` until they do, or narrows `scan` to the boundary it has
  actually organised.
- Rollback is deleting the manifest and the template entry; no product code and
  no other document depends on either.

## Explicit non-goals

- No CSS parsing, specificity computation, or cascade simulation.
- No browser automation, screenshot comparison, or visual regression gate.
- No shipped layer count, tier count, naming convention, or budget threshold.
- No opinion on which styling technology a project should use.
- No adoption gate for style: absence of the manifest is a decision, not an
  unfinished migration step.

## Completion record

- **2026-07-27 — completed:** style ownership landed as an instance of D2 in
  the existing frontend contract, a `style-system.md` template carried the
  project-level declaration, and an optional `style-ownership.toml` made layer
  partition and value-tier direction mechanically checkable without the checker
  learning anything about CSS.
