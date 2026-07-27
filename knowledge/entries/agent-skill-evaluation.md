---
type: Article
title: AI Agent & Skill 测评方案及落地实践
description: Agent 与 Skill 测评方案：Rubric 评分器、确定性评分
date: 2026-06-16
source: raw/2026-06/2026-06-16_AI Agent & Skill 测评方案及落地实践.md
tags: [evaluation, agent-evaluation, skill-evaluation, rubric]
timestamp: 2026-06-16T00:00:00+08:00
---

> 作者：martinskxu（腾讯TEG网关测试团队）

## 适用场景

- 想知道 Skill 写得到底好不好、有没有退步
- 需要量化 Agent 的交付质量而非靠主观感受
- 想建立可复现、可对比的测评体系
- 需要在 Demo 阶段就建立质量基准，而非上线后补救

## 核心问题

「当 AI Agent 从"Demo 可用"走向"生产可靠"，测评就是那道必须跨过的门槛。」三大难题：Agent 非确定性（同样输入不同输出）、黑盒化（推理过程不可见）、错误级联放大（上游小错下游大错）。

## 方法

**三类评分器组合**：

| 评分器 | 适用场景 | 特点 |
|--------|---------|------|
| 确定性评分器 | 有明确对错的验证点（格式、字段、数值范围）| 脚本化，无歧义 |
| Rubric 评分器 | 需要定性判断的维度（方案合理性、回答完整性）| LLM 按评分标准打分 |
| 人工评分器 | 强主观判断（体验、对齐、安全边界）| 最终兜底 |

**五大评测维度**：功能正确性、过程质量、效率成本、鲁棒性安全、体验对齐。在 TPerf 性能平台智能分析 Agent 项目中落地验证。

## 关联概念

- 前置：[Skill 编写手册](skill-design-handbook.md) — 先写好 Skill 再测评
- 配合：[Harness Eval](harness-eval.md) — 面向工作流的回归评测
- 配合：[Token 成本控制](token-cost-control.md) — 测评本身也消耗 Token

## 关键引用

> 「测评不是『好不好用』的感觉——是可复现、可量化、可对比的工程实践。」
