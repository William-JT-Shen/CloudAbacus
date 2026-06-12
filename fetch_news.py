#!/usr/bin/env python3
"""
GPU 算力新闻抓取器 v2
=====================
从 Google News RSS 抓取新闻 + 全文提取 + 翻译。
输出 news.js 供网页加载。

用法: python fetch_news.py
依赖: pip install feedparser deep-translator trafilatura requests
"""

import json, re, sys, io
from datetime import datetime
from pathlib import Path
from urllib.parse import quote

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

try: import feedparser
except ImportError: print("pip install feedparser"); sys.exit(1)
try: import requests
except ImportError: print("pip install requests"); sys.exit(1)

HAS_TRAF = False
try:
    import trafilatura
    HAS_TRAF = True
except ImportError:
    print("⚠️ trafilatura 未安装，仅获取摘要 (pip install trafilatura)")

HAS_TRANS = False
try:
    from deep_translator import GoogleTranslator
    HAS_TRANS = True
except ImportError:
    print("⚠️ deep-translator 未安装，英文保留原文")

OUTPUT = Path(__file__).parent / "news.js"
QUERIES = [
    ("GPU 算力 租赁", "zh-CN"),
    ("GPU cloud computing rental", "en"),
    ("AI GPU 算力 市场", "zh-CN"),
    ("NVIDIA GPU cloud price", "en"),
]
MAX_NEWS = 15
TIMEOUT = 10


def clean_html(text: str) -> str:
    return re.sub(r'<[^>]+>', '', text).strip()


def fetch_rss(query: str, hl: str) -> list[dict]:
    url = f"https://news.google.com/rss/search?q={quote(query)}&hl={hl}&ceid={hl}"
    try:
        feed = feedparser.parse(url)
    except Exception:
        return []
    results = []
    for e in feed.entries[:8]:
        t = e.get("title", "")
        parts = t.rsplit(" - ", 1)
        title = parts[0].strip() if len(parts) > 1 else t
        source = parts[1].strip() if len(parts) > 1 else ""
        results.append({
            "title": title, "source": source,
            "url": e.get("link", ""),
            "published": parse_date(e.get("published", "")),
            "summary": clean_html(e.get("summary", ""))[:400],
            "lang": "zh" if "zh" in hl else "en",
        })
    return results


def resolve_url(url: str) -> str:
    """解析 Google News 重定向链接为真实 URL"""
    try:
        r = requests.head(url, timeout=TIMEOUT, allow_redirects=True, headers={"User-Agent": "Mozilla/5.0"})
        return r.url
    except Exception:
        return url


def scrape_article(url: str) -> dict:
    """提取全文和图片"""
    real_url = resolve_url(url)
    try:
        r = requests.get(real_url, timeout=TIMEOUT, headers={"User-Agent": "Mozilla/5.0"})
        if r.status_code != 200:
            return {}
        html = r.text
    except Exception:
        return {}

    result = {}
    if HAS_TRAF:
        try:
            doc = trafilatura.extract(html, output_format="json", with_metadata=True, include_images=True)
            if doc:
                d = json.loads(doc)
                result["full_text"] = d.get("text", "")[:5000]
                imgs = d.get("images", [])
                if imgs:
                    result["images"] = [i.get("src", i) if isinstance(i, dict) else str(i) for i in imgs[:3]]
        except Exception:
            pass

    # Fallback: 从 HTML 提取图片
    if "images" not in result:
        imgs = re.findall(r'<img[^>]+src="([^"]+)"', html)
        result["images"] = [u for u in imgs[:3] if u.startswith("http") and not u.endswith(".svg")]

    if "full_text" not in result:
        body = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
        body = re.sub(r'<style[^>]*>.*?</style>', '', body, flags=re.DOTALL)
        text = clean_html(body)
        text = re.sub(r'\n{3,}', '\n\n', text)
        result["full_text"] = text[:5000]

    return result


def translate(text: str) -> str:
    """翻译文本，自动分块处理长文本"""
    if not HAS_TRANS or not text:
        return ""
    try:
        translator = GoogleTranslator(source='en', target='zh-CN')
        if len(text) <= 4000:
            return translator.translate(text)
        # 分块翻译
        chunks = []
        for i in range(0, len(text), 4000):
            chunk = text[i:i+4000]
            chunks.append(translator.translate(chunk))
        return " ".join(chunks)
    except Exception:
        return ""


def parse_date(date_str: str) -> str:
    """解析 RFC 2822 日期为 YYYY-MM-DD"""
    if not date_str:
        return ""
    try:
        from email.utils import parsedate_to_datetime
        return parsedate_to_datetime(date_str).strftime("%Y-%m-%d")
    except Exception:
        return date_str[:10] if len(date_str) >= 10 else date_str


def main():
    print("=" * 50)
    print("📰 GPU 算力新闻抓取器 v2")
    print("=" * 50)

    all_news, seen = [], set()
    for q, hl in QUERIES:
        print(f"🔍 {q}")
        for a in fetch_rss(q, hl):
            key = a["url"].split("?")[0]
            if key not in seen and a["title"]:
                seen.add(key)
                all_news.append(a)
        print(f"   ✅ {len(all_news)} 篇累计")

    all_news.sort(key=lambda x: x.get("published", ""), reverse=True)
    all_news = all_news[:MAX_NEWS]

    # 全文抓取
    en_count = sum(1 for a in all_news if a["lang"] == "en")
    print(f"\n📄 抓取全文 ({len(all_news)} 篇)...")
    for i, a in enumerate(all_news):
        real = resolve_url(a["url"])
        if real != a["url"]:
            a["source_url"] = a["url"]
            a["url"] = real
        full = scrape_article(a["url"])
        a["full_text"] = full.get("full_text", "")
        a["images"] = full.get("images", [])
        n = len(a.get('full_text',''))
        im = len(a.get('images',[]))
        print(f"   {i+1}. {a['title'][:40]}...  ({n} 字, {im} 图)")

    # 翻译（标题+摘要+全文都翻）
    if HAS_TRANS:
        to_translate = sum(1 for a in all_news if a["lang"] == "en")
        if to_translate > 0:
            print(f"\n🌐 翻译 {to_translate} 篇英文（标题+摘要+全文）...")
        for a in all_news:
            if a["lang"] == "en":
                a["title_cn"] = translate(a["title"])
                a["summary_cn"] = translate(a["summary"])
                full = a.get("full_text", "")
                a["full_text_cn"] = translate(full) if len(full) > 50 else ""
                a["translated"] = bool(a.get("title_cn"))
                print(f"   ✅ {a['title'][:40]}... ({len(a.get('full_text_cn',''))}字)")
            else:
                a["title_cn"] = a["summary_cn"] = a["full_text_cn"] = ""
                a["translated"] = False
    else:
        for a in all_news:
            a["title_cn"] = a["summary_cn"] = a["full_text_cn"] = ""
            a["translated"] = False

    # 写入
    t = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(f"// GPU 算力新闻 v2\n// 生成: {t}\n")
        f.write(f"var NEWS_FETCHED_AT = \"{t}\";\nvar GPU_NEWS = ")
        json.dump(all_news, f, indent=2, ensure_ascii=False)
        f.write(";\n")

    zh = sum(1 for a in all_news if a["lang"] == "zh")
    tr = sum(1 for a in all_news if a.get("translated"))
    ft = sum(1 for a in all_news if a.get("full_text"))
    im = sum(1 for a in all_news if a.get("images"))
    print(f"\n✅ {OUTPUT.name}: {len(all_news)} 篇 (中文{zh} 英文{en_count} 翻译{tr})")
    print(f"   有全文: {ft} | 有图片: {im}")


if __name__ == "__main__":
    main()
