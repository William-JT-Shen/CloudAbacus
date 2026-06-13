#!/usr/bin/env python3
"""
运算盘 · GPU 实时价格爬虫 v4
===============================
自动抓取各平台官网公开定价页面，提取 GPU 型号和实时价格。
覆盖 40+ 全球 GPU 云平台。

用法:
  python fetch_prices.py                      # requests 模式（快速，适合静态页面）
  python fetch_prices.py --save-history        # + 追加历史快照
  python fetch_prices.py --playwright          # Playwright 模式（浏览器渲染）
  python fetch_prices.py --playwright --save-history  # 全功能
  python fetch_prices.py --vast-only           # 仅抓取 Vast.ai（适合高频运行）
  python fetch_prices.py --vast-only --playwright --save-history
  python fetch_prices.py --quick               # 仅抓取高优先级平台（快速模式）

依赖:
  pip install requests beautifulsoup4
  pip install playwright && playwright install chromium  # 仅 --playwright 需要
"""

import requests
import json
import re
import sys
import io
from datetime import datetime, timezone
from pathlib import Path

# Playwright 可选导入
PLAYWRIGHT_AVAILABLE = False
try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    pass

# Windows GBK 编码修复
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# ============================================================
# 配置
# ============================================================
CODE_DIR   = Path(__file__).parent
OUTPUT_LIVE = CODE_DIR / "pricing_live.js"
OUTPUT_HIST = CODE_DIR / "price_history.js"
OUTPUT_HIST_JSON = CODE_DIR / "price_history.json"

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36")
TIMEOUT = 20

fetched_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
scrape_log = {}


# ============================================================
# 工具函数
# ============================================================
def get(url: str) -> str | None:
    """HTTP GET，返回文本，失败返回 None"""
    try:
        r = requests.get(url, timeout=TIMEOUT, headers={"User-Agent": UA}, allow_redirects=True)
        if r.status_code == 200:
            return r.text
        return None
    except Exception:
        return None


def find_between(text: str, start_pat: str, end_pat: str) -> str:
    """提取两个模式之间的文本"""
    m = re.search(start_pat + r'(.*?)' + end_pat, text, re.DOTALL)
    return m.group(1) if m else ""


# 各 GPU 型号的合理小时价格范围 (美元)
PRICE_RANGES = {
    "NVIDIA H200":                     (2.50, 8.00),
    "NVIDIA GH200":                    (3.00, 10.00),
    "NVIDIA H100 (80GB SXM)":          (1.20, 8.00),
    "NVIDIA A100 (80GB SXM)":          (0.40, 5.00),
    "NVIDIA A100 (40GB PCIe)":         (0.30, 3.50),
    "NVIDIA L40S":                     (0.50, 3.00),
    "NVIDIA L4":                       (0.15, 1.50),
    "NVIDIA A40":                      (0.25, 2.00),
    "NVIDIA T4":                       (0.10, 1.00),
    "NVIDIA V100":                     (0.20, 3.00),
    "NVIDIA RTX 6000 Ada / A6000":     (0.25, 2.00),
    "NVIDIA RTX 4090":                 (0.15, 1.50),
    "NVIDIA RTX 4080 / 4080 Super":    (0.10, 1.20),
    "NVIDIA RTX 4070 Ti / 4070":       (0.08, 0.80),
    "NVIDIA RTX 4060 Ti":              (0.05, 0.50),
    "NVIDIA RTX 3090 / 3090 Ti":       (0.08, 0.80),
    "NVIDIA RTX 3080 / 3080 Ti":       (0.06, 0.60),
    "NVIDIA RTX 3070 / 3070 Ti":       (0.04, 0.50),
    "NVIDIA RTX 3060 / 3060 Ti":       (0.03, 0.40),
    "NVIDIA RTX 2080 Ti":              (0.05, 0.50),
    "NVIDIA Tesla P100 / P40":         (0.05, 1.00),
    "NVIDIA Tesla K80 / M40 / M60":    (0.02, 0.30),
    "AMD Radeon RX 7900 XTX / 7900 XT": (0.08, 0.60),
    "AMD Radeon RX 7800 XT / 7700 XT":  (0.05, 0.40),
    "AMD Radeon RX 6900 XT / 6800 XT":  (0.05, 0.40),
    "AMD Radeon RX 6800 / 6700 XT":     (0.04, 0.30),
    # RTX 50 系列 (Blackwell)
    "RTX 5090":                        (0.30, 3.00),
    "RTX 5080":                        (0.20, 2.00),
    "RTX 5070 Ti":                     (0.12, 1.20),
    "RTX 5070":                        (0.10, 1.00),
    "RTX 5060 Ti":                     (0.08, 0.60),
    "RTX 5060":                        (0.06, 0.40),
}


def extract_prices(html: str, gpu_map: list[tuple[str, str, str]]) -> list[dict]:
    """从 HTML 中提取 GPU 价格（带合理性校验）"""
    results = []
    seen = set()
    for gpu_re, price_re, label in gpu_map:
        lo, hi = PRICE_RANGES.get(label, (0.01, 1000))
        for gpu_match in re.finditer(gpu_re, html, re.IGNORECASE):
            ctx_start = max(0, gpu_match.start() - 100)
            ctx_end = min(len(html), gpu_match.end() + 500)
            context = html[ctx_start:ctx_end]
            for price_match in re.finditer(price_re, context, re.IGNORECASE):
                try:
                    price_str = price_match.group(1).replace(',', '')
                    price = float(price_str)
                    if lo <= price <= hi and label not in seen:
                        seen.add(label)
                        results.append({"gpu": label, "price_usd": price})
                        break
                except (ValueError, IndexError):
                    continue
            if label in seen:
                break
    return results


def mark_failed(platform: str, reason: str):
    scrape_log[platform] = {"status": "failed", "gpu_count": 0, "error": reason}
    print(f"  ❌ {reason}")


def mark_ok(platform: str, count: int):
    scrape_log[platform] = {"status": "ok", "gpu_count": count}
    print(f"  ✅ 获取到 {count} 款 GPU")


# ============================================================
# 通用 GPU 名称映射
# ============================================================
COMMON_GPUS = [
    (r'H200\b',                   r'\$(\d+\.?\d*)', "NVIDIA H200"),
    (r'GH200\b',                  r'\$(\d+\.?\d*)', "NVIDIA GH200"),
    (r'H100\b.*?80\s*GB',         r'\$(\d+\.?\d*)', "NVIDIA H100 (80GB SXM)"),
    (r'H100\b(?!.*SXM)',          r'\$(\d+\.?\d*)', "NVIDIA H100 (80GB SXM)"),
    (r'A100\b.*?80\s*GB',         r'\$(\d+\.?\d*)', "NVIDIA A100 (80GB SXM)"),
    (r'A100\b.*?40\s*GB',         r'\$(\d+\.?\d*)', "NVIDIA A100 (40GB PCIe)"),
    (r'L40S\b',                   r'\$(\d+\.?\d*)', "NVIDIA L40S"),
    (r'L4\b(?!\d)',               r'\$(\d+\.?\d*)', "NVIDIA L4"),
    (r'A40\b(?!\d)',              r'\$(\d+\.?\d*)', "NVIDIA A40"),
    (r'T4\b(?!\d)',               r'\$(\d+\.?\d*)', "NVIDIA T4"),
    (r'V100\b',                   r'\$(\d+\.?\d*)', "NVIDIA V100"),
    (r'A6000\b.*?Ada',            r'\$(\d+\.?\d*)', "NVIDIA RTX 6000 Ada / A6000"),
    (r'RTX\s*A?6000\b(?!.*Ada)',  r'\$(\d+\.?\d*)', "NVIDIA RTX 6000 Ada / A6000"),
    (r'RTX\s*5090\b',             r'\$(\d+\.?\d*)', "RTX 5090"),
    (r'RTX\s*5080\b',             r'\$(\d+\.?\d*)', "RTX 5080"),
    (r'RTX\s*5070\s*Ti',         r'\$(\d+\.?\d*)', "RTX 5070 Ti"),
    (r'RTX\s*5070\b',             r'\$(\d+\.?\d*)', "RTX 5070"),
    (r'RTX\s*5060\s*Ti',         r'\$(\d+\.?\d*)', "RTX 5060 Ti"),
    (r'RTX\s*5060\b',             r'\$(\d+\.?\d*)', "RTX 5060"),
    (r'RTX\s*4090\b',             r'\$(\d+\.?\d*)', "NVIDIA RTX 4090"),
    (r'RTX\s*4080\b',             r'\$(\d+\.?\d*)', "NVIDIA RTX 4080 / 4080 Super"),
    (r'RTX\s*4070\s*Ti',         r'\$(\d+\.?\d*)', "NVIDIA RTX 4070 Ti / 4070"),
    (r'RTX\s*4070\b',             r'\$(\d+\.?\d*)', "NVIDIA RTX 4070 Ti / 4070"),
    (r'RTX\s*4060\s*Ti',         r'\$(\d+\.?\d*)', "NVIDIA RTX 4060 Ti"),
    (r'RTX\s*3090\b',             r'\$(\d+\.?\d*)', "NVIDIA RTX 3090 / 3090 Ti"),
    (r'RTX\s*3080\b',             r'\$(\d+\.?\d*)', "NVIDIA RTX 3080 / 3080 Ti"),
    (r'RTX\s*3070\b',             r'\$(\d+\.?\d*)', "NVIDIA RTX 3070 / 3070 Ti"),
    (r'RTX\s*3060\b',             r'\$(\d+\.?\d*)', "NVIDIA RTX 3060 / 3060 Ti"),
    (r'RTX\s*2080\s*Ti',         r'\$(\d+\.?\d*)', "NVIDIA RTX 2080 Ti"),
    (r'RTX\s*8000\b',             r'\$(\d+\.?\d*)', "RTX 8000"),
    (r'RTX\s*5880\b',             r'\$(\d+\.?\d*)', "RTX 5880"),
    (r'RTX\s*6000\b(?!.*Ada)',   r'\$(\d+\.?\d*)', "RTX 6000"),
    (r'P100\b',                   r'\$(\d+\.?\d*)', "NVIDIA Tesla P100 / P40"),
    (r'P40\b',                    r'\$(\d+\.?\d*)', "NVIDIA Tesla P100 / P40"),
    (r'K80\b',                    r'\$(\d+\.?\d*)', "NVIDIA Tesla K80 / M40 / M60"),
    (r'M40\b',                    r'\$(\d+\.?\d*)', "NVIDIA Tesla K80 / M40 / M60"),
    (r'RX\s*7900\s*XTX',         r'\$(\d+\.?\d*)', "AMD Radeon RX 7900 XTX / 7900 XT"),
    (r'RX\s*7900\s*XT\b',        r'\$(\d+\.?\d*)', "AMD Radeon RX 7900 XTX / 7900 XT"),
    (r'RX\s*7800\s*XT',          r'\$(\d+\.?\d*)', "AMD Radeon RX 7800 XT / 7700 XT"),
    (r'RX\s*6900\s*XT',          r'\$(\d+\.?\d*)', "AMD Radeon RX 6900 XT / 6800 XT"),
    (r'RX\s*6800\s*XT',          r'\$(\d+\.?\d*)', "AMD Radeon RX 6900 XT / 6800 XT"),
    (r'RX\s*6800\b',             r'\$(\d+\.?\d*)', "AMD Radeon RX 6800 / 6700 XT"),
    (r'RX\s*6700\s*XT',          r'\$(\d+\.?\d*)', "AMD Radeon RX 6800 / 6700 XT"),
]


def normalize_gpu_name(raw: str) -> str:
    """将各平台原始 GPU 名规范化"""
    raw = raw.strip()
    mapping = {
        'h100': 'NVIDIA H100 (80GB SXM)',
        'h200': 'NVIDIA H200',
        'gh200': 'NVIDIA GH200',
        'a100': 'NVIDIA A100 (80GB SXM)',
        'a6000': 'NVIDIA RTX 6000 Ada / A6000',
        'rtx 6000 ada': 'NVIDIA RTX 6000 Ada / A6000',
        'rtx 5090': 'RTX 5090', 'rtx 5080': 'RTX 5080',
        'rtx 5070 ti': 'RTX 5070 Ti', 'rtx 5070': 'RTX 5070',
        'rtx 5060 ti': 'RTX 5060 Ti', 'rtx 5060': 'RTX 5060',
        'rtx 4090': 'NVIDIA RTX 4090', 'rtx 4080': 'NVIDIA RTX 4080 / 4080 Super',
        'rtx 4070 ti': 'NVIDIA RTX 4070 Ti / 4070', 'rtx 4070': 'NVIDIA RTX 4070 Ti / 4070',
        'rtx 4060 ti': 'NVIDIA RTX 4060 Ti',
        'rtx 3090 ti': 'NVIDIA RTX 3090 / 3090 Ti', 'rtx 3090': 'NVIDIA RTX 3090 / 3090 Ti',
        'rtx 3080 ti': 'NVIDIA RTX 3080 / 3080 Ti', 'rtx 3080': 'NVIDIA RTX 3080 / 3080 Ti',
        'rtx 3070 ti': 'NVIDIA RTX 3070 / 3070 Ti', 'rtx 3070': 'NVIDIA RTX 3070 / 3070 Ti',
        'rtx 3060 ti': 'NVIDIA RTX 3060 / 3060 Ti', 'rtx 3060': 'NVIDIA RTX 3060 / 3060 Ti',
        'rtx 2080 ti': 'NVIDIA RTX 2080 Ti', 'rtx 8000': 'RTX 8000',
        'rtx 6000': 'RTX 6000', 'rtx 5880': 'RTX 5880',
        'rtx 2080': 'RTX 2080', 'rtx 4060': 'NVIDIA RTX 4060 Ti',
        'l40s': 'NVIDIA L40S', 'l40': 'NVIDIA L40S', 'l4': 'NVIDIA L4',
        'a40': 'NVIDIA A40', 't4': 'NVIDIA T4', 'v100': 'NVIDIA V100',
        'p100': 'NVIDIA Tesla P100 / P40', 'p40': 'NVIDIA Tesla P100 / P40',
        'k80': 'NVIDIA Tesla K80 / M40 / M60', 'm40': 'NVIDIA Tesla K80 / M40 / M60',
        'rx 7900 xtx': 'AMD Radeon RX 7900 XTX / 7900 XT',
        'rx 7900 xt': 'AMD Radeon RX 7900 XTX / 7900 XT',
        'rx 7800 xt': 'AMD Radeon RX 7800 XT / 7700 XT',
        'rx 6900 xt': 'AMD Radeon RX 6900 XT / 6800 XT',
        'rx 6800 xt': 'AMD Radeon RX 6900 XT / 6800 XT',
        'rx 6800': 'AMD Radeon RX 6800 / 6700 XT',
        'rx 6700 xt': 'AMD Radeon RX 6800 / 6700 XT',
    }
    key = raw.lower().replace('nvidia ', '').replace('geforce ', '').replace('amd ', '').strip()
    return mapping.get(key, raw)


# ============================================================
# 专用爬虫（需要特殊处理逻辑的平台）
# ============================================================

def scrape_lambda():
    """Lambda Labs: 修复版 - 多 URL 回退"""
    print("🔍 Lambda Labs ...")
    urls = [
        "https://lambdalabs.com/service/gpu-cloud/pricing",
        "https://lambdalabs.com/gpu-cloud",
        "https://lambdalabs.com/service/gpu-cloud",
        "https://lambdalabs.com/pricing",
    ]
    html = None
    for url in urls:
        html = get(url)
        if html:
            break
    if not html:
        return mark_failed("Lambda Labs", "所有 URL 均无法访问")

    results = extract_prices(html, COMMON_GPUS)
    if results:
        mark_ok("Lambda Labs", len(results))
        return results
    mark_failed("Lambda Labs", "未能解析价格数据（页面结构可能变更）")
    return []


def scrape_runpod():
    """RunPod: https://www.runpod.io/pricing"""
    print("🔍 RunPod ...")
    html = get("https://www.runpod.io/pricing")
    if not html:
        return mark_failed("RunPod", "无法访问定价页面")

    results = extract_prices(html, COMMON_GPUS)
    # RunPod 有 Secure Cloud 和 Community Cloud 两套价格
    secure_section = find_between(html, r'Secure\s*Cloud', r'Community\s*Cloud')
    community_section = find_between(html, r'Community\s*Cloud', r'(?:FAQ|footer|</main>)')

    if secure_section:
        secure_results = extract_prices(secure_section, COMMON_GPUS)
        for r in secure_results:
            r["plan_note"] = "Secure Cloud"
    if community_section:
        comm_results = extract_prices(community_section, COMMON_GPUS)
        for r in comm_results:
            r["plan_note"] = "Community Cloud"

    if results:
        mark_ok("RunPod", len(results))
        return results
    mark_failed("RunPod", "未能解析价格数据")
    return []


def scrape_vast():
    """Vast.ai: https://vast.ai/pricing"""
    print("🔍 Vast.ai ...")
    html = get("https://vast.ai/pricing")
    if not html:
        return mark_failed("Vast.ai", "无法访问定价页面")

    results = []
    # vast.ai 常见的显示模式: RTX 4090 ... $0.25
    vast_gpu_re = r'(?:>|\s)((?:RTX\s*\d{4}(?:\s*Ti)?|Tesla\s*[A-Z]\d+|A100|H100|H200|L40S?|A40|A6000|V100|T4|P100|P40|K80|M40|Radeon\s*RX\s*\d{4}(?:\s*XTX?)?))\b'
    vast_price_re = r'\$(\d+\.?\d{0,2})\s*/\s*(?:hr|hour|h)'

    seen = set()
    for gpu_m in re.finditer(vast_gpu_re, html, re.IGNORECASE):
        gpu_raw = gpu_m.group(1).strip()
        ctx = html[gpu_m.start():gpu_m.end() + 400]
        price_m = re.search(vast_price_re, ctx, re.IGNORECASE)
        if price_m:
            try:
                p = float(price_m.group(1))
                if 0.01 < p < 100 and gpu_raw.lower() not in seen:
                    seen.add(gpu_raw.lower())
                    gpu_label = normalize_gpu_name(gpu_raw)
                    results.append({"gpu": gpu_label, "price_usd": p, "plan": "市场起价"})
            except ValueError:
                continue

    if not results:
        results = extract_prices(html, COMMON_GPUS)

    if results:
        mark_ok("Vast.ai", len(results))
        return results
    mark_failed("Vast.ai", "未能解析价格数据（页面可能为 JS 动态渲染，需 Playwright）")
    return []


# ============================================================
# Playwright 浏览器自动化抓取
# ============================================================

def extract_prices_from_text(text: str) -> list[dict]:
    """从纯文本中提取 GPU 价格（Playwright 渲染后的文本）"""
    full_text = ' '.join(text.split('\n'))
    patterns = [
        (r'(RTX\s*\d{4}(?:\s*Ti)?(?:Super)?)\b.*?\$(\d+\.?\d{0,2})\s*/\s*(?:hr|hour|h)', False),
        (r'\b(H100|H200|A100|A6000|L40S?|A40|GH200|V100|T4|P100|P40)\b.*?\$(\d+\.?\d{0,2})\s*/\s*(?:hr|hour|h)', False),
        (r'\$(\d+\.?\d{0,2})\s*/\s*(?:hr|hour|h).{0,50}?\b(RTX\s*\d{4}|H100|H200|A100|A6000|L40S?|A40|GH200|V100|T4)\b', True),
    ]
    results = []
    seen = set()
    for pattern, swap_groups in patterns:
        for m in re.finditer(pattern, full_text, re.IGNORECASE):
            gpu_raw = (m.group(2) if swap_groups else m.group(1)).strip()
            price_str = (m.group(1) if swap_groups else m.group(2)).strip()
            try:
                price = float(price_str.replace(',', ''))
            except ValueError:
                continue
            gpu_label = normalize_gpu_name(gpu_raw)
            lo, hi = PRICE_RANGES.get(gpu_label, (0.01, 1000))
            if not (lo <= price <= hi):
                continue
            if gpu_label in seen:
                continue
            seen.add(gpu_label)
            results.append({"gpu": gpu_label, "price_usd": price, "plan": "市场价"})
    return results


def scrape_with_playwright(url: str, platform_name: str, wait_sec: int = 5,
                           wait_until: str = "load") -> list[dict]:
    """用 Playwright 无头浏览器访问页面，等待 JS 渲染后提取文本"""
    if not PLAYWRIGHT_AVAILABLE:
        scrape_log[platform_name] = {"status": "failed", "gpu_count": 0,
                                      "error": "Playwright 未安装"}
        print(f"  ❌ Playwright 未安装")
        return []

    print(f"  🌐 启动无头浏览器 ({platform_name}) ...")
    results = []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            try:
                page.goto(url, timeout=45000, wait_until=wait_until)
            except Exception:
                pass  # 即使超时也继续
            page.wait_for_timeout(wait_sec * 1000)

            body_text = page.inner_text("body")
            try:
                main_text = page.inner_text("main") or page.inner_text("#__next") or page.inner_text(".content")
                body_text = main_text + "\n" + body_text
            except Exception:
                pass
            browser.close()
            results = extract_prices_from_text(body_text)
    except Exception as e:
        scrape_log[platform_name] = {"status": "failed", "gpu_count": 0, "error": str(e)[:100]}
        print(f"  ❌ Playwright 异常: {e}")
        return []
    return results


# --- Playwright 专用爬虫 ---

def scrape_vast_playwright() -> list[dict]:
    """Vast.ai: Playwright 抓取"""
    print("🔍 Vast.ai (Playwright) ...")
    results = scrape_with_playwright("https://vast.ai/pricing", "Vast.ai",
                                      wait_sec=10, wait_until="networkidle")
    if results:
        mark_ok("Vast.ai", len(results))
        return results
    if scrape_log.get("Vast.ai", {}).get("status") != "failed":
        mark_failed("Vast.ai", "未提取到价格数据")
    return []


def scrape_lambda_playwright() -> list[dict]:
    """Lambda Labs: Playwright 修复版 - networkidle + 更长等待"""
    print("🔍 Lambda Labs (Playwright) ...")
    urls = [
        "https://lambdalabs.com/service/gpu-cloud/pricing",
        "https://lambdalabs.com/gpu-cloud",
        "https://lambdalabs.com/service/gpu-cloud",
    ]
    for url in urls:
        results = scrape_with_playwright(url, "Lambda Labs",
                                          wait_sec=8, wait_until="networkidle")
        if results:
            mark_ok("Lambda Labs", len(results))
            return results
    if scrape_log.get("Lambda Labs", {}).get("status") != "failed":
        mark_failed("Lambda Labs", "所有 URL 均未提取到价格数据")
    return []


def scrape_datacrunch_playwright() -> list[dict]:
    """DataCrunch: Playwright 抓取"""
    print("🔍 DataCrunch (Playwright) ...")
    results = scrape_with_playwright("https://datacrunch.io/pricing", "DataCrunch",
                                      wait_sec=6, wait_until="networkidle")
    if results:
        mark_ok("DataCrunch", len(results))
        return results
    if scrape_log.get("DataCrunch", {}).get("status") != "failed":
        mark_failed("DataCrunch", "未提取到价格数据")
    return []


def scrape_autodl_playwright() -> list[dict]:
    """AutoDL (中国): https://www.autodl.com/price - JS 渲染页面"""
    print("🔍 AutoDL (Playwright) ...")
    results = scrape_with_playwright("https://www.autodl.com/price", "AutoDL",
                                      wait_sec=8, wait_until="networkidle")
    if not results:
        # 尝试备用 URL
        results = scrape_with_playwright("https://www.autodl.com/price", "AutoDL",
                                          wait_sec=10, wait_until="load")
    if results:
        mark_ok("AutoDL", len(results))
        return results
    if scrape_log.get("AutoDL", {}).get("status") != "failed":
        mark_failed("AutoDL", "未提取到价格数据（可能需要调整 Playwright 等待时间）")
    return []


def scrape_matpool_playwright() -> list[dict]:
    """矩池云 Matpool: https://matpool.com/pricing"""
    print("🔍 Matpool 矩池云 (Playwright) ...")
    results = scrape_with_playwright("https://matpool.com/pricing", "Matpool",
                                      wait_sec=8, wait_until="networkidle")
    if results:
        mark_ok("Matpool", len(results))
        return results
    if scrape_log.get("Matpool", {}).get("status") != "failed":
        mark_failed("Matpool", "未提取到价格数据")
    return []


# ============================================================
# 通用平台爬虫（requests 模式 or Playwright fallback）
# ============================================================

def scrape_generic(name: str, url: str, use_pw: bool = False,
                   pw_fallback: bool = False) -> list[dict]:
    """
    通用爬虫：默认用 requests，如果 use_pw=True 则用 Playwright。
    若 pw_fallback=True 且 requests 失败，自动回退到 Playwright。
    """
    print(f"🔍 {name} ...")
    if use_pw:
        results = scrape_with_playwright(url, name, wait_sec=6, wait_until="networkidle")
        if results:
            mark_ok(name, len(results))
            return results
        if scrape_log.get(name, {}).get("status") != "failed":
            mark_failed(name, "Playwright 未提取到价格数据")
        return []

    # requests 模式
    html = get(url)
    if not html:
        if pw_fallback:
            # 回退到 Playwright
            print(f"  🔄 requests 失败，回退到 Playwright ...")
            results = scrape_with_playwright(url, name, wait_sec=6, wait_until="networkidle")
            if results:
                mark_ok(name, len(results))
                return results
        return mark_failed(name, "无法访问定价页面")

    results = extract_prices(html, COMMON_GPUS)
    if results:
        mark_ok(name, len(results))
        return results
    # 如果 requests 提取不到数据且允许回退，尝试 Playwright
    if pw_fallback:
        print(f"  🔄 requests 未提取到数据，回退到 Playwright ...")
        results = scrape_with_playwright(url, name, wait_sec=6, wait_until="networkidle")
        if results:
            mark_ok(name, len(results))
            return results
    mark_failed(name, "未能解析价格数据")
    return []


# ============================================================
# 平台注册表
# ============================================================
# 格式: (平台名, URL, 是否需要 Playwright)
# 按优先级排序：越靠前越重要

CORE_PLATFORMS = [
    # --- 核心高频平台 (每个周期都抓) ---
    ("Vast.ai",      "https://vast.ai/pricing",                    True),
    ("RunPod",       "https://www.runpod.io/pricing",              False),
    ("Lambda Labs",  "https://lambdalabs.com/service/gpu-cloud/pricing", True),
    ("CoreWeave",    "https://www.coreweave.com/pricing",          False),
    ("TensorDock",   "https://www.tensordock.com/",               False),
    ("Paperspace",   "https://www.paperspace.com/pricing",         False),
    ("JarvisLabs",   "https://jarvislabs.ai/pricing/",            False),
    ("DataCrunch",   "https://datacrunch.io/pricing",             True),
    ("AutoDL",       "https://www.autodl.com/price",              True),
]

EXTENDED_PLATFORMS = [
    # --- 欧洲平台 ---
    ("Hetzner",         "https://www.hetzner.com/cloud/gpu/",                False),
    ("OVHcloud",        "https://www.ovhcloud.com/en/public-cloud/prices/",  False),
    ("Scaleway",        "https://www.scaleway.com/en/gpu-instances/",        False),
    ("Genesis Cloud",   "https://genesiscloud.com/pricing",                  False),
    ("NexGen Cloud",    "https://www.nexgencloud.com/pricing",               False),
    ("Cudo Compute",    "https://www.cudocompute.com/",                      False),
    ("G-Core Labs",     "https://gcore.com/cloud/gpu-cloud",                 False),
    ("Cherry Servers",  "https://www.cherryservers.com/pricing/gpu-servers", False),
    ("LeaderGPU",       "https://www.leadergpu.com/pricing",                 False),
    ("Leaseweb",        "https://www.leaseweb.com/en/dedicated-servers/gpu", False),
    ("Hostkey",         "https://www.hostkey.com/gpu-servers",               False),
    ("UpCloud",         "https://upcloud.com/pricing/",                      False),
    ("Exoscale",        "https://www.exoscale.com/gpu/",                     False),
    ("21Cloud",         "https://www.21cloud.com/cloud/gpu-cloud",           False),
    ("Servers.com",     "https://www.servers.com/gpu-servers/",             False),
    ("Mystic AI",       "https://mystic.ai/pricing",                         False),

    # --- 北美平台 ---
    ("DigitalOcean",    "https://www.digitalocean.com/pricing/gpu-droplets", False),
    ("Vultr",           "https://www.vultr.com/products/cloud-gpu/",        False),
    ("FluidStack",      "https://www.fluidstack.io/pricing",                 False),
    ("Massed Compute",  "https://www.massedcompute.com/pricing",            False),
    ("Salad",           "https://salad.com/pricing",                         False),
    ("Hivelocity",      "https://www.hivelocity.net/products/gpu-servers/", False),
    ("SabrePC",         "https://www.sabrepc.com/hpc-cloud",                False),
    ("Bizon",           "https://bizon.ai/pricing",                          False),
    ("DataPacket",      "https://www.datapacket.com/gpu-hosting",           False),
    ("ServerMania",     "https://www.servermania.com/gpu-servers.htm",      False),
    ("Monster API",     "https://monsterapi.ai/pricing",                     False),
    ("Cerebrium",       "https://www.cerebrium.ai/pricing",                  False),

    # --- 中国平台 (需要 Playwright) ---
    ("Matpool",         "https://matpool.com/pricing",                       True),

    # --- 大厂平台 (页面结构复杂，成功率较低但不妨一试) ---
    ("Google Cloud",    "https://cloud.google.com/compute/gpus-pricing",    False),
    ("IBM Cloud",       "https://www.ibm.com/cloud/gpu",                    False),
    ("Oracle Cloud",    "https://www.oracle.com/cloud/compute/pricing/",    False),
]


# ============================================================
# 主流程
# ============================================================
def main():
    print("=" * 60)
    print("🚀 运算盘 · GPU 实时价格爬虫 v4")
    print(f"⏰ 开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print()

    use_pw = "--playwright" in sys.argv
    vast_only = "--vast-only" in sys.argv
    quick_mode = "--quick" in sys.argv

    if use_pw and not PLAYWRIGHT_AVAILABLE:
        print("⚠️ Playwright 未安装！请先运行:")
        print("   pip install playwright")
        print("   playwright install chromium")
        print()
        print("将使用 requests 模式继续...\n")
        use_pw = False

    if use_pw:
        print("🌐 Playwright 浏览器模式已启用\n")
    if vast_only:
        print("🎯 Vast.ai 专属模式（高频抓取）\n")
    if quick_mode:
        print("⚡ 快速模式（仅核心平台）\n")

    # --- 构建要执行的爬虫列表 ---
    all_data = {}

    if vast_only:
        # 仅 Vast.ai
        fn = scrape_vast_playwright if use_pw else scrape_vast
        try:
            results = fn()
            if results:
                all_data["Vast.ai"] = results
        except Exception as e:
            scrape_log["Vast.ai"] = {"status": "error", "gpu_count": 0, "error": str(e)}
            print(f"  ❌ 异常: {e}")
    else:
        # 确定要用的平台列表
        if quick_mode:
            platforms = CORE_PLATFORMS[:5]  # 前5个最高优先级
        else:
            platforms = CORE_PLATFORMS + EXTENDED_PLATFORMS

        # 专用爬虫映射表 (需要特殊逻辑的平台)
        custom_scrapers = {
            "Lambda Labs":  (scrape_lambda, scrape_lambda_playwright),
            "RunPod":       (scrape_runpod, scrape_runpod),
            "Vast.ai":      (scrape_vast, scrape_vast_playwright),
            "CoreWeave":    (scrape_coreweave, scrape_coreweave),
            "TensorDock":   (scrape_tensordock, scrape_tensordock),
            "DataCrunch":   (scrape_datacrunch, scrape_datacrunch_playwright),
            "Paperspace":   (scrape_paperspace, scrape_paperspace),
            "JarvisLabs":   (scrape_jarvislabs, scrape_jarvislabs),
            "AutoDL":       (None, scrape_autodl_playwright),  # 必须 Playwright
            "Matpool":      (None, scrape_matpool_playwright),  # 必须 Playwright
        }

        for name, url, needs_pw in platforms:
            try:
                if name in custom_scrapers:
                    req_fn, pw_fn = custom_scrapers[name]
                    if use_pw:
                        results = pw_fn()
                    elif req_fn:
                        results = req_fn()
                    else:
                        # 该平台必须 Playwright，但当前是 requests 模式，跳过
                        print(f"🔍 {name} ...")
                        print(f"  ⏭️ 跳过（需要 Playwright 模式）")
                        continue
                else:
                    # 通用爬虫
                    results = scrape_generic(name, url, use_pw=(use_pw and needs_pw), pw_fallback=use_pw)

                if results:
                    all_data[name] = results
            except Exception as e:
                scrape_log[name] = {"status": "error", "gpu_count": 0, "error": str(e)}
                print(f"  ❌ 异常: {e}")

    # ============================================================
    # 生成 pricing_live.js
    # ============================================================
    print("\n" + "=" * 60)
    print("📝 生成输出文件 ...")

    gpu_categories = {}
    for plat_name, gpus in all_data.items():
        for entry in gpus:
            label = entry["gpu"]
            if label not in gpu_categories:
                gpu_categories[label] = []
            gpu_categories[label].append({
                "platform": plat_name,
                "price_usd": entry["price_usd"],
                "plan": entry.get("plan", "按需"),
                "country": "",
                "region": "",
                "note": f"🟢 实时抓取 · {fetched_at}",
                "pricing_url": "",
                "source": "scraped"
            })

    CODE_DIR.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_LIVE, "w", encoding="utf-8") as f:
        f.write("// 运算盘 · 实时 GPU 价格数据\n")
        f.write(f"// 自动生成于: {fetched_at}\n")
        f.write("// ⚠️ 由 fetch_prices.py 自动生成，请勿手动编辑\n\n")
        f.write(f'var PRICE_FETCHED_AT = "{fetched_at}";\n')
        f.write(f"var PRICE_SCRAPE_SOURCES = {json.dumps(scrape_log, ensure_ascii=False, indent=2)};\n\n")
        f.write("var GPU_PRICING_LIVE = {\n")
        cats = list(gpu_categories.items())
        for i, (label, entries) in enumerate(cats):
            comma = "," if i < len(cats) - 1 else ""
            f.write(f'  "{label}": [\n')
            for j, e in enumerate(entries):
                ec = "," if j < len(entries) - 1 else ""
                f.write(f'    {{ "platform": "{e["platform"]}", "price_usd": {e["price_usd"]}, '
                        f'"plan": "{e["plan"]}", "country": "{e["country"]}", "region": "{e["region"]}", '
                        f'"note": "{e["note"]}", "pricing_url": "{e["pricing_url"]}", "source": "{e["source"]}" }}{ec}\n')
            f.write(f"  ]{comma}\n")
        f.write("};\n")

    total = sum(len(v) for v in all_data.values())
    print(f"✅ {OUTPUT_LIVE.name}: {len(gpu_categories)} GPU 类别, {total} 条价格")

    # ============================================================
    # 保存/追加历史数据
    # ============================================================
    if "--save-history" in sys.argv:
        today_str = datetime.now().strftime("%Y-%m-%d")
        history_data = {"snapshots": []}
        if OUTPUT_HIST.exists():
            try:
                raw = OUTPUT_HIST.read_text(encoding="utf-8")
                m = re.search(r'PRICE_HISTORY_DATA\s*=\s*(\{.*\});', raw, re.DOTALL)
                if m:
                    history_data = json.loads(m.group(1))
            except Exception:
                pass

        snap = {"date": today_str, "prices": {}}
        for label, entries in gpu_categories.items():
            snap["prices"][label] = [
                {"platform": e["platform"], "price_usd": e["price_usd"]}
                for e in entries
            ]

        replaced = False
        for i, s in enumerate(history_data["snapshots"]):
            if s["date"] == today_str:
                history_data["snapshots"][i] = snap
                replaced = True
                break
        if not replaced:
            history_data["snapshots"].append(snap)
        if len(history_data["snapshots"]) > 90:
            history_data["snapshots"] = history_data["snapshots"][-90:]

        with open(OUTPUT_HIST, "w", encoding="utf-8") as f:
            f.write("var PRICE_HISTORY_DATA = ")
            json.dump(history_data, f, indent=2, ensure_ascii=False)
            f.write(";\n")

        with open(OUTPUT_HIST_JSON, "w", encoding="utf-8") as f:
            json.dump(history_data, f, indent=2, ensure_ascii=False)

        action = "更新" if replaced else "追加"
        print(f"📝 历史数据已{action}: {OUTPUT_HIST.name} (共 {len(history_data['snapshots'])} 天)")

    # ============================================================
    # 总结
    # ============================================================
    platform_count = len(scrape_log)
    ok_count = sum(1 for v in scrape_log.values() if v["status"] == "ok")
    fail_count = platform_count - ok_count

    print(f"\n📋 抓取结果: {platform_count} 平台, ✅ {ok_count} 成功, ❌ {fail_count} 失败")
    for name, info in scrape_log.items():
        if info["status"] == "ok":
            print(f"  ✅ {name}: {info['gpu_count']} 款 GPU")
        else:
            err = info.get('error', 'Unknown')
            print(f"  ❌ {name}: {err[:80]}")

    if total == 0:
        print("\n⚠️ 警告: 未抓取到任何价格数据！")
        print("   可能原因: 1) 网络问题 2) 平台页面结构变更 3) 需要浏览器渲染")
        print("   建议: 使用参考数据 pricing.js 作为 fallback")
    else:
        print(f"\n✅ 共抓取 {total} 条实时价格，刷新页面即可查看 🟢 实时标记的数据")

    return 0


# 重导出旧版函数引用以兼容 main() 中的 custom_scrapers 字典
scrape_coreweave = lambda: scrape_generic("CoreWeave", "https://www.coreweave.com/pricing")
scrape_tensordock = lambda: scrape_generic("TensorDock", "https://www.tensordock.com/")
scrape_datacrunch = lambda: scrape_generic("DataCrunch", "https://datacrunch.io/pricing")
scrape_paperspace = lambda: scrape_generic("Paperspace", "https://www.paperspace.com/pricing")
scrape_jarvislabs = lambda: scrape_generic("JarvisLabs", "https://jarvislabs.ai/pricing/")


if __name__ == "__main__":
    sys.exit(main())
