---
title: Agent Harness到底怎么选？南洋理工大学安波团队最新研究给出答案
date: 2026-10-04
source: https://mp.weixin.qq.com/s?__biz=MzA3MzI4MjgzMw==&amp;mid=2651061081&amp;idx=2&amp;sn=cb11670b3a6aae956f8e44f4cdfa08e9
account: 机器之心
fetched_at: 2026-10-05 18:00:04 CST
article_id: cb11670b3a6aae956f8e44f4cdfa08e9
---

机器之心 2026-10-04 11:54 四川

  
  
*[图片]*

  
Harness 的好坏并不是固定属性，而是取决于它与模型、任务之间的具体组合

  
*[图片]*

机器之心发布

开发 Agent 应用时，大家一定都为选择 Harness 纠结过：同一个模型接入不同 Harness，工具调用、上下文管理和错误恢复的方式都会发生变化，最终表现也可能相差很大。一套 Harness 在某类任务上表现突出，换到另一类任务后，却未必仍是最佳选择。

那么，不同任务究竟该选择哪套 Harness？是否存在一套能够稳定适配多种任务的通用方案？模型厂商提供的原生 Harness，又是否一定更适合自家模型？

新加坡南洋理工大学安波教授团队在最新报告《Finding the Right Fit: Model–Harness Interactions across Agent Tasks》中，对这些问题进行了系统研究。

*[图片]*

- 报告链接： https://arxiv.org/abs/2610.00917
- 实验代码仓：https://github.com/liyix/finding-the-right-fit
- 数据集：https://huggingface.co/datasets/yixuanli97/finding-the-right-fit

这篇报告不是在做一张简单的 Harness 排行榜，而是把模型与 Harness 视为一个整体进行比较。实验覆盖 OpenHands、DSH、PI 和 openJiuwen 四套可配置 Harness，并将 Codex–GPT 与 Claude Code–Claude 两组原生搭配作为参照。报告最终指向了一个很实际的结论：Harness 的好坏并不是固定属性，而是取决于它与模型、任务之间的具体组合。与其寻找一套 “放之四海而皆准” 的 Harness，不如围绕真实任务，对模型与 Harness 进行联合评估。

01 实验背景

为了考察 Harness 对 Agent 表现的影响，研究首先选取了四种可自由配置模型的 Harness：OpenHands、DeepSeek Harness（DSH）、PI 和 openJiuwen。

实验分别为这四种 Harness 接入 Claude Opus 5、GPT-6 Astra、GLM-5.3、Kimi K3 和 DeepSeek V4 Pro。这样的交叉设计，可以观察同一个模型更换 Harness 后的表现变化，也能比较同一套 Harness 面对不同模型和任务时是否依然稳定。

除此之外，研究还加入了两组原生搭配作为参照：Claude Code–Claude 与 Codex–GPT。由于 Claude Code 和 Codex 只接入自家模型，因此它们没有参与完整的交叉实验。

任务方面，研究选择了三个定位不同的任务集：TUA-Bench 侧重通用终端操作，ALE-CLI 聚焦专业工作流，Terminal-Bench 4 则包含难度更高的命令行任务。

*[图片]*

表 1｜三个任务集及其评测方式

由于三个任务集的任务构成和评分标准不同，研究没有将结果合并为一个综合分数，而是分别进行比较。四种可配置 Harness、五个模型和三个任务集构成了 4×5×3，共 60 项结果；再加上 Codex–GPT 与 Claude Code–Claude 在三个任务集上的 6 项原生搭配结果，最终形成了包含 66 项记录 的比较矩阵。

02 实验配置与数据

2.1 Harness 版本与运行配置

本次实验涉及四种可配置 Harness，以及 Codex 和 Claude Code 两种原生 Harness。所有 Harness 都通过 OpenRouter 调用模型，并固定路由到各模型的官方服务商；推理强度统一设为 high，上下文管理、重试和轮数上限等保持各 Harness 的默认设置。TUA-Bench 和 Terminal-Bench 4 使用 Harbor v0.22.0 运行，ALE-CLI 使用任务集自带的运行器，且在 ALE-CLI 上所有 Harness 都会接入任务集提供的 14 个计算机操作工具。

各 Harness 的版本如下：

- OpenHands：openhands-tools 1.44.1 版本；
- DeepSeek Harness（DSH）：0.1.1-rc.2 版本；
- PI：v0.84.4 版本；
- openJiuwen：0.1.18 版本。
- Codex：0.150.1 版本，仅与 GPT 搭配；
- Claude Code：2.1.251 版本，仅与 Claude 搭配。

2.2 计分方式

为了尽可能统一不同组合的计分方式，研究采用了固定任务集分母：

- TUA-Bench：120 项任务；
- ALE-CLI：99 项任务；
- Terminal-Bench 4：63 项任务。

三个任务集分别按固定任务数计分（TUA-Bench 120 项、ALE-CLI 99 项、Terminal-Bench 4 63 项），TUA-Bench 和 ALE-CLI 允许部分得分，Terminal-Bench 4 按通过或未通过计分。因基础设施故障中断的任务进行了重跑，每个任务只按最后一次运行计一次分，没有得到有效结果的任务记 0 分。

2.3 实验数据

在上述口径下，三个任务集的完整结果如下。

*[图片]*

图 1｜TUA-Bench 完整结果

openJiuwen 在 TUA-Bench 上表现出最广泛的优势：在四种可配置 Harness 中，它搭配五个模型时均取得最高分；即使加入原生 Harness，仍在其中四个模型上领先。值得注意的是，不同组合的领先幅度差异明显：openJiuwen 搭配 GLM 时仅小幅领先 OpenHands，搭配 Kimi 时则大幅领先 PI。

*[图片]*

图 2｜ALE-CLI 的 99 项本地 Docker 任务结果

在 ALE-CLI 上，各 Harness 的优势开始分化：Claude 的最高分来自 Claude Code，GPT-6 Astra 更适合 PI，Kimi 仍然与 openJiuwen 配合最好，GLM 和 DeepSeek 的最高分则来自 OpenHands。

*[图片]*

图 3｜Terminal-Bench 4 中 63 项非 H100 任务的结果

在更具挑战性的命令行任务集 Terminal-Bench 4 上，模型与 Harness 的适配差异更加明显：OpenHands 最适合 Claude Opus 5，PI 最适合 GPT-6 Astra，DSH 在 GLM 和 DeepSeek 上领先，openJiuwen 则继续为 Kimi 取得最高分。

这三张表并不是一份简单的 Harness 排行榜。更值得关注的是，当模型、Harness 或任务发生变化时，原有的领先关系能否继续保持。

03 实验结果分析

66 项实验结果呈现出两种看似矛盾的现象：一方面，更换 Harness 可能改变模型排名，同一模型的最佳 Harness 也会随任务变化；另一方面，部分模型与 Harness 的组合又能在多个任务集上保持优势。

这意味着，Harness 很难脱离具体模型和任务形成一套固定排名。

3.1 Harness 显著影响模型表现

Terminal-Bench 4 展示了一个典型的排名反转。

在 63 项任务的固定计分口径下，Claude Opus 5 通过 OpenHands 完成了 36 项任务，GPT-6 Astra 完成了 31 项，Claude 领先 7.94 分。但换成 PI 后，Claude 只完成了 19 项，GPT 则完成了 38 项，GPT 反过来领先 30.16 分。

*[图片]*

图 4｜Terminal-Bench 4 上 Claude 与 GPT 的表现对比

从 OpenHands 换到 PI，Claude 少完成了 17 项任务，GPT 却多完成了 7 项。Harness 的变化并没有让两个模型同时提升或下降，而是对它们产生了方向相反的影响。

因此，在某一套 Harness 中观察到的模型优势，不能直接推广到其他 Harness。模型排名描述的并不只是模型本身，还包含了模型与工具接口、上下文管理和执行流程之间的适配关系。

3.2 最佳 Harness 会随任务变化

即使模型保持不变，它在不同任务上的最佳 Harness 也可能不同。

*[图片]*

图 5｜各模型在三个任务集上的最高分 Harness

五个模型中，有四个的最高分 Harness 随任务集发生了变化。GLM-5.3 和 DeepSeek V4 Pro 的变化最明显：在 TUA-Bench、ALE-CLI 和 Terminal-Bench 4 上，两者的最高分分别来自 openJiuwen、OpenHands 和 DSH。

GPT-6 Astra 在 TUA-Bench 上搭配 openJiuwen 得分最高，在另外两个任务集上则更适合 PI。Claude Opus 5 在 TUA-Bench 和 ALE-CLI 上的最高分来自 Claude Code，到了 Terminal-Bench 4，OpenHands 的表现更好。

Kimi K3 是唯一的例外。它与 openJiuwen 的组合在三个任务集上均取得该模型的最高分，分别领先其他已评测配置 5.61 分、6.91 分和 11.11 分，表现出较为稳定的适配优势。

3.3 原生搭配并不意味着最优选择

模型厂商提供的原生 Harness 通常被认为更了解自家模型，但实验结果并未显示这种优势能够稳定延续。

*[图片]*

图 6｜原生搭配与同模型最高分 Harness 的比较

Claude Code 在 TUA-Bench 和 ALE-CLI 上取得了 Claude 的最高分，但在 Terminal-Bench 4 上落后于 OpenHands。Codex–GPT 在三个任务集上的得分，则分别低于 openJiuwen–GPT 和 PI–GPT。

这些结果表明，原生 Harness 并不一定是自家模型的最佳搭配。同一个模型接入其他 Harness 后，在部分任务上反而能够取得更好的表现。因此，选型时不能只看是否 “原生适配”，还需要综合比较任务完成度和运行成本。尤其是在需要切换模型、接入更多工具或覆盖多类任务时，Harness 的可扩展能力也是重要的考量。

3.4 成本更高，不一定带来更好表现

Harness 影响的不只是任务得分，也会改变模型调用次数、Token 消耗和整体运行成本。论文按照 OpenRouter 的统一价格计算模型 API 成本，结果发现，更高投入并不能稳定换来更好的表现。

以 Terminal-Bench 4 上的 GPT-6 Astra 为例，PI 的总成本约为 293.30 美元，得分为 60.32%；DSH 的总成本达到 1,256.48 美元，是 PI 的约 4.3 倍，得分却只有 52.38%。

*[图片]*

图 7｜不同模型–Harness 组合在三项任务上的得分与单任务成本对比

成本差异主要来自 Harness 组织模型调用和上下文的方式。较低成本通常伴随着更少的模型调用和未缓存输入 Token，但不一定意味着模型输出更少。

不同 Harness 的上下文复用能力也存在明显差异：openJiuwen 有 94%～99% 的输入 Token 来自缓存，其他 Harness 的缓存比例则为 49%～77%。

因此，评估 Harness 时不能只看最终得分或模型单价，还需要结合调用次数、未缓存输入、缓存利用率以及任务完成度，比较完整配置在目标任务上的实际投入产出。

04 为什么会这样：

从轨迹看 Harness 做了什么

分数只能展示结果，却解释不了差异从何而来。为此，报告进一步分析了任务和模型相同、仅 Harness 不同的配对轨迹，观察模型收到失败信号后如何应对。

研究选取了 Terminal-Bench 4 上的 10 组 OpenHands–PI 配对，覆盖五个模型和 192 个失败事件，并补充分析了 6 组 Kimi K3 在 openJiuwen 与 PI 下的轨迹。

192 个事件中，有 180 个应对动作由模型主动发起。诊断或定点修复是最常见的处理方式，共出现 133 次，其中 116 次成功。真正影响结果的，往往不是模型会不会修复，而是 Harness 能否将失败转化为模型可以利用的反馈。

4.1 犯错不可怕，关键在于能否精准反馈错误

TUA-Bench 的 056-move-textbox-left 任务提供了一个典型案例。Kimi K3 在 openJiuwen 和 PI 下犯了同一个错误：通过管道执行 GIMP 脚本时遗漏退出指令，导致命令一直等待输入，区别是 openJiuwen 在错误后及时反馈并最终在下一轮任务中修复了该错误。

在 PI 下，Shell 默认不设超时，模型也没有主动设置，命令因此持续挂起。39.8 分钟后任务到达截止时间，没有生成最终文件，得分为 0。

在 openJiuwen 下，前两次 GIMP 调用失败后，错误信息被返回给模型。第三次调用挂起时，Shell 在 300 秒后返回超时。模型据此发现脚本缺少退出指令，并确认图片已经生成，随后核对画布尺寸、背景色和文字位置。整个任务用时 11 分钟，得分为 1。

*[图片]*

图 8｜Kimi K3 在 TUA-Bench 任务 056-move-textbox-left 上的配对轨迹。

从上图可以看出，openJiuwen 在命令挂起后返回超时，模型据此完成诊断和恢复；PI 没有返回信号，运行最终到达截止时间。默认超时并非 openJiuwen 独有，OpenHands 和 DSH 也会限制命令时长。这个案例说明的并不是哪套 Harness 绝对更强，而是失败能否以有效反馈返回，会直接影响模型是否有机会恢复。

4.2 模型与 Harness 的适配度与模型习惯有关

同一种设计放到不同模型上，效果可能完全不同。GPT-6 Astra 在 PI 中有 56%～67% 的 Shell 调用会主动设置超时，因此 PI 没有默认超时，对它的影响很小。GPT-6 Astra 通过 PI 在 Terminal-Bench 4 和 ALE-CLI 上取得了该模型的最高分。

Harness 应该介入多少，不能简单按照模型强弱划分。模型已经能够自行处理的环节，减少干预可能更合适；模型容易遗漏的环节，则需要 Harness 提供必要的支持。

4.3 模型和 Harness 稳定适配的原因

Kimi K3 是唯一一个在三个任务集上都由同一 Harness ：openJiuwen 取得最高分的模型。逐任务比较显示，这种优势并非由少数任务撑起：在 TUA-Bench、ALE-CLI 和 Terminal-Bench 4 上，openJiuwen 分别在 22、25 和 8 个任务中取得更高分。即使去掉领先幅度最大的三个任务，平均仍领先 3.11、3.88 和 6.35 分。

*[图片]*

图 9｜openJiuwen–Kimi K3 与各任务集次优配置的逐任务比较。

轨迹分析给出了三个可能的原因。

- 工具接口：在 OpenHands 中，Kimi 多次发出缺少必要参数的编辑调用，重复失败后会触发终止。这类终止共发生 55 次，其中 48 次来自 Kimi。openJiuwen 将 “写文件” 和 “修改文件” 拆分为两个工具，更符合 Kimi 的调用方式。

- 命令超时： openJiuwen 会在命令长时间无响应时返回超时信息，使挂起状态重新变成模型可以处理的反馈。

- 截断续写：当输出因长度限制被截断时，openJiuwen 会保留已有推理并提示模型继续。在报告分析的 6 组 Kimi 配对轨迹中，这一机制在其中 2 组里起到了决定性作用。

这些结果表明，openJiuwen 与 Kimi K3 的稳定表现并非单一机制带来的，而是工具接口、错误反馈和续写策略共同作用的结果。

05 结语：应把模型与 Harness 放在一起评估

这篇报告对 Agent 选型最直接的启示，是把模型与 Harness 作为一个整体，在目标任务上进行评估。

如果模型已经确定，就需要比较它接入不同 Harness 后的实际表现；如果 Harness 已经确定，也不能直接套用其他 Harness 下的模型排名。当 Agent 从一种业务迁移到另一种业务时，原有组合也应重新验证。

对于需要处理多类任务的 Agent 系统，保留模型与 Harness 的配置空间是有价值的。但 “允许选择” 与 “能够自动选对” 并不是一回事。报告中的最佳配置是在结果产生后比较得出的，并没有证明系统能够在面对新任务时提前判断应该使用哪套 Harness。

如果要验证自动选择或路由策略，还需要在开发集上完成配置选择，再到未见任务上测试，并与同样基于开发集选出的最佳固定 Harness 比较。实际部署时，延迟、调用成本和工具执行开销也应与任务完成度一起纳入考量。

> Agent 的评估单位不应只是模型或 Harness，而应是模型、Harness 与任务共同构成的完整配置。

当任务变化、模型升级或 Harness 更新时，这种适配关系都值得重新验证。相比单独查看模型或 Harness 排名，直接测试完整配置在目标工作负载中的表现，更接近 Agent 的真实部署需求。

参考资料：

Finding the Right Fit: Model–Harness Interactions across Agent Tasks： [https://arxiv.org/abs/2610.00917](https://arxiv.org/abs/2610.00917)

Github repo：[https://github.com/liyix/finding-the-right-fit](https://github.com/liyix/finding-the-right-fit)

Dataset：[https://huggingface.co/datasets/yixuanli97/finding-the-right-fit](https://huggingface.co/datasets/yixuanli97/finding-the-right-fit)

TUA-Bench：[https://arxiv.org/abs/2606.28480](https://arxiv.org/abs/2606.28480)

Agents’ Last Exam（ALE）：[https://arxiv.org/abs/2606.05405](https://arxiv.org/abs/2606.05405)

Terminal-Bench：[https://arxiv.org/abs/2601.11868](https://arxiv.org/abs/2601.11868)

OpenHands：[https://github.com/OpenHands/OpenHands](https://github.com/OpenHands/OpenHands)

DeepSeek Harness：[https://github.com/deepseek-ai/deepseek-harness](https://github.com/deepseek-ai/deepseek-harness)

PI：[https://github.com/earendil-works/pi](https://github.com/earendil-works/pi)

openJiuwen：[https://github.com/openJiuwen-ai/](https://github.com/openJiuwen-ai/)

Codex：[https://github.com/openai/codex](https://github.com/openai/codex)

Claude Code：[https://github.com/anthropics/claude-code](https://github.com/anthropics/claude-code)

© THE END

转载请联系本公众号获得授权

投稿或寻求报道：liyazhou@jiqizhixin.com

[跳转微信打开](https://wechat2rss.xlab.app/link-proxy/?k=e0086ee6&r=1&u=https%3A%2F%2Fmp.weixin.qq.com%2Fs%3F__biz%3DMzA3MzI4MjgzMw%3D%3D%26mid%3D2651061081%26idx%3D2%26sn%3Dcb11670b3a6aae956f8e44f4cdfa08e9)
