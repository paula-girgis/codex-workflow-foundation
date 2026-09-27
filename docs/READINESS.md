# Readiness and reusable lessons — v0.1.2

This local foundation is not a mandatory application template. Historical evidence and machine details stay in development records, not portable templates.

| Category | Demonstrated | Not established |
|---|---|---|
| Isolated foundation/helper tests | Selection, state/reference/hash validation, missing approval/evidence rejection, checkpoint failures, synthetic unknown operations, adoption/update preservation/conflicts, local restore | Real approval identity, arbitrary application correctness, real power-cut/cloud recovery |
| Pilot workflow | Documented adoption; real scoped wireframe then polished approval; editable sources → PNGs → actual app screenshots; incremental tests/checkpoints; central editing and local stop/resume/restore | Every platform/project scale, new-session automatic skill discovery, parallel pilot implementation |
| Application only | 10 task/storage tests, 12 Chrome journey groups and 12 app screenshots | Universal persistence policy, database choice, mandatory stack or browser harness |
| Unverified | Guidance for native/mobile, optional tools, hosting, databases and GitHub | Installed SDKs, authenticated accounts, actual device/cross-browser testing, remote CI/deployment or external backup |

The pilot exposed one executable defect: adopted milestones omitted the managed-file installation manifest. v0.1.1 fixed inclusion and added a restore-then-update regression. v0.1.2 retains it; helper code and schema are unchanged. No scheduler or universal storage adapter was justified.

| Reusable lesson | Core source |
|---|---|
| Preserve choices and reconcile changed evidence after managed updates | [Adoption](ADOPTION.md) |
| Real scoped approval, exact versions, focused review for material changes | [Workflow](WORKFLOW.md) |
| Editable sources, image manifest, immutable reviewed baseline and runtime editing ownership | [UI](UI.md) |
| Small cohesive modules, existing conventions, no fixed layer count | [Architecture](ARCHITECTURE.md) |
| Shared token/asset/component changes demonstrated in representative states | [UI](UI.md) |
| Incremental behavior checks with relevant inputs; refresh only affected evidence | [Workflow](WORKFLOW.md) |
| Agent-owned state, partial saved work, development recovery separate from application-data backup | [Recovery](RECOVERY.md) |
| Availability/configuration/authentication/testing are different facts | [Toolchain](TOOLCHAIN.md) |

## Browser harness decision

The pilot's direct Chrome DevTools driver avoided installation in a bounded environment. Making it core would impose browser discovery, protocol compatibility, waits/actions, process cleanup, diagnostics and multi-browser maintenance on every project. Keep it in the pilot. Prefer an existing project test runner, an available supported browser tool for bounded checks, or a maintained library such as Playwright when repeatable CI/multiple engines justify setup. Verify actual compatibility then; adoption installs none of them.

## Local distribution

The versioned ZIP is an upstream source distribution: instructions, clean templates, skills, helpers, examples and maintainer tests. It excludes development history/evidence, project state, approvals, actual pilot code/branding, local runtimes and credentials. Per-file manifest hashes and adjacent archive SHA-256 support integrity checking, not signatures or origin authentication. Extract, read START.md, then adopt. Python 3.10+ is required (tested locally on 3.14.6); Pillow is optional for the simple PNG fixture. Codex access and project runtimes are separate.

This is not an off-device backup. Later publication needs owner/repository name, visibility, license, review/CI policy and account access. No remote destination is configured.
