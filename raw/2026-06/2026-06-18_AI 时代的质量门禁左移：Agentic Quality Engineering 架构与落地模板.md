---
title: AI 时代的质量门禁左移：Agentic Quality Engineering 架构与落地模板
date: 2026-06-18
source: https://mp.weixin.qq.com/s?__biz=MzI0MjczMjM2NA==&amp;mid=2247499500&amp;idx=1&amp;sn=f084fc60050c017252355995afaff7b6
account: 爱奇艺技术产品团队
fetched_at: 2026-07-31 12:38:26 CST
article_id: f084fc60050c017252355995afaff7b6
---

移动产品研发团队 2026-06-18 12:00 北京

  
  
*[图片]*

  
AI质量门禁左移的架构实践

  
***01******#***

**为什么质量门禁必须左移**

AI 编码改变的不是单个开发者的写代码速度，而是整个交付系统里的流量分布。过去很多团队的瓶颈在“代码写不完”；现在瓶颈会快速迁移到 Review、测试、验收、复验和线上风险处置。

如果质量门禁仍然放在提交之后，团队会看到一个很典型的现象：代码变更多了，Review 队列更长了；功能分支更多了，测试环境更拥堵了；问题暴露更晚了，修复成本也更高了。质量门禁左移的本质，是把验证能力前置到开发活动内部，让每次 AI 参与生成的变更都能尽早进入可执行的验证闭环。

*[图片]*

## 左移不是多测一点，而是改变验证能力的位置

- **从人工经验到显式契约：**把入口、环境、动作、断言和证据要求写成 AI 可执行的结构。
- **从结论驱动到证据驱动：**任何通过、失败、阻塞都必须能回看截图、日志、网络请求、结构树或度量数据。
- **从单点工具到系统能力：**自动化执行、环境准备、报告治理、复验入口都要进入同一条链路。

***02******#***

**AI 在质量门禁中的角色：**

**从 Copilot 到 Quality Orchestrator**

AI 参与的是整条质量门禁链路的编排。它通过 Harness 管理上下文，通过 Agent 拆解任务，通过 Subagent 承担专项验证，通过 Skills 调用稳定工具，最后把证据交给门禁规则做可审计判定。

*[图片]*

- **Harness：**质量门禁的运行框架，管理上下文、工具、状态、权限、日志和执行约束。
- **Agent：**质量任务负责人，负责理解变更、识别风险、规划验证路径和解释证据。
- **Subagent：**专项验证角色，例如 UI、Network、Telemetry、Visual、Report，各自只处理清晰边界内的问题。
- **Skills：**可复用工程能力封装，例如进入指定页面、采集截图和结构树、抓取请求、校验字段、生成复验报告。

```
agentic_quality_gate:
`  harness:`
`    owns:`
`      - context_window`
`      - tool_registry`
`      - execution_state`
`      - audit_log`
`      - permission_boundary`
`  planner_agent:`
`    responsibilities:`
`      - understand_change`
`      - identify_risk`
`      - select_gate_level`
`      - dispatch_subagents`
`      - summarize_evidence`
`  subagents:`
`    ui_subagent:`
`      skills: [navigate_to_page, capture_screenshot, inspect_ui_tree]`
`    network_subagent:`
`      skills: [start_capture, filter_requests, assert_fields]`
`    telemetry_subagent:`
`      skills: [collect_events, compare_event_schema, count_occurrences]`
`    report_subagent:`
`      skills: [assemble_evidence, classify_failure, create_recheck_entry]`
`  rule:`
`    ai_orchestrates: true`
`    gate_decision_remains_rule_based: true`

***03******#***

**参考架构：**

**AI Harness 驱动的质量门禁系统**

要支撑大量 AI 生成代码的 Review 和测试，质量能力需要被封装成稳定的系统，而不是分散在个人脚本、口头经验和临时检查清单里。更合适的架构是：AI Harness 承载上下文和运行约束，Planner Agent 负责任务规划，Specialist Subagents 分工处理专项验证，Skills 调用稳定工具，真正的采证和判定由可审计的工程模块完成。

*[图片]*

## 架构边界要清楚

- **AI Agent：**负责任务拆解、风险识别、调用工具和解释证据，但不直接替代门禁判定规则。
- **执行运行时：**负责真实环境操作，包括 UI、接口、网络、Mock、设备或浏览器能力。
- **证据总线：**负责把过程数据统一收口，避免“通过了但无法证明”。
- **门禁引擎：**负责把不同证据映射为 PASS、FAIL、BLOCK，并产生可追溯报告。

```
`
quality_gate_system:`

`  trigger:`

`    - ide_generated_change`

`    - pull_request`

`    - pre_merge_ci`

`  ai_harness:`

`    context:`

`      - requirement`

`      - code_diff`

`      - case_library`

`      - historical_defects`

`    guardrails:`

`      - single_case_transaction`

`      - evidence_required_before_pass`

`      - block_when_context_missing`

`  planner_agent:`

`    output:`

`      - risk_assessment`

`      - gate_level`

`      - subagent_plan`

`  subagents:`

`    - ui_subagent`

`    - network_subagent`

`    - telemetry_subagent`

`    - visual_subagent`

`    - report_subagent`

`  contract:`

`    input: requirement_or_diff`

`    output: executable_case_dsl`

`  runtime:`

`    capabilities:`

`      - skills.ui_operation`

`      - skills.api_replay`

`      - skills.network_capture`

`      - skills.mock_injection`

`      - skills.visual_compare`

`  evidence:`

`    required:`

`      - screenshots`

`      - ui_tree`

`      - network_trace`

`      - logs`

`      - assertion_result`

`  gate:`

`    decisions:`

`      pass: evidence_complete_and_assertions_met`

`      fail: assertion_failed_with_repro_steps`

`      block: environment_or_evidence_not_ready`

```

***04******#***

**核心抽象：**

**把测试用例写成 AI 可执行契约**

AI 不怕用例长，AI 怕用例模糊。面向人的测试说明可以依赖经验补全上下文，但面向 AI 的自测用例必须像接口协议一样明确：输入是什么、环境如何准备、入口如何定位、每一步如何执行、证据如何收集、什么情况下不能继续。

*[图片]*

## 技术人员更容易复用的契约模板

契约并不是为了“把用例写复杂”，而是为了把 AI 原本需要猜的上下文变成明确输入。契约越清楚，AI 的执行越稳定，Review 的证据越可复查。

```
`
case:`

`  id: mobile_entry_bubble_hide_after_click`

`  goal: verify_entry_bubble_disappears_and_target_tab_selected`

`  risk_level: high`

`preconditions:`

`  account:`

`    login: required`

`    permissions: [content_access]`

`  device:`

`    platform: mobile`

`    orientation: portrait`

`  experiment:`

`    entry_bubble_enabled: true`

`  data:`

`    channel_has_reservation_bubble: true`

`entry:`

`  route: app_home_to_channel_page`

`  anchors:`

`    - channel_tab_visible`

`    - reservation_bubble_visible`

`  ready_when:`

`    - page_stable_for_ms: 1200`

`    - loading_indicator_absent: true`

`steps:`

`  - action: tap`

`    target: reservation_bubble`

`    observe:`

`      - target_tab_selected`

`      - bubble_not_visible`

`assertions:`

`  functional:`

`    - reservation_bubble.visible == false`

`    - selected_tab == target_tab`

`  telemetry:`

`    - event_name == entry_bubble_click`

`    - request_count == 1`

`  visual:`

`    - no_overlap_around_tab_area`

`evidence:`

`  required:`

`    - before_screenshot`

`    - after_screenshot`

`    - ui_tree_after_action`

`    - network_trace`

`    - final_report`

```

```
``

```

```
`***05******#***

**执行状态机：**

**让 AI 只能在证据闭环里给结论**
`

```

很多 AI 测试实践失败，不是因为 AI 不够聪明，而是因为执行过程没有状态机约束。只要允许 AI 在证据不足时继续往下走，就会出现“看起来执行了，但结论不可信”的情况。

一个可靠的执行引擎应该把每条用例当成事务：准备失败就是 BLOCK，导航失败就是 BLOCK，断言失败才是 FAIL，证据缺失不能写 PASS。

*[图片]*

```
`***06******#***

**技术广度：不是只测功能，**

**而是建设一条证据流水线**
`

```

质量门禁左移要解决的不只是“功能是否能点通”。在真实研发里，很多线上问题来自埋点字段错误、UI 偏差、弱网异常、状态污染、兼容性、性能退化或灰度配置错误。架构上要预留足够的证据类型和断言扩展点。

*[图片]*

```
`
## 证据模型要足够宽

- **功能证据：**用户动作前后的截图、页面结构、状态持久化结果。
- **数据证据：**接口请求、字段值、请求次数、链路耗时、错误码。
- **视觉证据：**运行截图、设计源、控件边界、差异定位。
- **环境证据：**账号、设备、版本、网络、实验、Mock、缓存状态。
- **治理证据：**失败归因、阻塞原因、复验记录、趋势指标。

```

```

```

***07******#***

**门禁策略：**

**用风险分级决定验证深度**

不是所有变更都应该跑同一套重型验证。合理的做法是用风险模型选择门禁强度：低风险变更快速验证，高风险链路进入更完整的证据闭环，涉及关键业务、支付、账号、埋点或 UI 核心路径时再提高验证级别。

*[图片]*

risk_model:`

`  dimensions:`

`    business_impact:`

`      high: payment, login, content_publish, critical_entry`

`      medium: recommendation, notification, profile`

`      low: copywriting, non_core_style`

`    change_complexity:`

`      high: cross_module_or_state_machine_change`

`      medium: single_module_logic_change`

`      low: static_resource_or_copy_change`

`    evidence_requirement:`

`      high: screenshot_plus_network_plus_logs_plus_replay`

`      medium: screenshot_plus_network`

`      low: smoke_result`

`gate_level:`

`  L1: low_risk_fast_gate`

`  L2: standard_gate_for_user_visible_change`

`  L3: strong_gate_for_core_path_or_ai_generated_large_diff`

```

```
`***08******#***

**实际案例：**

**移动端入口气泡的完整自测闭环**
`

```

下面用一个抽象后的移动端案例说明如何落地。需求是：频道页存在一个“预约气泡”，用户点击气泡后，应进入目标 Tab，气泡消失，并触发一次正确上报。这个需求看似很小，但覆盖了入口定位、状态切换、UI 展示、埋点上报和证据复验。

*[图片]*

```
`
## 这个案例能迁移到哪些场景

- **入口类需求：**浮层、气泡、弹窗、运营位、Tab、快捷入口。
- **状态类需求：**领取、预约、关注、收藏、订阅、购买、开关切换。
- **上报类需求：**点击、曝光、停留、转化、异常路径采集。
- **视觉类需求：**首屏布局、边界遮挡、动态字体、深色模式、多端适配。

`

```

```
``

```

```
``

```

```
``

```

***09******#***

**落地路线：**

**从工具试点到组织级质量资产**

真正能复利的不是“跑通一次 AI 自测”，而是让每次执行都能沉淀资产。用例会变成契约库，证据会变成问题样本，阻塞原因会变成基础设施建设清单，报告会变成质量趋势。

*[图片]*

```
`
## 建议优先观察的指标

- **提测前缺陷拦截数：**验证质量是否真的前移。
- **AI 自测覆盖率：**核心链路中可执行契约的覆盖比例。
- **BLOCK 原因分布：**环境、数据、入口、证据、工具能力哪个最拖后腿。
- **报告有效率：**有结论、有证据、有归因、有复验入口的报告比例。
- **复验耗时：**修复后从触发复验到给出可信报告的平均时间。

`

```

```
``

```

```
``

```

```
``

```

```
``

```

***10******#***

**写在最后：**

**AI工程化的核心竞争点会转向验证系统**

AI 编码会继续提升代码生产效率，但工程组织之间的差距不会只体现在“谁生成代码更快”。更关键的问题是：当代码生成速度提升之后，团队是否拥有足够强的验证系统来承接这些变更。

质量门禁左移的价值，是把测试从后置的人力活动，升级为开发过程中的系统能力。它要求团队把经验契约化、把执行状态机化、把证据流水线化、把报告治理化。这样，AI 才不只是一个写代码的助手，而是进入了一套能支撑真实交付的工程闭环。

*[图片：图片]*

[这张成绩单，数字一个比一个猛！](https://mp.weixin.qq.com/s?__biz=MzI0MjczMjM2NA==&mid=2247499458&idx=1&sn=6486858c5839abfd889e48cd0e8135bf&scene=21#wechat_redirect)

[别让AI瞎猜了：用Harness Engineering 终结无限返工](https://mp.weixin.qq.com/s?__biz=MzI0MjczMjM2NA==&mid=2247499431&idx=1&sn=baa9408cc9502ed7e54ca208d4af0f2b&scene=21#wechat_redirect)

[内存峰值降60%+，动图加载快75%：爱奇艺图片库一次从'能用'到'极致'的跨越](https://mp.weixin.qq.com/s?__biz=MzI0MjczMjM2NA==&mid=2247499415&idx=1&sn=ffb14bf71eac13f839a42a9c7865d809&scene=21#wechat_redirect)

[零侵入、低成本！轻松为老系统注入 AI 灵魂](https://mp.weixin.qq.com/s?__biz=MzI0MjczMjM2NA==&mid=2247499399&idx=1&sn=63e1a3f9204caaa35166cbc9e5812071&scene=21#wechat_redirect)

[治愈 Cursor AI 编程的 “幻觉”？用它就够了！](https://mp.weixin.qq.com/s?__biz=MzI0MjczMjM2NA==&mid=2247499312&idx=1&sn=14e73f366025eca7524e87f02eb759f9&scene=21#wechat_redirect)

[跳转微信打开](https://wechat2rss.xlab.app/link-proxy/?k=9ecfee41&r=1&u=https%3A%2F%2Fmp.weixin.qq.com%2Fs%3F__biz%3DMzI0MjczMjM2NA%3D%3D%26mid%3D2247499500%26idx%3D1%26sn%3Df084fc60050c017252355995afaff7b6)
