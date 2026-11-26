## Exchange 1

### User

帮我看看，现在如果 Agent 自己要更改规则，他能更改 core 的规则吗？还是说只能更改项目内的规则

### Assistant

好，我已经读完了所有相关文件，现在可以给你一个清晰的回答了。

**Agent 不能直接更改 `core/` 的规则，只能更改 `project/` 层的内容。** 但这个限制不是绝对的 — 有一条明确的路径让 core 的改动最终发生。具体来说：

### 1. `core/` 属于 Kit 仓库，Agent 不能直接修改

关键出处来自多个文件的一致表述：

- [core/README.md](file:///Users/a1234/WorkingSpace/TacT/.tact/core/README.md#L34) — *"The entry carries shared boundaries… `core/` belongs to the Kit; `project/` belongs to the adopting project."*
- [core/README.md](file:///Users/a1234/WorkingSpace/TacT/.tact/core/README.md#L51) — *"Make shared changes, including trimming and index changes, in the Kit repository. Adopting projects should not patch their shared copy."*
- [project/README.md](file:///Users/a1234/WorkingSpace/TacT/.tact/project/README.md#L37) — *"Record proposed shared changes in the project layer and take them to the Kit repository. An agent may edit guidance only within its actual responsibility and authorization."*

### 2. Agent 可以在 `project/` 层做的事

- 自由编辑 `project/notes.md` — 记录确认的约束、工作模式、观察和假设。
- 创建 `project/<topic>.md` 补充文件 — 如果是 core 所包含的内容的同名主题，可以在 `project/<topic>.md` 里面做**局部调整**（只覆盖它明确提到的部分，core 其余内容仍然有效）。
- 但即便是项目层的调整，也有限制：项目规则可以让约束范围更加精细或调整可修改的默认值，但不能仅凭"更具体"就践踏 core 中确定的底线。

### 3. Agent 想改 core 怎么办？只能走提议路径

[evolving.md](file:///Users/a1234/WorkingSpace/TacT/.tact/core/evolving.md#L19) 和 [project/README.md](file:///Users/a1234/WorkingSpace/TacT/.tact/project/README.md#L37) 描述的流程是：

1. Agent 在 **项目层** 记录提议（proposed shared changes）
2. 将提议**带回 Kit 仓库**（即 TacT 源仓库）处理
3. 如果需要改开发者确认过的约束，要**获得相应授权**，不能以"自我改进"的名义自行改动已经确定的原则与约束。

[delegation.md](file:///Users/a1234/WorkingSpace/TacT/.tact/core/delegation.md#L37) 进一步明确：一个只读调查者或没有编辑授权的 Agent，应该把提议传递给它的直接委托方，而不是自己直接改。**Agent 之间达成一致后更需要开发者确认这个变更。**

设计意图很清楚：core 是**共享的、版本化的**，属于 Kit 仓库；Agent 在采用项目里直接改 core 等于"patch 自己的共享副本"，会导致后续更新冲突和版本漂移。所以改动路径是提议 → Kit 仓库 → 统一更新到各采用项目。

### What this demonstrates

The developer asks who can change a rule. The reply names the agent, the files it can edit in an adopting project, and the route for proposing a shared change. That context matters because the same person might also maintain the Kit itself. The file references let the reader check the answer. Naming the developer as the person who confirms a change also explains what still has to happen after two agents agree. Firm wording fits a question about authority.
