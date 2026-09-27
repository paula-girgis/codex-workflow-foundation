# Scoped workflow instructions

These instructions apply inside this package, or where a project's own instructions explicitly adopt them. Never modify parent instructions or sibling projects to activate this foundation.

- Read START.md, the applicable project profile, and the authoritative state before work. In this source package the state is `development/state.json`; in adopted projects it is `project/state.json`.
- Scale work using docs/WORKFLOW.md. Preserve sound existing conventions. Use docs/ARCHITECTURE.md as observable review criteria; do not scaffold unnecessary layers.
- For applicable UI work, use docs/UI.md: actual wireframe images and real scoped approval, then polished images and separate approval, before production UI. Never fabricate approval or treat fixture output as product acceptance.
- Verify increments continuously. Passing a state validator proves structural/freshness checks only. Record meaningful behavior, integration and review evidence against relevant files/contracts.
- Coordinator owns dependencies, shared contracts, state and integration. Delegate bounded independent work only when useful and supported, with explicit file ownership and returned evidence. One writer updates authoritative state.
- Checkpoint persisted files after meaningful work/checks/transitions using the helper. Treat interrupted work and unknown external outcomes as uncertain; inspect before replaying anything.
- Follow existing authorization. Do not infer deployment, publication, external messaging, installations or destructive changes from a documentation template.
- Keep secrets, machine-specific runtime data and sensitive content out of portable records. Keep template records clean; do not copy development/ to future projects.
- Communicate concise findings, evidence, limitations and the next action. Use the user's language; default here is simple Egyptian Arabic with technical names retained.

Detailed rules live in linked documents; this file does not technically enforce an execution scheduler.
