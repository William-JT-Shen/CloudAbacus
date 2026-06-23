#!/usr/bin/env python3
"""
GPU 算力租赁新闻抓取器 v4
=========================
Google News RSS 站内搜索 → 元数据提取 → 翻译 → 输出 news.js

用法: python fetch_news.py
依赖: pip install feedparser deep-translator requests beautifulsoup4
"""

import json, re, sys, io, os
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

try:
    import requests
except ImportError:
    print("pip install requests"); sys.exit(1)
try:
    from bs4 import BeautifulSoup; HAS_BS4 = True
except ImportError:
    HAS_BS4 = False

try:
    import feedparser; HAS_FEED = True
except ImportError:
    HAS_FEED = False
try:
    from deep_translator import GoogleTranslator; HAS_TRANS = True
except ImportError:
    HAS_TRANS = False

OUTPUT = Path(__file__).parent / "news.js"
TIMEOUT = 15

# ====== HTTP 代理 ======
PROXY = None
http_proxy = os.environ.get("HTTP_PROXY") or os.environ.get("http_proxy")
if http_proxy:
    PROXY = {"http": http_proxy, "https": os.environ.get("HTTPS_PROXY", http_proxy)}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "Chrome/125.0.0.0 Safari/537.36"
}

# ====== Google News RSS 搜索词（聚焦 GPU 算力租赁） ======
GOOGLE_NEWS_QUERIES = [
    # 中文：站内精准搜索
    ("site:36kr.com GPU 算力 租赁", "zh-CN"),
    ("site:finance.sina.com.cn GPU 算力 租赁 价格", "zh-CN"),
    ("site:eastmoney.com 算力 租赁", "zh-CN"),
    ("site:jiqizhixin.com GPU 算力 租赁", "zh-CN"),
    # 中文精准搜索
    ("GPU 算力 租赁 价格 市场", "zh-CN"),
    ("H100 A100 GPU 租赁 云服务", "zh-CN"),
    ("GPU 云 服务器 租用 价格", "zh-CN"),
    ("AI 算力 租用 成本 定价", "zh-CN"),
    ("NVIDIA GPU 云计算 租赁 市场", "zh-CN"),
    ("CoreWeave GPU 算力 租赁", "zh-CN"),
    # 英文精准搜索
    ("GPU cloud rental pricing market", "en"),
    ("H100 A100 GPU instance pricing comparison", "en"),
    ("GPU compute rental cloud provider", "en"),
    ("CoreWeave RunPod Vast.ai GPU pricing", "en"),
    ("GPU cloud computing cost benchmark", "en"),
    ("NVIDIA GPU server rental data center", "en"),
]

# ====== 相关性过滤：必须同时命中 租赁/价格类 ∩ GPU/算力类 ======
RENTAL_TERMS = [
    "rent", "rental", "租赁", "租用", "price", "pricing", "价格", "定价",
    "cost", "费用", "成本", "instance", "实例", "provider", "供应商",
    "market", "市场", "cloud", "云", "server", "服务器", "hosting",
    "deploy", "部署", "cluster", "集群", "platform", "平台",
]
COMPUTE_TERMS = [
    "gpu", "算力", "compute", "computing", "nvidia", "英伟达",
    "h100", "a100", "h200", "b200", "amd instinct", "tpu",
    "coreweave", "vast.ai", "runpod", "lambda labs", "tensordock",
    "paperspace", "datacrunch", "ai", "人工智能", "machine learning",
    "chip", "芯片", "processor", "data center", "数据中心",
]

# ====== 专有名词还原 ======
PROPER_NOUNS = {
    "克劳德·费布尔": "Claude Fable", "克劳德": "Claude", "聊天 GPT": "ChatGPT",
    "开放人工智能": "OpenAI", "人类": "Anthropic", "英伟达": "NVIDIA",
    "谷歌": "Google", "微软": "Microsoft", "太空探索": "SpaceX",
    "核心编织": "CoreWeave", "运行舱": "RunPod", "浩瀚": "Vast.ai",
    "张量码头": "TensorDock", "拉姆达实验室": "Lambda Labs",
}


# ==================== 工具函数 ====================

def clean_html(text: str) -> str:
    return re.sub(r'<[^>]+>', '', text).strip()


def parse_date(date_str: str) -> str:
    if not date_str:
        return ""
    try:
        from email.utils import parsedate_to_datetime
        return parsedate_to_datetime(date_str).strftime("%Y-%m-%d")
    except Exception:
        return date_str[:10] if len(date_str) >= 10 else date_str


def detect_lang(text: str) -> str:
    if not text:
        return "en"
    cn_chars = sum(1 for c in text[:50] if '一' <= c <= '鿿')
    return "zh" if cn_chars >= 2 else "en"


def translate(text: str) -> str:
    if not HAS_TRANS or not text:
        return ""
    try:
        from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeout
        def _do_translate(t):
            if len(t) <= 4000:
                return GoogleTranslator(source='en', target='zh-CN').translate(t)
            chunks = []
            for i in range(0, len(t), 4000):
                chunks.append(GoogleTranslator(source='en', target='zh-CN')
                              .translate(t[i:i + 4000]))
            return " ".join(chunks)

        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(_do_translate, text)
            result = future.result(timeout=20)
        for cn, en in PROPER_NOUNS.items():
            result = result.replace(cn, en)
        return result
    except (FuturesTimeout, Exception):
        return ""


def build_rich_fallback(title: str, source: str, published: str,
                        lang: str, title_cn: str = "") -> str:
    """构建有意义的 fallback 正文"""
    display_title = title_cn or title
    if lang == "zh":
        return (
            f"「{display_title}」\n\n"
            f"来源：{source}\n"
            f"发布日期：{published}\n\n"
            f"本文由 Google News 聚合自 {source}。"
            f"点击卡片可跳转到原始文章页面阅读完整内容。\n\n"
            f"本栏目聚焦 GPU 算力租赁市场动态，"
            f"涵盖 H100/A100/H200/B200 等 GPU 云租赁价格、"
            f"CoreWeave/RunPod/Vast.ai/Lambda Labs 等平台定价、"
            f"以及 GPU 云计算市场的供需变化与成本趋势。"
        )
    else:
        return (
            f"「{display_title}」\n\n"
            f"Source: {source}\n"
            f"Published: {published}\n\n"
            f"Original: {title}\n\n"
            f"This article is aggregated from {source} via Google News. "
            f"Click the card to read the full article. "
            f"The Google News link will redirect you to the original page.\n\n"
            f"This section covers GPU compute rental market trends, "
            f"including H100/A100/H200/B200 cloud pricing, "
            f"CoreWeave/RunPod/Vast.ai/Lambda Labs rates, "
            f"and GPU cloud supply-demand dynamics."
        )


# ==================== RSS 抓取 ====================

def fetch_google_news_rss(query: str, hl: str) -> list[dict]:
    """从 Google News RSS 搜索文章 (带超时的 requests + feedparser)"""
    if not HAS_FEED:
        return []
    rss_url = f"https://news.google.com/rss/search?q={quote(query)}&hl={hl}&ceid={hl}"
    try:
        # 先用 requests 获取 RSS XML（带超时），再用 feedparser 解析
        r = requests.get(rss_url, timeout=TIMEOUT, headers=HEADERS, proxies=PROXY)
        if r.status_code != 200:
            print(f"   ⚠ HTTP {r.status_code} for: {query[:40]}")
            return []
        feed = feedparser.parse(r.content)
    except requests.Timeout:
        print(f"   ⏱ timeout ({TIMEOUT}s): {query[:40]}")
        return []
    except requests.RequestException as e:
        print(f"   ❌ network error: {type(e).__name__} for: {query[:40]}")
        return []
    except Exception:
        return []

    results = []
    for e in feed.entries[:10]:
        raw_title = e.get("title", "").strip()
        if " - " in raw_title:
            parts = raw_title.rsplit(" - ", 1)
            title = parts[0].strip()
            rss_source = parts[1].strip()
        else:
            title = raw_title
            rss_source = ""

        source_name = rss_source
        source_url = ""
        if "source" in e:
            source_name = e.source.get("title", source_name)
            source_url = e.source.get("href", "")

        gn_link = e.get("link", "")
        published = parse_date(e.get("published", ""))
        article_lang = "zh" if "zh" in hl else detect_lang(title)
        rss_summary = clean_html(e.get("summary", e.get("description", "")))

        results.append({
            "title": title,
            "source": source_name,
            "source_url": source_url,
            "url": gn_link,
            "published": published,
            "summary": rss_summary,
            "full_text": "",
            "images": [],
            "lang": article_lang,
        })
    return results


# ==================== 标准化 ====================

def normalize_article(a: dict) -> dict:
    """确保文章拥有所有必需字段"""
    defaults = {
        "title": "", "source": "", "source_url": "", "url": "",
        "published": "", "summary": "", "full_text": "", "images": [],
        "lang": "zh", "title_cn": "", "summary_cn": "", "translated": False,
    }
    for k, v in defaults.items():
        if k not in a:
            a[k] = v

    if not a.get("full_text") or len(a["full_text"]) < 80:
        a["full_text"] = build_rich_fallback(
            a.get("title", ""), a.get("source", ""),
            a.get("published", ""), a.get("lang", "zh"),
            a.get("title_cn", ""),
        )
    return a


# ==================== 主流程 ====================

def main():
    print("=" * 60)
    print("GPU 算力租赁新闻抓取器 v4")
    print(f"   feedparser={HAS_FEED} bs4={HAS_BS4} translate={'OK' if HAS_TRANS else 'NO'}")
    print("=" * 60)

    all_news = []
    seen_titles = set()

    # ---- Step 1: Google News RSS ----
    print("\nGoogle News RSS:")
    for query, hl in GOOGLE_NEWS_QUERIES:
        articles = fetch_google_news_rss(query, hl)
        added = 0
        for a in articles:
            key = a["title"][:60]
            if key not in seen_titles:
                seen_titles.add(key)
                all_news.append(a)
                added += 1
        print(f"   [{query[:45]}]: +{added} ({len(all_news)} total)")

    # ---- Step 2: 相关性过滤 (rental AND compute) ----
    filtered = []
    for a in all_news:
        text = (a.get("title", "") + " " + a.get("summary", "")).lower()
        has_rental = any(kw.lower() in text for kw in RENTAL_TERMS)
        has_compute = any(kw.lower() in text for kw in COMPUTE_TERMS)
        if has_rental and has_compute:
            filtered.append(a)
    if filtered:
        all_news = filtered
    print(f"\nAfter filter (rental AND compute): {len(all_news)} articles")

    # ---- Step 3: 翻译英文标题 ----
    en_articles = [a for a in all_news if a.get("lang") == "en"]
    if HAS_TRANS and en_articles:
        print(f"\nTranslating {len(en_articles)} English titles...")
        for a in en_articles:
            a["title_cn"] = translate(a["title"])
            a["summary_cn"] = translate(a.get("summary", "")) if a.get("summary") else ""
            a["translated"] = True
            print(f"   OK: {a['title'][:55]}...")
    else:
        for a in all_news:
            a["title_cn"] = a["summary_cn"] = ""
            a["translated"] = False

    # ---- Step 4: 标准化 + 构建 fallback ----
    for a in all_news:
        normalize_article(a)

    # ---- Step 5: 翻译英文 fallback 正文 ----
    if HAS_TRANS:
        for a in en_articles:
            ft = a.get("full_text", "")
            if ft and len(ft) < 1500:
                translated_body = translate(ft)
                if translated_body:
                    a["full_text_cn"] = translated_body

    # ---- Step 6: 合并旧数据 ----
    existing = []
    if OUTPUT.exists():
        try:
            raw = OUTPUT.read_text(encoding="utf-8")
            m = re.search(r'GPU_NEWS\s*=\s*(\[.*\]);', raw, re.DOTALL)
            if m:
                existing_data = json.loads(m.group(1))
                for a in existing_data:
                    normalize_article(a)
                existing = existing_data
                print(f"\nLoaded {len(existing)} existing articles")
        except Exception:
            pass

    existing_titles = {a["title"][:60] for a in existing}
    new_added = 0
    for a in all_news:
        if a["title"][:60] not in existing_titles:
            existing.insert(0, a)
            existing_titles.add(a["title"][:60])
            new_added += 1

    # 按发布日期倒序（最新在前）
    existing.sort(key=lambda x: x.get("published", ""), reverse=True)
    all_news = existing[:50]

    if len(all_news) == 0 and existing:
        print("   WARNING: no new articles, keeping existing data")
        all_news = existing

    print(f"   +{new_added} new, {len(all_news)} total")

    # ---- Step 7: 统计 ----
    zh = sum(1 for a in all_news if a.get("lang") == "zh")
    en = sum(1 for a in all_news if a.get("lang") == "en")
    tr = sum(1 for a in all_news if a.get("translated"))

    # ---- Step 8: 写入 news.js ----
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(f"// GPU算力租赁新闻 v4\n// Generated: {ts}\n")
        f.write(f"var NEWS_FETCHED_AT = \"{ts}\";\nvar GPU_NEWS = ")
        json.dump(all_news, f, indent=2, ensure_ascii=False)
        f.write(";\n")

    print(f"\n{'=' * 60}")
    print(f"Done: {OUTPUT.name}  {len(all_news)} articles")
    print(f"  CN:{zh}  EN:{en}  Translated:{tr}")
    print(f"  Generated: {ts}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
