---
type: Article
title: Loop Engineering 实践指南：在 Code Buddy 中构建自主循环系统
description: 自主循环设计——Sense-Decide-Repair 范式
date: 2026-06-22
source: raw/2026-06/2026-06-22_Loop Engineering 实践指南：在 Code Buddy 中构建自主循环系统.md
tags: [loop-engineering, agent, automation, loops]
timestamp: 2026-06-22T00:00:00+08:00
---

## 适用场景

- 单次 Agent 调用不够，需要多步骤「检测→判断→纠错→重试」的自主循环
- 需要 Agent 能在无人干预下连续完成复杂任务
- 想把 Harness 从「单次执行」升级到「持续自主运行」
- 正在设计需要自动恢复机制的 Agent 流程

## 核心问题

单次 Agent 调用只能解决一步任务。真实工作（开发→测试→修复→部署→监控）需要 Agent 在多个步骤间自主循环——检测结果、判断下一步、自动纠错。

## 方法

**Loop Engineering 的核心组件**：

- **感知环**（Sense Loop）：监控输出/状态变化，触发下一步
- **决策环**（Decide Loop）：根据结果判断走哪个分支
- **修复环**（Repair Loop）：失败时自动诊断→修复→重试

**在 Code Buddy 中的应用**：通过 Skill + CLI 构建确定性循环。`while` 循环配 Gate 门禁（类似 Workflow 的步进式披露），每一步验证通过才推进。关键约束：最大循环次数（防无限消耗）、每次循环的 Token 预算、失败时的人机交接点。

## 关联概念

- 前置：[Skill 工程化设计](skill-as-algorithm.md) — Gate / Workflow 是 Loop 的基础组件
- 配合：[Harness Engineering](harness-engineering.md) — Loop 是 Harness 的高级形态
- 配合：[OpenClaw & Hermes 架构](openclaw-hermes-arch.md) — 框架层面对循环编排的支持

## 关键引用

> 「Loop Engineering 是把 Harness 从"单次执行"升级到"持续自主运行"的关键一步。」
