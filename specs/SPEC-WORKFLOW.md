# Spec 工作流 · SPEC-WORKFLOW

> 规范 spec 文档从撰写到入库的完整流程。核心原则：不通过 lint 不能提交，提交时同步更新 glossary。

---

## 1. 流程总览

```
写/改 spec
    │
    ▼
┌─────────────┐     FAIL/WARN     ┌──────────────┐
│ spec-lint.py │ ─────────────────▶│ 修复违规      │
└─────────────┘                   └──────┬───────┘
    │ PASS                              │
    ▼                                   ▼
┌─────────────┐                  重新跑 lint
│ git add +   │
│ git commit  │
└──────┬──────┘
       │
       ▼
┌─────────────────────────┐
│ 提交时检查：              │
│ • 有新术语？→ 更新 glossary│
│ • 改了术语定义？→ 检查引用者│
│ • 改了 Gate 规则？→ 更新 AC │
└─────────────────────────┘
```

---

## 2. 具体步骤

### Step 1: 写 spec（按模板）

使用 `specs/spec-template.md` 规定的 5 节结构：
1. 标题 + 摘要
2. **术语引用** — 核心术语链接 `glossary.md`，不自行定义
3. 规范正文
4. 变更记录

### Step 2: 跑 lint（阻断条件）

```bash
cd 腾讯工程实践学习/
python3 scripts/spec-lint.py
```

- 退出码 0 → 通过，可提交
- 退出码 1 → 有 WARN，建议修复但不阻断
- 退出码 2 → 有 ERROR，必须修复后才能提交

**pre-commit hook 已自动运行**，不需要手动触发。

### Step 3: 更新 glossary（如需要）

| 场景 | 动作 |
|------|------|
| spec 中引入新术语 | 追加到 `glossary.md` 对应分类下 |
| 修改了现有术语的定义 | 跑 `spec-lint.py` 检查所有引用者是否受影响 |
| 术语被废弃 | 在 glossary 中标记 `[已废弃]` 但保留条目（不删除） |

### Step 4: 更新关联文档

| 改了哪个 spec | 需要检查的联动文档 |
|--------------|-------------------|
| requirements.md | test-cases.md（AC 变更 → TC 同步） |
| concept-gate.md | design.md、requirements.md AC-4（Gate 级别变更 → 引用方更新） |
| concept-template.md | validate_concept.py、concept-gate.md |
| glossary.md | 所有 spec（术语定义变更 → 全局影响） |

### Step 5: 提交

```bash
git add specs/ glossary.md
git commit -m "spec: [改动描述]"
```

---

## 3. 矛盾修复追踪

以下为 Module 1 审计发现的 6 个矛盾案例修复状态：

| # | 矛盾 | 状态 | 修复方式 |
|---|------|------|---------|
| 1 | Gate F2/F5/F6/F7 级别 (design.md vs concept-spec.md) | ✅ 已修复 | design.md 两处统一为 F1-F11 引用 concept-spec.md |
| 2 | Gate 条目数 (requirements.md/test-cases.md 仍写 F1-F7) | ✅ 已修复 | 更新为 F1-F11 |
| 3 | 知识库分类 (IDEA.md/PROJECT.md 说 methods/tools/cases) | 🔜 下次 | 非 spec 文件，不影响 lint |
| 4 | PROJECT.md 数据过期 (20 篇 vs 实际 223 篇) | 🔜 下次 | 运行时数据，按需更新 |
| 5 | description "必填"歧义 (template vs Gate) | ✅ 已修复 | glossary.md 明确定义"必填"双重含义 |
| 6 | tags 格式模糊 (逗号分隔 vs YAML 数组) | ✅ 已修复 | glossary.md 明确指定 YAML 数组格式 |

**已修复 4/6。** 剩余 2 个为非 spec 文档的数据同步问题，不阻塞 lint。

---

## 4. 维护规则

- **spec 修改频率低时**（≤1 次/周）：每次改 spec 手动跑一遍流程
- **spec 修改频繁时**：pre-commit hook 自动跑 lint，通过才能 commit
- **glossary 变更后**：必须在 commit message 中标注 `glossary:` 前缀，方便追溯
- **破例机制**：如有紧急修复需跳过 lint，使用 `git commit --no-verify`，但必须在 commit message 中说明原因

---

> 最后更新：2026-07-31
> 参考：腾讯《Loop Engineering》闭环部分 · 腾讯《Harness不是目的，知识才是护城河》
