#!/usr/bin/env python3
"""Concept file Gate rule validator (F1-F8).

Validates knowledge/entries/*.md files against the Gate rules defined in the
project spec. Reads YAML-like frontmatter from Markdown and checks each field.

Usage:
    python3 validate_concept.py knowledge/entries/harness-engineering.md
    python3 validate_concept.py knowledge/entries/

Output:
    PASS (8/8)                  — all checks passed
    FAIL: F4 module ...         — at least one FAIL-level check failed
    WARN: F3 description ...    — only WARN-level issues, no FAILs
"""

from __future__ import annotations

import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


# ============================================================================
# Gate Rules (from design.md + concept-spec.md)
# ============================================================================

GATE_RULES: dict[str, dict[str, Any]] = {
    "F1": {"field": "type",        "check": "non_empty",               "level": "FAIL"},
    "F2": {"field": "title",       "check": "non_empty",               "level": "FAIL"},
    "F3": {"field": "description", "check": "non_empty",               "level": "WARN"},
    "F4": {
        "field": "module",
        "check": "in_whitelist",
        "level": "FAIL",
        "whitelist": [
            "project-arch",
            "skill-design",
            "tools-integration",
            "memory-knowledge",
            "safety-guardrails",
            "eval-testing",
            "cost-performance",
            "fundamentals",
        ],
    },
    "F5": {"field": "date",       "check": "yyyy_mm_dd",              "level": "FAIL"},
    "F6": {"field": "source",     "check": "non_empty",               "level": "FAIL"},
    "F7": {"field": "tags",       "check": "lowercase_english_min_3", "level": "FAIL"},
    "F8": {"field": "timestamp",  "check": "iso8601",                 "level": "FAIL"},
    # F9-F11 暂不实现（需要解析正文段落，后续补充）
}


# ============================================================================
# Frontmatter Parser (stdlib only — no pyyaml)
# ============================================================================

def _strip_quotes(s: str) -> str:
    """Remove surrounding single or double quotes from a string."""
    s = s.strip()
    if len(s) >= 2:
        if (s[0] == s[-1]) and s[0] in ('"', "'"):
            return s[1:-1]
    return s


def parse_frontmatter(filepath: str) -> dict[str, Any]:
    """Parse YAML frontmatter from a Markdown file.

    Handles:
      - Simple key: value pairs
      - Inline bracket lists: key: [item1, item2, ...]
      - Quoted values (single or double)
      - Dashed list syntax (indented - item) — not used in current entries
        but supported for forward compatibility.

    Returns an empty dict if no frontmatter is found.
    """
    with open(filepath, encoding="utf-8") as f:
        content = f.read()

    # Split by --- delimiters; frontmatter is the second block.
    parts = content.split("---")
    if len(parts) < 3:
        return {}

    frontmatter_text = parts[1].strip()
    if not frontmatter_text:
        return {}

    result: dict[str, Any] = {}

    # Pattern for a bracketed inline list:  tags: [a, b, c]
    _bracket_list_re = re.compile(r"^([\w][\w-]*)\s*:\s*\[(.*)\]$")
    # Pattern for key: value on one line
    _key_value_re = re.compile(r"^([\w][\w-]*)\s*:\s*(.+)$")

    for line in frontmatter_text.split("\n"):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        # --- bracketed list ---
        m = _bracket_list_re.match(stripped)
        if m:
            key = m.group(1)
            items_str = m.group(2)
            items = [
                _strip_quotes(item.strip())
                for item in items_str.split(",")
                if item.strip()
            ]
            result[key] = items
            continue

        # --- key: value ---
        m = _key_value_re.match(stripped)
        if m:
            key = m.group(1)
            value = m.group(2).strip()
            value = _strip_quotes(value)
            result[key] = value
            continue

    return result


# ============================================================================
# Individual Check Functions
#
# Each returns (passed: bool, detail: str).
# detail is empty on success; on failure it's a human-readable reason.
# ============================================================================

def _check_non_empty(value: Any) -> tuple[bool, str]:
    """Value must be a non-empty string."""
    if value is None:
        return False, "为空（字段缺失）"
    if not isinstance(value, str):
        return False, f"类型错误（期望字符串，实际 {type(value).__name__}）"
    if not value.strip():
        return False, "为空字符串"
    return True, ""


def _check_yyyy_mm_dd(value: Any) -> tuple[bool, str]:
    """Value must be a valid date in YYYY-MM-DD format."""
    if value is None:
        return False, "为空（字段缺失）"
    if not isinstance(value, str):
        return False, f"类型错误（期望字符串，实际 {type(value).__name__}）"
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", value):
        return False, f"'{value}' 格式错误，期望 YYYY-MM-DD"
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        return False, f"'{value}' 不是合法日期"
    return True, ""


def _check_iso8601(value: Any) -> tuple[bool, str]:
    """Value must be a valid ISO 8601 timestamp."""
    if value is None:
        return False, "为空（字段缺失）"
    if not isinstance(value, str):
        return False, f"类型错误（期望字符串，实际 {type(value).__name__}）"

    iso_formats = [
        "%Y-%m-%dT%H:%M:%S%z",       # 2026-06-29T00:00:00+08:00
        "%Y-%m-%dT%H:%M:%S.%f%z",    # with microseconds
        "%Y-%m-%dT%H:%M:%SZ",        # UTC suffix
        "%Y-%m-%dT%H:%M:%S",         # no timezone
    ]
    for fmt in iso_formats:
        try:
            datetime.strptime(value, fmt)
            return True, ""
        except ValueError:
            continue
    return False, f"'{value}' 不是合法 ISO 8601 时间戳"


def _check_lowercase_english_min_3(value: Any) -> tuple[bool, str]:
    """Value must be a list of at least 3 lowercase-English tags.

    Allowed characters per tag: a-z, 0-9, hyphen (-).
    Tags must start with a lowercase letter.
    """
    if value is None:
        return False, "为空（字段缺失）"
    if not isinstance(value, list):
        return False, f"类型错误（期望列表，实际 {type(value).__name__}）"
    if len(value) < 3:
        return False, f"标签数量不足（需要至少 3 个，实际 {len(value)} 个）"

    tag_re = re.compile(r"^[a-z][a-z0-9-]*$")
    invalid: list[str] = []
    for tag in value:
        if not isinstance(tag, str):
            invalid.append(f"'{tag}'（非字符串）")
        elif not tag_re.match(tag):
            invalid.append(f"'{tag}'（非小写英文，只允许 a-z / 0-9 / -）")
    if invalid:
        return False, "; ".join(invalid)
    return True, ""


def _check_in_whitelist(value: Any, whitelist: list[str]) -> tuple[bool, str]:
    """Value must be a string present in the whitelist."""
    if value is None:
        return False, "为空（字段缺失）"
    if not isinstance(value, str):
        return False, f"类型错误（期望字符串，实际 {type(value).__name__}）"
    v = value.strip()
    if v not in whitelist:
        return False, f"'{v}' 不在白名单中（允许: {', '.join(whitelist)}）"
    return True, ""


# Dispatch table
_CHECK_FN: dict[str, Any] = {
    "non_empty":               _check_non_empty,
    "yyyy_mm_dd":              _check_yyyy_mm_dd,
    "iso8601":                 _check_iso8601,
    "lowercase_english_min_3": _check_lowercase_english_min_3,
}


# ============================================================================
# Validator
# ============================================================================

def validate_file(filepath: str) -> list[dict[str, Any]]:
    """Validate a single concept file against all Gate rules.

    Returns a list of result dicts, each containing:
        gate, field, level, passed (bool), detail (str)
    """
    frontmatter = parse_frontmatter(filepath)
    results: list[dict[str, Any]] = []

    for gate, rule in GATE_RULES.items():
        field = rule["field"]
        level = rule["level"]
        value = frontmatter.get(field)

        if rule["check"] == "in_whitelist":
            passed, detail = _check_in_whitelist(value, rule["whitelist"])
        else:
            check_fn = _CHECK_FN.get(rule["check"])
            if check_fn is None:
                passed, detail = False, f"内部错误：未知检查类型 '{rule['check']}'"
            else:
                passed, detail = check_fn(value)

        results.append({
            "gate": gate,
            "field": field,
            "level": level,
            "passed": passed,
            "detail": detail,
        })

    return results


# ============================================================================
# File collection
# ============================================================================

def collect_files(path: str) -> list[str]:
    """Collect .md files. Accepts a single file or a directory."""
    p = Path(path).expanduser().resolve()
    if p.is_file():
        return [str(p)] if p.suffix == ".md" else []
    if p.is_dir():
        return sorted(str(f) for f in p.glob("*.md"))
    return []


# ============================================================================
# CLI
# ============================================================================

def main() -> None:
    if len(sys.argv) < 2:
        print("用法: python3 validate_concept.py <path>", file=sys.stderr)
        print("  <path> — 单个 .md 文件或目录", file=sys.stderr)
        sys.exit(2)

    target = sys.argv[1]
    files = collect_files(target)

    if not files:
        print(f"未找到 .md 文件: {target}", file=sys.stderr)
        sys.exit(1)

    total_files = len(files)
    exit_code = 0

    for i, filepath in enumerate(files):
        results = validate_file(filepath)
        total = len(results)
        passed_count = sum(1 for r in results if r["passed"])

        failures = [r for r in results if not r["passed"] and r["level"] == "FAIL"]
        warnings = [r for r in results if not r["passed"] and r["level"] == "WARN"]

        # Print file header for multi-file runs
        if total_files > 1:
            if i > 0:
                print()  # blank line between files
            print(f"{'=' * 60}")
            print(f"📄 {filepath}")
            print(f"{'=' * 60}")

        # Print individual issues
        for r in failures:
            print(f"FAIL: {r['gate']} {r['field']} {r['detail']}")
        for r in warnings:
            print(f"WARN: {r['gate']} {r['field']} {r['detail']}")

        # Summary line
        if not failures and not warnings:
            print(f"PASS ({passed_count}/{total})")
        elif not failures:
            print(f"WARN ({passed_count}/{total}) — 有 WARN 项，无 FAIL")
        else:
            print(f"FAIL ({passed_count}/{total}) — {len(failures)} 项 FAIL")
            exit_code = 1

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
