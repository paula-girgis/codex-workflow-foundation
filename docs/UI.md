# Optional UI module

Enable this module only for UI work. A small nonvisual bug fix does not require a new design exercise. For existing UI, retain relevant approved baselines and review only the affected screens/states; record why unaffected stages remain applicable. Projects without a UI record that visual gates do not apply.

## Visual sequence and review gates

1. Define users, outcomes, journeys, constraints, accessibility needs, and acceptance criteria. Resolve risky feasibility questions early with limited technical checks.
2. Build the screen/state and interaction inventories below. Include the responsive layouts relevant to the product, not every possible width.
3. Produce **actual low-fidelity wireframe images** covering the agreed inventory. Save and display them with stable identifiers and versions. Obtain real user approval of the specific wireframe set before polishing it.
4. Produce **actual polished screen-design images** from the approved wireframes and agreed brand direction. Cover applicable states and responsive layouts consistently. Save, display, and obtain separate real user approval before production UI implementation.
5. Finalize interaction contracts, architecture, APIs, data expectations, tasks, and acceptance tests. Independent backend exploration can happen earlier; dependent implementation must honor the approved shared contracts.
6. Implement useful increments. Exercise real interactions in the appropriate runtime, capture application screenshots, compare relevant screens against the approved design, and correct meaningful discrepancies.

Design approval is a product decision, not a helper-generated result. Record the approver, actual message/reference, scope, artifact version/hashes, and limitations. Changed approved artifacts need a scoped re-review; do not carry approval to a new version silently. A synthetic technical fixture never supplies approval for a product.

Freeze reviewed sources, exported images and their manifest together. Do not edit an approved image to replace an embedded “not approved” label. Current approval belongs in authoritative state and its immutable user-message record; a review index only links them. Historical profiles/designs may describe earlier scope: label these snapshots and point to current authority instead of rewriting approved inputs. Material deltas need focused review of affected states before polishing; independent approved work can continue.

## Coverage inventories

Maintain these tables in the project's design artifacts. Combine rows that genuinely share presentation and behavior; identify the shared reference rather than exporting unnecessary duplicate images.

| Screen ID / route | Journey | Relevant layouts | States | Wireframe refs | Polished refs | Shared coverage / reason omitted |
|---|---|---|---|---|---|---|
| Example: items / `/items` | Find an item | Narrow, wide | Loading, empty, ready, error, permission denied | Versioned artifact IDs | Versioned artifact IDs | Shared error component reference if applicable |

Applicable states include loading, empty, error, success, validation, permission, disabled, focus, and selected states. Static images cannot prove keyboard order, animation, screen-reader behavior, or responsive interpolation; list these as implementation checks.

| Control ID / screen | Action / destination | Validation | Permissions | Success / failure state | Data / API dependency | Acceptance check |
|---|---|---|---|---|---|---|
| Example: save-item | Submit changes; stay on details | Required name | Can edit this item | Updated summary / inline error | Agreed update contract | Valid save persists; invalid/unauthorized save is rejected |

Inventory every button, link, form, menu, tab, dialog, and other control. Decorative elements must not imply an unavailable action. An unknown interaction remains an open decision, not an invented backend contract.

## Image production and honest evidence

The default reproducible route is a design-only HTML/CSS/SVG artifact rendered by an available browser renderer into PNG. A suitable local drawing/export helper can create simple wireframe fixtures. Confirm the renderer exists and works before promising images. ImageGen can generate bitmap concepts when available; a design tool can produce editable mockups and exports when configured. Neither is mandatory. Do not substitute prose for the required images.

Impeccable, when installed and selected, contributes frontend design guidance, critique, and implementation refinement. Do not treat it as the PNG renderer or assume it directly generates image files. Browser automation and screenshot tools must be available, configured where needed, and smoke-tested separately. An installed skill is not proof that its dependencies or account access work.

Recommended artifact naming convention (adapt to the project):

```text
artifacts/design/wireframes/v001/items-wide-ready.png
artifacts/design/wireframes/v001/items-narrow-empty.png
artifacts/design/polished/v001/items-wide-ready.png
artifacts/design/sources/...
artifacts/application-screenshots/<check-id>/...
```

Register exported images using the execution state's artifact/evidence format, with relative path, hash, role, screen/state coverage, and relevant source/version. Use the supported fields or an associated manifest; do not silently extend the state schema. Keep source files alongside images where practical. Present images inline using an absolute local file path or an available preview/gallery; retain relative paths in portable records. If export or display is unavailable, state the missing capability and leave the corresponding gate incomplete.

| Artifact | Establishes | Does not establish |
|---|---|---|
| Wireframe PNG | Proposed layout, hierarchy, navigation intent | Visual finish or working controls |
| Polished design PNG | Approved intended appearance and depicted states | A running application |
| Running-application screenshot | What one actual rendered state looked like | That the journey, API, permissions, or persistence works |
| Functional/integration results | Behavior exercised under recorded conditions | Complete visual quality or every possible behavior |

A fixture demonstrating image export, manifest registration, and preview is **technical pipeline evidence only**. It is not a wireframe or polished-design approval for a future product.

## Centralized design and branding

Use one logical source of truth in a small coherent set of files, with platform-native consumption. Keep semantic meaning stable while values vary by theme/brand. Avoid independently hard-coded repeated styling and brand information on each page.

| Layer | Owns | Typical change |
|---|---|---|
| Semantic design tokens | Background, surface, text, primary action, border, success, error; typography; spacing/sizing; radii/shadows; motion; relevant breakpoints and themes | Change a shared color or spacing value |
| Brand configuration/assets | Product name, shared organization details, logo paths and variants | Replace logo or product name |
| Shared components | Buttons, form controls, cards, dialogs, loading/empty/error patterns | Change common rendering, accessibility, or interaction behavior |
| Shared layouts | Navigation, header/footer, content shells, repeated page composition | Change placement shared by many screens |
| Page/feature code | Specific content, local state, feature-specific behavior | Add a particular screen's action or content |

Carry approved mockup values into tokens and shared components, then inspect representative implementation states against the images. Token coverage is not proof of visual parity. Use a platform's CSS custom properties, theme/context facilities, native asset catalogs, or equivalent mechanisms. A build may transform a canonical token source into platform outputs; mark generated files and edit/regenerate the source instead.

Declare runtime token/asset files as the source for future application edits. Immutable mockup copies are historical evidence, not competing live configuration. Demonstrate a central-edit change in an isolated copy across representative screens/shared placements; retain approved values and label alternate screenshots as technical fixtures. Do not add product features just to demonstrate reuse.

### Example: web color and logo edits

These snippets illustrate responsibilities, not required scaffold or framework:

```css
/* theme.css: authoritative semantic values */
:root {
  --color-primary-action: #2457d6;
  --color-on-primary-action: #ffffff;
}
/* Shared button styling consumes semantics. */
.button-primary {
  background: var(--color-primary-action);
  color: var(--color-on-primary-action);
}
```

```js
// brand.js: shared product metadata, using the chosen bundler's asset convention.
export const brand = {
  name: 'Example Product',
  logo: '/assets/brand/logo.svg',
  logoAlt: 'Example Product',
};
```

Change the primary token once and consumers update. Replace the configured logo asset or its reference once; shared headers/footers read that reference. Native apps use their native theme and asset mechanisms for the same responsibilities. Launcher icons, splash screens, email templates, external embeds, and generated assets can have separate platform/build requirements; document their authoritative sources and regeneration steps.

After global changes, inspect representative screens, narrow/wide layouts, themes, and disabled/focus/error states. Check contrast, readability, wrapping, touch targets, and layout. Confirm a shared component change did not break its interactions. Brand variants should select token/asset sets, without copying every page.
