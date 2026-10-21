# Using the TacT Agent Kit

TacT helps developers and agents make engineering judgments together. Delivery quality and the experience of working together have equal weight. The agent advances the task and supplies evidence; the developer can observe, learn, and guide important choices while they still affect the result.

Read this guide and [collaboration.md](collaboration.md) when adopting the Kit. Once setup and the relevant guidance are clear, ordinary tasks do not need to reread this guide.

## Set up a project

With the `tact` CLI installed, preview and initialize an existing project directory:

```sh
tact init /path/to/project --dry-run
tact init /path/to/project
```

The `init` command installs its bundled Kit into `.tact/` and appends a marked reading instruction to the root `AGENTS.md`. Existing entry text and `.tact/project/` content remain intact. It checks for conflicting shared files before writing and does not upgrade an existing snapshot; use the explicit update procedure below for that. New project notes explain their purpose and ownership and record the package source and version; they do not inherit the TacT source repository's constraints. `.tact/manifest.json` records the package version and shared-file hashes.

1. Read the project's existing instructions and review the proposed entry addition. Resolve meaningful conflicts between local guidance and the Kit; the CLI does not interpret or migrate those rules. Record additional confirmed constraints, work mode, and authorization limits in `.tact/project/notes.md` when useful.
2. Run initialization and review the files before committing them. Repeating initialization with the same Kit preserves existing content and can restore missing files. A different shared snapshot or edited shared file requires a deliberate update; `init` reports the differences and leaves files unchanged.
3. Keep shared files unchanged in adopting projects. Propose shared changes in the project notes and bring them back to the Kit repository. The source repository and package version identify a packaged Kit; for a manual copy, record the exact source commit instead.
4. Check the tool and startup method you actually use. Confirm that the agent receives the root entry and reads project notes before substantive work. For a relevant core topic, check that it also reads a matching project supplement if one exists. Use available prompt or tool records to support the check.
5. Try a real task with a meaningful judgment, such as choosing checks for a local change or diagnosing repeated failures. Look at the action and evidence, rather than whether the agent can repeat the index. Keep unmet checks visible.

Manual adoption remains possible: copy `AGENTS.md` and the complete `core/` directory from one commit, preserve the adopting project's `project/` directory, and add its guide and nearly empty notes only if needed. Read existing instructions before replacing an entry, and carry forward confirmed constraints. Paths start at the chosen Kit root; for CLI installations that root is `.tact/`, not the repository root.

The shared files do not guarantee that a host loads them. Topic links require reading when the task calls for them. Other tools or startup methods need their own check; there is no requirement to build a compatibility layer or package every topic as a Skill.

## Work with the Kit

Give the agent the goal, business facts it cannot obtain, work mode, and relevant authorization. It should obtain code, tests, and existing documentation itself. You can intervene when attempts stop producing evidence, supporting work displaces delivery, or a choice needs your judgment. You do not need to supervise each operation or redo all verification; [collaboration.md](collaboration.md) gives examples.

The entry carries shared boundaries, frequent judgments, and the reading index. `core/` belongs to the Kit; `project/` belongs to the adopting project. This ownership does not determine reading order: project restrictions may need to be known before any action. A matching project topic adjusts only the parts it names, leaving the rest of core applicable.

Paths in the entry start at the Kit's installation root, even when a task runs from a deeper directory. Reuse guidance already in context when it is still current and applicable. Putting practices above detailed reasons helps navigation; it does not make the host load only part of a file.

## Update or trim the shared files

Update `AGENTS.md` and `core/` together from one package release or one commit. Updating the CLI does not change any initialized project's files. The `refresh` command applies documents from the installed package to the selected project; it does not download or upgrade the CLI. Preview and apply its bundled snapshot explicitly:

```sh
tact refresh /path/to/project --dry-run
tact refresh /path/to/project
```

The command uses the manifest's recorded hashes to distinguish unchanged shared files from local edits. A local edit or invalid installation record stops the plan before writes. Already-updated files are accepted, and the manifest is written last so an interrupted update can resume after inspection. Project-owned files remain intact, except that an untouched generated `notes.md` can receive the current introduction and source line. Customized notes are preserved; the manifest remains the authoritative installed-version record. Review the diff before committing.

Projects may intentionally use different versions. Investigate an unknown source, accidental edits to a shared copy, or an entry that no longer matches its topic files. A manually copied Kit without a manifest needs a deliberate manual update rather than a guessed baseline.

Make shared changes, including trimming and index changes, in the Kit repository. Ordinary Kit maintenance here edits those files directly. Adopting projects should not patch their shared copy. Add synchronization tooling only if the actual update burden warrants it.

Keep a known source version or original authoring baseline available for fallback. If a regression is suspected, compare a bounded task from the same starting state and similar model settings. When restoring an entry, preserve current project constraints and their pre-action reading. Avoid changing principles, task, and model together and attributing the result to the split.

## Why the Kit preserves reasoning

The Kit is also a working prototype through which the developer can articulate engineering thinking and accumulate experience. Explain why a principle was proposed, what problem it responds to, when it applies, and which facts or trade-offs would change the conclusion. Detailed reasoning can help the developer examine their thinking and guide the agent; do not reduce it to conclusions merely to save tokens. This material can inform later Kit design; guidance alone is not expected to solve every engineering problem. Individual tasks read only what helps the current judgment.

Do not maintain a second account of project structure or code that can be read from the repository. Include implementation context and examples when they explain a judgment. [evolving.md](evolving.md) distinguishes useful experience, exploratory ideas, and confirmed guidance.

## Judge whether it helps

Look for actual progress, avoidable rework, proportionate verification, useful interaction, and timely visibility into important trade-offs. A smaller initial context is not evidence of better outcomes. Developer participation in design and learning can itself be valuable; reduce forced supervision without removing that participation.

When something goes wrong, distinguish content that was not available, guidance that did not help judgment, and a reasonable judgment blocked by execution or an external dependency. Improve the relevant part. Follow [evolving.md](evolving.md) to revise or remove guidance, including returning to a single file if the split costs more than it helps. Detailed records do not require every task to repeat the full argument or produce a compliance report.
