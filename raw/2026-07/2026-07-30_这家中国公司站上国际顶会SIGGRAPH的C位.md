---
title: 这家中国公司站上国际顶会SIGGRAPH的C位
date: 2026-07-30
source: https://mp.weixin.qq.com/s?__biz=MzA3MzI4MjgzMw==&amp;mid=2651047451&amp;idx=1&amp;sn=274e2733c0b51bffa02aeed28256404c
account: 腾讯技术工程
fetched_at: 2026-07-31 12:38:26 CST
article_id: 274e2733c0b51bffa02aeed28256404c
---

原创 关注AI的 2026-07-30 13:52 北京

  
  
*[图片]*

  
VAST在全球顶级学术舞台吸引全场最多目光

  
*[图片：图片]*

编辑｜陈陈

7 月 19 日至 23 日，美国洛杉矶，SIGGRAPH 2026 如期而至。这场汇聚全球计算机图形学与视觉计算领域顶尖学者、艺术家与工程师的年度盛会，吸引了来自 69 个国家的近万名参会者。渲染、几何建模、动画仿真、与生成式 AI，几乎所有关于如何用计算机创造视觉世界的最前沿探索，都在这五天里集中呈现。

而今年，这场盛会的聚光灯里，全球领先的通用人工智能公司 VAST（研发了Tripo系列3D大模型）成为大会上出现频率最高的中国团队之一：

登上 SIGGRAPH 主会场 Keynote，与迪士尼、英伟达、Bolt Graphics 一同进入本届大会四场主题演讲阵容；五篇论文入选 Technical Papers，覆盖网格生成、3D 高斯生成、纹理生成、可交互 3D 资产生成和跨拓扑动画。

*[图片]*

VAST 首席科学家曹炎培博士 Keynote 演讲

团队还在大会标志性的 Real-Time Live! 环节拿下最高奖 Best in Show。

*[图片]*

会场之外，VAST 与李飞飞创立的 World Labs 联合举办黑客松和世界模型行业之夜。大会同期，VAST 首席科学家曹炎培入选《麻省理工科技评论》TR35 中国区名单。

几件事叠加在一起，让这家成立仅三年的公司备受瞩目。

主舞台上的茶壶测试

如果说 SIGGRAPH 有什么环节最能代表这一年图形学领域最值得所有人都听一听的声音，那就是大会的 Keynote 环节。今年的 Keynote 只有四场，分别来自迪士尼、英伟达、Bolt Graphics，以及 VAST。

7 月 22 日下午，曹炎培博士带领算法团队登上 Main Stage，带来题为《The Teapot Test: First It Tested Showing. Now It Tests Making》的演讲。

*[图片]*

这个题目背后有一段计算机图形学的老典故：1975 年，计算机图形学先驱 Martin Newell 用手工测量的方式，做出了一个茶壶模型，这是人类历史上最早的 3D 模型之一，后来成为整个图形学领域检验渲染能力的标准测试对象。半个世纪以来，茶壶测试考验的始终是计算机能否把一个三维物体逼真地呈现出来。

但曹炎培认为，到了生成式 AI 时代，这道延续了半个世纪的考题需要被重新定义。

如今，生成模型已经能够跳过尺子、方格纸和手工录入。输入一句话，模型便可以生成一只表面光滑、光影逼真，还能从不同角度观察的茶壶，这样的结果看起来已经足够完整。

曹炎培随后向这只茶壶提出了三个要求：把它放进游戏，用 3D 打印机制造出来，或者用它训练机器人倒茶。这三个要求都无法真正完成。原因在于，画面背后根本没有一只真正存在的茶壶。

*[图片]*

VAST 首席科学家曹炎培博士 Keynote 演讲。演讲地址：[https://www.youtube.com/watch?v=zZ8fbEeaG-8](https://www.youtube.com/watch?v=zZ8fbEeaG-8)

模型可以生成大量精美图像，但它未必拥有可靠的网格、可编辑的拓扑、真实存在的几何细节、能够运动的关节，以及可以被仿真器读取的物理属性。

正如曹炎培所说：你可以围着它看，却无法真正触碰它。

五十年前，茶壶测试的是机器能否将一个物体展示出来。今天，新的茶壶测试开始追问：机器能否真正创造一个物体？

这里所说的创造，意味着生成结果可以进入游戏引擎，被 3D 打印，成为机器人训练和物理仿真的对象。

其实这是 VAST 第二次进入 SIGGRAPH 的 Keynote 演讲阵容。

三年前，VAST 创始人兼 CEO 宋亚宸曾与黄仁勋等世界级企业家同台，成为第一位在 SIGGRAPH 发表主题演讲的中国企业家。当时，生成式 3D 仍处于早期阶段，行业最直接的想象是大幅降低建模门槛。

三年之后，同一家公司再次站上主舞台，讨论的问题已经从怎样生成一个模型，扩展到怎样建立全栈 3D 生产体系，以及怎样驱动一个持续运行的世界。

在 Real-Time Live! 环节，VAST 拿到最高奖项

SIGGRAPH 的 Real-Time Live! 环节，团队需要在真实观众面前，实时演示技术效果，任何卡顿或翻车都无处遁形，这也是整场大会里关注度最高的环节之一。

*[图片]*

今年共有 8 个项目入选这一环节，既有迪士尼把动画角色 Olaf 实体化为机器人这样的重量级展示，也有 Runway 展示的单图生成实时 AI 角色。

VAST 团队带来的项目《Create Interactive 3D Assets in Seconds!》，现场演示了如何用生成式 AI 在数秒内做出完全带纹理、已绑定骨骼、可直接动画的三维资产，观众当场提交的 prompt 能够即时生成对应的资产，并实时呈现在共享的虚拟世界中。

*[图片]*

现场用户提交的 prompt 生成一个宝箱，正面写着 SIGGRAPH 2026。

这场演示真正验证的能力，远比输入一句话生成一个模型复杂。

系统需要理解用户输入，生成三维结构，完成纹理映射，预测合理骨骼和蒙皮，让角色产生动作，最后将多个结果放进一个可以实时运行的场景中。

*[图片]*

其中任何一个环节出错，最终展示都可能失败。

最终，这个项目拿下了由评审团评选的 Best in Show——Real-Time Live! 环节的最高奖项。

*[图片]*

现场观众参与创作，生成的 3D 道具会随机出现在赛道上，赛车撞到道具即可得分，30 秒内分数更高的一方获胜。

能在这样一个容错率极低的现场环节拿到最高奖，证明了 VAST 在论文里描述的能力，是真的能在没有剪辑的情况下、当着几千人的面跑起来的。

与 World Labs 同台，全球顶级世界模型团队的公开对话

SIGGRAPH 2026 的另一个明显趋势，是 3D 大模型与世界模型之间的边界正在快速消失。

英伟达在大会期间集中展示了神经渲染、仿真和 Cosmos 世界模型等进展，并将 3D 图形学视为物理 AI 理解、生成和模拟世界的重要基础。

World Labs 也将自身定位为一家空间智能公司，希望构建能够感知、生成、推理并与三维世界交互的模型。

VAST 在这场全球技术讨论中的位置也变得更加清晰。

大会开幕前的 7 月 18 日至 19 日，VAST 与李飞飞创立的 World Labs 联合举办了一场名为 Worlds in Action 的黑客松，吸引了 500 多位创作者在两天内搭建下一代 AI 原生 3D 交互体验原型，评审团里还出现了狮门影业、索尼、Meta、NBA 等机构的行业专家身影，奖金池加上 SIGGRAPH 现场展示机会构成了不小的吸引力。

*[图片]*

7 月 20 日，双方又联合发起了一场名为 World Models & GenAI Mixer 的行业社交夜，聚集了约 200 位来自 AI 平台、基础模型公司、视效工作室、虚拟制片团队和创意机构的从业者，VAST、World Labs 与群核科技三方还就 AI 驱动的下一代三维内容生产展开了一场对谈。

对一家中国公司来说，能在 SIGGRAPH 这样的场合与 World Labs 这样由学界顶流创立的公司联合发起活动，本身就是一种同行认可的体现，这比单次产品发布或榜单成绩更能说明其行业位置。

这也让 VAST 的角色发生了变化：它不再只是向外展示一项中国团队做出的 3D 生成技术，而是开始作为全球 AI 3D 基础模型领域的重要参与者，与头部公司共同讨论下一阶段的技术边界和产业方向。

SIGGRAPH Keynote 与 TR35

曹炎培获得双重认可

几乎与 SIGGRAPH 同期，曹炎培还收到了另一份认可：7 月 25 日，《麻省理工科技评论》发布了 35 岁以下科技创新 35 人（TR35）2025 年中国区名单，曹炎培位列其中。

*[图片]*

TR35 创立于 1999 年，旨在寻找全球 35 岁以下具有突出创新能力和发展潜力的青年科技人才。Linus Torvalds、苏姿丰、韩松、鲍哲南、庄小威等在各自领域举足轻重的人物都曾入选。

《麻省理工科技评论》对曹炎培的评价，聚焦于他在三维视觉与生成式 AI 领域的连续技术积累：从三维重建、神经渲染，到 AI 3D 生成，他推动相关技术从生成静态外观，进一步走向结构可用、资产可动和场景可交互，为空间智能与物理 AI 提供底层三维生成能力。

此次入选与曹炎培在 SIGGRAPH 2026 主会场发表 Keynote 几乎同期。个人荣誉与团队成果集中出现，也从侧面体现了 VAST 在 AI 3D 基础模型、可动画资产生成和世界模型方向的技术积累。

五篇论文：把三维资产创作的每一个环节都拆了一遍

更能反映一家公司技术厚度的，往往是论文的数量与质量。SIGGRAPH 的 Technical Papers 以极高的同行评审门槛著称，录用率长期维持在 25% 左右，是计算机科学各大顶会里含金量最高的赛道之一。

能中一篇已属不易，VAST 今年一次性拿下五篇，覆盖了三维资产从几何表征、网格生成、骨骼绑定，到跨拓扑动画迁移、纹理生成的几乎全部核心环节。

这组成果更值得关注的地方，是它们首尾相接，几乎覆盖了一个三维资产从生成出来到真正动起来的完整过程。

《Nexus: Native Mesh Generation with Diffusion》这篇论文是 VAST 旗舰模型 Tripo P1.0 背后的核心支撑。

它抛弃了此前主流的序列化生成思路，把顶点和拓扑的生成解耦开来：顶点被视为八叉树中的稀疏体素，用分层扩散模型由粗到细地全局生成；同时提出时空区间的概念，将任意边缘和非流形表面的拓扑编码为连续的每顶点嵌入。

这篇论文不是停留在实验室里的成果。今年 3 月发布的 Tripo P1.0，正是把 Nexus 的研究成果产品化的结果，它是行业内首个能在 2 秒内直接输出拓扑干净、可直接导入游戏引擎的 AI 3D 生成模型。

*[图片]*

Tripo P1.0 生成效果

另一篇同样走出了论文 - 产品闭环的是《Generative 3D Gaussians with Learned Density Control》，简称 DeG。

它提出了 Density-Sampled Gaussians 方法，把 3D 高斯的密度控制重新建模为一个端到端可学习的概率采样过程，并引入渲染损失贡献梯度，把过去那种离散、启发式的增删点规则，变成了一个可微分的密度优化过程。

这篇论文的成果已经变成了开源项目 TripoSplat，上线后很快登顶 HuggingFace Space 的 Trending 榜单，还拿到了 ComfyUI 官方的首发工作流支持，在 3D 生成社区里引发了不小的讨论。

*[图片]*

TripoSplat 可以将单张 2D 图像转换为高质量、数量可调的 3D 高斯表示。

剩下三篇论文分别指向不同的技术缺口：

- 《PixTex: Consistent 3D Texturing via Pixel-Space Multi-View Diffusion》通过像素空间的多视角扩散机制，解决了 3D 原生纹理在多视角投影下容易出现接缝错位、模糊伪影的老问题，让生成资产的材质能直接达到可导入游戏与影视引擎的清晰度，目前该技术已无缝接入 VAST 全栈生成生态；
- 《AniGen: Unified S³ Fields for Animatable 3D Asset Generation》提出了一套叫 S³ Fields 的统一表示方法，把形状、骨骼、蒙皮这三件过去通常串行处理的事情放进同一个共享空间里联合生成，在拓扑正确性、蒙皮分布等指标上都对当前的强基线方法形成了明显领先，且能泛化到动物、人物、卡通角色乃至机械臂等差异极大的类别；
- 《TopoCap: Learning Topology-Agnostic Motion Priors for Monocular Video-to-Animation》则瞄准了视频到动画这条链路，构建了第一个拓扑无感的运动提取框架，能把单目视频里的运动直接、零样本地迁移给任意未知骨骼结构的三维角色，团队为此还配套发布了一个包含超 5000 种骨骼拓扑、200 万帧动画的大规模数据集 MOBJAVERSE。

把这五篇论文放在一起，能看出一条清晰的逻辑线：VAST 想解决的从来不只是生成一个好看的三维模型，而是三维资产从几何、纹理到骨骼、动画的全流程可用性问题。这也恰好呼应了曹炎培在 Keynote 里提出的那个问题 —— 生成的东西，到底能不能被真正使用。

结语

VAST 是一家全球领先的通用人工智能公司，致力于构建通用 AI 3D 基础模型与世界模型。

短短三年，这家公司已经围绕 AI 3D 建立起一套相对完整的技术体系，全球用户已经超过 2000 万。

旗舰模型 Tripo P1.0 可以在 2 秒内直接生成拓扑干净、能够进入游戏引擎和实时工作流的低面数网格资产；Tripo H3.1 面向高精度资产生成，进一步强化几何密度、表面细节和结构准确性；Project Eden 则将探索范围延伸至世界模型，尝试跳出以连续像素或视频帧为中心的生成范式，将底层世界状态与视觉渲染解耦，让生成的世界能够持续运行、记录交互，并在不同观察视角下保持一致。

*[图片]*

Tripo H3.1：高保真 3D 生成

回过头看 VAST 此次在 SIGGRAPH 2026 的密集亮相，可以发现他们已经形成了一条相当清晰的技术主线。

Nexus 论文支撑起旗舰模型 Tripo P1.0，DeG 论文催生了开源项目 TripoSplat，PixTex、AniGen、TopoCap 分别补齐了纹理、骨骼绑定与动画迁移这几个此前三维生成领域相对薄弱的环节。学术研究、产品化、开源社区三者在这家公司身上形成了一个可以互相验证的闭环。

五十年前，Newell 茶壶测试的是计算机有没有能力显示三维世界。

今天，新的茶壶测试已经摆在所有 AI 3D 公司面前：生成之后，它能否真正进入世界？

从三年前宋亚宸第一次登上 SIGGRAPH 主会场，到今年曹炎培带着「茶壶测试」的新提问再度登台，再加上论文、奖项、开源项目和行业合作的全面开花，这或许可以被看作一个信号：在计算机图形学和三维生成这条技术门槛极高的赛道上，中国公司已经开始与英伟达等国际头部机构共同进入大会核心议程，并与 World Labs 等前沿团队展开直接对话，参与提出下一阶段需要回答的问题。

最后附上一些论文信息，供大家参考：

论文 1：Nexus: Native Mesh Generation with Diffusion（旗舰模型 P1.0 背后的论文）

论文链接：[https://dl.acm.org/doi/10.1145/3811344](https://dl.acm.org/doi/10.1145/3811344)

论文 2：Generative 3D Gaussians with Learned Density Control / DeG（TripoSplat 开源项目背后的论文）

论文链接：[https://arxiv.org/abs/2605.16355](https://arxiv.org/abs/2605.16355)

开源项目：[https://github.com/VAST-AI-Research/TripoSplat](https://github.com/VAST-AI-Research/TripoSplat)

HuggingFace 在线试玩：[https://huggingface.co/spaces/VAST-AI/TripoSplat](https://huggingface.co/spaces/VAST-AI/TripoSplat)

ModelScope 在线试玩：[https://modelscope.cn/studios/VAST-AI-Research/TripoSplat-Demo](https://modelscope.cn/studios/VAST-AI-Research/TripoSplat-Demo)

ComfyUI 工作流接入：[https://docs.comfy.org/tutorials/3d/triposplat](https://docs.comfy.org/tutorials/3d/triposplat)

论文 3：PixTex: Consistent 3D Texturing via Pixel-Space Multi-View Diffusion

论文 4：AniGen: Unified S³ Fields for Animatable 3D Asset Generation

论文链接：[https://arxiv.org/abs/2604.08746](https://arxiv.org/abs/2604.08746)

代码：[https://github.com/VAST-AI-Research/AniGen](https://github.com/VAST-AI-Research/AniGen)

HuggingFace 在线试玩：[https://huggingface.co/spaces/VAST-AI/AniGen](https://huggingface.co/spaces/VAST-AI/AniGen)

论文 5：TopoCap: Learning Topology-Agnostic Motion Priors for Monocular Video-to-Animation

论文链接：[https://arxiv.org/abs/2606.12153](https://arxiv.org/abs/2606.12153)

© THE END

转载请联系本公众号获得授权

投稿或寻求报道：liyazhou@jiqizhixin.com

[跳转微信打开](https://wechat2rss.xlab.app/link-proxy/?k=224512e6&r=1&u=https%3A%2F%2Fmp.weixin.qq.com%2Fs%3F__biz%3DMzA3MzI4MjgzMw%3D%3D%26mid%3D2651047451%26idx%3D1%26sn%3D274e2733c0b51bffa02aeed28256404c)
