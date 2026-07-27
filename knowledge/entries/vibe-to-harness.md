---
type: Article
title: 从Vibe Coding到Harness — 一套大仓AI工程化实战
description: 大仓 Monorepo 环境下从凭感觉写代码到工程化
date: 2026-07-07
source: raw/2026-07/2026-07-07_从Vibe Coding到Harness—— 一套大仓AI工程化实战.md
tags: [harness, vibe-coding, monorepo]
timestamp: 2026-07-07T00:00:00+08:00
---

## 适用场景

- 目前处于「凭感觉让 AI 写代码」的阶段
- 大仓（Monorepo）环境下 AI 改动引发连锁反应
- Demo 跑得通但一到生产环境就翻车
- 需要从自由式 AI 协作转型到工程化约束

## 核心问题

「Vibe Coding」——凭感觉让 AI 写代码，爽在 Demo 阶段，翻车在生产环境。大仓（Monorepo）场景下问题放大：多服务共享代码、跨模块依赖、AI 改一处引发连锁反应。

## 方法

大仓 Harness 的特殊要求：

- **依赖感知**：AI 改代码前先分析跨模块影响范围
- **增量变更**：大仓不能全量分析，diff 驱动的改动点识别
- **分层 Skill**：不同服务/模块有各自的 Skill，但共享基础 Rules
- **统一 Gate**：跨服务的变更用一个评分卡校验一致性

**核心转型**：从"AI 你帮我写这个"→"AI 你按这个规范跑完整条链路"。

## 关联概念

- 前置：[Harness Engineering 入门](harness-engineering.md) — 理解为什么要工程化
- 配合：[端到端全链路](ai-coding-to-harness.md) — Vibe → Harness 的完整路径
- 配合：[团队 Harness 规范](team-harness-spec.md) — 大仓场景的团队规范设计

## 关键引用

> 「Vibe Coding 到 Harness 的转变，是从『AI 你帮帮我』到『AI 你按规矩干活』的转变。」
