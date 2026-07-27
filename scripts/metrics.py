#!/usr/bin/env python3
"""Metrics CLI — 双层 Hook 指标收集与报告 (维度3)

Hook 架构:
  平台级: 所有脚本执行时自动往 hook_events.jsonl 追加记录
  业务级: metrics.py 按场景定制读取

四类指标:
  Token/成本    total_input_tokens + total_output_tokens → estimated_cost_usd
  耗时          每个阶段 duration_ms
  重试/失败率    retry_count > 0 的步骤
  代码改动量    lines_added / lines_deleted / files_changed
"""

import json, sys, os, subprocess
from pathlib import Path
from datetime import datetime, timezone, timedelta
from collections import defaultdict

ROOT = Path(__file__).resolve().parent.parent
HOOK_TABLE = ROOT / "logs" / "hook_events.jsonl"
CST = timezone(timedelta(hours=8))

# 费率 (USD / 1M tokens)
MODEL_RATES = {"deepseek-v4": 0.14, "default": 0.15}

def hook_engine(event_type, data):
    """平台级 Hook Engine: 统一在关键节点追加事件到中央表"""
    event = {"timestamp": datetime.now(CST).isoformat(), "type": event_type, "data": data}
    with open(HOOK_TABLE, "a") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")

# ── 业务级 CLI 命令 ────────────────────────────────────────────────────────────

def cmd_summary():
    """四类指标汇总"""
    if not HOOK_TABLE.exists():
        print("暂无 hook 事件数据")
        return ""

    entries = [json.loads(l) for l in open(HOOK_TABLE) if l.strip()]
    if not entries:
        print("暂无 hook 事件数据")
        return ""

    # 按阶段聚合
    phases = defaultdict(lambda: {"count": 0, "duration_ms": 0, "input_tokens": 0, "output_tokens": 0, "lines_added": 0, "lines_deleted": 0, "files_changed": 0, "retries": 0})
    total_cost = 0.0

    for e in entries:
        d = e.get("data", {})
        phase = d.get("phase", "unknown")
        phases[phase]["count"] += 1
        phases[phase]["duration_ms"] += d.get("duration_ms", 0)
        phases[phase]["input_tokens"] += d.get("total_input_tokens", 0)
        phases[phase]["output_tokens"] += d.get("total_output_tokens", 0)
        phases[phase]["lines_added"] += d.get("lines_added", 0)
        phases[phase]["lines_deleted"] += d.get("lines_deleted", 0)
        phases[phase]["files_changed"] += d.get("files_changed", 0)
        if d.get("retry_count", 0) > 0:
            phases[phase]["retries"] += d["retry_count"]
        # Token 成本估算
        rate = MODEL_RATES.get("default", 0.15)
        cost = (d.get("total_input_tokens", 0) + d.get("total_output_tokens", 0)) / 1_000_000 * rate
        total_cost += cost

    print(f"\n{'阶段':<8} {'次数':<6} {'耗时(s)':<10} {'Token输入':<12} {'Token输出':<12} {'新增行':<8} {'删除行':<8} {'文件':<6} {'重试':<6}")
    print("-" * 85)
    for phase in sorted(phases.keys()):
        p = phases[phase]
        print(f"{phase:<8} {p['count']:<6} {p['duration_ms']/1000:<10.1f} {p['input_tokens']:<12} {p['output_tokens']:<12} {p['lines_added']:<8} {p['lines_deleted']:<8} {p['files_changed']:<6} {p['retries']:<6}")
    print(f"\n💰 估算成本: ${total_cost:.3f} USD")
    total_lines = sum(p["lines_added"] for p in phases.values())
    print(f"📊 每千行 AI 成本: ${total_cost/(total_lines/1000):.3f}" if total_lines > 0 else "")

def cmd_changelog():
    """代码改动量明细"""
    if not HOOK_TABLE.exists():
        print("暂无")
        return
    entries = [json.loads(l) for l in open(HOOK_TABLE) if l.strip()]
    for e in entries:
        d = e.get("data", {})
        print(f"{d.get('phase','?'):<8} +{d.get('lines_added',0):<5} -{d.get('lines_deleted',0):<5} {d.get('files_changed',0)} files")

def cmd_retries():
    """重试/失败分析"""
    if not HOOK_TABLE.exists():
        print("暂无失败记录")
        return
    entries = [json.loads(l) for l in open(HOOK_TABLE) if l.strip()]
    retries = [e for e in entries if e.get("data", {}).get("retry_count", 0) > 0]
    if retries:
        for e in retries:
            d = e["data"]
            print(f"{d.get('phase')}: {d['retry_count']} 次重试")
    else:
        print("✅ 无重试记录")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: metrics.py [summary|changelog|retries]")
        sys.exit(1)

    cmd = sys.argv[1]
    {"summary": cmd_summary, "changelog": cmd_changelog, "retries": cmd_retries}[cmd]()
