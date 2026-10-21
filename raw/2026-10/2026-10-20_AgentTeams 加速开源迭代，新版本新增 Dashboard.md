---
title: AgentTeams 加速开源迭代，新版本新增 Dashboard
date: 2026-10-20
source: https://mp.weixin.qq.com/s?__biz=MzcwOTMzMTQyMA==&amp;mid=2247517043&amp;idx=1&amp;sn=6ebb734c54b2cefbb5e0a39bac27e546
account: 阿里巴巴中间件
fetched_at: 2026-10-21 18:00:05 CST
article_id: 6ebb734c54b2cefbb5e0a39bac27e546
---

柳遵飞（翼严） 2026-10-20 16:12 浙江

  
  
*[图片]*

  
从组建到交付，让智能体团队的协作更清晰可控。

  
AgentTeams**[****1]**是一个开源的多智能体协作与运行管理项目，支持将多个 Agent 组织成团队，分工执行任务。用户可以参与团队沟通、查看执行结果，并在需要时介入调整。

AgentTeams Dashboard 为团队提供统一的管理界面：管理成员与权限，配置模型、技能和工具，通过项目与任务两级看板跟踪协作进展。

AgentCore**[****2]**是阿里云提供的商业化版本，在 AgentTeams 开源能力的基础上，进一步提供面向企业应用的高阶能力。欢迎前往 AgentCore了解和体验。

从 1.2.0 到 1.2.5，AgentTeams 完成了从 HiClaw 的正式升级，并引入 Dashboard 作为整体管控面。最近几个版本的主要更新，都围绕这个统一入口展开：完善团队资源管理，提供项目与任务两级看板，统一 Skill 管理，并扩展运行时管理能力。

**AgentTeams 1.2.5 已正式发布，默认搭配独立发版的 Dashboard v1.3.1，新增编码 CLI 管理、执行记录查看与 LLM 参数调优等功能。**

**统一的团队与资源管理**

Dashboard 将用户与权限、Agent 实例、团队关系，以及技能、工具和模型资源集中管理。主要包括以下几类：

- **用户与权限管理：管理 Human 用户及其可访问的团队和 Worker。管理员负责敏感配置，团队成员在授权范围内查看项目、管理技能和处理审批，也可以为指定 Worker 授予只读访问权限。相关权限变更保留审计记录。**
- **Worker 与 Manager 管理：集中查看和管理 Agent 实例，了解运行状态与会话，维护运行时、频道、模型、工具和技能配置。用户可以从资源列表进入具体实例，查看其配置与运行情况。**
- **团队管理：维护 Team 的成员与负责人关系，组织 Team Leader 和 Worker 的协作分工。Team Leader 协调项目，Worker 执行任务；团队关系与 Worker 自身的运行配置分别管理。**
- **Skill 管理：集中查看内置、共享和团队技能，上传自定义技能，并按成员职责分配给 Worker。同时提供远程技能库的接入与同步入口，便于维护和复用团队能力。**
- **MCP 管理：管理 MCP 服务及其接入配置，为 Worker 配置可调用的工具。工具服务和 Agent 的工具使用配置都有对应的管理入口，便于维护工具接入关系。**
- **模型与路由管理：维护模型和相关网关资源配置，管理模型访问路由，并为 Agent 配置所使用的模型，方便集中调整团队的模型接入方式。**

*[图片：AgentTeams Dashboard 总览]*

Dashboard 与 Matrix 各有分工：Matrix 房间承载人类和 Agent 的协作对话，Dashboard 提供资源、配置和执行状态的结构化视图，两者共同支持团队协作与人工介入。

*[图片：AgentTeams 平台整体架构]*

**项目与任务两级看板**

项目与任务两级看板是近期新增的重点功能，提供项目概览、任务依赖、执行状态和结果查看能力。项目列表集中展示各项目的状态、更新时间和任务分布，进入详情后可以查看工作流拓扑、阻塞点，以及接下来具备推进条件的任务。

**项目组织完整目标与任务关系，任务记录具体工作的执行信息。**项目视图展示整体进度、任务分布和依赖关系；任务详情保留负责人、执行要求、状态变化、提交结果与产物。

*[图片：项目与任务两级看板的层级与依赖关系]*

通过两级视图，用户可以从项目整体进展定位到具体任务，查看尚未完成的工作及其前置依赖，也可以追溯已经提交的结果。任务详情还记录状态转换历史、事件和进度信息，让用户了解任务何时派发、经过哪些状态变化，以及当前有哪些提交内容。

*[图片：项目看板中的任务依赖与状态]*

项目支持暂停与恢复，相关操作和状态变化保留在时间线中，便于人工干预和后续追溯。

1.2.5 进一步完善项目完成检查：仍有未终结任务时不允许提前完成项目；重新委派任务时会发送新的通知，减少任务改派后未被及时接收的问题。

*[图片：任务详情]*

**统一 Skill 管理与分发**

Skill 管理界面统一提供技能查看、上传、分发和复用能力。团队可以集中维护技能资源，再按 Worker 的职责分配，减少重复配置。

技能目录覆盖内置技能、共享技能、团队技能和插件自带技能。用户可以集中了解可用技能及其来源，并结合 Worker 的技能配置和运行状态，确认成员具备哪些工作能力。技能上传与分配受相应的团队权限约束。

除本地技能管理外，Dashboard 还提供远程 Nacos Skill Registry 的配置与同步入口，支持团队接入已有技能库。

*[图片：统一 Skill 管理界面]*

QwenPaw Manager 和 Worker 已支持技能热加载，技能更新后无需重启运行时。结合统一管理界面，技能从维护、分配到加载的过程更加方便。

1.2.5 还增加了 Skill ZIP 下载能力，便于获取完整技能包并进行导出与复用。

*[图片：Skill 管理与分发示意]*

**运行时管理与可靠性优化**

团队中的 Worker 可以采用不同的运行时。Dashboard 提供运行状态、会话和配置的查看与管理入口，便于用户了解成员的实际运行情况。运行管理也覆盖会话查看、执行循环设置，以及频道、工具和技能状态，具体支持范围与 Worker 的运行时相关。

这一轮更新完成了主要运行时链路从 CoPaw 到 QwenPaw 的升级，1.2.4 使用 QwenPaw 2.2.1。同时，DeepSeek Harness（DSH）作为实验性 Worker 加入，已有的 OpenClaw、Hermes 等 Worker 路径继续保留。DSH 当前仅用于 Worker，仍处于实验阶段。

模型配置支持声明视觉、推理等能力，子 Agent 可以使用独立模型或继承团队默认值，并支持运行时热更新。模型与网关路由也有统一的配置入口，便于集中维护团队使用的模型和工具访问配置。

1.2.5 扩展了 QwenPaw Worker 的 LLM 配置能力，支持重试次数、并发限制，以及流式响应的首段内容等待和输出间隔超时调优。Dashboard v1.3.1 提供相应的配置入口，方便按任务需要调整模型调用参数。

QwenPaw Worker 同时新增升级前兼容性检查、原地运行时升级、升级状态查询及失败回滚能力。原地升级会重启目标运行时，容器镜像版本仍按部署升级流程管理。

支撑这些管理功能的运行链路也在持续改进：减少重复文件同步与不必要的配置重载，改进升级时的配置和数据保留，并完善文件上传失败后的重试。团队成员发生变化时，只更新必要的团队信息与权限，避免重复加载未变化的模型、频道和工具配置。这些优化随近期版本一同交付。

1.2.5 还修复了 Manager 重启后的 Worker 恢复与设置保留问题，改进 MCP 注册和独立 Higress Console 接入，避免 Matrix 空转回合被显示为“已完成”。安装验证增加模型通道检查，Dashboard 会话密钥也会在升级时保留。

**编码 CLI 管理与执行记录**

1.2.5 已交付 **Coding CLI 扩展**，支持 Qwen Code、OpenCode 和 Qoder 等编码工具。Worker 可以将编码任务委派给这些工具，Dashboard v1.3.1 提供工具安装、状态检查、授权配置和执行参数的管理界面。

除配置工具外，Dashboard 新增编码执行记录与只读详情页面，支持查看关联任务、执行结果和日志，也能查看被阻止的执行记录，帮助用户了解编码工具实际执行了什么、结果如何。

平台还提供 Worker 环境变量编辑和网关身份探测能力，便于配置工具授权及排查模型、MCP 工具的访问问题。使用编码 CLI 前，需要安装相应工具并完成有效授权。

**体验与贡献**

AgentTeams 开源仓库提供安装指南与版本说明。安装后即可通过 Dashboard 管理团队资源、查看项目任务、配置技能，并结合 Matrix 房间开展多 Agent 协作。

欢迎通过 Issue 分享使用反馈，或通过 Pull Request 参与项目建设。

特别感谢主要贡献者 @LUOSENGWA (罗承华) 和 @nillikechatchat (孙伟) 对 AgentTeams 的持续贡献，也感谢参与代码、文档、测试和问题反馈的社区开发者。

相关链接：

[1] AgentTeams

[https://github.com/agentscope-ai/AgentTeams](https://github.com/agentscope-ai/AgentTeams)

[2] AgentCore

[https://www.aliyun.com/product/agentcore](https://www.aliyun.com/product/agentcore)

[3] @LUOSENGWA

[https://github.com/LUOSENGWA](https://github.com/LUOSENGWA)

[4] @nillikechatchat

[https://github.com/nillikechatchat](https://github.com/nillikechatchat)

[5] AgentTeams 开源仓库

[https://github.com/agentscope-ai/AgentTeams](https://github.com/agentscope-ai/AgentTeams)

[6] 安装与使用指南

[https://github.com/agentscope-ai/AgentTeams/blob/v1.2.5/install/README.md](https://github.com/agentscope-ai/AgentTeams/blob/v1.2.5/install/README.md)

[7] AgentTeams 1.2.5 发布说明

[https://github.com/agentscope-ai/AgentTeams/releases/tag/v1.2.5](https://github.com/agentscope-ai/AgentTeams/releases/tag/v1.2.5)

[8] Dashboard v1.3.1 发布说明

[https://github.com/agentteams-group/agentteams-dashboard/releases/tag/v1.3.1](https://github.com/agentteams-group/agentteams-dashboard/releases/tag/v1.3.1)

[9] AgentTeams Dashboard

[https://github.com/agentteams-group/agentteams-dashboard](https://github.com/agentteams-group/agentteams-dashboard)

[阅读原文](https://github.com/agentteams-group/agentteams-dashboard)

[跳转微信打开](https://wechat2rss.xlab.app/link-proxy/?k=2439e6c3&r=1&u=https%3A%2F%2Fmp.weixin.qq.com%2Fs%3F__biz%3DMzcwOTMzMTQyMA%3D%3D%26mid%3D2247517043%26idx%3D1%26sn%3D6ebb734c54b2cefbb5e0a39bac27e546)
