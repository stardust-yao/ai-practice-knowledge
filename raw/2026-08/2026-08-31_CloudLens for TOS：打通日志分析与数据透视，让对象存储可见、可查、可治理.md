---
title: CloudLens for TOS：打通日志分析与数据透视，让对象存储可见、可查、可治理
date: 2026-08-31
source: https://mp.weixin.qq.com/s?__biz=MzI1MzYzMjE0MQ==&amp;mid=2247521877&amp;idx=1&amp;sn=0a0633b5daac6e93db59009212cb3e93
account: 字节跳动技术团队
fetched_at: 2026-09-01 18:00:04 CST
article_id: 0a0633b5daac6e93db59009212cb3e93
---

火山引擎存储 2026-08-31 19:00 北京

  
  
*[图片]*

  
  
**从“存得下”到“看得清”**

对象存储 TOS 正在承载日志归档、音视频素材、备份文件、数据湖和 AI 数据集等越来越多的核心数据。随着存储桶（Bucket）数量、对象规模和目录层级持续增长，团队面对的问题也从“容量是否够用”，转变为更具体的运营与治理问题：

- 流量或请求突然升高，究竟来自哪个存储桶、客户端或对象？
- 错误请求集中在什么时间、状态码和操作类型？
- 容量增长发生在哪个地域、存储类型、Bucket 或前缀（Prefix）？
- 历史版本和未合并分片占用了多少空间，应该优先治理哪里？

CloudLens for TOS 是日志服务 TLS 与对象存储联合推出的 TOS 日志观测应用，将 TOS  API 请求访问行为与存储资产纳入同一套观测框架。访问日志分析，还原 TOS API 请求访问，回答“发生什么、有哪些洞察”的问题；数据透视，沉淀按天统计的存储资产多维快照，回答“数据长期如何分布和变化”的问题。两者共同将 TOS 从“黑盒”转变为可查询、可分析、可治理。

访问日志分析适合实时排障、访问分析和安全审计；数据透视适合容量规划、成本优化和资产治理，两类能力互为补充。

**日志分析：TOS API 请求，发生了什么？**

TOS Bucket 开启日志分析后，会将 TOS API 访问日志写入日志服务 TLS。CloudLens for TOS 在这些明细日志之上提供资源用量、热度统计、访问分析、安全分析和检索分析五个视角，让团队能从全局趋势逐步下钻到单次请求。

- **流量与请求是否异常：**同时观察读写流量、请求数及 Bucket TopN，快速判断突增来自哪个存储桶。
- **谁在访问、访问了什么：**通过 PV、UV、客户端 IP、Referer 和热点对象，识别主要访问主体与内容。
- **高风险操作是否可追溯：**聚焦删除、覆盖写和分片上传等敏感操作，定位来源 IP 与访问身份。
- **异常请求如何还原：**从聚合图表下钻到原始日志，结合状态码、错误码和 RequestId 复原单次请求。

**资源用量：先看清流量和请求的全局走势**

资源用量监控提供资源概览，主要覆盖以下指标：

- 读流量、写流量、总流量以及读请求、写请求、总请求的时间趋势。
- 存储桶流量 / 带宽 Top1000 和请求 Top1000。出现突增时，先确认异常时间窗口，再快速定位主要贡献 Bucket。

*[图片]*

**热度统计：快速找到访问热度最高的目录**

热度统计监控便于快速定位热点目录。

- 按操作类型分析访问热点：展示各类 Operation 的请求占比，如 HeadObject、GetObject、PutObject、DeleteObject 等，用于判断主要访问行为和异常操作类型。
- 按对象大小分析访问分布：统计不同对象大小区间的访问占比，如小于 4KB、8MB～32MB、大于 128MB 等，用于识别热点访问主要集中在小文件还是大文件。
- 按目录聚合访问热度：以目录为维度汇总请求数、请求 QPS、响应流量和访问对象大小，快速识别热点目录。
- 支持目录下钻分析：目录名称可点击，支持逐层下钻进入子目录，查看更细粒度的访问分布。

*[图片]*

*[图片]*

**访问分析：理解谁在访问、访问了什么**

- 访问分析覆盖上传数据量、下载数据量、删除数据量、PV、UV 等核心指标。
- 提供客户端 IP、Referer、文件访问、上传 / 下载 / 删除数据量 Top1000。
- 配合状态码趋势和错误访问次数，判断异常来自访问主体、热点对象还是服务端错误。

*[图片]*

**安全分析：高风险操作有迹可循**

- 安全分析聚焦 DeleteObject、PostObject、AppendObject、UploadPart、CopyObject、ListObjects、CreateMultipartUpload、CompleteMultipartUpload 等操作，统计关注操作的增长趋势。
- 文件操作趋势、删除文件统计、来源 IP 和删除趋势共同回答“谁在什么时间，删除了哪些数据”，方便业务定位危险操作。

*[图片]*

**检索分析：还原 TOS API 请求记录**

仪表盘用于发现异常和统计特征，检索分析则可真实还原 TOS API 请求记录。基于 TLS 提供的检索和分析能力，用户可以：

- 灵活查询与追踪请求记录：按时间范围、Bucket、对象、操作、状态码、来源 IP 和访问身份检索原始日志，查看 RequestId、CostTime、DeltaDataSize 等字段，完成请求级追踪。
- 自定义统计分析请求访问：按时间、操作类型、状态码、访问 IP、Bucket、存储类型等维度，灵活统计分析操作分布、来源热点 IP 等信息。

*[图片]*

**一键接入 Agent，智能诊断分析**

开启日志分析后，可通过 **TLS CLI**（[https://docs.volcengine.com/docs/6470/2559490?lang=zh）](https://docs.volcengine.com/docs/6470/2559490?lang=zh）)让 Agent 访问 TLS 中的 TOS API 请求访问日志，对访问记录进行智能诊断分析。

一键安装 TLS CLI，详情可参考： **TLS CLI 安装与使用说明**（[https://docs.volcengine.com/docs/6470/2559491?lang=zh）](https://docs.volcengine.com/docs/6470/2559491?lang=zh）)

AI Agent 版：

```
npm install -g @volcengine-tls/volclog@latest --registry https://registry.npmjs.org/
```

**分析示例：**查询存储桶一天内的存储容量变化

```
`volclog --profile default tool exec log.search \`
`  --input '{`
`    "TopicId": "a0319c42-cdce-4a0a-87de-aa9a23388c91",`
`    "Query": "Bucket: archive-sy-shipper AND NOT Operation: \"BatchDeleteDetails\" | SELECT SUM(DeltaDataSize) / 1024.0/1024/1024 AS `总存储量变化(GB)`",`
`    "StartTime": 1786846906294,`
`    "EndTime": 1786933306295,`
`    "Limit": 20`
`  }'`

```

执行结果：可以看到总存储量变化（GB）为395.2。

```
`{`
`  "action": "tool.log.search",`
`  "artifacts": [],`
`  "contract_digest": {`
`    "policy": "soft",`
`    "value": "bda1a39bd021e0a22a52ff73d1c621a450665372d4ebb2b7c2e5f74973e91c83"`
`  },`
`  "data": {`
`    "Analysis": true,`
`    "AnalysisResult": {`
`      "Data": [`
`        {`
`          "总存储量变化(GB)": "395.2"`
`        }`
`      ],`
`      "Schema": [`
`        "总存储量变化(GB)"`
`      ],`
`      "Type": {`
`        "总存储量变化(GB)": "double"`
`      }`
`    },`
`    "Context": "",`
`    "Count": 1,`
`    "ElapsedMillisecond": 42,`
`    "HitCount": 1,`
`    "Limit": 100,`
`    "ListOver": true,`
`    "Logs": [],`
`    "ResultStatus": "complete"`
`  },`
`  "error": null,`
`  "requestId": "9261c8d379514054b1912e67f51b124b-ac13786f",`
`  "status": "success",`
`  "summary": {`
`    "deliveryMode": "stdout",`
`    "dryRun": false,`
`    "itemCount": 0,`
`    "outputMode": "stdout",`
`    "totalBytes": 751`
`  }`
`}`

```

**数据透视：数据都存在哪里，资产如何分布？**

数据透视按天统计 TOS 资产，支持从区域、存储类型、存储桶和前缀等维度分析总存储量、对象数量、当前版本、历史版本和未合并分片。数据透视不关注单次请求，而是帮助团队理解容量结构、增长趋势与治理优先级。

- **整体资产水位：**概览页汇总对象数量、总存储量、平均对象大小与 Bucket 数量，掌握当前资产规模。
- **地域容量是否集中：**对比不同 Region 的趋势和分布，为跨地域容量规划和治理排序提供依据。
- **存储分层是否合理：**比较标准、低频、归档和冷归档数据，发现应降冷但仍留在高成本层的数据。
- **治理应从哪里开始：**通过 Bucket 与前缀 TopN，将容量增长定位到具体存储桶和业务目录。
- **成本是如何分布：**量化历史版本和未合并分片占用，支撑生命周期与清理策略。

**概览：掌握规模、趋势与热点**

- **指标明细：**集中展示总存储量、总对象数量、当前版本 / 历史版本、未合并的分片上传对象数和字节数。
- **趋势分布：**观察近期变化，并按地域和存储类型拆解资产结构。
- **热点定位：**通过前缀 TopN 与增量榜单找到占用最大、增长最快的目录。

*[图片]*

**地域视角：识别容量集中度与区域差异**

- **趋势对比：**查看不同 Region 的指标变化趋势与当日分布。
- **多指标分析：**通过气泡图同时比较容量、对象数量等指标。
- **规划用途：**识别容量集中度和区域差异，辅助跨地域容量规划，可从摘要指标、成本优化指标和数据保护指标多角度分析。

*[图片]*

**存储类型视角：验证分层策略是否合理**

- **趋势分布：**比较各存储类型的容量趋势、当日分布和对象数量。
- **策略校验：**检查长期不访问的数据是否仍停留在标准存储层。
- **风险识别：**发现热数据误归档及生命周期策略未生效的问题。

*[图片]*

**存储桶视角：找到最值得优先治理的 Bucket**

- **排名趋势：**通过 Bucket TopN 和容量分布识别重点存储桶。
- **多指标比较：**使用气泡图同时观察容量、对象数量和成本优化指标。
- **治理判断：**区分“大容量少对象”与“容量不大、但对象极多”等形态。

*[图片]*

**前缀视角：把容量增长定位到具体目录**

- 启用高级功能后，可以按照前缀聚合指标。
- 前缀页展示趋势、分布、气泡图和 TopN 明细，将“某个 Bucket 在增长”进一步细化为“哪个业务目录在增长”，适合多租户或多业务共用 Bucket 的场景。

*[图片]*

**典型场景：从异常发现到治理行动**

**访问日志分析**

- **推荐场景**

- **日常运维与故障排查：**快速确认流量、请求和状态码异常发生的时间与 Bucket。
- **热点识别与访问优化：**分析客户端 IP、Referer、热点对象及下载流量，优化访问路径和缓存策略。
- **错误根因定位：**按 ErrorCode、HTTPStatus、Operation 和 RequestId 下钻原始日志。
- **安全审计：**追踪删除、覆盖写、分片上传等高风险操作的来源和身份。
- **近实时容量变化分析：**通过 DeltaDataSize 和 HistoricalVersionDeltaSize 计算请求引起的容量变化。

- **举例**

- **找到 QPS 突增的请求**

```
`Bucket: * | SELECT`
`          "Operation" AS Action,`
`          COUNT(*) AS `请求次数`, `
`          HTTPStatus AS `响应码`,`
`          COUNT(*) * 100.0 / NULLIF(SUM(COUNT(*)) OVER (), 0) AS `请求占比(%)``
`        WHERE "Operation" IS NOT NULL AND "Operation" <> '-'`
`        GROUP BY "Action", `响应码``
`        ORDER BY `请求次数` DESC`
`        LIMIT 50`

```

预期输出：可以看到该时间段内请求最多的是 HeadObject。

*[图片]*

还可以通过 SQL 查找 QPS 最高的请求以及出现的时间点。

```
`Bucket: *`
`|SELECT`
`    Action,`
`    ROUND(minute_request_count /60.0, 4) AS `请求峰值QPS`,`
`    time_minute AS `峰值出现时间``
`  FROM (`
`    SELECT`
`      Action,`
`      time_minute,`
`      minute_request_count,`
`      ROW_NUMBER() OVER (`
`        PARTITIONBY Action`
`        ORDERBY minute_request_count DESC, time_minute DESC`
`      ) AS rn`
`    FROM (`
`      SELECT`
`        "Operation" AS Action,`
`        DATE_TRUNC('minute', __time__) AS time_minute,`
`        COUNT(*) AS minute_request_count`
`      WHERE "Operation" ISNOTNULL`
`        AND "Operation" <>'-'`
`      GROUPBY "Operation", DATE_TRUNC('minute', __time__)`
`    ) minute_metrics`
`  ) ranked`
`  WHERE rn =1`
`  ORDERBY `请求峰值QPS` DESC`
`  LIMIT 50`

```

*[图片]*

- **查询访问量前 100 的对象**

```
`Bucket: *AND (Operation: "GetObject" OR Operation: "HeadObject") |SELECT`
`    Object AS `文件名`,`
`    Bucket AS `存储桶`,`
`    COUNT(*) AS PV`
`    GROUPBY Object, Bucket`
`ORDERBY PV DESC`
`LIMIT 100`

```

预期输出：

*[图片]*

- **查询客户端访问 Top100**

```
`Bucket: *|SELECT`
`    RemoteIp AS `客户端IP`,`
`    Bucket AS `存储桶`,`
`    COUNT(*) AS PV`
`  GROUPBY RemoteIp, Bucket `
`  ORDERBY PV DESC`
`  LIMIT 100`

```

预期输出：

*[图片]*

- **查询错误请求 API 分布**

```
`Bucket: *and HTTPStatus: >400|SELECT`
`    Operation AS `操作`,`
`    Bucket AS `存储桶`,`
`    COUNT(*) AS `出现次数``
`  GROUPBY Operation, Bucket `
`  ORDERBY `出现次数` DESC`

```

预期输出：

*[图片]*

**数据透视**

**推荐场景**

- **容量规划：**观察存储量和对象数量的长期增长趋势，判断容量是否符合业务预期。
- **成本优化：**找出存储量最大的 Bucket 或前缀，优先治理主要成本来源。
- **存储分层：**分析各存储类型的容量分布，评估标准、低频和归档数据的分层策略。
- **历史版本治理：**定位历史版本字节数较大的 Bucket，配置生命周期删除或降冷策略。
- **未合并分片治理：**发现长期未完成的分片上传，减少无效存储成本。
- **多业务共用 Bucket 治理：**通过前缀聚合，识别具体业务目录的容量与对象增长情况。

**举例**

- **找到 Bucket 内最大的前缀目录**

选择“总存储量”，默认 Top4，可以看到，parquet-tls-sy-shipper 这个 Bucket 的最大前缀是300个shard大流量写入。

*[图片]*

- **找到存储量最大的 Bucket**

选择“概览→快照 TopN→存储桶”，指标选择“总存储量”，可以看到最大的 Bucket 是 parquet-tls-sy-shipper。

*[图片]*

- **减少历史版本对象数量**

如果存储桶开启了版本控制，删除或覆盖数据时，TOS 会自动保存历史版本，可能累积大量历史版本对象，导致存储成本增加。可通过数据透视看板找出历史版本字节数较多的存储桶，再进行针对性清理。

*[图片]*

**一键接入：统一管理日志分析与数据透视**

CloudLens for TOS 目前已提供双入口，既可以在 TOS 控制台接入，也可以在 TLS 控制台接入，只需要接入一次即可，接入后按需分别开启日志分析和数据透视任务。

**TOS 控制台开通**

登录 TOS 控制台，选择“数据洞察”，点击“开通及授权”，完成授权后即可开通。

*[图片]*

开通后，即可看到日志分析与数据透视。

*[图片]*

**TLS 控制台开通**

进入 TLS 控制台，选择“日志应用 → 应用市场” ，搜索 “TOS” ，找到  CloudLens for TOS，点击“接入应用”，按提示完成授权后即可开通。

*[图片]*

开通后，即可看到日志分析与数据透视。

*[图片]*

**日志分析接入**

在**“日志分析 → 看板配置”**中，可按存储桶查看地域与接入状态，通过开关启用或停用日志分析，并直接进入对应分析页。

- **按 Bucket 开启：**在看板配置中搜索“目标存储桶”，并打开日志分析开关。开启后，系统会自动创建用于存放 TOS 访问日志的日志项目、主题及索引。
- **进入分析：**点击“去分析”，即可使用资源用量、访问分析、安全分析与检索分析看板。

*[图片]*

**数据透视接入**

数据透视通过任务方式接入。创建任务时，需要一次性确定任务名称、存储地域与指标采集方式，并选择纳入统计的区域和存储桶。

- **基础配置：**填写任务名称并选择地域。任务创建后，名称和地域不可修改，应使用可长期识别的命名方式。这里的地域指存储数据透视结果的 Region，不同区域的 Bucket 会汇总到此 Region。
- **选择采集方式：**普通模式采集基础指标；高级模式在基础指标之外，还提供活动指标及前缀分析能力，支持指定前缀或前缀阈值和深度。
- **选择覆盖范围：**支持按“包含”或“排除”方式选择区域和 Bucket。若选择“全部”时，即便后续新增 Bucket 也会动态生效。
- **导出指标：**检查 TOS 读写与 KMS 授权状态；如需在自有工具中继续分析，可开启指标导出，系统会每天导出一份数据到指定 Bucket。

*[图片]*

创建任务后，一般次日才能看到数据统计结果，统计维度按天聚合。

*[图片]*

- 初次开通 CloudLens for TOS，系统会默认创建一个名为 default-account-dashboard 的面板，该面板提供基础指标能力，包含用户所有的 Bucket，无需配置，且完全免费。

- 使用高级功能的前缀能力时，会引入 Table Topic 来存储桶的对象元数据信息，该功能目前限时免费。

**结语**

TOS 规模越大，越不能只依赖一张容量曲线图。CloudLens for TOS 以日志分析还原每一次请求，以数据透视描绘长期资产分布，让团队能够从异常发现走向请求定位，从容量统计走向目录级治理，并最终把可观测数据转化为稳定性、安全和成本优化行动。

**看见访问，理解数据，持续治理。**这正是 CloudLens for TOS 希望为对象存储带来的改变。

[阅读原文](https://www.volcengine.com/product/tls?_vtm_=a441938.b75322.0_0.0_0.0.160_7672313759130093108)

[跳转微信打开](https://wechat2rss.xlab.app/link-proxy/?k=9cb5f767&r=1&u=https%3A%2F%2Fmp.weixin.qq.com%2Fs%3F__biz%3DMzI1MzYzMjE0MQ%3D%3D%26mid%3D2247521877%26idx%3D1%26sn%3D0a0633b5daac6e93db59009212cb3e93)
