---
title: Warp CEO的Claude实战教程，两个Skill让Agent进化！
date: 2026-08-31
source: https://mp.weixin.qq.com/s?__biz=MzIyNjM2MzQyNg==&amp;mid=2247725873&amp;idx=1&amp;sn=0cdc741a73325e737e32d0dca203375a
account: Datawhale
fetched_at: 2026-09-01 18:00:04 CST
article_id: 0cdc741a73325e737e32d0dca203375a
---

原创 Datawhale 2026-08-31 22:30 浙江

  
  
*[图片]*

  
  
Datawhale干货

**作者：Warp CEO**

Warp 公开了自己搭自我改进 Agent 的实战方法：两个 Skill 文件，中间夹一条人类反馈，就能让 Agent 从每次错误里沉淀知识、越用越聪明。这家把 AI 终端做到 80 万月活、近 7500 万融资的公司，自己的开发团队就靠这套框架，把一个噪声缠身的 code review Agent 救了回来。

*[图片：Image]*

```
https://claude.com/blog/how-warp-builds-self-improving-agents-on-claude
```

这个 Agent 负责 code review，第一轮能做到 80% 正确。听起来不错，但剩下 20% 是噪声：不相关的评论、误判代码库惯例、低质量的修改建议。Warp 的工程师每天要在一堆无用评论里挑有用的，比没有 Agent 还累。

团队试过手动改 prompt、改进 AGENTS.md，都不解决问题。Warp CEO Zach Lloyd 最近在 Claude 官方博客上分享了他们最终的解法：两个 Skill 文件，搭出一个会自我改进的 Agent。

这套框架不复杂，但戳中了一个大多数团队都会遇到的问题：Agent 越用越笨，根子不在模型不够强，而在反馈在每次对话结束时消失了。

*[图片：Image]*

## 一、问题根源：80% 正确的 Agent，比完全错误更折磨人

先讲清楚 Warp 踩的坑。

他们的 code review agent 有一个典型毛病：第一轮输出能做到 80% 正确，但剩下 20% 的噪声会让工程师崩溃。比如它建议重命名一个变量，但没注意到这个代码库的惯例是这类全局变量有固定命名方式。这种评论不仅没用，还会浪费审查者的时间去判断"这条该不该理"。

团队的第一反应很直觉：手动改 prompt。看到哪类评论翻车，就去改对应的 prompt 片段。这确实有效，但每个新问题都要人盯，根本规模化不了。

后来又试了改进 AGENTS.md，把更多上下文写进去。有帮助，但远不是完整方案。

两个方案都触及了问题的表面，没碰到根。Warp 后来意识到：给 Agent 的反馈，通常在对话结束时消失。无论你在对话里纠正了它多少次，下一轮新对话开始，Agent 还是那个"没记住教训"的 Agent。

这就是 Agent 越用越笨的真正原因。不是模型能力问题，是反馈没有沉淀。

## 二、两个 Skill 加一次反馈，搭出自我改进的闭环

Warp 的解法是用 Agent Skills 搭一个自我改进循环。Skill 是基于文件的知识编码，把指令留在 prompt 之外，Agent 干活时可以查阅。

整个框架只有两个 Skill，中间夹着人类反馈：

内层 Skill（base skill）：存放功能领域的知识和指令。比如一个 PR 被打开时，Warp 的 code agent 就是用这个 base skill 加上上下文来做审查。

人类反馈：这是循环里最关键的一环。反馈可以简单到一个点赞，但越明确越好。Zach Lloyd 举了个例子：不只是说"这条评论不好"，而是说"你建议重命名这个变量，但我们代码库的惯例是这种全局变量用特定的命名上下文"。这种带理由的反馈，Agent 才能真正学会下次怎么做对。

外层 Skill（improver skill）：一个观察者 Agent，按计划运行，不是每个任务都跑。它的工作是把积累下来的人类反馈拉出来，对比"Agent 原本建议了什么"和"人类实际怎么回应"，然后提议一个最小、最聚焦的对 base skill 的编辑。

*[图片：Image]*

为什么这套机制能跑通？因为 Skill 是纯文件。Agent 很擅长改文件，而这些改动可以走正常的 PR / code-review 流程：人 review、approve、merge，下一轮 base skill 就自动继承了改进。

Warp 特别强调了一点：这里用的是 Skill，不是 Memory。两者的区别很关键。Skill 是程序性的、稳定的做某件事情的规范，跟单次运行无关，改动是刻意的；Memory 是 Agent 推理时自动写下来的，从不停在变。把"怎么做好 code review"这种稳定知识放进 Skill，才能被版本化、被审查、被复用。

现在这套模式跑在 Warp 整个开源仓库上，spec-writing、review、triage 三类 Agent 各自带着自己的自我改进循环。

## 三、实战案例：一个漏标的标签，怎么变成永久知识

光说框架有点抽象，看 Warp 的 issue triage agent（问题分诊 Agent）怎么跑通这个闭环。

触发条件很简单：有人在 GitHub 提了一个新 issue，GitHub Action 就触发一个 Agent，分析问题的复杂度和可行性，打上标签，再建议修复方向。这个 triage agent 跑在内层 Skill 上，里面写着每个标签是什么意思、动手前要怎么研究代码库。

有一次，第一轮分诊干得不错，但漏了一个标签："ready to spec"（可以开始写规格说明了）。这个标签很关键，它告诉贡献者"这个问题已经想清楚了，可以直接开始写产品和技术 spec"。

一位 Warp 的维护者在 issue 上留了反馈，而且说清楚了期望什么、为什么期望。这就是前面说的"高质量反馈"：不只是说"你漏了"，而是解释了"这个标签在这个场景下该打"。

接下来是外层 improver skill 登场。它在 Warp 的 Agent 编排平台 Oz 上按计划运行：认证 GitHub，跑一段打包好的 Python 脚本拉取最近带反馈的 issue，汇总成 JSON 读回上下文。注意这个细节，skill 里可以引用资源文件和脚本，不用每次重新写代码。

Agent 从反馈里识别出具体信号，提议一个最小编辑，然后开了一个 PR 来修改内层 Skill：当 issue 描述了一个真实问题、即使具体的 UI/UX 形态还没定义时，也打上 "ready to spec" 标签。

因为是 skill 文件，这个改动走正常的 code-review 流程。PR 带着描述说明"哪些信号促成了这次改动、改了什么"，人 review、approve、merge。下一轮 triage agent 跑起来时，就自动继承了这条新知识。

从"漏标一个标签"到"永久记住这个教训"，中间没有人工重写 prompt，只有一次反馈、一次 PR。这就是自我改进闭环跑通的样子。

## 四、工程经验：写好自我改进 Skill 的六条纪律

Warp 把搭自我改进 Agent 的经验提炼成六条纪律。这些理论，是从几千次 code review 里探索出来的。

1. 写原则，不写规则。把 Skill 当成在教一个聪明人，不是在给计算机编程。"找重复代码"这种方向性指引，比穷举所有变量命名规则有效得多。

2. 解释 why。每条规则背后给一句理由，让 Agent 能推理，而不是死记硬背。这样它遇到没见过的场景也能泛化。

3. 让反馈零摩擦。在人已经工作的地方捕获反馈，比如直接在 PR 或 issue 上评论，而且自动发生，不额外增加提交步骤。"反馈太难给，信号就断了。"

4. Skill 保持小，渐进式披露。好的 skill 文件不大，它引用资源文件和脚本，而不是把所有东西一次性倒进上下文。

5. 质量大于数量，但数量也有用。一位高级工程师给的几条详细领域反馈，可能比一百个点赞更有价值，因为单键点赞说不出理由。但质量信号的语料越大，系统改进越稳。Warp 用这套循环管理整个开源仓库，几百人贡献、几千次 review。

6. 重投入 improver skill。improver skill 很值得额外花精力，因为它高度可复用。code review agent 的 improver 和别的 Agent 的 improver，差别没你想的那么大。

## 写在最后：自我改进也可能让 Agent 系统性地学错

需要说清楚一件事：这篇内容来自 Claude 官方博客的一个客户案例系列，是 Anthropic 策划的，主角是 Warp。技术细节大概率是真的（Zach Lloyd 亲述）。

不过 Warp 在文末的常见问题里主动划了几条边界，反而比成功故事更有价值：

反馈会错。 他们明确说"假设反馈会出错"，不让 Agent 盲目接受。要给 Agent 上下文让它能 sanity-check，要过滤谁的反馈算数，在过滤或最终 review 阶段保持人类在环。

领域必须可验证。 如果领域可验证，先建验证 harness，再让 Agent 对着它调：生成参考语料、对比输出、修改、重复。如果不可验证，有 golden output 的地方用确定性评测；必须靠人类反馈时，只开放给领域专家，别开闸放水。

不是每个 Agent 都要独立 improver。他们的建议是折中：模板化的 base loop 捕获重叠部分，再叠加领域特定权重。少数 improver 各管一个，上百个 Agent 就该共享。

这几条边界说明一件事：自我改进不是搭个循环就一劳永逸。反馈质量、领域可验证性、人类在环的位置，任何一个没守住，闭环就会退化成"Agent 在有系统地学错东西"。

*[图片：图片]*

**一起“点****赞”****三连**↓

[跳转微信打开](https://wechat2rss.xlab.app/link-proxy/?k=4101d2ca&r=1&u=https%3A%2F%2Fmp.weixin.qq.com%2Fs%3F__biz%3DMzIyNjM2MzQyNg%3D%3D%26mid%3D2247725873%26idx%3D1%26sn%3D0cdc741a73325e737e32d0dca203375a)
