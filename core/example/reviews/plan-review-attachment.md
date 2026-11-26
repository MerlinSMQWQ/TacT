### Attached review document

# TacT 迭代计划评审

对照 Kit 现有内容（`0.1.3`，commit `6cb61ef`）逐项审查后，以下是我认为需要注意的问题，按严重程度排列。

---

## 一、结构性问题

### 1. "Adjustable strong defaults" 和现有 AGENTS.md 职能重叠，定位需要更加明确

计划在 AGENTS.md 中新增 `## Adjustable strong defaults` 章节，包含 6 条条目。但对照现有内容：

| 新条目                                       | 现有覆盖                                                                 |
| -------------------------------------------- | ------------------------------------------------------------------------ |
| Honor existing agreements                    | `Read project constraints before acting` 已涵盖                        |
| Discuss consequential unknowns with evidence | `Boundaries and authority` 段落 + `collaboration.md` 的 intervene 段 |
| Re-align on drift                            | `working.md` 的 "retire a plan" + `collaboration.md` 的 intervene    |
| Protect agreed participation                 | `collaboration.md` 的 "human control" + "observe and intervene"        |
| Keep communication direct and readable       | `communication.md` 大部分已覆盖                                        |
| Report grounded results                      | `Boundaries and authority` 的 truthful reporting + `verification.md` |

**问题**：这 6 条是对已有指引的**摘要/升级**，不是新增行为。如果不清楚它们和现有段落的关系（是替代、提取、还是增加约束力），Agent 执行时会面临"这段和那段说的是同一件事但措辞不同"的歧义，增加阅读负担而非减少。

> [!IMPORTANT]
> **建议**：明确每条 strong default 是**从哪个现有段落提取**的精炼表述，以及提升为 strong default 后原段落是否保留原状。考虑在 strong defaults 章节开头加一句说明，比如 "These distill the most frequently needed judgments from the topic files; the full reasoning remains in those files."

### 2. 五层优先级体系可能过度工程化

计划引入了 5 级裁决顺序：硬边界 → 任务约定 → 项目覆盖 → 可调强约束 → 软原则。当前 Kit 的层级其实只有 3 层（硬边界 → 项目层覆盖 → 日常判断原则），已经在 `AGENTS.md` 和 `project/README.md` 中一致表述。

**问题**：

- "任务约定"和"项目覆盖"之间的优先级在实践中很难分清。如果对话中约定了某事，然后 `project/notes.md` 有不同说法，Agent 需要裁决——但这种冲突本身就说明有人忘了同步，优先级规则帮不了忙。
- "可调强约束"夹在项目层和软原则之间，位置尴尬。如果项目层可以覆盖它，它比项目层弱；如果不能，它就是变相的硬边界。

> [!TIP]
> **建议**：保持现有 3 层结构，把 strong defaults 定位为 **"日常判断原则中的高优先子集"**，而非独立的第 4 层。任务约定不需要排入层级——它本身就是开发者当场行使授权的行为，天然高于项目层记录。

---

## 二、落地细节问题

### 3. `collaboration.md` 中约定的通过 5 维度判断表来确定步长有成为必填模板的风险

计划要求嵌入一个 **5 维度判断表**（目标与内聚、依赖与完整性、变化原因、当前不确定性、理解与参与）。计划自己也注了"不把 5 维度写成必填表单"，但问题是：

- 现有 `collaboration.md` 的 `Establish enough shared understanding` 段落风格完全是**叙述+举例**，突然嵌入一个维度表会改变文件的调性。
- Agent 对结构化列表有很强的"逐项填写"倾向，即使你说了不要求填写，表格的存在本身就是压力。

> [!WARNING]
> **建议**：用叙述体描述步长判断的考量因素，把维度作为行内举例而非表格呈现。或者把表格放在一个具体的示例场景中（"例如在判断是否合并两步时，可以考虑……"），而不是作为独立的结构化节。

### 4. `communication.md` 的反模式条目与现有段落大量重叠

计划 0.3 中的 7 条表达约束，对照 `communication.md` 现有内容：

- "结论前置" → 已有："lead with the best-supported judgment"
- "单次聚焦当前决策" → 已有："Answer the current question directly"
- "给出合理默认方案" → 已有："offer a recommendation when supported"
- "禁用格言体" → 已有："do not perform enthusiasm"、"natural, complete, familiar language"
- "按需解释" → 已有："do not reteach familiar basics"
- "同步吸收纠正" → 已有："incorporate the confirmed correction and continue"
- "无元输出" → 已有："without producing a separate language self-review or compliance report"

**问题**：绝大部分不是新增行为，而是用中文技术协作视角重新措辞。如果以"合并进 `Make the explanation understandable`"的方式落地，这个段落会膨胀很多，但增加的指导价值有限。

> [!TIP]
> **建议**：只合并现有段落确实没有覆盖到的具体场景（比如"否定排比"这个反模式确实比现有措辞更具体），对于已有覆盖的条目，考虑**修订现有措辞使其更精确**，而不是追加一组平行描述。

### 5. `core/README.md` 中明确 Pi 为验收环境是否合适？

计划要求在 `Set up a project` 中明确"本轮运行与验收环境为 Pi"。但 `core/README.md` 是**共享文件**，属于 Kit 仓库，所有采用项目都会收到。

**问题**：Pi 是你的当前宿主，不是所有 TacT 用户的宿主。把它写进 `core/README.md` 意味着每个 `tact init` 的项目都会看到"验收环境为 Pi"，这不合理。

> [!CAUTION]
> **建议**：Pi 验收环境的声明应该只出现在 `project/notes.md` 和 `project/verification.md`（计划中也有这两处，是对的）。`core/README.md` 保持宿主无关，最多说 "verify loading in your host environment" 这类通用表述。计划对 `core/README.md` 的修改应限于淡化 Codex 专属操作（这是对的）和说明 strong defaults 机制（也是对的），但不要加入 Pi 特定内容。

### 6. `README.md`（仓库根）中提及 Pi 同理

仓库根 `README.md` 面向的是所有 TacT 的潜在用户和贡献者。把"Pi 为当前运行与验收环境"写入 README 同样不合适，这是项目层的信息。

---

## 三、流程与验证问题

### 7. 阶段 2 和阶段 3 之间缺少明确的"规则冻结"节点

阶段 2 是打包回归验证，阶段 3 是 Pi 实测。但计划没有明确：从阶段 3 实测中发现的问题，应该怎样回流到阶段 1 的规则？如果 3.4 的复盘结论是"某条 strong default 需要修改"，整个循环是 3→1→2→3 还是 3→4？

**建议**：在阶段 3 和阶段 4 之间加入明确的要求：复盘结论如果涉及 core 规则的实质修改，回到阶段 1 的相应条目修订，然后只需重跑阶段 2 的测试（不需要完整重做阶段 3 的实验），再进入阶段 4。

### 8. 阶段 3.1 的"三层加载核对"很好，但缺少失败处理

计划要求分别核对入口发现、文档读取、行为影响——这个分层很精确。但如果第 1 层（入口发现）就失败了，计划只说"记录并按需适配入口"，没有说什么程度的适配是允许的。

如果 Pi 不加载根 `AGENTS.md` 的 `<!-- tact:begin -->` 块也不加载 `.agents/skills/tact/SKILL.md`，那么需要的可能是一个新的入口路径——这可能涉及新增文件或修改现有文件的结构，超出了"不为每个主题单独拆分 Skill"的范围边界。

**建议**：补充一条判断标准：如果 Pi 的入口发现需要的适配仅限于调整现有入口文件的位置或格式（如把 skill 路径改到 Pi 识别的位置），则在阶段 3 内处理；如果需要根本性的新机制（如新增配置文件、改变 Kit 结构），则升级为范围变更讨论。

### 9. 阶段 3.4 的复盘表格缺少"阅读负担"维度

复盘表格列了 5 个观察问题，都聚焦于新增机制是否有效。但本轮最大的风险在于**入口文件膨胀后 Agent 的阅读和遵守成本是否合理相称**。

现在 `AGENTS.md` 是 54 行。加入 strong defaults 章节后估计会到 70-80 行。对于每次对话都要读的入口文件来说，这个增长是否合理，需要观察和评价它是否为 Agent 带来了相应的行为改善。

**建议**：在复盘表中加一个维度："入口文件内容增加后，Agent 是否仍能在首次读取时形成正确的工作判断，还是出现了忽略或机械遵守的倾向？"

---

## 四、值得肯定的设计

以下几点设计在我看来是正确的，不需要修改：

1. **阶段 0 中"运行时 Kit 保持纯英文"的原则** — 避免了中英混杂的阅读负担。
2. **"合并修订现有章节"而非追加新段落** — 和 `evolving.md` 中的原则一致。
3. **阶段 3.2 选择较大规模重构实验** — 比执行小规模的实验更能暴露步长协作的真实问题。
4. **"只记录实际发生的讨论，未出现的事件不补写"** — 直接回应了 Agent 编造复盘的倾向。
5. **范围边界（明确不做）** — 清晰且务实。
6. **不修改 `delegation.md`、`tools.md`、`verification.md`** — 范围控制得当。

---

## 总结

最主要的 3 个问题：

1. **Strong defaults 和现有指引的关系不清** — 需要明确它们是摘要提取还是新增约束，否则会造成重复和歧义。
2. **5 层优先级过度工程化** — 建议简化为 3 层 + "高优先子集"。
3. **Pi 特定内容不应进入共享文件** — `core/README.md` 和根 `README.md` 中的 Pi 引用应移至项目层。

其他问题（步长表格调性、communication 重叠、复盘维度缺失）是优化项，不阻塞但值得考虑。
