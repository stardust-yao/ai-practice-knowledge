# Deploy

- **change-id**: `p3-p4-20260727`
- **branch**: main
- **commit**: `c93b1f0`
- **deploy-time**: 2026-07-27T18:00:00+08:00
- **target**: GitHub `stardust-yao/ai-practice-knowledge`
- **status**: pending

## 提交信息

- `feat(scripts): P3/P4 Gate 校验/管线/索引脚本 + module 回填 (D-1~D-8)`

## 变更文件

| 文件 | 操作 |
|------|------|
| `scripts/validate_concept.py` | 新建 |
| `scripts/pipeline2.py` | 新建 |
| `scripts/rebuild_backlinks.py` | 新建 |
| `scripts/build_embeddings.py` | 新建 |
| `scripts/p4_test.py` | 新建 |
| `knowledge/.state.json` | 新建 |
| `knowledge/.backlinks.json` | 新建 |
| `knowledge/.embeddings.json` | 新建 |
| `knowledge/entries/*.md` | 修改 (+module) |
| `specs/concept-template.md` | 修改 (+module) |
| `specs/concept-spec.md` | 修改 (F1-F11) |
| `specs/design.md` | 修改 (sandbox_mode, Gate) |
| `specs/p3-plan.md` | 新建 |
| `specs/p4-plan.md` | 新建 |
| `specs/p5-plan.md` | 新建 |
| `fetch_articles.py` | 修改 (去豁免) |

## 部署步骤

1. ✅ P4 测试 exit 0（5/5 PASS）
2. ✅ `git commit`（commit 格式符合规范）
3. ⬜ `git push origin main`（需手动执行 — 无 CI/CD）

## 评分卡

| 指标 | 结果 |
|------|------|
| P4 测试 | ✅ 5/5 PASS |
| Gate 校验 | ✅ 19/19 PASS |
| 模块覆盖 | ⚠️ 7/8 (tools-integration known gap) |
| 评分 | 95 (1 known gap) |
