---
doc_type: guide
status: current
authority: guidance
---

# Research & Capability-Preserving Access

## 1. Multi-Pass Engineering Research

When investigating unfamiliar frameworks, architecture patterns, or open-ended
design trade-offs:

1. **Check primary sources first**: Prefer official documentation, specifications,
   actual repository source code, and reproducible experiments over secondary
   summaries.
2. **Cross-check from multiple angles**: Do not stop at the first plausible
   answer. Compare how mature real-world systems handle scale, failure modes,
   and maintenance cost, and use peer reasoning tools (such as sequential
   well-contextualized `Ask ChatGPT` queries when available, or targeted web and
   codebase searches) to challenge blind spots.
3. **Translate into plain trade-offs**: Present the owner with clear options
   stating what each pattern is, how it works, what problem it solves, and what
   cost it adds at the project's current `stage`.

## 2. Capability-Preserving Fallbacks

When an external tool, bridge, or command fails:

- Distinguish **transient or routing failures** (switch cleanly to an alternate
  local or search tool that provides equivalent evidence) from **hard permission
  or safety boundaries** (never bypass access controls, sandboxes, or CAPTCHAs;
  report the exact block and stop on the gated path while continuing unaffected
  work).
