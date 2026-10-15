# Evolving the guidance

Use this when recording a reusable correction, changing a confirmed constraint, generalizing project experience, or removing guidance that no longer helps. Skip rereading it for ordinary implementation facts that can be recovered directly from code and tests.

## Record the reason at the right scope

When the developer clarifies an issue that is prone to repeated misjudgment, proactively record the confirmed conclusion in the appropriate place, including its rationale, scope, and necessary limitations. Resolve confusion locally when naming, implementation changes, or nearby decision comments can address it. Only information that genuinely affects judgment across tasks belongs in durable guidance; project-specific conclusions stay in the project layer. Do not elevate guesses, one-off workarounds, temporary states, or your own design preferences into lasting constraints.

In an adopting project, put confirmed project constraints and work mode in `project/notes.md`, with enough information to govern actions before work starts. Keep longer reasons in a relevant project topic file. Label observations and unadopted proposals as such; they do not become instructions. Do not copy a project encyclopedia, code walkthrough, or complete work log into guidance.

For recurring problems, first determine whether the cause is information, tool capability, task understanding, execution behavior, or the existing rules themselves, then choose where to improve. Not every failure calls for a more detailed prompt, and not every correction should become a permanent prohibition. Hard restrictions for known mistakes should have specific reasons and conditions of applicability, without expanding into obligations for unrelated tasks. Necessary security and authorization boundaries do not need to wait for an incident before being established.

Prefer revising, merging, and replacing existing wording to continually appending patches. Delete or rewrite rules confirmed to be obsolete. When a developer-confirmed constraint needs to change, obtain the relevant authorization rather than relaxing boundaries on your own in the name of self-improvement. Updates are meant to reduce misunderstandings and repeated explanations, not to expand the agent's authority to make its own rules.

## Revise instead of accumulating patches

Use natural language to explain the expected approach, applicable conditions, and necessary reasons. Do not mechanically convert them into fixed thresholds or command checklists for the sake of being "agent-readable." Prioritize useful ways forward, while stating explicit prohibitions directly where needed. Reminders about mistakes should inform the current choice, not require a full audit or an inventory of every rejected alternative for each change. Do not turn a one-off correction into a case study that every task must begin by reading.

Subject new rules to the same scrutiny as new code: what problem do they address, what will they make the agent do more or less of, are they worth the ongoing attention, and is there a more direct solution? Changes with unverified effects are attempts to be evaluated, not guarantees of quality. You can use existing tasks and tools for bounded, reversible trials, paying attention to quality, interaction burden, and added costs. Do not claim consistent improvement without a reliable comparison, and do not build a complete evaluation system as a prerequisite for every adjustment.

Bring shared changes back to the Kit repository, including index changes, trimming, and merges. Update the entry and core together; preserve adopting projects' own content. If project experience recurs elsewhere, identify the shared conditions and inspect counterexamples before generalizing. A second occurrence is a reason to investigate, not proof of universal applicability. Persistent conflicts between project supplements and core may call for revising core rather than adding another patch.

## Use bounded trials to locate the problem

Record a task, observed behavior, and effect only when it can inform a reusable judgment. Distinguish content not obtained, content obtained but unhelpful, and a reasonable judgment blocked by tools or external dependencies. Reading self-reports are clues; available loading and tool records give stronger evidence of acquisition, while task outcomes show whether it helped.

During a trial, a temporary one-line report of which Kit files were read may help diagnosis. Remove that request when its diagnostic value ends. If topic files repeatedly need to be assigned manually, inspect the entry and actual loading path before adding more prose. Use native path rules, explicit invocation, or Skill packaging only when the primary tool's capabilities and an observed problem justify it.

If verification output repeatedly overwhelms context, a focused project script may preserve overall status, failure detail, and the full log location. If module-specific constraints need separate maintenance, test when the primary tool acquires module instructions before relying on that placement. Required pre-action boundaries must remain available meanwhile. These are responses to observed problems, not adoption requirements.

## Why useful constraints have to earn their place

The Kit is not a project encyclopedia, code index, work log, or archive of every conversation. Preserve the reasons and boundaries needed for judgment, not the entire discussion. Do not separately maintain knowledge that can be recovered directly from code, tests, or existing documentation. Judge whether a record is worth keeping by whether its absence would lead to repeated misunderstanding, significant risk, or substantial reinvestigation.

The Kit and its individual files are tools that can be modified, replaced, and pared back. When the same problem keeps requiring reminders, explanations, and rescue work from the maintainer, reassess whether the changes are helping rather than indefinitely writing off the cost as part of learning to work together. Keep conventions that provide real help. Do not continue maintaining mechanisms without commensurate benefits merely because effort has already been invested or the system looks complete.
