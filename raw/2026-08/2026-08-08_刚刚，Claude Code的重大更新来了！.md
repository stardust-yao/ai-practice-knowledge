---
title: 刚刚，Claude Code的重大更新来了！
date: 2026-08-08
source: https://mp.weixin.qq.com/s?__biz=MzIyNjM2MzQyNg==&amp;mid=2247725083&amp;idx=1&amp;sn=72e37b4dd5ce3106a989f6707e7debb6
account: Datawhale
fetched_at: 2026-08-11 17:11:45 CST
article_id: 72e37b4dd5ce3106a989f6707e7debb6
---

原创 Datawhale 2026-08-08 22:56 浙江

  
  
*[图片]*

  
AI会话可以互相聊天了

  
Datawhale干货

**更新：Claude Code**

今天，Anthropic发布了一个重大更新，18个小时就被近500w人看过。

给Claude Code加了个新东西，不同的Claude Code会话，现在可以互相聊天了。

*[图片]*

之后不用再在窗口A里复制一段总结，粘贴到窗口B。这还是双向的：你同样可以向另一个会话提问，并在当前会话中收到回复。

而且当它刚做出的改动影响到另一个会话的工作内容时，Claude 还能主动向其他会话发送消息。

之后我们就能实现：无聊的时候开俩cc让他们说个相声了。

## 一、Claude Code重大更新：AI会话可以互相发消息了

以前，多个Claude Code会话一起跑的时候，比如分别开着前端、后端两个终端，或者拆了几个worktree并行开发，一个会话发现了什么、改了什么，得靠人工搬运。

Claude Code把会话之间打通了。跟其中一个会话说一句“把刚才接口改动的事告诉另一个终端里跑的会话”，Claude自己会去找目标、写内容、发过去。对方在下一轮空闲时接着往下改，不用人再回来同步。

*[图片]*

这背后是两个新工具，ListAgents负责找到能联系上的会话，SendMessage负责把消息发过去。

但这个传的是有限的，是Claude自己写的一段文字，不是发送方完整的对话历史，也不带文件；权限也管得很严，改不了接受方的配置，也批不了对方的权限申请。

如果想搬整个上下文，官方给的建议是还是用resume（恢复会话），不是发消息。

**二、Claude Code之前一直有team模式**

这是就有一个问题：Claude Code不是一直有team模式吗。

*[图片]*

确实。Claude Code能做“多个会话协同”不是第一次了。subagent，一个会话内部派生的子任务；Agent Teams，今年二三月上线的实验性功能，需要手动改config开启。这两种情况下，都能做到一组会话一起干活。

只是参与协作的会话，都是被同一个主会话派生出来、管着的。

这次不太一样的地方在于，它连的是用户自己在不同终端里分别敲命令启动的、彼此原本互不知道对方存在的会话，甚至可以是不同机器上的会话。没有谁派生谁，也没有谁管着谁，就是两个平级的、各干各活的会话，需要的时候相互搭一句话。

以前多会话协作基本靠一个中心节点分发任务，现在两个各自为战的会话也能直接说上话了。

**三、Codex一个月前也发布了Multi-agent v2**

一个月前，Codex CLI也刚刚转正了Multi-agent v2。

*[图片：Image]*

```
图源:[https://x](https://x).com/CheZS6/article/2076957388314431584
```

这套机制里确实有个send_message工具，也支持agent对agent直接发消息、不用绕回调度者的peer-to-peer模式，听着跟Claude Code这次的功能有点像。但拆开架构看，两者处理的场景不太一样。

Multi-agent v2用的是路径寻址。一个主会话（/root），用spawn_agent生出一批子agent，挂在路径树上，比如/root/researcher、/root/builder，兄弟节点之间可以直接send_message，不用绕回/root。

但这棵树从头到尾，还是由同一个orchestrator会话生出来、管着的。本质上跟Claude Code的subagent、Agent Teams是同一类机制。

真正对应“两个用户自己开的、互不隶属的终端会话”这个场景的，其实是Codex CLI原生的多会话用法。两个终端里各敲一遍codex命令，就是两个完全独立的进程。几份Codex CLI的官方使用指南里都提到，这种情况下两个会话互相不知道对方的存在，各自维护自己的上下文和工作目录，没有内置的通信通道。

想让它们互通，得靠tmux，或者把Codex当MCP server外接编排，用codex-reply续接线程，再或者手动复制粘贴，跟Claude Code更新之前的做法差不多。

**写在最后**

总结一下以前不论是cc还是codex，其实都是交出去一件事，内部自己拆开分工，几个子agent一起干活，用同一个任务派生出来的。

这次不一样。这两个会话根本不是因为同一个任务拆分出来的，但它们可以后台自己对进度了，是一个很实用的功能，聊天的内容我们都能直接看到。

*[图片：图片]*
**一起“点****赞”****三连**↓

[跳转微信打开](https://wechat2rss.xlab.app/link-proxy/?k=0a027a8f&r=1&u=https%3A%2F%2Fmp.weixin.qq.com%2Fs%3F__biz%3DMzIyNjM2MzQyNg%3D%3D%26mid%3D2247725083%26idx%3D1%26sn%3D72e37b4dd5ce3106a989f6707e7debb6)
