#!/usr/bin/env python3
"""
add_article.py — 手动单篇导入脚本

用法：
  python3 add_article.py "https://mp.weixin.qq.com/s?__biz=...&sn=..."
  python3 add_article.py --dry-run "https://mp.weixin.qq.com/s/..."

职责：
  1. 抓取微信文章全文（直接 HTTP）
  2. HTML 转 Markdown，写入 raw/YYYY-MM/YYYY-MM-DD_标题.md
  3. 追加写入 logs/ops.md
  4. 更新 logs/fetch_state.json（避免日后 fetch_articles.py 重复入库）
  5. git commit + push
"""

import sys
import re
import subprocess
import argparse
from datetime import datetime, timezone, timedelta
from pathlib import Path

# 复用 fetch_articles.py 中的所有工具函数
sys.path.insert(0, str(Path(__file__).parent))
import fetch_articles as fa

CST = timezone(timedelta(hours=8))

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/125.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9",
}


def fetch_article_html(url):
    """直接抓微信文章 HTML"""
    import urllib.request
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read().decode("utf-8")


def extract_meta(html, url):
    """从微信文章 HTML 提取标题、发布日期、正文"""

    # 标题：og:title 或 <h1>
    title = ""
    m = re.search(r'<meta[^>]+property=["\']og:title["\'][^>]+content=["\']([^"\']+)["\']', html)
    if m:
        title = m.group(1).strip()
    if not title:
        m = re.search(r'<h1[^>]*class=["\'][^"\']*rich_media_title[^"\']*["\'][^>]*>(.*?)</h1>', html, re.DOTALL)
        if m:
            title = fa._strip_tags(m.group(1)).strip()
    if not title:
        m = re.search(r'<title>(.*?)</title>', html)
        if m:
            title = fa._strip_tags(m.group(1)).strip()
    title = fa._unescape(title)

    # 发布日期：var ct = "1234567890"（unix timestamp）
    pub_date_str = fa.today_str()
    m = re.search(r'var ct\s*=\s*["\'](\d+)["\']', html)
    if m:
        ts = int(m.group(1))
        pub_date_str = datetime.fromtimestamp(ts, tz=CST).strftime("%Y-%m-%d")
    else:
        # 备选：publish_time
        m = re.search(r'publish_time\s*=\s*["\'](\d+)["\']', html)
        if m:
            ts = int(m.group(1))
            pub_date_str = datetime.fromtimestamp(ts, tz=CST).strftime("%Y-%m-%d")

    # 正文：id="js_content"，找到开口后向后截取到常见结束标记
    content_html = ""
    m = re.search(r'id=["\']js_content["\'][^>]*>(.*)', html, re.DOTALL)
    if m:
        body = m.group(1)
        for end in ['id="js_article_comment"', "id='js_article_comment'",
                    'id="js_content_bottom"', '</body>']:
            idx = body.find(end)
            if idx > 0:
                body = body[:idx]
                break
        content_html = body

    return title, pub_date_str, content_html


def main():
    parser = argparse.ArgumentParser(description="手动导入单篇微信文章")
    parser.add_argument("url", help="微信文章 URL")
    parser.add_argument("--dry-run", action="store_true", help="只打印，不写文件不提交")
    args = parser.parse_args()

    url = args.url.strip()
    dry_run = args.dry_run

    fa.log(f"=== 开始手动导入 {'[DRY-RUN] ' if dry_run else ''}===")
    fa.log(f"URL: {url}")

    # 1. 检查是否已导入
    state = fa.load_state()
    fetched_ids = set(state["fetched_ids"])
    aid = fa.article_id(url, "")
    if aid in fetched_ids:
        fa.log(f"已存在，跳过（ID={aid}）", "WARN")
        return

    # 2. 抓取 HTML
    fa.log("抓取文章...")
    html = fetch_article_html(url)
    fa.log(f"HTML 大小: {len(html):,} 字节")

    # 3. 提取元数据
    title, pub_date_str, content_html = extract_meta(html, url)
    fa.log(f"标题: {title}")
    fa.log(f"日期: {pub_date_str}")
    fa.log(f"正文 HTML: {len(content_html):,} 字节")

    if not title:
        fa.log("无法提取标题，请检查 URL 或页面结构", "ERROR")
        sys.exit(1)

    # 4. 筛选审核：标题过一遍自动筛选规则
    filter_reason = fa._filter_reason(title)
    if filter_reason:
        fa.log(f"⚠️  自动筛选建议：跳过（{filter_reason}）", "WARN")
        fa.log("   手动导入不受自动筛选限制，但建议确认后再入库")
    else:
        fa.log("✅  自动筛选通过")

    # 5. 构造文章对象，复用 save_article
    article = {
        "id": fa.article_id(url, title),
        "title": title,
        "link": url,
        "pub_date_str": pub_date_str,
        "content_html": content_html,
    }

    path = fa.save_article(article, dry_run=dry_run)
    fa.log(f"保存: {path}")

    # 5. 更新状态
    if not dry_run:
        fetched_ids.add(article["id"])
        state["fetched_ids"] = list(fetched_ids)
        state["total_count"] = state.get("total_count", 0) + 1
        state["last_run"] = fa.now_str()
        fa.save_state(state)
        fa.update_project_md(state["total_count"])

    # 6. 写日志
    run_result = {
        "run_time": fa.now_str(),
        "status": "success",
        "new_count": 1,
        "feed_total": 1,
        "total_fetched": state.get("total_count", 1),
        "new_articles": [article],
        "error": None,
    }
    entry = fa.append_ops_log(run_result, dry_run=dry_run)
    if dry_run:
        print("\n--- ops.md 将追加 ---")
        print(entry)

    # 7. Git commit + push
    if not dry_run:
        import os
        os.chdir(fa.ROOT)
        files = [
            str(fa.STATE_FILE.relative_to(fa.ROOT)),
            str(fa.OPS_LOG.relative_to(fa.ROOT)),
            str(fa.PROJECT_MD.relative_to(fa.ROOT)),
        ]
        year_month = pub_date_str[:7]
        files.append(f"raw/{year_month}/{pub_date_str}_{fa.safe_filename(title)}.md")

        subprocess.run(["git", "add"] + files, check=True)
        subprocess.run(["git", "commit", "-m", f"feat(raw): 手动导入 — {title[:40]}"], check=True)
        result = subprocess.run(["git", "push"], capture_output=True, text=True)
        if result.returncode == 0:
            fa.log("git push 成功")
        else:
            fa.log(f"git push 失败: {result.stderr}", "ERROR")

    fa.log("=== 导入完成 ===")


if __name__ == "__main__":
    main()
