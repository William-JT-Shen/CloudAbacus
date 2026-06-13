#!/usr/bin/env python3
"""GPU 算力期货新闻抓取器"""
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

HAS_TRAF = False
try: import trafilatura; HAS_TRAF = True
except ImportError: pass
HAS_NEWS = False
try: from newspaper import Article; HAS_NEWS = True
except ImportError: pass
HAS_BS4 = False
try: from bs4 import BeautifulSoup; HAS_BS4 = True
except ImportError: pass
HAS_TRANS = False
try: from deep_translator import GoogleTranslator; HAS_TRANS = True
except ImportError: pass
PLAYWRIGHT_AVAILABLE = False
try: from playwright.sync_api import sync_playwright; PLAYWRIGHT_AVAILABLE = True
except ImportError: pass

OUTPUT = Path(__file__).parent / "futures_news.js"
TIMEOUT = 12

# 全文本 RSS
FULLTEXT_FEEDS = [
    ("https://feeds.reuters.com/reuters/businessNews", "Reuters", "en"),
    ("https://www.36kr.com/feed", "36氪", "zh"),
    ("https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml", "NYT Tech", "en"),
    ("https://finance.sina.com.cn/roll/rss.xml", "新浪财经", "zh"),
]

# Google News 搜索（期货专题）
QUERIES = [
    ("CME GPU compute futures contract", "en"),
    ("芝商所 算力 期货", "zh-CN"),
    ("Silicon Data GPU futures", "en"),
    ("GPU cloud rental futures derivatives", "en"),
    ("算力 金融化 资产化 期货", "zh-CN"),
    ("digital commodity compute futures", "en"),
    ("ICE futures GPU cloud", "en"),
    ("GPU 算力 衍生品 合约", "zh-CN"),
    ("芝商所 Silicon Data GPU 算力", "en"),
    ("算力 期货 交易所 上市", "zh-CN"),
    ("算力 GPU 租赁 市场 金融", "zh-CN"),
    ("GPU cloud compute derivatives financial", "en"),
    ("AI算力 资产化 大宗商品 期货", "zh-CN"),
    ("GPU compute index pricing benchmark", "en"),
    ("云计算 GPU 定价 金融 衍生品", "zh-CN"),
    ("芝商所 Silicon Data 算力期货 推出", "zh-CN"),
    ("芝商所 CME 算力 合约 2026", "zh-CN"),
]

MAX_NEWS = 15

PROPER_NOUNS = {
    "克劳德·费布尔": "Claude Fable", "克劳德": "Claude", "聊天 GPT": "ChatGPT",
    "开放人工智能": "OpenAI", "人类": "Anthropic", "英伟达": "NVIDIA",
    "谷歌": "Google", "微软": "Microsoft", "太空探索": "SpaceX",
    "核心编织": "CoreWeave", "运行舱": "RunPod", "浩瀚": "Vast.ai",
}

def clean_html(t): return re.sub(r'<[^>]+>', '', t).strip()

def parse_date(d):
    if not d: return ""
    try:
        from email.utils import parsedate_to_datetime
        return parsedate_to_datetime(d).strftime("%Y-%m-%d")
    except: return d[:10] if len(d) >= 10 else d

def fetch_rss(url):
    try:
        feed = feedparser.parse(url)
    except: return []
    r = []
    for e in feed.entries[:10]:
        t = e.get("title","").strip()
        if " - " in t:
            p = t.rsplit(" - ",1); title = p[0].strip(); source = p[1].strip()
        else: title = t; source = feed.feed.get("title","")
        summary = clean_html(e.get("summary", e.get("description","")))
        content = ""
        if "content" in e: content = clean_html(e["content"][0].get("value",""))
        elif "content:encoded" in e: content = clean_html(e["content:encoded"])
        r.append({"title":title,"source":source,"url":e.get("link",""),"published":parse_date(e.get("published","")),
                   "summary":summary[:500],"full_text":content[:8000] if content else "",
                   "lang":"zh" if any("一"<=c<="鿿" for c in title[:20]) else "en"})
    return r

def resolve_url(url):
    try:
        r = requests.head(url, timeout=TIMEOUT, allow_redirects=True, headers={"User-Agent":"Mozilla/5.0"})
        return r.url
    except: return url

def extract_article(url):
    real = resolve_url(url)
    try:
        r = requests.get(real, timeout=TIMEOUT, headers={"User-Agent":"Mozilla/5.0"})
        if r.status_code != 200: return {}
        html = r.text
    except: return {}
    result = {}
    if HAS_TRAF:
        try:
            doc = trafilatura.extract(html, output_format="json", with_metadata=True, include_images=True)
            if doc:
                d = json.loads(doc)
                if len(d.get("text","")) > 100: result["full_text"] = d["text"][:8000]
                imgs = d.get("images",[])
                if imgs: result["images"] = [i.get("src",i) if isinstance(i,dict) else str(i) for i in imgs[:5]]
        except: pass
    if (not result.get("full_text") or len(result["full_text"]) < 200) and HAS_NEWS:
        try:
            from newspaper import Config
            art = Article(real, config=Config())
            art.download(); art.parse()
            if len(art.text) > 100: result["full_text"] = art.text[:8000]
            if not result.get("images") and art.top_image: result["images"] = [art.top_image]
        except: pass
    if (not result.get("full_text") or len(result["full_text"]) < 200) and HAS_BS4:
        try:
            soup = BeautifulSoup(html,"html.parser")
            for t in soup(["script","style","nav","header","footer","aside"]): t.decompose()
            text = re.sub(r'\n{3,}','\n\n',soup.get_text()).strip()
            if len(text) > 100: result["full_text"] = text[:8000]
        except: pass
    return result

# 已知的高质量算力期货文章（直接抓取，绕过RSS搜索）
KNOWN_URLS = [
    ("https://finance.sina.com.cn/wm/2026-05-16/doc-inhyahas2588021.shtml", "新浪财经", "zh"),
]


def extract_sina_article(html: str) -> dict:
    """新浪财经专用提取器"""
    result = {}
    if HAS_BS4:
        try:
            soup = BeautifulSoup(html, "html.parser")
            # 新浪文章正文通常在 .article-content 或 #artibody 中
            for sel in [".article-content", "#artibody", ".article-body", ".main-content"]:
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
    return result


def scrape_direct_urls() -> list[dict]:
    """直接抓取已知URL的文章"""
    results = []
    for url, source, lang in KNOWN_URLS:
        html = None
        # 策略1: requests
        for ua in ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/125.0.0.0 Safari/537.36",
                    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"]:
            try:
                r = requests.get(url, timeout=TIMEOUT, headers={"User-Agent": ua})
                if r.status_code == 200 and len(r.text) > 5000:
                    html = r.text
                    break
            except Exception:
                continue
        # 策略2: Playwright
        if not html and PLAYWRIGHT_AVAILABLE:
            try:
                from playwright.sync_api import sync_playwright
                with sync_playwright() as p:
                    browser = p.chromium.launch(headless=True)
                    page = browser.new_page()
                    page.goto(url, timeout=15000, wait_until="load")
                    page.wait_for_timeout(3000)
                    html = page.content()
                    browser.close()
            except Exception:
                pass
        if not html:
            continue

        # 先用新浪专用提取器
        extracted = extract_sina_article(html)
        if not extracted.get("full_text"):
            # 回退到通用提取器
            extracted = extract_article(url)

        if extracted.get("full_text") and len(extracted["full_text"]) > 200:
            # 从HTML提取标题
            title = ""
            if HAS_BS4:
                try:
                    soup = BeautifulSoup(html, "html.parser")
                    t = soup.find("title")
                    if t:
                        title = t.get_text().strip().split("|")[0].split("-")[0].strip()
                except Exception:
                    pass
            results.append({
                "title": title or url.split("/")[-1].replace(".shtml", ""),
                "source": source,
                "url": url,
                "published": "2026-05-16",
                "summary": extracted["full_text"][:400],
                "full_text": extracted["full_text"],
                "images": extracted.get("images", []),
                "lang": lang,
            })
    return results


def translate(text):
    if not HAS_TRANS or not text: return ""
    try:
        if len(text) <= 4000: result = GoogleTranslator(source='en',target='zh-CN').translate(text)
        else:
            chunks = []
            for i in range(0, len(text), 4000): chunks.append(GoogleTranslator(source='en',target='zh-CN').translate(text[i:i+4000]))
            result = " ".join(chunks)
        for cn, en in PROPER_NOUNS.items(): result = result.replace(cn, en)
        return result
    except: return ""

def main():
    print("="*50)
    print("📰 GPU算力期货新闻抓取器")
    print("="*50)
    all_news, seen = [], set()
    for url, src, lang in FULLTEXT_FEEDS:
        for a in fetch_rss(url):
            a["lang"] = lang; a["source"] = src
            k = a["title"][:60]
            if k not in seen: seen.add(k); all_news.append(a)
    for q, hl in QUERIES:
        url = f"https://news.google.com/rss/search?q={quote(q)}&hl={hl}&ceid={hl}"
        for a in fetch_rss(url):
            a["lang"] = "zh" if "zh" in hl else "en"
            k = a["title"][:60]
            if k not in seen: seen.add(k); all_news.append(a)
    # 直接抓取已知URL（最先加入，保证不被过滤）
    direct = scrape_direct_urls()
    print(f"   📌 直接抓取: {len(direct)} 篇")
    for a in direct:
        k = a["title"][:60]
        if k not in seen: seen.add(k); all_news.insert(0, a)

    # 相关性过滤（至少要有期货/衍生品关键词，但直接抓取的文章豁免）
    FUTURES_KW = ["futures","future","期货","derivative","衍生品","芝商所","CME","ICE","commodity",
                   "contract","合约","exchange","交易所","financial","金融","asset","资产","index",
                   "gpu","算力","compute","cloud","rental","租赁","定价","price","benchmark"]
    direct_sources = {s for _, s, _ in KNOWN_URLS}
    filtered = []
    for a in all_news:
        if a["source"] in direct_sources:
            filtered.append(a)  # 已知来源直接保留
        else:
            text = (a["title"]+" "+a.get("summary","")).lower()
            if any(kw in text for kw in FUTURES_KW): filtered.append(a)
    if len(filtered) >= 1: all_news = filtered

    # 提取全文
    need = [a for a in all_news if not a.get("full_text") or len(a["full_text"])<200]
    if need:
        print(f"\n📄 文章提取 ({len(need)}篇)...")
        for i,a in enumerate(need):
            full = extract_article(a["url"])
            if full.get("full_text"): a["full_text"] = full["full_text"]
            if full.get("images"): a["images"] = full["images"]
    # 翻译
    en_arts = [a for a in all_news if a["lang"]=="en"]
    if HAS_TRANS and en_arts:
        for a in en_arts:
            a["title_cn"] = translate(a["title"])
            a["summary_cn"] = translate(a.get("summary",""))
            full = a.get("full_text","")
            a["full_text_cn"] = translate(full) if len(full)>200 else ""
            a["translated"] = True
    else:
        for a in all_news: a["title_cn"]=a["summary_cn"]=a["full_text_cn"]=""; a["translated"]=False
    # 过滤：保留有正文或来自已知来源的文章
    all_news = [a for a in all_news if (a.get("full_text") and len(a["full_text"])>100) or a["source"] in ["新浪财经"]]
    # 合并旧文章
    existing = []
    if OUTPUT.exists():
        try:
            raw = OUTPUT.read_text(encoding="utf-8")
            m = re.search(r'GPU_NEWS\s*=\s*(\[.*\]);', raw, re.DOTALL)
            if m: existing = json.loads(m.group(1))
        except: pass
    et = {a["title"][:60] for a in existing}
    for a in all_news:
        if a["title"][:60] not in et: existing.insert(0,a); et.add(a["title"][:60])
    existing.sort(key=lambda x: x.get("published",""), reverse=True)
    all_news = existing[:50]
    # 排序
    all_news.sort(key=lambda x: x.get("published",""), reverse=True)
    # 保护：如果本次抓取为空，保留已有数据不覆盖
    if len(all_news) == 0 and existing:
        print("   ⚠️ 本次未抓取到新文章，保留已有数据")
        all_news = existing
    # 写入
    t = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with open(OUTPUT,"w",encoding="utf-8") as f:
        f.write(f"// GPU算力期货新闻\n// 生成:{t}\nvar NEWS_FETCHED_AT=\"{t}\";\nvar GPU_NEWS=")
        json.dump(all_news, f, indent=2, ensure_ascii=False)
        f.write(";\n")
    print(f"\n✅ {OUTPUT.name}: {len(all_news)} 篇")

if __name__ == "__main__": main()
