# knowledge-sync — change-id: p3-p4-20260727

> P6 第二步：本次交付中「被反复用到的设计、踩过的坑、约定的契约」沉淀进 specs/，
> 下一次相似需求 P1 阶段就能查到。

---

## 1. Gate 校验模式

**发现**: 全部 8 个 frontmatter 字段都需要 Gate 检查，格式字段（FAIL）和内容字段（WARN）分两档。

**沉淀到**: `specs/concept-spec.md` F1-F11

**复现方法**: 新概念类型增加字段时 → 先判断是 FAIL 还是 WARN → 加入 GATE_RULES 字典 → 脚本自动生效。

---

## 2. Sandbox 模式

**发现**: Git 分支隔离比本地沙箱目录更可靠。每次 D-x 改动走独立分支 → PR review → 合并。

**沉淀到**: `specs/design.md` sandbox_mode + `specs/p3-plan.md` 执行流程

**复现方法**: P3 实现前 `git checkout -b p3/D-x` → 改动完成后 PR → review 通过 merge。

---

## 3. AI/脚本分离

**发现**: 格式检查（日期/标签/类型）交给脚本，语义理解（提炼/补全关联）交给 AI。边界清晰是整套系统可靠的关键。

**沉淀到**: `specs/design.md` §4 分离表

**复现方法**: 新功能上线前，先画分离表——哪些脚本、哪些 AI——不一致就改设计。

---

## 4. SubAgent 模式

**发现**: 一个 SubAgent 只做一件事，独立上下文，单一职责。D-x 逐个派发 → code-reviewer 三档 review。

**沉淀到**: `specs/p3-plan.md` 执行流程

**复现方法**: 新改动拆成 D-x 列表 → 无依赖并行派 SubAgent → 每步过 Gate。

---

## 5. CI/CD 评分卡

**发现**: P4 测试全部 PASS 是部署的前置条件。6/6 PASS = 评分 95（tools-integration known gap 扣 5 分）。

**沉淀到**: `.github/workflows/test.yml` + `specs/p5-plan.md`

**复现方法**: 每次 push 自动跑 P4 → 不通过不部署。
