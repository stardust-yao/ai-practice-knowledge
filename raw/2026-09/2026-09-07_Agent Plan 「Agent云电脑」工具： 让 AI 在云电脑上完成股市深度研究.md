---
title: Agent Plan 「Agent云电脑」工具： 让 AI 在云电脑上完成股市深度研究
date: 2026-09-07
source: https://mp.weixin.qq.com/s?__biz=MzI1MzYzMjE0MQ==&amp;mid=2247522149&amp;idx=1&amp;sn=383a089a1ed8658ac6742851ca4d4325
account: 字节跳动技术团队
fetched_at: 2026-09-08 18:00:03 CST
article_id: 383a089a1ed8658ac6742851ca4d4325
---

Agent Plan 2026-09-07 19:00 北京

  
  
*[图片]*

  
  
**引言**

你有没有过这样的经历：接到一个深度调研任务，要查行情、翻研报、对数据、写分析，一坐就是大半天，浏览器开了十几个标签页，还得反复切换整理？

如果能把这些活儿 "丢给云端"，让一台 24 小时在线的云电脑自己拆解任务、检索资料、生成报告，而你只需要最后验收结果 ，将显著提升工作效率。

今天这篇文章，就来聊聊火山方舟 Agent Plan 里专属 Harness工具「Agent 云电脑」。它不只是一个远程桌面，而是一个自带 agent loop、能自行拆解并执行复杂任务的云端助手。

**核心亮点：**

- **跨网页与桌面操作：** CUA 可以在云桌面中打开网页、使用站内搜索、滚动页面、切换标签页，并处理需要交互的页面。它适合多步 GUI 工作流，不局限于返回搜索摘要。
- **一次委派，持续观察：**只创建一次任务，云平台可自动拆解并执行复杂任务。平台可持续监控任务进度，监控任务中断不影响任务执行，可以随时停止和恢复任务监控。
- **长程复杂任务自行拆解：** 对于复杂任务，云电脑agent可以自行拆解，充分利用云电脑预装的软件和交互方案，完成复杂任务。

我们以 "做一份股市大盘深度研究" 为例演示「Agent 云电脑」能力，把复杂调研交给云端，真的可以很简单。

**前置准备**

- **购买套餐：请登陆「火山方舟」或 「官网活动页」，购买Agent Plan套餐**

**1. 购买Agent Plan套餐**

进入 Agent Plan 控制台 购买 Agent Plan 套餐。购买后即可开启使用套餐内专属Harness工具。

注意：目前Agent 云电脑（Computer Use Agent）当前仅支持在 **Large/Max套餐** 下使用。

*[图片]*

**2. 安装并配置skill**

Agent 云电脑只使用 Agent Plan 凭证。推荐先用 arkcli 安装和配置 skill。

**使用 arkcli 安装和配置（推荐）。**

- 安装 arkcli

```
npm i @volcengine/ark-cli -g --registry https://registry.npmjs.org
```

- 通过 arkcli 配置 agentplan 并安装 cua，其中 profile 选择 agent plan

```
arkcli helper mcp codex --capability cua
```

在 codex 中确认是否已经安装完毕

*[图片]*

**详细操作指南**

**Step1  通过 skill 来发起任务**

Agent 云电脑是一个开箱即用的一个 skill，初次登录时，服务端会给用户分配一个云电脑，后续用户使用同一个 api key 登录时，会复用之前的云电脑机器，因此你可以随时启用云电脑而不必担心配置和安装的软件丢失。

Agent 云电脑自带 agent loop，因此可以不必像传统的 computer use 工具一样，只暴露基础的操作接口，agent需要频繁和云桌面操作，而只需要下达指令即可，Agent 云电脑可以自行拆解复杂任务，并自己驱动执行。

*[图片]*

**Step2  等待任务执行完成**

云电脑的 agent 会自动解析和拆解任务，并且触发云端安装的软件和工具进行资料检索。

*[图片]*

完成资料整理和分析，生成有深度的分析。

*[图片]*

*[图片]*

**Step3  登录云电脑查看执行过程**

可以通过 skill让agent 返回临时 URL 来访问 Agent 云电脑查看执行过程和执行产物。

*[图片]*

*[图片]*

**Step4 查询 AFP 用量消耗**

用户可通过方舟控制台查询 Agent Plan 套餐 AFP 的实时用量，完成该深度研究预估消费 11.46 AFP，此外还会根据任务独立消耗 token，请注意用量消耗根据个人具体使用情况存在差异。

详情可见 AFP 积分机制：

- 该 Demo 实现的预估 AFP 消耗明细如下：

**消耗项**

**消耗量**

**预估 AFP消耗**

**机器占用**

本次任务耗时11分钟，按照实际占用机器时长折算

11.46 AFP

**Token 消耗**

本次任务使用 Deepseek V4 pro 作为 CUA agent，输入消耗1221.3K，输出消耗29.7K

688.050 AFP

**结尾**

当然，Agent 云电脑的能力远不止做股市研究 —— 行业调研、竞品分析、资料汇总、数据采集…… 凡是需要多步检索和整理的复杂任务，都可以交给它来跑。

目前「Agent 云电脑」已在 Agent Plan 的 Large/Max 套餐开放，如果你手头正好有 "必须开浏览器、来回切换窗口才能完成" 的任务，不妨去尝试一次

[跳转微信打开](https://wechat2rss.xlab.app/link-proxy/?k=d391eac3&r=1&u=https%3A%2F%2Fmp.weixin.qq.com%2Fs%3F__biz%3DMzI1MzYzMjE0MQ%3D%3D%26mid%3D2247522149%26idx%3D1%26sn%3D383a089a1ed8658ac6742851ca4d4325)
