#!/usr/bin/env python3
"""
GPU 算力期货新闻抓取器 v2
=========================
策略：Google News RSS 站内搜索 → 元数据提取 → 摘要翻译 → 输出 futures_news.js

Google News RSS 提供的文章链接在浏览器中点击会自动跳转到原文，
因此我们用 Google News 链接作为 url，RSS 中的元数据（标题/来源/日期）作为新闻卡片内容。

用法: python fetch_futures.py
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

OUTPUT = Path(__file__).parent / "futures_news.js"
TIMEOUT = 15

# ====== HTTP 代理（GitHub Secrets 配置国内代理） ======
PROXY = None
http_proxy = os.environ.get("HTTP_PROXY") or os.environ.get("http_proxy")
if http_proxy:
    PROXY = {"http": http_proxy, "https": os.environ.get("HTTPS_PROXY", http_proxy)}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "Chrome/125.0.0.0 Safari/537.36"
}

# ====== Google News RSS 搜索词（站内精准搜索） ======
GOOGLE_NEWS_QUERIES = [
    # 中文金融站：站内搜索"算力+期货"
    ("site:finance.sina.com.cn 算力 期货", "zh-CN"),
    ("site:eastmoney.com 算力 期货", "zh-CN"),
    ("site:cls.cn 算力 期货", "zh-CN"),
    ("site:36kr.com 算力 期货", "zh-CN"),
    # 中文精准搜索
    ("芝商所 Silicon Data 算力 期货", "zh-CN"),
    ("GPU 算力 期货 合约 交易所", "zh-CN"),
    ("AI 算力 资产化 大宗商品 期货", "zh-CN"),
    ("算力 金融化 衍生品 GPU", "zh-CN"),
    # 英文金融站：站内搜索
    ("site:reuters.com GPU compute futures", "en"),
    ("site:bloomberg.com GPU compute futures", "en"),
    ("site:coindesk.com GPU compute futures", "en"),
    # 英文精准搜索
    ("CME Group silicon data compute futures", "en"),
    ("GPU cloud rental futures derivatives contract", "en"),
    ("compute power futures exchange benchmark", "en"),
    ("GPU commodity trading futures index", "en"),
]

# ====== 已知可提取全文的 URL ======
EXTRACTABLE_URLS = [
    ("https://www.nasdaq.com/articles/cme-group-expanding-compute-futures-market",
     "Nasdaq", "2026-05-13"),
    ("https://www.benzinga.com/news/topics/26/05/52762722/"
     "place-your-bets-futures-traders-are-about-to-see-the-launch-of-ai-semiconductor-contracts",
     "Benzinga", "2026-05-13"),
]

# ====== 相关性过滤关键词 ======
FUTURES_KW = [
    "futures", "future", "期货", "derivative", "衍生品", "芝商所", "CME", "ICE",
    "commodity", "contract", "合约", "exchange", "交易所", "financial", "金融",
    "asset", "资产", "index", "指数", "gpu", "算力", "compute", "cloud",
    "rental", "租赁", "定价", "price", "benchmark", "Silicon Data",
    "纳斯达克", "Nasdaq", "Benzinga", "listing", "上市", "对冲",
]

# ====== 翻译专有名词还原 ======
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
        for cn, en in PROPER_NOUNS.items():
            result = result.replace(cn, en)
        return result
    except Exception:
        return ""


# ==================== RSS 抓取 ====================

def fetch_google_news_rss(query: str, hl: str) -> list[dict]:
    """
    从 Google News RSS 搜索文章。
    返回标准化的文章列表，使用 Google News 链接（浏览器中会自动跳转到原文）。
    """
    if not HAS_FEED:
        return []
    rss_url = f"https://news.google.com/rss/search?q={quote(query)}&hl={hl}&ceid={hl}"
    try:
        feed = feedparser.parse(rss_url)
    except Exception:
        return []

    results = []
    for e in feed.entries[:10]:
        # 解析标题: "Title - Source Name"
        raw_title = e.get("title", "").strip()
        if " - " in raw_title:
            parts = raw_title.rsplit(" - ", 1)
            title = parts[0].strip()
            rss_source = parts[1].strip()
        else:
            title = raw_title
            rss_source = ""

        # 获取来源信息
        source_name = rss_source
        source_url = ""
        if "source" in e:
            source_name = e.source.get("title", source_name)
            source_url = e.source.get("href", "")

        # Google News RSS 的 link 在浏览器中自动跳转到原文
        gn_link = e.get("link", "")

        # RSS 中的摘要通常很短，我们构建一个基于标题的描述
        summary = clean_html(e.get("summary", e.get("description", "")))
        # 如果摘要太短（Google News RSS 通常只重复标题），用标题作为摘要
        if len(summary) < 20:
            summary = f"「{title}」— {source_name}"

        results.append({
            "title": title,
            "source": source_name,
            "source_url": source_url,
            "url": gn_link,  # Google News 链接（浏览器自动跳转）
            "published": parse_date(e.get("published", "")),
            "summary": summary[:400],
            "full_text": "",  # RSS 条目不含全文，后续尝试提取
            "images": [],
            "lang": "zh" if "zh" in hl else detect_lang(title),
        })
    return results


# ==================== 已知 URL 文章提取 ====================

def extract_full_article(url: str) -> dict:
    """尝试从已知可提取来源获取全文"""
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

        # 提取标题
        t = soup.find("title")
        title = ""
        if t:
            title = t.get_text().strip()
            for sep in [" | ", " - ", " _ ", "｜"]:
                title = title.split(sep)[0].strip()

        # 提取正文
        for sel in ["article", ".article-body", ".article-content",
                    ".post-content", "main", "[role='main']"]:
            div = soup.select_one(sel)
            if div:
                # 移除干扰元素
                for tag in div.find_all(["script", "style", "nav"]):
                    tag.decompose()
                text = re.sub(r'\n{3,}', '\n\n', div.get_text()).strip()
                if len(text) > 200:
                    result["full_text"] = text[:8000]
                    break

        # 兜底：用 body
        if not result.get("full_text"):
            for tag in soup(["script", "style", "nav", "header", "footer", "aside"]):
                tag.decompose()
            text = re.sub(r'\n{3,}', '\n\n', soup.get_text()).strip()
            if len(text) > 100:
                result["full_text"] = text[:8000]

        if title:
            result["title"] = title

        # 提取配图
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


# ==================== 主流程 ====================

def main():
    print("=" * 60)
    print("📰 GPU 算力期货新闻抓取器 v2")
    print(f"   feedparser={HAS_FEED} bs4={HAS_BS4} 翻译={'✅' if HAS_TRANS else '❌'}")
    print("=" * 60)

    all_news = []
    seen_titles = set()

    # ---- Step 1: 已知可提取 URL（直接抓取全文） ----
    print("\n📌 已知全文源（直接抓取）:")
    for url, source, date in EXTRACTABLE_URLS:
        print(f"   {source}: {url[:70]}...")
        extracted = extract_full_article(url)
        if extracted.get("full_text") and len(extracted["full_text"]) > 200:
            all_news.append({
                "title": extracted.get("title", url.split("/")[-1][:60]),
                "source": source,
                "url": url,
                "published": date,
                "summary": extracted["full_text"][:400],
                "full_text": extracted["full_text"],
                "images": extracted.get("images", []),
                "lang": "en",
            })
            seen_titles.add(extracted.get("title", "")[:60])
            print(f"      ✅ {len(extracted['full_text'])} 字")
        else:
            print(f"      ⚠️ 提取失败")

    # ---- Step 2: Google News RSS 搜索（主要数据源） ----
    print("\n🔍 Google News RSS 搜索:")
    for query, hl in GOOGLE_NEWS_QUERIES:
        articles = fetch_google_news_rss(query, hl)
        added = 0
        for a in articles:
            key = a["title"][:60]
            if key not in seen_titles:
                seen_titles.add(key)
                all_news.append(a)
                added += 1
        print(f"   「{query[:45]}」: +{added} 篇 (累计 {len(all_news)})")

    # ---- Step 3: 相关性过滤 ----
    filtered = []
    extractable_sources = {s for _, s, _ in EXTRACTABLE_URLS}
    for a in all_news:
        if a.get("source") in extractable_sources:
            filtered.append(a)  # 已知可提取来源直接保留
        else:
            text = (a.get("title", "") + " " + a.get("summary", "")).lower()
            if any(kw.lower() in text for kw in FUTURES_KW):
                filtered.append(a)
    if filtered:
        all_news = filtered
    print(f"\n📋 相关性过滤后: {len(all_news)} 篇")

    # ---- Step 4: 标准化所有文章字段 ----
    def normalize_article(a: dict) -> dict:
        """确保文章拥有所有必需字段，并填充空值"""
        defaults = {
            "title": "", "source": "", "source_url": "", "url": "",
            "published": "", "summary": "", "full_text": "", "images": [],
            "lang": "zh", "title_cn": "", "summary_cn": "", "translated": False,
        }
        for k, v in defaults.items():
            if k not in a:
                a[k] = v
        # 用摘要补全空正文
        if not a.get("full_text") or len(a["full_text"]) < 20:
            summary = a.get("summary", "")
            if summary and len(summary) > 20:
                a["full_text"] = summary
            else:
                # 用标题 + 来源构建内容
                src = a.get("source", "")
                title = a.get("title", "")
                a["full_text"] = f"原标题：{title}\n来源：{src}\n\n（本文来自 Google News 聚合，点击标题链接可查看原文。Google News 链接在浏览器中会自动跳转到原始文章页面。）"
        return a

    for a in all_news:
        normalize_article(a)

    # ---- Step 5: 翻译英文文章 ----
    en_articles = [a for a in all_news if a.get("lang") == "en"]
    if HAS_TRANS and en_articles:
        print(f"\n🌐 翻译 {len(en_articles)} 篇英文标题...")
        for a in en_articles:
            a["title_cn"] = translate(a["title"])
            a["summary_cn"] = translate(a.get("summary", "")) if a.get("summary") else ""
            a["translated"] = True
            print(f"   ✅ {a['title'][:50]}...")

    # ---- Step 7: 合并旧数据 ----
    existing = []
    if OUTPUT.exists():
        try:
            raw = OUTPUT.read_text(encoding="utf-8")
            m = re.search(r'GPU_NEWS\s*=\s*(\[.*\]);', raw, re.DOTALL)
            if m:
                existing_data = json.loads(m.group(1))
                # 标准化旧文章字段
                for a in existing_data:
                    normalize_article(a)
                existing = existing_data
                print(f"\n📚 已加载 {len(existing)} 篇旧文章")
        except Exception:
            pass

    existing_titles = {a["title"][:60] for a in existing}
    new_added = 0
    for a in all_news:
        if a["title"][:60] not in existing_titles:
            existing.insert(0, a)
            existing_titles.add(a["title"][:60])
            new_added += 1

    # 按发布日期倒序
    existing.sort(key=lambda x: x.get("published", ""), reverse=True)
    all_news = existing[:50]

    # 保护：如果本次抓取为空，保留已有数据
    if len(all_news) == 0 and existing:
        print("   ⚠️ 本次未抓取到新文章，保留已有数据")
        all_news = existing

    print(f"   新增 {new_added} 篇，总计 {len(all_news)} 篇")

    # ---- Step 7: 统计 ----
    zh = sum(1 for a in all_news if a.get("lang") == "zh")
    en = sum(1 for a in all_news if a.get("lang") == "en")
    tr = sum(1 for a in all_news if a.get("translated"))
    img = sum(1 for a in all_news if a.get("images"))

    # ---- Step 8: 写入 futures_news.js ----
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(f"// GPU算力期货新闻\n// 生成: {ts}\n")
        f.write(f"var NEWS_FETCHED_AT = \"{ts}\";\nvar GPU_NEWS = ")
        json.dump(all_news, f, indent=2, ensure_ascii=False)
        f.write(";\n")

    print(f"\n{'=' * 60}")
    print(f"✅ {OUTPUT.name}: {len(all_news)} 篇 (中文{zh} | 英文{en} | 翻译{tr} | 图{img})")
    print(f"   生成时间: {ts}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
