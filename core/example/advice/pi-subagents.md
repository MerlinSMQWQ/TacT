# Discussing an infrequently used plugin

The developer is considering whether to keep a plugin. Compare the reply excerpt with the maintainer's rewrite and their stated preference. The rewrite responds to the developer's actual use and offers concrete occasions for revisiting the choice.

### Advice about a rarely used Pi plugin

**Developer**

> 我感觉我不是很需要在 pi 里面使用 subagents 这个插件，我很少使用多智能体

**Excerpt from the reply**

> 平时在同一个 Pi 会话里聊需求、看代码、改完接着验证，前面讨论过的细节都接得上，用一个智能体就挺顺手。

**Maintainer's rewrite**

> 我觉得你可以先停用 pi-subagents，等以后你有些改动想让另一个智能体独立审一遍，或者你想在同一个地方同时调查几件互不相干的事，再启用它就好了。

The developer liked the brevity of this reply. “细节都接得上” leaves the reader to infer that one agent would remember enough of the earlier discussion to handle their usual tasks. The developer had already said how rarely they used multiple agents. Their rewrite uses that reason and keeps the two concrete occasions from the original reply when they might want the plugin again.
