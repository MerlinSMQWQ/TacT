# TacT project notes

Confirmed source: Use the complete English authoring baseline, preserved in `docs/baseline/AGENTS.en.md`. The source correction uses `AGENTS-10.en.md` (241 lines), not the shorter `AGENTS.en.md` used for the first migration. Kit filenames and guidance prose remain English; the Chinese planning draft stays outside the runtime Kit. The developer-selected conversation examples in `core/communication-examples.md` are an explicit exception: preserve their original Chinese and English text and distribute them with TacT.

Confirmed conversation examples: Keep the supplied question/answer order, tool-activity records, and attached review document. Restore Markdown transport escaping without rewriting, correcting, or adding critique to the original exchanges. Revise the examples in response to the maintainer's subsequent trial feedback.

Confirmed scope: Keep the Markdown entry, topic split, and project layer. Preserve the author's reasoning, conditions, examples, and useful existing additions when filling source gaps. Do not add synchronization, monitoring, an evaluation framework, mandatory project fields, or a Skill for every topic. Continuing trials determine whether the split improves outcomes.

Confirmed scope addition: Provide an installable Python package and a CLI to initialize selected repositories. PyPI is the intended distribution channel. Preserve the existing project's guidance during initialization.

Confirmed Skill scope: Add one project-local `tact` Skill through `init` and `refresh`, so users can discover and explicitly invoke the Kit in Codex. Keep it as a thin entry pointing to the project's `.tact/` snapshot, with UI metadata and the existing manifest's protection for local edits. Preserve the normal `AGENTS.md` loading path; do not duplicate the full Kit or create a Skill for every topic.

Confirmed publishing scope: Use the MIT license and publish to PyPI through GitHub Actions with Trusted Publishing. A published GitHub Release triggers publication after package checks; ordinary pushes and pull requests run the checks only. The maintainer does not publish packages manually from a local machine.

Refresh scope: The reported inability to adopt a newer installed Kit warrants an explicit `tact refresh` command for one selected repository. The name distinguishes refreshing project documents from upgrading the TacT package itself. Use the existing manifest to protect local shared-file edits and preserve project-owned guidance. This bounded operation does not introduce automatic or cross-project synchronization.

This is the Kit source repository, whose Git history identifies shared changes. Adopting projects retain package source/version metadata or, for manual copies, the source repository and copied commit; they do not edit the shared files to record it.

Confirmed iteration scope: Introduce step size and adjustable strong defaults by revising the existing entry and topic sections, preserving their reasoning, conditions, and examples. Pi is the runtime and acceptance environment for this iteration; that choice belongs in the project layer. Do not build a monitoring platform, a complete evaluation framework, a cross-host compatibility system, a Skill per topic, or new mandatory project configuration files.

Confirmed execution split: The agent's current work ends at stages 0–2 of the detailed execution plan: guidance changes, local packaging, and CLI verification. The maintainer leads stage 3 using QYCC as the real refactoring project. Pi trials and the subsequent release stages are outside the current execution scope; local checks must not be reported as Pi adoption or demonstrated collaboration improvement.

Confirmed conversation preference: The maintainer wants room for informal, open-ended conversation even when it does not advance a task. This does not require declaring a special mode. Tentative ideas should retain room for explanation and exploration before the agent develops a recommendation or treats them as work requests.

Confirmed initial reading: Require the Kit entry, project notes, communication guidance, and any matching project communication supplement before the first response in each new session, including a single short question. Put this requirement directly in the generated root entry as well as the shared entry and Skill. Current contents already in the session may be reused. An explicit refresh may migrate the known unchanged older generated entry while preserving surrounding project instructions; customized entry blocks remain protected.

Observed feedback and candidate revision: The supplied QYCC conversation shows advice developed before the reason for considering a backend change was established. A separate reply about an unfamiliar council skill included operating limits and a non-execution statement beyond the question about its purpose and presence. The maintainer reports that this single-question Pi session skipped TacT, including communication guidance, because the agent judged reading it unnecessary. The current revision adjusts the existing defaults for intent, recommendations, explanation depth, and initial reading, with short examples. Whether this improves conversation in Pi remains to be tested by the maintainer; the broader contribution of model and harness behavior remains unestablished.
