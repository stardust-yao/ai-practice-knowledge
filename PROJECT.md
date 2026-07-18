# PROJECT.md — 腾讯工程实践 AI 知识飞轮

> 我（Hermes）每次进入这个项目时必须先读这个文件。

## 当前状态

- 阶段：自动抓取已运行，手动补录进行中
- 上次更新：2026-07-18
- raw/ 文章数：20 篇（2026-06-22 ~ 2026-07-17）
- 已产出 Skill 数：0

---

## 抓取方案

### 自动抓取（每日定时）
- 来源：wechat2rss.xlab.app 免费 RSS
- Feed URL：`https://wechat2rss.xlab.app/feed/9685937b45fe9c7a526dbc32e4f24ba879a65b9a.xml`
- 脚本：`fetch_articles.py`（项目根目录）
- 触发：阿里云服务器 cron，每天凌晨 2 点（待部署）
- 服务器：47.85.56.224，Python 3.6.8 + git 2.43.7

**已知限制：免费版硬限返回最近 20 篇，无历史分页**
- `?page=`/`?limit=`/`?count=`/`.json` 等参数均无效
- 历史文章（20篇之前）只能通过手动导入补录
- 付费自托管（¥150/年）可解除限制，暂未启用

### 手动补录（历史文章 / 用户指定文章）
- 脚本：`add_article.py <微信文章URL>`
- 用途：用户发来觉得有价值的历史文章链接，逐篇抓取入库
- 输出同样写入 `raw/YYYY-MM/`，格式与自动抓取完全一致
- 每次运行同样追加写入 `logs/ops.md`

---

## 目录结构

```
raw/              ← 原始文章存档（按月份，内容不经处理，原样保存）
  2026-07/
    YYYY-MM-DD_标题.md
knowledge/        ← 经处理后按主题分类（人工或 AI 整理后写入）
  methods/        ← 方法论（如 Harness Engineering、Loop Engineering）
  tools/          ← 工具评估
  cases/          ← 腾讯落地案例
skills/           ← 沉淀为 Hermes Skill 的内容
logs/
  ops.md          ← 每次操作自动追加（脚本写入，不需要手动维护）
  fetch_state.json← 已抓取文章 ID，用于去重
  issues.md       ← 问题记录
```

---

## 脚本说明

### fetch_articles.py — 自动抓取
```bash
python3 fetch_articles.py           # 正常运行
python3 fetch_articles.py --dry-run # 只打印，不写文件不提交
```
每次运行自动完成：拉取 RSS → 去重过滤 → HTML转Markdown → 写入raw/ → 更新fetch_state.json → 写ops.md → git commit+push

### add_article.py — 手动单篇导入
```bash
python3 add_article.py "https://mp.weixin.qq.com/s?__biz=...&sn=..."
```
支持直接传入微信文章 URL，抓取全文保存到 raw/，同样写入 ops.md 和 git push。

---

## 工作规则

1. 每次操作后自动写入 `logs/ops.md`（脚本负责，无需手动）
2. 结构性变更（修改分类、调整工作流）前，先告知用户并等确认
3. raw/ 文章命名格式：`YYYY-MM-DD_标题关键词.md`，raw/ 内容不做任何修改
4. 每处理 10 篇文章，发起一次自进化回顾（提议，不自动执行）
5. 用户开始描述新项目/任务时，主动检索 `knowledge/` 中的相关方法并提醒

---

## 待完成

- [ ] fetch_articles.py 部署到阿里云 + 配 cron
- [ ] add_article.py 编写（手动单篇导入，用户已开始补录历史文章）
- [ ] raw/ → knowledge/ 处理 pipeline（主题分类逻辑待定）
- [ ] 微信通知机制
