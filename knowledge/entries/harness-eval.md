---
type: Article
title: Harness Eval：我们用一场考试撕掉了遮羞布
description: Harness Eval 回归评测——用考试检验工作流是否真的在进步
module: eval-testing
date: 2026-06-18
source: raw/2026-06/2026-06-18_你的 Harness 工作流真的在进步吗？我们用一场考试撕掉了遮羞布.md
tags: [harness, evaluation, eval]
timestamp: 2026-06-18T00:00:00+08:00
---

> 作者：chaseren

## 适用场景

- 改了 Skill / Rules 后不确定效果是变好还是变差
- 整个团队用主观感受（vibes）驱动工作流演进
- 需要一套轻量、可回归、可量化对比的评测标准
- 需要向团队证明「这版改进是数据可验证的」

## 核心问题

> 「团队花两周精心调教一套 Harness 工作流——写了十几条 Rules、打磨了 Skill——上线后评价体系是：'感觉这版稳了不少'、'昨天那版好像更聪明？'整个团队在用主观 vibes 驱动一个复杂系统的演进。」

**根本问题**：Harness 工作流没有可回归的客观评测标准。每次改 Skill/Rule 后不知道是进步了还是退步了。

## 方法

**Harness Eval：一套面向 Harness 工作流的、轻量的、可回归的闭环评测系统。**

核心思路：用一组固定任务作为"考卷"，每次改 Harness 配置后跑一次评测，对比得分变化。维度覆盖：任务完成度、步骤合规性（是否跳步骤）、产物质量、Token 效率。

**关键设计**：轻量——不需要复杂基础设施；可回归——同一套题反复跑，量化对比；闭环——评测结果反馈到 Rules/Skills 的改进方向。

## 关联概念

- 前置：[端到端全链路](ai-coding-to-harness.md) — 先建好 Harness 工作流再评测
- 配合：[Agent & Skill 测评](agent-skill-evaluation.md) — 评分器设计的具体方案
- 配合：[团队 Harness 规范](team-harness-spec.md) — 评测结果反馈到团队规范

## 关键引用

> 「Harness Eval 不是要证明你的工作流有多好——是要告诉你在哪里退步了。」
