---
title: 拆解大模型几项核心操作背后的数学与 Infra 优化逻辑
date: 2026-06-17
source: raw/2026-06/2026-06-17_拆解大模型几项核心操作背后的数学与 Infra 优化逻辑.md
tags: [推理优化, RoPE, GQA, SwiGLU, Flash Attention]
---

> 作者：binnnliu

## 核心问题

大模型推理慢、显存贵，性能瓶颈集中在几个核心算子。理解这些算子的原理和优化逻辑是 AI Infra 的必修课。

## 方法

| 操作 | 作用 | 优化手段 | 关键数字 |
|------|-----|---------|---------|
| **RoPE** | 位置编码，让模型感知 token 顺序 | 只对部分维度旋转（`head_dim - rope_dim` 不处理），减少计算 | Qwen 系列 `rope_dim=64`, `head_dim=128` |
| **GQA** | 减少 KV Cache 显存 | KV head 数 < Q head 数，通过 `repeat_kv` 广播对齐 | Llama 3 70B：8 KV heads / 64 Q heads |
| **SwiGLU** | FFN 激活函数 | 多一个 `gate_proj` 权重，比 ReLU 效果更好 | 3 个权重矩阵（gate/up/down）|
| **Flash Attention** | 优化显存和计算 | 分块计算 + 不存储中间矩阵 + 反向重算 | 显存 O(n) 而非 O(n²) |
| **RMSNorm** | 归一化层 | 相比 LayerNorm 去掉中心化，只做缩放 | 更快，效果相当 |

**RoPE 的核心公式**：旋转矩阵只作用于相邻维度对 `(0,1), (2,3)...`，不处理 `rope_dim` 之后的维度。高频组精细感知局部位置、低频组保留远端语义。

**GQA 的显存节省**：KV Cache 大小 = `2 * layers * num_kv_heads * head_dim * max_tokens * dtype`。从 MHA 切换到 GQA（如 8 KV heads vs 32 Q heads），KV Cache 减少到原来的 1/4。

## 关键引用

> 「理解张量维度的每一步变化，才能真正理解优化到底优化了什么。」
