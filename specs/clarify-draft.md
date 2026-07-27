# P2 技术澄清 — 结论汇总

> 全部 12 个问题已澄清。以下为最终决策。

---

## P0 — 阻断性问题

| Q | 问题 | 结论 |
|---|------|------|
| Q1 | `.state.json` 由谁创建 | `fetch_articles.py` 只写 `logs/fetch_state.json`（抓取去重）。`knowledge/.state.json` 由管线 2 独立维护（提炼管线状态） |
| Q2 | 模块归属 | Concept frontmatter 增加 `module` 字段，Agent 在提炼时填入。`index.md` 的模块分组从文件系统 + module 字段自动生成 |
| Q3 | F2 判定边界 | F2 降级为 WARN。FAIL（阻断）仅保留 F1(type)、F3(timestamp)、F4(tags) |

---

## P1 — 高优先级

| Q | 问题 | 结论 |
|---|------|------|
| Q4 | 并发模型 | 独立工作区 + PR 流程控制所有写操作。不做文件锁 |
| Q5 | 匹配机制 | C — 离线预计算向量索引。Concept 的 description + 适用场景 → embedding，消费项目 Agent 计算任务 embedding → Top 3 |
| Q6 | 反向索引 | 构建 `knowledge/.backlinks.json`，Gate 校验阶段自动维护 |
| Q7 | 管线 2 触发 | C — Agent 自动起草 Concept → 输出预览 → 用户确认后入库 |

---

## P2 — 中优先级

| Q | 问题 | 结论 |
|---|------|------|
| Q8 | 数据一致性 | 流程：fetch → fetch_state.json 去重 → 人工筛选 → 通过筛选的落 raw/。raw/ 目录为 source of truth |
| Q9 | 筛选豁免 | 统一机制，去掉豁免词。保留高置信度排除词（招募、获奖、发布等） |
| Q10 | 跨项目路径 | 知识库部署到 GitHub 仓库，消费项目通过 git clone / submodule 引用 |
| Q11 | 崩溃恢复 | 超时 10 分钟自动回退到 pending + 中间产物保存 `.draft.md` |
| Q12 | 文件名生成 | Agent 翻译 kebab-case，Gate 校验唯一性 + 链接断裂检查 |
