# Durable evidence

Store small, reproducible evidence that supports a contract or completed plan:

- structured probe output;
- test or migration summaries;
- compatibility matrices;
- benchmark metadata;
- audit notes with exact source references;
- hashes or manifests for supplied artifacts or obtainable external artifacts.

Evidence identifies the subject, environment, revision, observed result,
limitations, and supported claim. Reproducible checks include the required
materials and commands. A maintainer report about unavailable inputs is
labeled as such; a private path or an artifact hash alone does not let a reader
reproduce it. Explain relevant background in self-contained English.

Working screenshots, logs, and scratch dumps belong in `tmp/`. Promote only the
smallest durable representation needed to reproduce or audit the claim.
