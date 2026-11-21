---
title: TML开源新模型，循环Transformer架构，笔记本就能跑
date: 2026-11-21
source: https://mp.weixin.qq.com/s?__biz=MzA3MzI4MjgzMw==&amp;mid=2651075624&amp;idx=2&amp;sn=b6e7e23d631dba7a952cbe5da8e77769
account: 机器之心
fetched_at: 2026-11-21 18:00:04 CST
article_id: b6e7e23d631dba7a952cbe5da8e77769
---

原创 爱开源的 2026-11-21 12:11 四川

  
  
*[图片]*

  
Inkling 2 Mini 是一个仅有 26B 参数的循环 Transformer，小到足以在你的笔记本电脑上运行，强大到足以胜任智能体任务，在 AA Index 上的得分为 20.1。

  
*[图片]*

编辑｜Panda

昨晚，[黎曼猜想的一份 AI 证明声明](https://mp.weixin.qq.com/s?__biz=MzA3MzI4MjgzMw==&mid=2651075593&idx=1&sn=515456dc3e75d3a48fdee3e6b42d0bad&scene=21#wechat_redirect)，把大模型的推理能力再次推到聚光灯下。Anthropic 数学家 Levent Alpöge 宣称，自己与 Claude 合作找到了证明，并公布了形式化材料。虽然这项声明仍待独立核验，但已经让人们重新追问：AI 究竟能完成多复杂的工作？

而刚刚，Thinking Machines Lab（TML）发布并开放了 Inkling 2 Mini 的权重。

*[图片]*

这是一个总参数 26B 的多模态模型，采用循环 Transformer（looped transformer）架构，支持文本和图像输入，最大上下文窗口为 100 万 token。权重已按 Apache 2.0 许可发布，开发者可以下载部署，也能通过 Tinker 进行推理和微调。

- 模型卡与权重：https://huggingface.co/thinkingmachines/Inkling-2-Mini
- 官方博客：https://thinkingmachines.ai/news/inkling-2-mini/

官方宣称能在笔记本上运行，并且能胜任智能体工作。看起来，它要展示的是个人电脑上的模型能做到哪一步。

在 TML 公布的演示中，研究人员带着一台 MacBook Pro 登上飞机，断开网络，让 Inkling 2 Mini 在几分钟内写出了一个可玩的飞行模拟器。演示使用的是配备 48GB 内存的 M5 Pro 机型，推理在本地完成。

他们还构建了一个由 Inkling 2 Mini 搭建的微型像素小镇 Thinkyville。其中，同一模型在一台离线 MacBook 上驱动全部 20 位村民。他们规划一天的生活、闲聊八卦、举办烘焙比赛，还会回复你留在他们门上的便条。

模型发布后，社区反映非常热烈。有人将其接入了 DeepSeek Harness，跑出了飞快的速度。

*[图片]*

还有人让它玩通了一个电子游戏，并且发现它还能反复游玩并优化策略，并学会速通。

*[图片]*

生成动画 MV 也没有问题：

*[图片]*

让同一组权重，多算几轮

Inkling 2 Mini 的技术看点，在于它采用了循环 Transformer 架构。

普通 Transformer 在生成每个 token 时，会让信息依次经过一组固定的网络层。Inkling 2 Mini 则把中间一段网络重复利用：全模型共 24 层，最前和最后的 6 层各运行一次，中间 12 层运行三次。后续轮次还会读取上一轮传来的信息。

*[图片]*

因此，模型只需存储 24 层权重，就能为每个 token 完成 48 次层计算。增加的内部计算，为需要连续推导的任务提供了更多处理空间，同时控制了权重体积。

它还采用了混合专家（MoE）架构，每个 token 只调用部分专家参与计算。模型的激活参数约为 3.4B；将循环中的重复计算计入后，有效参数激活量约为 5.4B。

*[图片]*

[https://vllm-project.github.io/2026/11/20/inkling2-mini.html](https://vllm-project.github.io/2026/11/20/inkling2-mini.html)

编程表现

从 TML 公布的评测看，Inkling 2 Mini 的长处集中在智能体编程、搜索和工具使用上。

在 DeepSWE v1.1 上，它的任务解决率为 48.2%，对比的 Qwen3.8-27B 为 42.2%；在 SWE-bench Verified 上，两者分别为 79.2% 和 77.8%。

*[图片]*

要把这样的模型放进笔记本，权重的存储方式也很关键。Inkling 2 Mini 的专家层主要使用 NVFP4 低精度格式，最后 4 层采用 MXFP8。它在训练中就使用了相应精度，并以同样的精度部署，减少了交付时再次转换精度的环节。

发布的检查点约为 20GB。官方支持在至少配备 32GB 内存的 Apple 芯片设备上运行，其他 GPU 平台建议至少提供 32GB 显存；本地推理已有 Ollama、vLLM、SGLang 等工具支持。

更短的思维链

循环计算还有一层值得关注的含义：模型可以在输出文字之前，完成更多内部处理。于是，研究者需要继续检验，写出来的思维链能在多大程度上帮助人们理解和监督模型。

为此，TML 同步开放了 TML-d24-varloop-research。与固定循环三次的 Inkling 2 Mini 不同，这个研究版本允许在推理时调整循环次数，方便研究者在同一组权重上比较增加计算的影响。官方明确将它定位为研究模型，实际产品应用仍推荐使用 Inkling 2 Mini。

链接：[https://thinkingmachines.ai/model-card/tml-d24-varloop-research/](https://thinkingmachines.ai/model-card/tml-d24-varloop-research/)

Inkling 2 Mini 也有明确的能力边界。按照 TML 的说明，它在多轮对话和多重约束指令上仍有短板，复杂推理表现与更大模型存在差距；增加循环次数，也不会直接扩大权重中储存的事实知识。

这次发布值得关注的地方，是在有限的权重体积里增加推理计算，并把模型交给开发者在自己的设备上运行。对于希望搭建本地编程助手或长期运行智能体的人，Inkling 2 Mini 算是一个值得一试的新选择。

更多细节请访问官方博客与仓库。

*[图片：图片]*

© THE END

转载请联系本公众号获得授权

投稿或寻求报道：liyazhou@jiqizhixin.com

[跳转微信打开](https://wechat2rss.xlab.app/link-proxy/?k=d4a284c6&r=1&u=https%3A%2F%2Fmp.weixin.qq.com%2Fs%3F__biz%3DMzA3MzI4MjgzMw%3D%3D%26mid%3D2651075624%26idx%3D2%26sn%3Db6e7e23d631dba7a952cbe5da8e77769)
