# Concept 校验规则

> 协议层第二项——什么算「完成」、什么算「不合格」。
> 每条规则有明确判断标准，不依赖主观感受。

---

## Gate 校验清单

Concept 必须通过以下全部检查才算合规：

### F1. type 不为空

```
✅ type: Article
❌ type:（缺失或空字符串）
```

### F2. description 不为空且非复述标题

```
✅ description: AI 出码快但整体效率没跟上——三个根因与 Harness 方案
❌ description: 开启Harness Engineering探索之旅（← 等于标题）
❌ description:（空）
```

### F3. timestamp 符合 ISO 8601

```
✅ timestamp: 2026-06-29T00:00:00+08:00
❌ timestamp: 2026-06-29
❌ timestamp: 2026/06/29
```

### F4. tags 全部小写英文、无空格

```
✅ tags: [harness-engineering, methodology, engineering]
❌ tags: [Harness Engineering, 方法论]
❌ tags: [harness engineering]
❌ tags: []
```

### F5. 适用场景不为空，≥3 条

```
✅ 3-5 条具体场景
❌ 0 条（空）
❌ 1 条（太少，无法覆盖主要用例）
⚠️  2 条（警告，不阻断）
```

### F6. 关联概念不为空，链接指向存在的文件

```
✅ 每条包含文件名链接 + 说明
❌ 空
⚠️  链接指向不存在的文件（不阻断，标 warning——允许新文章还没入库）
```

### F7. 关键引用 ≥1 条

```
✅ ≥1 条 > 引用
❌ 0 条
```

---

## Delta Spec 变更标记

当 Concept 被修改时，必须在 `knowledge/log.md` 中记录变更，使用以下标记：

| 标记 | 含义 | 示例 |
|------|------|------|
| `**Update**` | 修改了现有字段或段落内容 | `**Update**: harness-engineering.md — 补充了 SpecWorker 对比` |
| `**Addition**` | 新增字段或段落 | `**Addition**: 补充关联概念——连接 skill-as-algorithm.md` |
| `**Deprecation**` | 标记为过时（不删除） | `**Deprecation**: 旧版 token 策略——已被 five-yuan-token.md 替代` |

---

## 合规等级

| 结果 | 条件 | 含义 |
|------|------|------|
| ✅ PASS | F1-F7 全部通过 | Concept 可发布 |
| ⚠️ WARN | F1-F4 通过，F5-F7 有 warning | 可发布但建议完善 |
| ❌ FAIL | 任一 F1-F4 不通过 | 不可发布，必须修正 |

---

## 现有 19 篇 Concept 对照

以 harness-engineering.md 为例，逐项对照：

| 检查项 | 状态 | 
|--------|------|
| F1 type | ✅ `Article` |
| F2 description | ✅ 「AI 出码快但整体节奏没跟上——三个根因与 Harness 工程化方案」|
| F3 timestamp | ✅ `2026-06-29T00:00:00+08:00` |
| F4 tags | ✅ `[harness-engineering, methodology, engineering]` |
| F5 适用场景 | ✅ 4 条 |
| F6 关联概念 | ✅ 3 条，链接均有效 |
| F7 关键引用 | ✅ 2 条 |

结论：这 19 篇已经符合规范。新入库的 Concept 以此为基准。
