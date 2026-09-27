# Decisions and approval index

No product/design/release approval exists in this template.

For each material decision record: ID, date, problem, options, choice, reasons, tradeoffs, revisit conditions and affected tasks/contracts.

For an actual user approval, save a separate immutable record under `project/approvals/` with ID, source message/date, exact scope, approved artifact versions and SHA-256 values, exclusions and decision. Register that record and its hash in state. Do not infer approval from silence, a generated mockup, a passing test or an agent's claim.

Do not append to an already hashed approval file; create a new version and supersede the old record. Keep unrelated future decisions here so they do not invalidate immutable approval provenance.
