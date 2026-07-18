# 知识索引（AI 入口）

> **渐进式披露第一层**：AI 扫描此文件匹配触发词 → 找到对应条目 → 加载 `entries/*.md` 全文。
> 当前条目数：19

---

## 1. 项目架构

搭建 AI 工程化项目的整体骨架——协议、管线、纪律如何设计。

| 触发词 | 查看条目 |
|---|---|
| Harness 工程化, 工作流不稳定, AI 偷懒, 提效不明显, Vibe Coding | [harness-engineering](entries/harness-engineering.md) |
| 团队 Harness 落地, 团队规范, Rules 基线 | [team-harness-spec](entries/team-harness-spec.md) |
| 端到端全链路, P1-P6, Gate 门禁 | [ai-coding-to-harness](entries/ai-coding-to-harness.md) |
| Vibe Coding, 大仓, Monorepo, 凭感觉写代码 | [vibe-to-harness](entries/vibe-to-harness.md) |
| Agent 架构对比, OpenClaw, Hermes, Gateway, 插件体系 | [openclaw-hermes-arch](entries/openclaw-hermes-arch.md) |

## 2. Skill / Rules 设计

把能力写成可执行的单元——怎么写、怎么编排、怎么让 AI 稳定执行。

| 触发词 | 查看条目 |
|---|---|
| Skill 怎么写, description, 渐进式加载, Few-Shot, 反模式 | [skill-design-handbook](entries/skill-design-handbook.md) |
| Agent=算法, CLI 接管确定性, Workflow, Gate, 步进式披露 | [skill-as-algorithm](entries/skill-as-algorithm.md) |
| Loop, 自主循环, Sense-Decide-Repair | [loop-engineering](entries/loop-engineering.md) |

## 3. 工具与集成

MCP、CLI、外部 API 怎么接入，工具怎么管理。

| 触发词 | 查看条目 |
|---|---|
| *待补充：MCP、CLI 工具设计、API 集成 | — |

## 4. 记忆与知识

AI 怎么记住该记住的事——知识库架构、知识沉淀流程、记忆系统。

| 触发词 | 查看条目 |
|---|---|
| 知识沉淀, 知识库, Delta Spec, changes-sync, 归档 | [knowledge-as-moat](entries/knowledge-as-moat.md) |
| 交互习惯, 上下文管理, 信噪比, 任务隔离 | [hygiene-habits](entries/hygiene-habits.md) |

## 5. 护栏与安全

怎么防 AI 偷懒、越权、失忆——Hook、HITL、沙箱。

| 触发词 | 查看条目 |
|---|---|
| Hook, 护栏, 越权, HITL, offload, 上下文失忆 | [agent-governance-hook](entries/agent-governance-hook.md) |

## 6. 评估与测试

怎么知道 AI 干得好不好——测评方案、回归测试、评分体系。

| 触发词 | 查看条目 |
|---|---|
| Agent 测评, 评分器, Rubric, 确定性评分 | [agent-skill-evaluation](entries/agent-skill-evaluation.md) |
| Harness Eval, 回归评测, 工作流评估 | [harness-eval](entries/harness-eval.md) |

## 7. 成本与性能

Token 怎么省、上下文怎么管、模型怎么选、压缩策略怎么定。

| 触发词 | 查看条目 |
|---|---|
| Token 成本, 模型选择, 上下文管理, 三层漏斗 | [token-cost-control](entries/token-cost-control.md) |
| Token 系统化治理, 会话管理, 看板告警 | [five-yuan-token](entries/five-yuan-token.md) |
| 省 Token 实践, 小步快跑, 脚本替代 LLM | [frugal-token](entries/frugal-token.md) |
| 上下文压缩, 四级水位线, compaction, 摘要 | [context-compression-survey](entries/context-compression-survey.md) |

## 8. 底层原理

推理怎么跑、算子怎么优化——数学与 Infra 层面的理解。

| 触发词 | 查看条目 |
|---|---|
| 推理优化, vLLM, Continuous Batching, PagedAttention, KV Cache | [ai-infra-inference](entries/ai-infra-inference.md) |
| RoPE, GQA, SwiGLU, Flash Attention, RMSNorm | [llm-core-operations](entries/llm-core-operations.md) |
