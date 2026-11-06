---
title: OpenViking连接业务系统，LLM Wiki一键编译
date: 2026-11-05
source: https://mp.weixin.qq.com/s?__biz=MzI1MzYzMjE0MQ==&amp;mid=2247524066&amp;idx=2&amp;sn=34ef93bca435a2d298fbe078aa081c69
account: 字节跳动技术团队
fetched_at: 2026-11-06 18:00:03 CST
article_id: 34ef93bca435a2d298fbe078aa081c69
---

OpenViking 2026-11-05 18:00 北京

  
  
*[图片]*

  
  
🔥**OpenViking上线数据连接器、知识编译功能**，支持飞书文档、项目和代码仓库的数据接入与同步，一键编译出业务需要的知识 Wiki、代码图谱、阶段性汇报产物，让 AI 帮你搞定项目交接、进展同步。

**OpenViking ✖️ 3D 内容理解模型**

OpenViking 是火山引擎推出的 Agent 上下文数据库，支持文档、图片、音视频、3D 等多模态数据的导入与理解。

现在，OpenViking 已上线多种数据连接器，支持飞书文档、项目、代码仓库的连接与定时同步。

使用可参考 [https://docs.volcengine.com/docs/vector_database_vikingdb/Overalldescription?lang=zh](https://docs.volcengine.com/docs/vector_database_vikingdb/Overalldescription?lang=zh)

*[图片]*

连接入口

*[图片]*

*[图片]*

数据导入

*[图片]*

定时同步

左右滑动查看更多精彩内容

基于导入的项目知识，通过知识编译(Compile)指令，就可以一键产出知识 Wiki、代码图谱、汇报材料等业务需要的加工产物，打通从数据连接到业务可用的高速通路。

支持自定义加工，使用可参考：[https://docs.volcengine.com/docs/vector_database_vikingdb/Compile-Compileresources?lang=zh#knowledge-graph](https://docs.volcengine.com/docs/vector_database_vikingdb/Compile-Compileresources?lang=zh#knowledge-graph)

*[图片]*

预置编译模版

*[图片]*

原始项目文件

*[图片]*

产物1：LLM-Wik

*[图片]*

产物2：知识图谱

左右滑动查看更多精彩内容

将数据导入 OpenViking，连接上你的 Agent，无论是豆包工作，Workbuddy，还是 Codex，Claude 都可以在以下场景感受到价值。

**场景一｜新人入职，快速了解项目全貌**

新员工入职、项目交接，动辄需要整理几万字的交接文档，新人理解多少还要另说。

现在，把项目资料上传到ov，一键形成 LLM Wiki，捕捉每一份上下文。新人安装好 ov，只需要跟自己的 Agent 说：“我是一个新来的研发，接下来主要负责xxx项目。根据 ov 公共库的内容，帮我梳理一份 onboarding 阅读材料”。

然后，Agent 就会自动通过 ov 查询，找到关联信息，最终推给用户一个含项目背景、目标、需求列表（来自飞书文档）、代码架构设计、模块设计（来自仓库）、项目进展、当前迭代情况（来自飞书项目）的完整阅读文档，同时通过 LLM-Wiki 清晰阐明各模块间的关系。

新人通过阅读了解很快就可以完成 onboarding。

*[图片]*

项目上传OV

*[图片]*

编译出LLM Wiki

*[图片]*

OpenViking + Codex检索

*[图片]*

Onboarding阅读材料

左右滑动查看更多精彩内容

**场景二｜周期汇报，业务进展一键追踪**

每次项目周会、季度总结，都需要成员一起复盘、梳理进展、互相关联，再集中呈现。

现在，项目在ov持续编译，LLM Wiki  实时更新。项目负责人只需要安装好 ov，跟自己的 Agent 说：“帮我整理xx项目这周的进展”。

然后，Agent 就会通过 ov 和最新的图谱，找到项目关联的所有产品需求、技术文档、市场反馈（来自飞书文档）、项目代码（来自仓库）以及当前版本正在开发的需求进展和 bug 处理进度（来自飞书项目）。最终整理出一份完整的市场、产品、技术进展以及版本迭代详情。

汇报再也不需要团队成员花时间去整理复盘，项目负责人也能随时获得最新反馈。

*[图片]*

项目上传OV

*[图片]*

编译出LLM Wiki

*[图片]*

OpenViking + Codex检索

*[图片]*

项目周报

左右滑动查看更多精彩内容

**场景三｜协同开发，代码逻辑清晰可见**

项目的 Git 仓库调用逻辑复杂、频繁更新，每次熟悉代码，都像剥了层皮一样痛苦。

现在，所有Git仓库都可以通过连接器上传到 OpenViking，并一键编译为 Code Wiki，清晰呈现函数间的调用和项目逻辑关系。每次开发时，你只需要跟安装好 ov 的 Agent 说：“基于xxx产品文档，帮我写一份技术方案”。

然后，Agent 就会通过ov自动查看库里同步的产品需求文档（来自飞书文档），找到当前项目的代码（来自于仓库），结合需求和现状，完成技术方案。如果是多人开发同一个项目也没关系，库里的仓库会保持定期同步，Code Wiki 也会动态更新，Agent 看到的永远是最新的，不用担心代码的版本问题。

进入测试，你也可以直接通过 Agent 看到所有的缺陷（来自飞书项目），指导它一步步完成修复，直到顺利上线。

*[图片]*

项目上传

*[图片]*

编译出LLM-Wiki

*[图片]*

OpenViking + Codex检索

*[图片]*

技术方案

左右滑动查看更多精彩内容

**最后**

OpenViking 将陆续覆盖钉钉、Confluence 等更多数据源，推出更强大且个性化的知识编译能力。

打通从数据连接到业务应用的高速通路。

现在接入，后续上线无需额外操作，即刻使用。

🚀 **上手试用，前 50 文档免费****：**

[https://s.c1ns.cn/WEuSd](https://s.c1ns.cn/WEuSd)

🌟 **开源 OpenViking****：**访问 GitHub 仓库

（[https://github.com/volcengine/OpenViking），为我们点亮一颗](https://github.com/volcengine/OpenViking），为我们点亮一颗) Star！

❓**三分钟测出你是哪种 Agent 饲养员选择属于你的 OpenViking**

[https://blog.openviking.ai/post/should-you-use-openviking/](https://blog.openviking.ai/post/should-you-use-openviking/)

💬 加入飞书交流群&微信群！

*[图片]*

点击阅读原文立即体验👇

[阅读原文](https://www.volcengine.com/product/openviking-service?utm_medium=social%5cx26amp;utm_source=wechat_bytetech%5cx26amp;utm_campaign=enterprise_knowledge_system_ai_20261105%5cx26amp;ov_target=landing)

[跳转微信打开](https://wechat2rss.xlab.app/link-proxy/?k=210e0544&r=1&u=https%3A%2F%2Fmp.weixin.qq.com%2Fs%3F__biz%3DMzI1MzYzMjE0MQ%3D%3D%26mid%3D2247524066%26idx%3D2%26sn%3D34ef93bca435a2d298fbe078aa081c69)
