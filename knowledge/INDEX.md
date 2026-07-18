# 知识索引（AI 入口）

> **渐进式披露第一层**：AI 扫描此文件匹配触发词 → 找到对应条目 → 加载 `entries/*.md` 全文。
> 当前条目数：19

---

## 速查表：我遇到 X → 看 Y

| 我遇到的问题 / 场景 | 触发词 | 查看条目 |
|---|---|---|
| AI Coding 提效不明显 / 团队靠主观感觉迭代 / AI 偷懒跳过步骤 / 想从 Vibe Coding 升级到工程化 | Harness, 工程化, 工作流不稳定, 偷懒, Fixed Flow | [harness-engineering](entries/harness-engineering.md) |
| Agent 长文本截断略写 / 未授权操作 / 改表不查风险 / 产出不汇报 | Hook, 护栏, 越权, HITL, offload, 上下文失忆 | [agent-governance-hook](entries/agent-governance-hook.md) |
| Skill 写了效果不好 / 不知道怎么组织 / 想写但不知从哪开始 | Skill, description, 渐进式加载, SKILL.md, 结构化 Prompt | [skill-design-handbook](entries/skill-design-handbook.md) |
| Agent 规则越多越不听话 / 想让 AI 输出确定可预期 / 工具多了上下文爆炸 | CLI, 状态机, Workflow, Gate, 步进式披露 | [skill-as-algorithm](entries/skill-as-algorithm.md) |
| LLM 推理慢/显存贵 / 想理解 vLLM 原理 | 推理优化, vLLM, Continuous Batching, PagedAttention, KV Cache | [ai-infra-inference](entries/ai-infra-inference.md) |
| 想了解 Agent 框架架构设计 / 多通道接入 / 记忆系统 | Agent架构, OpenClaw, Hermes, Gateway, 插件 | [openclaw-hermes-arch](entries/openclaw-hermes-arch.md) |
| 长对话质量下降 / 上下文窗口不够用 / 需要压缩策略对比 | 上下文压缩, Token优化, 摘要, compaction | [context-compression-survey](entries/context-compression-survey.md) |
| Token 烧太快 / 想系统化降本 / 不知道怎么选模型 | Token, 成本控制, 模型选择, 上下文管理 | [token-cost-control](entries/token-cost-control.md) |
| Agent/Skill 不知道怎么评估好坏 / 想建立测评体系 | 测评, 评分器, Rubric, Agent评估 | [agent-skill-evaluation](entries/agent-skill-evaluation.md) |
| 大模型算子原理 / RoPE/GQA/SwiGLU 怎么优化 | RoPE, GQA, SwiGLU, Flash Attention, RMSNorm | [llm-core-operations](entries/llm-core-operations.md) |
| Harness 工作流不知道是在进步还是退步 / 想建立回归评测 | Harness Eval, 评测, 回归 | [harness-eval](entries/harness-eval.md) |
| 想让 Agent 自主循环执行多步任务 / 失败自动修复 | Loop, 循环, 自主, 自动化 | [loop-engineering](entries/loop-engineering.md) |
| AI 交互习惯差 / 上下文管理脏乱 / 长 session 不换 | 交互习惯, 上下文管理, 信噪比, GIVEN-WHEN-THEN | [hygiene-habits](entries/hygiene-habits.md) |
| 知识没有系统沉淀 / 人走经验丢 / 每次新任务 AI 从零开始 | 知识管理, 知识库, Delta Spec, 归档 | [knowledge-as-moat](entries/knowledge-as-moat.md) |
| Token 优化实践 / Token 用量的度量和管理 | Token, 成本控制, 会话管理, 看板 | [five-yuan-token](entries/five-yuan-token.md) |
| 端到端全链路 AI 工程化实践 | 端到端, P1-P6, Gate, 全链路 | [ai-coding-to-harness](entries/ai-coding-to-harness.md) |
| 从 Vibe Coding/凭感觉写代码过渡到工程化 | Vibe Coding, Harness, 大仓, Monorepo | [vibe-to-harness](entries/vibe-to-harness.md) |
| 省 Token 的具体实践 / Token 浪费的根本原因 | Token, 成本, 小步快跑, 脚本替代LLM | [frugal-token](entries/frugal-token.md) |
| 团队层面 Harness 怎么落地 / 制定团队规范 | 团队规范, 落地, Rules, Skill | [team-harness-spec](entries/team-harness-spec.md) |

---

## 条目目录

- [harness-engineering](entries/harness-engineering.md) — 不教模型"怎么回答"，而是设计模型"怎么工作"
- [agent-governance-hook](entries/agent-governance-hook.md) — 用 Hook 切面在框架层确定性兜底 LLM 的偷懒、越权、失忆
- [skill-design-handbook](entries/skill-design-handbook.md) — 结构化 Prompt Engineering：description 写法、Few-Shot、反模式
- [skill-as-algorithm](entries/skill-as-algorithm.md) — Agent = 算法：CLI 接管确定性，Workflow 编排不确定性
- [ai-infra-inference](entries/ai-infra-inference.md) — vLLM 推理优化：Continuous Batching、PagedAttention、PD 分离
- [openclaw-hermes-arch](entries/openclaw-hermes-arch.md) — OpenClaw vs Hermes 源码级架构对比
- [context-compression-survey](entries/context-compression-survey.md) — 六大 Agent 上下文压缩策略横向拆解 + 四级水位线方案
- [token-cost-control](entries/token-cost-control.md) — AI Coding Agent 的 Token 成本控制三层漏斗
- [agent-skill-evaluation](entries/agent-skill-evaluation.md) — 三类评分器 + 五维度的 Agent 测评方案
- [llm-core-operations](entries/llm-core-operations.md) — RoPE/GQA/SwiGLU/Flash Attention 的原理与优化
- [harness-eval](entries/harness-eval.md) — Harness Eval：可回归的闭环评测系统
- [loop-engineering](entries/loop-engineering.md) — Loop Engineering：Sense→Decide→Repair 自主循环
- [hygiene-habits](entries/hygiene-habits.md) — AI 交互习惯：任务隔离、信噪比优先、明确指令
- [knowledge-as-moat](entries/knowledge-as-moat.md) — 知识才是护城河：changes-sync + knowledge-sync + Delta Spec
- [five-yuan-token](entries/five-yuan-token.md) — Token 成本系统化治理：三层降本策略
- [ai-coding-to-harness](entries/ai-coding-to-harness.md) — 端到端工程开发实践：P1-P6 全链路
- [vibe-to-harness](entries/vibe-to-harness.md) — 从 Vibe Coding 到 Harness：大仓 AI 工程化
- [frugal-token](entries/frugal-token.md) — 精打细算虾指南：省 Token = 把 AI 用好
- [team-harness-spec](entries/team-harness-spec.md) — 面向团队的 Harness Engineering 落地规范
