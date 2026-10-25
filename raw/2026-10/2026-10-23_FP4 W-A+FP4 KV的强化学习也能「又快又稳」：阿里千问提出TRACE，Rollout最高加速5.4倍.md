---
title: FP4 W/A+FP4 KV的强化学习也能「又快又稳」：阿里千问提出TRACE，Rollout最高加速5.4倍
date: 2026-10-23
source: https://mp.weixin.qq.com/s?__biz=MzA3MzI4MjgzMw==&amp;mid=2651069672&amp;idx=3&amp;sn=6b461b4dbff4fd3f156ce081b60ac69e
account: 机器之心
fetched_at: 2026-10-25 18:00:04 CST
article_id: 6b461b4dbff4fd3f156ce081b60ac69e
---

机器之心 2026-10-23 19:06 北京

  
  
*[图片]*

  
用 Rollout 侧真实的 FP4 量化结果，反过来指导训练侧的舍入方向。

  
*[图片：图片]*

大模型强化学习越来越「吃算力」，最昂贵的环节之一正是 Rollout。把 Rollout 从 BF16 压到 FP4，理论上可以显著降低计算和显存开销，但问题也随之而来 —— 训练端与 Rollout 端即使面对非常接近的数值，也可能因为 FP4 的离散量化边界而落到不同码点，最终把微小的数值误差放大成策略偏差导致训练崩溃。

阿里千问联合俄亥俄州立大学的研究团队提出了 TRACE。它的核心思路并不是继续分别提高训练端和 Rollout 端的量化精度，而是直接减少两条低精度执行路径之间的差异：用 Rollout 侧真实的 FP4 量化结果，反过来指导训练侧的舍入方向。在 Qwen3.5-35B-A3B、Qwen3.5-122B-A10B、Qwen3.8-Flash-Next 以及 Qwen3.8-2.4T-A95B 四个 MoE 模型上，TRACE 可以在联合 FP4 W/A 与 FP4 KV Cache Rollout 的设置下，将最终性能拉回到 BF16 Rollout 附近，同时在 128K 输出长度下 rollout 获得最高 5.4× 的解码吞吐提升。

*[图片]*

- 论文标题：TRACE: Rollout-Guided Quantization-Aware Training for FP4 Reinforcement Learning of MoE Language Models
- ArXiv 链接：https://arxiv.org/abs/2610.07767
- Huggingface 链接：https://huggingface.co/papers/2610.07767

为什么 FP4 Rollout 会把 RL 训练「搞崩」？

低精度 Rollout 的吸引力很直接：rollout 阶段通常占据 RL 大量时间，尤其当轨迹长度扩展到数万甚至数十万 token 时，低精度计算和低精度 KV Cache 能显著降低成本。相比 FP8，FP4 更激进，也意味着更大的潜在加速空间。但 FP4 的问题也更尖锐。现有方法通常关注「量化后的值离原始高精度值有多近」，也就是分别降低训练路径和 Rollout 路径的量化误差。TRACE 的作者指出，这并不等价于降低两条路径之间的差异。两个值都可以各自量得很准，却仍然被量化到不同码点。

*[图片]*

图 1：微小的 BF16 差异跨过 FP4 舍入边界后，可能被放大成显著的低精度差异。

论文给出了一个直观例子：训练侧激活为 60.24，Rollout 侧为 59.76，两者原本只差 0.48；经过相同的 global scale 和 block scale 后，归一化值分别变成 2.51 和 2.49。因为它们恰好位于舍入边界两侧，一个被量化到 3，一个被量化到 2，最终差异被放大到 24。对 MoE 模型而言，这类偏差尤其棘手：数值变化还可能影响 router 分数和专家选择，使训练策略与生成轨迹对应的策略进一步偏离。实验中，所有的 baseline 方法，包括普通 FP4 QAT、QaRL 和 QUADS 都出现了训练后期奖励与测试分数明显下滑甚至崩溃的现象。

*[图片]*

图 2：在 Qwen3.5-35B-A3B 上，FP4 QAT/QUADS/QaRL 出现性能下降，TRACE 保持稳定，并逐步和 BF16 持平。

TRACE 核心：

别只管「量得准」

直接让训练侧向 Rollout 的量化结果对齐

TRACE 的第一个设计是 Rollout-Guided Quantization-Aware Training。在 Rollout 阶段，系统记录 FP4 routed expert 激活和 FP4 KV 状态对应的量化结果；到了后续训练阶段，这些信息不再只是「历史数据」，而是直接参与训练侧 fake quantization 的舍入决策。具体来说，对于训练侧某个待量化值，TRACE 仍然只在相邻的两个 FP4 E2M1 码点之间选择，但不再机械使用标准 round-to-nearest （RTN）。它会优先选择距离 Rollout 侧实际码点更近的那个候选值。

*[图片]*

图 3：TRACE 总体流程。Rollout 侧保存紧凑量化信息，训练侧加载后用于调整 FP4 舍入。

然而，直接保存完整的 Rollout 量化结果并不便宜。这些信息需要经历 GPU→CPU、CPU 缓存、磁盘写入 / 读取，再在训练时回到 GPU；长轨迹、大 batch 和异步 RL 都会放大存储与通信压力。TRACE 的第二个设计，正是把「需要传什么」压到最少。作者统计发现，超过 99% 的训练 /rollout 量化不一致只相差一个相邻 FP4 codebook entry。既然训练侧自身的激活值已经把候选范围压得很小，那么 Rollout 侧没必要把完整低精度值全部传过去；保留少量 mantissa 信息，加上 scale，通常就足够告诉训练侧应该朝哪个方向舍入。

实验效果

在 Qwen3.5-35B-A3B 的 RL 任务上，TRACE 的平均分达到 75.3。作为对照，BF16 Rollout 为 74.9，普通 QAT 为 59.6，QaRL 为 58.6，QUADS 为 68.8。尤其在 HMMT25 上，TRACE 从 QUADS 的 59.0 提升到 70.0。

*[图片]*

论文专门测了 Rollout 吞吐和端到端 RL step time。结果显示，如果保存完整指导信息，通信开销确实会严重拖慢 Rollout；而采用紧凑缓存后，TRACE 的吞吐基本贴近原生 FP4 Rollout。在 8K 输入、128K 输出时，解码吞吐相对 BF16 Rollout 最高提升 5.4×。端到端来看，联合 FP4 Rollout 的 RL step time 中 TRACE 仅产生约 7.4% 的额外开销。

一个更有意思的现象：

模型会在 RL 中「适应」FP4

TRACE 的实验里还有一个很值得关注的现象：在训练早期，FP4 执行仍会带来性能损失；但只要 train-rollout discrepancy 被控制住，模型会逐步适应这个低精度执行环境。

*[图片]*

*[图片]*

图 4：TRACE 的性能适应现象，左图为 Qwen3.5-35B-A3B，右图为 Qwen3.8-Flash-Next

在 Qwen3.5-35B-A3B 的 HMMT25 曲线上，TRACE 大约在 120 个 RL step 后追上 BF16；在 Qwen3.8-Flash-Next 上，类似的「追平」 出现在约 240 step。这意味着低精度并不一定只能被看作训练中的静态噪声。若训练与生成使用的是一致、可学习的低精度环境，策略本身可能通过 RL 更新逐步适应这种数值约束。这一点也体现在最终 FP4 policy 的质量上。如果先用 BF16 Rollout 完成 RL，再做事后量化，Vanilla NVFP4、4over6 和 H-Scale 的平均分分别是 70.4、71.0 和 71.4；而 TRACE 从训练过程中就使用联合 FP4 Rollout，最终 FP4 policy 的平均分达到 75.3。

*[图片：图片]*

© THE END

转载请联系本公众号获得授权

投稿或寻求报道：liyazhou@jiqizhixin.com

[跳转微信打开](https://wechat2rss.xlab.app/link-proxy/?k=d5d2c750&r=1&u=https%3A%2F%2Fmp.weixin.qq.com%2Fs%3F__biz%3DMzA3MzI4MjgzMw%3D%3D%26mid%3D2651069672%26idx%3D3%26sn%3D6b461b4dbff4fd3f156ce081b60ac69e)
