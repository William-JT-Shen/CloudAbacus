#!/usr/bin/env python3
"""
GPU 算力期货新闻抓取器 v3
=========================
策略：
  1. 已知可抓取源 → 直接提取全文
  2. Google News RSS → 元数据（标题/来源/日期）+ 浏览器跳转链接
  3. 正文缺省时 → 用标题+摘要+来源构建有意义的 fallback 内容
  4. 英文文章 → Google 翻译标题

输出 futures_news.js，格式与 news.js 一致。

用法: python fetch_futures.py
依赖: pip install feedparser deep-translator requests beautifulsoup4
"""

import json, re, sys, io, os
from datetime import datetime, timezone, timedelta
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

OUTPUT = Path(__file__).parent / "futures_news.js"
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

# ====== Google News RSS 搜索词 ======
GOOGLE_NEWS_QUERIES = [
    ("site:finance.sina.com.cn 算力 期货", "zh-CN"),
    ("site:eastmoney.com 算力 期货", "zh-CN"),
    ("site:cls.cn 算力 期货", "zh-CN"),
    ("site:36kr.com 算力 期货", "zh-CN"),
    ("芝商所 Silicon Data 算力 期货 CME", "zh-CN"),
    ("GPU 算力 期货 合约 交易所 芝商所", "zh-CN"),
    ("AI 算力 资产化 大宗商品 期货 衍生品", "zh-CN"),
    ("算力 金融化 衍生品 GPU 期货", "zh-CN"),
    ("高盛 摩根大通 算力 期货", "zh-CN"),
    ("上海 算力 期货 研发", "zh-CN"),
    ("中信证券 算力 期货 金融化", "zh-CN"),
    ("CME Group Silicon Data compute futures", "en"),
    ("GPU compute futures contract ICE exchange", "en"),
    ("compute power futures derivatives benchmark", "en"),
    ("Goldman JPMorgan AI compute futures trading", "en"),
    ("Silicon Data GPU cloud futures market", "en"),
]

# ====== 已知可提取全文的 URL ======
EXTRACTABLE_URLS = [
    ("https://www.nasdaq.com/articles/cme-group-expanding-compute-futures-market",
     "Nasdaq", "2026-05-13"),
    ("https://www.benzinga.com/news/topics/26/05/52762722/"
     "place-your-bets-futures-traders-are-about-to-see-the-launch-of-ai-semiconductor-contracts",
     "Benzinga", "2026-05-13"),
]

# ====== 相关性过滤：必须同时命中期货类 ∩ 算力类 ======
FUTURES_TERMS = [
    "futures", "期货", "derivative", "衍生品", "芝商所", "CME", "ICE",
    "commodity", "大宗商品", "contract", "合约", "exchange", "交易所",
    "financial", "金融化", "金融衍生", "对冲", "hedge",
]
COMPUTE_TERMS = [
    "gpu", "算力", "compute", "computing", "cloud", "云计算", "AI 算力",
    "h100", "a100", "h200", "b200", "nvidia", "英伟达", "Silicon Data",
    "chip", "芯片", "processor", "处理器", "data center", "数据中心",
    "rental", "租赁", "price", "定价", "benchmark", "指数",
]

# ====== 专有名词还原 ======
PROPER_NOUNS = {
    "克劳德·费布尔": "Claude Fable", "克劳德": "Claude", "聊天 GPT": "ChatGPT",
    "开放人工智能": "OpenAI", "人类": "Anthropic", "英伟达": "NVIDIA",
    "谷歌": "Google", "微软": "Microsoft", "太空探索": "SpaceX",
    "核心编织": "CoreWeave", "运行舱": "RunPod", "浩瀚": "Vast.ai",
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


# 复用单个翻译器实例（避免每次创建 ThreadPoolExecutor 的开销）
_TRANSLATOR = None
def _get_translator():
    global _TRANSLATOR
    if _TRANSLATOR is None and HAS_TRANS:
        _TRANSLATOR = GoogleTranslator(source='en', target='zh-CN')
    return _TRANSLATOR

def translate(text: str) -> str:
    if not HAS_TRANS or not text:
        return ""
    try:
        from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeout
        translator = _get_translator()
        if translator is None:
            return ""

        def _do_translate(t):
            if len(t) <= 4000:
                return translator.translate(t)
            chunks = []
            for i in range(0, len(t), 4000):
                chunks.append(translator.translate(t[i:i + 4000]))
            return " ".join(chunks)

        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(_do_translate, text)
            result = future.result(timeout=20)
        for cn, en in PROPER_NOUNS.items():
            result = result.replace(cn, en)
        return result
    except (FuturesTimeout, Exception):
        return ""


# ==================== 生成丰富的 fallback 正文 ====================

def build_rich_fallback(title: str, source: str, published: str, url: str,
                        lang: str, title_cn: str = "") -> str:
    """
    当无法从原文抓取正文时，构建有意义的描述内容。
    包含标题、来源、日期和一个清晰的原文链接指引。
    """
    display_title = title_cn or title

    if lang == "zh":
        # 中文文章 —— 通过 Google News 链接在浏览器中可直接跳转原文
        return (
            f"「{display_title}」\n\n"
            f"📰 来源：{source}\n"
            f"📅 发布日期：{published}\n\n"
            f"本文由 Google News 聚合自 {source}。"
            f"点击下方「文章来源」链接可在浏览器中自动跳转到"
            f"原始文章页面，阅读完整内容。\n\n"
            f"💡 提示：本栏目聚焦 GPU 算力期货市场动态，"
            f"涵盖芝商所（CME）、洲际交易所（ICE）、"
            f"Silicon Data 等机构推出的算力期货/衍生品合约，"
            f"以及高盛、摩根大通等华尔街机构在算力金融化领域的布局。"
        )
    else:
        # 英文文章 —— 提供原文摘要信息
        display_title_cn = title_cn or title
        return (
            f"「{display_title_cn}」\n\n"
            f"📰 Source: {source}\n"
            f"📅 Published: {published}\n\n"
            f"Original title: {title}\n\n"
            f"This article is aggregated from {source} via Google News. "
            f"Click the source link below to read the full article. "
            f"The Google News link will automatically redirect you "
            f"to the original article page.\n\n"
            f"💡 This section focuses on GPU compute futures market developments, "
            f"including CME Group, ICE, Silicon Data compute futures contracts, "
            f"and Wall Street's involvement in compute financialization."
        )


# ==================== RSS 抓取 ====================

def fetch_google_news_rss(query: str, hl: str) -> list[dict]:
    """从 Google News RSS 搜索文章 (带超时的 requests + feedparser，含重试)"""
    if not HAS_FEED:
        return []
    rss_url = f"https://news.google.com/rss/search?q={quote(query)}&hl={hl}&ceid={hl}"

    for attempt in range(2):  # 最多重试一次
        try:
            # 先用 requests 获取 RSS XML（带超时），再用 feedparser 解析
            r = requests.get(rss_url, timeout=TIMEOUT, headers=HEADERS, proxies=PROXY)
            if r.status_code != 200:
                print(f"   ⚠ HTTP {r.status_code} for: {query[:40]}")
                return []
            feed = feedparser.parse(r.content)
            break  # 成功，跳出重试循环
        except requests.Timeout:
            if attempt == 0:
                print(f"   ⏱ timeout (attempt {attempt+1}), retrying: {query[:40]}")
                continue
            print(f"   ⏱ timeout ({TIMEOUT}s): {query[:40]}")
            return []
        except requests.RequestException as e:
            if attempt == 0:
                print(f"   🔄 {type(e).__name__} (attempt {attempt+1}), retrying: {query[:40]}")
                continue
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

        # 提取 RSS 中的摘要（可能非常短）
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


# ==================== 已知 URL 文章提取 ====================

def extract_full_article(url: str) -> dict:
    """从已知可抓取来源提取全文"""
    result = {}
    try:
        r = requests.get(url, timeout=TIMEOUT, headers=HEADERS, proxies=PROXY)
        if r.status_code != 200:
            return result
        html = r.text
    except Exception:
        return result

    if not HAS_BS4 or not html:
        return result

    try:
        soup = BeautifulSoup(html, "html.parser")
        t = soup.find("title")
        title = ""
        if t:
            title = t.get_text().strip()
            for sep in [" | ", " - ", " _ ", "｜"]:
                title = title.split(sep)[0].strip()

        for sel in ["article", ".article-body", ".article-content",
                    ".post-content", "main", "[role='main']"]:
            div = soup.select_one(sel)
            if div:
                for tag in div.find_all(["script", "style", "nav"]):
                    tag.decompose()
                text = re.sub(r'\n{3,}', '\n\n', div.get_text()).strip()
                if len(text) > 200:
                    result["full_text"] = text[:8000]
                    break

        if not result.get("full_text"):
            for tag in soup(["script", "style", "nav", "header", "footer", "aside"]):
                tag.decompose()
            text = re.sub(r'\n{3,}', '\n\n', soup.get_text()).strip()
            if len(text) > 100:
                result["full_text"] = text[:8000]

        if title:
            result["title"] = title

        imgs = []
        for img in soup.find_all("img", src=True):
            src = img["src"]
            if src.startswith("http") and not src.endswith(".svg"):
                imgs.append(src)
        if imgs:
            result["images"] = imgs[:5]
    except Exception:
        pass

    return result


# ==================== 文章标准化 ====================

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

    # 如果正文为空或太短（RSS 摘要不够），构建丰富内容
    if not a.get("full_text") or len(a["full_text"]) < 80:
        a["full_text"] = build_rich_fallback(
            a.get("title", ""),
            a.get("source", ""),
            a.get("published", ""),
            a.get("url", ""),
            a.get("lang", "zh"),
            a.get("title_cn", ""),
        )
    return a


# ==================== 主流程 ====================

def main():
    print("=" * 60)
    print("📰 GPU 算力期货新闻抓取器 v3")
    print(f"   feedparser={HAS_FEED} bs4={HAS_BS4} 翻译={'OK' if HAS_TRANS else 'NO'}")
    print("=" * 60)

    all_news = []
    seen_titles = set()

    # ---- Step 1: 已知可提取 URL ----
    print("\n📌 已知全文源（直接抓取）:")
    for url, source, date in EXTRACTABLE_URLS:
        print(f"   {source}: {url[:70]}...")
        extracted = extract_full_article(url)
        if extracted.get("full_text") and len(extracted["full_text"]) > 200:
            body = extracted["full_text"]
            all_news.append({
                "title": extracted.get("title", url.split("/")[-1][:60]),
                "source": source,
                "source_url": url,
                "url": url,
                "published": date,
                "summary": body[:400],
                "full_text": body,
                "images": extracted.get("images", []),
                "lang": "en",
            })
            seen_titles.add(extracted.get("title", "")[:60])
            print(f"      ✅ {len(body)} chars (full text extracted)")
        else:
            print(f"      ⚠️ extraction failed, skipped")

    # ---- Step 2: Google News RSS ----
    print("\n🔍 Google News RSS:")
    for query, hl in GOOGLE_NEWS_QUERIES:
        articles = fetch_google_news_rss(query, hl)
        added = 0
        for a in articles:
            key = a["title"][:60]
            if key not in seen_titles:
                seen_titles.add(key)
                all_news.append(a)
                added += 1
        print(f"   [{query[:40]}]: +{added} ({len(all_news)} total)")

    # ---- Step 3: 相关性过滤 ----
    filtered = []
    extractable_sources = {s for _, s, _ in EXTRACTABLE_URLS}
    for a in all_news:
        if a.get("source") in extractable_sources:
            filtered.append(a)
            continue
        text = (a.get("title", "") + " " + a.get("summary", "")).lower()
        has_futures = any(kw.lower() in text for kw in FUTURES_TERMS)
        has_compute = any(kw.lower() in text for kw in COMPUTE_TERMS)
        if has_futures and has_compute:
            filtered.append(a)
    if filtered:
        all_news = filtered
    print(f"\n📋 After filter (futures AND compute): {len(all_news)} articles")

    # ---- Step 4: 翻译英文标题 ----
    en_articles = [a for a in all_news if a.get("lang") == "en"]
    if HAS_TRANS and en_articles:
        print(f"\n🌐 Translating {len(en_articles)} English titles...")
        for a in en_articles:
            a["title_cn"] = translate(a["title"])
            a["summary_cn"] = translate(a.get("summary", "")) if a.get("summary") else ""
            a["translated"] = True
            print(f"   OK: {a['title'][:55]}...")
    else:
        for a in all_news:
            a["title_cn"] = a["summary_cn"] = ""
            a["translated"] = False

    # ---- Step 5: 标准化 + 构建 fallback 正文（此时 title_cn 已有） ----
    for a in all_news:
        normalize_article(a)

    # ---- Step 5b: 对英文文章的 fallback 正文做翻译 ----
    if HAS_TRANS:
        for a in en_articles:
            ft = a.get("full_text", "")
            # 只翻译 fallback 内容（短的），不翻译长文章（真实的全文）
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
                print(f"\n📚 Loaded {len(existing)} existing articles")
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
    has_img = sum(1 for a in all_news if a.get("images"))
    has_full = sum(1 for a in all_news if len(a.get("full_text", "")) > 500)

    # ---- Step 8: 写入 ----
    ts = datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:00") + " (北京时间)"
    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(f"// GPU算力期货新闻 v3\n// Generated: {ts}\n")
        f.write(f"var NEWS_FETCHED_AT = \"{ts}\";\nvar GPU_NEWS = ")
        json.dump(all_news, f, indent=2, ensure_ascii=False)
        f.write(";\n")

    print(f"\n{'=' * 60}")
    print(f"Done: {OUTPUT.name}  {len(all_news)} articles")
    print(f"  CN:{zh}  EN:{en}  Translated:{tr}  Images:{has_img}  FullText(>500):{has_full}")
    print(f"  Generated: {ts}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
