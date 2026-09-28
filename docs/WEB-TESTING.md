# Optional web browser testing with Playwright Test

Activate this module when a web project needs repeatable browser journeys, rendered screenshots, traces or browser CI. It is the recommended default for a **new** web project with those needs. An established project keeps a suitable runner when replacing it would add risk or duplicate coverage. A task with no browser behavior skips this module.

Playwright **Test** is a Node test runner with assertions, isolated browser contexts, projects, auto-waiting, traces, screenshots and HTML/JSON reports. It can run Chromium, Firefox and WebKit. Playwright **MCP** is a separate interactive tool and is not required here. Browser mobile emulation is a browser viewport/device simulation; it is not Android/iOS/native testing.

Official references checked 2026-09-27: [installation](https://playwright.dev/docs/intro), [configuration](https://playwright.dev/docs/test-configuration), [best practices](https://playwright.dev/docs/best-practices), [CI](https://playwright.dev/docs/ci), [screenshots and visual comparisons](https://playwright.dev/docs/test-snapshots), [trace viewer](https://playwright.dev/docs/trace-viewer). The current pilot used `@playwright/test` **1.63.0**, exact-pinned, on Node **22.23.1**, with Chromium behavior exercised through the installed Chrome executable because the Playwright browser download was unavailable. Recheck versions and supported Node/OS before a future project.

## Activation and installation

Adoption only copies the reference templates. It does not install npm packages, create a lockfile, download browsers or change an existing runner. The coordinator should:

1. Read the project profile, package-manager convention, existing tests and CI. Confirm that browser journeys are in scope.
2. Choose a reviewed exact `@playwright/test` version compatible with the project's supported Node version. Use the existing package manager and lockfile; do not create a competing lockfile or impose Node on an application that only needs another runtime.
3. Add the dependency in the project scope, then run the matching browser install. With npm and Chromium this is typically `npm install --save-dev --save-exact @playwright/test@<reviewed-version>` followed by `npx playwright install chromium`; CI Linux often uses `npx playwright install --with-deps chromium`. Record the actual version, browser revision, OS/runtime and commands in the project evidence.
4. Copy and adapt `templates/browser/playwright.config.mjs` and the representative `journey.spec.mjs`; do not copy their placeholder assertions as product proof. Configure the real `baseURL`, server command, routes, accessible names, fixtures and data reset.

Use the project's existing `package.json` scripts and lockfile. A reusable package may include templates, but its adoption helper must remain dependency-free and never run these commands implicitly.

## Configuration defaults

Start with one Chromium project and isolated contexts. Add Firefox or WebKit only when compatibility risk or acceptance criteria justify it, then run and record them; their presence in config is not test evidence. Keep retries at zero or a consciously bounded CI policy. A retry can expose flakiness but must not turn a persistent failure into success. Fail on focused tests and flaky results in CI. Use a bounded timeout and `fullyParallel` only when tests own independent data and the machine can support the workers.

Set `trace: 'retain-on-failure'`, `screenshot: 'only-on-failure'` and a useful HTML/JSON reporter. Keep reports, traces, videos and failure screenshots under ignored test-output paths or an explicitly reviewed CI artifact upload. Scrub credentials, tokens, customer data and secrets from URLs, test data, screenshots and reports. Do not commit generated output by default.

Keep the JSON report outside the HTML report directory: the HTML reporter may clean that directory. Ignore `test-results/`, `test-results.json` and `playwright-report/` in the target project. Review diagnostic retention; seven days is the CI template default, and local output may be replaced on the next run. Persist selected sanitized evidence separately when a checkpoint needs it.

Use an explicit loopback `webServer` command for a local app, with a bounded startup timeout and `reuseExistingServer: false` unless the project has a reviewed reason otherwise. A remote `BASE_URL` needs its own authorization, data isolation and environment contract; it is not implied by this module.

## Test design rules

- Prefer user-facing roles, accessible names, labels and stable test IDs owned by the product contract. Avoid CSS classes, generated IDs, DOM position and text that is incidental styling.
- Let Playwright auto-wait and use web-first assertions (`toBeVisible`, `toHaveText`, `toHaveURL`, `expect.poll`). Avoid arbitrary sleeps. Wait for an observable state or response that matters to the user.
- Give each test a fresh context and deterministic data. Reset through a supported API/fixture or a scoped storage/database setup. Do not depend on test order or a developer's browser profile.
- Assert behavior and outcomes: persistence after reload, validation, navigation, permissions, error recovery and data changes. An element existing is rarely enough.
- Isolate failure injection and mocks with clear names. Keep at least one production-like local path; a mocked API test does not prove the real integration.
- Capture screenshots for scoped running-app review and diagnostics. Keep them distinct from wireframes, polished design images and approved visual-regression baselines.
- Use `expect(page).toHaveScreenshot()` only after a stable environment and a reviewed baseline exist. A first generated baseline is not approved automatically. Review diffs; never use `--update-snapshots` just to silence a failure.
- Exercise keyboard and focus behavior where relevant. Narrow viewport checks are useful responsive web checks; they do not replace native-device or assistive-technology testing.

## Phase and checkpoint integration

During implementation increments, run the changed journey plus relevant unit/integration checks. Before release readiness, run the critical journey set across the selected browser projects and representative desktop/narrow viewports. A failed critical test, unresolved accessibility/permission/data-integrity issue or unexplained flaky result blocks dependent work. Record the exact source/config/package-lock/test files, browser/runtime, test counts and output paths in evidence; a later hash refresh cannot make old evidence current.

Parallel Playwright workers are test processes, not Codex subagents. Use them only for independent contexts/data and within machine resources. A coordinator still owns the shared contract, test data policy, state and integration gate.

## Debugging commands

Adapt the package manager and script names to the project:

```powershell
npx playwright test --project=chromium
npx playwright test tests/example.spec.mjs --headed
npx playwright test --debug --workers=1
npx playwright test --ui
npx playwright show-report
npx playwright show-trace path/to/trace.zip
```

Run one failing test first, inspect the trace/screenshot/console output, fix the cause, then rerun the affected scope. Keep a failure artifact and a short diagnosis in the checkpoint; do not claim a browser gate passed from a screenshot alone.

## CI template boundary

`templates/github/playwright-ci.yml` is a starting point, not an active workflow or a remote result. It assumes npm, a committed lockfile, `.nvmrc` with the selected Node version, a `test:e2e` package script and a project-local `playwright.config.*`; adapt the Node version, package-manager commands, web-server setup, permissions, artifact retention and browser projects. It installs only the selected Chromium browser, runs the project's named suite and uploads reports/available failure diagnostics unless cancelled. Keep it separate from this foundation's own CI and from pilot-specific selectors/assertions.

## Current pilot result and limits

The task-tracker pilot installed `@playwright/test` 1.63.0 locally and created a package lockfile. Its focused suite has 18 tests across Chromium desktop and narrow emulation: create/reload persistence, blank-title validation, edit/cancel, complete/reopen/filter, empty list, dialog focus/keyboard/confirm/cancel, failed write/retry, failed deletion recovery, discard/reload behavior and malformed storage protection. It passed using the locally installed Chrome executable. The Playwright-managed browser download timed out and was not silently replaced; Playwright MCP was not used. Firefox, WebKit, native devices, cross-machine CI for this module and remote CI are untested until explicitly run. Existing pilot `tests/browser.mjs` and direct Chrome driver remain and were not deleted; their coverage is separate historical/visual evidence.
