---
doc_type: evidence
status: historical
authority: evidence
last_reconciled: 2026-09-17
subject: template-outcomes-runtime-and-context-review
---

# Template review: user outcomes, actual effects, and necessary context

This is the English public edition of the September 6 research and design
review, revised on September 17. It preserves the dated findings and their
limits while explaining previously private references. The publication edit
does not rerun the historical experiments or update vendor capability claims.
This record is evidence and advice, not current project authority or mandatory
startup reading.

The review used repository baseline
`b0e5a8196fc529cb38da76d29d1d00c06e128403`, maintainer-reported problems, and
public technical sources. It recorded 111 passing repository tests and a
passing documentation check. It did not run commercial-agent compatibility
trials or obtain the original execution traces for the reported downstream
failures. Repository observations have stronger support than proposed causal
explanations or claims of improved user outcomes.

The recommendation was to organize work around an authorized user outcome
and observable effects, while retaining authority, evidence, and ownership
discipline. This does not require a new agent runtime, memory database,
scheduler, or requirements-management system. Most proposed improvements fit
existing contracts, entrypoints, verification records, and handoffs.

## Diagnoses considered and their limits

The review considered earlier assistant-written proposals. Those inputs are
not published, so this section explains the claims rather than asking readers
to reconstruct an exchange between unnamed assistants.

| Proposed diagnosis | Assessment in the September 6 review |
|---|---|
| Disable memory and require a single agent with a minimal runtime | No supplied owner decision established that preference. A minimal runtime is a useful comparison condition, not authority to exclude memory or delegation. |
| The mature checker proves that the template values process over outcomes | Checker maturity is a reason to investigate. File size and maturity alone do not establish the cause; behavioral acceptance was the more important evidence gap. |
| The `full` template profile and `adopted` stage are inherently wrong | Multiple profiles and an empty-product template exemption already existed. The unresolved question was the burden imposed on actual adopters. |
| A seven-stage method requires human approval at every stage | The contracts did not require that and allowed autonomous choices within scope. A fixed sequence could still encourage ceremony, but that hypothesis must be distinguished from an explicit rule. |
| Limit the entrypoint to 30–60 lines | A shorter task-relevant route is plausible; a universal line count has no demonstrated relationship to correctness. |
| Retired invariant identifiers still appear in new templates | Confirmed at the baseline: new templates taught `INV-1` despite the heading-based convention. This was a specific consistency defect, not the whole outcome problem. |
| Add runtime-boundary and behavioral acceptance records | Preserve the needed semantics, but first locate the failure before adding identities, receipts, memory promotion, and task-state records everywhere. |
| Inherit the evidence counts claimed by an earlier report | The underlying companion dataset and experiments were unavailable. The review did not inherit their counts or conclusions and assembled its own public source inventory. |

The inspectable repository basis is the [policy](../../docs-policy.toml),
[execution contract](../contracts/agent-execution-discipline.md),
[identifier convention](../contracts/documentation-harness.md#invariant-citations-resolve-to-headings),
and [contract template](../../templates/contract.md). Links show the current
files; the baseline commit identifies the historical versions. They are
first-party repository evidence, not an independent adoption trial.

## Portable semantics across runtimes

A shared filename, hook, or protocol does not establish equivalent behavior.
An instruction file might not load; a hook might observe without blocking; a
worker might inherit the full conversation or only its explicit assignment.
The portable requirements are:

1. The requested outcome, authorization, and exclusions remain identifiable.
2. Current facts and applicable authority can be located and reconciled.
3. Reads, writes, and externally visible effects stay inside the agreed scope.
4. After interruption or handoff, completed, incomplete, and unknown work can
   be distinguished.
5. Completion claims have appropriate observations and explicit limits.

These requirements still apply when implemented with files and shell commands.
Missing automation must not silently weaken a permission boundary or an
observation needed for the promised result.

The review used the [MCP architecture specification](https://modelcontextprotocol.io/specification/2025-11-25/architecture)
for connection/capability negotiation and the [Agent Skills specification](https://agentskills.io/specification)
for packaging procedural instructions. Neither selects a project's goals,
authorizes its work, or certifies completion. This was a scope comparison, not
a finding that every product implemented the same standard in the same way.

## Runtime observations recorded on September 6

The comparison sampled eleven product families for context, authority, and
completion differences. It was not a market ranking or compatibility
certification. Record product, client, version, mode, model configuration,
extensions, and relevant memory/permission state for any new comparison.
Most entries below came from one vendor's source family and were not
independently exercised. Rolling pages may have changed since the review.

| Product and historical baseline | Recorded mechanism and implication |
|---|---|
| Claude Code, 2.1.232/2.1.261 and documentation | Instruction-file bridging, fresh workers versus full-session forks, and interactive/headless defaults require actual loading checks. Creating a worker alone does not establish review independence. [Release](https://github.com/anthropics/claude-code/releases/tag/v2.1.232), [subagents](https://code.claude.com/docs/en/subagents). |
| Codex CLI, 0.153.3/0.153.4; app/Work considered separately | Delegation policies and prompting differed by environment and release. Record the actual configuration rather than inferring capabilities from a model name or a single execution mode. [Changelog](https://learn.chatgpt.com/docs/changelog), [subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents). |
| Kimi Code CLI, 0.41.0 and the legacy migration boundary | The new Node implementation, providers, explicitly supplied worker context, and background completion semantics limited reuse of old Python-runtime assumptions. Reasoning protocol state, memory, and project knowledge are different concerns. [Migration](https://www.kimi.com/code/docs/en/kimi-code-cli/guides/migration.html), [agents](https://www.kimi.com/code/docs/en/kimi-code-cli/customization/agents.html). |
| ZCode, 3.11.2 with 3.8.1/3.10.2 history | Instruction-loading scope, default-off main-session memory, and conflicting project-hook documentation required version-specific checks. Nested rules and imports could not be assumed to load. [Agents](https://zcode.z.ai/en/docs/agents), [changelog](https://zcode.z.ai/en/changelog). |
| DeepSeek Harness, 0.1.3-alpha.1 | Replaceable model/loop/storage components and changing session/log interfaces suggested studying boundaries without binding the template to internal session objects. [Architecture](https://www.deepseek.com/harness/en/), [releases](https://github.com/deepseek-ai/deepseek-harness/releases). |
| Cursor, documentation snapshot without a pinned release | Clean worker context required explicit task inputs; local and cloud work differed. The review did not establish an exact first-party specification for reported cross-brand session recovery. [Subagents](https://cursor.com/docs/subagents). |
| Amp, documentation snapshot | Modes combined model, effort, prompts, and tools; custom modes/subagents and selected key-configuration paths complicated blanket claims that models could never be configured. Switching cost and reproducibility remained evaluable. [Modes and models](https://ampcode.com/docs/models-and-subagents). |
| Gemini CLI, documentation snapshot | Hierarchical/on-access context files and `/memory` inspection did not imply automatic learning merely because the feature used the word memory. [Context files](https://geminicli.com/docs/cli/gemini-md/). |
| OpenCode, rules documentation without a pinned major | File precedence and configured references meant several instruction files might not all load. A rolling page could not certify several major versions. [Rules](https://opencode.ai/docs/rules/). |
| GitHub Copilot CLI, documentation snapshot | Combining instruction files and imports could duplicate content introduced by a bridge for another client. Inspect effective loading. [Instruction locations](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference). |
| Pi, 2025 author account and repository snapshot | A small core could gain workers, protocols, compaction, and permission controls through extensions. A small core did not imply that complex projects should prohibit those capabilities. [Design account](https://mariozechner.at/posts/2025-11-30-pi-coding-agent/), [repository](https://github.com/earendil-works/pi/tree/main/packages/coding-agent). |

Three recorded details illustrate the limits. Claude 2.1.261 release notes
reported fixes to resumed hook context and premature background completion;
that supported investigating runtime differences but did not diagnose the
maintainer's unavailable downstream traces. [Release notes](https://github.com/anthropics/claude-code/releases/tag/v2.1.261).

ZCode 3.8.1 notes advertised workspace hooks while its documentation said
project hooks were ignored. The more specific documentation was a conservative
configuration clue, not a resolution of the version conflict. [Changelog](https://zcode.z.ai/en/changelog),
[hooks](https://zcode.z.ai/en/docs/hooks).

The review also recorded that local Codex tool hooks did not cover hosted
WebSearch and therefore were not a complete permission boundary. Its import
documentation meant cross-brand migration could not be assumed exclusive to
another client. [Hooks](https://learn.chatgpt.com/docs/hooks),
[import](https://learn.chatgpt.com/docs/import).

## Outcomes and procedural completion have different feedback

At the baseline, the contracts already named user outcomes, failure/recovery,
quality attributes, production observations, risk-based execution, written
coordination, authorized discretion, and document retirement. A diagnosis that
these principles were entirely absent would be incorrect.

The proposed mechanism was more specific: filling a contract, writing a test,
running a checker, and updating a status give immediate completion signals.
Judging whether the user can accomplish the intended task is less mechanical.
An agent might substitute the former for the latter. Missing domain knowledge,
unobserved effects, and shared requirement misunderstandings are alternative
causes that need separate investigation.

At that baseline, execution's `enforced` status was qualified in its prose as
structural enforcement. It was not proof of adoption effectiveness. The
engineering-judgment contract was `target/pending`; its plan was correctly
completed because the authorized outcome was a draft target. A completed plan
did not claim that the proposed method had already been exercised.

The recommended correction was claim-specific acceptance: distinguish
structure checks, context-loading probes, and real user-scenario evidence.
Keep outcome, authority, factual basis, observation, and recovery obligations;
choose fixture-first, a failing regression, a runtime probe, or a packaged
entrypoint test according to the claim. Cheap evidence is useful only when it
can support the result being claimed.

## Express functional and quality requirements as scenarios

Extend the existing outcome/acceptance matrix with the actor, trigger, object,
required and forbidden effects, and relevant identity, frequency, timing,
quality boundaries, and next action. Keep each requirement at its existing
owner. The repository's `promise[...]` records are dated future commitments,
not a second product-feature inventory.

For example, detecting file changes is a function. Joining repeated clicks in
one operation, respecting a request budget, keeping unknown distinct from
unchanged, and explaining recovery are additional acceptance conditions for
the same user scenario. Do not fill unrelated quality categories by ritual.
The review related this approach to [SEI quality-attribute scenarios](https://www.sei.cmu.edu/library/reasoning-about-software-quality-attributes/)
and [user-centered experience metrics](https://research.google/pubs/measuring-the-user-experience-on-a-large-scale-user-centered-metrics-for-web-applications/).
The proposed matrix was the reviewer's design, not a structure validated by
those publications.

| Failure class | Observation | Example fault that acceptance should detect |
|---|---|---|
| Promised effect missing | Does the user entrypoint actually produce the result? | Disconnect the button or event registration while leaving helper tests green. |
| Undeclared effect | Requests, writes, permissions, notifications, and background work | Add an unrequested prefetch or configuration write. |
| Excessive frequency | Attempts and effects grouped by object and operation identity | Repeat clicks, open a second tab, retry, or replay after recovery. |
| Wrongly suppressed effect | Required work within its allowed time window | Change entity/account, expire cached data, or retry a failed operation. |

These classes are not exhaustive. Wrong objects or content, ordering, lateness,
partial updates, one-sided visibility, excess cost, and incomprehensible
results also matter. A total of three does not prove the correct three objects
were checked.

Tool-call counts are not effect counts. One call can issue several requests;
a timeout can follow a completed server-side write. Distinguish user intent,
logical operations, attempts, state changes, and notifications. The cited
[AWS idempotency account](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)
and [SRE overload guidance](https://sre.google/sre-book/handling-overload/)
addressed identity and load boundaries, respectively.

Observe the important boundaries without building an event platform for every
function. Finite observations do not establish unbounded absence of effects.
Production-only assumptions need an observation window and a recovery policy.

## Worked example: checking page-script dependencies

This is a design example for a browser extension that helps a user detect
changes to a page's script dependencies. No implementation or target-site
protocol was inspected. The example is complete enough to explain the design
questions; it is not a deployment specification for a private project.

Start by defining change: a new URL, changed bytes, a new implementation of a
logical role, or incompatible behavior are different promises. The same URL
can serve changed content; several files can implement one role. Establish
whether identity comes from a build manifest, actual loaded resources, module
exports, or a heuristic. Represent one-to-many and many-to-one mappings instead
of forcing three old files into three new ones by position or filename.

| Decision | Applicable approach | Required observation |
|---|---|---|
| Additional network work | Reuse sufficient page/build evidence; otherwise inspect a bounded candidate set | Each request has a purpose and any added permission cost is considered. |
| Meaning of change | Select evidence for bytes, version, or role compatibility | State the check type, baseline, observation time, and evidence strength. |
| Deduplication | Identify page version, account/environment, logical object, and operation | Join concurrent work without suppressing a new entity/version or expired result. |
| Stopping | Bound attempts, requests, duration, concurrency, and applicable retries | Return an explicit state when a bound is reached. |
| Ambiguous mapping | Present candidates, basis, and uncertainty | Do not truncate to three or call a partial match complete. |
| User action | Separate detection, mapping, configuration change, and compatibility verification | Show which step happened, affected files, and the available next action. |
| Recovery | Distinguish failure, partial result, and unknown effect; reconcile on restart | Avoid duplicate consumption, false freshness, and lost necessary retries. |

Passive observation is useful only when sufficient. The review cited
[Chrome webRequest caching limitations](https://developer.chrome.com/docs/extensions/reference/api/webRequest)
and [HTTP conditional-request semantics](https://www.rfc-editor.org/rfc/rfc9110.html#section-13.1.2)
to explain why request metadata, zero added requests, `304`, or weak validators
cannot substitute for every meaning of change. A mechanical `HEAD` followed
by `GET` can add a round trip.

Minimum work is relative to a freshness promise, detection guarantee,
permission boundary, and cost budget. No target-site policy or measurements
were available to establish a universally safe request frequency or guarantee
against account suspension. The implementer should find an economical method
within the agreed goal; only a material change to the goal or risk needs a new
owner decision.

A meaningful acceptance experiment runs the packaged extension against a
controlled page, account fixture, cache, and clock while observing requests,
persistence, and UI results. Include repeated clicks, multiple tabs, timeouts,
restart, three-to-five and five-to-three mappings, unchanged data, ambiguity,
and missing permission/evidence. This proposed experiment was not run; it does
not authorize load testing a real account.

## Reduce context cost by changing reading dependencies

The historical measurement found 30,973 bytes across three entry documents:
14,512 in `AGENTS.md`, 6,012 in `ARCHITECTURE.md`, and 10,449 in the document
map. Adding development, execution, and governance contracts produced a
107,449-byte illustrative read path, including 16,002 bytes of source and
reconciliation history. These are bytes on disk, not injected token counts or
proof that every task read all six documents.

Large documents do not by themselves prove poor modularity. Ask whether a
local task needs unrelated domain knowledge, a single rule is copied into many
owners, or a successor can find the current outcome and unfinished work.
Splitting a file into equal pieces does not resolve those dependencies.

Separate the information by use: template maintainers need rationale,
research, and history on demand; adopters need their own current boundaries,
contracts, and runtime facts; an executing task needs its goal, authority,
relevant code/rules, current progress, and material unknowns. The distinction
can be made inside one repository without inventing several products.

Entrypoints should contain core constraints and short routes to relevant
methods. Merge live decisions into their current owners before retiring old
working records. Completed plans are history, not current work registers.
Measure omitted constraints, stale knowledge, necessary reads, and actual task
results when evaluating a shorter context route; smaller input alone does not
establish better work.

## Memory, handoffs, and delegation

Derived context can locate facts and preferences but cannot manufacture
authorization or override current decisions. When observation disagrees with a
contract, preserve the observation and reconcile the implementation or rule.
For consequential experience, retain the source, applicability, and invalidation
condition. Reconstructible code facts need not be copied into a new database.
The review compared the separate responsibilities described in
[OpenAI memory documentation](https://learn.chatgpt.com/docs/customization/memories)
and [Anthropic memory documentation](https://code.claude.com/docs/en/memory);
that comparison did not prove every configuration safe from stale-context use.

Choose delegation by dependency and integration cost. Independent research and
read-only review can benefit; concurrent writes can conflict even when file
names differ. Each substantial assignment needs the parent outcome, allowed
writes/effects, baseline and environment, relevant rules/evidence, expected
artifact/checks, and a return path for failure. A short read-only task can carry
these in the native assignment rather than a separate form.

The parent inspects artifacts and results, reconciles stale baselines,
conflicts, failure and cancellation, and verifies the integrated outcome.
A worker's completion report does not establish whole-system success. Shared
files, cancellation, and background-process lifetime depend on the actual
runtime and must not be invented in a report.

Implementation workers may inherit useful history. Independent reviewers
should receive governing inputs and evidence without the implementer's
reasoning trace. Outcome acceptance also needs the original request and its
accepted interpretation; a diff alone can validate the wrong goal. Fresh
context reduces one source of correlated error, not shared model or rule errors.

The dated [Cognition account](https://cognition.com/blog/multi-agents-working)
and [Anthropic harness account](https://www.anthropic.com/engineering/harness-design-long-running-apps)
were used as examples of changing coordination practices, not proof of a
permanently best worker topology or stage count.

## Responses to reported practical problems

These are self-contained summaries of the problems motivating the review.
They are not excerpts that require the original conversation. The original
review proposed retaining source-language quotations where useful. The
maintainer replaced that recommendation on September 17 with contextual
English accounts throughout the public repository.

| Reported problem | Proposed correction | Insufficient completion signal |
|---|---|---|
| Jargon and generic prose burden readers | Name the actor, condition, action, impact, and next step; explain necessary terms through contextual examples | Forbidden-word counts, readability scores, or a request to sound natural |
| Delivery loses the user's goal | Retain the request and accepted interpretation; observe the complete scenario | Test counts, complete forms, checked task boxes |
| Wording leaves room for incompatible interpretations | Use plain language and contrasting examples that identify excluded meanings | Assuming a language choice alone eliminates ambiguity |
| Repeated failures produce an ever-growing rule set | Identify the mechanism, make a small durable correction, try a related unseen case, and retain removal conditions | A permanent rule for every incident or self-authorized goal changes |
| Old documents burden new work | Separate current decisions from optional history and preserve necessary rationale | Splitting by byte count or deleting solely by age |
| Authorized work stops at every internal phase | Continue through the outcome; pause only for a new material decision or real blocker | Repeated approval requests or treating silence as new authorization |
| Declared and actual behavior differ | Verify requirements against effects and effects against authorization | Deriving all requirements from existing tests |
| Reports ignore user cost and next action | Exercise the path from trigger through result, recovery, and follow-up | A rendered page, HTTP 200, or green mocks alone |

For the extension example, a useful message says: "Five candidate scripts were
found, but their relationship to the previous files is not yet confirmed. The
previous configuration is unchanged; the candidates and matching evidence are
shown below." It explains state and next action without hiding uncertainty
behind an internal label.

New facts can emerge during authorized delivery. Investigate checkable facts
and resolve reversible choices inside scope. Pause only the affected path when
new evidence changes the intended outcome, authority, irreversible cost, or
accepted risk. Internal evidence checks do not automatically require human
sign-off.

## Improvement should reduce failures and maintenance burden

Reconstruct the observation and impact; distinguish missing input,
misinterpretation, implementation defects, observation gaps, and premature
completion; then change the cheapest reliable owner. A script defect belongs
in the script, invalid state at its boundary, unclear requirements in examples,
and a poor reading route in the entrypoint. Record which old reminder or
redundant rule the correction replaces.

A lesson and a test written by the same agent can share the same mistake.
Preserve related cases not used in design or obtain independent feedback.
Local repair authority does not authorize changing objectives, risk budgets,
or acceptance standards. Evaluate recurrence, false completion, omitted
effects, human rework, and cost rather than the number of rules or memories.
After runtime changes, test whether old scaffolding can be removed safely.

## How the template could establish behavioral value

Keep the checker responsible for structure. Add a few reproducible adoption
exercises before building a general evaluation platform: an ordinary bug,
existing reusable code, a disconnected user entrypoint with passing helpers,
repeated requests, incorrect deduplication, mistaken requirement translation,
stale memory, context handoff, unfinished background work, and unclear user
messages. Actual operation, packaged artifacts, controlled external effects,
and user outcomes supply the evidence.

Calibrate acceptance with known faults before scaling it. Compare the current
instructions, a shorter equivalent route, and a targeted mechanism correction.
Hold task, code, model/configuration, tools, initial state, and budgets fixed;
repeat and interleave conditions. If old hosted behavior cannot be restored,
state that limit rather than attributing the result to one factor.

Distinguish successful context delivery from improved behavior. Observe goal
completion, incorrect effects, inappropriate stopping/continuation, human
correction, and time/token costs separately. A speed gain does not cancel a
harmful side effect.

The historical review found limited and differing research results:
[Gloaguen et al., v1](https://arxiv.org/html/2602.11988v1) studied Python issue
tasks with one sample per condition; [Lulla et al., v2 abstract](https://arxiv.org/abs/2601.20404v2)
reported efficiency benefits, but the full paper was not inspected in that
review; [Khatri's preprint](https://arxiv.org/html/2607.27250v1) reported no large
correctness change in 17 tasks across three repositories and 288 valid
evaluations. Their methods and limits did not establish this template's
behavior in long real projects. Local behavioral evidence remained a strong
recommendation; superiority of a particular context layout remained unproven.

## Recommended implementation boundaries

These were September 6 recommendations, not a newly assigned portfolio or a
sequence of human approval gates. Current contracts and later change records
own what was subsequently adopted.

| Existing owner | Proposed change | Needed evidence |
|---|---|---|
| Development and delivery templates | Connect intended outcomes, actual effects, identity, frequency/timing, and next action to acceptance | Representative missing, extra, repeated, suppressed, wrong-object, and partial-result faults are detected |
| Execution and governance | Preserve outcome/evidence duties while choosing methods proportionately and avoiding phase approvals | Authorized work reaches a usable result; new risk pauses only its affected path |
| Entrypoints and document map | Route domains on demand; reconcile live decisions; stop generating retired identifiers | Less irrelevant reading without lost authority or acceptance boundaries |
| Plans and handoffs | Carry bounded assignments, baselines, effects, artifacts, and return states when coordination is needed | Resume, cancellation, conflict, and integration observations |
| Client configuration | Add only needed instruction bridges and trusted, verifiable hooks | Effective loading in cold start, resume, and workers; explicit uncovered capabilities |
| Template evidence | Retain structural checks and add a few real adoption tasks | Observed improvements in outcomes and human effort before expanding scope |

One authorized pilot should reach a coherent working end state. Internal
construction follows dependencies; half-edited documents are not delivery.
The review did not recommend immediate plugins for every vendor, one session
format, another terminology system, a universal engineering score, or making
the structural checker a judge of semantic agreement.

## Published evidence and reproduction boundary

- [Sources](2026-09-06-template-review/sources.json): 43 selected identities,
  dates, observations, and limits; unknown publication dates remain unknown.
- [Version observations](2026-09-06-template-review/version-history.json):
  20 changes or observation baselines, not all versioned releases.
- [Repository measurements](2026-09-06-template-review/repository-observations.json):
  paths, sizes, hashes, and history for this repository at the stated baseline.
- [Recorded checks](2026-09-06-template-review/check-results.json): the historical
  111-test result and documentation checks; they are not today's test results.
- [Behavioral cases](2026-09-06-template-review/behavioral-cases.json): proposed,
  unrun exercises rather than demonstrated user outcomes.
- [Methods](2026-09-06-template-review/methods.json): variables, comparison
  design, public-source retrieval, and limits.
- [Limitations](2026-09-06-template-review/limitations.json): missing downstream
  traces, source disagreements, and unavailable earlier evidence.
- [Input account](2026-09-06-template-review/input-provenance.json): distinguishes
  the maintainer's request from earlier assistant interpretations; private
  reports are not presented as files supplied to readers.
- [Inspection script](2026-09-06-template-review/reproduce.py): run
  `python3 docs/evidence/2026-09-06-template-review/reproduce.py --checks` with
  Python 3.11+ in a checkout to inspect that checkout and run its checks.
  It does not run commercial agents, recover private inputs, or recreate the
  historical environment. The historical commit is needed to compare old
  repository measurements; current output will legitimately differ.

The collection retained source identities, short observations, and repository
fingerprints rather than full webpage mirrors. Rolling sources may change.
The retrieval method provides no vendor-specific breadth guarantee. No hidden
reasoning traces, private memory, or real-account traffic were collected.

The completed layer was research and improvement design. This report did not
implement the discipline changes, certify commercial-runtime compatibility,
or repair the reported downstream products.
