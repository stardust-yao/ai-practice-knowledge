---
title: Agent 治理：用 Hook 堵住 LLM 的偷懒、越权与失忆
date: 2026-07-16
source: raw/2026-07/2026-07-16_Agent 治理：用 Hook 堵住 LLM 的偷懒、越权与失忆.md
tags: [Agent治理, Hook, HITL, 长文本, 护栏]
---

> 作者：xiangnzhang（腾讯程序员）
> 背景：DECO 数仓 Agent 引擎的生产实践

## 核心问题

三种 LLM 行为，prompt 管不住：

| 问题 | 现象 | 根因 |
|------|------|------|
| **偷懒** | 长 SQL 写到一半跳过大段逻辑、输出 `-- 其他字段...` | 长文本超出 token 预算，模型结构性截断/略写 |
| **越权** | 还在方案设计阶段，Agent 直接把表结构推上了生产 | 模型把"发布"和"查询"视为同一类步骤，无法区分可逆性 |
| **失忆** | 改了表不分析下游风险、产出图表不告诉用户 | 模型追求最少 token 完成，不会主动加检查步骤 |

> 「"在 prompt 里多写几句 ⚠️ 禁止"根本管不住。这不是 prompt engineering 能解决的问题——长 SQL 是物理上超出 token 预算，危险操作是模型无法区分操作的可逆性差异，被动探测是模型追求最短完成路径的自然倾向。」

## 方法

**总思路**：在 Agent 框架的 Hook 切面上挂载护栏逻辑——不改业务循环、不动工具实现，靠框架层确定性兜底。

> 「prompt 定意图，Skill 定规矩，框架 Hook 定边界——能用确定性兜底的，别交给模型。」

<table>
<tr><th>护栏层</th><th>解决的问题</th><th>具体做法</th></tr>

<tr>
<td><strong>长文本完整性护栏：读写两侧 offload</strong></td>
<td>偷懒</td>
<td>

**核心原则**：「LLM 永远不直接接触脚本全文。」

- **读侧（Offload Hook，挂在 `afterTool`）**：拦截含 `scriptContent` 的响应 → 全文写入沙箱只读快照 → 返回引用句柄：

```
offloaded to /sandbox/{taskName}.remote.etl (read-only snapshot, length=N chars).
To start editing, run copy_file(...) first, then str_replace.>
```

- **写侧（Onload Hook，挂在 `beforeTool`）**：工具调用前从文件加载全文覆盖 `scriptContent`，LLM 只需传 `scriptFilePath`

- **失败语义差异化**：「读侧降级（落盘失败透传原文，承担自截断风险），写侧阻断（文件不存在直接抛异常，杜绝残缺脚本推上线）」

**效果**：修改任务工具调用输出 token **直降约 90%**（上下文里只有引用句柄）；SQL 复印自截断 **物理消除**（只走 `str_replace` 小步改）。

</td>
</tr>

<tr>
<td><strong>危险操作确认（HITL）</strong></td>
<td>越权</td>
<td>

挂在 `beforeTool` 切面上。「工具真正执行前，判断『是不是危险操作、用户授权了没』，没授权就阻断。」

- **配置驱动**：危险工具清单写在 yaml 里，每个配一个 `requiredState` key 和确认对话框
- **富交互确认**：不只是 yes/no——支持多选项（选发布方式）、带输入控件（填审批人、回刷日期）
- **完整时序**：拦截 → 弹框 → 用户选择 → 写 state → 续跑 → LLM 重调工具时守卫放行

> 「无论 Agent 是自作主张还是被诱导，只要没有人工确认这一步，packCommit / deployCommit 在框架层就物理走不通。」

**行业坐标**：HITL 已是主流框架标配（ADK `ToolConfirmation`、LangGraph HITL Middleware），但 DECO 自研了更业务化的版本——发布前展示变更清单、确认框带参数、配置驱动。

</td>
</tr>

<tr>
<td><strong>上下文联动闭环：Hook → state → Attachment</strong></td>
<td>失忆</td>
<td>

**范式**：「Hook 管『发生了什么』，Attachment 管『下一轮告诉模型什么』——采集是确定性的，注入是时机正确的。」

两个案例：

1. **RiskAnalysisHook**：改表后 `afterTool` 触发 → 分析下游影响 → 写 state → 下一轮 Attachment 自动注入风险提示。判定逻辑：带了 `tableId` 的 `upsertTable` 才算改表，新建表不触发。

2. **PythonImageHook**：Python 脚本跑完 → `beforeTool`/`afterTool` 对比文件快照 → 发现新图片 → 生成预签名 URL → Attachment 注入，**图直接出现在对话流里**。

> 「LLM 不知道 Python 脚本产出了什么文件——它是"瞎子"。这不是"忘了查"，而是根本不知道有东西该查。」

> 「把『LLM 需要主动查』的操作降维为『框架主动 push』——LLM 不再是『需要查的就不查』，而是『不管想不想查都会被喂到嘴边』。」

</td>
</tr>

</table>

## 关键引用

> 「基础设施和推理逻辑解耦——Hook 切面上的逻辑独立运作，模型的 ReAct 循环不用感知；新增/删除一个 Hook，主流程一行代码都不用改。」

> 「"在 prompt 里多写几句 ⚠️ 禁止"根本管不住。唯一的解法是在 Agent 框架层，让偷懒和越权的路径代码级强制走不通，让失忆的已知盲区确定性补齐。」

> 「prompt 是软约束，不是安全边界。」
