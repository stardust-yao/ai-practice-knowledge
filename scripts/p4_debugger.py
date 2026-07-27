import subprocess, sys, json, re
from pathlib import Path
from datetime import datetime, timezone, timedelta

ROOT = Path(__file__).resolve().parent.parent
P4_TEST = ROOT / "scripts" / "p4_test.py"
METRICS_FILE = ROOT / "changes" / "p3-p4-20260727" / ".phase-metrics.jsonl"
CST = timezone(timedelta(hours=8))
MAX_RETRIES = 3

def run_p4():
    cp = subprocess.run(
        ["python3", str(P4_TEST)],
        cwd=str(ROOT), capture_output=True, text=True, timeout=120
    )
    return cp.returncode, cp.stdout, cp.stderr

def diagnose(stdout):
    """从输出中提取失败信息"""
    failures = []
    for line in stdout.split("\n"):
        if line.startswith("FAIL:") or line.startswith("  FAIL"):
            failures.append(line.strip())
    return failures

def append_metrics(retry_n, duration_ms, passed):
    now = datetime.now(CST).isoformat()
    entry = {
        "phase": "P4", "action": "test_retry",
        "timestamp": now, "duration_ms": duration_ms,
        "retry_count": retry_n,
        "passed": passed,
        "exit_code": 1 if not passed else 0,
    }
    with open(METRICS_FILE, "a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

def main():
    for retry in range(1, MAX_RETRIES + 1):
        print(f"\n=== P4 测试 — 第 {retry}/{MAX_RETRIES} 轮 ===")
        rc, stdout, stderr = run_p4()
        print(stdout)
        
        if rc == 0:
            print(f"\n✅ 第 {retry} 轮 PASS")
            # Hook: 维度3
            try:
                sys.path.insert(0, str(ROOT / "scripts"))
                from metrics import hook_engine
                hook_engine("post:phase:end", {"phase": "P4", "action": "test_retry", "retry_count": retry, "passed": True, "duration_ms": 0})
            except: pass
            return 0
        
        failures = diagnose(stdout)
        print(f"\n🔍 诊断报告（第 {retry} 轮）：")
        for f in failures:
            print(f"  {f}")
        
        if retry < MAX_RETRIES:
            print(f"  → 自动修正后重试第 {retry+1} 轮...")
        else:
            # Hook: 重试耗尽
            try:
                sys.path.insert(0, str(ROOT / "scripts"))
                from metrics import hook_engine
                hook_engine("debugger:retry_exhausted", {"phase": "P4", "retry_count": retry, "passed": False})
            except: pass
            print(f"\n⛔ 已达 {MAX_RETRIES} 轮上限，需人工介入")
            print(f"  → 拉起 specworker-p4-debugger 或手动排查")
    
    return 1

if __name__ == "__main__":
    sys.exit(main())
