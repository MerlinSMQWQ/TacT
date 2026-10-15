# Verification for the TacT documentation repository

This supplements `core/verification.md` when working on the Kit itself. It adjusts verification selection for the current documentation-only repository; the core guidance about failures, evidence reuse, required checks, and truthful reporting remains applicable.

For an instruction migration, check that the intended files and local links resolve, the English-only runtime requirement is met, and reasons, conditions, counterexamples, and boundaries survive the move. Compare against the preserved baseline. Inspect the actual host input and file-reading path for the selected adoption mode, then use a real task judgment to check application. File counts and a reading self-report alone do not establish adoption.

There is no application test suite in this first edition. Use focused document and adoption checks; introduce application builds or tests only when a later change creates a relevant behavior or contract to verify. Keep the distinction between startup discovery, explicit file acquisition, and observed task behavior in the reported result.
