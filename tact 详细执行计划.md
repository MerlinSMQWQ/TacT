# TacT 步长协作迭代详细执行计划

* **基准版本**：TacT `0.1.3`（commit `6cb61ef`）
* **规划来源**：`TacT 步长协作迭代计划.md`
* **运行与验收环境**：Pi
* **核心目标**：以“步长（Step Size）”为核心，将讨论、执行、表达约束与改动汇报组织为可持续推进的人机协作机制；引入可调整的预设强约束；在不扩张架构边界的前提下，通过一次较大规模的项目重构实验（覆盖从可信性验证、需求分析到测试等大部分 Agent 可参与的软件工程阶段）在 Pi 中完成真实开发场景下的验证与收敛。
* **范围边界（明确不做）**：不建监控平台、不建完整评测框架、不做跨宿主兼容层、不为每个主题单独拆分 Skill、不新增必须填写的项目配置文件。

---

## 阶段 0：核心机制与规则基准

运行时 Kit 文档（`AGENTS.md`、`core/*.md`、`project/README.md`）保持纯英文；中文计划文档留在运行时 Kit 之外。所有新增规则以“合并修订现有章节”的方式落地，保留既有理由、适用条件与反例。

### 0.1 规则层级与冲突裁决顺序

从高到低依次生效，需在 `AGENTS.md` 和 `project/README.md` 中保持一致口径：

1. **硬边界（Hard boundaries）**：功能正确性、安全、授权、数据完整性、真实汇报。具体性或项目层补充均不得放宽。
2. **当前任务明确约定（Explicit task agreements）**：对话中双方就本步目标、范围、参与点、验证范围达成的确认。
3. **项目层覆盖（Project overrides）**：`.tact/project/notes.md` 及匹配的 `project/<topic>.md` 中经确认的调整。
4. **可调整的预设强约束（Adjustable strong defaults）**：采用后默认必须遵守；Agent 可建议修改，但不得自行将仍适用的强约束降级为可选建议。
5. **日常软原则（Principles for everyday judgment）**：按任务情境权衡使用。

### 0.2 预设强约束（6 条核心条目，英文落地参考）

在 `AGENTS.md` 中作为独立章节 `## Adjustable strong defaults` 呈现，直接内联最关键的协作、表达与汇报底线，降低“未主动翻阅主题文件导致基本盘跑偏”的风险：

~~~markdown
## Adjustable strong defaults

These defaults define the Kit's standard step-based collaboration. Follow them once adopted; you may propose changes, but do not silently downgrade an active default to optional advice. The developer may adjust or override them for a project in `project/notes.md` (or matching `project/<topic>.md`) or for the current task in conversation.

- **Honor existing agreements**: Reuse confirmed goals, scope, authorization, and prior feedback; do not ask for repeated confirmation.
- **Discuss consequential unknowns with evidence**: When an open question affects the step's goal or behavior, complete the investigation you can do first, then bring facts, a recommendation, and the specific decision before acting on dependent work.
- **Re-align on drift**: When a key assumption fails or the next move will significantly expand scope, change behavior, or add maintenance cost, state the finding, its impact, and options before proceeding.
- **Protect agreed participation**: When the developer asks to understand, design, or work through part of a task, build that into the step instead of running past the agreed checkpoint.
- **Keep communication direct and readable**: Lead with the conclusion or next action. Avoid rhetorical padding, unnecessary negation ("not A, not B, but C"), and repeating shared context. Distinguish facts, assumptions, and recommendations, and carry style corrections forward.
- **Report grounded results**: State actual changes, completion status, and key verification evidence; keep unresolved gaps and next-step trade-offs visible.
~~~

### 0.3 表达约束裁剪边界（Humanizer + 工程对话反模式）

面向中文与英文技术协作场景，合并进 `core/communication.md`（不照搬英文禁用词表或散文润色流程）：

* **必须纳入的行为约束**：
  * **结论前置，少用否定铺垫**：直接说明判断或下一步动作（“建议做 X”），避免习惯性使用“不是 A，也不是 B，而是 C”的否定排比。
  * **单次聚焦当前决策**：讨论需要收敛时，只抛出当前必须拍板的问题，禁止先列出一串彼此嵌套的假设清单再声明“我们先只看第 1 题”。
  * **给出合理默认方案，不抠字眼**：优先基于上下文给出可微调的默认做法，不将日常指令拆解成细碎的语义辨析题。
  * **禁用格言体、对仗与翻译腔**：用常规、准确的技术动词说清对象、动作与后果；禁用拔高意义的空话、模糊归因、凑字数过渡语和生硬书面直译。
  * **按需解释陌生概念，不重复已共享背景**：引入重要陌生术语时结合当前任务说明含义与作用；已确认的前提直接沿用，不再复述。
  * **同步吸收表达纠正**：当使用者指出不理解或表达不合适时，调整解释方式，检查误解是否影响当前方案，并将风格调整带入后续交流。
  * **无元输出**：直接输出符合要求的回应，不附带改写草稿或语言合规自检报告。
* **许可处理**：完全以自有英文工程表述重写时无需额外声明；若直接复制或改编 Humanizer 上游原文段落，须按其 MIT 许可保留所需声明。

---

## 阶段 1：逐文件改动规格（File-by-File Spec）

改动原则：**以现有章节为基础合并修订，保留原有理由、适用条件和反例，不逐文件追加重复段落**。

| 目标文件 | 改动位置与具体内容 | 保留项 / 禁区 |
| --- | --- | --- |
| **`AGENTS.md`** | 1. 在 `Boundaries and authority` 后新增 `## Adjustable strong defaults`，写入修改权说明与 0.2 中的 6 条强约束。<br>2. 在 `Read project constraints before acting` 中更新优先级描述，明确任务约定与项目层可调整强约束，但不能放宽硬边界。<br>3. 在 `When to read what` 索引中为 `collaboration.md`（步长确定与参与点）、`working.md`（单步推进与共同思考）、`communication.md`（改动汇报与表达纠正）补入具体触发词。 | 保留底部 `<!-- tact:begin -->` 块不变；不把整篇 `core/communication.md` 塞进入口。 |
| **`core/collaboration.md`** | 1. 在 `Establish enough shared understanding` 之后合并/新增 **Step size（步长）** 小节：定义步长（非工具调用数、行数、提交数或耗时），嵌入 5 维度判断表（目标与内聚、依赖与完整性、变化原因、当前不确定性、理解与参与），说明何时缩小或合并。<br>2. 在 `Observe and intervene where judgment matters` 中明确 **重新检查约定的 4 个触发条件**（关键假设失效或结果明显偏离、显著扩范围/改行为/增维护负担、需领域人员提供信息与取舍、使用者提出参与需求或指出解释妨碍判断）。<br>3. 明确：Agent 发出建议不等于已确认；等待答复时继续推进无依赖工作；不设统一每步审批。<br>4. 放入精简的英文讨论示例（如配置文件缺失时先给建议与理由，遇使用者不了解来源时先查调用链）。 | 保留 `Why human control is part of delivery quality` 原文理由；不把 5 维度写成必填表单。 |
| **`core/communication.md`** | 1. 在 `Make the explanation understandable` 中整合 0.3 的 **反 GPT 味 + Humanizer 裁剪规则**，并补充“用户指出不理解或表达不合适时，调整解释并检查误解是否影响当前方案”。<br>2. 将工程汇报段落收束为按需选用的 4 要素（实际变化、重要选择、验证依据、后续影响），明确“测试通过”需说明覆盖的行为，未运行/失败/受阻分别报告，并附简短英文汇报示例。<br>3. 合并与既有段落（如不重复否定无关选项、回答完即停、不输出自检报告）重叠的表述。 | 保留 `Preserve decisions in comments` 和 `Why qualifications need selection` 原文；不使用生硬英文禁用词表。 |
| **`core/working.md`** | 1. 在 `Prepare enough to act and preserve useful work` 或 `Let the outcome guide the path` 中补充 **单步内部推进**：明确“小”指减少同时依赖的未确认假设，优先用直接、范围清楚的动作尽早取得可检查结果。<br>2. 明确 **连续调查 vs 共同思考** 的分工：能自行查清的事实不反复提问；复杂问题连续调查时，说明当前未决问题、它影响的选择和下一步要取的证据。 | 保留“鉴别诊断”、“意外状态处理”和“退役失效计划”原文；不设固定行数/时间/工具数上限。 |
| **`core/complexity.md`** | 在 `Keep the business flow readable` 末尾补一小段衔接：说明内聚、变化原因和依赖关系如何辅助判断协作步长，同时注明代码职责与协作步长不是机械的一一对应，指向 `collaboration.md`。 | 其余内容不动。 |
| **`core/evolving.md`** | 在 `Use bounded trials to locate the problem` 中补充：试用复盘只记录真实发生的讨论、偏差、反馈与结果，未出现的事件不补写；不单凭日志中提到某条原则就断定其产生了效果。 | 其余内容不动。 |
| **`core/README.md`** | 1. 在 `Set up a project` 中明确本轮运行与验收环境为 **Pi**（保留不同宿主需各自验证加载的通用说明，淡化 Codex 专属操作）。<br>2. 在 `Work with the Kit` 中说明入口包含可调整的预设强约束，通过 `.tact/project/notes.md` 或任务讨论即可调整，无需新增配置文件。 | 保留 `init`/`refresh` 流程和 `Why the Kit preserves reasoning`。 |
| **`project/README.md`** | 在 `Add a topic file when needed` 中将 `change soft defaults` 同步更新为覆盖 `adjustable strong defaults and soft defaults`。 | 其余内容不动。 |
| **`README.md`** | 1. 简明补充步长协作和可调整预设强约束的理念。<br>2. 在 Skill 与采用说明中明确 Pi 为当前运行与验收环境，更新相关表述。 | 保留安装、构建、发版流程不变。 |
| **`project/notes.md`** | 补充本轮确认范围：Pi 为本轮运行与验收环境；保留既有不扩张边界（不建监控平台、完整评测框架、跨宿主兼容系统、按主题拆分 Skill）。 | 保留已有历史记录。 |
| **`project/verification.md`** | 补充 Pi 验收口径：需分别核对 Pi 的入口发现、实际读取 `.tact/AGENTS.md` 与主题文件、以及对任务行为的影响；Codex 加载结果不替代 Pi 验证。 | 保留既有 CLI 与打包检查要求。 |

**本轮明确不修改的文件**：`core/delegation.md`、`core/tools.md`、`core/verification.md`、`skills/tact/SKILL.md`（待阶段 3 在 Pi 实测发现路径后，仅在确有必要时适配）。

**阶段 1 完成条件**：新增要求的适用情况与行为清楚；使用者可通过现有项目补充或任务讨论调整预设强约束；普通工具操作不会自动变为人工审批点；原有理由和适用条件完整保留。

---

## 阶段 2：本地打包与 CLI 回归验证

在投入真实项目试用前，先确认打包和 CLI 行为未回归：

1. **文档链接与纯英文检查**：核对 `AGENTS.md` 与 `core/` 内所有相对路径链接可解析，运行时 Kit 无中文残留，原有理由和反例未被误删。
2. **重装并运行单元测试**（刷新 Hatchling 打包的 `tact_resources` 快照）：
   ~~~sh
   uv run --reinstall-package tact-agent-kit python -m unittest discover -s tests -v
   ~~~
   确认 `init`、`refresh`、冲突保护、dry-run 和项目笔记保留测试全部通过。
3. **源码目录外打包验收**：
   ~~~sh
   uv build
   ~~~
   在独立目录或隔离环境中安装生成的 wheel，验证打包结果包含更新后的共享指引，且排除了源仓库自身的 `project/notes.md` 与 `project/verification.md`。

---

## 阶段 3：Pi 加载核对与项目重构实验闭环

### 3.1 环境初始化与 Pi 三层加载核对

* 在选定的重构项目仓库中执行 `tact init`（或已有安装时执行 `tact refresh`）。
* 记录实验基线元信息：**Pi 版本号、所用模型及配置、重构项目代码起点 commit、TacT 候选 commit**。
* 在 Pi 中先跑一次最小探针任务，利用 Pi 会话记录与事件流，**分别确认三件事**（不合并为“已加载”）：
  1. **入口被发现**：Pi 确实加载了根目录 `AGENTS.md` 的 TacT 块和/或 `.agents/skills/tact/SKILL.md`。（若 Pi 的发现路径与现有入口存在差异，在此记录并按需适配入口。）
  2. **文档被读取**：Agent 在执行实质工作前实际读取了 `.tact/AGENTS.md`、`.tact/project/notes.md` 及当前任务触发的 `core/<topic>.md`。
  3. **行为受影响**：后续输出与协作动作实际体现了步长讨论、预设强约束与表达要求。

### 3.2 实验定位：较大规模的项目重构实验

* **实验范围**：由使用者选定一个较大规模的实际项目进行重构实验，覆盖从**可信性验证、需求分析、架构/方案设计、代码重构实现，一直到测试验证**等几乎全部 Agent 可参与的软件工程阶段。
* **实验目的**：相较于单一局部小任务，通过覆盖完整开发生命周期的真实重构工作，更贴近日常实际开发节奏，从而获取更明确、更真实的协作反馈，检验步长协作与语言约束在不同工程阶段（如探索验证 vs 需求收敛 vs 编码重构 vs 测试验收）的适应性。
* **项目层记录**：在试用项目的 `.tact/project/notes.md` 中简短记录本次重构的目标、阶段划分、使用者的参与/学习偏好，以及对预设强约束的任何项目级调整。

### 3.3 过程执行与留痕

* 随重构阶段推进动态商定并调整步长（例如：可信性验证阶段以快速取得验证证据为一步，需求分析阶段以收敛关键业务边界为一步，重构与测试阶段以可独立验证的行为模块为一步）。
* 过程记录优先利用 Pi 的会话记录，按需导出事件流，关联关键人工反馈、阶段交接、代码改动与检查结果。
* 只记录实际发生的讨论、理解偏差、暂停恢复与汇报；未出现的事件不补写为已发生。

### 3.4 试用复盘

实验完成（或达成阶段性里程碑/明确受阻）后，围绕真实过程片段，对每条候选规则做出 **保留 / 修改 / 移除** 判断：

| 观察问题 | 对照使用的过程材料 |
| --- | --- |
| 步长是否帮助判断当前工作（含跨阶段切换） | 各阶段的起始讨论、范围调整、阶段交接与对应结果。 |
| 共同思考是否改变后续行动 | 人的反馈及其引发的方案、需求、代码或测试变化。 |
| 语言要求是否帮助讨论继续 | 需要追问的表达、GPT 味是否减少、纠正后是否带入后续回应。 |
| 汇报是否支持核对和接续 | 汇报内容、实现定位、检查结果及自然暂停后的上下文恢复过程。 |
| 新增约定是否值得 | 实际重构成果，以及阅读、讨论、等待、纠正和恢复上下文所需的综合投入。 |

---

## 阶段 4：收敛回写与发布准备

### 4.1 分层回写

* 将复盘验证有效的通用经验回写并收敛到 `AGENTS.md` 和 `core/*.md`。
* 仅属于本次重构项目的特有约定保留在试用项目的 `.tact/project/notes.md`。
* 对增加负担而未体现价值的条目进行修改或移除。

### 4.2 发版前验收

* 确认文档引用、源文件与打包资源一致，且与试用结论一致。
* 在源码目录外使用最终构建的 wheel 验证：
  * `tact init` 生成的入口和指引能被 Pi 正常发现与读取。
  * `tact refresh` 更新已有项目后，Pi 能读取更新内容，且项目补充（`.tact/project/notes.md` 等）与覆盖保护行为完好。
  * CLI 写入成功与 Pi 实际读取分别核对并记录。

### 4.3 版本号与发布

* 根据最终改动确定版本号与发布日期，更新 `pyproject.toml` 与 `uv.lock`。
* 提交最终改动，打匹配的 `v` tag 并发布 GitHub Release，由 GitHub Actions 通过 PyPI Trusted Publishing 完成构建、测试与发布。
* 发布后通过 `uv tool install --reinstall tact-agent-kit` 验证 PyPI 安装可用。