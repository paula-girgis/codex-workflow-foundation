---
name: visual-review
description: Prepare and inspect visual-review artifacts for a project using the optional UI workflow module. Use for wireframe or polished-design review, coverage of screen states, or comparing actual application screenshots with approved designs; skip projects without UI changes.
---

# Review actual images and their coverage

Read the project's UI module, profile and screen/state/interaction matrices. Confirm the image renderer and display capability exist before promising output. Do not install missing tooling without required authorization.

1. Identify artifact type: wireframe, polished mockup, running-app screenshot, or technical fixture. Never interchange these claims.
2. Inspect source/export, actual image files, dimensions, versioned names, manifest and state hashes. Display the actual images with absolute local paths in chat or a supported preview; portable records retain relative paths.
3. Check scoped screens, responsive layouts and applicable loading/empty/error/success/validation/permission/disabled/focus states. Map shared state coverage explicitly. Check consistent tokens, brand, components, hierarchy and readability; record discrepancies.
4. For wireframes request actual scoped user approval before polishing. For polished designs request a separate actual scoped approval before production UI. Preserve immutable approved versions and the user's source message; never generate an approval from a test result or silence.
5. During application verification, exercise real controls/journeys in the browser/native runtime and compare real screenshots to approved designs. A screenshot alone does not prove behavior, permissions or persistence. Record behavior tests separately.

Impeccable may provide design guidance if selected and available; it does not replace a PNG renderer. A synthetic export fixture demonstrates only the technical pipeline. If images, coverage, approvals or runtime behavior are missing, record the affected gate as incomplete and continue only independent authorized work.
