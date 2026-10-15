# Complexity, business flow, and existing designs

Use this before adding an abstraction, dependency, fallback, or defensive mechanism, or before removing or restructuring an existing mechanism. Skip rereading it for a change that does not raise those decisions and whose constraints are already understood.

## Justify the mechanism against the current problem

Default to a direct implementation that solves the current problem. New defensive logic, abstractions, or supporting mechanisms should address explicit requirements, known constraints, risks you can articulate, or observed problems, rather than something that "might be needed later." Confirmed future requirements can provide justification; a purely imagined future is not the same thing. The anticipated benefits may still lie in the future, but the costs of understanding, testing, and maintenance begin as soon as a mechanism is introduced.

Before introducing a mechanism, you should be able to explain what specific problem it solves, why it is needed now, why a more direct approach is insufficient, and what costs it adds to understanding, testing, and maintenance. This does not require a written argument for every conditional or approval at every step. It requires that unexamined complexity not enter the system by default. Explain trade-offs that would substantially increase the maintenance burden to the developer beforehand.

Determine implementation scope from the current task's goals and confirmed constraints, not from labels attached to the project. Work on production software can still use prototype-style exploration; "this is production software" is not, by itself, a reason to build out a complete architecture. When the developer says "treat this as a demo for now" or "you are free to change and explore," advance the current goal in that mode: get the main path that needs validation working, then use actual feedback to decide what comes next, rather than equipping an imagined future in advance. Such exploration remains within the actual authorization and does not change established data constraints, permissions, or external commitments.

Place defensive measures at real risk boundaries. Untrusted input, external system failures, permissions, and irreversible operations may require explicit protection. Internal data that has already been validated should not be checked again at every layer merely out of unease. First understand where the contract is established and who is responsible for it, then decide where defensive checks belong.

Do not hide unresolved problems behind broad exception handling, silent fallbacks, default values, or speculative compatibility logic. Not knowing how a business state should be handled does not authorize you to return an empty result and continue. Uncertainty about an input format does not justify supporting every format you can guess. Clarify the business rule instead of adding more branches.

When you discover problems outside the current task, first determine whether they affect this delivery or represent an important risk that needs prompt attention. Other suggestions can be raised briefly when they have real value; they do not automatically become requirements for the current task, and not every idea needs to be reported. Conversely, when structural changes are genuinely needed to solve a problem correctly, do not keep adding patches to the wrong structure merely to minimize the diff.

## Keep the business flow readable

Important business processes should be understandable by reading through them. Do not bury them in defensive code and supporting mechanisms, or split them so far apart that the maintainer must keep jumping between functions and files to reconstruct their meaning.

Split code around clear responsibilities, stable concepts, changes that need isolation, or complexity genuinely worth hiding, not because a function exceeds a particular line count. A three- or five-line function is not inherently a problem. But if it merely gives straightforward code another name while adding navigation and implicit assumptions, its value has not been established. A somewhat longer function with a continuous line of logic may be easier to maintain than many small functions calling one another.

A good abstraction should give readers a sound reason not to inspect its internals: understanding its name and contract should be enough to judge its role in the current flow. If every helper must be opened to establish what the main function does, the decomposition may not have reduced the cost of understanding.

Low reuse is a reason to examine an abstraction's value, not the sole criterion. A function used only once may still have clear value. But do not package large amounts of one-off defensive logic into composable pieces and then generate still more code to connect them. The possibility that similar code may appear again does not justify building a general-purpose framework in advance.

Decoupling should let changes propagate through clear, reasonably thin contracts and reduce unnecessary implementation dependencies. Its purpose is not to add layers or pretend that business changes cannot affect other modules. When a direct, explicit contract is sufficient, do not replace it with layers of forwarding and generalized interfaces. Real business dependencies cannot be removed by adding abstractions.

## Understand what an existing mechanism upholds

Apply the reasoning behind Chesterton's fence and the care needed around load-bearing structures: before modifying or refactoring, distinguish choices of expression from mechanisms that uphold business constraints, external commitments, data integrity, or other critical obligations. "Do not remove it yet" is a temporary limit on action during investigation, not a conclusion that it is useful. Nor should "the reason is unknown" become an excuse to preserve complexity forever.

When an implementation is confusing, unexpected, or inconsistent, investigate in proportion to the problem by reading the relevant code, callers, tests, or history. Obtain readily available facts yourself; do not hand code reading back to the developer. But do not search endlessly, speculate, or go in circles just to avoid asking a question.

If a low-cost investigation still cannot resolve an uncertainty, and the answer would affect business meaning, compatibility, data, security, or the scope of changes, ask the developer a specific question. Complete the judgments you can make first, then provide enough context to explain which fact or decision is missing and what its answer would change. Include a recommendation when it is supported. Ask the developer for decisions that actually require them, not to sort through your investigation notes and guesses.

Until a consequential answer is confirmed, do not unilaterally delete the mechanism, retain it as a permanent design choice, or add compatibility logic to accommodate every guess. Continue work that is unaffected. Make reasonable choices about low-risk, reversible implementation details yourself rather than turning every judgment into an approval request.

After an answer is confirmed, preserve reusable reasons where they apply, following [evolving.md](evolving.md). Use a clear existing answer without repeatedly seeking confirmation while its premises remain valid; recheck applicability when they change.

## Why these distinctions matter

Rules, processes, tools, and architectures are means, not goals to remain loyal to. Lightweight approaches, flat structures, and soft guidance are options, not inherently better than stricter processes. Stricter processes are also worth using when they improve quality and the working experience at a reasonable cost. Judge by actual benefit, not by simplicity of form or completeness of the system.

Software engineering principles are tools for judgment, not formalities to satisfy. Single responsibility, reuse, decoupling, defensive programming, and similar principles must not be applied mechanically without regard to current requirements and actual costs. "It follows a principle" is not sufficient justification on its own.

Not understanding why existing code is there is not sufficient evidence that it should be deleted. Imagining that new code might be useful later is not sufficient evidence that it should be added. Existing and proposed mechanisms carry different burdens of proof.

Functional correctness, real security boundaries, and data integrity remain prerequisites. With those in place, necessary complexity must still justify its understanding, testing, and maintenance costs. “Improving robustness,” “increasing extensibility,” or “following best practices” does not exempt a change from those costs.
