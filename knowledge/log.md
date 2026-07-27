# 知识变更日志

## 2026-07-27 — P3/P4/P5 实现交付

* **Addition**: `scripts/validate_concept.py` — Gate F1-F8 校验脚本
* **Addition**: `scripts/pipeline2.py` — 管线 2 草稿保存 + 超时回退
* **Addition**: `scripts/rebuild_backlinks.py` — 反向索引重建
* **Addition**: `scripts/build_embeddings.py` — 向量索引生成
* **Addition**: `scripts/p4_test.py` — P4 集成测试 (TC-4/TC-5/TC-6, 6/6 PASS)
* **Addition**: `.github/workflows/test.yml` — CI/CD 自动测试
* **Addition**: `knowledge/.state.json` — 提炼管线状态
* **Addition**: `knowledge/.backlinks.json` — 反向索引数据 (18 concepts, 58 links)
* **Addition**: `knowledge/.embeddings.json` — 向量索引数据 (19 concepts)
* **Addition**: `specs/p3-plan.md` `specs/p4-plan.md` `specs/p5-plan.md` `specs/p6-plan.md` — P3-P6 计划
* **Addition**: `changes/p3-p4-20260727/` — P6 归档 (deploy + changes-sync + knowledge-sync + delta-spec + evaluation + metrics)
* **Update**: `knowledge/entries/*.md` — 19 篇增加 `module` 字段
* **Update**: `specs/concept-template.md` — 增加 `module` 字段
* **Update**: `specs/concept-spec.md` — F1-F11 Gate 规则 (6 FAIL + 5 WARN)
* **Update**: `specs/design.md` — sandbox_mode (git 分支) + Gate + 管线契约
* **Update**: `specs/clarify-draft.md` — 12 题全部决策
* **Removed**: `fetch_articles.py` — `_RETAIN_OVERRIDE_KEYWORDS` 豁免机制
* **Update**: `knowledge/index.md` — root index.md (OKF v0.1)

## 2026-07-27
* **Addition**: 新建 `specs/requirements.md` — P1 需求文档（原始口径 + 6 条可测 AC）
* **Addition**: 新建 `specs/test-cases.md` — P1 测试用例（TC-1~TC-6，与 requirements.md 同源）
* **Addition**: 新建 `specs/concept-template.md` — Concept 标准模板与填写契约
* **Addition**: 新建 `specs/concept-spec.md` — Concept 校验规则（Gate 清单 + Delta Spec 标记）
* **Update**: P1 阶段完成 — 协议层 + 需求文档 + 测试用例均已产出

## 2026-07-25
* **Update**: 全部 19 篇 Concept 增加 `## 适用场景` 段落 — 每篇 3-4 条具体触发条件
* **Update**: 全部 19 篇 Concept 增加 `## 关联概念` 段落 — 跨文章链接，标注前置/配合关系

## 2026-07-24
* **Update**: 全部 19 篇 Concept frontmatter 对齐 OKF v0.1 — 增加 `type: Article`、`description`、`timestamp`
* **Update**: 全部 19 篇 tags 从中文/混合格式统一为小写英文
* **Update**: INDEX.md 改写为 OKF 格式根 index.md
* **Creation**: 新建 log.md
