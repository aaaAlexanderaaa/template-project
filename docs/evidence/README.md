# Durable evidence

Store small, reproducible evidence that supports a contract or completed plan:

- structured probe output;
- test or migration summaries;
- compatibility matrices;
- benchmark metadata;
- audit notes with exact source references;
- hashes or manifests for external artifacts.

Evidence must name the subject, environment, revision, reproduction command,
observed result, limitations, and the contract claim it supports.

Working screenshots, logs, and scratch dumps belong in `tmp/`. Promote only the
smallest durable representation needed to reproduce or audit the claim.
