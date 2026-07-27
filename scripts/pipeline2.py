#!/usr/bin/env python3
"""管线 2：草稿路径管理 + 超时回退（10min）。

从 knowledge/.state.json 读取提炼管线状态，支持：
  - check-timeout: 检查当前 in_progress 任务是否超时
  - reset-timeout: 超时则回退 status 为 idle

草稿路径：{ROOT}/knowledge/entries/.{slug}.draft.md

Usage:
    python3 scripts/pipeline2.py check-timeout    # 检查是否超时
    python3 scripts/pipeline2.py reset-timeout    # 超时则重置为 idle
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path


# ============================================================================
# Constants
# ============================================================================

# 北京时间（CST = UTC+8）
CST = timezone(timedelta(hours=8))

# 项目根目录
ROOT = Path(__file__).resolve().parent.parent

# 状态文件
STATE_FILE = ROOT / "knowledge" / ".state.json"

# 草稿目录
DRAFT_DIR = ROOT / "knowledge" / "entries"

# 初始状态模板
INITIAL_STATE: dict = {
    "status": "idle",
    "current": None,
    "current_draft": None,
    "started_at": None,
    "timeout_minutes": 10,
    "history": [],
}


# ============================================================================
# State I/O
# ============================================================================

def load_state() -> dict:
    """加载 .state.json，文件不存在时返回初始状态。"""
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return {**INITIAL_STATE}
    return {**INITIAL_STATE}


def save_state(state: dict) -> None:
    """写入 .state.json，确保父目录存在。"""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
        f.write("\n")


# ============================================================================
# Draft Path Helpers
# ============================================================================

def draft_path_for(slug: str) -> Path:
    """返回草稿文件的完整路径：{DRAFT_DIR}/.{slug}.draft.md"""
    return DRAFT_DIR / f".{slug}.draft.md"


def final_path_for(slug: str) -> Path:
    """返回正式 Concept 文件的完整路径：{DRAFT_DIR}/{slug}.md"""
    return DRAFT_DIR / f"{slug}.md"


# ============================================================================
# Timeout Logic
# ============================================================================

def check_timeout(state: dict) -> bool:
    """检查当前 in_progress 状态是否已超时。

    Returns:
        True   — 已超时，需要回退
        False  — 未超时或不处于 in_progress 状态
    """
    if state.get("status") != "in_progress":
        return False

    started_at = state.get("started_at")
    if not started_at:
        return False

    try:
        started_dt = datetime.fromisoformat(started_at)
    except (ValueError, TypeError):
        return False

    timeout_minutes = state.get("timeout_minutes", 10)
    elapsed = (datetime.now(CST) - started_dt).total_seconds()

    return elapsed > timeout_minutes * 60


def reset_if_timeout() -> tuple[bool, str]:
    """检查并重置超时状态。

    Returns:
        (action_taken: bool, message: str)
    """
    state = load_state()

    if state.get("status") != "in_progress":
        return False, f"当前状态为 '{state.get('status', 'unknown')}'，无需检查超时"

    if not check_timeout(state):
        started_at = state.get("started_at", "—")
        elapsed = (datetime.now(CST) - datetime.fromisoformat(started_at)).total_seconds() if started_at else 0
        remaining = state.get("timeout_minutes", 10) * 60 - elapsed
        return False, f"未超时 (剩余 {remaining:.0f}s / {state.get('timeout_minutes', 10) * 60}s)"

    # 超时 → 回退
    current = state.get("current", "—")
    current_draft = state.get("current_draft", "—")
    state["status"] = "idle"
    state["current"] = None
    state["current_draft"] = None
    state["started_at"] = None
    save_state(state)

    return True, (
        f"⏰ 超时回退: idled\n"
        f"   原任务: {current}\n"
        f"   草稿:   {current_draft}"
    )


# ============================================================================
# CLI
# ============================================================================

def print_usage() -> None:
    print("用法:", file=sys.stderr)
    print("  python3 scripts/pipeline2.py check-timeout", file=sys.stderr)
    print("  python3 scripts/pipeline2.py reset-timeout", file=sys.stderr)
    print(file=sys.stderr)
    print("子命令:", file=sys.stderr)
    print("  check-timeout   检查当前 in_progress 是否超时，返回退出码 0/1", file=sys.stderr)
    print("  reset-timeout   超时则自动重置 status 为 idle", file=sys.stderr)


def cmd_check_timeout() -> None:
    """检查超时并返回退出码。"""
    state = load_state()
    if check_timeout(state):
        started_at = state.get("started_at", "—")
        timeout_minutes = state.get("timeout_minutes", 10)
        elapsed = (datetime.now(CST) - datetime.fromisoformat(started_at)).total_seconds()
        print(f"TIMEOUT: 已运行 {elapsed:.0f}s，阈值 {timeout_minutes * 60}s")
        sys.exit(1)
    else:
        status = state.get("status", "unknown")
        if status == "in_progress":
            started_at = state.get("started_at", "—")
            elapsed = (datetime.now(CST) - datetime.fromisoformat(started_at)).total_seconds()
            remaining = state.get("timeout_minutes", 10) * 60 - elapsed
            print(f"OK: in_progress，剩余 {remaining:.0f}s")
        else:
            print(f"OK: 状态为 '{status}'，无需检查")
        sys.exit(0)


def cmd_reset_timeout() -> None:
    """检查并重置超时状态。"""
    took_action, msg = reset_if_timeout()
    print(msg)
    sys.exit(0 if not took_action else 0)


def main() -> None:
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(2)

    subcommand = sys.argv[1]

    if subcommand == "check-timeout":
        cmd_check_timeout()
    elif subcommand == "reset-timeout":
        cmd_reset_timeout()
    elif subcommand in ("-h", "--help", "help"):
        print_usage()
        sys.exit(0)
    else:
        print(f"未知子命令: {subcommand}", file=sys.stderr)
        print_usage()
        sys.exit(2)


if __name__ == "__main__":
    main()
