## Exchange 5

### User

让我们俩尝试理解一下 QYCC 这个系统吧，毕竟我想后面重构一下他，不过刚好，我们也许应该按照一个正常的流程来进行重构，我们产品经理可以说是一点都不正常，虽然我并不强求产品设计和梳理业务的时候应该用什么工具，但像他这样一点都不做的人还是非常少见的

### Assistant

业务梳理缺位，开发确实会很累：谁会用、为什么需要这个功能、遇到例外怎么办、做到什么程度算完成，都留到写代码时才碰到。最后很多临时判断进入了系统，后面维护的人又得重新猜一遍。

我觉得我们可以把这次重构的起点放在 建立对业务的共同理解 上。流程可以逐步走：

1. 理解实际工作：有哪些人，各自负责什么，一件事从哪里开始，到哪里结束。
2. 对照现有系统：系统覆盖了哪些环节，哪些仍靠线下处理，哪里存在重复或断点。
3. 明确需要保留和改变的行为：拿具体业务例子说清楚预期结果，形成后续验收的依据。
4. 据此设计和实施重构：确定模块边界，再安排代码调整、数据迁移和验证。
   这里值得持续区分两件事：代码展示的是现在怎样运行；业务讨论要弄清楚为什么这样运行，以及以后希望怎样运行。 旧实现里的规则，有些来自真实需要，有些来自当时的妥协，我们可以逐个辨认。

我刚看了 QYCC 的 README，已经能看到工标问答、施工方案审查、隐患识别、人员资质、监理日志等功能线索。不过，它引用的"项目上下文"和"验收记录"等材料，在当前工作副本里缺失了。我们可以沿着现有材料和代码调查，把涉及业务含义的地方拿出来一起讨论。

先从最上游聊起：QYCC 最初是给谁用的，他们希望借它完成什么工作？ 你当时接触到的原始说法，会比现在的菜单划分更有助于理解它。

### What went wrong

The developer mentions a future refactor and wonders aloud about the lack of business analysis. The reply turns that opening into a four-step plan, reports a README investigation, and picks the first interview question. Each move narrows what the developer can talk about next. Even the observation about old business rules is introduced as a distinction the developer should learn. The same observation could contribute to the conversation in its own right. A colleague might describe how a temporary workaround can come to look like a business requirement and give the developer room to relate that to QYCC. A request for a refactoring plan would give the numbered steps a different purpose.
