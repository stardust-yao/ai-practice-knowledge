---
title: 同样的代码，Claude竟比GPT多算73%的token！token自测教程来了
date: 2026-07-18
source: https://mp.weixin.qq.com/s?__biz=MzIyNjM2MzQyNg==&amp;mid=2247724293&amp;idx=1&amp;sn=fcca123422738db4eb33744064a87654
account: Datawhale
fetched_at: 2026-07-31 12:38:26 CST
article_id: fcca123422738db4eb33744064a87654
---

原创 Datawhale 2026-07-18 23:59 上海

  
  
*[图片]*

  
  
# Datawhale干货 作者：Ruslan Ianberdin模型的账单价格标的是"每百万token多少钱"，但没人告诉你，同一段代码在不同模型上会被切成不同数量的token。这件事直接决定了你实际付了多少钱，而且大部分人从来没测过。Playcode本月发布的一份测评给出了具体数字：同一份2888字符的TypeScript文件，GPT用o200k分词器切出681个token，Claude最新的分词器切出1178个，多了73%。挂牌单价没有变化，实际花费已经变了。这篇文章分两部分：先说清楚这个差距从哪来，再给出你自己动手测的步骤。

## 一、差距是怎么来的

模型不会直接处理文字，而是先把文字切成token，再按token数量计价。切法由分词器决定，每家的分词器不是同一套逻辑，同一段内容切出的token数量自然不一样。

Playcode用16种真实内容（英文散文、HTML、JavaScript、Python、TypeScript、Rust、JSON工具schema、中文文本等）分别过了各家的官方计数接口，包括Anthropic的count_tokens、OpenAI的tiktoken（o200k_base编码器）、Gemini和Grok各自的计数接口，还用真实付费请求核对过预测值和账单是否一致。

几个具体数字：

- Anthropic的新分词器（Sonnet 5、Opus 4.8、Fable 5用的这一版）比旧分词器平均多切出约32%的token，挂牌价没变
- 以GPT的o200k为基准，Claude新分词器在TypeScript上是1.73倍，Rust是1.58倍，JavaScript是1.52倍，Python是1.50倍，英文散文是1.40倍
- 中文文本上，Claude新旧两版分词器都比GPT多切约1.45-1.55倍——这是长期存在的现象，不是新分词器造成的
- Gemini 3 Flash的分词器比GPT略重（1.09倍），但挂牌单价低很多，综合仍是最便宜的选项之一

Anthropic新旧分词器对比：

*[图片]*

中文这一行几乎没变化，涨幅主要集中在英文和代码上。

跨厂商对比：

*[图片]*

为什么代码上的差距比文字更大，尤其是TypeScript最明显：o200k对TypeScript的压缩效率特别高，平均4.24个字符对应1个token，这大概率是因为训练数据里有大量网络JavaScript/TypeScript代码，camelCase命名、JSX语法这些模式经常被压缩成一个token。Claude的分词器在代码和文字上的压缩效率比较接近，没有针对代码单独优化，所以差距在代码场景被放大，而编码任务恰好是agent最常处理的内容类型。

换算成实际价格，具体如下（挂牌单价为每百万token，输入/输出）：

*[图片]*

几个值得注意的行：Opus 4.6和4.8挂牌价一样，实际有效单价却差了约32%；GPT-5.5和GPT-5.6 Sol共用同一套分词器，挂牌价相同、实际单价也确实相同；Gemini 3 Flash虽然分词器比GPT略重，但挂牌价低出很多，仍是综合最便宜的选项之一。

```
需要说明的是，这只是输入端的分词差异。模型回复的啰嗦程度、思考token、缓存读写频率、工具调用次数，这些变量叠加起来，实际任务总花费的差距可能远超过73%这个数字
`有人反映实际用下来差2到4倍，也是合理的，只是这已经是另一层变量了。`

## 二、自己动手测一遍

不用等别人测，各家的计数接口大多免费，五分钟能测完你自己的代码。

测Claude（Anthropic）

Anthropic提供了官方的count_tokens接口，传入文本直接返回token数，不需要真的调用模型生成内容，也不产生模型调用的费用。

```
`POST [https://api.anthropic.com/v1/messages/count_tokens](https://api.anthropic.com/v1/messages/count_tokens)
```

传入你要测试的文本内容，返回结果里的字段就是这段内容会被计的token数。

测GPT（OpenAI）

OpenAI的o200k_base编码器是公开的，本地装一个开源库tiktoken就能直接算，完全不需要联网调用API，也不花钱。

import tiktoken`
`enc = tiktoken.get_encoding("o200k_base")`
`tokens = enc.encode(你的文本)`
`print(len(tokens))`

```

测Gemini / Grok

Google和xAI也各自提供了token计数接口，用法和上面类似，传文本进去返回数字。

怎么用这几个数字

拿你自己常用的一段代码或prompt，分别丢进上面几个接口，对比返回的token数，算出比例。如果你主要写TypeScript或JavaScript，大概率会看到Claude的数字明显更高；如果内容以中文为主，差距会缩小，甚至反过来。

## 三、一个判断方法，比记住某个百分比更有用

73%这个数字会随模型迭代很快过时，但背后的判断方法不会：

- 厂商换分词器，等同于变相调价，账单上不会写明这一条，需要自己核实
- 挂牌单价不能跨厂商直接比较，尤其是代码类工作负载
- 真正该比的是"完成同一个任务花了多少钱"，而不是"每token多少钱"——这个数字需要把分词、回复长度、缓存命中率都算进去，模型返回的usage字段能提供真实依据

模型选型不该只看挂牌价，用自己的真实内容测一遍，比记住任何单一数字都可靠。

*[图片：图片]*

**一起“点****赞”****三连**↓

[跳转微信打开](https://wechat2rss.xlab.app/link-proxy/?k=4bc546bb&r=1&u=https%3A%2F%2Fmp.weixin.qq.com%2Fs%3F__biz%3DMzIyNjM2MzQyNg%3D%3D%26mid%3D2247724293%26idx%3D1%26sn%3Dfcca123422738db4eb33744064a87654)
