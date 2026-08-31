---
title: Mac mini缺货原因找到了！OpenAI、Anthropic都在抢
date: 2026-08-31
source: https://mp.weixin.qq.com/s?__biz=MzA3MzI4MjgzMw==&amp;mid=2651053642&amp;idx=2&amp;sn=4b05490be78424c57d2d1d2f7b3215ed
account: 机器之心
fetched_at: 2026-08-31 18:00:04 CST
article_id: 4b05490be78424c57d2d1d2f7b3215ed
---

原创 关注AI的 2026-08-31 10:18 山东

  
  
*[图片]*

  
AI时代硬通货。

  
*[图片]*

机器之心编辑部

内存芯片价格飞涨，普通消费者快买不起电脑了，另一边，适合运行 AI 负载的设备却卖得火热。

据《The Information》援引 OpenAI 内部消息人士报道，过去几个月，OpenAI 购买了数万台 Mac mini 和 Mac Studio，用于强化学习和计算机操作智能体的开发。

*[图片]*

这些设备被集中部署，用来训练和测试能够自主操作电脑的 Agent。报道还称，Anthropic 也在通过亚马逊 AWS 租用大量 Mac 算力。

*[图片]*

苹果电脑过去主要面向普通消费者和专业创作者，如今，它们开始以集群形式进入顶级 AI 实验室，承担代码测试、邮件整理、文档处理和多步骤任务执行。

Mac 的身份正在发生变化，它逐渐从个人电脑变成 AI 基础设施的一部分。

AI 实验室为何开始囤 Mac？

OpenAI 和 Anthropic 并不缺少 GPU。

它们拥有庞大的英伟达加速器集群，也在持续采购更多数据中心算力。OpenAI 突然大量购买 Mac，瞄准的是计算机操作智能体带来的新需求。

这类 Agent 需要点击按钮、输入文字、拖动文件，还要在不同应用之间连续工作。OpenAI 此前发布的 Computer-Using Agent 便通过强化学习，学习如何直接操作图形界面。

训练这类系统，需要大量可以并行运行、反复重置的操作系统环境，Agent 在其中执行任务，系统记录操作轨迹、判断结果是否正确，再将这些反馈用于后续训练。

Mac 在这里更像智能体的训练场和执行节点，它能够提供原生 macOS 环境，避免模拟系统与真实设备之间出现界面、权限和应用兼容性偏差。

因此，OpenAI 采购数万台 Mac，并不意味着其前沿模型的主训练已经从英伟达 GPU 集群迁移到苹果设备。Mac 更可能承担并行交互、轨迹采集、任务验证、本地推理以及部分后训练工作。模型参数的集中更新，大概率仍由数据中心加速器完成。

苹果 M 系列芯片采用统一内存架构，CPU、GPU 和神经网络引擎可以访问同一个内存池，减少数据在不同内存区域之间反复搬运。对于本地大模型推理，这能缓解消费级独立显卡常见的显存容量限制。

最新 M5 Ultra 版 Mac Studio 最高可配备 512GB 统一内存，内存带宽达到 1.2TB/s，如此大的内存池可以在单机中装入参数规模极大的量化模型。桌面机的主动散热设计，也更适合持续数小时甚至数天的高负载任务。

苹果还在新款 Mac Studio 中强化了多机协同。根据苹果官方介绍，多台设备可以通过雷雳 5 组成集群，分布式 AI 推理性能最高可达到单机的 3 倍。

苹果终于开始正视这门生意

Mac mini 曾是苹果生态中最便宜的桌面电脑。它体积小、功耗低，可以在没有显示器的情况下长期运行。随着常驻型 AI Agent 流行，这些原本普通的产品特征突然变得十分适合数据中心和本地 AI 部署。

《华尔街日报》此前报道称，Mac mini 上一年仅占苹果美国 Mac 销量的大约 3%，进入 2026 年后，它却成为私有化、全天候 Agent 的热门宿主。部分高内存版本一度出现数周乃至数月的交付延迟。

苹果似乎也被这股需求打了个措手不及。

《The Information》援引苹果前企业 AI 产品营销经理 Todd Dailey 的说法称，Mac 在企业 AI 市场的走红带有很强的偶然性，苹果此前没有围绕这一市场建立完整的企业工程支持和开发者关系体系。

今年 6 月，苹果在 Apple Park 举办了一场少见的闭门企业活动，Anthropic 联合创始人 Jared Kaplan 也出席了活动。报道显示，Mac mini 成为整场活动的重点产品。

到了 8 月 25 日，苹果发布 M6 Mac mini 和 M5 Ultra Mac Studio，宣传重点已经明显转向设备端 AI、大模型推理和多机集群。苹果还明确提出，开发者可以在 Mac 上本地运行和微调大模型。

*[图片]*

价格也随之上升。新款 M6 Mac mini 在中国市场起售价为 6999 元。2024 年，配备 16GB 内存的 M4 Mac mini 起售价为 4499 元。两年时间，Mac mini 的入门价格提高了约 56%。芯片升级是一部分原因，内存和存储成本上涨也在推高整机价格。

AI 需求已经体现在苹果的财务数据中。苹果 2026 财年第三季度 Mac 业务收入达到 103.52 亿美元，同比增长约 28.7%，增速超过同期其他硬件品类。

企业和开发者对高内存 Mac 的需求，已经成为这轮增长中不可忽视的变量。

桌面 AI，成了苹果和英伟达的新战场

苹果的变化已经引起英伟达的注意。

从 DGX Spark 到今年新公布的 RTX Spark，英伟达正在把数据中心中的 AI 计算能力压缩到桌面机和笔记本中。RTX Spark 集成 Grace CPU 和 Blackwell GPU，提供最高 1 PFLOP 的 AI 计算性能和 128GB 统一内存，同时支持 CUDA、TensorRT 和 RTX 软件栈。

*[图片]*

英伟达将其直接定义为面向个人智能体的新型 PC。按照官方规划，首批 RTX Spark 笔记本和紧凑型台式机将在今年秋季上市。

产品尚未正式发售，供应已经趋紧。据报道，华硕首批 RTX Spark 机型已被渠道客户预订一空，微星高端 N1x 机型的首批货源也接近售罄，两家公司都在向英伟达争取更多配额。

苹果和英伟达由此站上了同一条新赛道。

苹果拥有大容量统一内存、较高能效和原生 macOS 环境。英伟达则掌握 CUDA、TensorRT 和更成熟的 AI 开发生态，并与 Windows 智能体体系深度结合。双方争夺的核心场景包括本地推理、Agent 执行、强化学习轨迹生成、模型评测和轻量后训练。

这些桌面设备短期内不会取代大型训练集群。它们补上了云端算力难以完全覆盖的一层：让 Agent 靠近用户数据、操作系统和真实应用，并以较低延迟持续运行。

供给问题也随之出现。

AI 数据中心正在大量消耗 DRAM 和 NAND，推高整个存储市场的成本。与此同时，本地 AI 和智能体又需要更大的内存容量。上游数据中心与下游 AI 终端同时争抢内存，最终形成价格上涨、交付延迟和高端型号缺货的连锁反应。

Mac mini 的走红，揭示了智能体时代的一条新硬件路线。未来的 AI 算力不会只集中在巨型数据中心，越来越多计算任务会被分配到办公室、家庭和企业机房中的本地节点。

AI 硬件的下一场竞争，已经从云端延伸到了每一张办公桌。

参考链接：

[https://www.theinformation.com/articles/apple-stumbled-ai-hardware-success-mac](https://www.theinformation.com/articles/apple-stumbled-ai-hardware-success-mac)

[https://wccftech.com/openai-hoarding-tens-of-thousands-of-apple-mac-mini-and-mac-studio-devices-as-asus-and-msi-burn-through-their-entire-first-batch-of-nvidia-rtx-spark-chip-and-beg-for-more/](https://wccftech.com/openai-hoarding-tens-of-thousands-of-apple-mac-mini-and-mac-studio-devices-as-asus-and-msi-burn-through-their-entire-first-batch-of-nvidia-rtx-spark-chip-and-beg-for-more/)

*[图片：图片]*

© THE END

转载请联系本公众号获得授权

投稿或寻求报道：liyazhou@jiqizhixin.com

[跳转微信打开](https://wechat2rss.xlab.app/link-proxy/?k=bbe7dc2a&r=1&u=https%3A%2F%2Fmp.weixin.qq.com%2Fs%3F__biz%3DMzA3MzI4MjgzMw%3D%3D%26mid%3D2651053642%26idx%3D2%26sn%3D4b05490be78424c57d2d1d2f7b3215ed)
