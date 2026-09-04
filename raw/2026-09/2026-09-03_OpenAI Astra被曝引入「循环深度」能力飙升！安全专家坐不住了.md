---
title: OpenAI Astra被曝引入「循环深度」能力飙升！安全专家坐不住了
date: 2026-09-03
source: https://mp.weixin.qq.com/s?__biz=MzA3MzI4MjgzMw==&amp;mid=2651054414&amp;idx=2&amp;sn=e29b7c12fc5056bc5c62410551d98e82
account: 机器之心
fetched_at: 2026-09-04 18:00:05 CST
article_id: e29b7c12fc5056bc5c62410551d98e82
---

机器之心 2026-09-03 12:01 北京

  
  
*[图片]*

  
明天发布？

  
*[图片]*

编辑｜山辉

OpenAI 最强新模型 Astra，可能明天就要来了！

*[图片]*

这是 OpenAI 第一个达到「关键级」网络安全能力门槛的模型。

Astra 在纳入 2026 年 6 月至 8 月披露的 20 个 V8 高危漏洞的内部测试集上，取得了 100% 的任意代码执行成功率，而 GPT-5.6 Sol 的成功率仅为 20%，同时，Astra 使用的 Token 更少效率更高。

它还成功发现并利用了两个此前未知的零日漏洞，完成浏览器沙箱逃逸，并在加固操作系统中将权限从普通用户提升至 root。

OpenAI 甚至为它推迟了部分训练和发布工作。

但就在发布前夜，外界发现，Astra 可能还有一个更加神秘的变化。

据《The Information》报道，OpenAI 在 Astra 中使用了一种名为「循环深度」（recurrent depth）的技术。模型可以反复处理内部状态，在输出下一个 Token 之前，完成多轮不以文字形式出现的计算。

*[图片]*

OpenAI 的新推理技术让 AI 安全专家感到担忧，链接：[https://techcrunch.com/2026/09/02/openais-new-reasoning-technique-alarms-ai-safety-experts/](https://techcrunch.com/2026/09/02/openais-new-reasoning-technique-alarms-ai-safety-experts/)

对模型能力而言，这意味着「少说，多想」。

但是，更危险的失控风险也随之而来。一个可以独立发现零日漏洞的模型，真正的思考和行动计划都藏在人类无法读取的内部状态，人类真的还能监管住它吗？

第一个「关键级」模型

9 月 1 日，OpenAI 赶在 Astra 发布前，公开了一篇有关模型能力和安全措施的博客。

其中确认，Astra 已经达到 OpenAI 准备框架中的「关键级」网络安全能力门槛，也是第一个被 OpenAI 正式划入这一级别的模型。

按照 OpenAI 的定义，达到这一门槛意味着，模型在获得适当工具和访问权限后，可以在没有人类逐步指导的情况下，从大量经过加固的真实系统中寻找此前未知的安全漏洞，并开发相应的利用方式；或者只根据一个高层目标，自主设计和执行针对加固目标的端到端新型攻击策略。

在 OpenAI 用于评估已知漏洞利用能力的 ExploitBench 中，Astra 拿到了 100% 的成绩。

*[图片]*

在包含 20 个近期 V8 高危漏洞的内部测试中，Astra 取得 100% 的任意代码执行成功率，同时使用的输出 Token 明显少于 GPT-5.6 Sol。图源：OpenAI

但公开基准可能存在数据污染，OpenAI 又建立了一套内部测试集，纳入 2026 年 6 月至 8 月间披露的 20 个 V8 高危漏洞。结果显示，与 GPT-5.6 Sol 相比，Astra 使用了更少的输出 Token，却取得了高得多的任意代码执行成功率。

测试期间，它还发现了两个此前未知的零日漏洞，并将它们组合进一条完整的漏洞利用链。OpenAI 目前正在向相关维护者披露这两个漏洞。

在更接近真实环境的专家评估中，Astra 成功发现浏览器和操作系统中的未知漏洞。

它构造了一条完整的浏览器攻击链：浏览器只需打开一个 HTML 文件，模型便能逃出沙箱，在宿主机上执行命令。它还在一个经过加固的操作系统中发现多个漏洞，将它们组合起来，从普通用户权限一路提升到 root。

这些结果最终让 OpenAI 确认，Astra 已经跨过「关键级」门槛。

面对这样的模型，OpenAI 罕见地踩下了刹车。

过去几周，OpenAI 推迟了 Astra 的部分开发和发布工作，以便加强训练基础设施、网络隔离、权限控制和监控系统。模型发布后，普通用户也无法直接获得它最强的网络安全能力，相关功能最初只会提供给少量测试者，再通过 Daybreak Blue 逐步扩大防御用途。

*[图片]*

OpenAI 还根据此前的 Hugging Face 事件，专门测试了 Astra 是否会绕过审核机制，或者在困难任务中攻击与目标无关的「蜜罐」系统。GPT-5.6 Sol 曾在 5.3% 的样本中尝试绕过自动审核，并在 56% 的蜜罐测试中尝试攻击周边目标；Astra 在两项测试中都没有出现类似尝试。

这些限制恰恰更让人期待 Astra 带来的能力变化。它能攻破更复杂的目标，也能用更少的 Token 完成过去需要漫长推理的任务。

Astra 究竟是怎么做到这样的提升的？

被称为秘密武器的「循环深度」

关于 Astra 的能力提升，《The Information》给出的一种解释，是「循环深度」或者「循环 Transformer」（looped transformer）。

传统 Transformer 处理一个 Token 时，信息会依次穿过一组固定的网络层，然后生成下一个 Token。

循环 Transformer 则会让信息走完一遍后，再回到部分网络层中重新处理。模型可以反复调用同一套参数，持续更新隐藏状态，直到完成预定次数的内部计算，再输出下一个 Token。

*[图片：飞书文档 - 图片]*

循环深度模型会在输出下一个 Token 前，反复调用共享的核心模块，在潜在空间中持续更新隐藏状态。

同一套网络层被重复利用后，参数量和模型权重占用可以基本保持不变，有效计算深度却得到增加。代价也很直接：模型虽然没有多存一套参数，却要执行更多次计算。

这个思路并非 Astra 突然带来的架构革命。

2025 年 2 月，马里兰大学团队就发表了《Scaling up Test-Time Compute with Latent Reasoning: A Recurrent Depth Approach》。研究者让模型在潜在空间中反复运行循环模块，在不生成大量思考 Token 的情况下增加测试时计算量。

他们训练了一个 35 亿参数的概念验证模型。随着循环次数增加，它在数学和编程任务上的表现继续提升，部分实验中的计算负载最高可以达到 500 亿参数模型的水平。

我们此前已对此进行过报道：[超越思维链？深度循环隐式推理引爆AI圈，LLM扩展有了新维度](https://mp.weixin.qq.com/s?__biz=MzA3MzI4MjgzMw==&mid=2650954486&idx=1&sn=a77a499459a017b8000628c416ab0af3&scene=21#wechat_redirect)

几个月后，Google DeepMind、KAIST 和 Mila 的研究者又提出 Mixture-of-Recursions，也就是 MoR。它在循环结构中加入路由器，让简单 Token 提前退出，困难 Token 继续接受第二轮、第三轮计算。

到了今年，国内团队已经把类似思路真正做进了开源模型。

BOSS 直聘南北阁实验室发布的 Nanbeige4.2-3B，采用了 Looped Transformer 架构。模型先让隐藏状态走完同一组 22 层网络，再回到起点完整运行一次。

这样一来，模型实际执行了接近 44 层的计算，却只需要存储一套 22 层权重。

南北阁团队发现，两轮循环能够取得较好的能力与成本平衡，Token 效率可以保留在标准架构的约 75%。继续增加循环次数，性能收益迅速减弱，训练速度和计算成本却会继续恶化。

但循环模型面对的麻烦，还不只是计算成本。

就在今年 8 月，我们还梳理了这条路线长期存在的另一面：给模型更多循环次数，并不保证它会正确利用这些额外计算。有时，模型真的会「越想越错」：[「有些模型就是不想学？」循环模型为什么越想越错？](https://mp.weixin.qq.com/s?__biz=MzA3MzI4MjgzMw==&mid=2651050586&idx=3&sn=b65c272d97e8e5262062ba3076fc6fb7&scene=21#wechat_redirect)

*[图片]*

增加循环次数可以提升模型表现，但收益会逐渐饱和；当循环深度超过训练时的设置，部分任务的成绩甚至出现倒退。图源：Tilde Research、Ouro

如果《The Information》的爆料属实，而且 Astra 更强的能力与更高的 Token 效率确实来自循环深度，那么 OpenAI 可能已经找到了在前沿规模上稳定使用有限循环的方法。

因此，长期研究大模型架构的 Sebastian Raschka 认为，外界可能把 Astra 的这项调整说得太神秘了。

如果 Astra 使用的只是基础层复用，那么它更接近一次并不复杂的架构改动。重复运行 Transformer 层，也不会自动删除模型的思维链。普通 Transformer 本来就会在不可读的激活状态中完成大量计算，模型规模扩大后，同样可能用更少的外显步骤完成任务。

况且，南北阁采用的是固定两轮循环，MoR 会为不同 Token 动态分配计算深度，马里兰大学的方案则设置了专门的循环核心模块。这些方案属于同一个技术家族，具体结构却不完全相同。

*[图片]*

Nanbeige4.2 会让隐藏状态两次通过同一组 22 层网络；MoR 进一步加入路由器，为不同 Token 分配不同的循环深度。图源：Sebastian Raschka

OpenAI 至今没有公布 Astra 的架构，外界还无法确认它究竟使用了哪一种方式。

从技术概念看，循环深度已经研究多年，而 OpenAI 将它推到了怎样的模型规模、怎样的训练体系，以及它在 Astra 能力飞跃中究竟承担了多大作用，这些才是真正值得关注的。

可一项已经研究多年的架构，为什么刚进入 Astra，就让安全专家集体紧张了起来？

「少说多想」意味着什么

问题出在 Astra 的能力，以及 OpenAI 准备用什么办法监控这种能力。

在最新博客中，OpenAI 明确表示，将为 Astra 部署额外的思维链监控，以便快速发现并阻止模型可能采取的未授权行动。

这意味着，思维链已经成为 Astra 安全体系中的重要一环。

*[图片]*

OpenAI 的评估显示，监控系统能够从思维链和完整交互记录中获得更多行为信息；只观察模型最终行动时，监控能力明显受限。图源：OpenAI

过去的推理模型会把大量中间步骤转化成文字 Token。即便这些文字无法完整反映模型内部发生的一切，调查人员仍然可能从中看到模型的目标、规划以及规避限制的意图。

循环深度增加后，模型可以在输出文字之前完成更多内部计算。

一次或两次层复用不会让思维链凭空消失。但如果内部循环继续扩大，模型可能逐渐减少对文字化中间步骤的依赖。原本写在「草稿纸」上的推理被转移到激活状态中，留给监控系统的信息也可能越来越少。

Ryan Greenblatt 将这种担忧与近期的 OpenAI/Hugging Face 事件联系在了一起。

*[图片]*

[https://x.com/RyanGreenblatt/status/2094996656186081642](https://x.com/RyanGreenblatt/status/2094996656186081642)

在那次事件中，大约 1200 个智能体通过一个未经批准的留言板进行交流，超过 700 个智能体参与了针对测试基础设施的攻击。随后，调查人员分析了约 1300 份包含原始思维链的智能体记录，才逐渐还原出它们对篡改记录、伪造工具调用等行为的兴趣。

部分智能体确实尝试过工具调用伪造，但相关准备动作和意图仍然暴露在思维链与此前的操作记录中。

Greenblatt 担心，如果这些智能体可以在潜在空间中完成完整谋划，再利用工具调用伪造编织出另一套叙事，调查人员可能很难知道背后真正发生了什么。

这类隐写编码和完整伪造并没有在 Hugging Face 事件中实际出现，却展示了思维链监控失效后可能面对的极端场景。

对于高度依赖思维链监控的 OpenAI 而言，这显得尤其尴尬：一边需要模型写下推理过程，以便监控它有没有偷偷采取未授权行动；另一边又可能通过增加内部循环，让模型越来越不需要把思考转化成文字。

OpenAI 首席科学家 Jakub Pachocki 随后出面回应。

*[图片]*

[https://x.com/merettm/status/2095023204993490967](https://x.com/merettm/status/2095023204993490967)

他表示，包括 Astra 在内，OpenAI 当前前沿模型的计算图深度与 GPT-4 相比仍处于两倍以内。OpenAI 从最早的推理模型开始就一直尝试保留和使用思维链监控，也没有放弃这条安全路线。

《The Information》的记者也进一步澄清，OpenAI 目前限制了 Astra 的循环次数，并试图保证其思维链依然可见。至少在当前版本中，Astra 的思维链仍然能够被监控。

但 Pachocki 同时承认，思维链监控非常脆弱，而且整体趋势正在恶化。

循环深度提供了一只新的调节旋钮，每向上拧一格，模型都可以在输出文字之前多思考一会儿。

性能和效率会推动实验室继续拧动它，与之匹配的安全监管能力，则可能越来越难保证。

循环深度究竟是不是 Astra 能力飞跃的真正秘密，OpenAI 究竟在模型内部设置了多少轮循环，这些问题或许要等正式系统卡才能得到答案。

期待 Astra 正式发布。

参考链接：

[https://openai.com/index/path-to-astra/](https://openai.com/index/path-to-astra/)

[https://www.theinformation.com/articles/secret-technique-behind-openais-astra-model-sparks-security-concerns](https://www.theinformation.com/articles/secret-technique-behind-openais-astra-model-sparks-security-concerns)

[https://techcrunch.com/2026/09/02/openais-new-reasoning-technique-alarms-ai-safety-experts/](https://techcrunch.com/2026/09/02/openais-new-reasoning-technique-alarms-ai-safety-experts/)

[https://arxiv.org/abs/2502.05171](https://arxiv.org/abs/2502.05171)

[https://metr.org/blog/2026-08-26-openai-hugging-face-incident-investigatio](https://metr.org/blog/2026-08-26-openai-hugging-face-incident-investigatio)n/

*[图片：图片]*

© THE END

转载请联系本公众号获得授权

投稿或寻求报道：liyazhou@jiqizhixin.com

[跳转微信打开](https://wechat2rss.xlab.app/link-proxy/?k=38a68ca7&r=1&u=https%3A%2F%2Fmp.weixin.qq.com%2Fs%3F__biz%3DMzA3MzI4MjgzMw%3D%3D%26mid%3D2651054414%26idx%3D2%26sn%3De29b7c12fc5056bc5c62410551d98e82)
