# Using the TacT Agent Kit

TacT is engineering guidance for developers working with agents. It keeps judgment, delivery, and collaboration connected: the agent advances the task, the developer supplies decisions only they can make, and both can see the evidence and trade-offs that matter.

Start here and with [collaboration.md](collaboration.md) when adopting the Kit. An agent already carrying out a bounded task can skip this adoption guide once the entry, project constraints, and relevant topic guidance are available.

## Adopt it in one real project

1. Read the project's existing instructions before changing them. Preserve its effective constraints, work mode, and authorization limits in `project/notes.md`; retain longer reasons in project topic files where useful. Do not overwrite an existing entry and lose its rules.
2. Copy the root `AGENTS.md` and the complete `core/` directory from one TacT source snapshot. Preserve an existing `project/`; add its `README.md` and `notes.md` only if absent, using [project/README.md](../project/README.md) as guidance. Start `notes.md` nearly empty when no project constraints are established; there is no required briefing form. The TacT-specific notes and verification supplement are examples, not defaults for another project.
3. Use the primary tool and the actual way you start work to confirm that the entry is obtained and `project/notes.md` is read before substantive work. Check one relevant core topic together with an existing project supplement, if present. Inspect available prompt or tool records rather than relying on a reading self-report alone.
4. Choose a real task with a meaningful judgment to make, such as verification scope for a local change or diagnosis after repeated failures. Observe the action and its evidence, not merely whether the agent can recite this index. Keep any unmet adoption checks explicit.

The first installation is TacT itself, in Codex. Its scoped evidence and remaining trial questions are recorded in [the migration record](https://github.com/MerlinSMQWQ/TacT/blob/main/docs/migration.md). Other tools and startup paths need their own check; this edition does not supply a compatibility layer or a Skill for each topic.

## Work with it

Give the agent the goal, business facts it cannot obtain, work mode, and authorization that affect this task. It should obtain code, tests, and existing documentation itself. You can intervene when agreed behavior stops getting closer to working, supporting work consumes the delivery, or a material decision needs your judgment. You do not have to supervise each operation or redo all verification; [collaboration.md](collaboration.md) gives examples.

The entry carries boundaries and frequent judgments. The topic index selects fuller guidance when an action or obstacle calls for it. `core/` and `project/` describe ownership and scope, not loading order. The entry requires project constraints before action and matching project supplements when a core topic is read. Layout puts practices above detailed reasons for navigation; it does not make the host load only half a file.

## Codex adoption notes

Codex discovers instruction files along its startup directory path, with override files and a size limit. The arbitrary Markdown files linked by this Kit still require explicit reading; the entry supplies that reading contract. Restart in the intended directory after changing an entry and inspect the actual context. See [official OpenAI documentation](https://developers.openai.com/codex/guides/agents-md).

For the locally checked CLI, `codex debug prompt-input` renders the startup input without a model call. Inspect that input for the effective entry, then use ordinary file-reading records to check notes and topic supplements. The CLI startup check and the current desktop task are distinct evidence; neither establishes every Codex startup path. Do not publish full prompt dumps, which can contain unrelated private instructions.

## Distribute and update

The shared distribution unit is the root `AGENTS.md` plus `core/`, maintained in this Kit repository. Copy them together from one source version. In an adopting project, record proposed shared edits in `project/notes.md` and bring them back here; do not silently fork the shared copy. Trimming, merging topics, and changing the index are shared-source changes too.

Do not overwrite `project/` with a shared update. Projects may intentionally use different snapshots. Investigate unknown provenance, accidental divergence from the same snapshot, or an entry that no longer matches its topic files. Add synchronization scripts or a submodule only if an observed maintenance burden warrants them.

This repository is the shared source, so authorized Kit maintenance changes the shared files here directly. When adopting elsewhere, set the source-version paragraph below to the exact TacT Git commit from which both the entry and `core/` were copied. That paragraph is installation provenance; recording it does not authorize local edits to the shared guidance. The upstream repository and that commit are sufficient; no separate version manifest is needed. The source checkout's own Git commit identifies the snapshot here without a self-referential commit hash in its contents.

## Source version and fallback

Source: [MerlinSMQWQ/TacT](https://github.com/MerlinSMQWQ/TacT), first English split edition, 2026-10-15. Resolve the source snapshot from this checkout's Git commit; adopters record that exact commit when copying.

The migration baseline is the complete English `AGENTS.md` supplied for this task, preserved unchanged as [docs/baseline/AGENTS.en.md](https://github.com/MerlinSMQWQ/TacT/blob/main/docs/baseline/AGENTS.en.md). The plan's separately named `AGENTS.en.md` was not present. The supplied file includes the requested revision about scoped conclusions and useful qualifications. The [migration record](https://github.com/MerlinSMQWQ/TacT/blob/main/docs/migration.md) identifies moved, merged, and newly written material.

The baseline is a reference and fallback, not a second set of active instructions. If a regression is suspected, compare a bounded real task from the same starting state and, as far as possible, the same model settings. Restore the baseline entry if needed while retaining current project constraints; ensure their pre-action reading remains explicit. Do not attribute differences to the split after simultaneously changing the principles, model, and task.

## Keep or trim based on use

Judge the Kit by result quality, avoidable rework, attention and maintenance costs, and whether important choices remain visible to the developer. A smaller initial context is not evidence of better engineering outcomes. Record concrete reusable observations in the project layer, without building a complete work log, monitoring system, or evaluation system.

When something goes wrong, distinguish unavailable content, content that did not help judgment, and sound judgment blocked by execution or an external dependency. Improve that layer. Reading all the files is not success if the task still does not advance. Follow [evolving.md](evolving.md) when revising or removing guidance, including returning to a single file if the split costs more than it helps.
