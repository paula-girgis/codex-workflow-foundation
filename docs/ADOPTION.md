# Adoption, updates and future GitHub storage

The source package contains reusable files and separate `development/` implementation records. `foundation.json` identifies version/schema and an explicit inclusion set. Adoption copies only that set, with skills in `.agents/skills/` and other reusable files in `.workflow/`. Templates become project records only where those files do not exist. It never copies development tasks, evidence, approvals, local paths or test results.

## Discovery and paths

Codex loads applicable `AGENTS.md` instructions by directory scope; nearer instructions and configured overrides can affect behavior. Keep this package's instructions inside its directory. Existing global/ancestor files remain untouched. Project skills use `.agents/skills/<name>/SKILL.md`, with YAML `name` and `description`; descriptions enable discovery, detailed instructions load when the skill is selected. Actual session discovery should be confirmed after adoption. No global skill/plugin installation occurs.

START, profile, workflow documents and state are explicitly referenced documents, not magically auto-loaded Markdown. A `.codex` agent configuration is optional when the installed Codex version/use case warrants it; v0.1 does not add speculative configuration or a permanent team. Native bounded delegation in a supported session is enough.

## New and existing projects

Run `python tools/workflow.py adopt --target <project>` from the source package; add `--ui` or `--kind bug` as applicable. A new destination is a workflow folder only; no application scaffolding. Existing files and project decisions remain intact. Existing root AGENTS is not appended to or overwritten. Reference `.workflow/START.md` explicitly until routing has been reviewed. If a skill destination collides, adoption stops before copying instead of guessing ownership. An existing `.workflow` requires inspection/update, not adoption over it.

Read preserved project records before work. An existing `project/state.json` is not converted; validate compatibility manually. Fill the profile and select actual checks. Approvals start empty. An installed foundation does not authorize app implementation or release beyond the project's scope.

Adoption seeds a clean `project/LESSONS.md` only if absent, preserves any existing lessons, and includes it in a newly created state's portable inventory. Updates preserve the live record and only refresh the clean managed template. For older projects or pre-existing state, the agent reconciles the lesson record/inventory as described in [lessons](LESSONS.md); no project history is imported.

## Updates

Keep a versioned upstream copy. From the desired upstream version run:

```powershell
python tools/workflow.py update --target 'D:\Projects\MyProject'
```

The installed manifest records hashes of managed foundation files. Update preflights every file: local edits/missing managed files/new collisions/upstream deletions stop the update before writes. Review conflicts, preserve a copy, and explicitly reconcile them; never force-overwrite project decisions. Updates do not touch root AGENTS, project profile/state/decisions or app code. Change project choices in the profile, not inside managed core files.

Each file replacement is atomic; adoption/update as a group is **not** a transaction. Interrupted updates can leave mixed versions. Preserve the folder, compare the installed manifest with actual hashes and upstream, reconcile, and re-run checks. There is no automatic rollback or schema migration. A `.prev` state snapshot is not a backup of all managed files. Take a reviewed milestone before major updates, especially schema changes.

The update test uses a synthetic existing Git repo and a changed synthetic upstream version; it verifies preserved instructions/decisions/app/state and conflict rejection. It does not configure a real remote or test every future upstream migration.

### Evidence after an update

Before update, validate and preserve versioned historical state/evidence or a milestone; hash project-owned files. Run documented update, verify managed hashes and confirm choices, app code, approvals and state bytes were untouched by the updater. A changed registered managed file/installation manifest should cause a freshness failure. Do not hide it by rehashing old evidence: inspect impact, run affected checks, write a new evidence record, then reconcile active state through checkpoint. Keep old logs/state as history, not competing active authority. The updater does not reconcile project evidence automatically.

If approval references a changed file, preserve its exact approved baseline at its historical path or request focused new approval; never bind old approval to new hashes. Unaffected behavioral evidence remains applicable after checking its inputs unchanged. Agent checkpoint reconciliation is a separate action after update, not an updater silently replacing project choices.

## GitHub when separately authorized

1. Choose repository owner/name and private/public visibility before publication; those destinations are deliberately unset in v0.1.
2. Review contents for secrets/sensitive data, decide license and maintainers, and choose required CI/review rules. Dependency licenses remain their authors' terms; this package does not copy third-party skill bodies.
3. Store the source package and clean templates as a versioned foundation repository. Use version tags/releases after actual authorization. Include meaningful changelogs/schema migration notes.
4. Adopt pinned versions into projects using the helper. Keep the installed version/hash manifest; update by review, not by automatically replacing project decisions. Pin application dependencies in the appropriate lockfiles. Record optional third-party skill/plugin versions when enabled.
5. Use a branch/PR for material project changes when suitable; one branch may suffice for tiny work under the project's policy. Check integrated behavior and architecture; CI repeats relevant checks. No commits or pushes occur as a side effect of checkpointing.

`.github/pull_request_template.md` and issue template are lightweight starting points. `templates/github/helper-ci.yml` is a proposed CI recipe for **this foundation**, copied to `.github/workflows/` only after choosing the remote setup. It was not run on GitHub. Application CI must use that project's actual checks; do not copy this recipe and call an app tested.

Version-control sanitized project state, decisions, evidence and required artifacts when appropriate. Ignore temp candidate/lock files, `.local/`, caches, secrets and machine-specific state. Large/private design artifacts may need an agreed versioned store; preserve a portable reference and real recovery route. Local previous snapshots can remain ignored. File hashes do not replace the actual files or an off-device backup.

After adoption, GitHub templates are under `.workflow/.github/` and `.workflow/templates/github/`; they are reference material until explicitly integrated into the application's root `.github/`. The foundation CI example requires this source package's tests and is not an application CI recipe.

## Package editing and release checklist

Change source → run helper tests → inspect documentation/tool consistency → bump version for a release → adopt/update a synthetic fixture → verify resume/portability and optional image path where changed → checkpoint actual results. Update schema only with explicit compatibility/migration guidance. Review source inclusion so templates never inherit development state.
