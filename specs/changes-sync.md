# changes-sync — change-id: p3-p4-20260727

> P6 第一步：对齐 git diff 与 design.md 契约。

## 对照结果

| D-x | 设计描述 | git 变更 | 一致？ |
|-----|---------|---------|--------|
| D-1 | `knowledge/.state.json` | ✅ 创建 | ✅ |
| D-2 | `concept-template.md` +module | ✅ 修改 | ✅ |
| D-3 | `validate_concept.py` | ✅ 创建 | ✅ |
| D-4 | 去掉 `_RETAIN_OVERRIDE_KEYWORDS` | ✅ 删除 | ✅ |
| D-5 | `pipeline2.py` | ✅ 创建 | ✅ |
| D-6 | `rebuild_backlinks.py` | ✅ 创建 | ✅ |
| D-7 | `build_embeddings.py` | ✅ 创建 | ✅ |
| D-8 | 19 篇 +module | ✅ 修改 | ✅ |

## 超出 D-x 的变更（合规）

| 变更 | 来源 | 原因 |
|------|------|------|
| `.github/workflows/test.yml` | P5 | CI/CD 部署 |
| `scripts/p4_test.py` | P4 | 集成测试 |
| `specs/p3~p6-plan.md` | P3-P6 | 实现计划 |
| `specs/deploy.md` | P5 | 部署记录 |
| `specs/delta-spec.md` | P6 | 本文档 |
| `specs/concept-spec.md` (F1-F11) | 协议层 | Gate 扩展 |

## 结论

✅ 全部 8 个 D-x 与设计契约一致。超出部分均有明确来源（P4/P5/P6 正常产出）。
