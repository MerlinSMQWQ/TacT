<p align="center">
  <img src="https://raw.githubusercontent.com/MerlinSMQWQ/TacT/main/assets/logo.png" alt="TacT logo: a developer and a friendly agent building together" width="280">
</p>

<h1 align="center">TacT Agent Kit</h1>

<p align="center">
  <strong>Good engineering takes tact.</strong><br>
  A guide for developers and agents to make sound decisions, deliver working results,<br>
  and keep important choices visible.
</p>

<p align="center">
  <a href="https://github.com/MerlinSMQWQ/TacT/blob/main/core/README.md">Get started</a> ·
  <a href="https://github.com/MerlinSMQWQ/TacT/blob/main/core/collaboration.md">Collaboration</a> ·
  <a href="https://github.com/MerlinSMQWQ/TacT/blob/main/AGENTS.md">Agent entry</a>
</p>

---

## The idea

TacT takes its name from *tact*: a sense of proportion and consideration in how people work together. It gives engineering delivery and the developer's interaction experience equal weight. The agent should advance the work and provide evidence, while the developer can observe, learn, and guide important choices when they still matter.

## Install and initialize

Requires Python 3.11 or newer. The CLI has no runtime dependencies. The distribution name is currently `tact-agent-kit`; the executable is `tact`. PyPI publication is pending, so install from this checkout for now:

```sh
uv tool install .
tact --version

# Preview first, then initialize an existing project directory.
tact init /path/to/project --dry-run
tact init /path/to/project

# From inside the target project, the path defaults to the current directory.
tact init
```

The project can use any language; it does not need a Python environment. TacT installs the bundled Markdown locally without fetching rules during initialization:

```text
your-project/
├── AGENTS.md                 # Existing text plus a marked TacT reading instruction
└── .tact/
    ├── AGENTS.md             # Shared Kit entry
    ├── core/                 # Shared topic guidance
    ├── project/
    │   ├── README.md         # Guide for project-owned notes and supplements
    │   └── notes.md          # Project-owned notes, with a short introduction
    └── manifest.json         # Package version, source URL, and shared-file hashes
```

Review and commit `AGENTS.md` and `.tact/` with your project. Put local constraints and supplements in `.tact/project/`; files already there are preserved. Existing root-level `core/` or `project/` directories are left intact. The root entry tells the agent to read the Kit and project notes before substantive work, and establishes `.tact/` as the base for the Kit's relative paths.

Repeated initialization with the same package leaves matching files untouched and restores missing files. `--dry-run` lists proposed writes and shows the root entry diff without creating files or directories. Existing shared files, version metadata, or a TacT entry block that differ cause initialization to stop with differences for review. There is no implicit upgrade or force-overwrite option.

TacT checks for conflicts before writing. It also rejects symbolic links at managed paths and a nonempty root `AGENTS.override.md`, which would hide the normal entry in Codex. Resolve those conditions explicitly before retrying. If a filesystem error interrupts writing, the command reports that partial files may remain; inspect them before retrying. Matching files are safe to reuse.

Initialization preserves existing instructions but does not interpret conflicts between their meaning and the Kit. Check actual agent loading and behavior using the [adoption guide](https://github.com/MerlinSMQWQ/TacT/blob/main/core/README.md). Installing a newer CLI does not change any initialized project.

## Refresh an initialized project's documents

`tact refresh` applies the documents bundled with the installed TacT package to a selected project. It does not download or upgrade the CLI. After installing a newer package, refresh a project's snapshot explicitly:

```sh
# Reinstall from your TacT checkout while developing locally.
uv tool install --reinstall /path/to/TacT
tact --version

tact refresh /path/to/project --dry-run
tact refresh /path/to/project
```

`refresh` compares each shared file with its recorded installation hash in `.tact/manifest.json`. Files that still match that baseline can be replaced with the bundled version. A file already matching the new bundle is also accepted, allowing an interrupted refresh to resume. Local changes or an untracked file occupying a new shared path stop the entire plan before any writes; the command shows the differences for review. A missing or invalid manifest also stops the refresh. Files missing from the new package require manual review; this command does not remove them automatically.

Project guidance is preserved. The only existing project file refreshed automatically is `notes.md` when it exactly matches a known untouched generated template, including the original source-only template. This adds the introduction and refreshes its version line. Once notes have been edited, they remain unchanged; the manifest is the authoritative record of the currently installed package, even if custom notes retain an older source line.

The preview shows all proposed file differences. Replacements are atomic per file, with the manifest written last. The entire refresh is not a filesystem transaction: if a write fails, inspect the reported partial changes before retrying. Repeating a completed refresh makes no changes.

## Find your way

| If you want to… | Start with |
| --- | --- |
| Bring the Kit into a project | [Adoption guide](https://github.com/MerlinSMQWQ/TacT/blob/main/core/README.md) |
| Understand how developers and agents work together | [Collaboration guide](https://github.com/MerlinSMQWQ/TacT/blob/main/core/collaboration.md) |
| See the agent's boundaries and topic index | [AGENTS.md](https://github.com/MerlinSMQWQ/TacT/blob/main/AGENTS.md) |

The shared Kit is `AGENTS.md` plus `core/`. Each adopting project owns its `project/` layer inside the Kit root. CLI installations record their package version and shared-file hashes. Manual copies should use files from one Git commit and record that commit in the adopting project's notes.

## Develop and build

```sh
# Reinstall so tests use the current bundled Markdown as well as current code.
uv run --reinstall-package tact-agent-kit python -m unittest discover -s tests -v

# Build the source distribution, then build its wheel.
uv build
```

Edit shared guidance at `AGENTS.md`, `core/`, and `project/README.md`. Hatchling includes these sources in the installed `tact_resources` namespace; no second editable copy is maintained. The source repository's `project/notes.md` and `project/verification.md` are not distributed as adopting-project defaults. When editing guidance during development, reinstall the package to refresh the bundled resource snapshot, including for editable installs.

The build produces a source archive and wheel in `dist/`. You can install a built wheel with `uv tool install /absolute/path/to/the.whl`. Package naming on PyPI and the project license still need to be settled before publication; this change does not configure publishing workflows.

## Source and migration

The [migration record](https://github.com/MerlinSMQWQ/TacT/blob/main/docs/migration.md) explains how the Kit was split from the complete authoring source, what was verified, and what remains to be tried. The [English baseline](https://github.com/MerlinSMQWQ/TacT/blob/main/docs/baseline/AGENTS.en.md) is preserved for comparison and fallback.
