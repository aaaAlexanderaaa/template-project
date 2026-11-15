---
doc_type: contract
status: current
authority: normative
---

# Standing Autonomous Charter (`mode = "unattended"`)

Fill and obtain human owner sign-off before running unattended multi-wake loops:

- **Authorized objective & stop condition**: {{exact observable goal}}
- **Permitted write paths & external side effects**: {{allowed directories/APIs}}
- **Resource & quota ceiling**: {{max iterations, spend, or runtime}}
- **Independent review gate**: {{fresh-context verification required before closing milestones}}
- **Auto-dormancy & anti-self-edit rule**: Enter dormancy and notify the owner
  on repeated test/check failures, blocked human decisions, or completion of the
  authorized scope. Never modify this charter, line budgets, or
  `human_check = "approved"` fields during unattended runs.
