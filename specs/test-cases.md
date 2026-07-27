# 测试用例

> 与 `requirements.md` 共用同一份 AC 列表。P4 阶段直接拿本文档执行测试。

---

## TC-1: 被动检索 — 按 tags + description 匹配并返回 Concept 核心内容

- **关联 AC**：AC-1
- **前置条件（GIVEN）**
  - 知识库中已存在至少 3 篇 Concept，每篇均包含 title、tags、description、适用场景、核心方法字段
  - 其中至少 1 篇 Concept 的 tags 包含 `"prompt-engineering"`，description 包含 `"提示词优化"`
- **测试步骤（WHEN）**
  1. 在某个项目中，向 Agent 提出与 AI 工程实践相关的问题，例如：「如何优化我的提示词？」
  2. Agent 从知识库中检索匹配结果
- **预期结果（THEN）**
  - Agent 返回的匹配结果中，至少包含 tags 含 `prompt-engineering` 或 description 含 `提示词优化` 的 Concept
  - 返回内容至少包含：title、适用场景、核心方法 三个字段
- **验证方式**：仅手动
  - 需在实际 Agent 对话环境中观察检索结果是否符合预期，无法纯脚本断言 LLM 输出

---

## TC-2: 主动提示 — 任务开始时入口匹配

- **关联 AC**：AC-2
- **前置条件（GIVEN）**
  - 知识库中存在一篇 Concept，其「适用场景」字段值为 `"团队知识库建设"`
  - Agent 已配置加载该知识库
- **测试步骤（WHEN）**
  1. 向 Agent 发起一个新任务，任务描述为：「帮我搭建一个团队知识库」
  2. 观察 Agent 的首轮回复
- **预期结果（THEN）**
  - Agent 首轮回复中 SHALL 出现格式为 `📚 知识库提示：该场景下可参考 [Concept 标题] — [description]` 的主动提示
  - 提示条数 ≤ 3
- **验证方式**：仅手动
  - 需在实际 Agent 对话中观察首轮回复是否包含指定格式的提示文本，且条数不超过 3

---

## TC-3: 主动提示 — 对话中关键词匹配

- **关联 AC**：AC-3
- **前置条件（GIVEN）**
  - 知识库中存在一篇 Concept，其 tags 包含 `"code-review"` 或 description 包含 `"代码审查"`
- **测试步骤（WHEN）**
  1. 与 Agent 进行多轮对话，在其中一轮自然提到关键词，例如：「我们团队最近在做代码审查的流程优化」
  2. 观察 Agent 在当前轮的回复
- **预期结果（THEN）**
  - Agent 当轮回复中 SHALL 出现格式为 `📚 相关方法：[Concept 标题] — 是否展开？` 的提示
- **验证方式**：仅手动
  - 需在实际 Agent 多轮对话中观察特定轮次是否触发关键词匹配提示

---

## TC-4: 知识库内容更新 — 从 raw 到 Concept 的加工流水线

- **关联 AC**：AC-4
- **前置条件（GIVEN）**
  - `raw/` 目录下已放入至少 2 篇新公众号文章（Markdown 格式）
  - `logs/filter_rules.md` 已定义筛选规则
  - `specs/concept-template.md` 已定义 Concept 格式契约
  - `specs/concept-spec.md` 已定义 Gate 校验规则 F1-F7
- **测试步骤（WHEN）**
  1. 执行内容加工流水线（触发筛选 → 提炼为 OKF Concept）
  2. 对产出的 Concept 文件运行 Gate 校验
- **预期结果（THEN）**
  - 仅通过 `filter_rules.md` 筛选的文章被提炼为 Concept
  - 产出的 Concept 文件字段结构完全符合 `specs/concept-template.md`
  - Gate 校验 F1-F7 全部 PASS
- **验证方式**：可脚本化
  - 筛选结果：对比 raw/ 文章列表与产出 Concept 数量，检查被过滤掉的文章是否命中 filter_rules
  - 格式校验：编写脚本逐字段对比 Concept 文件与 concept-template.md 的必填字段
  - Gate 校验：编写脚本按 concept-spec.md 中 F1-F7 逐条断言，输出 PASS/FAIL

---

## TC-5: 知识库内容维护 — Delta Spec 变更记录

- **关联 AC**：AC-5
- **前置条件（GIVEN）**
  - 知识库中已存在一篇 Concept（记为 C-A）
  - 存在另一篇 Concept（记为 C-B），其「关联概念」段落引用了 C-A
- **测试步骤（WHEN）**
  1. 对 C-A 执行 Update 操作（修改 title 或核心方法）
  2. 检查 `knowledge/log.md` 的变更记录
  3. 检查 C-B 的「关联概念」段落
- **预期结果（THEN）**
  - `knowledge/log.md` 中 SHALL 包含一条 Delta Spec 标记，记录 C-A 的变更信息
  - C-B 的「关联概念」段落 SHALL 被检查（如引用信息已过期，需补全或更新）
- **验证方式**：可脚本化（部分）
  - log.md 记录：可脚本化 — 检查 log.md 是否在变更后新增了对应 Concept 的 Delta Spec 条目
  - 关联概念检查：仅手动 — 需人工审查 C-B 的「关联概念」段落是否需要补全

---

## TC-6: 跨项目可用 — 渐进式路径消费

- **关联 AC**：AC-6
- **前置条件（GIVEN）**
  - 知识库目录结构完整：包含 `index.md`、各模块子目录及 Concept 文件
  - 存在一个消费项目（如 `job-seeking`），其 `.hermes.md` 已按规范配置
- **测试步骤（WHEN）**
  1. 检查消费项目的 `.hermes.md` 文件
  2. 从 `.hermes.md` 中解析知识库路径引用
  3. 按 `index.md → 模块 → Concept` 路径逐级读取内容
- **预期结果（THEN）**
  - `.hermes.md` 中 SHALL 包含指向知识库目录的路径引用
  - 能通过文件路径逐级访问到具体 Concept 文件，无需额外工具、API 或 Skill
- **验证方式**：可脚本化
  - 路径引用检查：用脚本读取 `.hermes.md`，正则匹配知识库路径
  - 渐进式加载验证：脚本依次读取 `index.md` → 解析模块列表 → 读取模块目录 → 访问 Concept 文件，全程仅使用文件系统操作，不需要网络或第三方依赖
