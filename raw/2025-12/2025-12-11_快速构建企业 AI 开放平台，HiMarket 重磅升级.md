---
title: 快速构建企业 AI 开放平台，HiMarket 重磅升级
date: 2025-12-11
source: https://mp.weixin.qq.com/s?__biz=MzU4NzU0MDIzOQ==&amp;mid=2247520228&amp;idx=1&amp;sn=3932db7f0e7a26d8b79145054d7b94b7
account: 腾讯技术工程
fetched_at: 2026-07-31 12:38:28 CST
article_id: 3932db7f0e7a26d8b79145054d7b94b7
---

阿里巴巴中间件 2025-12-11 19:11 浙江

  
  
*[图片]*

  
Agent 的下一站。

  
*[图片：图片]*

本文作者：赵恒、岛风、文想、彦林、于怀

2025 是 Agent 元年，企业开始大规模落地 Agent，都会遇到多 Agent 管理，多 MCP 工具管理，多模型管理问题，如何查找和选择合适的 Agent/MCP/Model？哪些高频场景可以快速让所有人参与？多个团队如何协同，权限如何管理，成本如何分摊？

为了解决这些挑战，阿里巴巴升级 AI 开放平台 HiMarket，基于阿里巴巴内部 IdeaLAB，扩展 AI 开放平台的能力，推出 v0.5.0 版本，提供 Agent/MCP/Model 市场能力，提供基于 Chat 的高频使用场景，提供账号权限管理和成本分摊能力。

*[图片：BB584FD1-A8C3-4F31-8338-910BA4BB8499.png]*

**01**

***HiMarket 是什么***

*Aliware*

HiMarket 是开源的 AI 开放平台，帮助企业快速构建 Agent 市场，释放 AI 创新潜能。对企业全员提供高频 AI 场景，释放 AI 创新潜能；为开发者提供 Agent 市场/MCP 市场/Model 市场，提升研发效能；为维护者提供 AI 治理能力，提升 AI 把控力。

*[图片：image.png]*

**02**

***使用场景***

*Aliware*

**AI 场景（面对企业员工）**

HiMarket 提供了 HiChat 能力，通过 Chat 模式替代搜索，做市场调研和产品调研，生成运营图片等工作。

*[图片：image.png]*

- **企业全员 AI 使用入口：通过 HiMarket AI 开放平台，同时解决了员工不知道用哪些模型，企业如何管控员工用模型的两个问题；全员可以通过这个入口进行使用 AI 模型能力，企业可以进行整体安全合规审核，保证企业和员工使用 AI 范围安全可控。**
- **多模型对比：可以选择多个模型市场的模型，输入一次对比多个模型，快速直接对比模型返回内容差异，选取最优内容。**
- **会话历史记录：方便员工管理历史会话记录，可以快速基于历史信息进行对话回溯，并且计划后续基于对话可以形成知识点，知识点可以进行横向传递，提升数据共享效率。**
- **联网搜索：通过体验中心可以支持配置联网搜索能力，配置 Higress AI 网关联网搜索能力之后，所有模型都可以支持联网搜索，AI 网关会把对应搜索内容传递给模型使用摘取，扩大实时数据能力。**
- **支持关联 MCP 工具：体验中心聊天框支持关联 MCP 市场，可以实时快速的使用 MCP 能力，可以快速体验验证 MCP 本身能力情况，并且支持企业原本 API 快速配置化转换成 MCP 协议，结合模型做快速验证。**

**AI 市场（面对开发者）**

HiMarket 支持构建涵盖 Agent、MCP Server、Model 的完整 AI 市场，让企业的各类 AI 资源不再分散，而是以标准化方式汇聚在一个平台上。

*[图片：image.png]*

- **Agent 市场：支持将复杂的 AI Agent 应用打包上架，可对接 AgentScope 等 Agent 开发平台，例如通过 AgentScope 构建的 Agent 可一键注册到 HiMarket，其他开发者订阅后即可直接使用，无需从零搭建；支持跨框架、跨语言的 agent 一键发布到 Agent 市场。**

*[图片：image.png]*

- **MCP 市场：支持接入不同平台的 MCP Server，并支持将外部 API 转换为标准化的 MCP Server，开发者订阅后，即可让 AI 应用轻松调用外部能力。**

*[图片：image.png]*

- **模型市场：支持公有云模型及企业自研私有模型的快速接入，平台以 Higress 作为模型服务的网关代理，提供内容安全、Token 限流等防护能力，保障模型服务对外开放的安全合规。**

*[图片：image.png]*

- **AI 资产生命周期管理：管理员将资源接入平台，配置访问策略和使用文档，发布上架；开发者在门户浏览、订阅、获取调用凭证即可订阅使用。**

**AI 治理（面对 AI 维护者）**

HiMarket 实现了对 AI 资源的集中式治理，提供全方位的安全管控和协作能力：

- **安全合规保障：通过 Higress 网关统一管控所有 AI 资源的访问，支持内容安全检测、敏感信息过滤、访问权限控制，确保企业 AI 能力对外开放时符合安全合规要求。**
- **高效协作共享：打破团队间的“能力孤岛”，一个模型或工具接入后，可被多个部门订阅复用，避免重复采购和重复开发。**
- **降低使用门槛：开发者无需逐一对接不同厂商的 API，HiMarket 提供统一的协议标准和开箱即用的调用凭证，大幅降低接入成本，让团队更专注于业务创新而非基础设施搭建。**

**03**

***产品优势***

*Aliware*

**企业级能力**

HiMarket 内置完善的企业级管理能力，确保 AI 资源的安全开放与高效运营。

- **产品管理：管理员可为不同 API 产品配置独立的认证鉴权和可见性策略，同时提供流量控制、IP 白名单等防护能力，保障服务安全稳定。**
- **观测分析：提供管理员视角的全局观测大盘，展示 AI API 的调用趋势、热门产品排行、异常流量预警等，支持按时间、产品类型、开发者等维度进行多维分析，为企业运营优化提供数据依据。**
- **计量计费：支持基于 Token、调用次数等多种计量模式，自动统计资源消耗并生成账单明细，既能服务企业内部的成本核算，也能支撑对外商业化运营。**
- **版本管理：支持 API 产品的多版本并行，管理员可以发布新版本、维护旧版本并平滑迁移用户，通过版本对比、灰度发布、快速回滚等功能，确保产品迭代的安全稳定。**

*[图片：image.png]*

**丰富观测能力**

观测分析（目前 v0.5.0 版本依赖阿里云商业化 SLS，开源版本的观测分析实现计划在后续版本中提供）：

*[图片：image.png]*

**灵活扩展能力**

为了能够快速对接企业现有的系统，HiMarket 提供了灵活的定制能力，包括：

- **门户品牌：管理员可为门户配置自定义域名、Logo、主题色、布局样式等元素，并灵活配置首页模块、产品分类、推荐栏等功能区域。**
- **身份认证：支持内置账号密码和企业 OIDC 认证方式，可与企业 SSO、IDaaS 等身份系统无缝集成，实现统一的用户管理和身份认证。**
- **审批流程：开发者注册、凭证申请、API 订阅等关键流程可灵活配置自动或人工审批。**

*[图片：image.png]*

**04**

***快速体验***

*Aliware*

HiMarket 提供多种部署方式，满足不同场景需求：

- 本地快速体验：HiMarket 本地部署指南**[****1]**。
- Docker Compose 部署：HiMarket Docker 部署指南**[****2]**。
- Kubernetes 部署：HiMarket Helm 部署指南**[****3]**。

**一键部署，开箱即用的完整方案**

HiMarket、Higress、Nacos 三大组件自动编排部署，无需人工干预。部署过程自动完成示例 MCP Server 的注册、配置和发布，让你在部署完成后即可体验 HiMarket 能力市场。无论是 Docker Compose 还是 Kubernetes 部署，均只需一条命令：

```
./deploy.sh install
```

部署脚本会自动完成以下所有工作：

- **核心组件部署：自动拉起 MySQL、Nacos 配置中心、Higress 网关服务**
- **应用本体部署：部署 HiMarket 全套服务（管理后台、开发者门户、后端服务）**
- **智能初始化：自动创建管理员账号、配置示例 MCP Server、发布演示 API 产品**
- **即开即用：部署完成后即可访问管理后台和开发者门户，无需任何手动配置**

方案支持灵活的场景适配：

- 支持使用内置 MySQL 或对接已有数据库
- 支持使用阿里云商业化 MSE 服务和 AI 网关服务
- 支持 ./deploy.sh himarket-only``仅部署 HiMarket 本体

详细步骤请参考：HiMarket Docker 一键部署指南**[****4]**，HiMarket Helm 一键部署指南**[****5]**。

**05**

***HiMarket Roadmap 规划***

*Aliware*

*[图片：image.png]*

**06**

***欢迎共建***

*Aliware*

HiMarket 是多个开源社区共同发起的开源项目，核心参与者包括阿里云、蚂蚁数科、高德、淘天等团队，面向开源可以助力企业快速构建 AI 开放平台，提供开箱即用的能力。

特别感谢淘天 IdeaLAB 团队为 HiMarket 提供的基础，期待更多企业一起参与共建～

HiMarket 仓库：[https://github.com/higress-group/HiMarket](https://github.com/higress-group/HiMarket)
基于 HiMarket 实现的 MCP 金融级市场：[https://antdigital.com/products/MCP](https://antdigital.com/products/MCP)

HiMarket 钉钉社区群（2 群）：163370001036

*[图片：image.png]*

入群链接（复制到浏览器打开）：[https://qr.dingtalk.com/action/joingroup?code=v1,k1,d+MJWsDVtfHq6XanvQEUxsVX3vVL1m+7DWfkoUkYxVM=&_dt_no_comment=1&origin=11](https://qr.dingtalk.com/action/joingroup?code=v1,k1,d+MJWsDVtfHq6XanvQEUxsVX3vVL1m+7DWfkoUkYxVM=&_dt_no_comment=1&origin=11)

推荐文章：

《[AgentScope Java v1.0 发布，让 Java 开发者轻松构建企业级 Agentic 应用](https://mp.weixin.qq.com/s?__biz=MzU4NzU0MDIzOQ==&mid=2247520193&idx=1&sn=cb69fc4c4e061fc0065e1f245f55bbed&scene=21#wechat_redirect)》

# 相关链接：

# [1] HiMarket 本地部署指南

# https://github.com/higress-group/himarket/blob/main/README.md
[2] HiMarket Docker 部署指南
[https://github.com/higress-group/himarket/blob/main/deploy/docker/Docker%E9%83%A8%E7%BD%B2%E8%AF%B4%E6%98%8E.md](https://github.com/higress-group/himarket/blob/main/deploy/docker/Docker%E9%83%A8%E7%BD%B2%E8%AF%B4%E6%98%8E.md)

# [3] HiMarket Helm 部署指南

[https://github.com/higress-group/himarket/blob/main/deploy/helm/Helm%E9%83%A8%E7%BD%B2%E8%AF%B4%E6%98%8E.md](https://github.com/higress-group/himarket/blob/main/deploy/helm/Helm%E9%83%A8%E7%BD%B2%E8%AF%B4%E6%98%8E.md)

# [4] HiMarket Docker 一键部署指南

[https://github.com/higress-group/himarket/blob/main/deploy/docker/Docker%E9%83%A8%E7%BD%B2%E8%84%9A%E6%9C%AC%E8%AF%B4%E6%98%8E.md](https://github.com/higress-group/himarket/blob/main/deploy/docker/Docker%E9%83%A8%E7%BD%B2%E8%84%9A%E6%9C%AC%E8%AF%B4%E6%98%8E.md)

# [5] HiMarket Helm 一键部署指南

[https://github.com/higress-group/himarket/blob/main/deploy/helm/Helm%E9%83%A8%E7%BD%B2%E8%84%9A%E6%9C%AC%E8%AF%B4%E6%98%8E.md](https://github.com/higress-group/himarket/blob/main/deploy/helm/Helm%E9%83%A8%E7%BD%B2%E8%84%9A%E6%9C%AC%E8%AF%B4%E6%98%8E.md)

[阅读原文](https://higress.ai/himarket)

[跳转微信打开](https://wechat2rss.xlab.app/link-proxy/?k=7eee732f&r=1&u=https%3A%2F%2Fmp.weixin.qq.com%2Fs%3F__biz%3DMzU4NzU0MDIzOQ%3D%3D%26mid%3D2247520228%26idx%3D1%26sn%3D3932db7f0e7a26d8b79145054d7b94b7)
