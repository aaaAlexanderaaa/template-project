# Plans

Plans describe how one coherent change reaches its end state. They carry
`authority: planning` and never override current contracts.

Use `templates/implementation-plan.md`. A useful plan includes:

- authoritative contracts;
- current facts and baseline evidence;
- complete end state;
- dependency-ordered execution within that change;
- affected files or systems;
- risks, failure handling, migration and rollback;
- verification and completion evidence;
- explicit non-goals.

When finished, mark the plan `completed`; when replaced, mark it `superseded`
and link its successor.
