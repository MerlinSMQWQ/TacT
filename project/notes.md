# TacT project notes

Confirmed source: Use the complete English authoring baseline, preserved in `docs/baseline/AGENTS.en.md`. The source correction uses `AGENTS-10.en.md` (241 lines), not the shorter `AGENTS.en.md` used for the first migration. Kit filenames and prose remain English; the Chinese planning draft stays outside the runtime Kit.

Confirmed scope: Keep the Markdown entry, topic split, and project layer. Preserve the author's reasoning, conditions, examples, and useful existing additions when filling source gaps. Do not add synchronization, monitoring, an evaluation framework, mandatory project fields, or a Skill for every topic. Continuing trials determine whether the split improves outcomes.

Confirmed scope addition: Provide an installable Python package and a CLI to initialize selected repositories. PyPI is the intended distribution channel. Preserve the existing project's guidance during initialization; adding a Skill is not part of this first implementation.

Confirmed publishing scope: Use the MIT license and publish to PyPI through GitHub Actions with Trusted Publishing. A published GitHub Release triggers publication after package checks; ordinary pushes and pull requests run the checks only. The maintainer does not publish packages manually from a local machine.

Refresh scope: The reported inability to adopt a newer installed Kit warrants an explicit `tact refresh` command for one selected repository. The name distinguishes refreshing project documents from upgrading the TacT package itself. Use the existing manifest to protect local shared-file edits and preserve project-owned guidance. This bounded operation does not introduce automatic or cross-project synchronization.

This is the Kit source repository, whose Git history identifies shared changes. Adopting projects retain package source/version metadata or, for manual copies, the source repository and copied commit; they do not edit the shared files to record it.
