#!/usr/bin/env python3
"""
GPU 算力新闻抓取器 v3
=====================
多源抓取：Google News RSS + 全文本 RSS 源 + 多引擎文章提取。
英文自动翻译。输出 news.js。

用法: python fetch_news.py
依赖: pip install feedparser deep-translator trafilatura requests newspaper3k
"""

import json, re, sys, io
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

try: import feedparser
except ImportError: print("pip install feedparser"); sys.exit(1)
try: import requests
except ImportError: print("pip install requests"); sys.exit(1)

# 文章提取器
HAS_TRAF, HAS_NEWS, HAS_BS4 = False, False, False
try: import trafilatura; HAS_TRAF = True
except ImportError: pass
try: from newspaper import Article; HAS_NEWS = True
except ImportError: pass
try: from bs4 import BeautifulSoup; HAS_BS4 = True
except ImportError: pass

# 翻译
HAS_TRANS = False
try:
    from deep_translator import GoogleTranslator
    HAS_TRANS = True
except ImportError:
    pass

OUTPUT = Path(__file__).parent / "news.js"
TIMEOUT = 12
MAX_NEWS = 20


# ====== 全文本 RSS 源（文章内容直接包含在 feed 中） ======
FULLTEXT_FEEDS = [
    ("https://techcrunch.com/category/artificial-intelligence/feed/", "TechCrunch AI", "en"),
    ("https://venturebeat.com/category/ai/feed/", "VentureBeat AI", "en"),
    ("https://www.theverge.com/rss/ai-artificial-intelligence/index.xml", "The Verge AI", "en"),
    ("https://feeds.arstechnica.com/arstechnica/index", "Ars Technica", "en"),
    ("https://www.36kr.com/feed", "36氪", "zh"),
    ("https://www.jiqizhixin.com/rss", "机器之心", "zh"),
]

# ====== Google News 搜索词 ======
GOOGLE_NEWS_QUERIES = [
    ("GPU 算力 租赁", "zh-CN"),
    ("GPU cloud rental price", "en"),
    ("NVIDIA GPU cloud computing", "en"),
    ("AI 算力 市场 云服务", "zh-CN"),
]


def clean_html(text: str) -> str:
    return re.sub(r'<[^>]+>', '', text).strip()


def resolve_url(url: str) -> str:
    try:
        r = requests.head(url, timeout=TIMEOUT, allow_redirects=True,
                          headers={"User-Agent": "Mozilla/5.0"})
        return r.url
    except Exception:
        return url


def fetch_rss(url: str) -> list[dict]:
    """通用 RSS 抓取"""
    try:
        feed = feedparser.parse(url)
    except Exception:
        return []
    results = []
    for e in feed.entries[:10]:
        title = e.get("title", "").strip()
        # 清理 Google News 标题格式 "Title - Source"
        if " - " in title:
            parts = title.rsplit(" - ", 1)
            title, source = parts[0].strip(), parts[1].strip()
        else:
            source = feed.feed.get("title", "")
        summary = clean_html(e.get("summary", e.get("description", "")))
        # 有些 RSS 提供 content:encoded（全文）
        content = ""
        if "content" in e:
            content = clean_html(e["content"][0].get("value", ""))
        elif "content:encoded" in e:
            content = clean_html(e["content:encoded"])
        results.append({
            "title": title, "source": source,
            "url": e.get("link", ""),
            "published": parse_date(e.get("published", "")),
            "summary": summary[:500],
            "full_text": content[:8000] if content else "",
            "lang": "zh" if any("一" <= c <= "鿿" for c in title[:20]) else "en",
        })
    return results


def parse_date(date_str: str) -> str:
    if not date_str:
        return ""
    try:
        from email.utils import parsedate_to_datetime
        return parsedate_to_datetime(date_str).strftime("%Y-%m-%d")
    except Exception:
        return date_str[:10] if len(date_str) >= 10 else date_str


def extract_article(url: str) -> dict:
    """多引擎文章提取：trafilatura → newspaper3k → BeautifulSoup"""
    html = None
    real_url = resolve_url(url)
    try:
        r = requests.get(real_url, timeout=TIMEOUT, headers={"User-Agent": "Mozilla/5.0"})
        if r.status_code == 200:
            html = r.text
    except Exception:
        pass

    if not html:
        return {}

    result = {}

    # 引擎 1: trafilatura
    if HAS_TRAF:
        try:
            doc = trafilatura.extract(html, output_format="json", with_metadata=True, include_images=True)
            if doc:
                d = json.loads(doc)
                text = d.get("text", "")
                if len(text) > 100:
                    result["full_text"] = text[:8000]
                imgs = d.get("images", [])
                if imgs:
                    result["images"] = [i.get("src", i) if isinstance(i, dict) else str(i) for i in imgs[:5]]
        except Exception:
            pass

    # 引擎 2: newspaper3k
    if (not result.get("full_text") or len(result["full_text"]) < 200) and HAS_NEWS:
        try:
            from newspaper import Config
            config = Config()
            config.browser_user_agent = "Mozilla/5.0"
            art = Article(real_url, config=config)
            art.download()
            art.parse()
            text = art.text
            if len(text) > 100:
                result["full_text"] = text[:8000]
            if not result.get("images") and art.top_image:
                result["images"] = [art.top_image]
            if art.images and not result.get("images"):
                result["images"] = list(art.images)[:5]
        except Exception:
            pass

    # 引擎 3: BeautifulSoup fallback
    if (not result.get("full_text") or len(result["full_text"]) < 200) and HAS_BS4:
        try:
            soup = BeautifulSoup(html, "html.parser")
            for tag in soup(["script", "style", "nav", "header", "footer", "aside"]):
                tag.decompose()
            text = soup.get_text()
            text = re.sub(r'\n{3,}', '\n\n', text).strip()
            if len(text) > 100:
                result["full_text"] = text[:8000]
            if not result.get("images"):
                imgs = []
                for img in soup.find_all("img", src=True)[:5]:
                    src = img["src"]
                    if src.startswith("http"):
                        imgs.append(src)
                if imgs:
                    result["images"] = imgs
        except Exception:
            pass

    return result


def translate(text: str) -> str:
    if not HAS_TRANS or not text:
        return ""
    try:
        if len(text) <= 4000:
            return GoogleTranslator(source='en', target='zh-CN').translate(text)
        chunks = []
        for i in range(0, len(text), 4000):
            chunks.append(GoogleTranslator(source='en', target='zh-CN').translate(text[i:i+4000]))
        return " ".join(chunks)
    except Exception:
        return ""


def main():
    print("=" * 60)
    print("📰 GPU 算力新闻抓取器 v3（多源+多引擎）")
    print(f"   提取器: trafilatura={HAS_TRAF} newspaper3k={HAS_NEWS} bs4={HAS_BS4}")
    print(f"   翻译器: {'✅' if HAS_TRANS else '❌'}")
    print("=" * 60)

    all_news, seen_urls, seen_titles = [], set(), set()

    # 1. 全文本 RSS 源
    print("\n📡 全文本 RSS 源:")
    for url, source, lang in FULLTEXT_FEEDS:
        print(f"   {source} ...")
        for a in fetch_rss(url):
            a["lang"] = lang
            a["source"] = source
            key = a["title"][:60]
            if key not in seen_titles:
                seen_titles.add(key)
                all_news.append(a)
        print(f"      ✅ {len(all_news)} 篇累计")

    # 2. Google News 搜索
    print("\n🔍 Google News:")
    for q, hl in GOOGLE_NEWS_QUERIES:
        url = f"https://news.google.com/rss/search?q={quote(q)}&hl={hl}&ceid={hl}"
        for a in fetch_rss(url):
            a["lang"] = "zh" if "zh" in hl else "en"
            key = a["title"][:60]
            if key not in seen_titles and a["url"] not in seen_urls:
                seen_titles.add(key)
                seen_urls.add(a["url"])
                all_news.append(a)
        print(f"   {q}: {len(all_news)} 篇累计")

    # 排序去重
    all_news.sort(key=lambda x: x.get("published", ""), reverse=True)
    all_news = all_news[:MAX_NEWS]
    print(f"\n📋 最终 {len(all_news)} 篇 (已去重排序)")

    # 3. 对没有全文的文章进行提取
    need_extract = [a for a in all_news if not a.get("full_text") or len(a["full_text"]) < 200]
    if need_extract:
        print(f"\n📄 文章提取 ({len(need_extract)} 篇需要)...")
        for i, a in enumerate(need_extract):
            full = extract_article(a["url"])
            if full.get("full_text"):
                a["full_text"] = full["full_text"]
            if full.get("images"):
                a["images"] = full["images"]
            n = len(a.get("full_text", ""))
            im = len(a.get("images", []))
            print(f"   {i+1}. {a['title'][:35]}... ({n}字, {im}图)")

    # 4. 翻译
    en_articles = [a for a in all_news if a["lang"] == "en"]
    if HAS_TRANS and en_articles:
        print(f"\n🌐 翻译 {len(en_articles)} 篇英文...")
        for a in en_articles:
            a["title_cn"] = translate(a["title"])
            a["summary_cn"] = translate(a["summary"]) if a.get("summary") else ""
            full = a.get("full_text", "")
            a["full_text_cn"] = translate(full) if len(full) > 200 else ""
            a["translated"] = True
            fc = len(a.get("full_text_cn", ""))
            print(f"   ✅ {a['title'][:35]}... (全文{fc}字)")
    else:
        for a in all_news:
            a["title_cn"] = a["summary_cn"] = a["full_text_cn"] = ""
            a["translated"] = False

    # 5. 统计
    zh = sum(1 for a in all_news if a["lang"] == "zh")
    en = sum(1 for a in all_news if a["lang"] == "en")
    ft = sum(1 for a in all_news if a.get("full_text") and len(a["full_text"]) > 200)
    im = sum(1 for a in all_news if a.get("images"))
    tr = sum(1 for a in all_news if a.get("translated"))

    # 6. 写入
    t = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(f"// GPU 算力新闻 v3\n// 生成: {t}\n")
        f.write(f"var NEWS_FETCHED_AT = \"{t}\";\nvar GPU_NEWS = ")
        json.dump(all_news, f, indent=2, ensure_ascii=False)
        f.write(";\n")

    print(f"\n{'='*60}")
    print(f"✅ {OUTPUT.name}: {len(all_news)} 篇")
    print(f"   中文{zh} | 英文{en} | 全文{ft} | 图片{im} | 翻译{tr}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
