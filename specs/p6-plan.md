# P6 归档

> 交付的最后一步：知识沉淀。按文章 P6 方法——changes-sync + knowledge-sync + Delta Spec。

---

## 1. changes-sync

对齐「代码做了什么」和「文档说了什么」：

| 文档 | 实际变更 | 操作 |
|------|---------|------|
| `index.md` | 19 篇 Concept 增加 `module` 字段 | 无需改——index.md 不存 module 信息 |
| `concept-template.md` | 新增 `module` 行 | ✅ 已更新 |
| `concept-spec.md` | F1-F11 Gate 规则 | ✅ 已更新 |
| `design.md` | sandbox_mode + Gate + 管线 | ✅ 已更新 |

---

## 2. knowledge-sync

本次交付中可复用的知识提炼入库：

| 来源 | 提炼 | 状态 |
|------|------|------|
| P2 澄清 | 12 个技术决策 → 设计契约 | 已写入 `design.md` |
| P3 实现 | D-1~D-8 改动点方法 | 已写入 `p3-plan.md` |
| P4 测试 | 自愈闭环模式 | 已写入 `p4-plan.md` |
| P5 部署 | CI/CD + 评分卡 | 已写入 `.github/workflows/test.yml` |

---

## 3. Delta Spec（写入 log.md）

按 ADDED/MODIFIED/REMOVED/RENAMED 四类标记：

```markdown
## 2026-07-27

* **Addition**: `scripts/validate_concept.py` — Gate F1-F8 校验脚本
* **Addition**: `scripts/pipeline2.py` — 管线 2 草稿保存 + 超时回退
* **Addition**: `scripts/rebuild_backlinks.py` — 反向索引重建
* **Addition**: `scripts/build_embeddings.py` — 向量索引生成
* **Addition**: `scripts/p4_test.py` — P4 集成测试 (TC-4/TC-5/TC-6)
* **Addition**: `.github/workflows/test.yml` — CI/CD 自动测试
* **Addition**: `knowledge/.state.json` — 提炼管线状态
* **Addition**: `knowledge/.backlinks.json` — 反向索引数据
* **Addition**: `knowledge/.embeddings.json` — 向量索引数据
* **Addition**: `specs/p3-plan.md` — P3 实现计划
* **Addition**: `specs/p4-plan.md` — P4 测试计划
* **Addition**: `specs/p5-plan.md` — P5 部署计划
* **Addition**: `specs/deploy.md` — 部署记录
* **Update**: `knowledge/entries/*.md` — 19 篇增加 module 字段
* **Update**: `specs/concept-template.md` — 增加 module 字段
* **Update**: `specs/concept-spec.md` — F1-F11 Gate 规则
* **Update**: `specs/design.md` — sandbox_mode + Gate + 管线
* **Update**: `specs/clarify-draft.md` — 12 题全部决策
* **Removed**: `fetch_articles.py` — 去掉 `_RETAIN_OVERRIDE_KEYWORDS`
* **Update**: `knowledge/log.md` — 本条目
```
