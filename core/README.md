# Using the TacT Agent Kit

TacT helps developers and agents make engineering judgments together. Delivery quality and the experience of working together have equal weight. The agent advances the task and supplies evidence; the developer can observe, learn, and guide important choices while they still affect the result.

Read this guide and [collaboration.md](collaboration.md) when adopting the Kit. Once setup and the relevant guidance are clear, ordinary tasks do not need to reread this guide.

## Set up a project

1. Read the project's existing instructions before replacing its entry. Carry forward confirmed constraints, work mode, and authorization limits into `project/notes.md`. Keep longer reasons in project topic files when useful.
2. Copy `AGENTS.md` and the complete `core/` directory from the same Git commit. Preserve an existing `project/` directory. If needed, add its `README.md` and a nearly empty `notes.md`, following [the project guide](../project/README.md); do not copy another project's constraints as defaults.
3. Record the source repository and copied commit in the adopting project's `project/notes.md`. Keep the shared files unchanged there. Propose shared changes in the project notes and bring them back to the Kit repository.
4. Check the tool and startup method you actually use. Confirm that the agent receives the root entry and reads project notes before substantive work. For a relevant core topic, check that it also reads a matching project supplement if one exists. Use available prompt or tool records to support the check.
5. Try a real task with a meaningful judgment, such as choosing checks for a local change or diagnosing repeated failures. Look at the action and evidence, rather than whether the agent can repeat the index. Keep unmet checks visible.

The shared files do not guarantee that a host loads them. Topic links require reading when the task calls for them. Other tools or startup methods need their own check; there is no requirement to build a compatibility layer or package every topic as a Skill.

## Work with the Kit

Give the agent the goal, business facts it cannot obtain, work mode, and relevant authorization. It should obtain code, tests, and existing documentation itself. You can intervene when attempts stop producing evidence, supporting work displaces delivery, or a choice needs your judgment. You do not need to supervise each operation or redo all verification; [collaboration.md](collaboration.md) gives examples.

The entry carries shared boundaries, frequent judgments, and the reading index. `core/` belongs to the Kit; `project/` belongs to the adopting project. This ownership does not determine reading order: project restrictions may need to be known before any action. A matching project topic adjusts only the parts it names, leaving the rest of core applicable.

Paths in the entry start at the Kit's installation root, even when a task runs from a deeper directory. Reuse guidance already in context when it is still current and applicable. Putting practices above detailed reasons helps navigation; it does not make the host load only part of a file.

## Update or trim the shared files

Update `AGENTS.md` and `core/` together from one commit. Keep source details in `project/notes.md`, and leave project content intact. Projects may intentionally use different versions. Investigate an unknown source, accidental edits to a shared copy, or an entry that no longer matches its topic files.

Make shared changes, including trimming and index changes, in the Kit repository. Ordinary Kit maintenance here edits those files directly. Adopting projects should not patch their shared copy. Add synchronization tooling only if the actual update burden warrants it.

Keep a known source version or original authoring baseline available for fallback. If a regression is suspected, compare a bounded task from the same starting state and similar model settings. When restoring an entry, preserve current project constraints and their pre-action reading. Avoid changing principles, task, and model together and attributing the result to the split.

## Why the Kit preserves reasoning

The Kit is also a working prototype through which the developer can articulate engineering thinking and accumulate experience. Explain why a principle was proposed, what problem it responds to, when it applies, and which facts or trade-offs would change the conclusion. Detailed reasoning can help the developer examine their thinking and guide the agent; do not reduce it to conclusions merely to save tokens. This material can inform later Kit design; guidance alone is not expected to solve every engineering problem. Individual tasks read only what helps the current judgment.

Do not maintain a second account of project structure or code that can be read from the repository. Include implementation context and examples when they explain a judgment. [evolving.md](evolving.md) distinguishes useful experience, exploratory ideas, and confirmed guidance.

## Judge whether it helps

Look for actual progress, avoidable rework, proportionate verification, useful interaction, and timely visibility into important trade-offs. A smaller initial context is not evidence of better outcomes. Developer participation in design and learning can itself be valuable; reduce forced supervision without removing that participation.

When something goes wrong, distinguish content that was not available, guidance that did not help judgment, and a reasonable judgment blocked by execution or an external dependency. Improve the relevant part. Follow [evolving.md](evolving.md) to revise or remove guidance, including returning to a single file if the split costs more than it helps. Detailed records do not require every task to repeat the full argument or produce a compliance report.
