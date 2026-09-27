# Architecture and clean code

Use the smallest structure that keeps the project's current responsibilities clear. These are review criteria, not a framework mandate. The executable state validator checks records and detectable consistency; it cannot prove good architecture or working behavior.

## Responsibility and dependency rules

| Responsibility | Owns | Must not own |
|---|---|---|
| Presentation | Rendering, accessibility, local view state, user input | Secrets, authoritative authorization, database access from an untrusted client |
| Application/use case | Coordinating a user action and its outcome | UI markup or vendor-specific connection details |
| Domain rules, when meaningful | Business invariants and calculations | HTTP, widgets, framework lifecycle, storage drivers |
| Data/provider adapter | Persistence, external API translation, retry boundaries | Duplicated business rules or hidden product decisions |
| Composition/configuration | Constructing dependencies and validated settings | Implicit global mutable application state |

The usual direction is presentation → application rules → explicit data/provider interfaces. An adapter implements the boundary; the composition point supplies it. Small projects can use functions and modules without interfaces or extra directories. A simple static page needs no domain or data layer. Existing repositories retain coherent conventions unless a specific problem justifies change.

Validate input at the trusted boundary. Client validation helps users; server-side validation and authorization enforce access. Check authorization for each protected action/resource. Keep credentials out of browser bundles, logs, state records, fixtures, and repository files. Errors should be useful to callers without disclosing sensitive details.

## Review criteria

| Criterion | Evidence a reviewer can inspect |
|---|---|
| Clear names and cohesion | A module/function has an explainable responsibility; callers can understand its inputs and outputs. |
| Explicit dependencies | External effects and configuration enter through clear parameters, imports, or platform-supported dependency mechanisms. |
| Consistent business rules | A rule has one authoritative implementation; similar-looking code is not merged when behavior differs. |
| Predictable failures | Expected failures have clear outcomes; unexpected errors retain diagnostic context; errors are not silently swallowed. |
| Maintainable changes | A routine change touches the responsible module rather than unrelated screens or duplicated implementations. |
| Controlled complexity | Remove unnecessary branches, speculative extension points, unused code, and accidental abstractions. |
| Useful documentation | Explain non-obvious constraints, contracts and reasons; do not narrate obvious code. |
| Verifiable behavior | Checks target meaningful outcomes and failure cases, with appropriate build/type/lint checks where the stack supports them. |

Apply SOLID, DRY, KISS, and YAGNI as judgment aids. Do not enforce arbitrary line counts, an interface per class, or a mandatory layer for every function. Reversible copy edits need proportionate checks; authentication, data integrity, recovery helpers, and integration boundaries need stronger evidence.

## Choose patterns for an observed need

| Pattern | Useful trigger | Avoid when |
|---|---|---|
| Feature modules | Features have related UI, behavior and tests; cross-feature coupling needs control. | A handful of files already communicates the structure. |
| Modular monolith | A growing product needs boundaries while one deployment remains practical. | Used as a name for unrelated folders with unrestricted dependencies. |
| Provider adapter | An external API or database needs translation, substitution, or test isolation. | A wrapper only renames every vendor method without adding a useful boundary. |
| Dependency injection | A dependency has real alternatives or needs controlled effects in tests. | A container would be more complex than passing a function/object. |
| Repository | Domain-oriented access meaningfully differs from raw persistence operations. | It duplicates an ORM wholesale or hides required transactions. |
| Strategy | Multiple real policies vary behind the same contract. | Only one policy exists and no concrete variation is required. |
| State machine | Transitions, permissions and invalid states are difficult to reason about. | A boolean or a small explicit enum is sufficient. |
| Shared UI composition | Repeated controls and layouts have stable behavior and visual semantics. | Page-specific behavior would require a large prop matrix. |

Do not add microservices, event buses, CQRS, DDD layers, a custom design framework, or an agent framework by default. Record why a chosen pattern earns its complexity in the project decisions.

## Apply the policy to this foundation

Keep instruction documents separate from executable helpers, templates separate from the foundation's own development evidence, and project decisions separate from reusable rules. The coordinator owns state/schema contracts and integration. Helper interfaces should be small, errors actionable, dependencies explicit, and source of truth singular. Reviews check those qualities; helper tests check their actual observable behavior.

Use [application examples](../examples/APPLICATIONS.md) as adaptable guidance. [UI conventions](UI.md) define shared design responsibilities when a project has a UI.
