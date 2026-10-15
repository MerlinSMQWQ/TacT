# Project-specific context

This directory belongs to the adopting project. Read this when introducing or changing project guidance; skip rereading it once the placement and authority of the relevant content are clear. It is preserved when the shared entry and `core/` are updated.

## Keep notes small and effective

The entry requires the agent to obtain `notes.md` before substantive work. Begin with an almost empty file when no project-specific constraints or work mode have been confirmed. There is no mandatory list of fields to complete.

Record only context whose absence would cause a repeated misunderstanding, consequential risk, or substantial reinvestigation. Preserve the confirmed conclusion, its reason, its scope, and necessary limits. Put readily recoverable code facts and implementation explanations in code or ordinary documentation instead.

Distinguish the force of a record explicitly. For example:

> Confirmed: Keep the current external response format during this stage.
>
> Observation: After two local changes, the agent ran the entire test suite each time.
>
> Proposal, not adopted: Try a more specific trigger for verification guidance.

These labels illustrate authority; they are not a required template. An observation or proposal does not become an instruction by being written here. An agent may organize confirmed conclusions and their reasons, but must not turn guesses, temporary workarounds, or its own design preferences into permanent constraints.

## Put action-changing constraints where they will be read

If a project rule changes what actions are allowed, `notes.md` must state enough of it to decide before acting. Do not hide it in a topic file that might never be selected or leave only a link to it. Longer explanations and scoped adjustments may live in `project/<topic>.md`.

When the agent reads `core/<topic>.md`, the entry also requires checking and reading a matching `project/<topic>.md` if present. The supplement changes only the parts it explicitly addresses; it does not replace the whole core document. Confirmed agreements can narrow boundaries, make them more specific, or change soft defaults. They cannot relax hard boundaries by claiming greater specificity. Resolve consequential conflicts from known authority and facts, or ask the specific question that remains.

Only create a supplement when there is a useful adjustment to make. TacT's own [verification.md](https://github.com/MerlinSMQWQ/TacT/blob/main/project/verification.md) is a scoped example for this documentation repository; do not copy it into an unrelated project as a universal rule.

For a module constraint, first keep the necessary restriction discoverable before action. Test the primary tool's actual timing for module `AGENTS.md` files before choosing that placement. Do not assume names or directory nesting prove acquisition.

## Maintain and propose changes

Revise or merge existing records instead of appending every correction. Remove obsolete guidance and keep observations only while they can inform a reusable decision. Ask for the relevant authorization before changing a developer-confirmed boundary. Follow [core/evolving.md](../core/evolving.md) when diagnosis or generalization is needed.

In an adopting project, record proposed shared changes here and take them to the TacT repository; leave the installed shared snapshot consistent. In this source repository, authorized Kit work edits shared files directly. Do not let a shared update overwrite this directory. Existing project instructions must be carried forward before deploying the shared entry.
