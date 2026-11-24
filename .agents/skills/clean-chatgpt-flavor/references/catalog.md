# Clean ChatGPT Flavor: Symptom Catalog, Rewrites & Inventory Format

Concrete examples of overly defensive ChatGPT patterns across prose, code, tests, external/LLM payloads, and pipelines — plus the Phase A code-inventory report format.

## 1. Anxious Prose, Stacked Disclaimers & Self-Justifying Paperwork *(Default edit target)*

### Smell A: Stacked Disclaimers & Raw Hashes on Human Surfaces
- Showing raw 64-character SHA-256 digests on reader-facing cards (`Body SHA-256 e3b0c442... · v1.3`).
- Printing stacked legalistic disclaimers in UI dialogs, CLI output, or generated PNG/PDF chart footnotes:
  > "Full-text score is an uncalibrated heuristic signal; coverage is not actual share. This run provides no accuracy ground truth, does not reconstruct edit history, and does not reconstruct historical status. Length does not represent quality."
- Linking self-justifying process logs (old compliance checklists, rejection memos, verbose verification transcripts) from live docs or UI dialogs.

### Smell B: Defensive Tone Contagion in Docs, Skills & Memory Files
> "This summary is built from local heuristic slicing and is not an exhaustive profile. A repeated keyword does not by itself establish a stable preference, cannot prove long-term intent, and is not a substitute for direct confirmation."

Reading paragraphs like this primes future AI sessions to hedge every response.

### Smell C: Over-Correction (Hollowing Out Real Discipline)
Replacing a bloated defensive rulebook with 15 lines of empty slogans ("keep code clean, run tests, write plain prose") — discarding real ownership boundaries, red lines, and concrete operational checks.

### Clean Replacement
- State what was computed, its source/cutoff, and any scope rule positively in one or two factual sentences:
  > "Model v1.3 (cutoff 2026-11-16). Full-text score and segment coverage are computed separately; inspect highlighted segments in the source view."
  > "Body length excludes whitespace and titles."
  > "Use this profile to align quickly on background, working style, and known friction points. Mark uncertain observations as open to confirmation, and update this file when priorities shift."
- Remove raw digests and self-justifying process paperwork from live user-facing surfaces; keep living guides, concrete boundaries, and actual domain outputs.
- Cut stacked negative hedges (`"is not ... rather ..."`, `"cannot prove ..."`, `"does not automatically mean ..."`, `"不是…而是…"`, `"不能证明…"`, `"并不等于…"`) and filler openers (`"It is worth noting that..."`) while keeping real operational rules intact.

---

## 2. Unnecessary Hashing & Verification Theater *(Inventory first)*

Normal codebases rarely compute hashes outside version control, auth/signing, content-addressed storage, or explicit artifact freezes.

### Smell
- Locking editable source/UI/asset files to stored hash baselines in unit tests so every normal edit breaks CI until the hash JSON is hand-edited:

```python
def test_assets_match_baseline(self):
    baseline = json.loads((ROOT / "docs/baseline.json").read_text())
    for name, digest in baseline.items():
        self.assertEqual(hashlib.sha256((ROOT / name).read_bytes()).hexdigest(), digest)
```

- Hashing scripts, configs, or local assets into manifests (`program_sha256`, `asset_sha256`, `sourceHashes`), or adding standalone `verify_*.py` scripts that re-open inputs and unzip fresh archives just to recompute SHA-256 digests:

```json
{
  "preprocessor": { "scripts": { "prepare.py": "a94a8fe5ccb19ba6..." } },
  "checks": { "artifact_checksums": true, "source_files_unchanged": true },
  "limits": [
    "Checks establish data preservation and view consistency, not verified authorship or preference interpretation"
  ]
}
```

- Refusing `--overwrite` or `--resume` unless every old file and source script still matches a stored digest.
- Deleting a backend audit hash without checking frontend callers (`?v=` cache tags like `data.input_sha256.slice(0, 12)`), causing silent runtime crashes despite green backend tests.

### Clean Replacement *(After Phase A inventory approval)*
- Delete baseline hash tests, script/asset self-hashing, and unasked forensic replay scripts.
- Before deleting any hash key, grep across all languages and layers; if a caller used it as a cache-buster, replace it with a simple version or timestamp token (`data.cutoff || data.version`) and verify the real loader.
- Keep functional guards instead: behavior/contract tests on domain logic and loaders, in-memory pagination/JSON validation (no raw API-page disk dumps), and straightforward `--overwrite` / `--resume` behavior.

---

## 3. CYA Schema Fields & Polluted External/LLM Payloads *(Inventory first)*

### Smell
Baking defensive natural-language caveats, processed audit wrappers, and unused hashes into machine-readable schemas — and forwarding them into external APIs or LLM prompts:

```json
{
  "id": "input-9f2a...",
  "classification": "user_candidate",
  "classification_review": "heuristic_not_individually_verified",
  "text_sha256": "e3b0c442...",
  "provenance": { "input_sha256": { "records.jsonl": "9f86d0..." } },
  "limits": [
    "Counts describe public contributions, not actual usage or installs.",
    "The decomposition is an accounting identity, not causal attribution."
  ]
}
```

Sending natural-language caveats and audit wrappers into an LLM call wastes tokens and primes the downstream model to imitate the anxious tone even when its system prompt requests plain prose.

### Clean Replacement *(After Phase A inventory approval)*
Pass only clean, minimal domain data across external and LLM boundaries:

```json
{
  "id": "input-9f2a...",
  "classification": "user_candidate",
  "analysis_eligible": true,
  "project_ref": "proj-1",
  "text": "..."
}
```

Add a small unit test on payload builders to confirm internal metadata and defensive caveats do not leak into external or LLM calls.

---

## 4. Defensive Multi-Stage Pipeline Rituals *(Inventory first)*

### Smell
Forcing a multi-stage `export -> prepare -> verify -> query` workflow with intermediate hash manifests and staging directories when direct reading or querying solves the task:

```sh
python3 scripts/export_inputs.py --output work/batch-1/raw
python3 scripts/prepare_inputs.py --raw-dir work/batch-1/raw --output work/batch-1/prepared
python3 scripts/verify_inputs.py --archive work/batch-1/prepared --manifest work/batch-1/hashes.json
python3 scripts/query_inputs.py --prepared work/batch-1/prepared
```

### Clean Replacement *(After Phase A inventory approval)*
- Collapse redundant verification and staging steps so the primary entrypoint reads the input directly and validates structure in memory.
- Keep optional format adapters separate from the core path instead of baking extra staging steps into every run.

---

## 5. Sample Code-Inventory Report (Phase A Output)

On a default pass, finish text/doc cleanup first, then hand the owner a concise code inventory like this before editing code, schemas, or tests:

```markdown
### Cleaned Directly (Text & Docs)
- `README.md`, `docs/guide.md`: removed 9 stacked disclaimer clauses and 1 obsolete verification-log section; kept factual scope and filter rules.

### Defensive Code & Schema Inventory (Not Modified Yet)

| Surface | Count | Locations | Cross-Boundary Consumers / Risk | Recommendation |
|---|---:|---|---|---|
| Unnecessary hashing | 3 | `scripts/build.py` (`program_sha256`), `scripts/verify_pack.py`, `tests/test_hashes.py` | `web/app.js:42` reads `meta.input_sha256` for `?v=` cache tag | Remove hash baseline & `verify_pack.py`; swap `web/app.js:42` to `meta.version` |
| CYA schema / LLM payload | 2 | `src/llm/prompt.py` (`limits`, `classification_review`), `src/export.py` (`provenance`) | `tests/test_export.py` asserts `limits` key exists | Strip from LLM payload & export schema; update test to assert clean payload |
| UI / chart disclaimers in code | 2 | `web/components/Card.tsx:88`, `charts/render.py:134` | User-facing strings inside code | Rewrite to 1-line factual metric definitions |

### Kept (Genuine Domain Need)
- `src/auth/tokens.py`: HMAC-SHA256 webhook signature check (real auth boundary).

Reply with which code items to govern in Phase B (all, selected rows, or none).
```

---

## 6. Genuine Boundaries (Do Not Strip)

Do not classify real engineering requirements as "ChatGPT flavor":
- **Explicit cryptographic or freeze boundaries**: Auth/webhook signing, package/release checksums, content-addressed storage, owner-requested artifact freezes, or active runtime contracts that genuinely depend on a digest.
- **Data-loss and privacy boundaries**: Blocking path traversal (`../`), stripping secrets or PII before public exports or LLM calls, confirming paid or destructive actions, and refusing to silently overwrite user-authored files.
- **Correctness and provenance facts**: Validating required inputs, checking pagination totals, verifying local links and `#heading` anchors, stating source/filter scope factually, and testing real execution paths.
