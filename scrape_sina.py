#!/usr/bin/env python3
"""极简脚本：只抓取一篇 Sina 文章并写入 futures_news.js"""
import json, sys, io
from datetime import datetime, timezone
from pathlib import Path

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError as e:
    print(f"Missing dependency: {e}")
    sys.exit(1)

URL = "https://finance.sina.com.cn/wm/2026-05-16/doc-inhyahas2588021.shtml"
OUTPUT = Path(__file__).parent / "futures_news.js"

# 代理配置（从环境变量读取）
PROXY = None
import os
http_proxy = os.environ.get("HTTP_PROXY") or os.environ.get("http_proxy")
https_proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
if http_proxy:
    PROXY = {"http": http_proxy, "https": https_proxy or http_proxy}
    print(f"Using proxy: {http_proxy}")

print("=" * 50)
print("Scraping Sina article...")
print(URL)
print("=" * 50)

# 1. Fetch
try:
    r = requests.get(URL, timeout=20, proxies=PROXY, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/125.0.0.0 Safari/537.36"
    })
    r.raise_for_status()
    print(f"HTTP {r.status_code}, {len(r.text)} bytes")
except Exception as e:
    print(f"FETCH ERROR: {e}")
    sys.exit(1)

# 2. Parse
soup = BeautifulSoup(r.content, "html.parser")

# Title
title = ""
t = soup.find("title")
if t:
    title = t.get_text().strip()
    # Clean sina title format: "title|source|other"
    title = title.split("|")[0].split("_")[0].strip()
print(f"Title: {title[:80]}")

# Content
content = ""
for sel in ["#artibody", ".article-content", ".article-body", ".article", "article"]:
    div = soup.select_one(sel)
    if div:
        content = div.get_text().strip()
        if len(content) > 100:
            print(f"Found content in '{sel}': {len(content)} chars")
            break

if not content:
    # brute force: get body text, remove nav/header/footer
    body = soup.find("body")
    if body:
        for tag in body.find_all(["script", "style", "nav", "header", "footer", "aside"]):
            tag.decompose()
        content = body.get_text().strip()
        # Remove excessive whitespace
        lines = [l.strip() for l in content.split("\n") if l.strip()]
        content = "\n".join(lines)
        print(f"Body fallback: {len(content)} chars")

if len(content) < 100:
    print("ERROR: Could not extract article content!")
    sys.exit(1)

# 3. Date
pub_date = "2026-05-16"  # from URL

# 4. Build article
article = {
    "title": title,
    "source": "新浪财经",
    "url": URL,
    "published": pub_date,
    "summary": content[:400],
    "full_text": content[:8000],
    "lang": "zh",
    "title_cn": title,
    "summary_cn": content[:400],
    "full_text_cn": content[:8000],
    "translated": False,
    "images": [],
}

# 5. Merge with existing
existing = []
if OUTPUT.exists():
    try:
        raw = OUTPUT.read_text(encoding="utf-8")
        if "GPU_NEWS" in raw:
            import re
            m = re.search(r"GPU_NEWS\s*=\s*(\[.*\]);", raw, re.DOTALL)
            if m:
                existing = json.loads(m.group(1))
                print(f"Loaded {len(existing)} existing articles")
    except Exception:
        pass

# Deduplicate
existing_titles = {a["title"][:60] for a in existing}
if article["title"][:60] not in existing_titles:
    existing.insert(0, article)
    print("Added new article")
else:
    print("Article already exists, updating")
    for i, a in enumerate(existing):
        if a["title"][:60] == article["title"][:60]:
            existing[i] = article
            break

# Sort by date
existing.sort(key=lambda x: x.get("published", ""), reverse=True)

# 6. Write
t = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
OUTPUT.write_text(
    f"// GPU算力期货新闻\n// 生成:{t}\nvar NEWS_FETCHED_AT=\"{t}\";\nvar GPU_NEWS="
    + json.dumps(existing, indent=2, ensure_ascii=False)
    + ";\n",
    encoding="utf-8"
)
print(f"\nWritten {len(existing)} articles to {OUTPUT.name}")
print("DONE")
