# Delta Spec — change-id: p3-p4-20260727

> P6 核心产出。按 ADDED/MODIFIED/REMOVED/RENAMED 四类标记增量变更，
> specs-generator 据此合并到 specs/ 对应章节，避免全量复制。

---

## ADDED

| 文件 | 类别 | 说明 |
|------|------|------|
| `scripts/validate_concept.py` | 脚本 | Gate F1-F8 校验 |
| `scripts/pipeline2.py` | 脚本 | 管线 2 草稿 + 超时 |
| `scripts/rebuild_backlinks.py` | 脚本 | 反向索引重建 |
| `scripts/build_embeddings.py` | 脚本 | 向量索引生成 |
| `scripts/p4_test.py` | 脚本 | P4 集成测试 |
| `.github/workflows/test.yml` | CI/CD | 自动测试 |
| `knowledge/.state.json` | 数据 | 管线状态 |
| `knowledge/.backlinks.json` | 数据 | 反向索引 |
| `knowledge/.embeddings.json` | 数据 | 向量索引 |
| `specs/p3-plan.md` | 规范 | P3 计划 |
| `specs/p4-plan.md` | 规范 | P4 计划 |
| `specs/p5-plan.md` | 规范 | P5 计划 |
| `specs/p6-plan.md` | 规范 | P6 计划 |
| `specs/deploy.md` | 规范 | 部署记录 |

## MODIFIED

| 文件 | 变更内容 |
|------|---------|
| `knowledge/entries/*.md` | 19 篇增加 `module` 字段 |
| `specs/concept-template.md` | 表格 + 模板增加 `module` 行 |
| `specs/concept-spec.md` | F1→F11，6 FAIL + 5 WARN |
| `specs/design.md` | sandbox_mode(git分支) + Gate 契约 + Mermaid 图 |
| `specs/clarify-draft.md` | 12 题全部决策汇总 |
| `knowledge/index.md` | OKF v0.1 root index |
| `knowledge/log.md` | P3-P6 变更记录 |

## REMOVED

| 文件 | 删除内容 |
|------|---------|
| `fetch_articles.py` | `_RETAIN_OVERRIDE_KEYWORDS` 豁免机制 |

## RENAMED

无
