---
doc_type: guide
status: current
authority: guidance
last_reconciled: 2026-09-28
projection_of: [docs/contracts/development-discipline.md, docs/contracts/agent-execution-discipline.md, docs/contracts/project-adoption.md]
---

# Information access: obtain usable evidence and retain useful methods

## Purpose

Use this method when source access is uncertain, costly, recurring, or sensitive
to how content is observed. It applies during coding, review, and ordinary
information gathering as well as research. The existing
[fallback invariant](../contracts/development-discipline.md#tool-failure-triggers-capability-preserving-fallback)
owns capability, evidence strength, retry, and reuse boundaries.

This is a callable role and method, not a tool installer or a requirement to
dispatch another agent. Straightforward access needs no separate record.
[Research](research.md) decides which observations matter to the question;
access work obtains them and states what the method actually observed. The
task owner decides whether a gap warrants further spending or a narrower claim.

## Preconditions

Identify the source or information needed, the property to observe, its role in
the parent question, permissions, resource limit, previous attempts and their
cost, and any permitted locator for prior methods. Use the existing task and
tool context. Do not search unrelated private locations or assume that access
to credentials or a paid service has been authorized.

## Invocation

For the current agent:

> Use `docs/guides/information-access.md` to obtain this material. Check known
> methods before repeating exploration; report what you actually observed,
> its limits, and any method worth reusing.

For bounded delegation:

```text
Use docs/guides/information-access.md as the access role.
Parent question and why this material matters: [original purpose]
Source and required observation: [identity, version/date, content or behavior]
Existing methods and prior attempts: [permitted locator, result, spent effort]
Allowed tools/effects, remaining total time or attempt budget, tool-specific
caps if needed, and stop condition: [shared envelope across retrieval routes]
Return destination and permitted method-record owner: [existing task/location]

Obtain the required material where possible. Verify that the method observes
the needed property; preserve partial or failed access as such. Return source
identity, actual observation and its limits, attempts and available cost,
the remaining gap, and useful reuse or revalidation information. Do not reset
the parent budget, broaden permissions, or infer missing content. If permitted
durable storage is unavailable, return the method to the task owner and state
that persistence and future reuse remain unverified.
```

## Procedure

### Retrieve prior experience before repeating exploration

Use the task's supplied locator, relevant project guide, tool configuration or
approved private entrypoint. Match source, required capability, and environment
conditions, not just a similar page title. Read the smallest relevant note.
Absence of a note is not permission to create another global memory system.

Check the recorded conditions and last observation against the present task.
Try a still-applicable verified route before rediscovering alternatives. A past
failure can become irrelevant after authentication, page structure, service,
network, or tool conditions change. Refresh the observation rather than blindly
trusting or permanently rejecting the old route.

### Obtain the property the claim needs

Choose a method that can observe the required property. An extracted article
may answer a question about its prose while failing to show comments, layout,
interaction, or media. A transcript may identify a passage without establishing
its exact wording. Source identity and reading range matter alongside tool
success. These examples select checks; they are not universal tool rankings.

Use available fallbacks that preserve the needed evidence and permission
boundary. Another tool reading the same underlying material may improve
observation fidelity; it does not add an independent real-world observation.
Two readers can agree while sharing the same omission. If only an abstract,
archive, quotation, or secondary account is accessible, identify its status
and what remains unobserved rather than describing the original as fully read.

### Decide whether another attempt is worthwhile

Ask what changed since the last attempt and what the alternative could recover.
Track material effort across routes and handoffs in the existing task record;
the resource envelope belongs to the parent task. Different tools do not each
receive a fresh full allowance. A web-call cap alone does not bound a browser
fallback: state how that route fits the shared time or attempt allowance before
starting it. A capability-preserving fallback is useful;
unbounded retries against an unchanged failure are not.

Stop when the required observation is obtained, no justified permitted route
remains, or the budget is reached. Rate-limit and account responses follow the
existing [resource rule](../contracts/agent-execution-discipline.md#billed-rate-limited-and-account-bound-resources-are-spent-deliberately).
Do not translate one timeout into a claim that the source is unavailable
everywhere. Return the specific capability gap and its effect on the parent
claim. A lower-evidence substitute may enable a narrower result.

### Retain experience at the next decision point

For costly or recurring work, update the smallest useful note at an existing
owner, and put its permitted locator where matching future tasks begin. A note
buried only in a completion transcript does not establish reusable access.
If the owner or storage permission is missing, return the note and that limit
to the task owner; do not invent successful persistence.

A useful note can be a short paragraph or a section in an existing guide:

| Content | Purpose |
|---|---|
| Source identity and capability needed | Match future requests without confusing text, rendering, comments, or behavior |
| Applicable environment conditions | Know whether the method can transfer; keep sensitive details at their permitted owner |
| Verified steps or failed attempts and observed result | Execute the useful route or avoid an unchanged failure, rather than trust an untested recipe |
| Observation date and source version/date where relevant | Distinguish method freshness from information freshness |
| Limitations and revalidation conditions | Recognize misleading output or when a past failure warrants another attempt |
| Existing owner and retrieval location | Let the next context locate and update the experience |

Keep the active note concise and update superseded advice at that owner;
retain historical evidence only when useful for audit or recovery. Do not add
an incident log entry for every transient error. A general method can be public;
account, machine, and personal details keep their original audience boundary.
The template provides this method, not a universal storage backend.

### Return evidence and access limits

Return the material actually obtained, source identity and observation scope,
limitations, useful attempts and costs, and the locator or proposed destination
of reusable knowledge. Distinguish successful access, partial observation,
exhausted budget, and unsupported claims of absence. The research or task owner
integrates the findings; access success is not proof of the final conclusion.

## Verification

Inspect the retrieved material for the claimed property, not only a successful
tool status. To verify reuse, give a fresh task its normal permitted entrypoint
and the source need; observe whether it finds and applies the relevant method.
Also inspect how it handles a changed condition or an obsolete note. Record
actual attempts and available cost; missing timing or token data stays unknown.
One successful reuse establishes that occurrence, not a general time-saving
estimate or permanent source availability.

## Failure and recovery

| Symptom | Response |
|---|---|
| Successful extraction is missing relevant content | Check method capability; use an appropriate observation or preserve the gap |
| Prior method cannot be found in fresh context | Repair its permitted locator or handoff, not another duplicate memory file |
| Old instructions fail under changed conditions | Revalidate the route and update the active note with the new scope |
| Access succeeds but the data is stale | Seek the required version or date; report freshness separately from access |
| Another worker repeats exhausted attempts | Reconcile parent effort and attempt history before further work |
| No permitted route can provide the decisive evidence | Return the precise gap and recovery options through existing blocker routing |

## Safety and rollback

Task permission, privacy, and account boundaries apply to every fallback.
Access work does not authorize new subscriptions, credential sharing, external
writes, or changes to standing instructions. Retire incorrect advice at its
existing owner and revisit conclusions that relied on it. A generated recipe
without an observed result remains a candidate, not a verified method.

## Related authority

- [Capability-preserving fallback](../contracts/development-discipline.md#tool-failure-triggers-capability-preserving-fallback)
- [Evidence classes](../contracts/agent-execution-discipline.md#evidence-classes-remain-explicit)
- [Bounded delegation](../contracts/agent-execution-discipline.md#delegated-work-carries-bounded-context-and-returns-to-an-owner)
- [Personal-context boundary](../contracts/project-adoption.md#learning-and-personal-context-have-a-bounded-entry-path)
- [Document lifecycle](../README.md#document-stock-and-coupling)
