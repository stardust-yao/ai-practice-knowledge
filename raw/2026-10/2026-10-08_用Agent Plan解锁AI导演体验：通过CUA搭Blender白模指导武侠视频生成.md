---
title: 用Agent Plan解锁AI导演体验：通过CUA搭Blender白模指导武侠视频生成
date: 2026-10-08
source: https://mp.weixin.qq.com/s?__biz=MzI1MzYzMjE0MQ==&amp;mid=2247522909&amp;idx=1&amp;sn=82ca1c732c0de74e3530284c6c4df3f1
account: 字节跳动技术团队
fetched_at: 2026-10-09 18:00:04 CST
article_id: 82ca1c732c0de74e3530284c6c4df3f1
---

原创 Agent Plan 2026-10-08 19:02 北京

  
  
*[图片]*

  
  
用 AI 直接生成一段带动作和运镜的视频，最容易卡住的地方是：动作和镜头对不上你想要的效果。

提示词里写  "360 度环绕镜头"" 第 7 秒主角撩剑反击 "，模型往往给不出稳定结果 —— 动作节点偏移、镜头节奏随机、分镜顺序漂移，多调几轮提示词也未必收敛。

这篇文章想分享的是我们在实践中跑通的一条思路：使用 Agent Plan 中的专属 Harness —— CUA（Computer Use Agent），操作最近火热的 Blender，零门槛将一句武侠创意转化为白模预演和可控的视频成片。

思路其实很像真正的导演拍片：先把人物关键动作、运镜轨迹定下来，Blender 白模则提供了这样的三维空间。再把这段白模视频作为参考喂给生视频模型。火山方舟 Agent Plan 套餐覆盖全流程所需的模型及Harness，由 Agent 自动操控云桌面中的 Blender，从创意构思、白模搭建，到一键生成电影感成片，全程无需专业基础，纯小白也能解锁 AI 导演体验。

**核心亮点：**

- **CUA操作Blender简单易用：**让 Agent 直接使用云桌面中的专业三维软件，串联建模、动画、运镜和渲染，**0门槛白模视频制作**。
- **全模态模型及专属 Harness升级：**Agent Plan套餐支持多模态模型，集成**字节SOTA级 Seedance、Seedream 生图生视频模型**能力，串联从创意构思、动作设计到视频成片的完整流程。
- **兼容主流工具：**多生态兼容，无缝接入 Claude Code、Codex等**主流编程及 Agent 工具**。
- **用量清晰可查：**采用 Agent 燃料值（AFP）作为统一用量单位，**额度用量清晰可查**。

下面我们用一个武侠主题的视频生成案例，完整展现从创意到 20 秒武侠成片的全过程。

下面我们用一个武侠主题的视频生成案例，完整展现从创意到 20 秒武侠成片的全过程。

**一、视频生成案例**

本案例选的题材是 "武当山之巅，两位武者交手"，展示 **20 秒白模预演、3 张角色／场景参考图、20 秒武侠成片及对照视频。**下文保留了实际使用的各阶段的提示词与演示素材，可按顺序一步步复现。

本文中的“白模”指的是以简化几何体和基础材质表达动作、空间与镜头的预演；也可以用不同颜色区分角色，无需先完成精细人物建模。

**「核心使用能力」：**

*[图片]*

**二、前置准备**

**Step1：开通 Agent Plan 并准备Computer Use Agent 环境**

（1）**购买套餐：请登陆**「**火山方舟**」（[https://console.volcengine.com/ark/region:cn-beijing/openManagementLLM=%7B%7D&OpenModelVisible=false&advancedActiveKey=agentPlan）](https://console.volcengine.com/ark/region:cn-beijing/openManagementLLM=%7B%7D&OpenModelVisible=false&advancedActiveKey=agentPlan）)或 「**官网活动页**」（[https://www.volcengine.com/activity/agentplan）](https://www.volcengine.com/activity/agentplan）)

购买 Agent Plan 套餐。购买**Medium 及以上套餐**即可开启使用套餐内专属 Harness 工具——   Computer Use Agent。

请注意，仅large及以上套餐支持seedance模型

*[图片]*

**（2）安装 Computer use Agent：**参考官方文档：[https://docs.volcengine.com/docs/82379/2670601?lang=zh](https://docs.volcengine.com/docs/82379/2670601?lang=zh)

**（3）配置 Agent Plan 套餐模型：**您可通过以下两种方式进行安装

- **方式1: 一键安装：**推荐使用 ArkCLI 一键安装模型及Harness，1分钟帮你的 Agent 一键安装 Agent Plan。○具体教程可见官方指南（https://docs.volcengine.com/docs/ark/agent-plan-personal-ark-cli?lang=zh）
- **方式2: 手动配置：****○**需要获取 Agent Plan 支持的专属 Base URL、专属 API Key及模型配置，才能正常使用并抵扣套餐额度。

**方式1: 自动化配置 (推荐)**

**配置项**

ArkCLI -一键配置模型及 harness

**截图示意**

*[图片]*

**说明**

ArkCLI （[https://docs.volcengine.com/docs/ark/agent-plan-personal-ark-cli?lang=zh）Helper](https://docs.volcengine.com/docs/ark/agent-plan-personal-ark-cli?lang=zh）Helper) 是一个编码工具助手，支持快速配置选择的工具接入 Agent Plan。安装并运行该助手，根据界面提示操作可自动完成工具配置，降低手动配置的时间成本和出错风险。

**方式2: 手动配置**

**配置项**

配置模型及专属 Base URL

**截图示意**

*[图片]*

**说明**

获取 Agent Plan 的专属 Base URL、模型配置。套餐集合优秀主流国产模型，可灵活自由切换或使用Auto模式调度。详见 快速开始 ([https://docs.volcengine.com/docs/ark/agent-plan-personal-get-started?lang=zh）](https://docs.volcengine.com/docs/ark/agent-plan-personal-get-started?lang=zh）)

**配置项**

获取专属API Key

**截图示意**

*[图片]*

**说明**

请注意 Agent Plan 使用专属 API Key，请勿混用。

**配置项**

安装生图生视频Skill

**截图示意**

*[图片]*

**说明**

套餐内包含生图、生视频模型，支持通过 Skill 接入并使用。具体参照 视觉模型配置文档（[https://s.c1ns.cn/z58Kd）](https://s.c1ns.cn/z58Kd）)

**配置项**

安装Harness

**截图示意**

*[图片]*

**说明**

套餐内包括豆包搜索、专业数据集、Agent记忆、Al Native 应用开发底座、Agent进化等Harness，支持开箱即用，并统一抵扣套餐内AFP额度

**接入使用**

**配置项**

接入AI工具

**截图示意**

*[图片]*

**说明**

兼容主流工具，详细接入可参照官网文档：

- Codex（https://console.volcengine.com/ark/region:cn-beijing/docs/ark/agent-plan-personal-codex?agentMode=close&lang=zh）
- Claude Code（https://docs.volcengine.com/docs/ark/agent-plan-personal-claude-code?lang=zh）
- OpenCode（https://docs.volcengine.com/docs/ark/agent-plan-personal-opencode?lang=zh）
- OpenClaw（https://docs.volcengine.com/docs/ark/agent-plan-personal-openclaw?lang=zh）
- Hermes Agent（https://docs.volcengine.com/docs/ark/agent-plan-personal-hermes-agent?lang=zh）
- Trae（https://docs.volcengine.com/docs/ark/agent-plan-personal-trae?lang=zh）
- 其他工具（https://docs.volcengine.com/docs/ark/agent-plan-personal-other-tools?lang=zh）

**Step2 ：检查生图、生视频与素材存储的配置**

下文提示词中的 tos://generate-video/... 是本案例路径，复现时应替换为自己实际上传的桶名和对象路径；白模预演的版本也应与最终选定的视频一致。

*[图片]*

**三、详细操作指南**

**Step1：使用 Blender 制作白模预演**

**prompt：**

```
帮我创建一个2个人使用少林武功，太极拳和峨眉派武功相互激烈打斗的武功场景，场景是在武当山。
`人物打斗要非常激烈，符合太极拳、峨眉剑术的艺术设计，包括轻功追逐、跳跃，镜头360度翻转，超快速运镜，人物对峙的特写等镜头，运镜要非常丰富，武装电影的运镜效果`
`
`
`按照上面提示词使用blender完成建模、运镜，再进行白模预演，生成参考视频（比如：使用立方体代替拟人化建模）`
``

blender制作白模参考：

*[图片]*

效果展示：

**Step2：上传白模视频至 TOS**

把白模视频上传到tos桶中，便于后期生视频使用；

**prompt：**

```
`帮我上传白模预演视频文件到tos桶中
```

**Step3：生成角色与场景参考图**

**prompt：**

生成角色参考图片，参考，`
`【角色】橙色简模，少林/太极武僧（男，约1.8米，灰褐僧袍，太极掌法，圆活连绵）；蓝色简模＝峨眉派女武者，（约1.65米，白衣蓝纹劲装，手中长剑由你生成：请按她手臂的运动轨迹还原峨眉剑法——她每次手臂由下而上或横扫的动作即为撩剑/挂剑，由上而下即为劈崩）。深蓝屋顶红柱白石建筑＝武当山道观山顶石台，临崖云海，远景群峰；补充写实木构瓦面、山岚与清晨柔光。`
``

```

效果展示：

*[图片]*

*[图片]*

*[图片]*

**Step4：使用白模视频生成最终视频**

**prompt：**

```
`参考视频是武当山之巅比武的灰色简模预演（无武器、纯动作参考），请还原为写实武侠电影质感的打斗短片，严格保留人物位置、运动轨迹、相机运动和切镜时序，20秒内不新增或删减镜头。`
`【角色】橙色简模，tos://generate-video/role_shaolin_monk.png，少林/太极武僧（男，约1.8米，灰褐僧袍，太极掌法，圆活连绵）；蓝色简模＝峨眉派女武者，tos://generate-video/role_emei_female.png（约1.65米，白衣蓝纹劲装，手中长剑由你生成：请按她手臂的运动轨迹还原峨眉剑法——她每次手臂由下而上或横扫的动作即为撩剑/挂剑，由上而下即为劈崩）。深蓝屋顶红柱白石建筑＝武当山道观山顶石台，临崖云海，远景群峰；补充写实木构瓦面、山岚与清晨柔光。tos://generate-video/scene_wudang_temple.png`
`【分镜】tos://generate-video/wudang_white_model_v2_20s_480f.mp4  0–2.5s 对峙特写缓推；2.5–5s 大全景绕圈游走；5–7s 中景横移：武僧突进按掌、峨眉侧闪横掌反击、双双撤步；7–10s 慢动作：峨眉挑掌由下而上撩起（还原为撩剑剑光）、武僧仰身闪避；10–12.5s 双双360°后空翻，相机同步360°环绕+翻转；12.5–14.5s 低机位：峨眉下扫（还原挂剑下扫）、武僧野马分鬃跃过她头顶；14.5–17s 轻功追逐飞檐上房；17–18.5s 殿顶迎面对冲；18.5–20s 子弹时间：腾空对撞，峨眉崩掌（还原崩剑下劈）对武僧双按掌，悬停后坠落，落地定格对峙收尾。`
`【约束】写实武侠电影质感；相机与变速节奏跟参考一致；太极用云手、揽雀尾、野马分鬃，峨眉用撩云挂点崩剑法，剑刃剑光随手臂轨迹生成；无字幕水印；保持身高比例、朝向与站位，不互换角色。`
`
`
`好的 我们现在参考图和白模视频都有了，参考白模视频和参考图生成最终的视频；`
``

```

**四、AFP 用量消耗**

本案例包含 **Blender 白模预演 + 参考图生成 + 最终视频生成**，需统计整条制作流程，不能只计算 Blender 渲染或最终一次生成。AFP 详情参见官方AFP抵扣规则（[https://s.c1ns.cn/2wQid），实际消耗以方舟控制台账单为准。](https://s.c1ns.cn/2wQid），实际消耗以方舟控制台账单为准。)

*[图片]*

这套 「白模预演 → 参考帧 → 生视频」的流程并不局限于武侠短片。科幻机甲追逐、都市动作戏、古风场景调度等对动作和镜头时序有要求的内容，都可以沿用同样的思路 —— 先用白模把节奏和机位定准，再交给生视频模型出画面。

目前 CUA（Computer Use Agent）已在 Agent Plan 的 Medium 及以上套餐开放，Large 及以上套餐支持 Seedance 生视频模型。想体验AI导演的创作流程，可以直接按文章中的步骤跑一遍。

[跳转微信打开](https://wechat2rss.xlab.app/link-proxy/?k=4e0e3f4b&r=1&u=https%3A%2F%2Fmp.weixin.qq.com%2Fs%3F__biz%3DMzI1MzYzMjE0MQ%3D%3D%26mid%3D2247522909%26idx%3D1%26sn%3D82ca1c732c0de74e3530284c6c4df3f1)
