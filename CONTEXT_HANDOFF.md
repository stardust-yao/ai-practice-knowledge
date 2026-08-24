# 上下文交接文档 · Context Handoff

> 生成时间：2026-07-31
> 来源：微信 session（云服务器 47.85.56.224 上的 Hermes）
> 用途：让 mac 端 Hermes session（20260731_115501_0c2b1c）无缝继续以下工作

---

## 一、当前运行的系统（4 个 cron job）

### 每日精读三件套（都已接入"只看更新"去重）

| # | Job | 时间 | 内容 | 去重 |
|---|-----|------|------|------|
| 1 | 每日精读 · 晨间版（f70fabd4253e） | 每天 10:00 | AI Builders Digest：X推文/播客/GitHub Trending | 待接入 |
| 2 | 工程实践日报 · 午间版（71fb1515cd4c） | 每天 14:00 | 7个大厂公众号精选工程实践文章 | ✅ 已接入 fetch_new.py |
| 3 | 每日精读 · 晚间版（aefd87116322） | 每天 18:00 | 前沿项目/Product Hunt/HF论文/趋势洞察 | 待接入 |

### 推送守望哨兵（自动补发失败推送）
- Job：**6fc9de602759**，每小时 30 分运行，no_agent 模式
- 脚本：`~/.hermes/scripts/watchdog_push.py`
- 逻辑：检查 3 个推送 job 的 `last_delivery_error`，发现"内容生成成功但推微信失败"时，自动读取 cron output 里的 Response 重新推送；记录补偿时间戳，同一内容只补发一次；全部正常时静默

### 关键文件
- 去重抓取脚本：`/home/admin/.hermes/engineering-digest/fetch_new.py`
  - 用法：`python3 fetch_new.py --days 3`（只输出最近3天未推送过的新文章，自动标记已见）
  - 去重记录：`/home/admin/.hermes/engineering-digest/seen.json`
- 守望脚本：`/home/admin/.hermes/scripts/watchdog_push.py`
- 补偿记录：`/home/admin/.hermes/engineering-digest/compensated.json`
- 7个公众号 feed 配置在 fetch_new.py 的 FEEDS 字典里：
  - 腾讯技术工程 / 美团技术团队 / 字节跳动技术团队 / 阿里技术 / 小米技术 / 哔哩哔哩技术 / 阿里云开发者

### 已知问题
- **微信 iLink 推送限流**：内容太长会触发 `iLink sendmessage rate limited`。已通过拆分推送（10/14/18点）+ 哨兵补发缓解
- **旧 job 报错**：job `e2838e966197`（AI Builders Digest 双语）已删除但微信仍可能推送延迟错误通知，忽略即可
- DeepSeek 模型名已从 deepseek-chat 变更为 deepseek-v4-flash，cron job 需显式指定

---

## 二、模块化学习机制（skill）

- Skill 位置：`~/.hermes/skills/modular-learning/SKILL.md`
- 示例：`~/.hermes/skills/modular-learning/examples/spec-consistency.md`

### 核心理念
```
🎯 实践目标（可验证）
    ↓ 反向拆解
模块1 → 模块2 → 模块3 → ... → 模块N（按实现顺序）
每个模块 = 📚知识点 + 🔧实践项目 + ✅验收标准
```

### 规则
1. 反向拆解：从目标倒推，拆到"今天就能开始"的最小模块
2. 依赖顺序：前一个模块的产出是后一个模块的输入
3. 固定结构：目标 / 知识点 / 实践 / 验收 / 资源
4. 可验证的完成标准（不许"感觉学会了"）
5. 一次只做一个模块，没过验收不进下一个

---

## 三、学习工作台（Web 界面，已运行）

- **服务**：运行在云服务器 0.0.0.0:8787（后台进程，Python 标准库 http.server）
- **启动方式**：`cd /home/admin/.hermes/learning-workbench && python3 learning_workbench.py --port 8787`
- **数据文件**：`/home/admin/.hermes/learning-workbench/data.json`
- **前端**：`/home/admin/.hermes/learning-workbench/frontend.html`

### 功能
- 项目总览 + 进度条
- 模块链（点击展开：知识点/实践/验收/资源链接）
- 状态管理（未开始/进行中/完成）
- 每模块学习笔记（自动保存）
- 实践产出记录（粘贴代码/文档）
- 新建项目/添加模块（前端 UI 操作）

### 访问方式
- 公网 8787 被阿里云安全组拦截，需放行或 SSH 隧道：
  `ssh -L 8787:127.0.0.1:8787 admin@47.85.56.224` → 浏览器开 `http://localhost:8787`

### 已预置项目
**Spec 一致性学习项目**（spec-consistency）7 个模块：
1. 盘点现状找病根 → 2. 建立术语表 glossary → 3. 设计 spec 目录分层 → 4. 统一 spec 模板 → 5. 写 L1 一致性检查脚本 → 6. 建立迭代闭环 → 7. L3 语义检查（进阶）

---

## 四、知识沉淀：spec 一致性问题的解法（用户最近学习主题）

来源文章（都在 `/home/admin/work/AI实践项目/腾讯工程实践学习/raw/`）：
- 腾讯《开启Harness Engineering探索之旅》(2026-06-29) 2.3节：SSOT、目录分层、原位更新、归档三件套
- 腾讯《从AI Coding到Harness Engineering的端到端工程开发实践》(2026-07-03)：知识库工程
- 腾讯《Harness不是目的，知识才是护城河》(2026-05-11)
- 阿里《分解一座冰山：后端系统「AI知识库体系」建设实践》(2026-07-24)：4层知识库分层、技术元语定义重复、全流程闭环

### 核心解法对比
| 维度 | 腾讯 | 阿里 |
|------|------|------|
| 核心理念 | SSOT 从源头不让重复发生 | 分层消歧，承认不同上下文定义不同 |
| 手段 | 目录单向依赖 + 原位更新 + 强制归档 | 4层知识库 + 业务↔架构映射 + 闭环 |

### 可借用的跨领域方法
- Hook 模式（写 spec 前自动检查）
- 考试思维（多维度打分+归因）
- 契约模板（每类 spec 强制标准结构）
- 分层渐进检查（L1文本→L2交叉引用→L3语义）
- 反馈闭环（矛盾自动路由修复）
- 自检 Skill（harness-audit 模式）

---

## 五、重要约定

1. **不要修改用户已有项目** `/home/admin/work/AI实践项目/` 里的文件（腾讯工程实践学习目录）——新方案都在 Hermes 自有目录（`~/.hermes/`）下
2. 用户偏好：**中文回复、大白话**、内容详细清楚不精简
3. 用户使用 deepseek-v4-flash 模型
4. 每日推送用户偏好：内容要详细（"太短了看不明白"），但太长会触发微信限流，现在靠拆分+哨兵解决

---

*交接文档结束。mac 端 session 读取此文件后即可无缝继续所有工作。*
