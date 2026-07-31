---
title: 从JS云函数到MCP：打造跨平台AI Agent工具的工程实践
date: 2025-12-12
source: https://mp.weixin.qq.com/s?__biz=Mzg3Njc0NTgwMg==&amp;mid=2247503836&amp;idx=1&amp;sn=d84b2e1c6ce9330751cd4d58b3ec32ef
account: 腾讯技术工程
fetched_at: 2026-07-31 12:38:25 CST
article_id: d84b2e1c6ce9330751cd4d58b3ec32ef
---

原创 AI 2025-12-12 12:01 上海

  
  
*[图片]*

  
构建 AI 工具生态这件事上，过去一年B站做了不少尝试。

  
构建 AI 工具生态这件事上，过去一年我们做了不少尝试。

回头看，会觉得这条路径像是在搭建一条越来越清晰的“能力生产线”：

从写 JS → Agent Tool 工具 → 成为 MCP 工具 → 成为跨平台 Agent 能力。

这篇文章我们就按这条演进路线，把底层逻辑、踩坑经验和最终的工程方案完整讲清楚。

**一、先做简单介绍**

我们做了一个“在线 JS 云函数平台”，它的本质是：把写一个 JS 函数，变成给 AI 赋予一个 Tool 新能力。

这套系统经历了三个阶段：

**1.  第一版：**只是 Flowise 里的一个 LangChain StructuredTool 扩展，能在工作流里被 Agent 调用。

**Flowise**（*https://flowiseai.com/*） 是一款开源、可视化的 AI 工作流工具，通过拖拽节点即可构建 LLM 应用或 Agent。它底层基于 LangChain 的 TypeScript 版本，因此天然具备模型调用、工具调用、链式处理、记忆与向量检索等能力。

当时我们在技术选型时使用 Flowise 做AI工作流平台有两个原因：

一是它基于 LangChain 的 TypeScript 版本——在早期 AI 框架还不成熟时，这是少数原生支持 TS 的方案；二是它提供了可拖拽的可视化工作流，能让我们快速搭建和验证 AI 原型。

**2.  第二版：**演进为一个浏览器里的 云函数 IDE：在线写代码、调试、沙箱运行时、连内网 gRPC/HTTP/MySQL。

**3.  现在：**接上 MCP 协议，变成一个可以被「任何支持 MCP 的 Agent / Studio」跨平台调用的独立工具平台，并支持 SSE + Streamable HTTP 两种流式协议。

**二、为什么我们需要“AI 工具能力层”？**

在我们内部构建 AI 应用（客服、直播运营助手等）时，遇到几个非常典型的痛点。

**1. 工具很多，但每接一次 AI，**

**都要重写一遍工具**

- 想让 AI 查开播状态、查卡顿、查稿件、给用户发通知……
- 后端能力其实都有，但每接一个新智能体，就要：

- 在某个项目里再写一遍调用代码
- 手动写结构化参数 / 返回值
- 校验、鉴权

- 每个团队都重新写一遍

**2. AI 需要的是“能力”，而不是“接口”**

业务接口往往是这样的：

```
GET /room/info?roomid=123
```

但是用户却会说：“查一下imzerooo开播状态”

这中间的自然语言 → 参数的语义映射，很难靠简单规则完成。

如果让开发者直接暴露接口，AI 是很难用好的。

**3. JSON 不是 AI 友好的输入格式**

内网接口通常返回一大坨 JSON。LLM 解析 JSON 没问题，但：

- 字段多、嵌套深 → 容易丢字段
- 字段名杂乱 → 模型记不住
- 文本内容多 → 容易产生幻觉

AI 友好的格式是：

- Markdown 表格
- 简洁的自然语言
- 提炼过的信息

而不是整包 JSON。

**4. 工具没有做成“资产层”**

以前的工具要么：

- 绑死在某个 AI 工作流上
- 埋在某个项目里
- 放在某个业务脚本中

无法像资产一样复用。

所以一切问题的核心其实是：

缺少一个可以写工具、管理工具、发布工具、复用工具的统一能力层。

而我们做的，就是让这件事：**只需写一段 JS 函数**。

**三、第一版：StructuredTool**

**——****工具能力的萌芽**

最初我们是在 Flowise 里写 StructuredTool 组件。

*[图片]*

Flowise 底层基于 LangChain，所以我们写了很多 StructuredTool：

```
exportclassQueryLiveRoomToolextendsStructuredTool {**`  name = 'QueryLiveRoomTool'``  description = '根据 uid 查询主播信息'````  schema = z.object({``    roomid: z.string().describe('直播间id')``  })````  async _call({ roomid }) {``    const res = await axios.post({...})``    return formatForAI(res)``  }``}`这一版有几个优点：工具能被 Agent 调用参数有 schema有一定的模块化但有几个局限：工具生命周期跟 Flowise 项目绑死要写 TS、写 Node 项目，对效率很不友好无法跨平台使用JSON 处理还是要自己写无法注入通用能力（如内网 SDK）于是我们开始考虑平台化。**四、第二版：在线 JS 云函数平台（NodeVM 运行时）**我们打造了一套全新的平台：在线 JS 云函数平台。开发者不需要知道 Flowise、LangChain，也不用开Node 项目。**4.1 NodeVM：一个安全可控的 JS 执行沙箱**我们基于 vm2（NodeVM）做了一个“可控的 JS 执行环境”。运行时基于 StructureToolNodeVM 作为安全隔离的执行环境自动注入企业内部能力（统一上下文能力层）
```
`/**`` * 核心思路抽象版`` */``import { NodeVM } from 'vm2'``import { StructuredTool } from '@langchain/core/tools'``//...````classDynamicToolextendsStructuredTool {``  constructor({ name, description, schema, code }) {``    super({ name, description, schema })``    this.code = code // 用户在在线编辑器里写的 JS 代码``  }````  async _call(args, runManager, flowContext) {``    // 1. 构建沙箱（所有注入能力都放在这里）``    const sandbox = {``      // 用户传入的参数转成 $xxx``      ...Object.fromEntries(Object.entries(args).map(([k, v]) => [`$${k}`, v])),````      // 内部上下文（cookie/env/session）``      $flow: flowContext,``      $cookie: flowContext.cookie,````      // 内网能力封装（gRPC/HTTP）``      $yuumi: yuumi,````      // 结果转换工具（用于把 JSON 转成更 AI 友好的 Markdown 表格）``      $json2MarkdownTable: json2MarkdownTable,````      // 内部 AI 模型``      $biliLLM: biliLLMClient``    }````    // 2. 构建 NodeVM 沙箱``    const vm = new NodeVM({``      sandbox,``      console: "inherit",``      require: {``        builtin: allowedBuiltinDeps,``        external: allowedExternalDeps``      }``    })````    // 3. 执行开发者写的云函数代码``    return await vm.run(``      `module.exports = async () => { ${this.code} }()`,``      __dirname``    )``  }``}`
```
它既能隔离风险，又能注入能力：禁止访问文件系统禁止随意 require只开放白名单依赖内置 $yuumi（内网 gRPC/HTTP 调用）内置 $json2MarkdownTable内置 $cookie内置 $flow（上下文）内置 内部 AI 能力于是开发者传入的业务代码类似这样：
```
`const res = await $yuumi.grpc({``  appId: 'live.service',``  path: '/room/info',``  params: { roomid: $roomid },``  cookie: $cookie,``})````return $json2MarkdownTable(res.data.list)`
```
**4.2 在线调试：monaco-editor****+ Mock****+ 沙箱日志**编辑器底层用的是 microsoft/monaco-editor，好处是：TypeScript / JS 语法高亮可以做一些简单的智能提示UI 很像 VSCode，大家上手成本低调试方面：提供了一个 参数 Mock 面板：可以填入调用时的 JSON点击「运行」，平台会在沙箱里跑一遍你的函数，把：日志打印（console.log）、返回字符串、可能的异常，全都展示出来每次保存，我们都会生成一个版本：当前编辑的是“草稿”发布的时候会把某个版本标记为发布出现问题可以一键回滚到上一版最后，开发者只需要在编辑器里写一个 “普通 JS 函数”，但：安全隔离由 NodeVM 负责内网调用靠 $yuumi会话靠 $cookieAI 友好的结果格式靠 $json2MarkdownTable**4.3 Tool Arguments：****为 AI 帮开发者“定义接口”**传统开发写接口参数：
```
`roomid: string
```
为此，我们提供了转为 Tool Arguments 的可视化配置：它会统一生成：MCP Tool 的 JSON SchemaStructuredTool 的 Zod SchemaNodeVM 内 $roomid 变量一次配置，全平台复用。**4.4 工具市场：企业内部的 Agent 工具仓库**我们提供了工具市场：各部门把工具上架其他部门直接复用工具行为一致，调用方式一致避免重复开发工具从“项目资产”变成“企业能力”。**五、第三版：接入 MCP****——****让工具跨平台、跨模型、跨框架**做到第二版时，工具已经变得很好用了。但还缺一块：同一份工具定义，既能在 Flowise 里当 LangChain StructuredTool 用，又能在 MCP 里变成跨平台 ToolCall。**5.1 MCP 是什么？以及一个常见误区**MCP 全称 Model Context Protocol，可以简单理解为：给“大模型 + 工具调用”定义了一个“统一插线板”它解决的是：大模型想调用一个外部工具这个工具可能跑在本机、另一台服务器、甚至另一个团队的系统里我们希望“调用方式”是统一、可描述、可流式的。**5.2 一个常见误区：把旧接口一包就行了？**很多人第一反应是：那我把现在的业务 HTTP 接口包成一个 MCP 工具，不就行了吗？理论上可以，实践里有两个坑：**1.  自然语言 ≠ 接口参数**用户会说：“查一下未完成的任务”。但你的接口长这样：/tasks?status=1&owner_id=xxx。中间这层 “自然语言 → status=1” 的映射，需要：prompt / few-shot枚举表 / 映射关系甚至分类模型。所以我们在 Tool Arguments 设置时一定要尽量贴近自然语言，比如 status 描述写成“任务的进度状态（未开始/进行中/已完成）”，而不是“1/2/3”。**2.  JSON 返回 ≠ AI 可读**很多内部接口返回一大坨嵌套 JSON，LLM 虽然能解析，但：容易“漏看”字段；回答会很啰嗦或不稳定。所以我们在云函数层统一规定：**返回给 AI 的一定是“人类可读”的文本/Markdown，**JSON 只是中间态。这就是前面 $json2MarkdownTable 那段代码存在的原因。**5.3 StructuredTool → MCP：****我们是怎么做“代理层”的？**前面说了两件事：工具在平台内部用 LangChain StructuredTool + NodeVM 来执行我们希望同一份工具定义，既能在 Flowise 里用，也能被任意支持 MCP 的 Agent / Studio 调用**createMCPServer：Express 里的一层 MCP 网关**在服务端，我们做了一层很薄的 MCP 网关，挂在 Express 应用上：export function createMCPServer({ app, AppDataSource }: App){``  // 单个云函数 → MCP-StreamableHTTP``  app.post('/api/mcp/function-tool/:toolId', singleToolCreateStreamableHTTPServer)``  // 多个云函数组合 → MCP-StreamableHTTP``  app.post('/api/mcp/:mcpId', multipleToolCreateStreamableHTTPServer)````  // 会话后续请求复用``  app.get('/api/mcp/function-tool/:id', handleSessionRequest)``  app.delete('/api/mcp/function-tool/:id', handleSessionRequest)``  app.get('/api/mcp/:mcpId', handleSessionRequest)``  app.delete('/api/mcp/:mcpId', handleSessionRequest)````  const transports = {``    streamable: {} as RecordStreamableHTTPServerTransport>``  }````  // ... 省略 SSE 相关 ...``}`
```
对外就是几条 HTTP 路由；对内维护一个 streamable 的 transport 池，用 sessionId 作为 key。这样，不同 AI Studio / Agent 只要知道某个 URL，就可以把它当 MCP 端点来用。**Streamable HTTP：用 session 管住一条“长连接”**StreamableHTTPServerTransport 是 MCP 官方 SDK 提供的一个传输实现，用来做 Streamable HTTP 模式。我们做的事情有两种情况：客户端第一次初始化（没有 sessionId）；之后所有请求都带上 mcp-session-id 头，复用之前的 session。核心代码大概是这样：
```
`async function createStreamableHTTP(config: CreateMcpServerConfig){``  const { req, res, username } = config``  const sessionId = req.headers['mcp-session-id'] as string | undefined``  let transport: StreamableHTTPServerTransport````  if (sessionId && transports.streamable[sessionId]) {``    // ① 有 sessionId，复用之前的 transport``    transport = transports.streamable[sessionId]``  } elseif (!sessionId && isInitializeRequest(req.body)) {``    // ② 首次初始化，请求体符合 MCP 初始化格式``    transport = new StreamableHTTPServerTransport({``      sessionIdGenerator: () => randomUUID(),``      onsessioninitialized: (sessionId) => {``        transports.streamable[sessionId] = transport``      }``    })````    // 连接关闭时清理掉这个 session``    transport.onclose = () => {``      if (transport.sessionId) {``        delete transports.streamable[transport.sessionId]``        opsLogger.info(`[Streamable] 删除sessionId: username=${username} sessionId=${transport.sessionId}`)``      }``    }````    const server = buildMcpServer({``      ...config,``      transport: 'streamable-http'``    })````    await server.connect(transport)``  } else {``    // 既不是初始化，又没有合法 sessionId：直接返回错误``    res.status(400).json({``      jsonrpc: '2.0',``      error: {``        code: -32000,``        message: 'Bad Request: No valid session ID provided'``      },``      id: null``    })``    return``  }````  await transport.handleRequest(req, res, req.body)``}`
```
配合一个统一的会话请求入口：
```
`async function handleSessionRequest(req: Request, res: Response){``  const sessionId = req.headers['mcp-session-id'] as string | undefined``  if (!sessionId || !transports.streamable[sessionId]) {``    res.status(400).send('Invalid or missing session ID')``    return``  }````  const transport = transports.streamable[sessionId]``  await transport.handleRequest(req, res)``}`
```
这样实现的好处是：客户端只需要记住一个 mcp-session-id，之后所有请求都可以复用同一条 Streamable HTTP 会话。**buildMcpServer：真正把“工具注册到 MCP 协议”**首先，用户可以将云函数平台创建的智能体工具代理到MCP协议上，一个MCP可以关联多个工具接下来是最关键的一步：用官方 McpServer 把 Tool Registry 里的工具挂成 MCP Tool。
```
`function buildMcpServer(config: BuildMcpServerConfig): McpServer {``  const { name, tools, cookie, env, id, type, username, transport } = config````  const server = new McpServer({``    name,``    version: '1.0.0'``  })````  for (const tool of tools) {``    // 1）把数据库里的元信息，转成 DynamicStructuredTool 入参``    const obj = {``      name: tool.name,``      description: tool.description,``      schema: z.object(convertSchemaToZod(tool.schema as string | object)),``      code: tool.func as string``    }````    // DynamicStructuredTool 内部就是一个“动态 StructuredTool” + NodeVM 沙箱``    const dynamicStructuredTool = new DynamicStructuredTool(obj)````    // Flow 信息：cookie + env（来自 MCP URL 上的 sign / 其它 query）``    dynamicStructuredTool.setFlowObject({``      cookie,``      env: typeof env === 'object' && Object.keys(env).length ? env : {}``    })````    // 2）把我们在 UI 里配置的 Tool Arguments schema，转成 MCP 需要的 zod 参数定义``    const schemaParser = (tool.schema ? JSON.parse(tool.schema) : []) as Schema[]````    const paramsSchema = schemaParser.reduce((res, cur) => {``      if (cur.required) {``        res[cur.property] = z[cur.type]({ required_error: `${cur.property} required` })``          .describe(cur.description) as z.ZodTypeAny``      } else {``        res[cur.property] = z[cur.type]()``          .describe(cur.description)``          .optional() as z.ZodTypeAny``      }``      return res``    }, {} as any)````    // 3）用官方 server.tool() 方法注册 MCP Tool``    server.tool(tool.name, tool.description, paramsSchema, async (args, _extra) => {``      // 注意：这里的 call() 对应的就是 LangChain StructuredTool._call()``      const runnerResult = await dynamicStructuredTool.call({``        ...args``      })````      // 线上环境做一层使用上报（方便统计谁在用哪个 MCP）``      if (process.env.DEPLOY_ENV === 'prod') {``        reportMcpUse({``          id,``          type,``          name,``          username,``          transport``        })``      }````      // MCP 协议统一的返回格式：content[] 数组``      return {``        content: [{ type: 'text', text: runnerResult }]``      }``    })``  }````  return server``}`
```
把Tool Registry 里的：namedescriptionschema（以数组 JSON 形式存）func（在线编辑器里的 JS 代码）按 MCP 需要的格式做了一层映射：输入 → paramsSchema（zod 校验）执行 → dynamicStructuredTool.call()输出 → MCP 标准的 content[{ type: 'text', text: ... }]StructuredTool 内部：从 MCP 入参到 NodeVM 执行的最后一步DynamicStructuredTool.call() 里面最终会走到 _call()，这一步就是前面介绍的 NodeVM 沙箱执行：把 MCP 传进来的参数变成 $xxx 变量把 cookie / env、以及会话信息塞进 $flow注入 $yuumi、$json2MarkdownTable、$biliIndex、$deepseek、$chatgpt 等能力在受限依赖白名单下创建 NodeVM以 module.exports = async function() { ${this.code} }() 的形式执行开发者写的 JS对于上层 MCP 调用方来说：调用了一个名字叫 QueryLiveRoomInfo 的 MCP 工具，传了一些参数，收到了一个文本/Markdown 结果而对于我们平台来说，这中间其实已经执行了一整套：MCP → McpServer.tool → DynamicStructuredTool → NodeVM → 内网服务的完整链路。**可复用可共享的MCP市场**对于 MCP 新手，我们在平台上还提供了“MCP 市场” 的入口，里面还提供了一键调试：不需要真的连上一个大模型直接在浏览器里模拟一次 MCP ToolCall看看云函数有没有跑对、返回是不是 AI 友好的格式**六、身份鉴权：MCP 是独立服务，****安全必须先想清楚**MCP 本质上是一个“跨平台的服务访问入口”，如果不做鉴权，很容易变成无法管理。我们的做法大致是这样：1.  注册阶段就要带 sign：每个 MCP 工具的注册地址必须带一个 sign 参数sign 是基于内网规范签出的签名没有合法签名，工具不会被注册成功2.  调用阶段统一 Proxy：外部 Agent 调用 MCP ServerMCP Server 把调用转发给云函数平台的 Proxy 层Proxy 层会：校验 sign注入对应的 $cookie / 会话再去调真正的内网业务接口3.  业务侧拿到的是“处理后的内网协议”：Proxy 会把 sign 解密、校验后，以内部统一格式透传给业务避免在业务里掺杂各种外部协议细节这样，MCP 既可以对外暴露统一的工具接口，又仍然受控在内网的安全体系内**七、结语：把“接 AI”变成“写一个云函数”**从 AI工作流 → StructuredTool → 云函数平台 → MCP 的这条路径，我们最终得到了：一个统一的工具定义方式：元信息一个统一的执行方式：NodeVM一个统一的调用协议：MCP一个统一的共享方式：工具市场一个统一的安全体系：sign + cookie也让我们真正做到了：让业务同学不再关心“怎么接 AI”，而是只需要关心“我能给 AI 提供什么能力”。把写一个 JS 函数，变成给 AI 加一个新能力。未来我们还会继续提升运行时性能、正确性评估观测、深度研究等方向，把工具能力建设得更现代、更企业级。-End-作者丨Zerooo、Gengar开发者问答**

**在你们团队做 AI 应用时，最困扰你的一件事是什么？**

欢迎在留言区分享你的经历~

转发本文至朋友圈并留言，即可参与**下方抽奖****⬇️**

小编将抽取1位幸运的小伙伴获取**星星向龙系列卡套包**

**抽奖截止时间：12月19日12:00**

如果喜欢本期内容的话，欢迎点个“在看”吧！

**往期精彩指路**

- B站社群AI智能分析系统的实践
- 面向AI应用开发实战分享 - 基础篇
- B站AI计算网络建设实践

[通用工程](https://mp.weixin.qq.com/mp/appmsgalbum?__biz=Mzg3Njc0NTgwMg==&action=getalbum&album_id=3289447926347317252#wechat_redirect)丨[大前端](https://mp.weixin.qq.com/mp/appmsgalbum?__biz=Mzg3Njc0NTgwMg==&action=getalbum&album_id=2390333109742534656#wechat_redirect)丨[业务线](https://mp.weixin.qq.com/mp/appmsgalbum?__biz=Mzg3Njc0NTgwMg==&action=getalbum&album_id=3297757408550699008#wechat_redirect)

[大数据](https://mp.weixin.qq.com/mp/appmsgalbum?__biz=Mzg3Njc0NTgwMg==&action=getalbum&album_id=2329861166598127619#wechat_redirect)丨[AI](https://mp.weixin.qq.com/mp/appmsgalbum?__biz=Mzg3Njc0NTgwMg==&action=getalbum&album_id=2782124818895699969#wechat_redirect)丨[多媒体](https://mp.weixin.qq.com/mp/appmsgalbum?__biz=Mzg3Njc0NTgwMg==&action=getalbum&album_id=2532608330440081409#wechat_redirect)

[阅读原文](2247503836)

[跳转微信打开](https://wechat2rss.xlab.app/link-proxy/?k=c0cd161d&r=1&u=https%3A%2F%2Fmp.weixin.qq.com%2Fs%3F__biz%3DMzg3Njc0NTgwMg%3D%3D%26mid%3D2247503836%26idx%3D1%26sn%3Dd84b2e1c6ce9330751cd4d58b3ec32ef)
