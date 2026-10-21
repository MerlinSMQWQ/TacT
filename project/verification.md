# Verification for the TacT source repository

This supplements `core/verification.md` when working on the Kit and its initialization CLI. The core guidance about failures, evidence reuse, required checks, and truthful reporting remains applicable.

For an instruction migration, check that the intended files and local links resolve, the English-only runtime requirement is met, and reasons, conditions, counterexamples, and boundaries survive the move. Compare against the preserved baseline. Inspect the actual host input and file-reading path for the selected adoption mode, then use a real task judgment to check application. File counts and a reading self-report alone do not establish adoption.

For CLI changes, run the relevant initialization and update tests, especially preservation of existing guidance, conflict handling, repeat operations, and dry-run behavior. Update checks should cover migration from an older installation, edited project notes, invalid manifests, and recovery after an interrupted write. For packaging or bundled-content changes, build both the source distribution and wheel and exercise an installed package outside the source checkout. Verify that shared guidance is included while this repository's project-specific constraints are excluded.

CLI tests establish file behavior, not agent adoption. Keep the distinction between startup discovery, explicit file acquisition, and observed task behavior in the reported result.
