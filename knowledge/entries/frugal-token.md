---
type: Article
title: 精打细算虾养成指南：省 Token 和把 AI 用好，从来就是一件事
description: 省 Token 实战心法：小步快跑、脚本替代 LLM
module: cost-performance
date: 2026-07-08
source: raw/2026-07/2026-07-08_精打细算虾养成指南： 省 Token 和把 AI 用好，从来就是一件事.md
tags: [token, cost-control, practice]
timestamp: 2026-07-08T00:00:00+08:00
---

## 适用场景

- 每步都在优化但总消耗没降下来
- 需要具体可操作、今天就能做的省钱技巧
- 想理解「省 Token = 把 AI 用好」这个核心关系
- 需要简单直接的 Before/After 示例

## 核心问题

> 「省 Token 和把 AI 用好，从来就是一件事。」

Token 浪费的根源不是"用得太多"，而是 AI 在低价值事情上反复消耗——十轮对话才对齐需求、全量扫描无关代码、输出冗长废话。

## 方法

**降低 Token "浪费率" 而非绝对用量**：

- **需求前置对齐**：第一次 prompt 就把边界说清楚，别让 AI 猜
- **小步快跑**：任务拆成小块，每一步 context 小了、出错重跑成本也低了
- **用结构换 Token**：JSON/YAML schema 输入比自然语言省 80%+ Token
- **脚本替代 LLM**：格式化、校验、统计这些用脚本跑，别喂给 AI

## 关联概念

- 前置：[Token 成本控制](token-cost-control.md) — 先看全局框架
- 配合：[五块钱花三天](five-yuan-token.md) — 系统化治理
- 配合：[AI 交互习惯](hygiene-habits.md) — 习惯层面最省钱

## 关键引用

> 「精打细算不是小气——干净的上下文让 AI 注意力集中，少即是多。」
