# 知识地图（人工入口）

> **按搭项目的流程组织**：从骨架→能力→工具→记忆→安全→评估→成本→原理，每一步解决一类问题。
> AI 检索请用 INDEX.md。

---

## 1. 项目架构（5 篇）

搭骨架——协议、管线、纪律怎么设计。Harness Engineering 方法论体系。

- [开启 Harness Engineering 探索之旅](entries/harness-engineering.md) — 四层骨架 + 四条工程原则
- [团队 Harness 落地规范](entries/team-harness-spec.md) — 团队级别怎么制定 Rules/Skills 基线
- [端到端工程实践](entries/ai-coding-to-harness.md) — P1-P6 全链路 Harness 落地
- [Vibe Coding → Harness](entries/vibe-to-harness.md) — 大仓 Monorepo 场景的转型实践
- [OpenClaw vs Hermes 架构对比](entries/openclaw-hermes-arch.md) — 两套 Agent 框架源码级拆解

## 2. Skill / Rules 设计（3 篇）

能力怎么写——Skill 设计方法、编排机制、自循环系统。

- [Skill 设计实战手册](entries/skill-design-handbook.md) — description/Few-Shot/反模式
- [Skill = 算法](entries/skill-as-algorithm.md) — CLI 接管确定性 + Workflow 编排
- [Loop Engineering](entries/loop-engineering.md) — Sense→Decide→Repair 自主循环

## 3. 工具与集成

MCP、CLI、外部 API 怎么接入——工具层设计。

> *待补充：MCP 协议、CLI 工具设计、外部服务对接*

## 4. 记忆与知识（2 篇）

AI 怎么记住该记住的——知识库架构、知识沉淀、记忆管理。

- [知识才是护城河](entries/knowledge-as-moat.md) — changes-sync + knowledge-sync + Delta Spec
- [你讲卫生吗](entries/hygiene-habits.md) — 交互习惯：任务隔离、信噪比、明确指令

## 5. 护栏与安全（1 篇）

防翻车——Hook 体系、HITL 门禁、沙箱隔离。

- [Agent 治理：用 Hook 堵](entries/agent-governance-hook.md) — 长文本 offload + HITL + 上下文联动闭环

## 6. 评估与测试（2 篇）

怎么知道做得好不好——测评、评分、回归。

- [Agent & Skill 测评方案](entries/agent-skill-evaluation.md) — 三类评分器 + 五大评测维度
- [Harness Eval](entries/harness-eval.md) — 可回归的闭环评测系统

## 7. 成本与性能（4 篇）

Token 怎么省、上下文怎么管、模型怎么选。

- [Token 成本控制](entries/token-cost-control.md) — 三层漏斗：习惯→工具→架构
- [五块钱如何花三天](entries/five-yuan-token.md) — Token 系统化治理
- [精打细算虾指南](entries/frugal-token.md) — 省 Token = 把 AI 用好
- [六大上下文压缩策略](entries/context-compression-survey.md) — 四级水位线方案

## 8. 底层原理（2 篇）

推理怎么跑、算子怎么优化——数学与 Infra 原理。

- [AI Infra 入门](entries/ai-infra-inference.md) — Continuous Batching / PagedAttention / PD 分离
- [大模型核心算子](entries/llm-core-operations.md) — RoPE / GQA / SwiGLU / Flash Attention

---

## 推荐阅读路径

| 场景 | 阅读顺序 |
|---|---|
| 从零搭一个 AI 工程化项目 | 1→2→4→5→6→7 |
| 团队已有的 AI Coding 想升级 | 1→6→5→7 |
| Skill 写了但效果差 | 2→6→7 |
| Token 账单控制不住 | 7→1（上下文管理部分）|
| 想深入 Agent 技术细节 | 8→5→1 |
