# Adaptable application structures

These are written examples, not scaffolded applications, selected stacks, or mandatory folders. Choose the platform and runtime in the project profile. Preserve sensible existing structure. Framework-required conventions differ from our recommendations: verify the selected framework/version before implementation.

## Small website

A small static or Vite-style website may need only:

```text
src/
  pages/                 # Recommended when there are several pages
  components/            # Shared navigation, buttons, footer
  styles/theme.css       # Semantic tokens
  brand.js               # Shared brand metadata
  main.js                # Example entry; stack-dependent
public/assets/brand/
tests/                   # Only meaningful checks for this site's behavior
```

Vite itself does not prescribe this feature structure. The selected build configuration determines actual entries and asset behavior. Page code composes shared controls and reads common tokens/brand configuration. A site without dynamic data needs no database, API, domain layer, or provider abstraction. Validate links, forms where present, relevant layouts and accessibility. Use the UI module's approvals for new screens.

## Full-stack CRUD or growing SaaS

An illustrative Next.js App Router project could use:

```text
src/
  app/                   # Framework routing conventions for this selected router
  features/
    items/               # Feature UI, use cases and related tests
    accounts/
  server/
    authorization/       # Trusted authorization rules
    data/                # Database access and transaction boundaries
    providers/           # External service adapters when needed
  ui/
    components/
    layouts/
    theme.css
  config/brand.ts
public/assets/brand/
db/migrations/
tests/integration/
tests/journeys/
```

The router's filenames and server/client conventions are framework-specific; `features`, `server`, `ui`, and their exact locations are recommendations. Respect the framework's server/client boundary. UI calls an agreed application/API contract; server logic validates input and permissions, applies rules, and performs persistence. Do not import database or secret-bearing modules into client code. Domain modules become useful when genuine business invariants outgrow simple CRUD.

Frontend and backend can run in parallel after the API schema, error shape, authentication assumptions, state examples and ownership are agreed. One owner controls that contract. A frontend mock is useful during implementation; acceptance still requires the real endpoint and persistence. Integrate a complete useful slice early, such as create → validate → persist → list, and verify failure/permission cases before advancing dependent tasks.

Select the database and hosting together. Local SQLite requires durable suitable filesystem storage; D1 is a Cloudflare-managed database API with its own limits; PostgreSQL brings different operational and concurrency characteristics. This example does not select any of them.

## Mobile/native app

An illustrative Flutter project might use:

```text
lib/
  app/                   # App composition, navigation and native theme wiring
  features/
    items/               # Screens, state/application behavior, related models
  shared/
    widgets/
    layouts/
    theme/
    brand/
  data/                  # API/persistence adapters when needed
assets/brand/
test/
integration_test/
android/                 # Platform-owned project; retain platform conventions
ios/                     # Platform-owned project; retain platform conventions
```

Flutter's platform projects and package/asset configuration are platform conventions; feature separation is an adaptable recommendation. Widgets consume shared themes and assets; application behavior depends on explicit data/provider boundaries. For SwiftUI, Kotlin/Compose, React Native or another platform, use native structure and mechanisms instead of copying these directory names.

Record which files are authored source and which are generated. Edit declared source/configuration and run the appropriate generator; do not hand-edit generated platform/assets outputs without an explicit documented reason. Keep legitimate platform-specific behaviors visible rather than forcing all platforms through a lowest-common-denominator abstraction.

A browser preview is insufficient evidence for native behavior. Test on available appropriate emulator/simulator/device targets, including navigation, permissions, keyboard, lifecycle and network failure where relevant. iOS build/simulator verification normally requires suitable Apple tooling; record unavailable target checks as pending. A mobile backend is a separate runtime choice from app-store distribution and signing. Neither is configured by these examples.

## Small change in an existing repository

For a narrow bug, inspect the closest instructions and conventions, reproduce the failure, identify affected code/contracts, make the smallest coherent change, and run the relevant regression checks. Keep the existing architecture. Do not trigger full product discovery, new screen inventories, or new branding for an unrelated logic fix.

A visually changed control may need a scoped visual review; a new UI journey needs the screen/state and separate wireframe/polished approval gates. A CLI, service, or data-processing project skips visual stages with a recorded reason and uses input/output, contract, integration and operational evidence instead.

See [architecture policy](../docs/ARCHITECTURE.md) for dependency and pattern decisions and [UI conventions](../docs/UI.md) for central editing responsibilities.
