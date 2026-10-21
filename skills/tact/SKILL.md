---
name: tact
description: Apply the project's TacT Agent Kit when the user asks to use TacT or assess work against its collaboration and delivery guidance.
---

# TacT Agent Kit

Use the TacT snapshot installed in this project to guide the current task.

Read the [TacT entry](../../../.tact/AGENTS.md) and
[project notes](../../../.tact/project/notes.md), reusing current guidance already
supplied by the host. Follow the entry's topic-reading triggers and read matching
project supplements when present.

This skill is installed at `.agents/skills/tact/SKILL.md`. Resolve the links above
from this file's directory, even when working in a nested folder. The Kit root is
`../../../.tact/` relative to this directory; resolve paths inside the Kit from
that root.

Keep the user's task and existing repository instructions in force. If the
referenced Kit is missing, report the missing path; do not silently use a global
copy or initialize or refresh the project unless the user requested that work.
