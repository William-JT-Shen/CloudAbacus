#!/usr/bin/env python3
"""
GPU 算力新闻抓取器
==================
从 Google News RSS 免费抓取中英文 GPU 算力相关新闻，
英文新闻通过 deep-translator 翻译为中文，输出为 news.js

用法:
  python fetch_news.py

依赖:
  pip install feedparser deep-translator
"""

import json
import re
import sys
import io
from datetime import datetime
from pathlib import Path
from urllib.parse import quote

# Windows 编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

try:
    import feedparser
except ImportError:
    print("请安装: pip install feedparser deep-translator")
    sys.exit(1)

# 尝试导入翻译库
HAS_TRANSLATOR = False
try:
    from deep_translator import GoogleTranslator
    HAS_TRANSLATOR = True
except ImportError:
    pass

OUTPUT_FILE = Path(__file__).parent / "news.js"
MAX_NEWS = 20  # 最多保留条数

# 搜索关键词（中英文）
QUERIES = [
    ("GPU 算力 租赁", "zh-CN"),
    ("GPU cloud computing rental price", "en"),
    ("GPU 云计算 价格", "zh-CN"),
    ("AI GPU 算力 市场", "zh-CN"),
    ("NVIDIA GPU cloud service", "en"),
]


def fetch_google_news(query: str, hl: str = "zh-CN") -> list[dict]:
    """从 Google News RSS 抓取新闻"""
    url = f"https://news.google.com/rss/search?q={quote(query)}&hl={hl}&ceid={hl}"
    try:
        feed = feedparser.parse(url)
    except Exception as e:
        print(f"  ⚠️ RSS 抓取失败 ({query}): {e}")
        return []

    results = []
    for entry in feed.entries[:10]:
        title = entry.get("title", "")
        # Google News title 格式: "标题 - 来源"
        parts = title.rsplit(" - ", 1)
        real_title = parts[0].strip() if len(parts) > 1 else title
        source = parts[1].strip() if len(parts) > 1 else ""

        results.append({
            "title": real_title,
            "source": source,
            "url": entry.get("link", ""),
            "published": entry.get("published", ""),
            "summary": clean_html(entry.get("summary", "")),
            "lang": "zh" if "zh" in hl else "en",
        })
    return results


def clean_html(text: str) -> str:
    """去除 HTML 标签"""
    return re.sub(r'<[^>]+>', '', text).strip()[:300]


def translate_to_chinese(text: str) -> str:
    """将英文翻译为中文"""
    if not HAS_TRANSLATOR or not text:
        return text
    try:
        result = GoogleTranslator(source='en', target='zh-CN').translate(text[:500])
        return result
    except Exception:
        return text


def main():
    print("=" * 50)
    print("📰 GPU 算力新闻抓取器")
    print("=" * 50)

    all_news = []
    seen_urls = set()

    for query, hl in QUERIES:
        print(f"🔍 搜索: {query} (hl={hl})")
        articles = fetch_google_news(query, hl)
        new_count = 0
        for a in articles:
            if a["url"] not in seen_urls and a["title"]:
                seen_urls.add(a["url"])
                all_news.append(a)
                new_count += 1
        print(f"   ✅ {new_count} 篇新文章")

    # 去重 + 排序（按时间倒序）
    all_news.sort(key=lambda x: x.get("published", ""), reverse=True)
    all_news = all_news[:MAX_NEWS]

    # 翻译英文文章
    if HAS_TRANSLATOR:
        en_count = sum(1 for a in all_news if a["lang"] == "en")
        if en_count > 0:
            print(f"\n🌐 翻译 {en_count} 篇英文文章...")
            for a in all_news:
                if a["lang"] == "en":
                    zh_title = translate_to_chinese(a["title"])
                    zh_summary = translate_to_chinese(a["summary"])
                    a["title_cn"] = zh_title if zh_title != a["title"] else ""
                    a["summary_cn"] = zh_summary if zh_summary != a["summary"] else ""
                    a["translated"] = bool(a.get("title_cn"))
                    print(f"   ✅ {a['title'][:50]}...")
    else:
        print("\n⚠️ deep-translator 未安装，英文文章保留原文")
        print("   安装: pip install deep-translator")
        for a in all_news:
            a["title_cn"] = ""
            a["summary_cn"] = ""
            a["translated"] = False

    # 写入 news.js
    fetched_at = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("// GPU 算力新闻数据\n")
        f.write(f"// 自动生成于: {fetched_at}\n")
        f.write(f"var NEWS_FETCHED_AT = \"{fetched_at}\";\n")
        f.write("var GPU_NEWS = ")
        json.dump(all_news, f, indent=2, ensure_ascii=False)
        f.write(";\n")

    print(f"\n✅ 输出: {OUTPUT_FILE.name}")
    print(f"📊 共 {len(all_news)} 篇文章")
    zh = sum(1 for a in all_news if a["lang"] == "zh")
    en = sum(1 for a in all_news if a["lang"] == "en")
    tr = sum(1 for a in all_news if a.get("translated"))
    print(f"   中文: {zh} | 英文: {en} | 已翻译: {tr}")


if __name__ == "__main__":
    main()
