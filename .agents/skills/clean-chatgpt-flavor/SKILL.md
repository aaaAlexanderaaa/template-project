---
name: clean-chatgpt-flavor
description: Counter overly defensive "ChatGPT flavor" in docs, copy, prompts, code, tests, schemas, LLM payloads, and pipelines. Defaults to cleaning anxious prose, stacked disclaimers, and self-justifying paperwork directly while inventorying defensive code, unasked SHA-256 verification theater, and CYA schema fields for owner review before modifying code. Also usable as an authoring or review checklist to avoid generating these habits.
---

# Clean ChatGPT Flavor

ChatGPT-style coding and writing often drifts into an overly defensive "forensic auditor / CYA lawyer" posture: stacked disclaimers in docs and UI copy, self-justifying compliance logs, unasked SHA-256 checks across ordinary scripts and tests, cover-your-ass metadata fields stuffed into JSON and LLM payloads, and multi-stage verification rituals nobody asked for.

This skill strips that residue out — or prevents it while authoring and reviewing — without weakening real safety or engineering discipline. It is completely self-contained and works in any repository or document set.

## Root Cause & Core Principle

Most ChatGPT defensive bloat comes from **treating internal trusted steps and ordinary readers as hostile auditors**.

- **Defend real boundaries**: Guard untrusted external input, path traversal, secrets/PII, destructive or paid operations, and explicit release freezes.
- **Stay direct inside**: Trust internal contracts, fail fast on real errors, pass clean domain data across boundaries, and explain scope in one positive factual sentence instead of stacking negative disclaimers about what something does *not* prove.

## Default Operating Mode: Clean Text First, Inventory Code First

Rewriting prose and refactoring code carry very different blast radius. Treat them as two separate steps unless the user explicitly asks to clean code in the same pass:

1. **Default — Clean text, docs, and copy directly**
   - Edit Markdown docs, READMEs, skills, memory files, prompt templates, and standalone user-facing copy to remove stacked disclaimers, defensive hedging, raw internal hashes, and self-justifying paperwork.
   - Ask before deleting whole historical documents if the owner might want to keep them archived.
2. **Code, schemas, tests, payloads, and pipelines — Inventory first, govern after confirmation**
   - Do **not** silently remove hash checks, alter JSON schemas, edit LLM payloads, or delete test gates by default.
   - Scan and report a structured inventory first: group findings by pattern, list exact file paths and counts, trace cross-boundary consumers (such as frontend cache tags or test assertions), and separate genuine domain requirements from defensive theater.
   - Execute code/schema cleanup only after the owner confirms the scope (or explicitly asks to clean code upfront).

## Four Signature ChatGPT Surfaces

### 1. Anxious Prose, Stacked Disclaimers & Self-Justifying Paperwork *(Default edit target)*
- Stacked legalistic hedges (`"does not by itself"`, `"is not proof"`, `"cannot establish"`, `"is not a substitute"`, `"不能证明"`, `"并不等于"`, `"不是…而是…"`) anywhere a human or future agent reads: docs, skills, memory files, CLI output, UI cards/modals, and generated chart/report footnotes.
- Defensive filler and generic truisms (`"It is worth noting that..."`, `"keep code clean"`, fake-balanced caveats when a direct factual sentence works).
- Raw 64-character digests or obsolete draft self-references leaked onto human-facing surfaces.
- Self-justifying process paperwork (compliance matrices, verbose verification logs, outdated failure memos) wired into live docs solely to prove an agent was careful. Future AI sessions imitate the tone they read — anxious docs produce timid, verbose agents.

### 2. Unnecessary Hashing & Verification Theater *(Inventory first)*
- **Baseline rule**: Normal codebases do not compute hashes during ordinary execution. Outside version control, auth/signing, content-addressed storage, or an explicit artifact freeze, treat runtime or test hashing as defensive theater by default.
- Typical residue: hashing scripts, configs, or local assets into manifests (`program_sha256`, `asset_sha256`, `sourceHashes`); tests locking editable source or UI files to stored hash baselines; standalone `verify_*.py` replay scripts; unzipping freshly written archives just to re-hash them; blocking `--overwrite`/`--resume` behind hash checks; dumping raw API pages to disk solely for byte-by-byte replay.

### 3. CYA Schema Fields & Polluted External/LLM Payloads *(Inventory first)*
- Cover-your-ass metadata fields baked into machine-readable records or manifests (`limits`, `interpretation`, `*_review`, `*_sha256`, caveat arrays no real consumer uses).
- Forwarding defensive natural language or internal audit wrappers across external boundaries — especially inside JSON payloads or tool outputs fed to downstream LLMs. Beyond wasting tokens, defensive wording in input payloads primes downstream models to hedge even when their system prompt forbids it.

### 4. Defensive Multi-Stage Pipeline Rituals *(Inventory first)*
- Splitting a straightforward read or query into a mandatory `export -> prepare -> verify -> query` pipeline with intermediate audit manifests solely to prove intermediate artifacts did not drift.
- Wrapping simple local commands in redundant staging folders or verification scripts when direct reading solves the task cleanly.

For concrete before/after rewrites and a sample code-inventory report, read [references/catalog.md](references/catalog.md).

## Keep Real Safety, Cut the Theater

Stripping defensive theater is not lowering quality. Keep genuine guardrails and concrete engineering discipline intact:

| Keep (Real Safety, Factuality & Discipline) | Cut (ChatGPT Defensive Theater) |
|---|---|
| Trust-boundary protection: blocking path traversal, stripping secrets/PII before export or LLM calls, confirming destructive or paid actions | Default hashing in ordinary runtime code, manifests, or editable-file tests; unasked `verify_*.py` replay scripts |
| Hashes with an explicit domain need (auth/signing, content-addressed storage, release checksums, or an active runtime contract like cache keys) | Hashing local scripts/configs for "auditability"; printing raw digests on UI cards; blocking `--overwrite`/`--resume` on old code hashes |
| Clean domain data plus one factual provenance/scope sentence when needed (source, cutoff, filter rule) | CYA schema fields (`limits`, `*_review`, unused `*_sha256`) and defensive caveats forwarded into external or LLM calls |
| Real integrity checks (valid JSON, pagination completeness, broken links and `#heading` anchors, surfacing anomalous inputs) | Dumping raw API pages to disk for byte replay; unzipping a new archive just to re-hash it |
| Living docs, concrete ownership boundaries, and actionable rules | Self-justifying compliance logs, stacked disclaimers, and bloated legalese rulebooks — or hollowing real rules into empty slogans |

## Execution Workflow

### Phase A: Text Cleanup + Code Inventory (Default)
1. **Clean text surfaces directly**: Rewrite anxious docs, skills, READMEs, prompt templates, and standalone copy into plain subject-verb-object sentences. State what an object is, how to run it, and any real scope rule positively in one sentence.
2. **Audit code surfaces without editing them**: Scan code, tests, schemas, prompt builders, UI templates, and scripts for Surfaces 2–4 (common anchors: `sha256`, `hashlib`, `digest`, `verify_`, `sourceHashes`, `limits`, `_review`, `provenance`, and disclaimer phrases inside UI/chart code).
3. **Trace cross-boundary consumers during inventory**: Note callers across all languages and layers (backend JSON, frontend `?v=` cache tags, CLI flags, tests) so the owner sees real blast radius before approving edits.
4. **Deliver the report**: Summarize (a) text files cleaned, (b) defensive code/schema/pipeline findings grouped by surface with counts, locations, and consumer risk, and (c) items recommended to keep for real domain needs; then ask which code items (if any) to govern in Phase B.

### Phase B: Code, Schema & Pipeline Governance (After Confirmation or Explicit Request)
1. **Replace reused tags before deleting fields**: If a removed hash also served as a cache-buster or lightweight version tag, swap in a simple version or timestamp token first.
2. **Cut cleanly without stubs**: Remove unasked hashing, forensic replay scripts, CYA fields, and redundant pipeline stages outright rather than leaving commented-out shells.
3. **Clean external and LLM call boundaries**: Strip defensive natural language and internal audit wrappers inside payload builders so only clean domain data crosses out.
4. **Verify real execution paths end-to-end**:
   - Update tests to verify real behavior, cross-boundary loaders, and clean payloads rather than file bytes.
   - Check local links and `#heading` anchors after deleting docs or renaming headings.
   - Run actual CLI commands, loaders, local servers, or rendered UI surfaces rather than relying on mocked unit tests alone.

## Quick Self-Check (Cleanup, Authoring, or Review)

1. Are user-facing docs, UI text, chart footnotes, and CLI messages direct and free of stacked disclaimers, raw hashes, and self-justifying paperwork?
2. On a default pass, did you leave code/schemas untouched and provide a concrete, consumer-traced inventory instead of silently refactoring code?
3. When code or schemas were modified, does every remaining hash have a genuine domain role, are LLM/external payloads free of defensive wrappers, and did real end-to-end execution paths pass?
