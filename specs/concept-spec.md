# Concept 校验规则

> 协议层第二项——什么算「完成」、什么算「不合格」。
> 每条规则有明确判断标准，不依赖主观感受。

---

## Gate 校验清单

Concept 必须通过以下全部检查才算合规。FAIL 为阻断，WARN 可发布但标注 TODO。

### F1. type 不为空

```
✅ type: Article
❌ type:（缺失或空字符串）
```
级别: **FAIL**

### F2. title 不为空

```
✅ title: 开启 Harness Engineering 探索之旅
❌ title:（缺失或空字符串）
```
级别: **FAIL**

### F3. description 不为空

```
✅ description: AI 出码快但整体效率没跟上——三个根因与 Harness 方案
❌ description:（空）
```
级别: **WARN**

### F4. module 不为空且在 8 模块内

```
✅ module: project-arch
❌ module:（缺失或空字符串）
❌ module: 随便写的（不在白名单内）
```

白名单: `project-arch` / `skill-design` / `tools-integration` / `memory-knowledge` / `safety-guardrails` / `eval-testing` / `cost-performance` / `fundamentals`

级别: **FAIL**

### F5. date 符合 YYYY-MM-DD

```
✅ date: 2026-06-29
❌ date: 2026/06/29
❌ date:（缺失）
```
级别: **FAIL**

### F6. source 不为空

```
✅ source: raw/2026-06/2026-06-29_标题.md
❌ source:（缺失或空字符串）
```
级别: **FAIL**

### F7. tags 不为空、全小写英文、≥3 个

```
✅ tags: [harness-engineering, methodology, engineering]
❌ tags: [Harness Engineering, 方法论]
❌ tags: [harness]
❌ tags: []
```
级别: **FAIL**

### F8. timestamp 符合 ISO 8601

```
✅ timestamp: 2026-06-29T00:00:00+08:00
❌ timestamp: 2026-06-29
❌ timestamp:（缺失）
```
级别: **FAIL**

### F9. 适用场景 ≥3 条

```
✅ 3-5 条具体场景
⚠️  2 条（警告，不阻断）
❌ 0-1 条
```
级别: **WARN**

### F10. 关联概念 ≥1 条

```
✅ 每条包含文件名链接 + 说明
⚠️  链接指向不存在的文件（不阻断）
❌ 0 条
```
级别: **WARN**

### F11. 关键引用 ≥1 条

```
✅ ≥1 条 > 引用
❌ 0 条
```
级别: **WARN**

---

## 合规等级

| 结果 | 条件 | 含义 |
|------|------|------|
| ✅ PASS | F1-F11 全部通过 | Concept 可发布 |
| ⚠️ WARN | F1-F8 全部通过，F3/F9/F10/F11 有 warning | 可发布但建议完善 |
| ❌ FAIL | 任一 F1/F2/F4/F5/F6/F7/F8 不通过 | 不可发布，必须修正 |

---

## Delta Spec 变更标记

当 Concept 被修改时，必须在 `knowledge/log.md` 中记录变更，使用以下标记：

| 标记 | 含义 | 示例 |
|------|------|------|
| `**Update**` | 修改了现有字段或段落内容 | `**Update**: harness-engineering.md — 补充了 SpecWorker 对比` |
| `**Addition**` | 新增字段或段落 | `**Addition**: 补充关联概念——连接 skill-as-algorithm.md` |
| `**Deprecation**` | 标记为过时（不删除） | `**Deprecation**: 旧版 token 策略——已被 five-yuan-token.md 替代` |
