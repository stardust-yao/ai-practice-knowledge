# Concept 标准模板

> 协议层第一项——每个 Concept 文档的产出格式和填写契约。
> 模板不是建议，是契约。偏离模板的段落不会被自动校验通过。

---

## Frontmatter 字段

| 字段 | 必填 | 格式约束 | 填写说明 |
|------|------|---------|---------|
| `type` | ✅ | 固定值 `Article` | 当前所有内容均为公众号文章提炼 |
| `title` | ✅ | 原文标题 | 从 raw/ 原文复制，不修改措辞 |
| `description` | ✅ | 一句话，≤80 字 | 回答「这篇文章解决什么问题」。用于 index.md 条目和检索匹配。不要复述标题 |
| `date` | ✅ | `YYYY-MM-DD` | 原文发布日期 |
| `source` | ✅ | `raw/YYYY-MM/YYYY-MM-DD_标题.md` | 指向 raw/ 原文路径，不用绝对路径 |
| `tags` | ✅ | 小写英文，逗号分隔，3-6 个 | 从模块关键词和文章核心方法中提取。不用中文、不用驼峰、不用空格 |
| `timestamp` | ✅ | ISO 8601 `YYYY-MM-DDTHH:MM:SS+08:00` | 最后修改时间。新增时等于 date，修改时更新 |

### description 写法

```
✅  解析了 AI 出码快但整体效率没提升的三个根因，提出四层 Harness 骨架方案
❌  这篇文章讲了 Harness Engineering 的概念
❌  开启Harness Engineering探索之旅  （← 这等于复制标题，没提供新信息）
```

### tags 写法

```
✅  [harness-engineering, methodology, engineering]
❌  [Harness Engineering, 方法论, 工程化]
❌  [harness engineering, 方法论]
```

---

## 正文段落

| 段落 | 必填 | 格式约束 | 填写说明 |
|------|------|---------|---------|
| `## 适用场景` | ✅ | 无序列表，3-5 条 | 每条描述一个具体场景，用「你正在…」「你需要…」「当你…」开头。不用抽象描述 |
| `## 核心问题` | ✅ | 1-3 段 | 回答「这篇文章解决了什么问题」。开头引用原文关键句（`>` 引用格式）|
| `## 方法` | ✅ | 无格式约束 | 文章的核心方法和方案。表格优先于长段落 |
| `## 关联概念` | ✅ | 无序列表，≥1 条 | 每条包含关联类型（前置/配合/补充）+ 文件名 + 一句话说明关联原因 |
| `## 关键引用` | ⭕ | 引用格式（`>`），≥1 条 | 从原文中摘取最有价值的判断句或总结句 |

### 适用场景写法

```
✅  - 发现 AI 出码速度快但整体项目节奏没有同步提升
    - 正在搭建 AI 工程化项目，不确定从哪里入手
    - 需要说服团队从 Prompt Engineering 升级到 Harness Engineering

❌  - 工程化相关（太模糊）
    - 所有 AI 项目（太宽泛，等于没说）
    - 腾讯的文章（不是场景）
```

### 关联概念写法

```
✅  - 前置：[Harness Engineering 入门](harness-engineering.md) — 先理解 Harness 基本概念
    - 配合：[端到端全链路](ai-coding-to-harness.md) — Gate 门禁机制的技术实现

❌  - 相关：Harness Engineering
    - 也看看 xxx（没有链接）
    - 配合：skill-as-algorithm.md（没有说明为什么相关）
```

---

## 完整模板

```markdown
---
type: Article
title: [原文标题]
description: [一句话，≤80 字，回答「解决什么问题」]
date: YYYY-MM-DD
source: raw/YYYY-MM/YYYY-MM-DD_[标题].md
tags: [tag1, tag2, tag3]
timestamp: YYYY-MM-DDT00:00:00+08:00
---

> 作者：[原文作者]
> 背景：[如果有特定背景]

## 适用场景

- [场景 1]
- [场景 2]
- [场景 3]

## 核心问题

[1-3 段，开头引用原文关键句]

## 方法

[文章的核心方法，表格优先]

## 关联概念

- [关联类型]：[概念标题](文件名.md) — [一句话说明关联原因]

## 关键引用

> [原文金句 1]

> [原文金句 2]
```
