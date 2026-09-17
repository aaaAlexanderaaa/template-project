# Engineering Discipline Template

This is a domain-neutral engineering template. It is independent of any
particular product, framework, or runtime, and it contains no product
implementation. Its most important product is not the directories, templates,
or checker, but the judgment and delivery discipline those carriers exist to
hold.

This repository is a harness: a working institution under which a cognitive
subject with high local intelligence and low native executive function — one
that acts on the real world through tools — can be delegated work over the
long term, with its failures sedimenting into organizational learning instead
of organizational debt. Everything here serves the requested observable
outcome; contracts, tests, documents, and checks preserve intent and expose
mistakes, and completing them alone is never completion of the task.

Two further observations shape the discipline: the owner's attention is the
most expensive resource and compute is the cheapest, so cost is pushed toward
the machine side by default — while staying cost-aware, because quotas and
circuit breakers protect accounts and attention rather than ration compute;
and a claim that was not verified is not true, however plausible it sounds.
The discipline has been exercised and corrected in the maintainer's own
projects since 2026-07, and feeding that experience back is a standing
practice; independent adoption remains the open frontier.

## Transfer value order

When an agent enters this repository and decides for itself what to take away,
rank attention by breadth of use, downstream leverage, cost of being wrong,
portability, and how much the target project must already exist:

| Base priority | Understand first | Why first | Current owner |
|---|---|---|---|
| **P0** | Human–agent interaction and epistemic discipline | It decides whether facts are established, whether the right question is asked, and whether user authority and task scope are preserved; it affects every later judgment | [development discipline](docs/contracts/development-discipline.md) § research-unknowns – causal-mechanism; [governance boundary](docs/contracts/governance-decision-boundary.md) (all invariants) |
| **P1** | Current truth, authority, ownership, dependency boundaries, and historical debt | It decides whether existing truth is overwritten, whether rules are copied, and whether local debt spreads across the project | [architecture](ARCHITECTURE.md); [development discipline](docs/contracts/development-discipline.md) § one-owner – coherent-end-state; [project adoption](docs/contracts/project-adoption.md) § current-vs-target – visible-debt |
| **P2** | Coherent end states, risk-scaled execution, outcome-specific evidence, class-level guards, failure recovery, and the test for facts that leak across the system if left unnamed | It decides how a correct understanding becomes a verifiable complete delivery, and whether an unnamed default will have to be cut over later | [agent execution](docs/contracts/agent-execution-discipline.md) § risk-selects-depth – smallest-route; [development discipline](docs/contracts/development-discipline.md) § outcomes-first – decisions-not-volume; recognition rule in [foundational runtime](docs/contracts/foundational-runtime-discipline.md) |
| **P3** | Frontend, backend, cross-stack, style, data, operations, security, performance, time/calendar, demonstration data, and other conditional disciplines | They are high-value when the target project activates the matching boundary, and should be promoted by real risk | the matching domain contracts in [development discipline](docs/contracts/development-discipline.md) and the activated concern owner; time and demo invariants: [foundational runtime](docs/contracts/foundational-runtime-discipline.md) |
| **P4** | Documentation topology, templates, adoption stage, policy manifests, the checker, and CI examples | They carry or enforce the discipline above; copyability is not the same as value priority | [documentation map](docs/README.md); [documentation harness](docs/contracts/documentation-harness.md) |

This is an **attention and extraction order**, not the document authority
order, and not a requirement to copy everything. Target-project evidence can
promote a P3 domain into P1/P2; for example, a complex UI immediately moves
user states, interaction, accessibility, and style ownership forward. Learning
and adoption use the same ranking; only the latter writes into the target
project and requires governance authorization. Take the method first, then
decide whether this repository's files and tools are needed.

The documentation checker depends only on the Python standard library.
The minimum version is Python 3.11.

## How to use it

1. Read `docs/README.md` for the document authority order.
2. Start a new project from this repository. For a running project, first do
   the read-only inventory in `docs/guides/onboarding.md`; do not overwrite
   existing authority.
3. Record current facts, governance scope, priority authority, and adoption
   stage in `templates/adoption-assessment.md`, and have the project owner
   confirm them.
4. Declare those decisions in `docs-policy.toml` (see “Scaling to project
   size” below): `[adoption].stage`, `source_roots`, `managed_paths`, and
   `[templates].profile`. The checker reads these fields; it does not assume
   one project shape.
5. Complete a current-state `ARCHITECTURE.md` and the relevant contracts
   before the first governed product change. Date/time and operator-visible
   demo data are [development § activate-concerns](docs/contracts/development-discipline.md#activate-concerns-instead-of-expanding-ceremony) concerns: read them when they apply; do not fill a pit
   catalog when they do not.
6. Material delivery must land a contract first. When a technical fact cannot
   be learned read-only, use [development § contract-first](docs/contracts/development-discipline.md#contract-before-material-delivery-evidence-before-certainty)'s disposable controlled-experiment path; the
   experiment must not become product behavior.
7. Choose the [smallest execution route](docs/contracts/agent-execution-discipline.md#the-harness-selects-the-smallest-executable-route).
   Authorized low-impact local behavior may update its existing owner without
   a standalone plan. Only the high-risk route requires independent design
   review and a fresh-context evaluation. Classification does not grant authority.
8. Configure `architecture-rules.toml`, or record why it does not apply.
9. Run the unit tests and `python3 scripts/check_docs.py` with Python 3.11+.
10. Adapt `templates/ci/docs-check.example.yml` to the project's own CI.

## Scaling to project size

The template does not assume project size, and it does not require a finished
migration before CI is connected. Four knobs live in `docs-policy.toml`:

| Knob | Role | Typical values |
|---|---|---|
| `[adoption].stage` | Whether adoption work fails the build | `observed`/`baselined` report and return 0; `scoped_enforcement`/`adopted` block |
| `[adoption].source_roots` | What counts as product code | `["src"]`, `["app", "lib"]`, `["packages"]`, `["cmd", "internal"]` |
| `[adoption].managed_paths` | Governed boundaries under `scoped_enforcement` | `["packages/billing/**"]` |
| `[templates].profile` | Which templates are required (tiers accumulate) | `minimal` / `standard` / `full` |

That produces these working modes:

- **Small project:** `profile = "minimal"` keeps only the contract, plan,
  issue, and guide templates; the rest can be deleted. Leftover references to
  removed templates become advisory and do not turn the build red.
- **Running project:** the checker can enter CI on day one. `stage =
  "observed"` prints unfinished adoption work and returns 0, then tightens as
  the stage advances.
- **Layouts other than `src/`:** if code sits outside every configured source
  root, the checker names it instead of giving a meaningless green result on an
  empty set. The same stage rule applies: early stages only report, so CI can
  start before the layout is fully declared. Files in the repository root
  (`setup.py`, `conftest.py`, `vite.config.ts`, and the like) never count as
  product code. Tooling directories go in `harness_paths`, which accepts globs
  such as `tools/**`.
- **CI:** structural problems are errors. Findings that appear only because a
  date moved (an aged target, an overdue promise, expired pending evidence)
  default to advisory. Put `--strict` on a scheduled job so a calendar change
  does not fail an unrelated pull request. A rule set to `off` stays off even
  under `--strict` — turning it off is the project's own decision.

## Layout

```text
.
├── README.md                 # English homepage
├── AGENTS.md                 # working agreement for automated developers
├── CONTRIBUTING.md           # shared workflow for humans and agents
├── ARCHITECTURE.md           # structural authority template for the adopting project to fill
├── architecture-rules.toml   # machine-checkable baseline architecture boundaries
├── docs-policy.toml          # document aging, templates, and adoption policy
├── docs/
│   ├── README.md             # document authority and lifecycle map
│   ├── contracts/            # current, durable norms
│   ├── design/               # raw ↔ translated contracts for UI surfaces
│   ├── plans/                # execution plans for one change
│   ├── issues/               # lifecycle of defects and audit findings
│   ├── guides/               # operating and maintenance procedures
│   └── evidence/             # durable, reviewable evidence
├── templates/                # copyable templates; they have no project-behavior authority
├── scripts/                  # portable mechanical enforcement of the discipline
├── src/                      # product-code placeholder; currently empty
├── tests/                    # checker fixture tests; add product tests after adoption
├── tmp/                      # local scratch evidence; gitignored
└── archive/                  # local replacement backups; gitignored
```

## Migration principles

Migrate the method, not the original project's tools or numbers:

- A contract precedes material delivery; unknown technical facts are
  investigated or run as bounded, disposable experiments.
- Current authority is identifiable.
- Conflicts must be reconciled.
- Plans aim at one coherent end state.
- Defects are fixed by category; add a class-level guard when a sibling
  mechanism is repeatable and the cost is proportionate.
- Frontend work enumerates reachable states and combines perceptual and
  structural evidence.
- Frontend visuals and copy are translated from a raw brief: design candidates
  and probes are evidence only; accepted direction enters the surface/style
  owner; missing product intent still returns to a human decision.
- Style has one owner: layer order, shared visual-value tiers, and the
  published override surface are explicit. Consumers compose published
  contracts; unauthorized escalation is recorded as owned debt with a removal
  condition.
- Backend work names state ownership, failure, and recovery.
- Time policy declares scope and the roles of storage, calendar calculation,
  input, and display. Visible demonstration data meets its declared temporal
  promise; mutations remain environment-gated. Read the
  [runtime owner](docs/contracts/foundational-runtime-discipline.md) when activated.
- Agent risk decides execution depth; high-risk design and acceptance use a
  genuinely independent context.
- Each activated quality concern has one normative contract as owner; plans
  record links, steps, and evidence, not a second copy of the policy.
- Developers own direction and priority; the framework supplies facts, risks,
  recommendations, and bounded execution gates.
- Unfamiliar references and checkable facts are not filled in by guessing;
  prefer primary or official sources, and when a tool is unavailable first
  seek a fallback that preserves semantics and evidence strength.
- Investigate technical facts first; the executor makes reversible engineering
  choices; product intent, material trade-offs, and risk acceptance return to
  the user as a bounded choice. Interdependent decisions advance on a
  prerequisite-safe frontier and establish authorization before delivery;
  an existing explicit instruction covering that understanding is sufficient.
  Analysis is judged by whether it makes the causal mechanism, applicable
  boundary, and material implied questions clear.
- Onboarding preserves current facts first, then tightens
  observed → baselined → scoped_enforcement → adopted.
- Task, task-group, objective, and release-gate completion close separately;
  lower-layer completion does not impersonate a higher layer.
- Raw inputs and derived representations stay layered; deletion, migration,
  and GC keep verifiable evidence.
- Prefer rules in the environment over rules in memory.
- Plans, contracts, issues, and evidence do not impersonate one another.
- Documentation governance manages both increment and stock: update, merge,
  distill, retire, and delete scratch evidence. File counts, line counts, and
  a uniform retention age are not substitutes for quality judgment.

Viewport count, test framework, directory depth, publishing platform, style
scheme (CSS organization, token names, and theme implementation), and file-line
thresholds must be decided again by the actual project.

## License

This repository is published under the [MIT License](LICENSE).
