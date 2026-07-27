# P4 集成测试

> 按文章 P4 方法：从 test-cases.md 生成可执行脚本 → 失败时 debugger 自动诊断 → 自愈闭环。

---

## 测试生成

从 `specs/test-cases.md` 的 TC-4/TC-6 自动生成 `scripts/p4_test.py`：

| TC | 测试内容 | 执行 |
|----|---------|------|
| TC-4 | 加工流水线验证 | `validate_concept.py knowledge/entries/` |
| TC-4 | 筛选流水线验证 | `fetch_articles.py --dry-run` |
| TC-4 | 反向索引完整性 | `rebuild_backlinks.py` → 验证 JSON |
| TC-6 | 跨项目加载验证 | 读 `index.md` → 解析模块列表 → 逐级读 Concept |
| TC-6 | 渐进式路径验证 | 检查 19 篇 module 字段非空、8 模块全覆盖 |

---

## 自愈闭环

```
p4_test.py 执行
    │
    ├── 全部 PASS → ✅
    │
    └── 任一 FAIL
          │
          ▼
    specworker-p4-debugger SubAgent 接管
          │
          ├── 读失败 case 的 stdout/stderr
          ├── 读 .state.json（如果是管线 2 相关失败）
          ├── 读 Gate 校验输出（定位具体字段）
          │
          ▼
    产出诊断报告：
      - 失败点（哪个脚本/哪个文件/哪个字段）
      - 根因（格式错误 / 字段缺失 / 契约不一致）
      - 修复建议（具体到文件:行号）
          │
          ▼
    诊断报告 → implementation Agent 修正
          │
          ▼
    重跑该 case
          │
          ├── PASS → 销案
          └── FAIL（第 N 轮，N<3）→ 回到 debugger
          │
          └── FAIL（第 3 轮）→ STOP 标注「需人工介入」
```

---

## AI vs 脚本分离

| 环节 | 谁做 |
|------|------|
| `p4_test.py` 执行 | 脚本 |
| 失败时 stdout 收集 | 脚本 |
| 根因诊断 + 修复建议 | AI（specworker-p4-debugger） |
| 修复代码 | AI |
| 重跑验证 | 脚本 |
