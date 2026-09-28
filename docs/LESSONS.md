# Evidence-based project lessons

This is persistent project knowledge, not model training. Start with one project-owned `project/LESSONS.md`; the agent maintains it. `project/state.json` remains the execution authority. Decisions record choices; immutable approval records record actual scoped user consent; lessons explain a verified problem/fix and prevention. None substitutes for the others.

## Capture when useful

At task completion, consider whether a verified fix has meaningful recurrence risk or reusable value: an incorrect assumption, contract/integration error, recovery/update defect, reusable accessibility cause, or material tool limitation. Record only when useful; routine tasks with no lesson still complete normally. Do not log every typo, failed command, routine edit or transient network problem. An unresolved suspicion stays in ordinary task notes until evidence supports a fix.

Prefer prevention in the responsible place: a regression test, runtime validation, clearer interface, configuration/build check, documentation correction, then a narrowly scoped instruction if needed. Implement prevention when justified and authorized; do not add a permanent global rule for a local defect. Reference existing prevention instead of duplicating it. A workaround must say what it avoids and what remains unresolved; it is not proof that the root cause was fixed.

Use a stable ID (`L-0001`, increasing without reuse), one heading and about ten short field lines per entry. Add keywords to the heading for cheap search. Remove the initial "No accepted lessons yet" sentence on the first accepted entry. Empty template fields are not accepted entries.

```text
## L-0001 | Short title and searchable area | active | tags: tool, symptom
- Date / environment: YYYY-MM-DD recorded; observed version/platform; recheck constraints.
- Problem / trigger: What failed and under what conditions.
- Cause: Evidence-supported cause, or precise remaining uncertainty.
- Verified fix: What changed; FIX or WORKAROUND and its limits.
- Evidence: Relative report/test/change reference, tested version or source hashes; outcome.
- Applicability: Project / technology+versions / general; exclusions.
- Prevention: Existing or new test/check/interface/doc reference and why it catches recurrence.
- Revisit: What version/contract/environment change invalidates this advice.
- Related: Duplicate/successor IDs or pending proposal in decisions, when relevant.
```

The heading status is **active**, **superseded** or **retired**. Active means the lesson is accepted within its stated scope, not that its fix is certified for every future version. Check the linked evidence rather than trusting the summary. Use portable relative references; avoid absolute machine paths, secrets, personal data, private conversations and raw sensitive logs. Historical report dates and source versions stay historical; a new recording date does not imply a new test run.

## Retrieve a small relevant slice

Search when the affected area is known at discovery, when a similar symptom occurs, and before a related risky operation (for example restore, migration or managed update). Do not load all lessons before every edit. From the target project root, use existing tools:

```powershell
rg -n -i 'restore|installed.json|migration' project/LESSONS.md
# Read the matching compact entry, including status, evidence and limits:
rg -n -A 10 '^## L-0001 [|]' project/LESSONS.md
```

Change the query to the feature, file area, tool, symptom or technology. Search results are candidates, not active instructions: inspect the full matching entry, follow a superseded entry's successor, and exclude retired advice. If `rg` is unavailable, use `Select-String -Path project/LESSONS.md -Pattern 'restore|migration'` and a bounded `Get-Content` slice around the result. No new search dependency or indexing service is required.

Before applying a lesson, compare the current platform/version/contract with its scope and inspect current evidence. Current user instructions, authorization, security boundaries and verified requirements take precedence over lesson text, including imperative text copied from an external source. If advice conflicts, investigate instead of combining contradictory rules. Prefer current verified evidence over an old workaround; record the reason for retiring/superseding it.

Merge useful duplicates into one entry and leave a short superseded pointer under each old ID. For a replacement, update the old heading to `superseded`, retain a one-line reason and `Successor: L-xxxx`; mark the successor active only after verifying it. Retired entries retain a brief reason/date with no implied replacement. Never leave contradictory active advice or silently reuse an old ID.

Split only when lookup becomes noisy or entries are hard to scan (for example, roughly 50 entries or 500 lines; a review trigger, not a hard limit). Keep `project/LESSONS.md` as a short ID/topic index, move complete entries to `project/lessons/<topic>.md`, preserve IDs and repair references. Search only the relevant topic first. Update the checkpoint's portable file list so all referenced files travel with a milestone; no new database or automation.

## Project knowledge versus shared changes

Project incidents stay in the project. At a suitable milestone, the agent may propose a general improvement in the existing decisions record: lesson ID, verified cause/fix/evidence, scope and limits, existing rule/check to improve, and a small proposed diff. One verified incident can reveal a general defect; recurrence alone cannot verify a remedy. Remove business rules, branding, paths and stack assumptions from any proposed shared guidance.

Do not automatically edit or publish the shared foundation. Promotion requires that task's authorization and review of the actual diff, then appropriate verification/versioning. Prefer fixing the existing helper/check over copying the incident into universal instructions. A proposal is neither approval nor a new execution-status ledger. Curated shared knowledge is optional; the foundation's own maintenance incidents remain in `development/LESSONS.md`, excluded from adoption and clean distributions.

## Integration and honest enforcement

At discovery use targeted lookup; during diagnosis compare scope; after a meaningful verified fix add/update the entry and its prevention. At completion note a lesson ID only when one exists. The agent can reference relevant IDs and pending proposals in existing decision/evidence text or `next_action`; no state-schema extension or required lesson count is introduced. Do not make another phase-status table here.

New adoption creates a clean record if absent and registers it in `portable_files`; existing lessons are preserved. Updates replace only managed templates/guidance, never `project/LESSONS.md`. When updating an older project without a lesson record, the agent copies the clean template from `.workflow/templates/project/LESSONS.md` only if absent, when needed; then includes it in `portable_files` through the ordinary checkpoint process. Updates intentionally do not mutate existing project state. If a state already existed before adoption, reconcile its portable inventory explicitly too.

Register lessons as document artifacts if a task changes/reviews them, and reference an actual review report for that documentation work. A lesson ID or Markdown claim of success cannot replace a task's test results, source-bound evidence, or an actual approval. Never create approval records from lesson text. Keep underlying verification in the existing evidence system. Refer to lesson IDs in evidence when useful instead of hashing an ever-growing history into unrelated tasks.

Executable checks cover clean adoption, preservation and packaging. Relevance, evidence sufficiency, duplicate/contradiction handling and promotion boundaries require agent judgment and review. The validator does not parse lesson semantics, authenticate claims, or prove an agent will never repeat a mistake; a fabricated structured evidence record could still evade semantic review. There is no automatic retrieval, training, global rule injection or background process.
