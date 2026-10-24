---
title: OpenSandbox 正式加入 AAIF，从阿里开源项目走向行业公共基础设施
date: 2026-10-23
source: https://mp.weixin.qq.com/s?__biz=Mzg4NTczNzg2OA==&amp;mid=2247512151&amp;idx=1&amp;sn=4141fadeb55100e34b5481d5543e28b3
account: 阿里技术
fetched_at: 2026-10-24 18:00:04 CST
article_id: 4141fadeb55100e34b5481d5543e28b3
---

原创 OpenSandbox 2026-10-23 18:04 浙江

  
  
*[图片]*

  
Agent执行环境走向开放共建

  
今天，Agentic AI Foundation（AAIF）正式宣布接收四个新项目，阿里巴巴捐赠的 OpenSandbox 位列其中。另外三个项目分别是 Anthropic 捐赠的 Agent Skills、OpenAI 捐赠的 Open Responses 和 Hugging Face 捐赠的 OpenEnv。

AAIF 是 Linux 基金会旗下的一个中立、开放的基金会，它托管着用于智能体的开放协议和开源项目，目前包括模型上下文协议 (MCP)、goose、AGENTS.md、Agent2Agent (A2A) 、agentgateway 和 Agent Router 项目。

### 关于 OpenSandbox

OpenSandbox 是面向 AI 应用的通用沙箱平台。它提供多语言 SDK、统一的沙箱 API、Docker 和 Kubernetes 运行时，适用于编程智能体、GUI 智能体、智能体评估、AI 代码执行和强化学习训练等场景。它包含一个定义生命周期和执行 API 的沙箱协议，团队可扩展自定义运行时。

*[图片]*

这个项目始于一个具体的工程问题：AI 执行代码，需要一个安全且可隔离的地方。随着 Agent 进入真实任务，问题变得更加复杂——既要支持多语言接入、完备的执行能力与运行环境定制；也要适应高并发、短生命周期的负载，在启动延迟、批量吞吐与资源成本之间取得平衡；同时覆盖租户隔离、网络与凭据管控，以及运行过程的审计与追踪。基于此，OpenSandbox 内置命令执行、文件操作与代码解释器等能力，并支持 SDK、CLI、MCP 等多种接入方式；通过沙箱的批量创建与池化预热应对规模压力，MicroVM 沙箱可做到 100 毫秒级启动、按需 Snapshot 与跨主机 Pause/Resume；出入站流量管控与凭据隔离确保真实凭证不进入沙箱，运行指标基于 OpenTelemetry 标准化输出，可通过 OTLP 接入既有可观测体系。

自 2025 年 11 月开源以来，OpenSandbox 收获 GitHub Stars 16k，获 OpenSSF Best Practices Silver，收录于 CNCF Landscape；适配主流 Coding Agent 工具，并已集成了 Harbor、AgentScope、NeMo Gym、DeerFlow 等开源 Agent 框架；已在阿里内部生产环境中规模化落地，日均创建百万数量级的沙箱，内部版本与开源版本同源，核心逻辑始终在公开仓库中演进。

*[图片]*

### 捐赠 OpenSandbox

Linux 基金会是全球领先的开源软件、硬件、标准和数据协作平台。Linux、Kubernetes、Node.js、OpenSSF、PyTorch 等项目对全球基础设施至关重要。AAIF 正是这一治理模式在智能体 AI 领域的延伸，通过透明治理和广泛的产业参与，推动相关基础设施以开放、中立和生产级的方式持续演进。

加入 AAIF 后，OpenSandbox 将在这一治理框架下继续发展。开放的执行环境标准，是智能体系统能够跨框架、跨基础设施运行的前提。沙箱协议把沙箱如何创建、执行与回收写成一份规范，而不是某个产品的 API，任何团队都可以基于它接入自己的运行时，也可以参与决定规范本身如何演进。随着它被越来越多系统依赖，这份规范的方向更应该由使用它的人共同决定。进入 AAIF，意味着 OpenSandbox 从阿里巴巴主导的开源项目，进一步走向由中立基金会治理的行业公共基础设施。

“OpenSandbox 诞生于阿里巴巴，但我们不希望它的未来由一家公司来定义。把项目带入 AAIF，是为了开辟一条路径，让更多开发者和组织共同参与塑造沙箱环境在整个 Agent 生态中的运作方式。”

——许晓斌，阿里巴巴研发基础设施负责人

进入 AAIF 之后，我们会继续作为贡献者参与其中，也欢迎更多开发者、团队与组织加入共建。

---

点此了解更多关于 OpenSandbox 的信息：[https://aaif.io/projects/opensandbox](https://aaif.io/projects/opensandbox)

查看 AAIF 原文：

[https://www.prnewswire.com/news-releases/agentic-ai-foundation-announces-four-new-projects-agent-skills-open-responses-openenv-and-opensandbox-302916689.html](https://www.prnewswire.com/news-releases/agentic-ai-foundation-announces-four-new-projects-agent-skills-open-responses-openenv-and-opensandbox-302916689.html)

*[图片：图片]*

*[图片：图片]*

欢迎留言一起参与讨论~

[跳转微信打开](https://wechat2rss.xlab.app/link-proxy/?k=08c971f8&r=1&u=https%3A%2F%2Fmp.weixin.qq.com%2Fs%3F__biz%3DMzg4NTczNzg2OA%3D%3D%26mid%3D2247512151%26idx%3D1%26sn%3D4141fadeb55100e34b5481d5543e28b3)
