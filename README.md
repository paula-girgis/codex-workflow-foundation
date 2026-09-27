# Codex Workflow Foundation

Reusable, adaptive development instructions and small local helpers. Start with [START.md](START.md) and the [copy-ready prompts](docs/STARTER-PROMPTS.md). No application framework, hosting provider or permanent agent team is required.

This private repository publishes the unchanged **v0.1.3 package**. README, Git byte-preservation settings, CI and the release integrity reference are repository infrastructure; they are not added to adopted projects or the original distribution. No open-source license has been selected.

## Use

Download the ZIP and adjacent checksum from the [v0.1.3 release](https://github.com/paula-girgis/codex-workflow-foundation/releases/tag/v0.1.3), or clone this repository with authorized account access. Open your target project folder in Codex, provide the foundation path and a brief, and ask the agent to follow START.md. Python 3.10+ is required; verification uses 3.14. Core helpers use the standard library.

From this source folder, after replacing the example target:

```powershell
python tools/workflow.py adopt --target '../my-project' --ui
python tools/workflow.py update --target '../existing-adopted-project'
```

Adoption preserves existing project instructions and choices; collisions stop for inspection. Use `--kind bug` instead of `--ui` for a small non-design fix. From an adopted project:

```powershell
python .workflow/tools/workflow.py resume
python .workflow/tools/workflow.py validate
```

The agent maintains state, evidence and checkpoints. UI work requires actual wireframe images and scoped approval, then polished images and a separate approval before implementation. Automatic discovery of the two local skills in a fresh Codex session remains unverified; use the check in the starter prompts.

## Verify a clean checkout

```powershell
python tests/run_acceptance.py
python tests/release_check.py
```

Tests generate isolated synthetic fixtures; they need no unpublished development records. Reports are generated under `development/evidence/`, and packaging output under `dist/`. An absent Pillow dependency skips the optional PNG test explicitly. Core CI installs no optional tools. Local historical image verification does not imply a remote image test ran.

CI checks source hashes against `.github/release/v0.1.3-manifest.json`, runs the helper suite, then exercises release extraction, links, adoption and update preservation. Its generated ZIP may differ in metadata/timestamps; it is not the published release payload. The release contains the original verified ZIP and its exact checksum.

## Maintainer boundaries

The publication allowlist is the release manifest's source files plus this README, `.gitattributes`, the minimal CI workflow and release integrity references. Stage explicit reviewed files; never upload local `development/`, `dist/` wholesale, checkpoints, user approvals, application/browser data, credentials or reference projects. Release assets are reviewed separately. Local private records are excluded through this checkout's `.git/info/exclude`; that local protection is not inherited by a clone. The existing `.gitignore` covers common caches and secret files but is not a publication allowlist.

The source ZIP's tool/publication documents retain their dated pre-publication observations. They are not live account status. This repository adds no cloud deployment, database setup, optional design/spec tools or public license. See [readiness limits](docs/READINESS.md).
