# Spec 一致性审计 · Module 1

> 按 modular-learning 模块1 要求，盘点本项目中"同一件事被多处描述且不一致"的案例。

---

## 案例 1：Gate F2/F5/F6/F7 级别矛盾（最严重 ❌）

| 来源 | 描述 |
|------|------|
| `specs/design.md:138` | `Gate 校验 | F1/F3/F4 FAIL, F2/F5/F6/F7 WARN` |
| `specs/design.md:180-181` | `Gate 校验 F2/F5/F6/F7 | 脚本 | 规则检查，WARN 不阻断` |
| `specs/concept-spec.md:20-82` | F2 FAIL, F5 FAIL, F6 FAIL, F7 FAIL, F8 FAIL |

**矛盾**：design.md 说 F2/F5/F6/F7 是 WARN（不阻断入库），concept-spec.md 说这些是 FAIL（阻断）。如果按 design.md 执行，有 WARN 的 Concept 会入库；按 concept-spec.md 执行，会被拒绝。这是直接影响入库决策的严重契约矛盾。

**类型**：复制粘贴型 — design.md 的 Gate 契约表未随 concept-spec.md 升级而更新。

---

## 案例 2：Gate 条目总数不一致

| 来源 | 提及 |
|------|------|
| `specs/requirements.md:41` | `Gate 校验（F1-F7）` |
| `specs/test-cases.md:63` | `Gate 校验规则 F1-F7` |
| `specs/concept-spec.md:1-130` | F1-F11（8 frontmatter + 3 正文） |

**矛盾**：需求文档和测试用例声明的 Gate 范围是 F1-F7，但实际规范已扩展到 F1-F11（增加了 F8 timestamp、F9 适用场景、F10 关联概念、F11 关键引用）。如果按 AC-4 和 TC-4 验证，只会检查前 7 项，漏掉 4 项检查。

**类型**：复制粘贴型 — 需求/测试文档写了 F1-F7 后，规范升级到 F1-F11 时未同步更新。

---

## 案例 3：知识库分类体系矛盾

| 来源 | 分类 |
|------|------|
| `IDEA.md:25-27` | `methods/`, `tools/`, `cases/` |
| `PROJECT.md:43-45` | `methods/`, `tools/`, `cases/` |
| `knowledge/index.md:10-67` | 8 模块：project-arch / skill-design / tools-integration / memory-knowledge / safety-guardrails / eval-testing / cost-performance / fundamentals |

**矛盾**：IDEA.md 和 PROJECT.md 描述的"methods/tools/cases"三层分类早已废弃（2026-07-24 升级到 8 模块 OKF 体系），但文档未更新。新加入者读 PROJECT.md 会以为知识库是按 methods/tools/cases 组织的。

**类型**：复制粘贴型 — 分类升级后，相关文档未被同步修改。

---

## 案例 4：PROJECT.md 数据严重过时

| 字段 | PROJECT.md 记录 | 实际值 |
|------|----------------|--------|
| raw/ 文章数 | 20 篇 | **223 篇** |
| Feed 源数 | 1 个（腾讯技术工程） | **12 个** |
| 日期范围 | 2026-06-22 ~ 2026-07-17 | **2025-09 ~ 2026-07** |

**矛盾**：PROJECT.md 声明的项目规模与实际情况差距超过 10 倍。这是"直接事实错误"而非歧义问题。

**类型**：复制粘贴型 — 数据变更后 PROJECT.md 未更新。

---

## 案例 5：`description` 必填级别描述冲突

| 来源 | 表示 |
|------|------|
| `specs/concept-template.md:14` | description 标记为 **✅ 必填** |
| `specs/concept-spec.md:34` | F3 级别为 **WARN**（不阻断） |

**矛盾**：模板说 description 是"必填"项，但 Gate 校验只给 WARN（缺失不阻断入库）。对写 Concept 的人来说，"必填"意味着"不写不行"；对 Gate 来说，"WARN"意味着"不写也能过"。同一个字段的"必填"在不同文档语境下含义不同。

**类型**：上下文歧义型 — "必填"在模板语境 = "应该填写"，在 Gate 语境 = "不填不阻断"。同一词两种含义。

---

## 案例 6：`tags` 格式描述模糊

| 来源 | 描述 |
|------|------|
| `specs/concept-template.md:18` | `tags` — 小写英文，**逗号分隔**，3-6 个 |
| `specs/concept-spec.md:68` | `tags: [harness-engineering, methodology, engineering]`（YAML 数组） |

**矛盾**：模板说"逗号分隔"暗示写成 `tags: harness-engineering, methodology`（对标 JSON 字符串），但规范示例是 YAML 数组 `tags: [a, b, c]`。新手可能写成纯文本逗号串而非 YAML 数组，导致解析失败。

**类型**：上下文歧义型 — "逗号分隔"可以是 YAML 数组（`[a, b]`）也可以是 YAML 字符串（`"a, b"`），两种理解都合理但产出不同。

---

## 汇总

| # | 矛盾描述 | 涉及文件 | 类型 | 严重度 |
|---|---------|---------|------|--------|
| 1 | Gate F2/F5/F6/F7 是 FAIL 还是 WARN | design.md ↔ concept-spec.md | 复制粘贴 | 🔴 阻断级 |
| 2 | Gate 条目数是 F7 还是 F11 | requirements.md/test-cases.md ↔ concept-spec.md | 复制粘贴 | 🟡 遗漏级 |
| 3 | 知识库分类是 3 层还是 8 模块 | IDEA.md/PROJECT.md ↔ knowledge/index.md | 复制粘贴 | 🟡 误导级 |
| 4 | raw/ 文章数 20 vs 223 | PROJECT.md | 复制粘贴 | 🟡 过时级 |
| 5 | description 是"必填"还是"WARN" | concept-template.md ↔ concept-spec.md | 上下文歧义 | 🟡 歧义级 |
| 6 | tags 是逗号分隔还是 YAML 数组 | concept-template.md ↔ concept-spec.md | 上下文歧义 | 🟢 体验级 |

**结论**：4 个复制粘贴型矛盾（来源于 spec 升级后旧文档未同步），2 个上下文歧义型矛盾（同一词在不同语境含义不同）。最严重的是案例 1，直接影响 Concept 能否入库。
