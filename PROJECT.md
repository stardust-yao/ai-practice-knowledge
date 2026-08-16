# PROJECT.md — 腾讯工程实践 AI 知识飞轮

> 我（Hermes）每次进入这个项目时必须先读这个文件。

## 当前状态

- 阶段：**双线并行** —— ① 文章抓取与知识库 ② teach 方法论学习
- 上次更新：2026-08-16
- raw/ 文章数：285 篇（2025-09 ~ 2026-08，多源）
- knowledge/ 条目数：19 篇 Concept（8 模块分类）
- 学习工作台：✅ 已上线 https://learn.yaolib.cc（Cloudflare 永久隧道）
- teach 工作区：2 个（spec-consistency、open-code-review）
- 已产出 Skill 数：0（可沉淀，见下方待完成）

---

## 两条线

### 线一：文章抓取与知识库（原项目）

#### 自动抓取（每日定时）
- 来源：wechat2rss.xlab.app 免费 RSS（7+ 公众号）
- 脚本：`fetch_articles.py`（项目根目录）
- 触发：**阿里云服务器系统 cron，每天 18:00**（已部署 ✅）
  - `0 18 * * * cd ~/work/AI实践项目/腾讯工程实践学习 && /usr/bin/python3 fetch_articles.py >> ~/fetch_articles.log 2>&1`
- 已扩展：多 Feed 支持（腾讯/字节/阿里/美团/小米/B站/阿里云等）
- 状态：稳定运行，8/12 抓取 9 篇新文章

**已知限制：免费版硬限返回最近 20 篇，无历史分页**
- 历史文章（20篇之前）只能通过手动导入补录
- 付费自托管（¥150/年）可解除限制，暂未启用

#### 手动补录
- 脚本：`add_article.py <微信文章URL>`
- 输出写入 `raw/YYYY-MM/`，格式与自动抓取一致

#### 知识库（P2-P6 已交付 ✅）
- `knowledge/entries/` — 19 篇 Concept（frontmatter + module 字段，F1-F11 Gate 校验）
- `knowledge/INDEX.md` / `MAP.md` — 索引与地图
- `knowledge/.state.json` / `.backlinks.json` / `.embeddings.json` — 管线状态
- 脚本：`scripts/validate_concept.py`（Gate）、`pipeline2.py`、`rebuild_backlinks.py`、`build_embeddings.py`
- specs/：concept-spec（F1-F11）、design、p3-p6 计划、deploy 记录
- P4 测试 5/5 PASS、Gate 19/19 PASS、评分 95（tools-integration 模块已知缺口）

### 线二：teach 方法论学习（学习工作台）

#### 学习工作台
- 网址：**https://learn.yaolib.cc**（永久域名，Cloudflare Tunnel）
- 代码：`learning/workbench/`（软链 → `~/.hermes/learning-workbench/`）
- 服务：`python3 learning_workbench.py --port 8787`
- 隧道：`cloudflared tunnel run learn`（配置 `~/.cloudflared/config.yml`）
- 风格：Tufte 纸感（`#fffff8` + `#111` + `#8b4513`），站内 iframe 阅读课程

#### teach 工作区（learning/ 下软链）
| 工作区 | 内容 | 进度 |
|--------|------|------|
| `spec-consistency` | 7 课（盘点→术语表→分层→模板→L1脚本→闭环→L3语义）+ 速查卡 | 进行中 |
| `open-code-review` | 5 课（病根→All in Code→先完成→快速响应→实践）+ 速查卡 + 学习记录 | 第 1 课完成 |

#### 学习机制
- **modular-learning skill**：项目拆成按实现顺序的小模块（知识点+实践+验收）
- **teach skill**（Matt Pocock）：MISSION 驱动 + lessons/reference/learning-records 结构
- 学习进度以 teach 工作区的 learning-records/ 和课程状态为准

---

## 目录结构

```
raw/              ← 原始文章存档（按月份，285 篇）
knowledge/        ← 经处理后按主题分类（19 篇 Concept + 索引/图谱/向量）
  entries/        ← 每篇 Concept 一个 md（frontmatter + module）
  INDEX.md        ← 索引（8 模块分类）
  MAP.md          ← 知识地图（场景→方法）
specs/            ← 规范体系（P2 design + P3-P6 计划 + F1-F11 Gate）
scripts/          ← 工具链（validate/pipeline/backlinks/embeddings/p4_test）
changes/          ← 变更记录（delta-spec、归档）
learning/         ← 学习板块（软链到 ~/.hermes/teaching/ 和 learning-workbench）
skills/           ← 沉淀为 Hermes Skill 的内容
logs/             ← ops.md（操作日志）、fetch_state.json（去重）、issues.md
inbox/            ← 待整理输入
```

---

## 脚本说明

### fetch_articles.py — 自动抓取
```bash
python3 fetch_articles.py           # 正常运行
python3 fetch_articles.py --dry-run # 只打印，不写文件不提交
```
每次运行：拉取 RSS → 去重过滤 → HTML转Markdown → 写入raw/ → 更新fetch_state.json → 写ops.md → git commit+push

### add_article.py — 手动单篇导入
```bash
python3 add_article.py "https://mp.weixin.qq.com/s?__biz=...&sn=..."
```

### 学习工作台服务
```bash
# 工作台（8787）
cd ~/.hermes/learning-workbench && python3 learning_workbench.py --port 8787
# 隧道（域名 learn.yaolib.cc）
cloudflared tunnel run learn
```

---

## 工作规则

1. 每次操作后自动写入 `logs/ops.md`（脚本负责，无需手动）
2. 结构性变更（修改分类、调整工作流）前，先告知用户并等确认
3. raw/ 文章命名格式：`YYYY-MM-DD_标题关键词.md`，raw/ 内容不做任何修改
4. 每处理 10 篇文章，发起一次自进化回顾（提议，不自动执行）
5. 用户开始描述新项目/任务时，主动检索 `knowledge/` 中的相关方法并提醒
6. 学习板块：teach 工作区用软链挂载（单一事实来源在 ~/.hermes/teaching/），学习进度以 learning-records/ 为准

---

## 待完成

- [ ] 更新 knowledge/：285 篇 raw → 提炼更多 Concept（当前 19 篇）
- [ ] tools-integration 模块补全（知识库 8 模块中第 3 模块空）
- [ ] 学习工作台：open-code-review 第 2 课（一切皆代码）制作
- [ ] 微信通知机制（抓取完成提醒，受 iLink 限流，考虑待阅制）
- [ ] skills/ 沉淀：把学习方法论沉淀为 Hermes Skill
- [ ] 清理工作区：.bak 备份文件、未提交的 fetch_articles.py 修改
