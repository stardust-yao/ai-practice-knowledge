# 知识索引（AI 入口）

> **渐进式披露第一层**：AI 扫描此文件匹配触发词 → 找到对应条目 → 加载 `entries/*.md` 全文。
> 人也可以快速浏览，但推荐用 MAP.md 看全景。
>
> 当前条目数：3

---

## 速查表：我遇到 X → 看 Y

| 我遇到的问题 / 场景 | 触发词 | 查看条目 |
|---|---|---|
| AI Coding 提效不明显 / 团队靠主观感觉迭代 / AI 偷懒跳过步骤 / 想从 Vibe Coding 升级到工程化 | Harness, 工程化, 工作流不稳定, 偷懒, Fixed Flow | [harness-engineering](entries/harness-engineering.md) |
| Agent 长文本截断略写 / 未授权操作 / 改表不查风险 / 产出不汇报 | Hook, 护栏, 越权, HITL, offload, 上下文失忆 | [agent-governance-hook](entries/agent-governance-hook.md) |
| Skill 写了效果不好 / 不知道怎么组织 / 想写但不知从哪开始 | Skill, description, 渐进式加载, SKILL.md, 结构化 Prompt | [skill-design-handbook](entries/skill-design-handbook.md) |

---

## 条目目录

- [harness-engineering](entries/harness-engineering.md) — 不教模型"怎么回答"，而是设计模型"怎么工作"
- [agent-governance-hook](entries/agent-governance-hook.md) — 用 Hook 切面在框架层确定性兜底 LLM 的偷懒、越权、失忆
- [skill-design-handbook](entries/skill-design-handbook.md) — 结构化 Prompt Engineering：description 写法、Few-Shot、反模式

---

> 规则：新增条目时，在 «速查表» 加一行、在 «条目目录» 加一条链接。
> 触发词要站在「我会用什么词来搜」的角度写，多于不用少于漏。
