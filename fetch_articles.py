#!/usr/bin/env python3
"""
fetch_articles.py — 腾讯技术工程文章自动抓取脚本

职责：
  1. 拉取 wechat2rss RSS feed
  2. 过滤出新文章（对比已有记录）
  3. HTML 转 Markdown，保留代码块和标题层级
  4. 保存到 raw/YYYY-MM/
  5. 更新 logs/ops.md（每次运行必写）
  6. 更新 logs/fetch_state.json（去重状态持久化）
  7. 更新 PROJECT.md 统计数字
  8. git commit + push

运行方式：
  python3 fetch_articles.py           # 正常运行
  python3 fetch_articles.py --dry-run # 只打印，不写文件不提交

部署：在阿里云服务器上配 cron，每天凌晨 2 点自动运行
"""

import os
import sys
import json
import re
import hashlib
import argparse
import traceback
from datetime import datetime, timezone, timedelta
from pathlib import Path

# ── 配置 ──────────────────────────────────────────────────────────────────────

FEED_URL = "https://wechat2rss.xlab.app/feed/9685937b45fe9c7a526dbc32e4f24ba879a65b9a.xml"
ACCOUNT_NAME = "腾讯技术工程"

# 脚本所在目录即为项目根目录
ROOT = Path(__file__).parent.resolve()
RAW_DIR = ROOT / "raw"
LOG_DIR = ROOT / "logs"
STATE_FILE = LOG_DIR / "fetch_state.json"   # 记录已抓取文章的 ID，用于去重
OPS_LOG = LOG_DIR / "ops.md"
PROJECT_MD = ROOT / "PROJECT.md"
PENDING_REVIEW_FILE = LOG_DIR / "pending_review.json"  # --review 模式写入，待用户确认
FILTER_FEEDBACK_FILE = LOG_DIR / "filter_feedback.json"  # 筛选反馈记录，驱动规则更新和自动审批

CST = timezone(timedelta(hours=8))  # 北京时间

AUTO_APPROVE_THRESHOLD = 10  # 连续一致次数阈值，达到后跳过人工审核

# ── 工具函数 ──────────────────────────────────────────────────────────────────

def now_str():
    return datetime.now(CST).strftime("%Y-%m-%d %H:%M:%S CST")

def today_str():
    return datetime.now(CST).strftime("%Y-%m-%d")

def month_str():
    return datetime.now(CST).strftime("%Y-%m")

def log(msg, level="INFO"):
    """打印到 stdout，同时记录，供调用方收集"""
    print(f"[{level}] {msg}", flush=True)

def article_id(link, title):
    """从链接提取 sn= 作为稳定 ID，否则用标题 hash"""
    m = re.search(r'sn=([a-f0-9]+)', link)
    if m:
        return m.group(1)
    return hashlib.md5((link + title).encode()).hexdigest()[:16]

def load_state():
    if STATE_FILE.exists():
        with open(STATE_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {"fetched_ids": [], "total_count": 0, "last_run": None}

def save_state(state):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

# ── RSS 解析 ──────────────────────────────────────────────────────────────────

def fetch_feed():
    """拉取 RSS feed，返回原始 XML 字符串"""
    import urllib.request
    log(f"拉取 Feed: {FEED_URL}")
    req = urllib.request.Request(
        FEED_URL,
        headers={"User-Agent": "ai-practice-knowledge-bot/1.0"}
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8")

def parse_feed(xml_text):
    """
    解析 RSS XML，返回文章列表。
    每篇：{id, title, link, pub_date, pub_date_str, content_html}
    """
    articles = []

    # 提取所有 <item> 块
    items = re.findall(r'<item>(.*?)</item>', xml_text, re.DOTALL)
    log(f"Feed 中共 {len(items)} 篇文章")

    for item in items:
        title = _cdata_or_tag(item, "title")
        link  = _cdata_or_tag(item, "link")
        pub   = _cdata_or_tag(item, "pubDate")
        # content:encoded 是全文 HTML
        content_html = _cdata_or_tag(item, "content:encoded")
        if not content_html:
            content_html = _cdata_or_tag(item, "description")

        if not title or not link:
            continue

        aid = article_id(link, title)
        pub_date_str = _parse_pubdate(pub)

        articles.append({
            "id": aid,
            "title": title,
            "link": link,
            "pub_date": pub,
            "pub_date_str": pub_date_str,
            "content_html": content_html or "",
        })

    return articles

def _cdata_or_tag(text, tag):
    """提取 <tag><![CDATA[...]]></tag> 或 <tag>...</tag> 的值"""
    # CDATA 形式
    m = re.search(rf'<{re.escape(tag)}><!\[CDATA\[(.*?)\]\]></{re.escape(tag)}>', text, re.DOTALL)
    if m:
        return m.group(1).strip()
    # 普通形式
    m = re.search(rf'<{re.escape(tag)}>(.*?)</{re.escape(tag)}>', text, re.DOTALL)
    if m:
        return m.group(1).strip()
    return ""

def _parse_pubdate(pub_str):
    """将 RSS pubDate 转成 YYYY-MM-DD，失败返回今天"""
    for fmt in [
        "%a, %d %b %Y %H:%M:%S %z",
        "%a, %d %b %Y %H:%M:%S %Z",
    ]:
        try:
            dt = datetime.strptime(pub_str.strip(), fmt)
            return dt.astimezone(CST).strftime("%Y-%m-%d")
        except Exception:
            pass
    return today_str()

# ── HTML → Markdown ───────────────────────────────────────────────────────────

def html_to_markdown(html):
    """
    将微信文章 HTML 转成干净的 Markdown。
    保留：标题层级、代码块、粗体、列表、段落、引用块。
    丢弃：所有 inline style、图片 URL（只保留 alt 文字提示）。
    纯 stdlib 实现，无第三方依赖。
    """
    text = html

    # 1. 去掉 <script> / <style> 块
    text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)

    # 2. 代码块：<pre> / <code>
    text = re.sub(r'<pre[^>]*><code[^>]*>(.*?)</code></pre>',
                  lambda m: '\n```\n' + _unescape(m.group(1)).strip() + '\n```\n',
                  text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<pre[^>]*>(.*?)</pre>',
                  lambda m: '\n```\n' + _unescape(m.group(1)).strip() + '\n```\n',
                  text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<code[^>]*>(.*?)</code>',
                  lambda m: '`' + _unescape(m.group(1)) + '`',
                  text, flags=re.DOTALL | re.IGNORECASE)

    # 3. 标题
    for i in range(6, 0, -1):
        text = re.sub(rf'<h{i}[^>]*>(.*?)</h{i}>',
                      lambda m, n=i: '\n' + '#' * n + ' ' + _strip_tags(m.group(1)).strip() + '\n',
                      text, flags=re.DOTALL | re.IGNORECASE)

    # 4. 粗体 / 斜体
    text = re.sub(r'<strong[^>]*>(.*?)</strong>',
                  lambda m: '**' + _strip_tags(m.group(1)).strip() + '**',
                  text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<b[^>]*>(.*?)</b>',
                  lambda m: '**' + _strip_tags(m.group(1)).strip() + '**',
                  text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<em[^>]*>(.*?)</em>',
                  lambda m: '*' + _strip_tags(m.group(1)).strip() + '*',
                  text, flags=re.DOTALL | re.IGNORECASE)

    # 5. 引用块
    text = re.sub(r'<blockquote[^>]*>(.*?)</blockquote>',
                  lambda m: '\n> ' + _strip_tags(m.group(1)).replace('\n', '\n> ').strip() + '\n',
                  text, flags=re.DOTALL | re.IGNORECASE)

    # 6. 列表
    text = re.sub(r'<li[^>]*>(.*?)</li>',
                  lambda m: '\n- ' + _strip_tags(m.group(1)).strip(),
                  text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<[ou]l[^>]*>', '\n', text, flags=re.IGNORECASE)
    text = re.sub(r'</[ou]l>', '\n', text, flags=re.IGNORECASE)

    # 7. 图片：只保留提示文字，丢弃 URL
    text = re.sub(r'<img[^>]*alt=["\']([^"\']+)["\'][^>]*/?>',
                  r'\n*[图片：\1]*\n', text, flags=re.IGNORECASE)
    text = re.sub(r'<img[^>]*/?>',
                  '\n*[图片]*\n', text, flags=re.IGNORECASE)

    # 8. 链接
    text = re.sub(r'<a[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>',
                  lambda m: '[' + _strip_tags(m.group(2)).strip() + '](' + m.group(1) + ')',
                  text, flags=re.DOTALL | re.IGNORECASE)

    # 9. 段落 / 换行
    text = re.sub(r'<br\s*/?>', '\n', text, flags=re.IGNORECASE)
    text = re.sub(r'<p[^>]*>(.*?)</p>',
                  lambda m: '\n' + _strip_tags(m.group(1)).strip() + '\n',
                  text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<div[^>]*>(.*?)</div>',
                  lambda m: '\n' + _strip_tags(m.group(1)).strip() + '\n',
                  text, flags=re.DOTALL | re.IGNORECASE)

    # 10. 水平线
    text = re.sub(r'<hr[^>]*/?>','\n---\n', text, flags=re.IGNORECASE)

    # 11. 剥掉所有剩余 HTML 标签
    text = _strip_tags(text)

    # 12. HTML 实体解码
    text = _unescape(text)

    # 13. 清理多余空行（最多保留 2 个连续空行）
    text = re.sub(r'\n{3,}', '\n\n', text)

    return text.strip()

def _strip_tags(html):
    return re.sub(r'<[^>]+>', '', html)

def _unescape(text):
    replacements = [
        ('&amp;', '&'), ('&lt;', '<'), ('&gt;', '>'),
        ('&quot;', '"'), ('&#39;', "'"), ('&nbsp;', ' '),
        ('&#xA;', '\n'), ('&#10;', '\n'),
    ]
    for old, new in replacements:
        text = text.replace(old, new)
    # 数字实体
    text = re.sub(r'&#(\d+);', lambda m: chr(int(m.group(1))), text)
    return text

# ── 文件写入 ──────────────────────────────────────────────────────────────────

def safe_filename(title):
    """将标题转成安全文件名，保留中文"""
    title = re.sub(r'[\\/:*?"<>|]', '-', title)
    title = title.strip('-').strip()
    return title[:80]  # 限制长度

def save_article(article, dry_run=False):
    """
    将文章保存到 raw/YYYY-MM/YYYY-MM-DD_标题.md
    返回保存路径
    """
    pub = article["pub_date_str"]
    year_month = pub[:7]  # "2026-07"
    filename = f"{pub}_{safe_filename(article['title'])}.md"
    dest_dir = RAW_DIR / year_month
    dest_path = dest_dir / filename

    # 组装 Markdown 文件内容
    md_content = article["content_html"]
    if md_content and "<" in md_content:
        md_content = html_to_markdown(md_content)

    content = f"""---
title: {article['title']}
date: {article['pub_date_str']}
source: {article['link']}
account: {ACCOUNT_NAME}
fetched_at: {now_str()}
article_id: {article['id']}
---

{md_content}
"""

    if not dry_run:
        dest_dir.mkdir(parents=True, exist_ok=True)
        with open(dest_path, "w", encoding="utf-8") as f:
            f.write(content)

    return dest_path

# ── 日志写入 ──────────────────────────────────────────────────────────────────

def append_ops_log(run_result, dry_run=False):
    """
    将本次运行结果追加写入 logs/ops.md。
    格式：每次运行一个条目，包含时间、新文章数、标题列表、错误信息。
    """
    lines = [
        f"\n## {run_result['run_time']} — 抓取运行\n",
        f"- **状态**: {run_result['status']}",
        f"- **新文章**: {run_result['new_count']} 篇",
        f"- **Feed 总量**: {run_result['feed_total']} 篇",
        f"- **累计已抓**: {run_result['total_fetched']} 篇",
    ]
    if run_result.get("error"):
        lines.append(f"- **错误**: {run_result['error']}")
    if run_result["new_articles"]:
        lines.append("\n**本次新增：**")
        for a in run_result["new_articles"]:
            lines.append(f"- [{a['title']}]({a['link']}) `{a['pub_date_str']}`")
    lines.append("")

    entry = "\n".join(lines)

    if not dry_run:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        with open(OPS_LOG, "a", encoding="utf-8") as f:
            f.write(entry)

    return entry

def update_project_md(total_count, dry_run=False):
    """更新 PROJECT.md 中的知识条目数量"""
    if not PROJECT_MD.exists():
        return
    text = PROJECT_MD.read_text(encoding="utf-8")
    updated = re.sub(
        r'(- 知识条目数量：)\d+',
        rf'\g<1>{total_count}',
        text
    )
    updated = re.sub(
        r'(- 上次更新：)\S+',
        rf'\g<1>{today_str()}',
        updated
    )
    if not dry_run:
        PROJECT_MD.write_text(updated, encoding="utf-8")

# ── Git 操作 ──────────────────────────────────────────────────────────────────

def git_commit_push(new_articles, dry_run=False):
    """将新文件提交并推送"""
    import subprocess

    if dry_run:
        log("[DRY-RUN] 跳过 git commit/push")
        return True

    os.chdir(ROOT)

    # 只 add 新生成的文件和日志，不 add 全部
    files_to_add = [
        str(STATE_FILE.relative_to(ROOT)),
        str(OPS_LOG.relative_to(ROOT)),
        str(PROJECT_MD.relative_to(ROOT)),
    ]
    for a in new_articles:
        pub = a["pub_date_str"]
        year_month = pub[:7]
        filename = f"{pub}_{safe_filename(a['title'])}.md"
        rel = f"raw/{year_month}/{filename}"
        files_to_add.append(rel)

    result = subprocess.run(
        ["git", "add"] + files_to_add,
        capture_output=True, text=True
    )
    if result.returncode != 0:
        log(f"git add 失败: {result.stderr}", "ERROR")
        return False

    titles = "、".join(a["title"][:20] for a in new_articles[:3])
    if len(new_articles) > 3:
        titles += f" 等{len(new_articles)}篇"
    commit_msg = f"feat(raw): 新增 {len(new_articles)} 篇文章 — {titles}"

    result = subprocess.run(
        ["git", "commit", "-m", commit_msg],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        log(f"git commit 失败: {result.stderr}", "ERROR")
        return False

    log(f"git commit: {commit_msg}")

    result = subprocess.run(
        ["git", "push"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        log(f"git push 失败: {result.stderr}", "ERROR")
        return False

    log("git push 成功")
    return True

# ── 文章质量筛选 ──────────────────────────────────────────────────────────────
#
# 规则来源：logs/filter_rules.md（人工决策 2026-07-18）
# 命中任一排除规则 → 跳过，不写入 raw/，但 ID 不计入 fetched_ids（下次仍可重判）

_EXCLUDE_TITLE_KEYWORDS = [
    # 产品发布 / 推广
    "发布", "上线了", "推出", "全新", "凭什么", "带你速通", "你真的需要",
    # 招募 / 活动
    "招募", "犀牛鸟", "报名",
    # 娱乐
    "高考", "几分",
    # 新闻稿 / 获奖
    "获奖", "杰出论文", "重要突破", "ACL 202",
    # 腾讯混元系列（产品发布/推广，全系列排除，不适用技术豁免）
    "混元",
    # 特定框架/平台推广
    "Kuikly", "Ray",
    # 标题党 / 营销味
    "揭秘",
]

_EXCLUDE_PRODUCT_NAMES = [
    "Marvis", "马维斯",   # 腾讯 Marvis 产品推广系列
]

# 即使命中产品名，标题含这些词说明是技术分析，保留
_RETAIN_OVERRIDE_KEYWORDS = [
    "原理", "技术拆解", "推理优化", "架构", "实战", "方法论", "工程",
]


def _apply_filter_rules(articles):
    """
    返回 (kept, skipped)。
    skipped 列表每项含额外字段 'reason'。
    跳过的文章 ID 不写入 fetched_ids，下次运行仍会重新判断。
    """
    kept, skipped = [], []
    for a in articles:
        title = a.get("title", "")
        reason = _filter_reason(title)
        if reason:
            a_copy = dict(a, reason=reason)
            skipped.append(a_copy)
        else:
            kept.append(a)
    return kept, skipped


def _filter_reason(title):
    """返回排除理由字符串，无理由则返回空字符串（保留）。"""
    # 1. 产品名黑名单（先检查，再看是否有技术关键词豁免）
    for prod in _EXCLUDE_PRODUCT_NAMES:
        if prod in title:
            if any(kw in title for kw in _RETAIN_OVERRIDE_KEYWORDS):
                break  # 豁免：虽含产品名但属技术分析
            return f"产品推广系列（含「{prod}」）"

    # 2. 标题关键词排除
    for kw in _EXCLUDE_TITLE_KEYWORDS:
        if kw in title:
            return f"标题命中排除词「{kw}」"

    return ""


# ── 反馈驱动规则更新 & 自动审批 ──────────────────────────────────────────────
# 每次人工审核后记录结果。连续一致 ≥10 次 → 自动跳过审核直接入库。

def load_feedback():
    if FILTER_FEEDBACK_FILE.exists():
        return json.loads(FILTER_FEEDBACK_FILE.read_text(encoding="utf-8"))
    return {
        "total_reviews": 0,
        "total_overrides": 0,
        "consecutive_agreements": 0,
        "auto_approve_enabled": False,
        "history": [],
    }


def save_feedback(data):
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    FILTER_FEEDBACK_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2),
                                    encoding="utf-8")


def should_auto_approve():
    """连续一致 ≥ 阈值 → 自动跳过人工审核"""
    fb = load_feedback()
    streak = fb["consecutive_agreements"]
    if streak >= AUTO_APPROVE_THRESHOLD:
        if not fb.get("auto_approve_enabled"):
            fb["auto_approve_enabled"] = True
            save_feedback(fb)
        return True
    return False


def record_feedback_overrides(overrides, kept_count, skipped_count):
    """
    overrides: [{id, action: keep|skip, title, reason?}]
    记录反馈，更新连续一致计数，返回 (agreed, suggestions)。
    """
    fb = load_feedback()
    fb["total_reviews"] += 1

    has_overrides = len(overrides) > 0

    entry = {
        "time": now_str(),
        "kept_count": kept_count,
        "skipped_count": skipped_count,
        "overrides": overrides,
        "agreed": not has_overrides,
    }
    fb["history"].append(entry)

    if has_overrides:
        fb["total_overrides"] += len(overrides)
        fb["consecutive_agreements"] = 0
        fb["auto_approve_enabled"] = False
    else:
        fb["consecutive_agreements"] += 1
        # 第一次达到阈值时打印提示
        if fb["consecutive_agreements"] >= AUTO_APPROVE_THRESHOLD:
            fb["auto_approve_enabled"] = True

    save_feedback(fb)

    suggestions = _suggest_rule_updates(overrides) if has_overrides else None
    return not has_overrides, suggestions


def _suggest_rule_updates(overrides):
    """根据用户 override 生成规则更新建议"""
    suggestions = {"add_exclude": [], "add_retain": [], "remove_exclude": []}
    for ov in overrides:
        title = ov.get("title", "")
        action = ov.get("action", "")
        reason = ov.get("reason", "")

        if action == "keep" and reason:
            # 被自动筛选跳过了，但用户认为该保留 → 考虑移除触发词或加上豁免词
            kw = _extract_trigger_keyword(reason)
            if kw:
                suggestions["remove_exclude"].append(
                    f"考虑从排除词中移除「{kw}」（原因：{title[:30]} 被误筛）")

        elif action == "skip":
            # 自动筛选通过了，但用户认为该跳过 → 考虑添加排除词
            suggestions["add_exclude"].append(
                f"考虑添加排除词（原因：{title[:30]} 应排除但未命中规则）")

    return suggestions


def _extract_trigger_keyword(reason):
    """从排除理由中提取触发关键词"""
    m = re.search(r'「([^」]+)」', reason)
    return m.group(1) if m else None


def apply_feedback(overrides_json):
    """
    --feedback 模式：读取 pending_review.json，应用用户 override，返回最终 kept/skipped。
    overrides_json: '[{"id":"abc","action":"keep"},{"id":"def","action":"skip"}]'
    """
    if not PENDING_REVIEW_FILE.exists():
        log("无待处理审核文件", "ERROR")
        return [], [], []

    pending = json.loads(PENDING_REVIEW_FILE.read_text(encoding="utf-8"))
    ov_list = json.loads(overrides_json)
    override_map = {o["id"]: o for o in ov_list}

    # 将 pending 中的文章按用户覆盖重新分配
    kept_by_id = {a["id"]: a for a in pending["kept"]}
    skip_by_id = {s["id"]: s for s in pending["skipped"]}

    final_kept, final_skipped, overrides = [], [], []

    # 处理覆盖
    for oid, ov in override_map.items():
        action = ov["action"]
        title = ov.get("title", oid)

        if action == "keep" and oid in skip_by_id:
            a = skip_by_id.pop(oid)
            a["override"] = "skip→keep"
            final_kept.append(a)
            overrides.append({"id": oid, "action": "keep", "title": title,
                              "reason": a.get("reason", "")})

        elif action == "skip" and oid in kept_by_id:
            a = kept_by_id.pop(oid)
            a["override"] = "keep→skip"
            final_skipped.append(a)
            overrides.append({"id": oid, "action": "skip", "title": title,
                              "reason": ov.get("reason", "")})

    # 未被覆盖的保持原判断
    final_kept.extend(kept_by_id.values())
    final_skipped.extend(skip_by_id.values())

    # 记录反馈
    agreed, suggestions = record_feedback_overrides(
        overrides, len(final_kept), len(final_skipped))

    print()
    if agreed:
        print(f"✅ 本次审核完全一致（连续 {load_feedback()['consecutive_agreements']}/{AUTO_APPROVE_THRESHOLD} 次）")
    else:
        streak = load_feedback()["consecutive_agreements"]
        print(f"📝 已记录 {len(overrides)} 条覆盖（连续一致计数已重置为 {streak}）")
        if suggestions:
            for cat, items in suggestions.items():
                if items:
                    print(f"\n  [{cat}]:")
                    for item in items:
                        print(f"    • {item}")

    if load_feedback()["auto_approve_enabled"]:
        print(f"\n⚡ 自动审批已启用！下次抓取将跳过人工审核。")
        print(f"   （连续 {AUTO_APPROVE_THRESHOLD} 次一致验证通过）")

    return final_kept, final_skipped, overrides


# ── 审核流程 ──────────────────────────────────────────────────────────────────
#
# --review 模式不自动入库，先输出审核表让用户确认再执行。
# 流程：fetch → filter → 输出审核表 → 保存 pending_review.json → STOP
# 用户确认后，不带 --review 再跑一次即入库。

def print_review_table(kept, skipped):
    """输出清晰的审核表，供用户确认筛选决策"""
    print()
    print("╔" + "═" * 78 + "╗")
    print("║  📋 文章审核表 — 请您确认筛选决策                       ║")
    print("╠" + "═" * 78 + "╣")
    for a in kept:
        title = a["title"][:55]
        print(f"║  ✅ KEEP  {title:<55}  {a['pub_date_str']}  ║")
    for s in skipped:
        title = s["title"][:45]
        reason = s.get("reason", "?")[:20]
        print(f"║  ❌ SKIP  {title:<45}  {s['pub_date_str']}  原因:{reason:<20}  ║")
    print("╚" + "═" * 78 + "╝")
    print(f"\n👉 如确认无误请直接回复「入库」，如需调整筛选规则请说明")
    print(f"   待确认数据已保存至 {PENDING_REVIEW_FILE}")


def save_pending_review(kept, skipped, run_time):
    """将待确认的审核结果写入 JSON"""
    data = {
        "run_time": run_time,
        "status": "pending_review",
        "kept": [{"id": a["id"], "title": a["title"], "link": a["link"],
                  "pub_date_str": a["pub_date_str"]} for a in kept],
        "skipped": [{"id": s["id"], "title": s["title"], "link": s["link"],
                      "pub_date_str": s["pub_date_str"], "reason": s.get("reason", "")}
                     for s in skipped],
    }
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    with open(PENDING_REVIEW_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ── 主流程 ────────────────────────────────────────────────────────────────────

def _save_and_commit_articles(new_articles, skipped_articles, dry_run=False):
    """共享入库逻辑：保存文章、更新状态、写日志、git commit"""
    state = load_state()
    fetched_ids = set(state["fetched_ids"])

    for a in new_articles:
        path = save_article(a, dry_run=dry_run)
        log(f"  保存: {path.relative_to(ROOT) if not dry_run else path}")
        fetched_ids.add(a["id"])

    state["fetched_ids"] = list(fetched_ids)
    state["total_count"] = state.get("total_count", 0) + len(new_articles)
    state["last_run"] = now_str()
    if not dry_run:
        save_state(state)

    update_project_md(state["total_count"], dry_run=dry_run)

    run_result = {
        "run_time": now_str(),
        "status": "success",
        "new_count": len(new_articles),
        "feed_total": len(new_articles) + len(skipped_articles),
        "total_fetched": state["total_count"],
        "new_articles": new_articles,
        "error": None,
    }
    append_ops_log(run_result, dry_run=dry_run)
    git_commit_push(new_articles, dry_run=dry_run)
    return True


def main(dry_run=False, review=False, feedback=None, reset=False):
    # --reset：重置连续一致计数
    if reset:
        fb = load_feedback()
        fb["consecutive_agreements"] = 0
        fb["auto_approve_enabled"] = False
        save_feedback(fb)
        log("连续一致计数已重置为 0")


    # --feedback：应用用户覆盖
    if feedback:
        final_kept, final_skipped, overrides = apply_feedback(feedback)
        if not final_kept:
            log("无文章需入库（全部被排除）")
            return True
        # 直接走入库流程
        return _save_and_commit_articles(final_kept, final_skipped, dry_run)
    run_result = {
        "run_time": now_str(),
        "status": "unknown",
        "new_count": 0,
        "feed_total": 0,
        "total_fetched": 0,
        "new_articles": [],
        "error": None,
    }

    log(f"=== 开始运行 {run_result['run_time']} {'[DRY-RUN]' if dry_run else ''} ===")

    try:
        # 1. 加载已抓取状态
        state = load_state()
        fetched_ids = set(state["fetched_ids"])
        log(f"已有记录 {len(fetched_ids)} 篇")

        # 2. 拉取 Feed
        xml_text = fetch_feed()

        # 3. 解析文章
        articles = parse_feed(xml_text)
        run_result["feed_total"] = len(articles)

        # 4. 过滤出新文章（去重 + 质量筛选）
        new_articles = [a for a in articles if a["id"] not in fetched_ids]
        log(f"新文章（去重后）{len(new_articles)} 篇")
        new_articles, skipped = _apply_filter_rules(new_articles)
        for s in skipped:
            log(f"  [筛选跳过] {s['title']} — {s['reason']}", "WARN")
        log(f"通过筛选 {len(new_articles)} 篇，跳过 {len(skipped)} 篇")
        run_result["new_count"] = len(new_articles)
        run_result["new_articles"] = new_articles

        # --- review 模式：输出审核表后停止，不入库 ---
        if review:
            fb = load_feedback()
            print(f"\n📊 当前连续一致: {fb['consecutive_agreements']}/{AUTO_APPROVE_THRESHOLD} "
                  f"({'⚡ 已达阈值' if fb.get('auto_approve_enabled') else '还需继续验证'})")
            print_review_table(new_articles, skipped)
            save_pending_review(new_articles, skipped, run_result["run_time"])
            run_result["status"] = "review_pending"
            log("=== 审核模式：已输出审核表，等待用户确认 ===")
            return True

        # --- 自动审批检查：连续一致 ≥ 阈值 → 跳过审核直接入库 ---
        if not review and new_articles:
            if should_auto_approve():
                log(f"⚡ 自动审批已启用（连续 {AUTO_APPROVE_THRESHOLD}+ 次一致），跳过人工审核")
                # 自动审批也记录一次无覆盖的反馈
                record_feedback_overrides([], len(new_articles), len(skipped))
            else:
                fb = load_feedback()
                log(f"⚠️  连续一致仅 {fb['consecutive_agreements']}/{AUTO_APPROVE_THRESHOLD} 次，"
                    f"建议使用 --review 先审核再入库")
                # 也自动记录（视为确认）
                record_feedback_overrides([], len(new_articles), len(skipped))

        if not new_articles:
            run_result["status"] = "success_no_new"
            log("无新文章，正常退出")
        else:
            return _save_and_commit_articles(new_articles, skipped, dry_run)

    except Exception as e:
        run_result["status"] = "error"
        run_result["error"] = str(e)
        log(f"运行出错: {e}", "ERROR")
        log(traceback.format_exc(), "ERROR")

    # 9. 写操作日志（无论成功失败都写）
    run_result["total_fetched"] = run_result.get("total_fetched", 0)
    entry = append_ops_log(run_result, dry_run=dry_run)
    if dry_run:
        print("\n--- ops.md 将追加以下内容 ---")
        print(entry)

    log(f"=== 运行结束，状态: {run_result['status']} ===")
    return run_result["status"] in ("success", "success_no_new")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="腾讯技术工程文章抓取脚本")
    parser.add_argument("--dry-run", action="store_true",
                        help="只打印，不写文件不 git commit")
    parser.add_argument("--review", action="store_true",
                        help="抓取后输出审核表，等待用户确认后再入库")
    parser.add_argument("--feedback",
                        help='应用用户反馈: \'[{"id":"abc","action":"keep"}]\'')
    parser.add_argument("--reset", action="store_true",
                        help="重置连续一致计数为 0")
    args = parser.parse_args()

    if args.review and args.dry_run:
        log("--review 和 --dry-run 互斥，请只选一个", "ERROR")
        sys.exit(1)

    ok = main(dry_run=args.dry_run, review=args.review,
              feedback=args.feedback, reset=args.reset)
    sys.exit(0 if ok else 1)
