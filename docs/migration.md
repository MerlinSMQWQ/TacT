# Source correction and migration record

Date: 2026-10-20. The Kit keeps its entry, topic split, and project layer. This revision corrects the incomplete authoring source used for the first migration and restores the missing material. It records source coverage and local checks; improvements in engineering outcomes remain under trial.

## Which source was used

The first migration used a 40,670-byte, 185-line English file. The file later supplied as `AGENTS.en.md` is identical to that older baseline. After the source mismatch was reported, the same directory was checked and `AGENTS-10.en.md` was found: 61,760 bytes, 241 lines, with the delegation chapter and other additions described in the review feedback. The full text, rather than the feedback summary, is the source of this revision.

That complete file is preserved byte-for-byte as [baseline/AGENTS.en.md](baseline/AGENTS.en.md). SHA-256: `71a8b089c4b636ec57b16333bd8ea2c1f66a997702c46c012848bafdb2e4a9c2`.

The [first migration record](https://github.com/MerlinSMQWQ/TacT/blob/09dac8487bbf17b99e861f999580be315518a50f/docs/migration.md) and [older baseline](https://github.com/MerlinSMQWQ/TacT/blob/09dac8487bbf17b99e861f999580be315518a50f/docs/baseline/AGENTS.en.md) remain in Git history. Their completeness claims apply only to the older source; they did not establish coverage of the complete authoring draft. The earlier statement that there was no source delegation chapter was true of the file used, not of the full draft.

The baseline is reference material and a fallback, not a second active entry. The Chinese plan remains local discussion material, excluded by the existing ignore rules. Current reading and maintenance conventions live in the entry, `core/README.md`, `project/README.md`, and `core/evolving.md`.

## Coverage of the complete source

Line ranges below refer to the current 241-line baseline. Unchanged guidance was retained; additions and changed passages were migrated into the existing topics. The earlier developer-facing additions remain where they still help. In particular, the scoped-conclusion guidance and qualification examples already in `core/communication.md` are retained alongside the full source's communication changes.

| Source section | Destination and treatment |
| --- | --- |
| Opening, lines 1–12 | Goals and boundaries in the entry; the Kit's prototype role, value of reasoning, and distinction from a duplicate project inventory in `core/README.md` and `core/evolving.md`. |
| Human control, lines 13–32 | `core/collaboration.md`: interaction helps form the result; developer participation has value; delivery supports effective review; sufficient evidence is also a stopping condition. The correctness and complexity-cost paragraph remains in `core/complexity.md`; key judgments remain in the entry. |
| Delegation, lines 33–68 | All 17 body paragraphs in `core/delegation.md`, grouped for navigation. The task-cancellation example, recipient background, proportionate observation, changed premises, integration duties, read-only scope, direct reporting route, independent review, uncertainty, and decision authority are preserved. File-relative references now point to the Kit or the relevant topic. |
| Complexity, lines 69–88 | `core/complexity.md`, including the new restriction on incidental formatting, renaming, import, and comment changes. A short version is also in the entry. |
| Business flow and abstraction, lines 89–100 | Retained in `core/complexity.md`, including the reasons for decomposition and the limits of reuse and decoupling. |
| Existing designs, lines 101–114 | Retained in `core/complexity.md`; the recording reference points to `core/evolving.md`. Settled answers remain reusable while their premises hold. |
| Investigation and progress, lines 115–144 | `core/working.md`, including the new plan-invalidation paragraph, both unexpected-state paragraphs, and updated intermediate-result guidance. The entry now includes unexpected state as a reading trigger. |
| Tools, lines 145–162 | `core/tools.md` separates the source's caller and designer duties. The existing concrete status-operation guidance remains useful and is retained. |
| Verification, lines 163–178 | All seven source paragraphs remain in `core/verification.md`. The expanded truthfulness paragraph from lines 203–204 also lives here, distinguishing executed checks from reasoning about code. |
| Comments, lines 179–188 | All four paragraphs remain in `core/communication.md`, including the timeout and idempotency example. |
| Judgments and communication, lines 189–206 | `core/communication.md`, with existing scoped-conclusion and qualification guidance retained. The expanded evidence paragraph is in `core/verification.md`; its shared boundary is summarized in the entry. |
| Understandable documentation, lines 207–222 | `core/communication.md`, including agent handoffs, the warning against unrelated contrasts, and the distinction between current delivery explanations and records of how principles developed. |
| Judgment, experience, and constraints, lines 223–241 | `core/evolving.md`: preserve reasoning, applicable conditions, counterexamples, and useful history; retain exploratory ideas without making them instructions; distinguish observation, hypothesis, proposal, and developer confirmation. Project placement is explained in `project/README.md`. |

## Passages reviewed for meaning after adaptation

The source has 106 body paragraphs, excluding headings. A text comparison found 92 unchanged paragraphs in the entry and topic files. The remaining 14 were reviewed individually. Exact matches help locate preserved text; the meaning checks below address the consolidated passages and changed references.

| Source lines | How the meaning is retained |
| --- | --- |
| 3 | The entry and collaboration topic give delivery and interaction equal weight, retain the maintainer's control, and treat avoidable attention and review costs as part of delivery quality. |
| 5 | The adoption guide keeps the Kit's prototype role, the value of understanding the developer's engineering thinking, reasons and applicability, and the limits of what guidance alone can solve. Detailed experience is supported in the evolving topic. |
| 7 | The adoption guide and evolving topic distinguish recoverable project inventories from implementation context and examples needed to explain a judgment. |
| 9 | The entry retains hard boundaries and scoped restrictions, permission controls, judgment for soft guidance, and the distinction between preserving reasons and repeating the argument on every task. |
| 11 | The opening principle and goal together retain solving grounded current problems while preserving understanding, review, and the ability to change the system. |
| 27 | The entry and complexity topic retain correctness, real security, and integrity boundaries, alongside maintenance costs that still apply to robustness or extensibility work. |
| 55 | “In this file” becomes “in this Kit”; human roles, the direct delegator route, explicit communication arrangements, and the prohibition on delaying or concealing conflicts remain intact. |
| 57 | “Updates this file” becomes “updates the guidance”; actual edit authority, read-only proposals, and the difference between agent agreement and developer confirmation remain intact. |
| 59 | The reference to “this file's verification principles” becomes a link to `verification.md`; proportional integration checks, uncertainty, and avoiding both blind trust and wholesale repetition remain intact. |
| 113 | The recording reference points to `evolving.md`; reusable reasons and constraints, reuse of settled answers, and rechecking changed premises remain intact. |
| 195 | The communication topic retains cautious language tied to actual uncertainty, direct judgments for discussion and low-risk exploration, one relevant qualification, and consequential risks. The existing more detailed qualification-selection method and examples are preserved. |
| 225 | “This file” becomes “The Kit”; specific problems, contemporary facts, options, trade-offs, subsequent results, and variable depth remain legitimate experience records. |
| 229 | The recording reference links to `delegation.md`, with project-specific material kept in the project layer. Confirmed reasons, experiential context, scope, and limits on promoting guesses remain intact. |
| 241 | “This file and the Kit” becomes “The Kit and its individual files”; both engineering guidance and learning value remain criteria for retention, alongside actual collaboration costs. |

## Corrections to the Kit's own guidance

- The adopting project's `project/notes.md` now records the upstream repository and copied commit. No shared file needs an installation-specific edit. This removes the conflict between source recording and keeping shared copies unchanged.
- The entry keeps action-relevant reading rules and boundaries. Detailed setup, distribution, and fallback instructions live in `core/README.md`.
- The adoption and project guides use direct language for reading files, recording source details, and checking what a tool actually loaded. Tool-specific and dated source records are kept here, outside shared `core/`.
- The communication trigger now applies before delivery explanations, recommendations, agent handoffs, and code comments. Unexpected state and recording reasoning also have explicit triggers.

## Local verification and limits

The representative real task is this source correction. The source-dependent migration paused when the specified file proved to be the older version. A bounded directory check found the full file matching the review's size, line count, and missing chapter. The migration then used its actual text. This is an observed application of investigating unexpected state before continuing dependent work, rather than guessing the missing content or creating a test project.

The working session read current project notes, the relevant core topics, and the existing project verification supplement. The paragraph comparison covered the complete source, and the 14 adapted passages were reviewed for changed conditions, authority, evidence, and scope. Delegation text and the cancellation example come from the original file; no subagents were required to migrate or review the documents.

Focused checks passed for all 16 delivered Markdown files and 28 local links, including English content and filenames, whitespace, the unchanged core layout, the complete baseline's byte match, and source coverage. Shared `core/` files have no local dependency on `docs/`, dated source block, or Codex-specific setup note. There is no application suite in this documentation repository.

A fresh `codex-cli 0.162.1` invocation of `codex debug prompt-input` from the TacT root exited successfully. A comparison with the exact current entry confirmed the full updated text was present, including the final paragraph. Project notes were not automatically included; the entry's explicit read requirement still matters. The current working session read those notes and the matching verification supplement. The full input dump remained in a local temporary file because it can contain unrelated private instructions. No model call was made for this startup check.

These checks establish source coverage, document structure, and the checked CLI input construction. They do not establish the reliability of fresh model-driven reading decisions, every desktop startup path, or improvements in engineering outcomes.

## Trial handoff

The missing-source correction was not covered by the first migration. Its coverage and local checks are now complete, so the local plan can remain archived as an implementation checklist with its source and completion status corrected; adoption effects remain under trial. Preserve useful observations in the adopting project's existing notes rather than creating a second long-term plan or a monitoring system.

Normal use still needs to check whether a fresh agent follows the reading triggers and whether delivery, verification choices, understanding, and useful developer participation improve. Where a concrete regression appears, compare with the appropriate preserved source and hold the task, starting state, and model settings as steady as practical. A source-coverage check alone does not establish those outcomes.
