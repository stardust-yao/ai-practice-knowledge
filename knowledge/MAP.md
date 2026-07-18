# 知识地图（人工入口）

> **按搭项目的流程组织**：从骨架→能力→工具→记忆→安全→评估→成本→原理，每一步解决一类问题。

---

## 1. 项目架构（5 篇）

搭骨架——协议、管线、纪律怎么设计。

| 条目 | 场景 / 问题 | 提出的方法与思路 |
|------|-----------|----------------|
| [开启 Harness Engineering](entries/harness-engineering.md) | AI Coding 代码产出翻倍但发布节奏没加快；瓶颈从"写"转移到了"理解、对齐、验证" | 四层骨架：协议层（输入输出契约）→ 管线层（P1-P6 六阶段）→ 纪律层（防 AI 五种偷懒模式）→ 知识库（长期记忆）。四条工程原则：Fixed Flow 追求确定性、上下文控制、Token 成本优化、确定的事用脚本 |
| [团队 Harness 落地规范](entries/team-harness-spec.md) | Harness 概念有了，但团队层面怎么统一？规范不是某个人的 Rules，而是整个团队的基线 | 四层团队结构：全局 Rules（安全红线、Git 规范）→ 项目级 Skill（按需触发）→ 共享知识库（业务规则、架构决策、接口契约）→ 评估与演进（定期跑 Eval 回归） |
| [端到端工程实践](entries/ai-coding-to-harness.md) | 从"AI 写代码"到"AI 交付完整需求"之间的鸿沟——编码快了但测试、部署、归档没跟上 | P1-P6 全链路 Harness 落地：需求分析→方案设计→代码实现→测试验证→部署上线→归档沉淀。每阶段 Gate 门禁，不低于 95 分、最多 3 轮整改 |
| [Vibe Coding → Harness](entries/vibe-to-harness.md) | 大仓 Monorepo 场景下凭感觉用 AI——改一处可能影响多服务 | 大仓 Harness 特殊要求：依赖感知（改前分析跨模块影响）、增量变更（diff 驱动）、分层 Skill（模块独立、Rules 共享）、统一 Gate 评分卡 |
| [OpenClaw vs Hermes](entries/openclaw-hermes-arch.md) | 两套主流 Agent 框架各有取舍，如何选型？ | OpenClaw：TypeScript 微内核 + 万物皆插件 + 五层安全纵深 + 配置驱动。Hermes：技能自创建闭环 + Smart Approval 三态 + 8 种沙箱后端。未覆盖落地难题：记忆分层、确定性编排边界、多 Agent 协作 |

## 2. Skill / Rules 设计（3 篇）

能力怎么写——设计方法、编排机制、自循环系统。

| 条目 | 场景 / 问题 | 提出的方法与思路 |
|------|-----------|----------------|
| [Skill 设计实战手册](entries/skill-design-handbook.md) | Skill 写了但效果不好：触发不准、Token 太高、AI 不遵指令 | 渐进式三级加载（常驻→触发→按需）；description 是成败关键（用通用语言 + 具体技术词，不用内部黑话）；五个技巧（开头说清三件事、祈使句下指令、Before/After 对比、Few-Shot 3-5 例、决策流程图）；五种反模式 |
| [Skill = 算法](entries/skill-as-algorithm.md) | 规则写越多 AI 越不听话：200 条规则灌进去，AI 只能记住开头几条 | Agent 只做"大脑"（理解意图、收集参数、组织回复），CLI 做"手脚"（调 API、写文件、管状态），用 JSON 通信。Workflow 五机制：步进式披露（永远只看到当前一步）、Gate 门禁（开放题变填空题）、状态持久化（记忆不在 AI 脑子里）、模板变量（数据流由 CLI 管）、三种步骤协奏 |
| [Loop Engineering](entries/loop-engineering.md) | 单次 Agent 调用只能做一步，真实工作需要多步循环：开发→测试→修复 | 三环结构：感知环（监测状态变化）→ 决策环（判断下一步分支）→ 修复环（失败时自动诊断→修复→重试）。配最大循环次数 + Token 预算 + 失败交接点 |

## 3. 工具与集成

MCP、CLI、外部 API 怎么接入——工具层设计。

| 条目 | 场景 / 问题 | 提出的方法与思路 |
|------|-----------|----------------|
| *待补充* | MCP 协议集成、CLI 工具设计、外部服务对接 | — |

## 4. 记忆与知识（2 篇）

AI 怎么记住该记住的——知识库架构、知识沉淀、记忆管理。

| 条目 | 场景 / 问题 | 提出的方法与思路 |
|------|-----------|----------------|
| [知识才是护城河](entries/knowledge-as-moat.md) | Harness 让你跑得快，但知识留在人脑/聊天记录里——下次同类需求 AI 从零开始 | 每次交付强制跑三件套：changes-sync（代码=文档对齐）→ knowledge-sync（踩坑→知识库）→ specs-generator（ADDED/MODIFIED/REMOVED 增量合并）。Delta Spec 是灵魂——不复制全文，只标记"哪些变了" |
| [你讲卫生吗](entries/hygiene-habits.md) | AI 交互"脏习惯"：一个 session 聊几天、塞一堆无关文件、需求说不清楚就让 AI 猜 | 三条原则：任务隔离（每件事开新 session）、信噪比优先（宁少勿滥）、明确指令（GIVEN-WHEN-THEN 结构化）。好习惯 > 好模型 |

## 5. 护栏与安全（1 篇）

防翻车——Hook 体系、HITL 门禁、沙箱隔离。

| 条目 | 场景 / 问题 | 提出的方法与思路 |
|------|-----------|----------------|
| [Agent 治理：用 Hook 堵](entries/agent-governance-hook.md) | 三种 LLM 行为 prompt 管不住：长 SQL 截断略写（偷懒）、未确认就发布（越权）、改表不分析下游影响（失忆） | 三道护栏：长文本 offload（读写两侧全量落盘、LLM 只看到引用句柄、修改输出 token 降 90%）→ HITL 门禁（配置驱动危险工具清单、beforeTool 拦截、富交互确认框）→ 上下文联动闭环（Hook 采集 → state → Attachment 注入，不靠 LLM 自觉） |

## 6. 评估与测试（2 篇）

怎么知道做得好不好——测评、评分、回归。

| 条目 | 场景 / 问题 | 提出的方法与思路 |
|------|-----------|----------------|
| [Agent & Skill 测评方案](entries/agent-skill-evaluation.md) | Agent 从 Demo 到生产的门槛：非确定性、黑盒化、错误级联放大 | 三类评分器组合：确定性评分器（明确对错的脚本验证）+ Rubric 评分器（LLM 按标准打分）+ 人工评分器（强主观兜底）。五大评测维度：功能正确性、过程质量、效率成本、鲁棒性安全、体验对齐 |
| [Harness Eval](entries/harness-eval.md) | 团队用主观 vibes 评价工作流——"感觉这版稳了不少"，不知道是进步还是退步 | 固定~考卷~式回归评测：每次改 Harness 配置后跑同一套任务→对比得分变化。覆盖任务完成度、步骤合规性、产物质量、Token 效率 |

## 7. 成本与性能（4 篇）

Token 怎么省、上下文怎么管、模型怎么选。

| 条目 | 场景 / 问题 | 提出的方法与思路 |
|------|-----------|----------------|
| [Token 成本控制](entries/token-cost-control.md) | Token 不知不觉烧光了——长 session、全量代码分析、递归压缩 | 三层漏斗：行为习惯（开新 session、精简 prompt）→ 工具链（按任务选模型、diff 优先）→ 架构（知识库按需加载、SubAgent 计费隔离） |
| [五块钱如何花三天](entries/five-yuan-token.md) | Token 用量不可见、不可控——账单"不知不觉就上去了" | 三层降本策略：会话管理（任务结束即关、不强模型跑小事）→ 上下文精简（diff 优先、结构化输入省 80%）→ 架构优化（配用量看板+阈值告警）。核心洞见：只有可度量的 Token 才能被管理 |
| [精打细算虾指南](entries/frugal-token.md) | 省 Token 和把 AI 用好是两件事？——其实是一件事 | 降低浪费率而非绝对用量：需求前置对齐（第一次就说清楚）、小步快跑（小块 context 小成本）、用结构换 Token（JSON schema 输入省 80%+）、脚本替代 LLM（格式化/校验/统计） |
| [六大上下文压缩策略](entries/context-compression-survey.md) | 长对话质量下降、上下文爆满——六家产品各有做法，哪个对？ | 第一代问题：悬崖式触发、全量摘要丢细节、不区分信息价值。六家对比 + 自研四级水位线：安全区（不做）→ 预警区（摘要长工具输出）→ 压缩区（结构化摘要历史）→ 上限区（强制截断+补偿） |

## 8. 底层原理（2 篇）

推理怎么跑、算子怎么优化——数学与 Infra 原理。

| 条目 | 场景 / 问题 | 提出的方法与思路 |
|------|-----------|----------------|
| [AI Infra 入门](entries/ai-infra-inference.md) | 大模型推理为什么慢？vLLM 到底做了什么优化？ | Continuous Batching（调度从 request→token level）+ PagedAttention（KV Cache 按 token 级动态分配，block_table 间接寻址）+ PD 分离（Prefill 计算密集 vs Decode 访存密集分开部署） |
| [大模型核心算子](entries/llm-core-operations.md) | 每个算子到底在做什么？优化又优化了什么？ | RoPE（只对部分维度旋转，高频精细/低频语义）+ GQA（KV head 数 < Q head 数，KV Cache 显存砍到 1/4）+ SwiGLU（多一个 gate_proj）+ Flash Attention（分块计算、不存中间矩阵、显存 O(n)） |

---

## 推荐阅读路径

| 场景 | 阅读顺序 |
|---|---|
| 从零搭一个 AI 工程化项目 | 1→2→4→5→6→7 |
| 团队已有的 AI Coding 想升级 | 1→6→5→7 |
| Skill 写了但效果差 | 2→6→7 |
| Token 账单控制不住 | 7→1 |
| 想深入 Agent 技术细节 | 8→5→1 |
