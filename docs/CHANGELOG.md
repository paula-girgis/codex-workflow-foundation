# Changelog

## 0.1.4 — clean-checkout publication fix

- Isolated synthetic fixture Git discovery from the parent source repository; clean-checkout testing exposed false checkpoint HEAD mismatches that did not occur before Git initialization.
- Added a regression for fixture checkpoint/resume isolation; explicit fixture Git repositories continue to exercise real Git behavior.
- Excluded private maintainer records and generated distribution output from source tracking. Test upstream copies also omit local runtime and distribution folders.
- Activated minimal pinned-action CI in the repository. Runtime helpers, state schema, approval gates and skill bodies are unchanged; v0.1.3 artifacts remain preserved.

## 0.1.3 — onboarding and publication preparation

- Clarified which folder opens in Codex, how the foundation path is supplied, and how existing instructions/skills are preserved.
- Added one complete reusable start prompt and a reviewable GitHub publication/CI/licensing plan.
- Updated the current-environment capability guidance: an earlier Figma identity check passed, but its integration is absent from the latest inventory and no design smoke test ran; mobile binaries are present locally but no native runtime is verified; GitHub/Cloudflare access remains unconfigured.

- Release-maintainer correction in 0.1.3: write evidence to the actual release version, preserving older release reports. Core runtime helpers/schema are unchanged. Pilot remains at 0.1.2.

## 0.1.2 — local consolidation

- Six starter prompts, setup inputs and exact fresh-session skill-discovery check.
- Immutable design baselines, scoped approvals, runtime editing ownership and affected-evidence reconciliation after updates.
- Tested capability limits and development checkpoints separated from application-data backup; pilot browser harness remains optional and project-local.
- Clean versioned local source distribution with manifest/checksum and extraction/adoption verification.
- No helper/schema change, mandatory stack, new dependency or optional installation.

## 0.1.1 — pilot adoption correction

- Milestone includes `.workflow/installed.json` for safe updates after restore; regression covers restore then update.
- Agent owns checkpoint/hash maintenance, not the user.

## 0.1.0 — initial local foundation

- Scoped instructions, architecture/phases/UI/recovery, clean templates and two skills.
- State/checkpoint/adoption/update/milestone helpers, isolated fixtures and optional PNG fixture.
- No publication, deployment, global setup or inherited project approvals.
