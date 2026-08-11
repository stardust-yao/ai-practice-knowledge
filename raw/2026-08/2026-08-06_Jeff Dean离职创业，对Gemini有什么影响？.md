---
title: Jeff Dean离职创业，对Gemini有什么影响？
date: 2026-08-06
source: https://mp.weixin.qq.com/s?__biz=MzA3MzI4MjgzMw==&amp;mid=2651048783&amp;idx=2&amp;sn=77f120b8174e08bd902a968a3d6040d4
account: 腾讯技术工程
fetched_at: 2026-08-11 17:11:44 CST
article_id: 77f120b8174e08bd902a968a3d6040d4
---

原创 机器之心 2026-08-06 12:05 北京

  
  
*[图片]*

  
短期影响可能有限，但中长期影响会有点大。

  
*[图片]*

编辑｜Panda、张倩

[Jeff Dean 离职创业去了](https://mp.weixin.qq.com/s?__biz=MzA3MzI4MjgzMw==&mid=2651048705&idx=1&sn=0efead2307b59aba90456862c1c37f1f&scene=21#wechat_redirect)，Pichai 的全员信感谢了 Jeff Dean「了不起的 27 年」，说他要和 Sanjay Ghemawat 一起去创业。他在 𝕏 上发的也是这两个名字。

*[图片]*

但 Discovery Loop 官网当天上线，列出的创始人是四位。被谷歌那份公告略过的两位，一位是 Google Brain 联合创始人 Quoc Le，另一位是 Oriol Vinyals —— 他 𝕏 简介上写着的头衔是「Gemini co-lead」。

*[图片]*

Dean 自己领英上的写法是「Gemini overall co-technical lead」。

*[图片]*

同一天，谷歌宣布 Koray Kavukcuoglu 升任 Google DeepMind 高级副总裁，直接向 Pichai 汇报，负责 Gemini 模型研发。据 CNBC 报道，Gemini 4 归他管。

也就是在宣布谁来造 Gemini 4 的那一天，Gemini 的两位技术联合负责人一起走了。

整体来说，市场并不看好：Alphabet 当日股价下跌一度超过 5%。

*[图片]*

先把两件事拆开

「Jeff Dean 离职」和「Gemini 的技术负责人集体离开」被打包进了同一条新闻，但对 Gemini 的影响不是一回事。

Dean 在 2023 年 Google Brain 与 DeepMind 合并后的实际角色，是 Google DeepMind 与 Google Research 的首席科学家。这个位置更接近技术总设计师和跨层协调者，而不是具体研究方向。

他的不可替代性来自另一个方向：从 MapReduce、BigTable、Spanner 到 DistBelief、TensorFlow、Pathways，再到发起 TPU 项目，谷歌 AI 的物理地基基本是他和 Ghemawat 这批人一层层砌上去的。他离开影响的是地基层，不是模型的日常研发。

Vinyals 是另一回事。他是 2014 年 seq2seq 论文的共同作者之一，与 Ilya Sutskever、Quoc Le 合作完成；做过 Pointer Networks 和知识蒸馏的早期工作；领导过 AlphaStar；后来出任 DeepMind 研究副总裁和 Gemini 的技术联合负责人。他的位置更靠近模型本身。

*[图片]*

区分这两者很重要，因为把 Dean 的离职当成「Gemini 失去了主帅」，既高估了他在模型层的日常介入，也低估了另外三个人一起走造成的空缺。

七周，三位 co-lead 都走了

真正该写进时间线的是这一条：Gemini 的三位技术联合负责人（co-technical lead），在七周内全部离开谷歌。

6 月 17 日，Noam Shazeer 宣布加入 OpenAI，出任 AI 架构研究负责人。

*[图片]*

Shazeer 是 2017 年 Transformer 论文的八位共同作者之一，也是稀疏专家混合（sparse MoE）和多查询注意力（Multi-Query Attention）的提出者。2024 年 8 月，谷歌以外界报道约 27 亿美元的代价，通过与 Character.AI 的交易把他请了回来。不到两年，他走了。奥特曼当时在 𝕏 上说，Shazeer 是他从 OpenAI 创立之初就最想合作的人之一。更多详情请参阅机器之心报道《[用了 10 年，奥特曼终于等到了他想要的人](https://mp.weixin.qq.com/s?__biz=MzA3MzI4MjgzMw==&mid=2651039911&idx=2&sn=2b99ae81a2110fc37afeed89d4a367b3&scene=21#wechat_redirect)》。

8 月 5 日，Dean 和 Vinyals 一起离开。

一位高管离职是人事新闻。同一岗位上的三个人在七周内全部离开，则是结构性信号。

短期：影响可能被高估了

先给一个反直觉的判断：Gemini 眼下最明显的问题不是这次离职造成的，而且这三个人还在的时候，问题也没解决。

看时间线。5 月 19 日 I/O 2026 上，Pichai 当着开发者的面承诺 Gemini 3.5 Pro「下个月」交付。6 月没有。7 月 21 日，谷歌一口气发布了 Gemini 3.6 Flash、3.5 Flash-Lite 和 3.5 Flash Cyber 三个模型，唯独没有 3.5 Pro，官方说法是仍在与合作伙伴测试。同一篇公告的末尾，谷歌顺带提了一句：Gemini 4 的预训练已经启动。

*[图片]*

[https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-6-flash-3-5-flash-lite-3-5-flash-cyber/](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-6-flash-3-5-flash-lite-3-5-flash-cyber/)

据彭博社报道，推迟的原因是模型没有达到谷歌自己的内部质量标准。

这些事全部发生在 Dean 和 Vinyals 还在岗的时候。

反过来看接手的局面也没那么悲观。Gemini 4 的预训练已经开始，训练配方基本锁定，执行层的绝大多数研究员和工程师没有走。Koray 在 DeepMind 待了 13 年，从早期就参与，组建了公司的深度学习团队，WaveNet 和 DQN 出自他带的团队，此前的职务是 DeepMind 首席技术官兼谷歌首席 AI 架构师。他不是空降，接任本身没有引起什么质疑。

所以如果你的预期是「Gemini 4 会因此难产」，大概率不会。

中长期：真正的三层损失

但把时间轴拉到 Gemini 5 和 2027 年，账要重新算。

第一层是架构判断力。 Shazeer、Vinyals、Le 三个人的共同点是，他们的代表作不是把某个模型调好，而是提出了后来所有人都在用的结构，包括 Transformer、稀疏 MoE、MQA、seq2seq、神经架构搜索。这类工作出现频率极低，一旦出现就重置整条赛道，而且几乎无法用 KPI 衡量。一个组织可以在几个月内补齐执行层的人手，却很难补齐这种判断力。它依赖的是同一批人在同一类问题上积累十几年的直觉，不存在可以交接的文档。

第二层是纵向链路。 谷歌相对 OpenAI 和 Anthropic 最硬的优势，是从 TPU 到编译器到 Pathways 再到模型的完整自研栈。Hassabis 在全员信里把这一点表述为「唯一一家拥有完整技术栈的公司」。这条链路的价值不在每一层单独多强，而在跨层的协同设计。Dean 和 Ghemawat 恰好是全公司少数几个能同时在这几层上做判断的人。

*[图片]*

[https://blog.google/company-news/inside-google/message-ceo/next-chapter-ai-momentum/](https://blog.google/company-news/inside-google/message-ceo/next-chapter-ai-momentum/)

值得注意的是，Discovery Loop 官网对四位创始人的描述，用了几乎一模一样的措辞：横跨芯片、硬件基础设施、软件基础设施、ML 模型和产品的全栈深度。一家有十几万员工的公司和一家四个人或许还没找到办公室的创业公司，在同一天声称了同一件事。考虑到这四个人的履历从搜索、MapReduce 一路排到 Spanner、TensorFlow、TPU、AlphaFold 和 Gemini，这个说法算不上离谱。

第三层是组织引力。Vinyals 在告别帖里写，13 年前他因为和 Dean 的一次简短邮件往来加入谷歌；而现在，把他招进来的那个人，正在邀请他挑战下一步。Dean 招进来的人，跟着 Dean 走了。这类离开会打开一扇门：留下来的资深研究员会重新考虑「继续留在这里」的价值。谷歌今年已经在这道题上丢了一次分。

*[图片]*

研究与交付，被拆开了

从组织结构看，这次调整做的是一件事：把研究和交付分开。

Hassabis 出任 Google DeepMind 主席兼 Alphabet 首席科学家，交出日常运营，转向 AGI 长线战略和 Isomorphic 的药物研发，办公地点在伦敦新的 Platform 37。他在信里说，AI 最重要的应用应当是改善人类健康，现在是时候让 AI 证明自己的价值了。Koray 则以高级副总裁身份接管日常，直接向 Pichai 汇报，管 Gemini 模型研发、前沿 AI 研究，以及 Gemini 应用和开发者团队。

注意职级的变化。Hassabis 是主席，Koray 是 SVP。这不只是称谓问题。它意味着 Google DeepMind 从一个拥有独立 CEO 的半自治实体，变成了汇报线更短、离产品更近的部门。

对 Gemini 来说，这未必是坏消息。过去一年谷歌的困境不像是想法不够，更像是交付节奏跟不上。Pichai 在最近一次财报电话会上提到，希望未来把 Gemini 的发布节奏做到「几乎每月一次」，并以 Gemini 4 为基线。一个更靠近产品、汇报链更短的负责人，理论上正是为解决这个问题设的。

风险在另一头。当最有分量的研究声音一个去做长线战略、四个去了创业公司，剩下的组织会不会在优化「按时发下一个版本」的过程中，让那些没有排期、也说不清何时有回报的方向持续让位？毕竟，谷歌历史上最值钱的几项工作 （Transformer、TPU、MoE），没有一项是排期排出来的。

一个更值得追问的问题

Discovery Loop 要做的事，和谷歌当下最需要的事高度重合。

按其官网的说法，公司认为科学发现的瓶颈不在方法本身，而在执行：提出假设、跑实验、读结果，再来一轮，每次只能走一个循环。

*[图片]*

它想做的是把这个循环自动化，并让数千个循环并行。第一步是自动化机器学习研究本身，然后把这套能力指向自己的技术栈，成为自己的第一个客户。Quoc Le 对《连线》说，他们可能会发现一种不同于 Transformer 的架构。

这正是当下所有前沿实验室都在下的注：让 AI 来做 AI 研究。谷歌自己也在做。

那么，四个最了解谷歌内部能做什么、不能做什么的人，判断这件事在谷歌内部做不成或者不够快，这个判断本身就是一条关于谷歌的信息。Dean 对《纽约时报》的说法是，在上市公司之外，团队有空间做一些不完全符合公司纯粹财务利益的决定。这句话的另一面是：在上市公司之内没有这个空间。

更耐人寻味的是谷歌的应对方式。Alphabet 成为 Discovery Loop 的创始投资方之一，谷歌云是它的算力供应商，第一年的算力由谷歌提供，双方还将共建机器学习系统的联合研究框架。种子轮由 Radical Ventures 和 Khosla Ventures 领投，Lightspeed、Kleiner Perkins、Doerr Capital 参投，金额与估值均未披露，Radical 的 Jordan Jacobs 进入董事会。

这是一次理性的对冲。如果自动化研究这条路走通了，谷歌在里面有份额、有优先接触权；如果走不通，谷歌损失的只是一笔投资和四个本来就要走的人。但对冲成立的前提，是承认这条路在谷歌内部跑不出来。

顺带一提，Vinyals 自己点出了这个方案最大的漏洞：他们接下来最需要关注的，是模型如何提出值得一试的新想法，而这恰恰不是当前模型的强项。这也正是自动化研究闭环里最难自动化的那一环。

那么，对 Gemini 到底有什么影响？

回到标题这个问题，分三个时间尺度回答。

短期，对 Gemini 4 的直接影响有限。模型已在预训练，执行团队完整，接任者是内部资深人士。3.5 Pro 的反复推迟与这次离职无关 —— 它发生得更早，也更能说明问题所在。

中期，该盯的不是下一个模型什么时候发，而是谷歌能否在没有这几个人的情况下，继续做出让别人跟着抄的架构决策。Gemini 3.5 Pro 三次延期、最终由 Flash 系列填空，已经暴露出前沿模型这条线的压力。接下来一两代模型是继续在既有配方上加规模，还是拿得出新的结构，这是可观察、可验证的。

长期，真正的变量是谷歌那种「同一批人从芯片一直做到模型」的组织能力还剩多少。这既不是招聘能解决的，也不是一次架构调整能解决的。

有一个判断可以先给出来：这次人事变动本身不足以决定 Gemini 的成败，但它把谷歌已经存在的问题，从内部报告推到了公开层面。Pichai 的信、Hassabis 的信、四个人的离开和 5% 的跌幅，讲的其实是同一件事：谷歌手握 AI 领域最完整的牌面，从 TPU 到云到 9.5 亿月活的 Gemini 应用，但交付速度一直是它的短板，而现在负责补这块短板的人换了。

Gemini 4 会给出答案。只是这一次，交卷的人不再是当初设计考题的那批人。

参考链接

[https://blog.google/company-news/inside-google/message-ceo/next-chapter-ai-momentum/](https://blog.google/company-news/inside-google/message-ceo/next-chapter-ai-momentum/)

[https://www.discoveryloop.com/](https://www.discoveryloop.com/)

[https://www.wired.com/story/jeff-dean-google-discovery-loop-startup/](https://www.wired.com/story/jeff-dean-google-discovery-loop-startup/)

[https://www.nytimes.com/2026/08/05/technology/google-researchers-ai-startup.html](https://www.nytimes.com/2026/08/05/technology/google-researchers-ai-startup.html)

[https://techcrunch.com/2026/08/05/jeff-dean-and-other-top-ai-researchers-are-leaving-google-to-launch-their-own-startup/](https://techcrunch.com/2026/08/05/jeff-dean-and-other-top-ai-researchers-are-leaving-google-to-launch-their-own-startup/)

[https://fortune.com/2026/08/05/demis-hassabis-steps-down-google-deepmind-ai-shakeup/](https://fortune.com/2026/08/05/demis-hassabis-steps-down-google-deepmind-ai-shakeup/)

*[图片：图片]*

© THE END

转载请联系本公众号获得授权

投稿或寻求报道：liyazhou@jiqizhixin.com

[跳转微信打开](https://wechat2rss.xlab.app/link-proxy/?k=a4fd41f0&r=1&u=https%3A%2F%2Fmp.weixin.qq.com%2Fs%3F__biz%3DMzA3MzI4MjgzMw%3D%3D%26mid%3D2651048783%26idx%3D2%26sn%3D77f120b8174e08bd902a968a3d6040d4)
