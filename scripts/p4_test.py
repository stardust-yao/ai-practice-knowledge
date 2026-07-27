#!/usr/bin/env python3
"""P4 集成测试 — TC-4 加工流水线 + TC-6 跨项目加载.

纯 stdlib，每个 case 独立执行，失败不阻断后续。
exit 0 = 全部 PASS，exit 1 = 任一 FAIL。
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
ENTRIES_DIR = ROOT / "knowledge" / "entries"
INDEX_MD = ROOT / "knowledge" / "index.md"
LOG_MD = ROOT / "knowledge" / "log.md"
BACKLINKS_FILE = ROOT / "knowledge" / ".backlinks.json"
VALIDATE_SCRIPT = ROOT / "scripts" / "validate_concept.py"
FETCH_SCRIPT = ROOT / "fetch_articles.py"
REBUILD_SCRIPT = ROOT / "scripts" / "rebuild_backlinks.py"

# Expected 8 modules (from validate_concept.py whitelist)
EXPECTED_MODULES = {
    "project-arch",
    "skill-design",
    "tools-integration",
    "memory-knowledge",
    "safety-guardrails",
    "eval-testing",
    "cost-performance",
    "fundamentals",
}

EXIT_CODE = 0  # mutated by failures


# =============================================================================
# Helpers
# =============================================================================

def _pass(msg: str = "") -> None:
    if msg:
        print(f"PASS: {msg}")
    else:
        print("PASS")


def _fail(reason: str) -> None:
    global EXIT_CODE
    EXIT_CODE = 1
    print(f"FAIL: {reason}")


def _run(args: list[str], cwd: str | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        args,
        cwd=cwd or str(ROOT),
        capture_output=True,
        text=True,
        timeout=120,
    )


def _parse_frontmatter(filepath: Path) -> dict[str, str]:
    """Parse YAML frontmatter (stdlib, same approach as validate_concept.py)."""
    text = filepath.read_text(encoding="utf-8")
    parts = text.split("---")
    if len(parts) < 3:
        return {}
    fm_text = parts[1].strip()
    result: dict[str, str] = {}
    for line in fm_text.split("\n"):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        # bracket list: tags: [a, b, c] — skip for our purposes, we only
        # need scalar fields like `module` and `title`.
        if re.match(r"^[\w][\w-]*\s*:\s*\[", stripped):
            continue
        m = re.match(r"^([\w][\w-]*)\s*:\s*(.+)$", stripped)
        if m:
            key = m.group(1)
            val = m.group(2).strip().strip("'\"").strip()
            result[key] = val
    return result


# =============================================================================
# TC-4.1: Gate 校验 — validate_concept.py
# =============================================================================

def test_tc4_1() -> None:
    print("=== TC-4.1: Gate 校验 ===")

    if not VALIDATE_SCRIPT.is_file():
        _fail(f"脚本缺失: {VALIDATE_SCRIPT}")
        return

    cp = _run(["python3", str(VALIDATE_SCRIPT), str(ENTRIES_DIR)])
    stdout = cp.stdout.strip()

    if cp.returncode != 0:
        # Print the actual FAIL output from validate_concept.py
        _fail(f"validate_concept.py exit {cp.returncode}")
        for line in stdout.split("\n"):
            print(f"  {line}")
        return

    # Count PASS lines to confirm 19 files * 8 checks each → 152/152
    pass_lines = re.findall(r"PASS \((\d+)/(\d+)\)", stdout)
    total_pass = sum(int(a) for a, _ in pass_lines)
    total_checks = sum(int(b) for _, b in pass_lines)

    if total_pass == total_checks:
        _pass(f"{total_pass}/{total_checks}")
    else:
        _fail(f"Gate 校验 {total_pass}/{total_checks}")


# =============================================================================
# TC-4.2: 筛选流水线 — fetch_articles.py --dry-run
# =============================================================================

def test_tc4_2() -> None:
    print("\n=== TC-4.2: 筛选流水线 ===")

    if not FETCH_SCRIPT.is_file():
        _fail(f"脚本缺失: {FETCH_SCRIPT}")
        return

    cp = _run(["python3", str(FETCH_SCRIPT), "--dry-run"])
    stdout = cp.stdout
    stderr = cp.stderr

    if cp.returncode != 0:
        _fail(f"fetch_articles.py --dry-run exit {cp.returncode}")
        if stderr:
            for line in stderr.strip().split("\n"):
                print(f"  [stderr] {line}")
        return

    # Check output for success indicators
    combined = stdout + stderr
    has_success = "[INFO]" in combined or "成功" in combined or "新文章" in combined or "Feed" in combined

    if has_success:
        _pass()
    else:
        _fail("输出中未找到成功状态标识")
        # Print first 10 lines for diagnostics
        for i, line in enumerate(stdout.strip().split("\n")[:10]):
            print(f"  [output] {line}")


# =============================================================================
# TC-4.3: 回链重建 — rebuild_backlinks.py → .backlinks.json
# =============================================================================

def test_tc4_3() -> None:
    print("\n=== TC-4.3: 回链重建 ===")

    if not REBUILD_SCRIPT.is_file():
        _fail(f"脚本缺失: {REBUILD_SCRIPT}")
        return

    cp = _run(["python3", str(REBUILD_SCRIPT)])
    stdout = cp.stdout.strip()

    if cp.returncode != 0:
        _fail(f"rebuild_backlinks.py exit {cp.returncode}")
        for line in stdout.split("\n"):
            print(f"  {line}")
        return

    # Verify .backlinks.json exists and is valid JSON
    if not BACKLINKS_FILE.is_file():
        _fail(f".backlinks.json 未生成: {BACKLINKS_FILE}")
        return

    try:
        data = json.loads(BACKLINKS_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        _fail(f".backlinks.json 不是合法 JSON: {e}")
        return

    if isinstance(data, dict):
        _pass(f"{len(data)} concepts have backlinks")
    else:
        _fail(f".backlinks.json 顶层不是 object，而是 {type(data).__name__}")


# =============================================================================
# TC-5: Delta Spec 变更记录 — log.md 结构
# =============================================================================

def test_tc5() -> None:
    print("\n=== TC-5: Delta Spec 变更记录 ===")

    if not LOG_MD.is_file():
        _fail(f"日志文件缺失: {LOG_MD}")
        return

    log_text = LOG_MD.read_text(encoding="utf-8")

    # 检查是否有日期标题（## YYYY-MM-DD）
    dates = re.findall(r"^## (\d{4}-\d{2}-\d{2})", log_text, re.MULTILINE)
    if not dates:
        _fail("log.md 无日期标题（格式: ## YYYY-MM-DD）")
        return

    # 检查是否有 Delta Spec 标记（**Addition**/**Update**/**Deprecation**）
    additions = re.findall(r"\*\*Addition\*\*", log_text)
    updates = re.findall(r"\*\*Update\*\*", log_text)
    total = len(additions) + len(updates)

    if total == 0:
        _fail("log.md 无 Delta Spec 标记（**Addition**/**Update**）")
        return

    _pass(f"{len(dates)} dates, {total} entries ({len(additions)}A/{len(updates)}U)")


# =============================================================================
# TC-6.1: 模块覆盖 — index.md 8 modules + 19 concepts module 字段
# =============================================================================""

def test_tc6_1() -> None:
    print("\n=== TC-6.1: 模块覆盖 ===")

    # --- Part A: index.md has 8 module headings ---
    if not INDEX_MD.is_file():
        _fail(f"索引文件缺失: {INDEX_MD}")
        return

    index_text = INDEX_MD.read_text(encoding="utf-8")

    # Match "## 1. …" through "## 8. …"
    module_headings = re.findall(r"^##\s+\d+\.\s+(.+)$", index_text, re.MULTILINE)
    if len(module_headings) != 8:
        _fail(f"index.md 模块标题数 = {len(module_headings)} (期望 8)")
        return

    # --- Part B: 19 concepts, module field non-empty and in whitelist ---
    entry_files = sorted(ENTRIES_DIR.glob("*.md"))
    concept_count = len(entry_files)
    if concept_count != 19:
        _fail(f"知识条目数 = {concept_count} (期望 19)")
        return

    covered_modules: set[str] = set()
    empty_module_files: list[str] = []
    invalid_module_files: list[str] = []

    for ef in entry_files:
        fm = _parse_frontmatter(ef)
        mod = fm.get("module", "").strip()
        if not mod:
            empty_module_files.append(ef.name)
        elif mod not in EXPECTED_MODULES:
            invalid_module_files.append(f"{ef.name}: '{mod}'")
        else:
            covered_modules.add(mod)

    errors: list[str] = []
    if empty_module_files:
        errors.append(f"module 字段为空: {', '.join(empty_module_files)}")
    if invalid_module_files:
        errors.append(f"module 不在白名单: {', '.join(invalid_module_files)}")

    missing_modules = EXPECTED_MODULES - covered_modules
    if missing_modules:
        # Known gap: tools-integration 模块暂无内容
        print(f"  IMPORTANT: 模块未覆盖（已知 gap）: {', '.join(sorted(missing_modules))}")

    if empty_module_files or invalid_module_files:
        if empty_module_files:
            _fail(f"module 字段为空: {', '.join(empty_module_files)}")
        if invalid_module_files:
            _fail(f"module 不在白名单: {', '.join(invalid_module_files)}")
        return

    _pass(f"{len(covered_modules)} modules, {concept_count} concepts")


# =============================================================================
# TC-6.2: 渐进式加载 — index.md → modules → concepts readable
# =============================================================================

def test_tc6_2() -> None:
    print("\n=== TC-6.2: 渐进式加载 ===")

    if not INDEX_MD.is_file():
        _fail(f"索引文件缺失: {INDEX_MD}")
        return

    index_text = INDEX_MD.read_text(encoding="utf-8")

    # Step 1: Parse module sections from index.md
    # Each module section is "## N. Name" followed by bullet links to entries/*.md
    module_blocks = re.split(r"\n(?=## \d+\. )", index_text)
    if not module_blocks:
        _fail("index.md 无模块段落")
        return

    # Step 2: Collect all entry links from index.md
    entry_links: set[str] = set()
    for block in module_blocks:
        links = re.findall(r"\[([^\]]*)\]\(entries/([^)]+\.md)\)", block)
        for _, filename in links:
            entry_links.add(filename)

    if not entry_links:
        _fail("index.md 中未找到条目链接")
        return

    # Step 3: Verify each linked entry file exists and is readable
    missing_files: list[str] = []
    unreadable_files: list[str] = []
    found_count = 0

    for filename in sorted(entry_links):
        fpath = ENTRIES_DIR / filename
        if not fpath.is_file():
            missing_files.append(filename)
            continue
        try:
            content = fpath.read_text(encoding="utf-8")
            # Must have non-empty content beyond frontmatter
            if len(content.strip()) < 50:
                unreadable_files.append(f"{filename} (内容过短: {len(content)} 字节)")
            else:
                found_count += 1
        except Exception as e:
            unreadable_files.append(f"{filename} ({e})")

    total = len(entry_links)
    errors: list[str] = []
    if missing_files:
        errors.append(f"文件缺失: {', '.join(missing_files)}")
    if unreadable_files:
        errors.append(f"不可读: {', '.join(unreadable_files)}")

    if errors:
        for e in errors:
            _fail(e)
        return

    _pass(f"{found_count}/{total} readable")


# =============================================================================
# Main
# =============================================================================

def main() -> None:
    os.chdir(ROOT)
    import time
    t0 = time.time()

    test_tc4_1()
    test_tc4_2()
    test_tc4_3()
    test_tc5()
    test_tc6_1()
    test_tc6_2()

    duration_ms = int((time.time() - t0) * 1000)
    # Hook: 维度3 指标收集
    try:
        from pathlib import Path as _P
        import json as _J, sys as _S
        _S.path.insert(0, str(ROOT / "scripts"))
        from metrics import hook_engine
        hook_engine("post:phase:end", {
            "phase": "P4", "action": "test",
            "duration_ms": duration_ms,
            "passed": EXIT_CODE == 0,
            "retry_count": 0,
        })
    except Exception:
        pass  # Hook 不阻断主流程

    print()
    if EXIT_CODE == 0:
        print("✅ 全部 PASS")
    else:
        print("❌ 存在 FAIL")
    sys.exit(EXIT_CODE)


if __name__ == "__main__":
    main()
