---
okf_version: "0.1"
---

# AI 实践知识库

腾讯技术工程公众号文章的知识提炼，按搭建 AI 项目的流程组织为 8 个模块。
当前条目数：19

## 1. 项目架构

搭建 AI 工程化项目的整体骨架——协议、管线、纪律如何设计。

* [开启 Harness Engineering 探索之旅](entries/harness-engineering.md) - AI 出码快但整体节奏没跟上——三个根因与 Harness 工程化方案
* [团队 Harness 落地规范](entries/team-harness-spec.md) - 团队级 Rules 基线、Spec 驱动的协作模式
* [从 AI Coding 到 Harness Engineering](entries/ai-coding-to-harness.md) - P1-P6 端到端全链路与 Gate 门禁体系
* [从 Vibe Coding 到 Harness](entries/vibe-to-harness.md) - 大仓 Monorepo 环境下从凭感觉写代码到工程化
* [OpenClaw 与 Hermes 架构对比](entries/openclaw-hermes-arch.md) - Agent 框架的 Gateway、插件体系、部署模式对比

## 2. Skill / Rules 设计

把能力写成可执行的单元——怎么写、怎么编排、怎么让 AI 稳定执行。

* [Skill 编写终极手册](entries/skill-design-handbook.md) - Skill 编写最佳实践：description、渐进式加载、Few-Shot、反模式
* [Skill 工程化设计](entries/skill-as-algorithm.md) - Agent 即算法——CLI 接管确定性、Workflow、Gate、步进式披露
* [Loop Engineering 实践指南](entries/loop-engineering.md) - 自主循环设计——Sense-Decide-Repair 范式

## 3. 工具与集成

MCP、CLI、外部 API 怎么接入，工具怎么管理。

*暂无内容*

## 4. 记忆与知识

AI 怎么记住该记住的事——知识库架构、知识沉淀流程、记忆系统。

* [知识才是护城河](entries/knowledge-as-moat.md) - 知识沉淀流程：Delta Spec、changes-sync、归档策略
* [AI 交互习惯的工程化](entries/hygiene-habits.md) - AI 交互习惯：上下文管理、信噪比、任务隔离

## 5. 护栏与安全

怎么防 AI 偷懒、越权、失忆——Hook、HITL、沙箱。

* [Agent 治理：Hook 堵漏](entries/agent-governance-hook.md) - 用 Hook 堵住 LLM 的偷懒、越权与失忆

## 6. 评估与测试

怎么知道 AI 干得好不好——测评方案、回归测试、评分体系。

* [Agent & Skill 测评方案](entries/agent-skill-evaluation.md) - Agent 与 Skill 测评方案：Rubric 评分器、确定性评分
* [Harness Eval](entries/harness-eval.md) - Harness Eval 回归评测——用考试检验工作流是否真的在进步

## 7. 成本与性能

Token 怎么省、上下文怎么管、模型怎么选、压缩策略怎么定。

* [Token 成本控制](entries/token-cost-control.md) - Token 成本控制：模型选择、上下文管理、三层漏斗策略
* [五块钱花三天](entries/five-yuan-token.md) - Token 系统化治理：五块钱花三天的会话管理与看板告警
* [省 Token 心法](entries/frugal-token.md) - 省 Token 实战心法：小步快跑、脚本替代 LLM
* [上下文压缩策略](entries/context-compression-survey.md) - 六大 Agent 上下文压缩策略横向拆解

## 8. 底层原理

推理怎么跑、算子怎么优化——数学与 Infra 层面的理解。

* [大模型高效推理](entries/ai-infra-inference.md) - 大模型推理优化：vLLM、Continuous Batching、PagedAttention、KV Cache
* [核心算子拆解](entries/llm-core-operations.md) - LLM 核心算子拆解：RoPE、GQA、SwiGLU、Flash Attention、RMSNorm
