---
title: EP-Harness：从个人 AI Coding 到团队级 Agent 工作流｜得物技术
date: 2026-08-19
source: https://mp.weixin.qq.com/s?__biz=MzkxNTE3ODU0NA==&amp;mid=2247546472&amp;idx=1&amp;sn=f81736e344109ae41c6f78127d847519
account: 得物技术
fetched_at: 2026-08-20 18:00:03 CST
article_id: f81736e344109ae41c6f78127d847519
---

原创 方舟 2026-08-19 18:30 上海

  
  
*[图片]*

  
个人用 AI 写代码方便，团队化却会暴露 Prompt 无人审、经验不沉淀、链路没闭环等问题。EP-Harness 把 Agent 当团队成员来管理，核心不是让模型更强，而是让它能在真实研发流程里正确工作，最终让 AI Coding 从个人工具变成可治理、可持续闭环的团队生产力。

  
*[图片]*

**目录**

一、本地 AI Coding 的团队级缺口

二、EP-Harness 的定位：团队级 Agent 工作系统

1.分层可组合架构

2.Backend.Execute：统一 Agent 执行契约

三、AI Coding 正在从工具使用走向工程系统

1.Agent 需要理解真实研发现场

2.Prompt 从个人技巧变成团队规程

3.Context 从“复制粘贴材料”变成结构化上下文

4.Harness：让 Agent 真正可执行、可观察、可治理

5.Loop：把重复工作变成可控闭环

四、落地效果

1.决策追溯

2.多 Agent 协作

3.自动化治理

五、后续演进

六、结语

**一**

**本地 AI Coding 的团队级缺口**

直接在本地使用 AI Coding 工具，短期看，很方便，但团队化之后会暴露出几个缺口。

- **Prompt 没有 Review**

代码有 Code Review，prompt 没有。Agent 指令写得好不好、有没有歧义、有没有安全风险、能不能复用，往往只靠个人判断。

- **经验无法沉淀**

日志排查步骤、部署检查方式、开发提示词通常只留在个人本地文件里，下一个人还要重新摸索。

- **过程缺少可见性**

谁在用哪个 Agent？用了什么模型和 runtime？成功率、耗时、token 花费是多少？没有平台化就很难进入团队管理。

- **研发链路没有闭环**

Agent 写完代码不是结束。代码审查、推送、部署、提测、CR 反馈、BUG 回流和日志巡检如果仍靠人手动接力，价值就停在局部提效。

**EP-Harness 的核心价值，就是把这些缺口从个人习惯问题变成平台能力。**

**二**

**EP-Harness 的定位：团队级 Agent 工作系统**

EP-Harness 可以理解为一个 Managed Agents 平台。它把 Agent 当成团队里的工作成员来管理：Agent 有身份、有任务、有状态、有执行记录、有可见性、有权限边界，也有自己的 instructions、skills、runtime 和历史产出。

**技术基座：**EP-Harness 是基于开源项目 Multica 的二次开发。Multica 官方定位是 open-source managed agents platform，核心思路是把 coding agents 作为可分配任务、可跟踪进度、可沉淀技能的真实队友来管理；EP-Harness 在这个基座上，进一步贴合公司研发流程和内部系统。

**分层可组合架构**

*[图片]*

*[图片]*

从架构上看，Multica 由 server、daemon 和 AI 编程工具三部分协作：server 管理工作区、Issue、成员和任务队列，并承担实时更新；daemon 运行在开发者本机，领取任务并调用本地 AI 编程 CLI；实际的代码执行发生在本地工具链和工作目录中。

在 EP-Harness 里，任务不是散落在聊天窗口里，而是进入 Issue。Issue 可以关联项目、需求、应用分支、工作流、评论、执行日志、文件变更和后续反馈。

- 当 Agent 的任务进入 Issue，团队就可以追踪它。
- 当 Agent 的规则进入 Instructions 和 Workflow，团队就可以审查它。
- 当 Agent 的经验进入 Skills，团队就可以复用它。
- 当 Agent 的执行进入 Runtime 和日志，团队就可以复盘它。
- 当 Agent 的结果进入部署、评审和反馈链路，团队就可以让它持续闭环。

**Backend.Execute：统一 Agent 执行契约**

EP-Harness 在 server/pkg/agent/agent.go 中以 Backend.Execute(ctx, prompt, ExecOptions) 作为各 Agent Runtime 的统一入口。agent.New 根据 agentType 和 Config 选择具体 Provider Backend；Claude、Codex、OpenCode、ACP 等实现可以保留各自的参数、进程和传输协议，但对上层暴露一致的执行生命周期。

*[图片]*

**三**

**AI Coding 正在从工具使用走向工程系统**

AI Coding 的使用方式正在经历四层变化。它们不是互相替代，而是逐层外扩：从"怎么问"，走向"喂什么材料"，再走向"如何执行和约束"，最终走向"如何持续闭环"。

*[图片]*

个人 AI Coding 工具通常解决前两层。EP-Harness 还解决后两层，并把四层能力放进团队研发流程。

*[图片]*

**Agent 需要理解真实研发现场**

通用 AI Coding 工具并不了解公司的研发体系。它不知道需求结构，不知道内部飞书文档权限，不知道应用分支如何创建，不知道代码管理和发布平台的实际流程，也不知道每个团队沉淀过哪些 Skills。

EP-Harness 的价值，就是把这些内部系统接进 Agent 的工作环境里。它要解决的不是"模型有没有能力写代码"，而是"模型能不能在我们的研发流程里正确工作"。

*[图片]*

外部工具能给你一个 Agent，EP-Harness 要给团队一个 Agent 可以工作的组织环境。

**Prompt 从个人技巧变成团队规程**

很多团队刚开始用 AI 时，会把重点放在 prompt 技巧上。但用得久了会发现，更重要的是把 prompt 变成可维护的规程。

*[图片]*

**Context 从“复制粘贴材料”变成结构化上下文**

Agent 做不好，很多时候不是模型不够强，而是上下文不对。需求背景、设计文档、验收标准、关联代码仓库、目标分支、历史讨论、失败记录和内部系统调用方式，不应该靠用户每次手动复制粘贴。

- **Issue：**任务目标、评论、状态和历史记录。
- **需求：**业务背景、需求文档和迭代信息。
- **项目：**业务边界和仓库资源。
- **Workflow：**阶段目标和交付要求。
- **Skills：**团队沉淀的方法和工具说明。
- **Runtime：**真实执行环境。
- **飞书集成：**通知、讨论和文档读取能力。
- **运行记录：**执行过程、产出和失败信息。

这样 Agent 不再只拿到一段文字描述，而是进入一个由 Issue、项目、文档、分支、评论和运行记录组成的工作现场。

**Context Engineering 的重点不是把上下文塞满，而是让正确上下文在正确时机进入 Agent。**

**Harness：让 Agent 可执行、可观察、可治理**

一个裸模型没有工作目录，不会天然知道当前项目怎么测试，也不会自动遵守团队规范，更不会自己接入需求管理、代码管理、发布平台、飞书和日志平台。Harness 的价值，就是在模型外面补齐这些工程能力。

*[图片]*

这让 Agent 从"一个能说话的模型"变成"一个可管理的执行单元"。对团队来说，更重要的不是 Agent 某次回答得多漂亮，而是它能否长期稳定地在工程约束里工作。

**Loop：把重复工作变成可控闭环**

Loop Engineering 不是让 Agent 一直跑，也不是无限自动化。有价值的 Loop，需要包含发现、派发、执行、验证、记录和下一步决策。

- **上游版本更新分析**

自动化定时检查外部 release。 判断是否已有分析 Issue。 发现新版本后创建分析任务。 Agent 分析影响、风险、迁移建议和验证项。 需要落地时继续拆成迁移子任务。

- **线上日志巡检**

自动化按时间窗口拉取异常。 聚合错误 fingerprint、影响范围和样本。 Agent 分析可能根因。 生成修复建议和验证建议。 必要时创建后续修复 Issue。

这些场景的关键不是"Agent 自动跑了"，而是每一轮都有记录、判断、产出和后续动作。Loop 的价值在闭环，不在循环本身。

**四**

**落地效果**

*[图片]*

**决策追溯**

需求交付完成后，可依托 Issue 中沉淀的决策记录、实现说明，快速还原当时的实现背景和关键取舍。

*[图片]*

**多 Agent 协作**

**案例结论：**通过将交付流程拆分为提议、开发、评审、归档等阶段，并引入多 Agent 协作机制，形成从需求澄清、实现落地、质量评审到经验沉淀的闭环，持续提升代码质量。

*[图片]*

**自动化治理**

治理成效：累计自动化修复 100+ 个异常日志问题，异常日志从高频暴露逐步收敛，问题识别、归类和修复效率明显提升。典型高频问题由治理前每 4 小时 2400+ 条，降低到治理后的个位数。

*[图片]*

**五**

**后续演进**

*[图片]*

*[图片]*

**六**

**结语**

AI Coding 的第一阶段，是个人把 Agent 当工具。下一阶段，是团队把 Agent 当协作成员。当 Agent 开始接触真实需求、真实代码、真实部署和真实反馈时，单纯依赖聊天窗口和本地 prompt 已经不够。团队需要一个平台，把 Agent 的任务、上下文、规则、执行、审查、反馈和度量都组织起来。当这套机制跑起来，Agent 才能从一个个人电脑里的助手，慢慢变成团队研发流程里可管理、可复用、可持续优化的生产力。

**往期回顾**

1.[得物知识问答：复合检索 Agent 的系统设计实践](https://mp.weixin.qq.com/s?__biz=MzkxNTE3ODU0NA==&mid=2247546407&idx=1&sn=bf3d73aab43b7634074d2331a14764f5&scene=21#wechat_redirect)

2.[实战从零开始构建一个Coding Agent：Violin ｜得物技术](https://mp.weixin.qq.com/s?__biz=MzkxNTE3ODU0NA==&mid=2247546363&idx=1&sn=e497e41b6f529e7efb771672bc6864a0&scene=21#wechat_redirect)

3.[AI Native 交易核心系统的研发范式｜得物技术](https://mp.weixin.qq.com/s?__biz=MzkxNTE3ODU0NA==&mid=2247546316&idx=1&sn=cbe17a317044b279de6ad192302d9390&scene=21#wechat_redirect)

4.[推荐系统体验的数字化突破：得物自动化评测平台的技术实践｜AICon 文章整理](https://mp.weixin.qq.com/s?__biz=MzkxNTE3ODU0NA==&mid=2247546265&idx=1&sn=46de88c503a39ae3a77bd1ab36b85aff&scene=21#wechat_redirect)

5.[RAG 核心概念与原理：Chunking、Embedding、相似度、HNSW 与多路召回｜得物技术](https://mp.weixin.qq.com/s?__biz=MzkxNTE3ODU0NA==&mid=2247546214&idx=1&sn=1ea66a2621a684b57f05339341dde10f&scene=21#wechat_redirect)

文 / 方舟

关注得物技术，每周三更新技术干货

要是觉得文章对你有帮助的话，欢迎评论转发点赞～

未经得物技术许可严禁转载，否则依法追究法律责任。

“

**扫码添加小助手微信**

如有任何疑问，或想要了解更多技术资讯，请添加小助手微信：

*[图片]*

[跳转微信打开](https://wechat2rss.xlab.app/link-proxy/?k=1f9093e9&r=1&u=https%3A%2F%2Fmp.weixin.qq.com%2Fs%3F__biz%3DMzkxNTE3ODU0NA%3D%3D%26mid%3D2247546472%26idx%3D1%26sn%3Df81736e344109ae41c6f78127d847519)
