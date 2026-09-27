---
name: resume-project
description: Resume interrupted project work from a persisted workflow checkpoint. Use when continuing after context loss, a closed session, a restart, or an explicit request to resume a project using this foundation.
---

# Resume from persisted reality

Locate the project root and read its applicable AGENTS.md, `.workflow/START.md` (or START.md in the foundation source), profile and recovery protocol. Do not infer the root from a remembered absolute path.

1. Run the local helper: `python .workflow/tools/workflow.py resume` in an adopted project. In the foundation source use `python tools/workflow.py resume --state development/state.json`.
2. Read the authoritative state and referenced decisions/evidence. Inspect actual filesystem, Git status/HEAD/worktree and relevant changed/untracked files. State validity does not prove functional correctness.
3. Distinguish recorded verified work, saved unverified edits, stale evidence and unknown external outcomes. Never present the latter as complete. Inspect interrupted operations read-only before deciding whether retry is safe; do not automatically restart agents/processes.
4. Reconcile affected dependencies and necessary checks. Preserve valid evidence when its applicability is established; repeat checks only for changes or uncertainty. Do not manufacture approvals or carry them to changed artifacts.
5. Continue the next safe action within existing authorization. Save actual files and use the checkpoint helper after a meaningful increment. One coordinator writes state; delegated reports are inputs, not competing ledgers.

Missing/malformed/unsupported state: follow RECOVERY.md, preserve the original and inspect `.prev`; no automatic schema relabeling, destructive cleanup or claimed recovery of unsaved memory. An interrupted lock needs confirmation no writer remains before removal. A checkpoint cannot restore credentials, quota, running processes or lost disk contents without a real backup.

Report briefly: verified work, uncertainty/blockers, next action and any required user decision. Keep local machine details and secrets out of portable records.
