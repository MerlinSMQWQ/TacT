# Verification and evidence

Use this before choosing verification scope, investigating a check failure, or resolving an evidence gap in a delivery claim. Skip rereading it when executing an already justified check and its scope remains applicable.

## Choose checks for the behavior and risk affected

Match the scope of verification to the impact and risk of the current change and the current delivery stage. By default, select relevant tests, builds, and checks based on the behavior changed and the affected interfaces and callers. Do not treat every check available in the repository as an obligation for every task. Broaden verification when shared mechanisms, cross-module behavior, significant risks, or insufficient evidence warrant it, including a full run when needed. A small diff does not imply a small impact; "just to be safe" is not sufficient justification for repeatedly running every check.

Separate rapid feedback during development from comprehensive checks before merging or releasing. Prefer the repository's existing targeted checks, incremental execution, and trustworthy caches. Do not build another test management system merely to comply with this section. Explicitly required merge and release checks must still be completed at the appropriate stage, without mechanically repeating them after every intermediate change. Do not assume later automation will perform verification that is necessary now.

## Reuse evidence and know when to stop

Reuse results from checks that actually ran when the relevant code, dependencies, configuration, environment, and inputs are unchanged and the checks themselves are suitable for reuse. Rerun the verification whose conclusions are invalidated by subsequent changes, rather than repeating all checks as a formality. End the current round of verification once the agreed acceptance criteria have sufficient supporting evidence, necessary checks are complete, and there is no concrete reason to broaden the scope. Address specific evidence gaps with targeted checks; do not make "every check has been run" a universal condition for completing a task.

## Investigate failures and read useful output

When a check fails, investigate whether the current change introduced or worsened the failure and whether it prevents acceptance of the current work. Briefly record problems confirmed to be unrelated to the change and not to affect delivery, without automatically expanding the repair scope. An unchanged file alone does not establish that a failure is unrelated. Do not weaken valid assertions, ignore failures, or rerun checks until they happen to pass merely to obtain an all-passing result. When verification is blocked or a conclusion cannot be established, explain the gap and its consequences rather than report a pass.

When reading check results, start with the overall status, failure summaries, and relevant details, keeping the full output available for investigation. Do not load all successful-test logs into context, or lose failure status and diagnostic evidence through output truncation. Report the scope actually verified and any outstanding issues that affect delivery; passing targeted checks must not imply that the entire system has been verified.

## Report what the evidence establishes

State which behavior, interfaces, and relevant conditions were checked, the overall results, and any outstanding gap that affects delivery. If a check did not run, report that status and its practical consequence. Keep evidence accessible without crowding the conclusion with successful logs. Subsequent changes require rechecking the evidence they invalidate; the existence of an old pass is insufficient.

A targeted parser check supports the parser behavior it exercised. If a changed response format still needs an integration check with the caller before merging, say so and perform it when possible. The shared requirement for truthful reporting is in the entry; [communication.md](communication.md) explains how to present a scoped conclusion without irrelevant caveats.

## Why tests should protect behavior

Tests should focus on behavior that must be guaranteed, real boundaries, and known risks, rather than preserving every internal step of the current implementation. Do not introduce extensive mocks, setup, and supporting frameworks merely to test layers you created, making an ordinary business scenario harder and harder to understand.

When tests are substantially more complicated than the business behavior itself, examine whether that complexity comes from real requirements or from unnecessary decomposition, implicit dependencies, and defensive mechanisms. Do not simply accept the current structure and keep generating more code to support it. This is not a reason to reduce necessary testing. Keep verification of critical behavior and actual risks, while avoiding permanently locking in call sequences, internal structures, or repeated defensive checks that have no business significance.
