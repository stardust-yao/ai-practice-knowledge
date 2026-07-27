# P5 部署

> 按文章 P5 方法。我们无服务器/DB/流水线，部署目标为 GitHub，评分卡用 P4 测试替代。

---

## 1. Git 提交规范

commit message 必须符合 `<type>(<scope>): <subject>`：

| type | 用途 |
|------|------|
| `feat` | 新功能 / 新脚本 |
| `fix` | 修 bug |
| `refactor` | 重构，不改行为 |
| `chore` | 配置、日志、杂项 |
| `test` | 测试脚本 |
| `docs` | 文档 / specs |

scope 从模块名选择：`specs` / `scripts` / `knowledge` / `raw` / `fetch`

---

## 2. deploy.md 生成

按文章模板，P5 产出 `specs/deploy.md`：

```markdown
# Deploy — P3/P4 产出部署

- **change-id**: `p3-p4-20260727`
- **branch**: main
- **commit**: <hash>
- **deploy-time**: <ISO 8601>
- **target**: GitHub stardust-yao/ai-practice-knowledge
- **status**: deployed

## 提交信息

- feat(scripts): P3 Gate/Pipeline/Backlinks/Embeddings 脚本
- feat(specs): P2 design + P3 plan + P4 plan
- feat(knowledge): 19 篇 Concept 增加 module 字段
- fix(fetch): 去掉筛选豁免机制
- test(scripts): P4 集成测试脚本

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
| `knowledge/entries/*.md` | 修改（+module） |
| `specs/design.md` | 修改（sandbox_mode） |
| `specs/p3-plan.md` | 新建 |
| `specs/p4-plan.md` | 新建 |
| `fetch_articles.py` | 修改（去豁免） |

## 部署步骤

1. P4 测试全部 PASS（exit 0）
2. git commit + push to main
3. 验证 GitHub 页面可读
```

---

## 3. 评分卡 ≥ 95

我们没有后端流水线，评分卡 = P4 集成测试必须全部 PASS。

| 指标 | 要求 | 当前 |
|------|------|------|
| P4 测试 | exit 0 + 5/5 PASS | ✅ |
| Gate 校验 | 19/19 PASS | ✅ |
| 模块覆盖 | 7/8（tools-integration known gap） | ⚠️ |

---

## 4. 部署步骤

1. **组装 deploy.md** — 汇总变更文件列表和提交信息
2. **git commit** — 按规范格式提交
3. **git push** — 推送到 GitHub main 分支
4. **验证** — 检查 GitHub 页面可访问、文件完整
