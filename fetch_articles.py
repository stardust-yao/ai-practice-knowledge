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

CST = timezone(timedelta(hours=8))  # 北京时间

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


# ── 主流程 ────────────────────────────────────────────────────────────────────

def main(dry_run=False):
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

        if not new_articles:
            run_result["status"] = "success_no_new"
            log("无新文章，正常退出")
        else:
            # 5. 保存文章
            for a in new_articles:
                path = save_article(a, dry_run=dry_run)
                log(f"  保存: {path.relative_to(ROOT) if not dry_run else path}")
                fetched_ids.add(a["id"])

            # 6. 更新状态文件
            state["fetched_ids"] = list(fetched_ids)
            state["total_count"] = state.get("total_count", 0) + len(new_articles)
            state["last_run"] = run_result["run_time"]
            if not dry_run:
                save_state(state)

            # 7. 更新 PROJECT.md
            update_project_md(state["total_count"], dry_run=dry_run)

            run_result["total_fetched"] = state["total_count"]
            run_result["status"] = "success"

            # 8. Git commit + push
            git_commit_push(new_articles, dry_run=dry_run)

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
    args = parser.parse_args()

    ok = main(dry_run=args.dry_run)
    sys.exit(0 if ok else 1)
