# 知识地图（人工入口）

> **渐进式披露第二层**：可读的知识全景图。看关系、看学习路径、看领域覆盖度。
> 点击任何条目进入 `entries/*.md` 读完整提炼。
> AI 检索请用 INDEX.md。

---

## 知识领域全景

```
AI 工程化实践（19 篇已提炼）
│
├── 一、Harness Engineering（核心方法论）
│   驾驭AI Coding：一份面向团队的Harness Engineering落地规范 → [📖](entries/team-harness-spec.md)
│   开启Harness Engineering探索之旅 → [📖](entries/harness-engineering.md)
│   从AI Coding到Harness Engineering的端到端工程开发实践 → [📖](entries/ai-coding-to-harness.md)
│   从Vibe Coding到Harness—— 一套大仓AI工程化实战 → [📖](entries/vibe-to-harness.md)
│   你的 Harness 工作流真的在进步吗？（Harness Eval）→ [📖](entries/harness-eval.md)
│   Harness不是目的，知识才是护城河 → [📖](entries/knowledge-as-moat.md)
│
├── 二、Skill 设计（Harness 的执行单元）
│   如何写好 Skill：一份终极实战经验手册 → [📖](entries/skill-design-handbook.md)
│   当我把 AI 变成一个"算法"：Skill 工程化设计的心路历程 → [📖](entries/skill-as-algorithm.md)
│   AI Agent & Skill 测评方案及落地实践 → [📖](entries/agent-skill-evaluation.md)
│
├── 三、Agent 架构与治理
│   Agent 治理：用 Hook 堵住 LLM 的偷懒、越权与失忆 → [📖](entries/agent-governance-hook.md)
│   OpenClaw与Hermes：源码里的 AI Agent 架构知识大复盘 → [📖](entries/openclaw-hermes-arch.md)
│   横向拆解六大Agent上下文压缩策略 → [📖](entries/context-compression-survey.md)
│   Loop Engineering 实践指南 → [📖](entries/loop-engineering.md)
│
└── 四、工程实践 & 技术分析
    一篇搞懂 AI Coding Agent 的 Token 成本控制 → [📖](entries/token-cost-control.md)
    五块钱如何花三天（Token 成本控制实践）→ [📖](entries/five-yuan-token.md)
    精打细算虾养成指南：省 Token → [📖](entries/frugal-token.md)
    拆解大模型几项核心操作背后的数学与 Infra 优化逻辑 → [📖](entries/llm-core-operations.md)
    AI Infra入门干货总结：大模型是如何高效推理的 → [📖](entries/ai-infra-inference.md)
    你讲卫生吗？（AI 交互习惯）→ [📖](entries/hygiene-habits.md)
```

---

## 推荐阅读路径

| 想解决的问题 | 推荐阅读顺序 |
|---|---|
| **我刚带团队做 AI Coding，不知道从哪开始** | 开启Harness → 落地规范 → Skill 设计手册 |
| **团队 AI 工作流已经有了，但不知道好不好** | Harness Eval → Agent 治理 → 测评方案 |
| **写了一堆 Skill，效果参差不齐** | Skill 设计手册 → Skill=算法 → 测评方案 |
| **上下文/Token 不够用** | Token 成本控制 → 五块钱实践 → 上下文压缩 |
| **想深入 Agent 架构** | OpenClaw/Hermes 复盘 → Loop Engineering → Agent 治理 |
| **想优化推理成本/延迟** | 大模型算子 → AI Infra 入门 |
| **知识没有沉淀，每次重来** | 知识=护城河 → 端到端实践 |
| **交互习惯需要改进** | 你讲卫生吗 → 精打细算虾 |
