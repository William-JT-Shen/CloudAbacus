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

OUTPUT = Path(__file__).parent / "futures_news.js"
TIMEOUT = 12

# 全文本 RSS
FULLTEXT_FEEDS = [
    ("https://feeds.reuters.com/reuters/businessNews", "Reuters", "en"),
    ("https://www.36kr.com/feed", "36氪", "zh"),
    ("https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml", "NYT Tech", "en"),
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
    # 相关性过滤（至少要有期货/衍生品关键词）
    FUTURES_KW = ["futures","future","期货","derivative","衍生品","芝商所","CME","ICE","commodity",
                   "contract","合约","exchange","交易所","financial","金融","asset","资产","index"]
    filtered = []
    for a in all_news:
        text = (a["title"]+" "+a.get("summary","")).lower()
        if any(kw in text for kw in FUTURES_KW): filtered.append(a)
    if len(filtered) >= 2: all_news = filtered
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
    # 过滤空文章
    all_news = [a for a in all_news if a.get("full_text") and len(a["full_text"])>100]
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
    # 写入
    t = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with open(OUTPUT,"w",encoding="utf-8") as f:
        f.write(f"// GPU算力期货新闻\n// 生成:{t}\nvar NEWS_FETCHED_AT=\"{t}\";\nvar GPU_NEWS=")
        json.dump(all_news, f, indent=2, ensure_ascii=False)
        f.write(";\n")
    print(f"\n✅ {OUTPUT.name}: {len(all_news)} 篇")

if __name__ == "__main__": main()
