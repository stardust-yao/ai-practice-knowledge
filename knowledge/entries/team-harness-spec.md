---
title: 驾驭AI Coding：一份面向团队的Harness Engineering落地规范
date: 2026-07-17
source: raw/2026-07/2026-07-17_驾驭AI Coding：一份面向团队的Harness Engineering落地规范.md
tags: [Harness, 团队规范, 工程化]
---

## 核心问题

Harness Engineering 的概念有了，但团队层面怎么落地？需要一个"团队章程"级别的规范文档——不是某个人的 Rules，而是整个团队的 Harness 基线。

## 方法

**团队 Harness 规范的四层结构**：

1. **全局 Rules**（所有项目遵守）：安全红线、编码底线、Git 规范
2. **项目级 Skill**（按需触发）：项目特定的迁移流程、部署规范、测试模板
3. **知识库**（团队共享）：业务规则、架构决策、接口契约、术语表
4. **评估与演进**：定期跑 Harness Eval 回归，规则过时了就更新

**核心原则**：规范不是"写一次就完"，是要在每次交付后持续演进——通过 P6 归档阶段的 knowledge-sync 自动沉淀。

## 关键引用

> 「规范不是束缚——是让整个团队用同一套语言和 AI 协作。」
