---
doc_type: plan
status: completed
authority: planning
last_reconciled: 2026-07-26
implements: docs/contracts/agent-execution-discipline.md
supersedes: []
---

# AI agent execution governance implementation plan

## Cold-start summary

The template already governs contracts, document lifecycle, frontend surfaces,
backend services, cross-stack work, and evidence. It does not yet provide a
complete execution profile for autonomous coding agents: fixture-first phases,
work selection when no task is ready, mandatory independent lenses for
high-risk design, fresh-context holistic evaluation, or layered completion.

The governing target is
`docs/contracts/agent-execution-discipline.md`. This plan adds that profile
without making heavyweight multi-agent review mandatory for routine work.

## Authority and prerequisites

- Structural authority: `ARCHITECTURE.md`
- Base discipline: `docs/contracts/development-discipline.md`
- Target contract: `docs/contracts/agent-execution-discipline.md`
- Harness contract: `docs/contracts/documentation-harness.md`
- Baseline evidence: prior checker and 31 fixture tests

## Complete end state

The repository exposes a domain-neutral, risk-based AI execution contract and
four reusable templates. The documentation harness validates the new template
inventory, fixture tests guard the new requirements, contributor guidance
routes applicable work to the contract, and Python version mismatches fail with
an actionable message.

## Current state and gap

| Concern | Current verified fact | Contract requirement | Gap/evidence |
|---|---|---|---|
| Agent design review | Independent verification appears only in selected templates | Three independent lenses plus separate synthesis for high-risk work | No reusable record |
| Implementation loop | Eight-step contract workflow | Fixture-first and red-first seven-phase engineering loop | Not explicit |
| Work selection | Read order exists | No-idle portfolio decision tree | Missing |
| Completion | General definition of done | Task/group/objective/release layering | Missing |
| Runtime entry | Before this change, Python 3.11 was documented but Python 3.9 raised a raw `tomllib` traceback | Wrong runtime fails actionably | Friendly preflight was missing |

## Execution order within one coherent change

### 1. Extend the normative discipline

- Land the agent execution contract before template/checker changes.
- Update authority and contributor entrypoints.
- Preserve the base development contract as the default for routine work.

### 2. Add reusable execution and review records

- Add agent execution plan, independent review, holistic evaluation, and
  evidence-preserving data templates.
- Keep product terms, agent vendors, and orchestration APIs out of templates.

### 3. Extend the documentation harness

- Register the templates and required sections in `docs-policy.toml`.
- Extend template type validation.
- Add fixture tests for inventory and section failures.
- Add a friendly Python 3.11 preflight.

### 4. Verification and closure

- Run the Python 3.11 fixture suite and repository checker.
- Run a Python 3.9 preflight check when available.
- Update contract implementation/verification status and this plan's
  completion record.
- Keep the promised real-project independent adoption review open until it is
  actually performed.

## Risk register

| Risk | Trigger | Impact | Prevention/detection | Recovery |
|---|---|---|---|---|
| Governance becomes too heavy | Routine changes routed through all reviews | Contributors bypass the system | Risk profiles and explicit applicability | Reclassify with recorded rationale |
| Fake independence | Same context authors every lens | False confidence | Required verifier identity and limitation fields | Mark blocked or obtain human exception |
| Template sprawl | Multiple overlapping records | Authority becomes unclear | Four bounded templates and docs-policy inventory | Supersede redundant templates explicitly |
| Generic template absorbs product vocabulary | Concrete source terms enter reusable files | Portability loss | Scoped repository-independence audit | Remove product-specific language |
| Runtime mismatch remains opaque | Default Python is older than 3.11 | Checker appears broken | Entry preflight and documented canonical command | Use Python 3.11/uv path |

## Verification matrix

| Outcome | Unit/class guard | Integration/lifecycle | User-visible/probe | Evidence path |
|---|---|---|---|---|
| New templates remain complete | Missing-file and missing-section fixtures | Repository checker | Actionable path/section errors | contract acceptance record |
| Agent profile is reachable | Metadata/link checks | Authority-map and guidance review | Cold-start read-order inspection | plan completion record |
| Runtime mismatch is clear | subprocess preflight test | Python 3.11 suite | Python 3.9 error text | plan completion record |
| Existing governance remains green | 31 pre-existing plus 3 new fixtures | repository check | no product-specific terms | plan completion record |

## Rollout, migration, and rollback

- This is an additive template change with no product data migration.
- Existing adopted projects opt into the new contract and templates explicitly.
- Removing the new profile requires superseding the contract and updating the
  template inventory; silent deletion is forbidden.

## Explicit non-goals

- No product implementation.
- No mandatory multi-agent review for routine changes.
- No execution of agent orchestration from the documentation checker.
- No claim that one review topology fits every team.

## Progress log

- **2026-07-26 — in progress:** target contract and coherent plan landed before
  templates and checker changes.
- **2026-07-26 — completed:** added and registered four domain-neutral
  templates; updated agent, contributor, contract, authority-map, and root
  entrypoints; added template inventory/section fixtures and a Python 3.11
  preflight; all 34 fixtures and the repository check passed.

## Completion record

- Final revision/commit: verified working tree; commit intentionally left to
  the repository owner
- Contract implementation status: implemented
- Contract verification status: enforced
- Issues resolved/superseded: none
- Durable evidence: this completion record and
  `docs/contracts/agent-execution-discipline.md` § “Acceptance evidence”
