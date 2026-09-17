---
title: 复杂的Harness Evolution，甚至不如多跑几遍
date: 2026-09-16
source: https://mp.weixin.qq.com/s?__biz=MzA3MzI4MjgzMw==&amp;mid=2651057510&amp;idx=2&amp;sn=8e1bea2b097f6ec4c012b75cf0ccfacb
account: 机器之心
fetched_at: 2026-09-17 18:00:04 CST
article_id: 8e1bea2b097f6ec4c012b75cf0ccfacb
---

机器之心 2026-09-16 12:00 四川

  
  
*[图片]*

  
当 “自我进化” 的 Agent 得分提高时，我们怎么知道它是真的学会了更好的工作方式，而不是因为它比普通 Agent 多获得了几次尝试机会？

  
*[图片]*

*[图片]*

- 论文标题：Rethinking the Evaluation of Harness Evolution for Agents
- 论文链接：https://arxiv.org/abs/2607.12227

- 代码：https://github.com/rethinking-harness-evolution

- 博客：https://yikee.github.io/harnessevolution/

一个 Agent 第一次没把任务做对。

接下来，你有五份额外的推理预算，可以有很多种花法。

你可以让它把同一道题重新做几遍，从多个结果里挑最好的；可以把上一次失败的过程交给它，让它接着修；也可以做一件听起来更 “高级” 的事 —— 让 Agent 分析自己的失败，修改 Prompt、工具、Memory 和控制逻辑，甚至自动重写整个运行框架。

最后一种思路，正在成为 Agent 研究里一个很热门的方向：Harness Evolution。

它背后的愿景非常吸引人。今天是工程师观察 Agent 为什么失败，然后修改 Prompt、添加工具、设计 Memory、调整 workflow；未来，也许这些工作可以交给 Agent 自己。Agent 不只是完成任务，还能够修改支撑自己工作的系统，从而一轮比一轮更强。

但这里隐藏着一个很容易被忽略的问题：

当 “自我进化” 的 Agent 得分提高时，我们怎么知道它是真的学会了更好的工作方式，而不是因为它比普通 Agent 多获得了几次尝试机会？

AI2 和华盛顿大学的一项最新研究，专门把这个问题摆到了台面上。

研究者做的事情并不复杂：把 Harness Evolution 和最简单的 “多跑几遍” 放到尽可能公平的条件下，给它们相同的反馈、相近的 inference budget，然后看看究竟谁更有效。

结果有些出人意料。在他们的实验中，复杂的 Harness Evolution 并没有稳定胜过简单的 test-time scaling。更值得注意的是，当进化出来的 Harness 被拿去解决从未参与优化的新任务时，提升只剩下了很小的一部分。

这意味着，我们可能需要重新理解过去一些所谓 “Agent 自我进化” 的提升。

Harness，其实就是模型外面的那套 “操作系统”。一个大模型真正成为 Agent，通常不只是因为模型本身。模型外面还有一整套系统：Prompt 怎么写、能调用哪些工具、有没有 Memory、如何验证结果、失败以后是否重试、什么时候停止、下一步看到什么信息…… 这些东西加起来，可以理解成 Agent 的 Harness。同一个模型，底层参数完全不变，仅仅因为 Harness 不同，表现就可能出现明显差异。

过去 Harness 大多依赖工程师手工优化。Agent 跑一次任务，工程师阅读 trajectory，发现某个工具调用方式不合理，于是修改 Prompt；发现 Agent 总忘记前面的信息，就加入 Memory；发现它不会检查答案，再增加 verifier。

Harness Evolution 想做的，就是把这套人工迭代过程自动化。Agent 运行任务，观察结果，总结失败经验，自动修改自己的 Harness，再运行一轮，然后继续修改。Meta-Harness、AHE、AEVO 等工作，都在探索类似的方向。如果这条路最终走通，它的意义很大：Agent 系统可能开始具备某种形式的自动工程优化，甚至成为递归自我改进的一部分。

问题是 —— 这种 “进化” 本身也是一种搜索。真正应该比较的，不是 “进化前” 和 “进化后” 假设一个普通 Agent 只运行一次，得分是 70。然后 Harness Evolution 允许系统连续运行五轮：分析失败、修改 Harness、重新执行、再次分析…… 最后得分变成 75。我们能不能因此说：Harness Evolution 让 Agent 提升了 5 分？

不一定。因为在第二种情况下，系统不只改变了 Harness，同时也使用了更多推理计算、执行了更多 trajectory、获得了更多反馈。真正公平的对照应该是：如果不修改 Harness，也给普通 Agent 五次运行机会，会发生什么？例如，同一道任务直接独立运行五次，从中选择最好的一个。或者第一次失败以后，让 Agent 看着之前的结果继续修改，连续修五轮。这些方法没有复杂的 “自我进化” 模块，本质上只是增加测试时计算，因此通常被称为 test-time scaling。这也是这篇论文想回答的核心问题：

在反馈和计算预算基本一致的情况下，

修改 Harness 本身究竟贡献了多少额外收益？

五份预算，四种花法。研究者在 Terminal-Bench 2.1 上做了对照实验。为了尽量减少其他因素干扰，所有方法都从一套非常简单的初始 Harness 出发：只有一个 bash 工具，没有额外 Skills，没有 Middleware，也没有持久化 Memory。使用的模型包括 Claude Opus 4.6、GPT-5.4 和 GPT-5.4 mini。每个任务统一获得 (K=5) 的计算预算。别只是：这五份预算怎么用。

*[图片]*

第一种是 Parallel Sampling。Harness 从头到尾都不修改。同一个任务独立执行多次，再从候选结果中选择最终答案。可以把它理解为：不会就多做几遍。

第二种是 Sequential Refinement。Harness 同样固定，但后一次执行能够利用前一次留下的结果和反馈。不是从头重来，而是 “第一次没做好，那就接着改”。

第三种才是传统意义上的 Harness Evolution。系统从多个任务的运行经验里总结规律，再修改一套共享 Harness，希望新的 Prompt、工具配置或者控制逻辑，可以让整个任务分布上的 Agent 都变强。论文中使用 AHE 作为具体实现。

第四种是作者设计的 Harness Scaling。它介于两者之间：不是学习一个面向整个数据集的通用 Harness，而是针对当前这道题，根据刚刚发生的 trajectory 动态修改 Harness。

四种方法的区别看起来很大，但它们面对的是同一个问题：五次计算机会，到底应该拿来 “改系统”，还是直接 “继续做题”？没有正确答案反馈时，最朴素的方法反而赢了

研究者首先去掉了 Unit Test。也就是说，Agent 做完任务以后，没有一个可靠的外部信号告诉它 “你到底做对没有”。这种场景对 Harness Evolution 尤其有挑战，因为它需要根据自己的 trajectory 判断究竟哪里出了问题，再决定 Harness 应该怎么改。

*[图片]*

结果是：最初的简单 Harness，平均分为 68.2。Parallel Sampling，也就是 Harness 完全不变、单纯多尝试几次，平均提升到了 72.3。Sequential Refinement 为 69.3。Harness Scaling 达到 71.8。而传统 Harness Evolution 的平均成绩只有 67.4。换句话说，花了更多步骤去 “学习如何改进自己的 Harness”，最后甚至没有超过最开始那套简单 Harness。

为什么会这样？一个可能的原因是：没有可靠 verifier 时，Agent 连 “自己为什么错了” 都未必判断准确。假如第一轮错误诊断就出现偏差，后续的 Harness 修改实际上是在基于错误信息继续优化。它可能不是越改越好，而是越改越偏。Parallel Sampling 则完全没有这个问题。它什么也不学习，什么也不总结，只利用模型输出本身存在的随机性，多尝试几次。这种方法非常简单，却反而更加稳定。

那如果 Agent 明确知道自己做错了呢？接下来，研究者加入了 Unit Test。

*[图片]*

这一次，各种方法都能够得到相对可靠的 correctness signal。如果前面的 Harness Evolution 主要吃亏在 “自己不知道自己错在哪”，那么有了 Unit Test，它理论上应该更有优势。实验结果确实整体大幅提高。但赢家依然不是 Harness Evolution。

在 Claude Opus 4.6 和 GPT-5.4 上，Parallel Sampling 的平均 pass@1 达到 86.0。Sequential Refinement 的平均 pass@5 达到 91.8。Harness Evolution 的平均 pass@1 是 75.8，pass@5 为 86.2。Harness Scaling 的平均 pass@1 为 82.6，pass@5 为 89.3。

这里最值得看的，其实不是哪一个数字最高，而是 pass@1。因为如果 Harness Evolution 真的发现了一套明显更好的 Harness，那么理论上，换上这套新 Harness 以后，Agent 第一次尝试就应该比以前更容易成功。换句话说，真正属于 Harness 的能力提升，应该很明显地出现在 first-try performance 上。但实验中看到的现象并不是这样。很多提升只有在系统拥有多次 trajectory、能够反复尝试或从多个结果中挑选成功答案以后才出现。

还有一个比计算预算更关键的问题。很多 Harness Evolution 方法会利用 benchmark 中的任务和反馈不断优化 Harness，最后再回到同一个 benchmark 上报告成绩。这很容易造成一种混淆：系统究竟学会了某种通用的 Agent 设计原则，还是越来越熟悉这一批 benchmark？

*[图片]*

为了把两种情况区分开，作者重新划分了 Terminal-Bench 2.1。其中 45 个任务用于 Harness Evolution，10 个作为 validation set，最后留下 34 个完全隔离的任务作为 test set。进化过程中，系统不能看到最终 test set。最后再拿选出的 Harness 去做这些真正没有见过的任务。

结果是：Claude Opus 4.6 从 63.3 提升到 64.5。GPT-5.4 则从 72.1 变成 72.1，没有提升。两个模型平均下来，成绩从 67.7 变成 68.3。也就是：+0.6 个百分点。

这和 Harness 在参与优化的任务上表现出来的增益形成了鲜明反差。如果一种 Harness 设计真正捕捉到了通用的 Agent 工作原则，那么换一批新任务以后，理论上应该继续带来明显收益。但这里看到的迁移效果非常有限。

因此作者提出了一种解释：当前自动 Harness Evolution 得到的部分收益，可能更接近 task-specific adaptation。系统在搜索过程中逐渐适应了这组 benchmark，而不一定发现了一套能够稳定迁移的新 Agent 架构。这不是在证明 “Agent 自进化没有意义”，更准确的说法是：现有实验可能还不足以证明，我们看到的性能提升确实来自 “Harness 变聪明了”。

其中一个原因，可能恰恰在于 Terminal-Bench 这样的任务已经可以被强模型用相对简单的 Harness 解决。Shell 加一个基本 Prompt，对于很多能够解决的任务来说可能已经足够。剩下那些做不出来的问题，也许真正卡住 Agent 的并不是 Prompt、Memory 或工具配置，而是底层模型本身的能力上限。如果模型根本不知道该怎么解决一道问题，再复杂的 Harness 也不一定能凭空创造出缺失的推理能力。

这反过来也指出了一个很重要的研究方向：真正适合研究 Harness Evolution 的 benchmark，可能需要让 “Harness 的质量” 成为决定成败的关键变量。例如任务确实需要长期 Memory，需要多个专业工具协同，需要复杂 workflow，需要在不同阶段采用不同策略，或者必须依靠精心设计的验证和恢复机制。只有在这些任务里，我们才能真正观察到：不换模型，只改变 Agent 外部架构，能不能让系统获得原本没有的能力？

这篇论文真正挑战的，可能是 Agent Evaluation。从这个角度看，这项工作的意义其实并不局限于 Harness Evolution。今天越来越多 Agent 系统都会加入 Reflection、Memory、Planner、Evaluator、Multi-Agent、Self-Improvement、自动 Prompt 优化等模块。系统也因此越来越复杂。但与此同时，一个非常基础的问题变得更加重要：复杂系统成绩更高，到底因为算法更好，还是因为它消耗了更多计算？假设一个新 Agent 架构有 Planner、有 Critic、有 Memory，还有三个子 Agent。它每道题总共调用模型二十次，最终 benchmark 提高了五个百分点。另一个极简 Agent 什么模块都没有。但如果也允许它调用模型二十次，只是重复采样、不断修正，结果同样提高五个百分点。那么前面那套复杂架构真正带来的算法价值，就值得重新衡量。

因此，未来评估这类系统时，一个更严格的标准可能应该是：比较双方是否拥有相近的 inference budget，是否获得同等级别的外部反馈。

而随着 Agent 从单次调用模型，走向越来越长的 trajectory、越来越复杂的工作流，这个问题只会越来越重要。这篇工作的价值，也许就在于提醒我们：在谈 Agent 的 “自我进化” 之前，首先要把一个更朴素的问题算清楚 —— 如果给最简单的方法同样多的时间、反馈和计算，它能做到什么程度？

有时候，看起来像 “进化” 的提升，可能只是一次没有被计入对照组的重试。

欢迎提问和讨论

作者简介：Yike Wang 是华盛顿大学 (University of Washington) 的博士生，导师为 Prof. Hanna Hajishirzi 和 Prof. Yulia Tsvetkov。她同时也是艾伦人工智能研究所 (Allen Institute for AI，AI2) 的学生研究员。Teng Xiao 在艾伦人工智能研究所和华盛顿大学工作，与 Prof. Noah A. Smith 和 Prof. Hanna Hajishirzi 合作。本文的共同第一作者还包括 Huaisheng Zhu。

*[图片：图片]*

© THE END

转载请联系本公众号获得授权

投稿或寻求报道：liyazhou@jiqizhixin.com

[跳转微信打开](https://wechat2rss.xlab.app/link-proxy/?k=163702c7&r=1&u=https%3A%2F%2Fmp.weixin.qq.com%2Fs%3F__biz%3DMzA3MzI4MjgzMw%3D%3D%26mid%3D2651057510%26idx%3D2%26sn%3D8e1bea2b097f6ec4c012b75cf0ccfacb)
