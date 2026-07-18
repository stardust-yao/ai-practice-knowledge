---
title: Loop Engineering 实践指南：在 Code Buddy 中构建自主循环系统
date: 2026-06-22
source: raw/2026-06/2026-06-22_Loop Engineering 实践指南：在 Code Buddy 中构建自主循环系统.md
tags: [Loop Engineering, Agent, 自动化, 循环]
---

## 核心问题

单次 Agent 调用只能解决一步任务。真实工作（开发→测试→修复→部署→监控）需要 Agent 在多个步骤间自主循环——检测结果、判断下一步、自动纠错。

## 方法

**Loop Engineering 的核心组件**：

- **感知环**（Sense Loop）：监控输出/状态变化，触发下一步
- **决策环**（Decide Loop）：根据结果判断走哪个分支
- **修复环**（Repair Loop）：失败时自动诊断→修复→重试

**在 Code Buddy 中的应用**：通过 Skill + CLI 构建确定性循环。`while` 循环配 Gate 门禁（类似 Workflow 的步进式披露），每一步验证通过才推进。关键约束：最大循环次数（防无限消耗）、每次循环的 Token 预算、失败时的人机交接点。

## 关键引用

> 「Loop Engineering 是把 Harness 从"单次执行"升级到"持续自主运行"的关键一步。」
