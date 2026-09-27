# Checkpoints and recovery

`project/state.json` is the sole active execution record in an adopted project. In the foundation source tree it is `development/state.json`. Profile, decisions and immutable approval evidence hold their own content; state references them. Do not create competing STATUS files. `.prev` is an old recovery snapshot, never a second authority. A candidate is unaccepted input.

## Record and save

After meaningful saved work, verification, a phase transition, before/after an external operation, or before a handoff, record:

- Current objective/scope and route, task statuses/owners/dependencies and next concrete action.
- Artifacts with portable paths, kind and SHA-256; relevant code, contracts, configuration, lockfiles and test fixtures must be included, whether committed or not.
- Completion evidence: file/hash, kind, command or review procedure, result and input artifact hashes. A log saying passed without meaningful checks still needs review.
- Actual scoped approvals, immutable decision files/hashes, artifact versions; blockers in next action/decision records and incomplete saved edits in `saved_unverified`.
- Delegated ownership and last persisted handoff; external operation identifier/description/status and a read-only check to determine outcome. Never include tokens or credentials.
- Git HEAD if applicable. Git changes are inspected live by resume; local absolute worktree paths/process IDs remain in ignored local notes, not the portable state.

Use standard SHA-256, e.g. `Get-FileHash -Algorithm SHA256 <file>` (lowercase the result in state), or `hashlib.sha256(path.read_bytes()).hexdigest()` in Python. The JSON schema is the state contract. The helper implements the subset of JSON Schema used here plus reference/freshness rules; it is not a general JSON Schema engine.

Prepare `project/state.candidate.json`, increment `revision` exactly once, then run:

```powershell
python .workflow/tools/workflow.py checkpoint --candidate project/state.candidate.json --expected-revision 3
```

Candidate validation happens before replacement. A single-writer lock and expected revision detect cooperative concurrent updates. Writes use a temporary file in the same directory, flush/fsync and atomic replacement. The previous accepted record is retained at `state.json.prev` before replacement. Old artifact hashes may be stale after subsequent edits; snapshots do not freeze code or certify current behavior. Filesystems, power loss, hardware and antivirus can still cause failure; this is risk reduction, not a transactional filesystem/backup guarantee.

Invalid candidates do not replace current/previous records. A malformed/unsupported current record requires explicit recovery; no automatic version relabeling or migration. An interrupted stale `.lock` needs confirmation that no writer is active before manual removal. Preserve suspicious records before choosing an older snapshot. Schema changes require backup, explicit reviewed migration and revalidation; v0.1 has no automatic schema migration.

Before preserving the previous snapshot, the helper checks its internal structural and semantic integrity independently of files changed/deleted since that record was accepted. A coherent replacement can therefore account for deliberately removed files. An internally corrupted record requires explicit preservation and recovery, rather than replacing the last usable snapshot. The helper checks candidate HEAD against live Git where available, but never commits on the user's behalf.

## Resume procedure

1. Read project instructions, START, profile, decisions and authoritative state. Missing state is a reason to inspect files and reconstruct a reviewed candidate, not invent completed work.
2. Run `python .workflow/tools/workflow.py resume`. Inspect filesystem and actual Git status, branch/worktree and relevant changed/untracked/ignored files. The helper reads HEAD/status and registered hashes; it does not read every file or prove branch correctness. Dirty Git status conservatively sets `git_requires_review` and withholds current completion claims even for intended edits. `recorded_complete_tasks` preserves previous claims for reconciliation. Do not commit merely to silence this flag: review changes and evidence. Identical Git status text does not certify identical file contents.
3. Reconcile records with actual artifacts/code and evidence. The helper conservatively withholds all completion claims if consistency/freshness fails or recorded HEAD differs. Review the affected dependency graph; narrow rechecks only when justified.
4. Inspect interrupted processes and external operations read-only using stored receipts/provider IDs. Unknown deployments, migrations or publications stay unknown until checked. No automatic replay or process restart occurs.
5. Separate recorded verified work, saved but unverified changes, and uncertain work. If files changed, update affected tasks and rerun relevant checks before replacing evidence; retain historical logs outside the active evidence set as needed.
6. Continue from the next safe action with usable runtime/access/quota. Repeat only checks required by changes, missing evidence or uncertainty. Checkpoint the reconciled result.

The helper cannot authenticate a claimed approval, prove screenshot coverage, infer semantic dependencies from arbitrary code, or detect omitted input files. Review scope and input selection. It inspects only registered artifact hashes; unregistered changes and the meaning of Git differences need review. A passing validator is not a functional test.

## Portability and backups

For an adopted project, bundle also includes `.workflow/installed.json` automatically when present. This ownership/version manifest is required to update the restored foundation safely. v0.1.1 fixes its omission exposed by the task-tracker pilot; no existing project choices are rewritten.

Same machine or another chat with the same files: read the persisted artifacts and reconcile. Another machine/disk loss: restore code (including needed untracked changes), design source/images/manifests, state, approval/evidence records, contracts, configuration/lockfiles and instructions from a real backup. Ignored local notes and chat history are insufficient.

`portable_files` is an explicit allowlist in state; the bundle helper also includes artifact/evidence/approval/handoff/saved-unverified references. List required application files and runtime manifests; it does not infer a complete application dependency tree. Adoption seeds reusable files and project profile, but later additions require review. Never include secrets, real sensitive test data or machine-specific config.

```powershell
python .workflow/tools/workflow.py bundle --output 'D:\Milestones\project-v001.zip'
python .workflow/tools/workflow.py restore --bundle 'D:\Milestones\project-v001.zip' --target 'D:\Restore\Project'
```

Use a new output name and empty restore directory. Bundle validates current state; restore verifies explicit manifest hashes and restored state before copying. Archives contain files, not Git history or credential/runtime installations. A hash manifest detects accidental corruption, not a maliciously replaced archive. Content secret scanning/encryption is not implemented; filename screening alone is insufficient. Review the allowlist and contents.

The local archive is not an off-device backup. Choose a destination/security/retention policy explicitly later. Git commits and pushes are separate actions under project authorization; checkpointing does neither. Include sanitized milestones/evidence in version control when suitable, exclude local locks/temp files, sensitive data and machine notes. Preserve required images and large artifacts in an agreed versioned store if unsuitable for Git.

Development checkpoints protect saved code/design/evidence, not application runtime data. Browser storage, native databases, uploaded objects and hosted databases need their own selected backup/export and restore process. Do not call a source ZIP a backup of these data. A clean reusable distribution also differs from a project milestone: it excludes live project state, approvals and test results.

Tie a controlled stop/resume drill to a specific milestone: save useful partial work, record it as unverified, stop a local process, inspect from a fresh process, resume and verify. After completion, replay the drill from its isolated milestone; never reintroduce fake unfinished work into live state just to satisfy an old test.

Guarantee: resume from the latest usable persisted state, identify recorded verified work, inspect/recover partial saved work where possible. No recovery of unsaved memory, exact interrupted instruction, automatic quota bypass/restart or guaranteed disk-loss recovery. The v0.1 stop/resume and milestone tests use a new local directory and fresh process; they are **local portability tests**, not another-machine or real power-cut certification.
