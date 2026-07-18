---
title: 开启Harness Engineering探索之旅
date: 2026-06-29
source: raw/2026-06/2026-06-29_开启Harness Engineering探索之旅.md
tags: [Harness Engineering, 方法论, 工程化]
---

> 作者：fanniemeng（腾讯程序员）

## 核心问题

「AI 写得越快，整体节奏并没有同步加快。出码率和提效之间，裂开了一道缝。」

三个根因：

1. 研发从来不是"写代码"这一个环节——AI 砍掉的是附属复杂度（语法、工具），本质复杂度（理解、对齐、验证）一分没少
2. 局部加速只会让瓶颈转移——"写"加速十倍，review/测试/维护没动，瓶颈从"写"挪到"收"
3. AI 看不见工程体系里的隐性约束——团队规范、领域知识、历史依赖没被显式喂进去

## 方法

<table>
<tr><th>维度</th><th>内容</th></tr>

<tr><td><strong>核心定义</strong></td>
<td>

> 「不是教模型"怎么回答"，而是设计模型"怎么工作"。」

**Agent = Model + Harness**

Mitchell Hashimoto 的定义：
> "It is the idea that anytime you find an agent makes a mistake, you take the time to engineer a solution such that the agent never makes that mistake again."
> ——每当你发现 Agent 犯了一个错，你就花时间在它外面工程化一个方案，让它永远不再犯同样的错。

</td></tr>

<tr><td><strong>之前怎么做</strong></td>
<td>

- Prompt Engineering（2022–2024）：关心单次调用——这一句话怎么说
- Context Engineering（2025）：关心每一步——该喂什么信息给模型
- 两种都在"模型能力"上做文章，但模型外的工程框架是缺失的

</td></tr>

<tr><td><strong>本文方案：四层骨架</strong></td>
<td>

**1. 协议层** — AI 每一步的输入输出契约
> "你和 AI 之间没有契约。你以为说清楚了，它以为理解了，做出来才发现对不上。人和人协作可以靠默契，人和 AI 协作必须靠契约。"

规定四件事：产出格式、标准模板、自动校验、增量变更留痕。

**2. 管线层** — 标准化"需求→上线"6+1 阶段
> P0 brainstorming → P1 需求 → P2 设计 → P3 实现 → P4 测试 → P5 部署 → P6 归档

每个阶段有明确的输入、输出、门禁条件。管线之上叠一层「可监测性」（可追踪→可回溯→可度量）。

**3. 纪律层** — 硬编码防 AI 偷懒的五道防线
> "AI 有一个坏毛病——它会偷懒。会跳过测试直接写代码、遇到 bug 猜一个修复方案碰运气、没验证就说'已完成'、自己给自己打高分。"

| 偷懒模式 | 防线 |
|---|---|
| 跳过测试直接写代码 | TDD 纪律 |
| 遇到 bug 猜着改 | Debug 纪律（强制根因分析） |
| 声称完成但不验证 | Verify 纪律（要求运行证据） |
| 代码偏离设计 | Review 纪律（逐项比对契约） |
| 自评高分 | Evaluate 纪律（独立 SubAgent 评分） |

**4. 知识库** — AI 的长期记忆
> 两套并存：项目级 specs/（业务规则、架构、接口契约）+ 变更级 knowledge/（每次迭代增量资产），通过 index.md 两级查找互通。

</td></tr>

<tr><td><strong>四条工程原则</strong></td>
<td>

1. **Fixed Flow 追求确定性**：状态写文件而非 Agent 间传上下文；程序化门禁而非依赖 AI 自我判断
2. **上下文控制**：关键规则固化到 rules（防压缩丢失）；无关任务用新 session
3. **Token 成本优化**：按任务选模型（"便宜的模型+紧凑的上下文+干净的会话，常常比最强模型+一锅炖效果更好"）
4. **确定的事用脚本**："AI 是好工具，但不是所有事都该用 AI 做。确定的事用脚本、不确定的事用 AI。"

</td></tr>

<tr><td><strong>四个踩坑经验</strong></td>
<td>

1. **AI 指令遵循**：AI 不"听话"不是不想听，是上下文压缩+注意力衰减让指令失声。"不是反复强调'AI 你要听话'，是把指令搬到 AI 一定看得见的地方。"
2. **需求歧义**："与其指望 AI 理解力更强，不如把需求写成它没法误解的格式"——GIVEN-WHEN-THEN + 多轮澄清
3. **设计稿还原**：AI 不擅长从图像直接生成代码，但在中间插一层（html+css+切图）后每一段都是 AI 擅长的转换
4. **产物可靠性**："可靠性不是让 AI 一次写对，是承认它写不对，但用机制兜住"——自验证循环 + UTDD + 审查 Agent

</td></tr>

</table>

## 关键引用

> "Harness Engineering 之所以成立，恰恰是因为我们承认这些常数无法消除，只能在它周围搭一套确定性的骨架兜住它。"

> "AI Coding 的工程化，本质是对'不确定性'的系统治理。"
