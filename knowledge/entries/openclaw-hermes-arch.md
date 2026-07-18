---
title: OpenClaw与Hermes：源码里的 AI Agent 架构知识大复盘
date: 2026-05-29
source: raw/2026-05/2026-05-29_OpenClaw与Hermes：源码里的 AI Agent 架构知识大复盘.md
tags: [Agent架构, OpenClaw, Hermes, Gateway, 设计模式]
---

> 作者：rianli（腾讯程序员）

## 核心问题

> 「第一次见 OpenClaw——24/7 后台常驻、跨多 IM 通道无缝流转、有人格长期记忆、自主完成开放性复杂任务。这就是 AI 时代的私人助理操作系统。」

但实际使用后发现：费 token（Bootstrap 每轮 push 几万 token）、健忘（长对话中段断片）、复杂任务交付度低。Hermes 这边也有：多人串扰风险、核心仍是单体、记忆管理半自动。

> 「踩完坑再回头看源码，反而看懂了每个"不完美"背后的工程取舍。」

## 方法

<table>
<tr><th>维度</th><th>内容</th></tr>

<tr><td><strong>OpenClaw：TypeScript 微内核</strong></td>
<td>

**五个核心设计理念**：

1. **本地优先**：不是云服务，是运行在用户设备上的 Gateway 进程。控制平面和状态数据留在本地，仅 LLM 推理请求出站。
2. **万物皆插件**：核心代码只负责编排（消息路由/会话管理/安全网关），所有具体能力以插件形式实现。
3. **安全纵深**：五层递进防御——TLS→Device Identity→命令执行审批→插件安装扫描→沙箱隔离。执行策略默认 deny。
4. **记忆驱动**：静态工作区文件（SOUL/USER/MEMORY.md）+ 向量记忆引擎（混合搜索 + Dreaming 后台整合 + Active Recall）。
5. **配置驱动**：一个 JSON 定义所有行为，支持运行时热重载。

**架构五层**：触达层（Channel Plugin）→ Gateway 路由聚合层 → Agent 执行层（模型+记忆+工具）→ 安全层（沙箱+审批）→ 基础设施层（会话持久化+后台任务调度）。

</td></tr>

<tr><td><strong>OpenClaw 的四个关键设计取舍</strong></td>
<td>

1. **多协议可插拔契约**：Channel 25+ Adapter，统一消息抽象层
2. **LLM 上下文资源预算**：可插拔 Context Engine + 多级 Compaction（有损压缩是权衡）
3. **记忆自动沉淀**：Dreaming 三阶段加权晋升——近期记忆→总结→长期知识
4. **凭证失败与业务失败分治**：网络错误重试 vs 业务错误上报

</td></tr>

<tr><td><strong>Hermes 的补充启示</strong></td>
<td>

1. **经验自动复用**：技能自创建 + 改进闭环（Skill 是 Hermes 的"可复用能力单元"）
2. **Smart Approval 三态**：安全审批先 LLM 分诊（low/medium/high），再按级别决定自动通过/需确认/阻断
3. **8 种沙箱后端**：执行隔离从本地 Docker 到云端 VM，覆盖不同安全等级

</td></tr>

<tr><td><strong>两套方案仍未覆盖的落地难题</strong></td>
<td>

- **记忆分层**：不同生命周期的记忆应该用不同存储策略，当前方案都是扁平化的
- **上下文工程**：融合 Anthropic "上下文焦虑症"与"上下文重置"理论——模型在近端上下文表现好、远端失焦
- **确定性编排**：Workflow 层面的状态机 vs LLM 自由推理的边界
- **多 Agent 协作**：GAN-like 生成-对抗架构、Sprint Contract（Agent 间的交付契约）
- **自我评估偏差的对抗性消除**：LLM 天然倾向给自己打高分，需要独立评估 Agent

</td></tr>

</table>

## 关键引用

> 「Security in OpenClaw is a deliberate tradeoff: strong defaults without killing capability.」

> 「两个都还在路上——但看懂了每个"不完美"背后的工程取舍，才是真正从"看山是山"走到了"看山还是山"。」
