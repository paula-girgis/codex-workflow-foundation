# Tool inventory and capability boundaries

This is a selection guide, not an installation request. Capability labels are independent: **Available** means callable/binary present; **Installed** means local package/plugin files were observed (not necessarily callable); **Configured** means relevant settings exist; **Authenticated** means required account access is confirmed; **Smoke-tested** means a recorded end-to-end check passed; **Proposed** means a candidate only. Do not compress them into “installed and working.” Recheck changing versions, compatibility, prices and quotas when selecting a project stack.

## Components in plain Egyptian Arabic

| Component | معناه | تعليمات ولا قدرة تنفيذ؟ |
|---|---|---|
| Markdown | ملف نص منظم للقراءة والخطة | تعليمات/معلومات |
| AGENTS.md | تعليمات للمساعد في نطاق المجلد حسب discovery والقرب | تعليمات؛ مش security boundary |
| Skill / SKILL.md | خطوات متخصصة ووصف يساعد اختيارها، وممكن معها scripts | التعليمات وحدها لا تثبت توفر scripts/dependencies |
| Tool / CLI | برنامج أو وظيفة بتقرأ أو تنفذ فعلًا | قدرة تنفيذ؛ تحتاج runtime وصلاحيات |
| Plugin | حزمة ممكن تجمع skills/tools/integrations | التوفر والتفعيل والاتصال محتاجين تحقق |
| MCP server | واجهة بتعرّض أدوات/موارد للمساعد | مش بالضرورة backend التطبيق أو hosting |
| Agent / subagent | مساعد رئيسي أو مهمة فرعية محدودة | سياق تنفيذ؛ مش OS thread ولا chat دائم |
| Delegation | توزيع مهمة بمدخلات ومخرجات وملكية واضحة | تنسيق؛ مش إثبات إن الشغل خلص |
| Persistent Codex chat | محادثة منفصلة لها تاريخ ودورة حياة | مش مطلوب لكل subtask |
| Hosting / backend runtime | المكان اللي الموقع أو server code بيشتغل فيه | خدمة تشغيل منفصلة عن أدوات المساعد |
| Database | التخزين والاستعلام والمعاملات | خدمة/ملف حسب الاختيار؛ مش مجرد ملف تعليمات |

ذكر اسم أداة في Markdown مش تثبيت أو authentication، ومش بيخليها callable.

## Minimal setup and optional additions

| Component / stage | Choice and real role | Setup, accounts and costs | Known status for this package / alternatives |
|---|---|---|---|
| Python / local validation/recovery | Standard-library helpers; no framework | Python 3.10+ proposed minimum; local testing used Python 3.14.6. No pip dependency for core | Local helper tests recorded in development/evidence. No service account. Earlier Python versions/cross-platform behavior not certified |
| Codex / coordination, skills | Main assistant; bounded subagent only for independent work | Existing Codex access and applicable usage limits | Current session used supported bounded delegation. No external framework. A new project's availability must be checked |
| Git / changes | Inspect actual state; optional branches/reviews later | Existing Git; no remote needed for local checkpoint | Local inspection and synthetic initialized repo tested; no commits/push performed |
| Renderer / UI | Editable HTML/CSS/SVG rendered to PNG; drawing helper for simple fixtures | Inspect available renderer per project; local route needs no service account | Available/configured/smoke-tested in web pilot: installed Chrome exported wireframes, polished boards and actual app screenshots. Pillow fixture tested separately. Neither browser nor renderer is installed by adoption |
| Browser automation / web verification | Existing runner or supported browser tool; maintained library for repeatable CI where justified | Runtime/browser setup per project; local testing needs no account | Pilot-only direct Chrome driver passed 12 journey groups. Playwright was not installed/tested by this foundation. Driver is excluded from reusable defaults; see READINESS.md for maintenance tradeoff |
| Impeccable / frontend guidance | Design skills, critique and refinement; not a raster image renderer | Review upstream Codex install instructions and pin selected version before setup; no install in v0.1 | Optional; use when visual quality benefits. Built-in design review is minimal alternative |
| Spec Kit / larger feature workflow | Requirements, spec, plan, tasks and implementation workflow across frontend/backend | Its Specify CLI/templates and chosen agent integration need local setup/version selection; inspect generated files for conflicts | Optional for substantial scope/contracts. Does not supply user approval or functional proof; plain profile/tasks suffice for small work |
| Caveman / communication | Concise language preference | No dependency needed; user chose style as sufficient | Implemented as instructions, no named Caveman tool installed or assumed |
| Figma / editable design | Optional collaborative design source/export | Plugin/tool/account/file permissions and plan-dependent cost must be checked | Earlier in this effort a Figma identity check succeeded; its tools/skills disappeared from the latest session inventory. Current access must be rechecked. No design smoke test. HTML/SVG is available locally |
| ImageGen / bitmap assets | Optional generated bitmap concepts/assets | Availability, usage allowance and applicable account cost require checking | Callable capability is present in this session; not invoked/smoke-tested here. Does not replace deterministic UI implementation |
| Mobile runtime / native checks | Stack-native build/tests + Android emulator/device or iOS simulator/device | Selected SDKs/images/device; iOS tooling/signing needs suitable Apple environment; distribution account costs separate | Flutter/ADB binaries found; emulator/xcrun not found on PATH. Native build, device, simulator and signing untested; binary presence is not SDK compatibility |
| GitHub / storage, review, CI | Optional repository, PR templates, CI | Destination/visibility/access must be chosen; plan-dependent CI/storage costs | No GitHub connector is callable in the latest inventory; gh not found on PATH; destination access/authentication unverified. Templates prepared; no remote, commit, push or CI execution |
| Cloudflare / release | Optional Workers/static assets/Pages + required storage/services | Account, scoped credentials, project-local CLI/config, compatibility and current pricing review | Existing plugin presence is not authentication or deployment verification. No service configured here |

Choose only what's needed: core Python + existing Codex + local files, Git when already used. Add a renderer for UI; actual browser/native tests for target behavior; Spec Kit for complex spec/task coordination; Impeccable for frontend critique; provider/DB tools only after architecture selection. No optional inventory is installed by adoption.

## Current capability snapshot (2026-09-27)

This is an inspection of this session/machine, not a guarantee for another project. `Unknown` means not established; `N/A` means no separate account is needed. The inventory changed during this effort: earlier Figma access is historical, not current availability. No optional installation occurred.

| Capability | Available / Installed | Configured | Authenticated | Smoke-tested / next action |
|---|---|---|---|---|
| Core Python, Git, helpers | Yes; local binaries/files | Local package | N/A | Helper/release evidence retained; ready for local adoption |
| resume-project / visual-review | Files installed in source/pilot; absent from session skill inventory | Correct local paths; limited frontmatter checks | N/A | Explicitly read; automatic discovery and native invocation pending fresh-session test in STARTER-PROMPTS.md |
| Impeccable | No detected skill or CLI; proposed | No project setup | N/A for local guidance | Not tested; optional next UI project |
| Spec Kit | No detected skill/Specify CLI; uv absent on PATH | No project setup | N/A for local toolkit | Not tested; optional complex requirements/contracts |
| Caveman style | Instruction policy applied | Yes | N/A | No package needed |
| PNG rendering | Chrome installed, editable sources and exporter available | Pilot | N/A | Wireframes, polished boards and app screenshots tested in pilot |
| ImageGen | Tool callable; local install N/A | Session tool | No generation call made | Untested; optional bitmap assets |
| Browser testing | Chrome/Node local; supported browser control callable | Pilot-specific driver | N/A for local app | 12 pilot journey groups retained; no portable cross-browser certification |
| Figma | Not callable/listed in latest inventory; earlier tool/skill present | Current integration unknown | Earlier identity-only check passed | No design/export test; recheck connection only if selected |
| Subagents | Native delegation tools available | Per bounded task | Uses current Codex access | Historical bounded handoff tested; no new delegation in onboarding |
| GitHub | No current connector; gh absent on PATH; Git present | No repository/remote here | Unknown | No remote/CI test; decide destination before authorized setup |
| Cloudflare | Plugin skills/MCP available; Wrangler command found | No project service config | Unknown; no account request made | No deployment test; choose only after architecture |
| Databases | Python sqlite3 import works (SQLite 3.50.4); sqlite3 command found; psql absent on PATH | No application DB/server selected | N/A local SQLite; remote unknown | Import is not DB integration/backup testing; select per workload |
| Mobile/native | Flutter/ADB binaries found; emulator/xcrun absent on PATH | SDK/device compatibility unverified | Signing/store access unknown | No native build/device test; inspect selected SDK before choosing stack |

### Optional installation recipes — not executed

Default recommendation: use existing Codex + Python and the local foundation. For UI, reuse the available renderer/browser and add **Impeccable only when design critique/refinement is useful**. For a larger specification, add **Spec Kit only when its spec/plan/task artifacts reduce coordination effort**. Keep Figma, AI image generation, cloud/database and native tools optional. No new paid account is required for the local core; Codex usage and optional services have their own allowances/costs.

Sources below were opened on 2026-09-27. Resolve a reviewed immutable release/tag and record its digest before a future install; never silently track latest. These are installation proposals, not authorization.

- **Impeccable:** [original repository and installation](https://github.com/pbakaus/impeccable). Upstream supports `npx impeccable install --providers=codex --scope=project`. Before execution replace the unpinned package selection with a reviewed release; Node/npm is needed for this route. It installs project skills and hooks; review hook trust separately. Its launcher can download an engine into a user cache, so project scope does not mean zero writes outside the repo. Local deterministic checks need no API key; AI usage is separate. Use its guidance alongside this foundation's approval gates, never as automatic design acceptance. It is not an image-generation service.
- **Spec Kit:** [official installation](https://github.github.io/spec-kit/installation.html), [Codex integration](https://github.github.io/spec-kit/reference/integrations.html). Requires Python 3.11+ and uv for the recommended route; uv is currently missing. Published pinned recipe: `uv tool install specify-cli --from git+https://github.com/github/spec-kit.git@vX.Y.Z` (replace placeholder with reviewed release). This is a user-level isolated CLI install, not project-only. Initialization uses `--integration codex`, creating `.agents/skills`; invocation is `$speckit-<command>`. Inspect generated-file conflicts in a scratch copy before adopting into an existing repo; do not use force blindly. No toolkit service account required; agent usage is separate. Its specs/plans/tasks overlap our profile and task records: link them rather than duplicate truth. Keep final implementation planning after visual approval, with feasibility checks earlier.

## Hosting and database selection framework

Cloudflare is a preferred candidate, not a default architecture. Static assets/Pages suit compatible static frontends. Workers suit compatible request/backend workloads. D1 is managed SQLite-derived access through bindings/API, R2 is object storage, KV is appropriate key/value data subject to its consistency model, Durable Objects can coordinate state, Queues/Workflows can handle suitable asynchronous work. Hyperdrive connects compatible Workers workloads to existing databases; it is not itself PostgreSQL storage. Verify current framework adapters, runtime APIs, limits, jobs and pricing before selection. Do not assume Node compatibility means every server library/process/filesystem feature works.

| Question | Local SQLite | Cloudflare D1 | PostgreSQL |
|---|---|---|---|
| Where data runs | File on a runtime with durable, appropriate filesystem | Cloudflare-managed service accessed with its own API/bindings | Server/managed DB separate from application runtime |
| Main fit | Embedded/local apps, modest write contention, single suitable host | Compatible Cloudflare workloads within current database/query limits | Rich queries/transactions, concurrent writers and growing relational needs |
| Write/transaction decision | Writes serialize; test contention and transaction design | Verify current D1 batching/transaction semantics; not arbitrary local SQLite connection behavior | Strong transaction/concurrency features; design pool/connection limits |
| Persistence constraint | Ephemeral/serverless filesystem cannot be assumed durable | No application-controlled database file/mount | Requires network access or a colocated database service |
| Operations/cost | Low service overhead; host/storage/backup responsibility remains | Provider-managed operations and usage/plan limits | Managed plan cost or self-host operations, backups/monitoring/upgrades |
| Migrations/restore | Version migrations; use consistent SQLite backup method and restore test | Version migrations; verify current export/restore/Time Travel capabilities | Version migrations; compatible dump/PITR/restore procedure depends on provider |
| Portability | File/data portable, deployment storage assumptions may not be | SQL overlap helps; binding/API/features and restore procedures differ | Broad hosting choice; extensions/provider specifics can constrain portability |

Record workload/scale estimates, competing writes, transaction/query needs, data residency, backup/restore objectives and cost constraints in the profile. Verify with a representative migration/restore/integration test when setting up. Prefer another host for required long-lived processes, native modules, unsupported framework features or durable local filesystem semantics that do not fit the selected service. Mobile backend hosting is separate from store distribution/signing.

The bundled skill-format validator requires PyYAML, absent from the Python runtime used here. No installation was performed. The two simple skill frontmatters received a limited manual/standard-library check against the validator's format requirements. Runtime skill discovery/invocation in a newly adopted Codex session remains untested. The optional PNG test uses the already-available Pillow; when absent it is explicitly skipped, so an installation without Pillow must not claim image export was tested.

## References retained from design research

Original/official sources to consult when enabling a capability; these links are not a claim that every current capability or price was retested during implementation (baseline research date: 2026-09-27):

- [Codex AGENTS.md](https://developers.openai.com/codex/guides/agents-md), [skills](https://developers.openai.com/codex/skills), [MCP](https://developers.openai.com/codex/mcp), [multi-agents](https://developers.openai.com/codex/multi-agent).
- [Impeccable original repository](https://github.com/pbakaus/impeccable), [Spec Kit original repository](https://github.com/github/spec-kit).
- [Playwright screenshots](https://playwright.dev/docs/screenshots), [visual comparisons](https://playwright.dev/docs/test-snapshots), [Flutter testing](https://docs.flutter.dev/testing/overview).
- [Cloudflare developer docs](https://developers.cloudflare.com/), [D1](https://developers.cloudflare.com/d1/), [Workers runtime](https://developers.cloudflare.com/workers/runtime-apis/), [Hyperdrive](https://developers.cloudflare.com/hyperdrive/).
- [SQLite appropriate uses](https://www.sqlite.org/whentouse.html), [PostgreSQL concurrency](https://www.postgresql.org/docs/current/mvcc.html), [GitHub Actions](https://docs.github.com/en/actions).

No live pricing is frozen into this foundation. Local core helper use has no new service charge; existing Codex usage, optional API generation, CI, hosting, database, storage and distribution plans remain separate costs to approve when chosen.
