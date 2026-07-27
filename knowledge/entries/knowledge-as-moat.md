---
type: Article
title: Harness不是目的，知识才是护城河
description: 知识沉淀流程：Delta Spec、changes-sync、归档策略
date: 2026-05-11
source: raw/2026-05/2026-05-11_Harness不是目的，知识才是护城河 —— 一个AI工程交付团队的知识沉淀实践.md
tags: [knowledge-management, harness, engineering]
timestamp: 2026-05-11T00:00:00+08:00
---

## 适用场景

- 团队知识散落在人脑 / Wiki / TAPD，每次做相似需求 AI 从零开始
- Harness 让你跑得快但知识没有积累成「更快」
- 想建立自动化的知识沉淀机制（changes-sync / knowledge-sync）
- 需要说服团队：工具不是护城河，知识才是

## 核心问题

「团队有了 Harness 工作流，交付效率提升了，但一个新问题浮现了：知识去哪了？」

Harness 让你跑得快，但每次变更产生的设计决策、踩坑经验、接口契约如果只留在 TAPD/Wiki/人脑里，下次相似需求来 AI 从零开始。"快"没有积累成"更快"。

## 方法

**知识沉淀三件套**：每次交付结束强制跑

1. **changes-sync**：git 实际改动与 design/planning 文档对齐（代码做了什么=文档说了什么），不一致就更新
2. **knowledge-sync**：本次变更中反复用到的设计/踩坑/契约→提炼进知识库
3. **specs-generator**：按 ADDED/MODIFIED/REMOVED/RENAMED 四类标记增量更新 specs 索引，避免全量复制导致膨胀

**Delta Spec 是灵魂**：不复制全部文档进 specs，只标记"哪些变了"→增量合并。

## 关联概念

- 前置：[Harness Engineering](harness-engineering.md) — 知识层是四层骨架的第四层
- 配合：[端到端全链路](ai-coding-to-harness.md) — P6 归档阶段的实现
- 配合：[AI 交互习惯](hygiene-habits.md) — 知识卫生是交互卫生的延伸

## 关键引用

> 「Harness 让你跑得快，知识让你跑得越来越快。没有知识沉淀的 Harness，只是一条越来越快的传送带。」
