---
title: AI Infra入门干货总结：大模型是如何高效推理的
date: 2026-05-25
source: raw/2026-05/2026-05-25_AI Infra入门干货总结：大模型是如何高效推理的.md
tags: [推理优化, vLLM, Continuous Batching, PagedAttention, KV Cache]
---

> 作者：binnnliu（腾讯程序员）

## 核心问题

「看了很多文章以为理解了大模型工作原理，直到看了 vLLM 代码，发现很多地方理解得太过表面。」LLM 推理的核心矛盾：每个请求的输出序列长度不可预测且差异巨大，传统 request-level 调度造成 GPU 利用率低下。

## 方法

<table>
<tr><th>维度</th><th>内容</th></tr>

<tr><td><strong>Continuous Batching</strong></td>
<td>

**核心思路：将调度从 request level 下沉到 token level。**

在 vLLM 调度器视角中，不区分 Prefill 和 Decode 阶段。每个请求只有两个状态：`num_computed_tokens`（已计算 token 数）和 `num_tokens`（当前总共 token 数）。每一步调度的目标就是让 `num_computed_tokens` 追上 `num_tokens`。

受 4 个硬性约束：最大并发请求数、token budget（单步最多计算 token 数）、模型最大序列长度、空闲 KV Cache blocks。

</td></tr>

<tr><td><strong>PagedAttention</strong></td>
<td>

**核心思路：每个请求的 KV Cache 按 token 级别动态分配，用地址数组（block table）维护。**

vLLM 启动时申请 KV Cache，每层 shape 为 `[num_blocks, block_size, num_kv_heads, head_dim]`。block_table 记录每个请求分配的物理块 ID。

推理时通过 `slot_mapping` 告诉 kernel 把 KV 写到哪个 slot，通过 `block_table` 告诉 kernel 去哪些物理块读取 KV Cache。

> 「PagedAttention 的虚拟页表机制解决了显存碎片问题，极大提升 GPU 显存利用率，是支撑 Continuous Batching 高性能推理的基础。」

**Trade-off**：block_table 间接寻址打破物理连续性，跨 block 读取触发离散访存。vLLM 通过合理 block_size（默认 16）缓解——block 内保证连续访存。

</td></tr>

<tr><td><strong>推理全流程（Llama 3 为例）</strong></td>
<td>

1. **Tokenize**：BPE 分词，主流 LLM 全部使用
2. **Embedding Lookup**：查表操作，Token ID → `[num_sched_tokens, hidden_size]` 特征矩阵
3. **RMSNorm + QKV 投影**：Query 向量拆分多头（含 GQA 处理，`num_kv_heads < num_heads`），RoPE 位置编码只对部分维度旋转（`head_dim - rope_dim` 不处理）
4. **Flash Attention / MLA**：优化显存与计算的核心算子
5. **O 投影 + RMSNorm + FFN**：SwiGLU 激活（多一个 gate_proj 权重）
6. **lm_head + Sampler**：非投机解码模式下一次只预测 1 个 token

</td></tr>

<tr><td><strong>KV Cache 优化</strong></td>
<td>

KV Cache 是推理显存占用的核心大头，`(2 * layers * num_kv_heads * head_dim * max_tokens * dtype_size)` 字节。

优化手段：Prefix Caching（共享前缀复用 Cache）、FP8 KV Cache 量化（显存砍半、精度损耗可控）、Multi-Turn 场景下多轮复用。

</td></tr>

<tr><td><strong>PD 分离（Prefill-Decode Disaggregation）</strong></td>
<td>

Prefill（计算密集、latency-sensitive）和 Decode（访存密集）对硬件需求截然不同。PD 分离将两者部署在不同 GPU 上专用优化，Prefill 节点不维护完整 KV Cache（ReduceMemoryOverhead≈100%），Decode 节点专注低延迟自回归。代价是跨节点 KV Cache 传输的网络开销。

</td></tr>

</table>

## 关键引用

> 「有没有可能将调度的从 request level 下沉到 token level 呢？恭喜你发明了 continuous batching。」

> 「系统设计从来都是 Trade-off。相比于因显存碎片导致的 OOM，牺牲少部分访存带宽换取整个系统吞吐量的大幅跃升，是划算的。」
