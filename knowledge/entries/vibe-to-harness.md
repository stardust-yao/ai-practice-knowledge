---
title: 从Vibe Coding到Harness — 一套大仓AI工程化实战
date: 2026-07-07
source: raw/2026-07/2026-07-07_从Vibe Coding到Harness—— 一套大仓AI工程化实战.md
tags: [Harness, Vibe Coding, 大仓]
---

## 核心问题

「Vibe Coding」——凭感觉让 AI 写代码，爽在 Demo 阶段，翻车在生产环境。大仓（Monorepo）场景下问题放大：多服务共享代码、跨模块依赖、AI 改一处引发连锁反应。

## 方法

大仓 Harness 的特殊要求：

- **依赖感知**：AI 改代码前先分析跨模块影响范围
- **增量变更**：大仓不能全量分析，diff 驱动的改动点识别
- **分层 Skill**：不同服务/模块有各自的 Skill，但共享基础 Rules
- **统一 Gate**：跨服务的变更用一个评分卡校验一致性

**核心转型**：从"AI 你帮我写这个"→"AI 你按这个规范跑完整条链路"。

## 关键引用

> 「Vibe Coding 到 Harness 的转变，是从『AI 你帮帮我』到『AI 你按规矩干活』的转变。」
