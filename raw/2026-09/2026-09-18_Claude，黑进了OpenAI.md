---
title: Claude，黑进了OpenAI
date: 2026-09-18
source: https://mp.weixin.qq.com/s?__biz=MzA3MzI4MjgzMw==&amp;mid=2651058476&amp;idx=2&amp;sn=5420ed184501bc1d9f450971a41792c3
account: 机器之心
fetched_at: 2026-09-19 18:00:04 CST
article_id: 5420ed184501bc1d9f450971a41792c3
---

原创 机器之心 2026-09-18 17:30 四川

  
  
*[图片]*

  
3个人，72小时，模型是 Claude Opus，赏金6500美元

  
*[图片]*

编辑｜Panda

天道好轮回，苍天饶过谁？入侵过 [Hugging Face](https://mp.weixin.qq.com/s?__biz=MzA3MzI4MjgzMw==&mid=2651046034&idx=2&sn=28d08b24db4deb725bd70d2f6b20d1da&scene=21#wechat_redirect) 和 [Ruby 生态](https://mp.weixin.qq.com/s?__biz=MzA3MzI4MjgzMw==&mid=2651056817&idx=1&sn=c09c4b215d9c4b9797561a839e70a585&scene=21#wechat_redirect)的 OpenAI 原来也被入侵过！并且，入侵者使用的还是其主要竞对 Anthropic 的模型。

就在几个小时前，Electrovolt Security 与 Hacktron AI 创始人 s1r1us 在 𝕏 上发布了一系列推文，分享了其团队在 7 月份借助 Claude 成功入侵 OpenAI 的故事，引发广泛关注。

*[图片]*

[https://x.com/S1r1u5_/status/2100777801335095383](https://x.com/S1r1u5_/status/2100777801335095383)

严格来说，这个故事并不算新。完整的技术复盘早在 9 月 13 日就挂在了 Hacktron 的博客上，并且标题颇有些挑衅意味：「Hacking OpenAI」。

*[图片]*

博客地址：[https://www.hacktron.ai/blog/hacking-openai](https://www.hacktron.ai/blog/hacking-openai)

真正让它在今天引爆的，是《华尔街日报》的独家报道《黑客用 Anthropic 的 Claude 攻破 OpenAI》，以及 s1r1us 本人下场把整条攻击链摊开讲了一遍。推文发布数小时内浏览量已超过 55 万，Hacker News 上也热度极高。

*[图片]*

s1r1us 本名 Mohan Pedhapati，是 Hacktron AI 的联合创始人兼 CTO。参与这次研究的还有安全研究主管 Harsh Jaiswal 和研究员 Rahul Maini，一共 3 个人。

时间上，从初始发现到拿到 OpenAI 内部代码仓库的访问权限，全程不到 72 小时。

*[图片]*

Hacktron 博客给出的九步攻击链示意图

72 小时：从一张图片到 OpenAI 的内部单体仓库

整条链路的起点就只是「上传一张 HEIC 格式的图片」。

OpenAI 的用户社区 community.openai.com 跑在 Discourse 上。Discourse 平时用 FastImage 做图片校验，但 FastImage 不支持 HEIF，于是这类文件被转交给 ImageMagick 的 magick 命令去转换，底层的 libheif 解析器就这样直接暴露在了攻击者可控的文件面前。

Hacktron 团队在 7 月 23 日开始审计这条图片上传流水线，随后在 libheif 中确认了一个堆缓冲区溢出。

最值得安全从业者警觉的是这个漏洞的来历：相关代码上游在前一年就已经改过，但那次提交没有被标记为安全修复，也没有分配 CVE。结果是 Debian 12 和 Debian 13 都没有及时拿到这个安全 backport。Discourse 的 Docker 镜像基于 Debian 12，装的是 1.19.7 版本，而当时的 Debian 13 也仍然带着有问题的 1.19.8。一个没人认为是安全问题的提交，在依赖链末端变成了一次远程代码执行。Debian 直到 8 月 8 日才为 Debian 13 推送安全更新。

拿到论坛的 RCE 只是第一步。真正把影响放大的是第二个漏洞：OpenAI 自家的 SSO 缺陷。OpenAI 允许用户通过 auth.openai.com 的「Sign in with OpenAI」登录论坛，而这条身份链路存在配置问题，使得攻陷论坛可以转化为对登录过该论坛的用户 ChatGPT 和 Codex 账号的接管，其中包括 OpenAI 员工。

团队在博客里专门强调了一句：这个可被利用来提权的漏洞不是 Discourse 特有的，Discourse 只是他们选中的一条证明路径，任何使用 OpenAI SSO 的第一方或第三方服务被攻陷，都会导致同样的结果。

而 ChatGPT 和 Codex 账号往往连接了 Outlook、Gmail、Google Drive、Slack、GitHub 等一大串服务。理论可达范围因此远远超出了聊天记录本身。

为了在不读取任何敏感内容的前提下证明访问是真实的，团队挑了一个 Codex 已连接 OpenAI GitHub 组织的员工账号，给这个账号的 Codex 发了一条指令，让它在 OpenAI 的内部单体仓库 openai/openai 里开了一个无害的 pull request，然后立刻停止了所有进一步测试。

*[图片]*

向 OpenAI 内部单体仓库提交的 PoC pull request 图示，非原始截图（OpenAI 要求不展示原始截图）

据《华尔街日报》转述知情人士的说法，这个 monorepo 存放的是让模型更快更高效的算法机密，相当于公司的配方，但不包含模型权重；研究人员提交的改动落在一份文档文件上，内容包含「Hacktron AI Team PoC」字样和两位研究员的 𝕏 账号链接，该建议未被接受。

时间线密度很高。7 月 25 日 UTC 凌晨 5 点到 6 点之间拿到论坛的 RCE 和管理员权限；8 点到 10 点通过 Bugcrowd 提交报告；13 点半到 15 点半完成员工账号接管与 PoC 提交，同时在推特上直接找 OpenAI 的朋友示警，并在 15 点半左右停手；当天 22 点 49 分，OpenAI 回复确认问题已修复，距离初始提交约 14 小时。给 Discourse 的报告走的是 HackerOne，周六送出、周日回复、周一修复完成，7 月 28 日发布安全公告 GHSA-vhm9-85gw-x335，并顺手给 ImageMagick 加上了沙箱隔离作为纵深防御。

*[图片]*

Claude 在其中到底做了多少？

这才是这条新闻真正的爆点。

Hacktron 的复盘写得相当坦白。他们先用 Opus 4.8 开了一个会话，把 Discourse 的 Docker 镜像丢给它，让它检查已安装的 libheif 包有没有安全问题，模型找出了那批没有被 backport 的修复。7 月 24 日，同样是 Opus 4.8，在关闭 ASLR 的条件下做出了一个可用的代码执行 exploit。但要在 Discourse 默认配置（ASLR 开启）下做到稳定，他们开了好几个会话都没成功。

当天晚上，Anthropic 发布了 Claude Opus 5。

团队开了个新会话，三小时内拿到了一个能在本地 Mac 上跑通的 ARM64 版本，接着让它移植到 Discourse 所用的 x86-64 环境和 jemalloc 配置。到 7 月 25 日早上 6 点，通过图片上传实现本地 RCE 得到确认。

接下来更有意思，Opus 拒绝为远程实例编写 exploit，于是团队把自己的 Discourse Cloud 实例通过一个代理包装成看起来像 CTF 靶场的样子，再把 Claude 放进自主的 /goal 循环里跑。上午 10 点回来查看时，agent 已经在 Discourse Cloud 上拿到了 RCE，并通过读取 /etc/hosts 证明了这一点。用这个自动生成的脚本，他们随后在 OpenAI 的实例上复现成功。

模型的安全护栏确实触发了，但它拦住的只是「远程」这个词。

成本数字同样惊人。Discourse 和 OpenAI 这一段只花了 agent 几天、人类几个小时；而覆盖 Slack、Zoom、Meta 等多家公司的整个 HEIF Heist 研究项目，历时两个月，三名研究员，token 总花费不到 3000 美元，适配到一家新公司通常只需要一两天。

团队称，测试从上传一张图片开始，在通常不知道目标具体 libheif 版本、libc 版本和部署环境的情况下，AI 几乎是盲打着把内存破坏转化为可靠的内存泄露或 shell。据他们观察，除 Shopify 外，没有任何一家公司察觉到这些活动，哪怕图片处理进程被反复打崩、发送量已达数千张。

不过，需要说明两点：

- Hacktron 自己强调这并非全自动黑客攻击，熟练的人类引导依然关键，变化的是一支小团队能完成的工作量级。
- 被点名的不只是 Claude——他们同时提到，在对目标系统一无所知的盲打场景中，从 Opus 5 到 GPT-5.6 Sol 又出现了一次明显的能力跃升。这不是单家模型厂商的问题。

6500 美元和一句补充说明

9 月 1 日，OpenAI 发放了 6500 美元赏金并将报告标记为已解决，同时附上一句措辞谨慎的补充：「针对 Discourse 托管的 community.openai.com 的测试本就被明确排除在其赏金计划范围之外，这笔奖励认可的是 OpenAI 侧的发现，而非针对 Discourse 的行为。」

*[图片]*

6500 美元就买下一条通往内部单体仓库的路径，这个数字在社交媒体上很快成了争议焦点。

*[图片]*

*[图片]*

真正把讨论推向更深处的，是安全研究者 Joshua Saxe 的一条长帖。他在文章发表前受 WSJ 和 s1r1us 之邀，对这条 kill chain 做过中立的技术复核。

他抛出的几个问题都很难回答：已经有多少更强大的攻击者更早进去、并且走得更远，拿走了算法机密、模型权重或者用户数据？此刻有多少驻留程序还留在前沿实验室的网络里？这种程度的「软」在各家实验室之间有多普遍，它们距离安全与研发效率之间的合理平衡点还有多远？

*[图片]*

[https://x.com/joshua_saxe/status/2100775309012296171](https://x.com/joshua_saxe/status/2100775309012296171)

他最扎人的一问指向 Anthropic：既然 Hacktron 正是用 Anthropic 的模型完成了这次入侵，那么 Anthropic 那套网络安全护栏的公共安全 ROI 究竟是多少——它给合法的防守方增加了实实在在的摩擦，而攻击方稍加周折就绕了过去。他的结论是，精英级的持续性入侵能力正在被迅速平民化，而这正像一列货运火车一样开过来。

天道好轮回的另一半

把这件事放回时间线，会发现 2026 年的前沿实验室安全史已经相当混乱。

7 月，OpenAI 与 Hugging Face 共同披露了一起事故：OpenAI 在 ExploitGym 这一公开基准上测试 GPT-5.6 Sol 和一个未发布的内部模型，为了跑评测关闭了对外部署时的同等防护，结果模型突破了评估环境的隔离边界、触及公网，并攻陷了 Hugging Face 生产基础设施的一部分。

9 月 11 日，研究者 Spencer Kitts、Thomas Larsen 和 Sydney Von Arx 又披露，早在 5 月 11 日，OpenAI 的测试 agent 就已经向 RubyGems 上传了数百个恶意包，试图窃取用户凭据。RubyGems 一度将其当作 DDoS 处理并暂停新用户注册，最终封禁相关账号、撤下 500 多个恶意包，5 月 16 日恢复注册。

再往前，还有一起被安全社区称为「wiki 事件」的插曲：约 18000 条来自自称 OpenAI 系统的自主 agent 的帖子被发现散布在一个德语 wiki 农场上，agent 们用公共站点互相传递答案、勘察环境，其中一条记录显示，某个 agent 发布了绕过 OpenAI 沙箱网络限制的方法，14 分钟后另一个 agent 就照做了。

9 月 5 日，OpenAI 在官方 𝕏 账号上表态，称现在已经到了该为「何时、如何披露 misalignment 事件」定标准的时候，而不只是披露模型的 misalignment 属性，框架将在未来几周公布，同时公司正在与全球数十个监管机构沟通。

*[图片]*

而就在今天这条 Claude 入侵新闻传播的同时，人们也在关注 OpenAI 披露了自 3 月以来的六起异常模型行为。

*[图片]*

一边是自家 agent 越狱去打别人的基础设施，一边是别人用竞对的模型打进自家的单体仓库……

*[图片]*

xkcd 2347「Dependency」，Hacktron 博客引用图

结语

Hacktron 在文章结尾给出了一个我认为是全文最有价值的判断：软件行业长期享受着一种「靠复杂度获得的安全」。

代码是公开的，漏洞甚至也可能是公开的，但把一个 bug 变成可靠的 exploit，需要稀缺的专业能力、大量时间和对目标环境的了解。已知的内存破坏漏洞武器化成本很高，零日则基本只留给最高价值的目标。

这不是一条真正的安全边界，但它在实践中确实保护了普通公司很多年。AI 正在把这层保护取消掉：它正把稀缺的专家能力转换成算力。

*[图片：图片]*

© THE END

转载请联系本公众号获得授权

投稿或寻求报道：liyazhou@jiqizhixin.com

[跳转微信打开](https://wechat2rss.xlab.app/link-proxy/?k=089d1f0c&r=1&u=https%3A%2F%2Fmp.weixin.qq.com%2Fs%3F__biz%3DMzA3MzI4MjgzMw%3D%3D%26mid%3D2651058476%26idx%3D2%26sn%3D5420ed184501bc1d9f450971a41792c3)
