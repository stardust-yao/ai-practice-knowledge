#!/usr/bin/env python3
"""
spec-semantic-check.py — L3 语义一致性检查

将两份描述相同事物的 spec 段落发送给 LLM，判断是否存在语义矛盾。
输出 JSON 格式的冲突清单。

用法：
  python3 scripts/spec-semantic-check.py
  python3 scripts/spec-semantic-check.py --json   # 仅输出 JSON

API: DeepSeek (key via env DEEPSEEK_API_KEY)
"""

import json
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path

ROOT = Path(__file__).parent.parent.resolve()
API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
API_URL = "https://api.deepseek.com/chat/completions"
MODEL = "deepseek-chat"

# ── 检查对列表 ──
# 每对：(名称, 文件A, 段落标题A, 文件B, 段落标题B)
CHECK_PAIRS = [
    (
        "Gate 规则级别",
        "specs/design.md",
        "管线 2：加工",
        "specs/concept-spec.md",
        "合规等级"
    ),
    (
        "Concept 字段必填约束",
        "specs/concept-template.md", 
        "Frontmatter 字段",
        "specs/concept-spec.md",
        "Gate 校验清单"
    ),
    (
        "管线 2 输入/输出定义",
        "specs/design.md",
        "管线 2：加工",
        "specs/requirements.md",
        "AC-4"
    ),
    (
        "知识库分类体系",
        "knowledge/index.md",
        "项目架构",
        "specs/design.md",
        "数据模型"
    ),
]


def read_section(filepath: str, section_hint: str) -> str:
    """从 Markdown 文件中提取指定段落"""
    full_path = ROOT / filepath
    if not full_path.exists():
        return f"[FILE NOT FOUND: {filepath}]"

    text = full_path.read_text(encoding="utf-8")
    lines = text.split("\n")

    # 查找段落：找到匹配 section_hint 的标题后，取后续内容直到下一个 ##
    collecting = False
    collected = []
    for line in lines:
        if not collecting and section_hint.lower() in line.lower() and line.strip().startswith("##"):
            collecting = True
            collected.append(line)
            continue
        if collecting:
            if line.strip().startswith("##") and len(collected) > 3:
                break
            collected.append(line)

    result = "\n".join(collected[:60])  # max 60 lines
    if len(result) < 100:
        # Fallback: return file beginning
        result = text[:2000]
    return result


def call_llm(prompt: str) -> dict:
    """调用 DeepSeek API 做语义矛盾判断"""
    data = json.dumps({
        "model": MODEL,
        "messages": [
            {"role": "system", "content": (
                "你是一个技术文档审查专家。你的任务是判断两份 spec 段落是否存在语义矛盾。"
                "「矛盾」的定义：对同一件事的结论不同（如一个说 A 是阻断，另一个说 A 不阻断）。"
                "返回严格的 JSON 格式，不要带任何其他文字。"
            )},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.0,
        "max_tokens": 400,
        "response_format": {"type": "json_object"}
    }).encode("utf-8")

    req = urllib.request.Request(API_URL, data=data, headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    })

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read())
            content = result["choices"][0]["message"]["content"]
            return json.loads(content)
    except (urllib.error.HTTPError, urllib.error.URLError) as e:
        return {"conflict": False, "confidence": 0, "explanation": f"API error: {e}", "error": True}
    except (json.JSONDecodeError, KeyError) as e:
        return {"conflict": False, "confidence": 0, "explanation": f"Parse error: {e}", "error": True}


def check_pair(name: str, file_a: str, section_a: str, file_b: str, section_b: str) -> dict:
    text_a = read_section(file_a, section_a)
    text_b = read_section(file_b, section_b)

    prompt = f"""判断以下两份 spec 段落是否存在语义矛盾。

段落 A（来源：{file_a}）：
---
{text_a[:2000]}
---

段落 B（来源：{file_b}）：
---
{text_b[:2000]}
---

请返回 JSON：
{{
  "conflict": true/false,
  "confidence": 0.0-1.0,
  "explanation": "一句话说明是否有矛盾、矛盾在哪里",
  "severity": "high" / "medium" / "low" / "none"
}}"""

    result = call_llm(prompt)
    result["name"] = name
    result["file_a"] = file_a
    result["file_b"] = file_b
    return result


def main():
    json_only = "--json" in sys.argv

    if not json_only:
        print("=" * 60)
        print("Spec Semantic Check — L3 语义一致性检查")
        print("=" * 60)
        print(f"[INFO] 检查 {len(CHECK_PAIRS)} 对 spec 段落...\n")

    results = []
    for name, file_a, sec_a, file_b, sec_b in CHECK_PAIRS:
        if not json_only:
            print(f"  检查: {name}")
            print(f"    A: {file_a} > {sec_a}")
            print(f"    B: {file_b} > {sec_b}")

        r = check_pair(name, file_a, sec_a, file_b, sec_b)
        results.append(r)

        if not json_only:
            if r.get("error"):
                print(f"    ❌ API 调用失败: {r['explanation']}")
            elif r["conflict"]:
                print(f"    ⚠️  发现矛盾 (置信度 {r['confidence']:.0%}, 严重度 {r['severity']})")
                print(f"    → {r['explanation']}")
            else:
                print(f"    ✅ 无矛盾 (置信度 {r['confidence']:.0%})")
            print()

    # 摘要
    conflicts = [r for r in results if r.get("conflict") and not r.get("error")]
    errors = [r for r in results if r.get("error")]

    if not json_only:
        print("─" * 60)
        print(f"  结果: {len(conflicts)} 处语义矛盾 / {len(results)} 对检查")
        if errors:
            print(f"  API 错误: {len(errors)} 对")
        print("─" * 60)

    # JSON 输出
    output = {
        "total_checks": len(results),
        "conflicts_found": len(conflicts),
        "api_errors": len(errors),
        "results": results
    }
    print("\n" + json.dumps(output, ensure_ascii=False, indent=2))

    sys.exit(0 if not conflicts else 1)


if __name__ == "__main__":
    main()
