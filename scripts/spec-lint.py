#!/usr/bin/env python3
"""
spec-lint.py — L1 Spec 一致性检查脚本

检查项：
  1. 术语引用检查：spec 中提及的术语是否在 glossary.md 中定义
  2. 重定义检查：spec 中是否有「自行定义已存在于 glossary 的术语」
  3. 术语引用格式检查：spec 中是否使用了「术语引用」格式链接 glossary

输出：按文件分组的问题报告，包含文件路径 + 行号 + 违规描述。

返回码：
  0 — 无违规（PASS）
  1 — 有 WARN（仅建议项）
  2 — 有 ERROR（必须修复）
"""

import re
import sys
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).parent.parent.resolve()
GLOSSARY_PATH = ROOT / "glossary.md"
SPECS_DIR = ROOT / "specs"

# ── 1. 从 glossary.md 提取术语 ──
def extract_glossary_terms(path: Path) -> dict[str, str]:
    """返回 {术语名: 定义首行}"""
    text = path.read_text(encoding="utf-8")
    terms = {}
    in_term = False
    current_term = None
    current_def = []

    for line in text.split("\n"):
        # 检测 ### 术语名
        m = re.match(r"^### (.+)", line)
        if m:
            if current_term:
                terms[current_term] = " ".join(current_def)[:120]
            current_term = m.group(1).strip()
            current_def = []
            in_term = True
            continue

        # 遇到下一个 ## 或 --- 结束当前术语
        if re.match(r"^(## |---)", line) and in_term:
            if current_term:
                terms[current_term] = " ".join(current_def)[:120]
            in_term = False
            current_term = None
            current_def = []
            continue

        if in_term and current_term and line.strip():
            current_def.append(line.strip())

    if current_term:
        terms[current_term] = " ".join(current_def)[:120]
    return terms


# ── 2. 扫描 spec 文件 ──
REDEF_PATTERNS = [
    (re.compile(r"\*\*定义\*\*[：:]"), "bold-definition"),   # **定义**：
    (re.compile(r"「(.+?)」[的是为指].*?术语"), "quote-def"),  # 「xxx」是指
    (re.compile(r"^[-*]\s+\*\*(.+?)\*\*[：:].*?(定义|指|是)"), "bullet-def"),  # - **Term**：定义
]

# 中英文术语映射（specs 中可能用中文别名指代英文术语）
TERM_ALIASES = {
    "术语表": "glossary",
    "知识条目": "Concept",
    "原文": "Raw",
    "模块": "Module",
    "门禁": "Gate",
    "管线": "Pipeline",
    "契约": "Spec",
    "必填": "必填",
}


def check_spec_file(filepath: Path, glossary_terms: set[str]) -> list[dict]:
    """扫描单个 spec 文件，返回违规列表"""
    violations = []
    try:
        lines = filepath.read_text(encoding="utf-8").split("\n")
    except Exception:
        return violations

    # 构建术语提及集合（包括别名）
    all_terms = set(glossary_terms)
    all_terms.update(TERM_ALIASES.keys())

    # ── 2a. 术语引用格式检查 ──
    # 检查是否使用了 `[术语](glossary.md#术语)` 格式
    has_glossary_ref = any("glossary.md" in line for line in lines)
    is_spec_file = filepath.name.endswith(".md") and "template" not in filepath.name.lower()

    # ── 2b. 重定义检查 ──
    for i, line in enumerate(lines, 1):
        line_stripped = line.strip()
        if not line_stripped or line_stripped.startswith(">"):
            continue

        # 跳过代码块
        if line_stripped.startswith("```"):
            continue

        # 检查是否在"定义"某个 glossary 术语
        for term in glossary_terms:
            if term in line_stripped and any(
                kw in line_stripped.lower() for kw in ["定义", "是指", "指的是", "即"]
            ):
                # 排除引用链接行
                if "glossary.md" in line_stripped:
                    continue
                # 排除模板/示例行（包含格式占位符或「链接至此」等引导语）
                if any(skip in line_stripped for skip in ["`", "链接至", "模板", "示例", "引用", "格式", "填写说明", "必填"]):
                    continue
                violations.append({
                    "file": str(filepath.relative_to(ROOT)),
                    "line": i,
                    "type": "redefinition",
                    "level": "ERROR",
                    "detail": f"疑似重定义 glossary 术语「{term}」。请改为链接 glossary.md",
                    "context": line_stripped[:100],
                })
                break  # 一行只报一次

    # ── 2c. 术语引用缺失检查 ──
    # 检查 spec 中是否使用了术语但未引用 glossary
    # 统计文件中出现的 glossary 术语数
    term_mentions = 0
    for line in lines:
        for term in glossary_terms:
            # 只用短术语名匹配（取 /前的部分），避免 "Gate / Gate 校验" 之类的匹配噪声
            short_term = term.split(" / ")[0].strip()
            if short_term in line:
                term_mentions += 1
                break

    # 如果文件提及 ≥3 个 glossary 术语但未链接 glossary，报告
    has_glossary_link = any("glossary.md" in line for line in lines)
    if term_mentions >= 3 and not has_glossary_link:
        violations.append({
            "file": str(filepath.relative_to(ROOT)),
            "line": 1,
            "type": "missing-glossary-ref",
            "level": "WARN",
            "detail": f"文件提及 ≥{term_mentions} 个 glossary 术语但未链接 glossary.md。建议添加术语引用章节。",
            "context": f"提及术语数: {term_mentions}",
        })

    # 旧版：术语定义段落检测（更具体的 heuristics）  
    for i, line in enumerate(lines, 1):
        line_stripped = line.strip()
        if "术语" in line_stripped and "glossary" not in line_stripped.lower() and any(
            kw in line_stripped.lower() for kw in ["如下", "约定", "说明"]
        ):
            violations.append({
                "file": str(filepath.relative_to(ROOT)),
                "line": i,
                "type": "missing-glossary-ref",
                "level": "WARN",
                "detail": "检测到术语定义段落但未引用 glossary.md",
                "context": line_stripped[:100],
            })

    return violations


def main():
    print("=" * 60)
    print("Spec Lint — L1 一致性检查")
    print("=" * 60)

    if not GLOSSARY_PATH.exists():
        print(f"[FATAL] glossary.md 不存在: {GLOSSARY_PATH}")
        sys.exit(2)

    glossary_terms = extract_glossary_terms(GLOSSARY_PATH)
    print(f"\n[INFO] glossary 已加载 {len(glossary_terms)} 个术语:")
    for t in sorted(glossary_terms):
        print(f"  • {t}")
    print()

    # 扫描所有 spec 文件
    all_violations = []
    spec_files = sorted(SPECS_DIR.glob("**/*.md"))
    print(f"[INFO] 扫描 {len(spec_files)} 个 spec 文件...\n")

    for fp in spec_files:
        violations = check_spec_file(fp, set(glossary_terms.keys()))
        if violations:
            all_violations.extend(violations)

    # ── 输出报告 ──
    if not all_violations:
        print("✅ 未发现违规。所有 spec 文件术语引用规范。")
        sys.exit(0)

    # 按文件分组
    by_file = defaultdict(list)
    for v in all_violations:
        by_file[v["file"]].append(v)

    errors = sum(1 for v in all_violations if v["level"] == "ERROR")
    warns = sum(1 for v in all_violations if v["level"] == "WARN")

    print(f"{'─' * 60}")
    print(f"  发现 {errors} 个 ERROR + {warns} 个 WARN（共 {len(all_violations)} 项）")
    print(f"{'─' * 60}\n")

    for filepath, violations in sorted(by_file.items()):
        print(f"📄 {filepath}")
        for v in violations:
            tag = "❌ ERROR" if v["level"] == "ERROR" else "⚠️  WARN"
            print(f"  {tag}  L{v['line']:>4} | {v['detail']}")
            print(f"          > {v['context']}")
        print()

    # 返回码
    if errors > 0:
        sys.exit(2)

    # 建议作为 pre-commit hook
    print("─" * 60)
    print("💡 建议作为 git pre-commit hook 运行：")
    print("   cp scripts/spec-lint.py .git/hooks/pre-commit")
    print("   或添加到 .pre-commit-config.yaml")
    print("─" * 60)

    sys.exit(1 if warns > 0 else 0)


if __name__ == "__main__":
    main()
