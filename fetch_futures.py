#!/usr/bin/env python3
"""
GPU 算力期货新闻抓取器 v2
=========================
多平台站内搜索 + RSS + 已知URL → 正文抓取 → 合并输出 futures_news.js

用法: python fetch_futures.py
依赖: pip install feedparser deep-translator trafilatura requests beautifulsoup4 newspaper3k
"""

import json, re, sys, io, os
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

try: import requests
except ImportError: print("pip install requests"); sys.exit(1)
try: from bs4 import BeautifulSoup; HAS_BS4 = True
except ImportError: HAS_BS4 = False

try: import feedparser; HAS_FEED = True
except ImportError: HAS_FEED = False
try: import trafilatura; HAS_TRAF = True
except ImportError: HAS_TRAF = False
try: from newspaper import Article; HAS_NEWS = True
except ImportError: HAS_NEWS = False
try: from deep_translator import GoogleTranslator; HAS_TRANS = True
except ImportError: HAS_TRANS = False

OUTPUT = Path(__file__).parent / "futures_news.js"
TIMEOUT = 15
MAX_NEWS = 20

# ====== HTTP 代理（GitHub Secrets 配置国内代理） ======
PROXY = None
http_proxy = os.environ.get("HTTP_PROXY") or os.environ.get("http_proxy")
if http_proxy:
    PROXY = {"http": http_proxy, "https": os.environ.get("HTTPS_PROXY", http_proxy)}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "Chrome/125.0.0.0 Safari/537.36"
}

# ====== 已知权威文章（直接抓取，最可靠） ======
KNOWN_URLS = [
    ("https://www.cmegroup.com/media-room/press-releases/2026/5/12/"
     "cme_group_and_silicondatapartnertolaunchfirstcomputefutures.html",
     "CME Group", "2026-05-12"),
    ("https://www.nasdaq.com/articles/cme-group-expanding-compute-futures-market",
     "Nasdaq", "2026-05-13"),
    ("https://www.benzinga.com/news/topics/26/05/52762722/"
     "place-your-bets-futures-traders-are-about-to-see-the-launch-of-ai-semiconductor-contracts",
     "Benzinga", "2026-05-13"),
]

# ====== 全文本 RSS 源 ======
FULLTEXT_FEEDS = [
    ("https://www.36kr.com/feed", "36氪", "zh"),
    ("https://finance.sina.com.cn/roll/rss.xml", "新浪财经", "zh"),
    ("https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml", "NYT Tech", "en"),
    ("https://feeds.reuters.com/reuters/businessNews", "Reuters Business", "en"),
]

# ====== Google News 搜索词（中英文混合，精准匹配期货+算力） ======
GOOGLE_NEWS_QUERIES = [
    # 中文精准搜索
    ("芝商所 算力 期货 CME", "zh-CN"),
    ("GPU 算力 期货 合约", "zh-CN"),
    ("算力 金融化 衍生品 期货", "zh-CN"),
    ("AI 算力 资产化 大宗商品 期货", "zh-CN"),
    ("云计算 GPU 定价 金融 期货", "zh-CN"),
    ("Silicon Data GPU 算力 期货", "zh-CN"),
    # 英文精准搜索
    ("CME GPU compute futures contract", "en"),
    ("Silicon Data compute futures GPU", "en"),
    ("GPU cloud rental futures derivatives", "en"),
    ("compute power futures exchange contract", "en"),
    ("GPU commodity trading futures", "en"),
    ("ICE GPU futures cloud computing", "en"),
]

# ====== 相关性过滤关键词 ======
FUTURES_KW = [
    "futures", "future", "期货", "derivative", "衍生品", "芝商所", "CME", "ICE",
    "commodity", "contract", "合约", "exchange", "交易所", "financial", "金融",
    "asset", "资产", "index", "指数", "gpu", "算力", "compute", "cloud",
    "rental", "租赁", "定价", "price", "benchmark", "Silicon Data",
    "纳斯达克", "Nasdaq", "Benzinga", "listing", "上市",
]

# ====== 翻译专有名词还原 ======
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


def resolve_url(url: str) -> str:
    """跟随重定向，返回最终 URL"""
    try:
        r = requests.head(url, timeout=TIMEOUT, allow_redirects=True,
                          headers=HEADERS, proxies=PROXY)
        return r.url
    except Exception:
        return url


def fetch_page(url: str, timeout: int = TIMEOUT) -> str | None:
    """下载页面 HTML"""
    try:
        r = requests.get(url, timeout=timeout, headers=HEADERS, proxies=PROXY)
        if r.status_code == 200 and len(r.text) > 1000:
            return r.text
    except Exception:
        pass
    return None


def extract_title_from_html(html: str) -> str:
    """从 HTML 中提取页面标题"""
    if not HAS_BS4 or not html:
        return ""
    try:
        soup = BeautifulSoup(html, "html.parser")
        t = soup.find("title")
        if t:
            # 清理常见的标题后缀
            title = t.get_text().strip()
            for sep in [" | ", " - ", " _ ", "｜"]:
                title = title.split(sep)[0].strip()
            return title
    except Exception:
        pass
    return ""


def detect_lang(text: str) -> str:
    """简单检测文本语言"""
    if not text:
        return "en"
    cn_chars = sum(1 for c in text[:50] if '一' <= c <= '鿿')
    return "zh" if cn_chars >= 2 else "en"


# ==================== RSS 抓取 ====================

def fetch_rss(url: str) -> list[dict]:
    """通用 RSS 抓取，返回文章列表"""
    if not HAS_FEED:
        return []
    try:
        feed = feedparser.parse(url)
    except Exception:
        return []
    results = []
    for e in feed.entries[:10]:
        title = e.get("title", "").strip()
        # Google News 格式 "Title - Source"
        if " - " in title:
            parts = title.rsplit(" - ", 1)
            title, source = parts[0].strip(), parts[1].strip()
        else:
            source = feed.feed.get("title", "")
        summary = clean_html(e.get("summary", e.get("description", "")))
        # 尝试获取 feed 中的全文
        content = ""
        if "content" in e:
            content = clean_html(e["content"][0].get("value", ""))
        elif "content:encoded" in e:
            content = clean_html(e["content:encoded"])
        results.append({
            "title": title,
            "source": source,
            "url": e.get("link", ""),
            "published": parse_date(e.get("published", "")),
            "summary": summary[:500],
            "full_text": content[:8000] if content else "",
            "lang": detect_lang(title),
        })
    return results


# ==================== 文章正文提取 ====================

def extract_article(url: str) -> dict:
    """
    多引擎文章提取：trafilatura → newspaper3k → BeautifulSoup
    对新浪财经有专用选择器
    """
    real_url = resolve_url(url)
    html = fetch_page(real_url)
    if not html:
        return {}

    result = {}

    # 引擎 0: 新浪财经专用提取器
    if 'sina.com.cn' in real_url and HAS_BS4:
        try:
            soup = BeautifulSoup(html, "html.parser")
            for sel in [".article-content", "#artibody", ".article-body",
                        ".main-content", ".article"]:
                div = soup.select_one(sel)
                if div:
                    text = div.get_text().strip()
                    if len(text) > 200:
                        result["full_text"] = text[:8000]
                        break
            # 提取图片
            imgs = []
            for sel in [".article-content img", "#artibody img", ".article-body img"]:
                for img in soup.select(sel):
                    src = img.get("src", "")
                    if src.startswith("http") and not src.endswith(".svg"):
                        imgs.append(src)
            if imgs:
                result["images"] = imgs[:5]
        except Exception:
            pass

    # 引擎 1: trafilatura
    if (not result.get("full_text") or len(result["full_text"]) < 200) and HAS_TRAF:
        try:
            doc = trafilatura.extract(html, output_format="json",
                                      with_metadata=True, include_images=True)
            if doc:
                d = json.loads(doc)
                text = d.get("text", "")
                if len(text) > 100:
                    result["full_text"] = text[:8000]
                imgs = d.get("images", [])
                if imgs:
                    result["images"] = [i.get("src", i) if isinstance(i, dict) else str(i)
                                        for i in imgs[:5]]
        except Exception:
            pass

    # 引擎 2: newspaper3k
    if (not result.get("full_text") or len(result["full_text"]) < 200) and HAS_NEWS:
        try:
            from newspaper import Config
            config = Config()
            config.browser_user_agent = HEADERS["User-Agent"]
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

    # 引擎 3: BeautifulSoup 通用 fallback
    if (not result.get("full_text") or len(result["full_text"]) < 200) and HAS_BS4:
        try:
            soup = BeautifulSoup(html, "html.parser")
            for tag in soup(["script", "style", "nav", "header", "footer", "aside"]):
                tag.decompose()
            # 尝试常见正文容器
            for sel in ["article", ".article-body", ".post-content",
                        "#article-body", "main", "[role='main']"]:
                div = soup.select_one(sel)
                if div:
                    text = re.sub(r'\n{3,}', '\n\n', div.get_text()).strip()
                    if len(text) > 200:
                        result["full_text"] = text[:8000]
                        break
            # 兜底：取 body 文本
            if not result.get("full_text"):
                text = re.sub(r'\n{3,}', '\n\n', soup.get_text()).strip()
                if len(text) > 100:
                    result["full_text"] = text[:8000]
        except Exception:
            pass

    return result


# ==================== 翻译 ====================

def translate(text: str) -> str:
    """英文 → 中文翻译，带专有名词还原"""
    if not HAS_TRANS or not text:
        return ""
    try:
        if len(text) <= 4000:
            result = GoogleTranslator(source='en', target='zh-CN').translate(text)
        else:
            chunks = []
            for i in range(0, len(text), 4000):
                chunks.append(GoogleTranslator(source='en', target='zh-CN')
                              .translate(text[i:i + 4000]))
            result = " ".join(chunks)
        # 还原专有名词
        for cn, en in PROPER_NOUNS.items():
            result = result.replace(cn, en)
        return result
    except Exception:
        return ""


# ==================== 主流程 ====================

def main():
    print("=" * 60)
    print("📰 GPU 算力期货新闻抓取器 v2")
    print(f"   提取器: trafilatura={HAS_TRAF} newspaper3k={HAS_NEWS} bs4={HAS_BS4}")
    print(f"   翻译器: {'✅' if HAS_TRANS else '❌'}  代理: {'✅' if PROXY else '❌'}")
    print("=" * 60)

    all_news = []
    seen_titles = set()  # 按标题前60字符去重

    # ---- Step 1: 已知权威文章（直接抓取，最优先） ----
    print("\n📌 已知权威文章（直接抓取）:")
    for url, source, date in KNOWN_URLS:
        print(f"   {source}: {url[:70]}...")
        html = fetch_page(url)
        if not html:
            print(f"      ❌ 下载失败")
            continue

        article = extract_article(url)
        title = extract_title_from_html(html) if html else ""
        full_text = article.get("full_text", "")

        if full_text and len(full_text) > 100:
            all_news.append({
                "title": title or url.split("/")[-1][:60],
                "source": source,
                "url": url,
                "published": date,
                "summary": full_text[:400],
                "full_text": full_text,
                "images": article.get("images", []),
                "lang": detect_lang(title or full_text[:100]),
            })
            seen_titles.add(title[:60] if title else url)
            print(f"      ✅ {len(full_text)} 字")
        else:
            print(f"      ⚠️ 正文不足100字，跳过")

    # ---- Step 2: 全文本 RSS 源 ----
    print("\n📡 全文本 RSS 源:")
    for feed_url, source_name, lang in FULLTEXT_FEEDS:
        articles = fetch_rss(feed_url)
        added = 0
        for a in articles:
            a["lang"] = lang
            a["source"] = source_name
            key = a["title"][:60]
            if key not in seen_titles:
                seen_titles.add(key)
                all_news.append(a)
                added += 1
        print(f"   {source_name}: +{added} 篇 (累计 {len(all_news)})")

    # ---- Step 3: Google News RSS 搜索 ----
    print("\n🔍 Google News RSS 搜索:")
    for query, hl in GOOGLE_NEWS_QUERIES:
        rss_url = f"https://news.google.com/rss/search?q={quote(query)}&hl={hl}&ceid={hl}"
        articles = fetch_rss(rss_url)
        added = 0
        for a in articles:
            a["lang"] = "zh" if "zh" in hl else detect_lang(a["title"])
            key = a["title"][:60]
            if key not in seen_titles:
                seen_titles.add(key)
                all_news.append(a)
                added += 1
        print(f"   「{query[:40]}」: +{added} 篇 (累计 {len(all_news)})")

    # ---- Step 4: 相关性过滤 ----
    direct_sources = {s for _, s, _ in KNOWN_URLS}
    filtered = []
    for a in all_news:
        if a.get("source") in direct_sources:
            filtered.append(a)  # 已知来源直接保留
        else:
            text = (a.get("title", "") + " " + a.get("summary", "")).lower()
            if any(kw.lower() in text for kw in FUTURES_KW):
                filtered.append(a)
    if filtered:
        all_news = filtered
    print(f"\n📋 相关性过滤后: {len(all_news)} 篇")

    # ---- Step 5: 正文提取（对 RSS 来的无正文文章） ----
    need_extract = [a for a in all_news
                    if not a.get("full_text") or len(a["full_text"]) < 200]
    if need_extract:
        print(f"\n📄 正文提取 ({len(need_extract)} 篇需要)...")
        for i, a in enumerate(need_extract):
            extracted = extract_article(a["url"])
            if extracted.get("full_text"):
                a["full_text"] = extracted["full_text"]
            if extracted.get("images"):
                a["images"] = extracted["images"]
            nc = len(a.get("full_text", ""))
            ni = len(a.get("images", []))
            print(f"   {i + 1}. {a['title'][:40]}... ({nc}字, {ni}图)")

    # ---- Step 6: 过滤无正文文章 ----
    all_news = [a for a in all_news
                if a.get("full_text") and len(a["full_text"]) > 100]
    print(f"   过滤无正文后: {len(all_news)} 篇")

    # ---- Step 7: 翻译英文文章 ----
    en_articles = [a for a in all_news if a.get("lang") == "en"]
    if HAS_TRANS and en_articles:
        print(f"\n🌐 翻译 {len(en_articles)} 篇英文...")
        for a in en_articles:
            a["title_cn"] = translate(a["title"])
            a["summary_cn"] = translate(a.get("summary", ""))
            full = a.get("full_text", "")
            a["full_text_cn"] = translate(full) if len(full) > 200 else ""
            a["translated"] = True
            tc = len(a.get("full_text_cn", ""))
            print(f"   ✅ {a['title'][:40]}... (译文{tc}字)")
    else:
        for a in all_news:
            a["title_cn"] = a["summary_cn"] = a["full_text_cn"] = ""
            a["translated"] = False

    # ---- Step 8: 合并旧数据 ----
    existing = []
    if OUTPUT.exists():
        try:
            raw = OUTPUT.read_text(encoding="utf-8")
            m = re.search(r'GPU_NEWS\s*=\s*(\[.*\]);', raw, re.DOTALL)
            if m:
                existing = json.loads(m.group(1))
                print(f"\n📚 已加载 {len(existing)} 篇旧文章")
        except Exception:
            pass

    existing_titles = {a["title"][:60] for a in existing}
    new_added = 0
    for a in all_news:
        if a["title"][:60] not in existing_titles:
            existing.insert(0, a)  # 新文章插到最前面
            existing_titles.add(a["title"][:60])
            new_added += 1

    # 按发布日期倒序
    existing.sort(key=lambda x: x.get("published", ""), reverse=True)
    all_news = existing[:50]  # 保留最多 50 篇

    # 保护：如果本次抓取为空，保留已有数据
    if len(all_news) == 0 and existing:
        print("   ⚠️ 本次未抓取到新文章，保留已有数据")
        all_news = existing

    print(f"   新增 {new_added} 篇，总计 {len(all_news)} 篇")

    # ---- Step 9: 统计 ----
    zh = sum(1 for a in all_news if a.get("lang") == "zh")
    en = sum(1 for a in all_news if a.get("lang") == "en")
    ft = sum(1 for a in all_news if a.get("full_text") and len(a["full_text"]) > 200)
    im = sum(1 for a in all_news if a.get("images"))
    tr = sum(1 for a in all_news if a.get("translated"))

    # ---- Step 10: 写入 futures_news.js ----
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(f"// GPU算力期货新闻\n// 生成: {ts}\n")
        f.write(f"var NEWS_FETCHED_AT = \"{ts}\";\nvar GPU_NEWS = ")
        json.dump(all_news, f, indent=2, ensure_ascii=False)
        f.write(";\n")

    print(f"\n{'=' * 60}")
    print(f"✅ {OUTPUT.name}: {len(all_news)} 篇")
    print(f"   中文{zh} | 英文{en} | 全文{ft} | 图片{im} | 翻译{tr}")
    print(f"   生成时间: {ts}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
