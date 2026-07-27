# Deploy — P3/P4 产出部署

- **change-id**: `p3-p4-20260727`
- **branch**: main
- **deploy-time**: 2026-07-27T18:00:00+08:00
- **target**: GitHub stardust-yao/ai-practice-knowledge
- **status**: deployed

## 提交信息

- feat(scripts): Gate 校验/管线2/反向索引/向量索引脚本 (D-3~D-7)
- feat(knowledge): 19 篇 Concept 增加 module 字段 (D-8)
- feat(specs): P3/P4 实现计划
- fix(fetch): 去掉筛选豁免机制 (D-4)
- fix(knowledge): context-compression-survey 中文 tag→英文
- test(scripts): P4 集成测试脚本
- chore(knowledge): .state.json/.backlinks.json/.embeddings.json

## 变更文件

| 文件 | 操作 | D-x |
|------|------|-----|
| `scripts/validate_concept.py` | 新建 | D-3 |
| `scripts/pipeline2.py` | 新建 | D-5 |
| `scripts/rebuild_backlinks.py` | 新建 | D-6 |
| `scripts/build_embeddings.py` | 新建 | D-7 |
| `scripts/p4_test.py` | 新建 | P4 |
| `knowledge/.state.json` | 新建 | D-1 |
| `knowledge/.backlinks.json` | 新建 | D-6 |
| `knowledge/.embeddings.json` | 新建 | D-7 |
| `knowledge/entries/*.md` | 修改 | D-8 (+module) |
| `specs/concept-template.md` | 修改 | D-2 (+module) |
| `specs/concept-spec.md` | 修改 | F1-F11 |
| `specs/design.md` | 修改 | sandbox_mode, Gate |
| `specs/p3-plan.md` | 新建 | P3 |
| `specs/p4-plan.md` | 新建 | P4 |
| `specs/p5-plan.md` | 新建 | P5 |
| `fetch_articles.py` | 修改 | D-4 (去豁免) |

## 评分卡

| 指标 | 结果 |
|------|------|
| P4 测试 exit 0 | ✅ |
| Gate 校验 19/19 | ✅ |
| 模块覆盖 7/8 | ⚠️ tools-integration known gap |

## 部署步骤

1. P4 测试全部 PASS ✅
2. git commit + push → GitHub main
3. 验证 GitHub 页面可读
