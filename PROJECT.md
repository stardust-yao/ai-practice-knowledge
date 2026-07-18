# PROJECT.md — 腾讯工程实践 AI 知识飞轮

> 我（Hermes）每次进入这个项目时必须先读这个文件。

## 当前状态

- 阶段：抓取 pipeline 搭建中
- 上次更新：2026-07-18
- 知识条目数量：20
- 已产出 Skill 数：0

## 抓取方案（已确定）

- 来源：wechat2rss.xlab.app 免费 RSS
- Feed：`https://wechat2rss.xlab.app/feed/9685937b45fe9c7a526dbc32e4f24ba879a65b9a.xml`
- 方式：完全自动，无需扫码/Cookie
- 部署目标：阿里云服务器（47.85.56.224），Python 3.6.8 + git 2.43.7

## 目录结构

```
raw/              ← 原始文章存档（按月份，内容不经处理，原样保存）
  2026-07/
    YYYY-MM-DD_标题.md
knowledge/        ← 经处理后按主题分类（人工或自动整理后写入）
  methods/        ← 方法论
  tools/          ← 工具评估
  cases/          ← 落地案例
skills/           ← 沉淀为 Hermes Skill 的内容
logs/
  ops.md          ← 每次操作记录
  issues.md       ← 问题记录
```

## 我的工作规则

1. 每次处理文章后，更新 `logs/ops.md`
2. 结构性变更（修改分类、调整工作流）前，先告知用户并等确认
3. raw/ 文章命名格式：`YYYY-MM-DD_标题关键词.md`
4. raw/ 只存原始内容，不做任何修改
5. 每处理 10 篇文章，发起一次自进化回顾（提议，不自动执行）
6. 用户开始描述新项目/任务时，主动检索 `knowledge/` 中的相关方法并提醒

## 未完成的关键决策

- [ ] 定时抓取脚本编写与部署（RSS → raw/）
- [ ] raw/ → knowledge/ 的处理 pipeline（主题分类逻辑待定）
- [ ] 微信通知机制
- [ ] 主动提醒触发机制
