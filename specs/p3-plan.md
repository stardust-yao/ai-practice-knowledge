# P3 实现计划

> 按文章 P3 方法：状态文件驱动 + D-x 逐个派子 Agent + code-reviewer 三档 Gate。
> 每个 D-x 完成后对照 `design.md` 契约 review，Critical 阻断。

---

## 状态文件 (`p3-state.json`)

```json
{
  "phase": "p3",
  "d_list": [
    {"id": "D-1", "desc": "knowledge/.state.json", "status": "pending", "agent": null, "review": null},
    {"id": "D-2", "desc": "module 字段", "status": "pending", "agent": null, "review": null},
    {"id": "D-3", "desc": "Gate 校验脚本", "status": "pending", "agent": null, "review": null},
    {"id": "D-4", "desc": "去掉筛选豁免", "status": "pending", "agent": null, "review": null},
    {"id": "D-5", "desc": "中间草稿 + 超时回退", "status": "pending", "agent": null, "review": null},
    {"id": "D-6", "desc": "反向索引脚本", "status": "pending", "agent": null, "review": null},
    {"id": "D-7", "desc": "向量索引脚本", "status": "pending", "agent": null, "review": null},
    {"id": "D-8", "desc": "module 字段回填 19 篇", "status": "pending", "agent": null, "review": null}
  ]
}
```

---

## 执行流程

```
D-x START
    │
    ▼
git checkout -b p3/D-x（独立分支）
    │
    ▼
派 SpecWorker-Dx SubAgent（独立上下文）
    │
    ▼
输出改动 → 提交到 p3/D-x 分支
    │
    ▼
code-reviewer 对照 design.md 契约 review → 三档
    │
    ├── 0 Critical → PR → merge to main → ✅ D-x DONE
    └── >0 Critical → 返回 SubAgent 在分支上修正（最多 3 轮）
```

---

## 依赖关系与分组

```
D-1 (.state.json) ────┐
D-2 (module 字段) ────┤  独立，可并行
D-3 (Gate 脚本) ──────┤
D-4 (去豁免) ─────────┘
        │
        ▼
D-5 (草稿+超时) ────── 依赖 D-1（需要 .state.json 格式）
        │
        ▼
D-6 (反向索引) ───────┐
D-7 (向量索引) ───────┤  依赖 D-3（需要 Gate 脚本框架）
        │
        ▼
D-8 (回填 module) ──── 依赖 D-2（需要 module 字段定义）
```

---

## code-reviewer 三档标准

| 级别 | 标准 | 处置 |
|------|------|------|
| **Critical** | 与 design.md 契约不一致 / 破坏性变更 / 语法错误 | 阻断，返回修正 |
| **Important** | 实现方式偏离但可接受 / 遗漏边界处理 | 标记，写入 evaluation 日志 |
| **Suggestion** | 命名、注释、代码风格 | 自由处置，不阻断 |
