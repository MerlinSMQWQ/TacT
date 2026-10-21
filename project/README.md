# Project notes and supplements

This directory belongs to the adopting project. Shared Kit updates must preserve it. Read this guide when adding or changing project guidance; ordinary work can use the current notes and relevant topic files directly.

## Start with notes

`notes.md` is read before substantive work. Record confirmed constraints and work mode whose absence would cause repeated misunderstanding, consequential risk, or substantial reinvestigation. State enough of any action-changing restriction here to guide the action; a link alone is insufficient. Longer reasons can live in a topic file.

When copying the Kit manually, record the source repository and exact commit here. The CLI records the source and package version in new notes, with shared-file hashes in the Kit's `manifest.json`. Initialization preserves existing notes. An explicit update may refresh an untouched generated notes template; customized notes remain intact. The manifest records the currently installed package even if custom notes retain an older source line. Update source records when the shared files are updated. Do not edit a source-version paragraph in `core/README.md`; the shared copy stays unchanged.

There is no required form to fill. Start nearly empty when no project constraints are established. Keep code facts in code and ordinary documentation; retain the reasoning and examples needed to explain a decision.

## Distinguish requirements from exploration

For example:

> Confirmed: Keep the current external response format during this stage.
>
> Observation: After two local changes, the agent ran the entire test suite each time.
>
> Hypothesis: The reading trigger may be too broad; this has not been established.
>
> Proposal, not adopted: Try a more specific verification trigger.

These labels show what takes effect; they are not a template. Unverified ideas and unresolved disagreements can remain useful exploration material. Recording them does not make them instructions. Preserve evidence gaps and never present a plausible explanation as something the developer confirmed.

## Add a topic file when needed

When the agent reads `core/<topic>.md`, it also checks for and reads a matching `project/<topic>.md`. The project file adjusts only the parts it explicitly addresses. Other core guidance remains applicable. Confirmed project agreements may narrow boundaries or change soft defaults; greater specificity alone cannot relax hard boundaries.

Create a supplement only for a useful adjustment. Keep action-changing restrictions in `notes.md` even when the details live elsewhere. Before relying on module-level instruction files, check when the primary tool actually reads them.

## Keep guidance useful

Revise or merge existing records instead of appending every correction. Remove obsolete instructions; retain historical reasoning when it explains a principle, labeling its former premises so it no longer governs action. Follow [core/evolving.md](../core/evolving.md) when diagnosing a recurring problem or generalizing experience.

Record proposed shared changes in the project layer and take them to the Kit repository. An agent may edit guidance only within its actual responsibility and authorization; a read-only investigator passes a proposal to its direct delegator. Agreement between agents is not developer confirmation.
