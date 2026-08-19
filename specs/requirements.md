# 需求文档

> P1 产出。与 test-cases.md 共用同一份 AC 列表。

---

## 原始需求

> "建立一个自动化的 AI 实践工程知识库。每次在 AI 工程实践中遇到相关问题，能快速查阅到相关资料；除了主动查询，还应做到 proactive 提示，有哪些实践方法可以用。建立一个持续更新、积累和运营的知识系统。"
>
> "这个知识库服务所有项目，本项目只负责知识库的建立和运营。"
>
> 范围：在现有 OKF 知识库基础上重构扩展。消费项目配 Rules 主动拉取，知识库不负责推送。

---

## Acceptance Criteria

### AC-1: 被动检索

> WHEN 用户或 Agent 提出与 AI 工程实践相关的问题  
> THEN Agent SHALL 按 tags + description 匹配到对应 Concept  
> AND 返回内容至少包含 title、适用场景、核心方法

### AC-2: 主动提示 — 入口匹配

> WHEN Agent 开始一个新任务，且任务描述匹配某篇 Concept 的「适用场景」  
> THEN Agent SHALL 在首轮回复中提示可参考的 Concept（≤3 条）  
> AND 提示格式为 `📚 该场景下可参考 [标题] — [description]`

### AC-3: 主动提示 — 关键词匹配

> WHEN Agent 在对话中识别到与某篇 Concept 的 tags 或 description 匹配的关键词  
> THEN Agent SHALL 在当轮回复中提示该 Concept  
> AND 提示格式为 `📚 相关方法：[标题] — 是否展开？`

### AC-4: 内容更新

> WHEN 新文章被抓取到 raw/ 且通过筛选规则  
> THEN 系统 SHALL 将其提炼为 Concept  
> AND 新 Concept SHALL 通过 Gate 校验（F1-F11，见 `specs/concept-spec.md`）

### AC-5: 内容维护

> WHEN 已有 Concept 被修改  
> THEN 变更 SHALL 以 Delta Spec 标记记录在 log.md  
> AND 关联 Concept 的「关联概念」应检查是否需要补全

### AC-6: 跨项目可用

> WHEN 任意项目的 Agent 启动  
> THEN 该项目 SHALL 能通过 index.md → 模块 → Concept 的路径消费知识库  
> AND 不需要额外工具、API 或 Skill
