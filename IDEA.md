# 腾讯工程实践 AI 知识飞轮

## 项目定位

这不是一个"做完就结束"的项目，而是一套**持续运转的 AI 实践知识飞轮**：
- 自动抓取"腾讯技术工程"公众号文章 → 提炼进知识库 → 我在你开始新任务时主动检索并提醒相关方法 → 你应用 → 沉淀成 Hermes Skill
- 循环往复，越用越强

## 核心目标

1. **构建知识库**：系统学习腾讯技术工程公众号的 AI 实践文章
2. **知识应用**：在你进行任何 AI 项目/任务时，我 proactive 地提醒相关方法（如 loop-engineering、hook pattern 等）
3. **固化方法**：将学到的方法固化成 Hermes Skill，持续复用

## 已确认的架构

```
阿里云服务器（47.85.56.224）
├── Hermes Gateway（已运行）
└── we-mp-rss（待部署）—— 定时抓取"腾讯技术工程"新文章，转 Markdown，通过 Webhook 触发处理

GitHub 知识库（本仓库）
├── inbox/          ← 原始文章（we-mp-rss 抓取后存入）
├── knowledge/      ← 加工后的知识条目（你主要看这里）
│   ├── methods/    ← 方法类（loop-engineering, hook pattern 等）
│   ├── tools/      ← 工具类
│   └── cases/      ← 案例类
├── skills/         ← 可导入 Hermes 的 Skill 草稿
├── logs/           ← 我的操作日志（你不需要读）
│   ├── ops.md
│   └── issues.md
├── PROJECT.md      ← 项目上下文（我每次进来必读）
└── EVOLUTION.md    ← 系统结构的演化历史
```

## 技术选型

| 组件 | 方案 | 状态 |
|------|------|------|
| 文章抓取 | [we-mp-rss](https://github.com/rachelos/we-mp-rss)（⭐3.9k，Docker部署）| 待部署 |
| 知识库存储 | GitHub 仓库（本仓库）| ✅ 确认 |
| 知识检索 | Hermes search_files | ✅ 确认 |
| 主动提醒 | Hermes Skill（任务开始时加载）+ 定期 Cron | 待实现 |
| 部署平台 | 阿里云轻量服务器（与 Hermes Gateway 同机）| 待部署 |

## 待确认事项

- [ ] we-mp-rss 部署要求验证（是否需要微信扫码登录？依赖环境？）
- [ ] 主动提醒的具体触发机制（任务开始时 Skill 自动加载 + 定期推送）
- [ ] 自进化（self-evolution）触发方式：手动 / 每N篇文章后 / 定期 Cron

## 关键设计原则

1. **日志只给我用**：你日常只看 knowledge/ 目录
2. **PROJECT.md 我自动维护**：结构性变更先跟你确认
3. **自进化机制**：系统本身可以被修改，定期回顾并调整结构，避免过早固化
4. **渐进完善**：先跑通最小闭环，再逐步优化
