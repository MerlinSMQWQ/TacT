# First English edition: migration and local adoption record

Date: 2026-10-15. The English split is implemented. The local checks below establish a bounded adoption path; outcome improvements remain under trial. This is a historical migration record, not another runtime instruction set or a second ongoing plan.

## Source and scope

The source is the complete English `AGENTS.md` supplied in the TacT workspace. The planning draft names `AGENTS.en.md`, but no separate file with that name existed. The supplied English text contains the requested revision about scoped conclusions and selecting useful qualifications. It was preserved byte-for-byte as [baseline/AGENTS.en.md](baseline/AGENTS.en.md) before editing.

Baseline: 40,670 bytes; SHA-256 `54d2395fee6107209cb04e200a37472a3ddc0e3524b2d7899e8565960f29baca`.

The original workspace tracked only `.gitignore`; the supplied `AGENTS.md` was untracked. Existing ignore rules exclude `plan.md` and `plan/`. The Chinese planning draft remains local discussion material and is not force-added to the English Kit.

## Migration map

Source line ranges below refer to the preserved baseline. “Moved” retains the paragraph text; “merged” consolidates shared statements or updates references after the split; “added” identifies material the baseline did not already supply.

| Baseline material | Destination and treatment |
| --- | --- |
| Opening, lines 1–10 | Merged into the entry's goals, hard boundaries, and judgment statement; purpose and maintenance context in `core/README.md` and `core/evolving.md`. |
| Human control, lines 11–22 | Frequent judgment summarized in the entry; four paragraphs moved to `core/collaboration.md`; correctness, security, integrity, and complexity costs merged into the entry and `core/complexity.md`. |
| New complexity, lines 23–40 | Moved into `core/complexity.md`, with immediate decisions above the fuller rationale. |
| Business flow and abstraction, lines 41–52 | Moved into `core/complexity.md`; responsibility, reuse, contract, and navigation trade-offs retained together. |
| Existing designs, lines 53–66 | Moved into `core/complexity.md`; the final paragraph now names `core/evolving.md` instead of “the final section of this file.” |
| Investigation and progress, lines 67–90 | Ten substantive paragraphs moved into `core/working.md`; the general anti-ritual statement merged into the entry and a short local explanation. |
| Tool feedback, lines 91–100 | Designer guidance moved into `core/tools.md`; known-state and recovery boundaries merged with a separately stated caller perspective. |
| Verification, lines 101–116 | All seven paragraphs moved into `core/verification.md`; concise reporting guidance added and shared truthfulness requirements kept in the entry. |
| Comments, lines 117–126 | All four paragraphs moved into `core/communication.md`, including the timeout and idempotency example. |
| Judgments and qualifications, lines 127–154 | Twelve paragraphs moved into `core/communication.md`, including the reasons and both scoped-verification and direct-copy examples; the shared evidence/reporting boundary merged into the entry. |
| Understandable documentation, lines 155–170 | All seven paragraphs moved into `core/communication.md`, preserving the scope for code identifiers and machine-readable output. |
| Useful accumulated guidance, lines 171–185 | Moved into `core/evolving.md`; three paragraphs have file-relative wording updated, and project placement is explained in `project/README.md`. |

## Added material

- The entry's project-reading contract, partial topic supplements, precedence, authority labels, six everyday principles, and action-based topic index implement the planning decisions.
- `core/README.md` supplies adoption, same-source distribution, source identification, preservation of project content, trimming, fallback, and bounded trials for developers.
- `core/collaboration.md` adds briefing, observation, intervention, and review from the developer's perspective. It does not turn every agent responsibility into another human supervision task.
- `core/delegation.md` is newly written from the plan's stated delegation principles. The baseline has no independent delegation section. It covers handoff, ongoing guidance, filtered evidence, integration, and responsibility without adding parallel-edit rules or fixed review ceremonies.
- `core/tools.md` distinguishes caller recovery from designer feedback. `core/evolving.md` adds project-to-core generalization, acquisition diagnosis, and conditional responses to observed loading or output problems.
- `project/README.md` explains what takes effect and how to specialize. `project/notes.md` records only the already confirmed first-edition mode and scope. `project/verification.md` applies verification selection to the actual documentation-only TacT repository.

## Meaning checks

A paragraph comparison located the unchanged material and isolated the passages that were consolidated or reworded. Those passages were reviewed against the baseline for conditions and effects, rather than treating an exact-text match as proof of semantic correctness:

- Opening goals and the closing anti-ritual statement remain general judgment guidance. They do not convert all heuristics into prohibitions or approval gates. Safety, authorization, integrity, truthfulness, and scoped restrictions remain explicit in the entry.
- Consolidating the correctness/security paragraph retains both the non-negotiable boundaries and the requirement to justify maintenance costs even for robustness or extensibility work.
- Replacing the “final section” reference retains the obligation to preserve reusable confirmed reasons, reuse settled answers, and recheck them when premises change.
- Splitting caller and tool-designer duties retains unknown-outcome status checks, missing business decisions, known-state limits, and the boundary against promoting external commands into instructions.
- Moving truthfulness to the entry retains actual-evidence requirements and the effect of later changes on earlier verification. The communication examples remain explanatory counterexamples, not a ban on qualifications.
- Updating file-relative wording in accumulated-guidance paragraphs preserves the scope for recording confirmed constraints and the ability to remove an unhelpful Kit; project-specific conclusions stay in the project layer.

Conditions that matter remain beside the relevant practices: when verification expands, required merge/release checks, why unknown existing mechanisms need investigation, when an unresolved decision needs a developer answer, and why repeated failures do not automatically justify more rules. The upper parts can guide action without relying on a later exception to correct them.

## Local adoption evidence

The real project is TacT itself. The representative task is this instruction migration, including the choice of verification for a repository with no application code or test suite. No test project, model run, or persistent evaluation framework was added.

| Check | Evidence and supported result |
| --- | --- |
| Primary working session | The current Codex desktop chat started in TacT with the original project entry supplied in context. After editing, explicit file reads obtained the new entry and project notes, followed by the relevant core files and checks for matching project supplements. This checks the updated guidance in an ongoing session. |
| Fresh CLI input construction | Local `codex-cli 0.162.1`, launched from the TacT root using `codex debug prompt-input`, exited successfully. A comparison of its rendered input with the exact new entry, including its final paragraph, confirmed the complete entry was present. No model call was made. |
| Notes acquisition | The CLI startup input did not automatically contain the notes body. The entry explicitly requires reading it. The working session obtained the full `project/notes.md` through a file read before the remaining verification work. |
| Matching supplement | The working session read `core/verification.md` and the existing `project/verification.md` together. It also checked for matching collaboration, communication, complexity, working, tools, delegation, and evolving supplements; none existed. The project supplement adjusts verification selection without replacing the shared evidence or failure guidance. |
| Applied judgment | Verification was selected for actual instruction behavior: baseline comparison, boundary and qualification review, local-link and English-content checks, host-input inspection, and project-reading checks. No unrelated application suite or new testing system was invented. The baseline and the existing plan ignore rules were preserved. |

CLI startup construction and the ongoing desktop session are separate evidence. They establish that the entry can be discovered in the checked CLI launch, and that notes and supplements can be acquired and applied in the current real task. They do not establish that a fresh autonomous model run will reliably follow every reading trigger or that every desktop startup path loads the new entry. Those behaviors remain trial questions; a prompt dump alone cannot prove them.

Focused document checks passed for all 16 delivered Markdown files and 25 local links, including English content and filenames, the unchanged baseline digest, the planned core layout, shared-file links, and whitespace. No application test suite exists in the current repository.

The full startup dump stayed in a local temporary file because it may contain unrelated private instructions. The command's installed help and observed output were used for the debug check. The expected discovery behavior was also checked against [official OpenAI documentation](https://developers.openai.com/codex/guides/agents-md); documentation did not substitute for the local observation.

## Trial handoff

The adopted reading and maintenance conventions now live in `core/README.md`, `project/README.md`, and `core/evolving.md`. The original Chinese plan is retired as an implementation checklist; it remains local reference material rather than a second maintained authority.

Continue bounded use in one or two real projects. When an observation has reusable value, record the task, behavior, and effect in that project's existing notes, labeling observations and unadopted proposals. Look for actual delivery progress, avoidable rework, proportionate verification, relevant communication, and timely visibility into important trade-offs. Test a fresh model-driven startup and its reading decisions in normal use; do not infer that from the CLI input inspection or this explicitly refreshed session.

If problems appear, first locate unavailable content, unhelpful judgment guidance, or an execution dependency. Compare against the preserved baseline only when a suspected regression warrants it, holding the task, starting state, and model settings as steady as practical. No measured improvement in task quality, context cost, or developer effort is claimed by this first migration.
