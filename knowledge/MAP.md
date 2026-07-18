# 知识地图（人工入口）

> **渐进式披露第二层**：这是一个可读的知识全景图。看关系、看学习路径、看领域覆盖度。
> 点击任何条目进入 `entries/*.md` 读完整提炼。
> AI 检索请用 INDEX.md。

---

## 知识领域全景

```
AI 工程化实践（21 篇原文）
│
├── 一、Harness Engineering（核心方法论）  → [📖 entries/harness-engineering](entries/harness-engineering.md)
│   驾驭AI Coding：一份面向团队的Harness Engineering落地规范
│   开启Harness Engineering探索之旅
│   从AI Coding到Harness Engineering的端到端工程开发实践
│   从Vibe Coding到Harness—— 一套大仓AI工程化实战
│   你的 Harness 工作流真的在进步吗？（Harness Eval）
│   Harness不是目的，知识才是护城河
│
├── 二、Skill 设计（Harness 的执行单元）
│   如何写好 Skill：一份终极实战经验手册  → [📖 entries/skill-design-handbook](entries/skill-design-handbook.md)
│   当我把 AI 变成一个"算法"：Skill 工程化设计的心路历程
│   AI Agent & Skill 测评方案及落地实践
│
├── 三、Agent 架构与治理
│   Agent 治理：用 Hook 堵住 LLM 的偷懒、越权与失忆  → [📖 entries/agent-governance-hook](entries/agent-governance-hook.md)
│   OpenClaw与Hermes：源码里的 AI Agent 架构知识大复盘
│   横向拆解六大Agent上下文压缩策略
│   Loop Engineering 实践指南
│   【揭秘】如何打造一支凌晨3点还在交付的AI军团
│
└── 四、工程实践 & 技术分析
    一篇搞懂 AI Coding Agent 的 Token 成本控制
    五块钱如何花三天（Token 成本控制实践）
    精打细算虾养成指南：省 Token
    拆解大模型几项核心操作背后的数学与 Infra 优化逻辑
    AI Infra入门干货总结：大模型是如何高效推理的
    你讲卫生吗？（AI 交互习惯）
    AI+ Kuikly：7.5小时落地三端多模态聊天 App 实战
```

---

## 推荐阅读路径

| 想解决的问题 | 推荐阅读顺序 |
|---|---|
| **我刚带团队做 AI Coding，不知道从哪开始** | 开启Harness → 落地规范 → Skill 设计 |
| **团队 AI 工作流已经有了，但不知道好不好** | Harness Eval → Agent 治理 |
| **写了一堆 Skill，效果参差不齐** | Skill 工程化 → 测评方案 |
| **上下文/Token 不够用** | Token 成本控制 → 上下文压缩 |
| **想深入 Agent 架构** | OpenClaw/Hermes 复盘 → Loop Engineering |
| **想优化推理成本/延迟** | 大模型推理优化 → AI Infra 入门 |

---

> 维护规则：新增知识条目时，在对应领域下加一行链接，并在阅读路径表
> 中考虑是否新增路径。领域可以重组、拆分、合并，以可读性为准。
