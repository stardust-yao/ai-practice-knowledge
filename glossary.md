# 术语表 · Glossary

> SSOT（Single Source of Truth）：每个术语只在此定义一次。别处引用时请使用 `[术语名](#术语名)` 链接至此，不得自行重定义。
>
> 维护规则：新增术语时更新本文档。修改定义时，检查所有引用该术语的文档是否需要同步。

---

## 知识库体系

### Concept
- **定义**：知识库中一篇经过提炼的知识条目。按 OKF v0.1 规范编写，包含 frontmatter 元数据和 5 段标准正文（适用场景、核心问题、方法、关联概念、关键引用）。
- **文件格式**：`knowledge/entries/{slug}.md`，Markdown + YAML frontmatter
- **与 raw 的关系**：一篇 raw 原文经 Agent 提炼后生成一篇 Concept
- **别名**：知识条目、entry
- **引用**：本概念在 `specs/concept-spec.md`、`specs/concept-template.md`、`specs/design.md` 中均有详细规范

### Raw / 原文
- **定义**：从 RSS Feed 抓取后未经处理的公众号文章原文。保留完整正文，按年月归档。
- **文件格式**：`raw/YYYY-MM/YYYY-MM-DD_标题.md`
- **与 Concept 的关系**：raw 是 Concept 的原料，Concept 是 raw 的提炼

### OKF
- **定义**：Open Knowledge Framework（开放知识框架），Google 提出的知识库格式规范（v0.1）。规定 Bundle 结构（index.md、log.md、entries/）和 Concept frontmatter 字段标准。
- **本项目采用版本**：v0.1
- **落地点**：`knowledge/index.md` 的 `okf_version` 字段

### Module / 模块
- **定义**：知识库顶层分类维度。按搭建 AI 工程项目的流程分为 8 个模块，而非按学术分类。Concept 的 `module` 字段从以下白名单中选一：
  ```
  project-arch        # 项目架构
  skill-design        # Skill / Rules 设计
  tools-integration   # 工具与集成
  memory-knowledge    # 记忆与知识
  safety-guardrails   # 护栏与安全
  eval-testing        # 评估与测试
  cost-performance    # 成本与性能
  fundamentals        # 底层原理
  ```
- **与 index.md 的关系**：`knowledge/index.md` 按 8 模块组织条目列表

### Gate / Gate 校验
- **定义**：Concept 入库前的自动化检查机制。按 F1-F11 规则逐条检查 frontmatter 字段和正文段落，FAIL 阻断入库，WARN 可入库但标记 TODO。
- **校验脚本**：`scripts/validate_concept.py`
- **规则清单**：`specs/concept-spec.md`（权威定义）
- **⚠️ 注意**：`specs/design.md` 中存在旧版 Gate 级别描述（F2/F5/F6/F7 标为 WARN），该描述已过时，以 `concept-spec.md` 为准

### 管线 / Pipeline
- **定义**：知识库运转的三条自动化流水线：
  - 管线 1（入库）：cron → `fetch_articles.py` → raw/ → 去重 + 筛选
  - 管线 2（加工）：raw/ → Agent 提炼 → Gate 校验 → entries/ 
  - 管线 3（服务）：Agent 任务开始 → embedding 匹配 → 提示 Concept
- **设计文档**：`specs/design.md`

---

## 工程实践

### Harness Engineering
- **定义**：一套 AI 工程化纪律体系。核心理念：不是让 AI 写更多代码，而是通过协议、管线、门禁、知识沉淀四层骨架，让 AI 产出的代码可预测、可验证、可持续改进。
- **四层骨架**：协议层（Spec → Contract）→ 管线层（Pipeline）→ 纪律层（Gate / Hook）→ 知识层（Concept / Skill）
- **相关文档**：`specs/design.md`（四层实现）

### SSOT
- **定义**：Single Source of Truth（单一事实来源）。原则：每条信息只在一处定义，其余所有地方通过引用消费该定义。违反 SSOT 的结果是信息在多处独立描述、不同步更新后产生矛盾。
- **本项目体现**：本术语表即 SSOT 实践——每个术语只在此定义一次
- **来源**：腾讯《开启 Harness Engineering》2.3.1 节

### Delta Spec
- **定义**：变更记录规范。当 Concept 被修改时，在 `knowledge/log.md` 中以 `**Update**` / `**Addition**` / `**Deprecation**` 三种标记记录变更类型和内容。
- **目的**：让 git log 之外有一份「语义变更日志」，说明改了什么、为什么改
- **记录位置**：`knowledge/log.md`

### Hook / Hook 模式
- **定义**：在关键操作点（pre-commit、pre-push、写入前）插入自动化检查，不通过则阻断。类比 git hooks。
- **本项目体现**：Gate 校验就是 Concept 入库的 Hook（F1-F8 FAIL 阻断写入）
- **来源**：腾讯《Agent 治理：用 Hook 堵住 LLM 的偷懒、越权与失忆》

### Loop Engineering
- **定义**：自主循环设计范式。核心循环：Sense（感知当前状态）→ Decide（决策下一步）→ Repair（检测到错误时自动修复）→ 循环。
- **来源**：腾讯《Loop Engineering 实践指南》 + Addy Osmani / Boris Cherny 方法论

### Skill
- **定义**：可复用的 AI 能力单元。以 Markdown 文件形式定义触发条件、工作流程、产出标准，Agent 在匹配场景下自动加载执行。
- **与 Concept 的关系**：Concept 是知识（知道什么），Skill 是能力（能做什么）。Concept 的「适用场景」可触发对应 Skill。

---

## Spec / 契约体系

### Spec / 契约
- **定义**：一份规定「什么算对」「什么算错」的文档。每份 spec 有明确的校验标准，不依赖主观判断。
- **本项目的 Spec 清单**：
  - `specs/requirements.md` — 功能需求 + AC
  - `specs/design.md` — 数据模型 + 管线契约
  - `specs/concept-spec.md` — Concept Gate 规则（权威）
  - `specs/concept-template.md` — Concept 模板契约
  - `specs/test-cases.md` — 测试用例
- **⚠️ 注意**：`specs/design.md` 中 Gate 校验表（F1/F3/F4 FAIL, F2/F5/F6/F7 WARN）与 `concept-spec.md`（F1-F8 全部 FAIL）矛盾，以 `concept-spec.md` 为准。

### 必填
- **定义**：在 spec 语境中，「必填」指字段/段落必须存在，但其缺失的严重级别由 Gate 规则独立决定。例如 Concept 的 `description` — template 标记为「必填」意味着应填写，但 Gate F3 将其缺失定为 WARN（不阻断入库）。
- **⚠️ 解决矛盾**：Module 1 案例 5 的矛盾根因是「必填」一词在模板语境（"应当填写"）和 Gate 语境（"缺失阻断"）中含义不同。本定义明确：模板的「必填」是填写建议，Gate 级别才是阻断判断。

### tags
- **定义**：Concept frontmatter 中的标签字段。**正确格式**为 YAML 数组：`tags: [harness-engineering, methodology, pipeline]`。约束：全小写英文、≥3 个、用连字符连接词组。**错误示例**：`tags: harness, methodology`（非 YAML 数组）。
- **⚠️ 解决矛盾**：Module 1 案例 6 的矛盾根因是 `concept-template.md` 中「逗号分隔」的措辞可能被误解为 YAML 字符串。本定义澄清：tags 必须是 YAML 数组格式，逗号在数组内部是 YAML 语法而非字符串。

---

## 筛选体系

### 筛选规则 / Filter Rules
- **定义**：`fetch_articles.py` 中用于自动排除非技术文章的关键词匹配规则。分为排除词（招募、获奖、发布、上线、推出、全新、凭什么、带你速通、你真的需要、犀牛鸟、报名、高考、几分、杰出论文、重要突破、ACL 202）和产品名黑名单。
- **规则源**：`fetch_articles.py`（代码实现） + `logs/filter_rules.md`（可读说明）
- **原则**：仅保留高置信度排除词，无豁免机制

---

> 最后更新：2026-07-31
> 术语数：15
> 参考：腾讯《开启Harness Engineering》SSOT 原则 · 阿里《分解一座冰山》知识库分层
