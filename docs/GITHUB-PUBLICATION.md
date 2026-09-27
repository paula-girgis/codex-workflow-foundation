# GitHub publication plan — prepared, not executed

This plan is for a later, separately authorized publication of the reusable foundation. Current inspection on 2026-09-27 found no `.git` repository or remote in `codex-workflow-foundation` or `workflow-pilot`. No GitHub connector was callable in this session, so account access, owner and destination availability remain unknown.

## Proposed repository contents

Track the reusable source only:

- `START.md`, `AGENTS.md`, `foundation.json` and `docs/`.
- `schema/`, `tools/`, `tests/` and clean `templates/`.
- `.agents/skills/` and lightweight `.github/` review/issue templates.
- `examples/`, `docs/CHANGELOG.md` and release-maintainer documentation.
- A generated `dist/` release asset only if the repository policy wants a checked-in checksum/manifest; prefer attaching the ZIP to a tagged GitHub Release instead of duplicating large binaries in every branch.

Keep out of the public source repository:

- `development/` checkpoints, handoffs, pilot evidence, historical state and local milestone archives.
- Adopted project `project/state.json`, approvals, app code, design exports, browser data and runtime screenshots.
- `.local/`, caches, lock/candidate files, machine paths, tokens, credentials, private test data and generated temporary files.
- Any private client material from Ekova or another reference project.

The repository may contain sanitized maintainer test fixtures, but synthetic approvals must stay clearly isolated and never become a project template default. Run secret scanning and license review before publication; path checks in the local release script are not a general secret scanner.

## Repository shape and release flow

1. Choose an owner, exact repository name, public/private visibility, license, maintainers and branch protection before creation.
2. Create a normal Git repository with `main` (or the chosen default), add the source package and a README that points to `START.md`.
3. Work on a branch and review a pull request for material foundation changes. A repository template is **optional**: it is useful only if new projects should start with the reusable files already copied. It must not clone pilot application code or development state. For most use, the versioned source ZIP plus `adopt` is safer and keeps projects independent.
4. Tag a version such as `v0.1.3`, publish the ZIP and checksum as release assets, and keep `foundation.json`/`docs/CHANGELOG.md` aligned. Consumers pin a release rather than silently tracking `main`.
5. A project updates from a reviewed source release with `python tools/workflow.py update --target ...`. The updater preflights conflicts, preserves project choices/application code/state, and leaves evidence reconciliation to the coordinator. Record the installed version/hash manifest.
6. A later foundation release changes `foundation.json` and changelog, runs helper/release checks, adopts into a synthetic project and tests an update of an existing synthetic repository before the tag.

## Proportionate CI proposal

On pull requests and pushes to the default branch, run the existing `python tests/run_acceptance.py` on the supported Python range selected by the repository (start with the tested version, then add another supported version only after compatibility checks). Run `python tests/release_check.py` when release packaging or inclusion changes. Upload test logs and the generated manifest as artifacts. Keep image rendering, browser/native checks and optional integrations in separate workflows or opt-in jobs; they need their own runtimes and should not make documentation-only PRs depend on a browser or mobile SDK.

Pin or review action versions under the repository policy. The existing `templates/github/helper-ci.yml` is a starting point, not proof of a GitHub run. Add dependency/security scanning and secret scanning after selecting the repository's policy and tools; do not invent a service or credential here.

## Licensing and unresolved publication choices

Before public distribution, choose a license compatible with the foundation's own files and any third-party references. A permissive MIT or Apache-2.0 license is a reasonable default for a reusable workflow, but the owner should choose after checking whether the package will contain contributor terms, trademarks, bundled assets or copied third-party text. The local package currently has no selected license file. Add `LICENSE`, contributor/security guidance and attribution notices before publishing.

The only decisions needed later are: owner, repository name, visibility, license, default branch/branch protection, maintainer/reviewer policy, whether to use GitHub Template Repository or release ZIP adoption, and whether to enable CI/security scanning. None is needed to use the local ZIP now.
