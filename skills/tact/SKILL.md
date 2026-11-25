---
name: tact
description: Apply the project's TacT Agent Kit when the user asks to use TacT or assess work against its collaboration and delivery guidance.
---

# TacT Agent Kit

Use the TacT snapshot installed in this project to guide the current task.

On first use in a session, before responding, read the [TacT entry](../../../.tact/AGENTS.md),
[project notes](../../../.tact/project/notes.md),
[communication guidance](../../../.tact/core/communication.md), and
[language and conversational style](../../../.tact/core/style.md), along with
`../../../.tact/project/communication.md` and `../../../.tact/project/style.md`
if present. This includes short questions
and casual conversation. Reuse their current contents if already supplied in
this session; otherwise read the files. Follow the entry's remaining topic-reading
triggers and read matching project supplements when present.

Read each required file in full before the response or action it governs.
Check the text actually returned: successful commands can still yield truncated
output. Keep reads within individual and combined output limits; read long files
separately in consecutive ranges and recover every missing range, including
partly returned lines. If coverage is unclear, reread that file in smaller
ranges. Reuse complete current contents already in context. If required content
remains unavailable, report the gap and pause dependent actions.

This skill is installed at `.agents/skills/tact/SKILL.md`. Resolve the links above
from this file's directory, even when working in a nested folder. The Kit root is
`../../../.tact/` relative to this directory; resolve paths inside the Kit from
that root.

Keep the user's task and existing repository instructions in force. If the
referenced Kit is missing, report the missing path; do not silently use a global
copy or initialize or refresh the project unless the user requested that work.
