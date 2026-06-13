#!/usr/bin/env python3
"""抓取国外 GPU 算力期货新闻（CME/Nasdaq/Benzinga 等权威来源）"""
import json, sys, io, os, re
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

OUTPUT = Path(__file__).parent / "futures_news.js"
PROXY = None
http_proxy = os.environ.get("HTTP_PROXY") or os.environ.get("http_proxy")
if http_proxy:
    PROXY = {"http": http_proxy, "https": os.environ.get("HTTPS_PROXY", http_proxy)}

# 权威来源 URL
SOURCES = [
    {
        "url": "https://www.cmegroup.com/media-room/press-releases/2026/5/12/cme_group_and_silicondatapartnertolaunchfirstcomputefutures.html",
        "source": "CME Group",
        "date": "2026-05-12",
    },
    {
        "url": "https://www.nasdaq.com/articles/cme-group-expanding-compute-futures-market",
        "source": "Nasdaq",
        "date": "2026-05-13",
    },
    {
        "url": "https://www.benzinga.com/news/topics/26/05/52762722/place-your-bets-futures-traders-are-about-to-see-the-launch-of-ai-semiconductor-contracts",
        "source": "Benzinga",
        "date": "2026-05-13",
    },
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/125.0.0.0 Safari/537.36"
}


def fetch_page(url):
    try:
        r = requests.get(url, timeout=20, proxies=PROXY, headers=HEADERS)
        if r.status_code == 200 and len(r.text) > 2000:
            return r.content
    except Exception as e:
        print(f"  FETCH ERROR: {e}")
    return None


def extract_article(html_bytes, url):
    soup = BeautifulSoup(html_bytes, "html.parser")

    # Title
    title = ""
    t = soup.find("title")
    if t:
        title = t.get_text().strip().split("|")[0].split(" - ")[0].strip()

    # Content - try multiple selectors
    content = ""
    selectors = [
        "article", ".article-body", ".article-content", ".post-content",
        "#article-body", ".entry-content", "main", "[role='main']",
        ".body-content", ".press-release-content",
    ]
    for sel in selectors:
        div = soup.select_one(sel)
        if div:
            text = div.get_text().strip()
            if len(text) > 200:
                content = text
                break

    if not content:
        body = soup.find("body")
        if body:
            for tag in body.find_all(["script", "style", "nav", "header", "footer", "aside"]):
                tag.decompose()
            lines = [l.strip() for l in body.get_text().split("\n") if l.strip()]
            content = "\n".join(lines)

    # Get meta description as summary
    summary = ""
    meta = soup.find("meta", attrs={"name": "description"})
    if meta and meta.get("content"):
        summary = meta["content"].strip()

    return {
        "title": title or url.split("/")[-1],
        "content": content,
        "summary": summary or (content[:400] if content else ""),
    }


def main():
    print("=" * 50)
    print("Scraping GPU Compute Futures news...")
    print("=" * 50)

    new_articles = []
    for src in SOURCES:
        print(f"\n📄 {src['source']}: {src['url'][:60]}...")
        html = fetch_page(src["url"])
        if not html:
            print("  ❌ Failed to fetch")
            continue
        print(f"  ✅ {len(html)} bytes")

        article = extract_article(html, src["url"])
        cl = len(article["content"])
        print(f"  Title: {article['title'][:80]}")
        print(f"  Content: {cl} chars")

        if cl < 100:
            print("  ⚠️ Content too short, skipping")
            continue

        new_articles.append({
            "title": article["title"],
            "source": src["source"],
            "url": src["url"],
            "published": src["date"],
            "summary": article["summary"],
            "full_text": article["content"][:8000],
            "lang": "en",
            "title_cn": "",
            "summary_cn": "",
            "full_text_cn": "",
            "translated": False,
        })

    if not new_articles:
        print("\n❌ No articles scraped!")
        return

    # Merge with existing
    existing = []
    if OUTPUT.exists():
        try:
            raw = OUTPUT.read_text(encoding="utf-8")
            m = re.search(r"GPU_NEWS\s*=\s*(\[.*\]);", raw, re.DOTALL)
            if m:
                existing = json.loads(m.group(1))
        except Exception:
            pass

    et = {a["title"][:60] for a in existing}
    added = 0
    for a in new_articles:
        if a["title"][:60] not in et:
            existing.insert(0, a)
            et.add(a["title"][:60])
            added += 1
    existing.sort(key=lambda x: x.get("published", ""), reverse=True)

    t = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    OUTPUT.write_text(
        f"// GPU算力期货新闻\n// 生成:{t}\nvar NEWS_FETCHED_AT=\"{t}\";\nvar GPU_NEWS="
        + json.dumps(existing, indent=2, ensure_ascii=False)
        + ";\n",
        encoding="utf-8",
    )
    print(f"\n✅ {OUTPUT.name}: {len(existing)} articles ({added} new)")


if __name__ == "__main__":
    main()
