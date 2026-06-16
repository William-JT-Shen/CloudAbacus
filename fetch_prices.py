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
from _availability import scrape_vast_rental_scale, get_rental_scale_str

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
def get(url: str, accept_any_status: bool = False) -> str | None:
    """HTTP GET，返回文本，失败返回 None
    accept_any_status: 若为 True，即使非 200 也返回内容（用于 SPA 返回 404 但有内容的场景）"""
    try:
        r = requests.get(url, timeout=TIMEOUT, headers={"User-Agent": UA}, allow_redirects=True)
        if r.status_code == 200:
            return r.text
        if accept_any_status and len(r.text) > 5000:
            return r.text  # SPA 页面可能返回 404 但包含实际内容
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
    "NVIDIA V100":                     (0.10, 3.00),  # 含 TensorDock 低价
    "NVIDIA RTX 6000 Ada / A6000":     (0.25, 2.00),
    "NVIDIA RTX 4090":                 (0.15, 1.50),
    "NVIDIA RTX 4080 / 4080 Super":    (0.10, 1.20),
    "NVIDIA RTX 4070 Ti / 4070":       (0.08, 0.80),
    "NVIDIA RTX 4060 Ti":              (0.05, 0.50),
    "NVIDIA RTX 3090 / 3090 Ti":       (0.08, 0.80),
    "NVIDIA RTX 3080 / 3080 Ti":       (0.06, 1.20),  # 含服务器溢价
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


def extract_prices(html: str, gpu_map: list[tuple[str, str, str]],
                   currency: str = "USD") -> list[dict]:
    """从 HTML 中提取 GPU 价格（带合理性校验）
    currency: "USD" 或 "EUR" — 欧元价格会自动转换为美元"""
    results = []
    seen = set()
    eur_to_usd = 1.08  # EUR → USD 汇率（近似）
    for gpu_re, price_re, label in gpu_map:
        lo, hi = PRICE_RANGES.get(label, (0.01, 1000))
        # 欧元价格范围 = USD 范围 / 汇率
        if currency == "EUR":
            lo, hi = lo / eur_to_usd, hi / eur_to_usd
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
                        price_usd = round(price * eur_to_usd, 2) if currency == "EUR" else price
                        results.append({"gpu": label, "price_usd": price_usd})
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


# 欧元价格模式 (用于欧洲平台)
# 格式: €X.XX/h, €X.XX per hour, X.XX €/h 等
COMMON_GPUS_EUR = [
    (r'H200\b',                   r'€\s*(\d+\.?\d*)\s*/\s*(?:h|hr|hour)', "NVIDIA H200"),
    (r'GH200\b',                  r'€\s*(\d+\.?\d*)\s*/\s*(?:h|hr|hour)', "NVIDIA GH200"),
    (r'H100\b.*?80\s*GB',         r'€\s*(\d+\.?\d*)\s*/\s*(?:h|hr|hour)', "NVIDIA H100 (80GB SXM)"),
    (r'H100\b(?!.*SXM)',          r'€\s*(\d+\.?\d*)\s*/\s*(?:h|hr|hour)', "NVIDIA H100 (80GB SXM)"),
    (r'A100\b.*?80\s*GB',         r'€\s*(\d+\.?\d*)\s*/\s*(?:h|hr|hour)', "NVIDIA A100 (80GB SXM)"),
    (r'A100\b.*?40\s*GB',         r'€\s*(\d+\.?\d*)\s*/\s*(?:h|hr|hour)', "NVIDIA A100 (40GB PCIe)"),
    (r'L40S\b',                   r'€\s*(\d+\.?\d*)\s*/\s*(?:h|hr|hour)', "NVIDIA L40S"),
    (r'L4\b(?!\d)',               r'€\s*(\d+\.?\d*)\s*/\s*(?:h|hr|hour)', "NVIDIA L4"),
    (r'A40\b(?!\d)',              r'€\s*(\d+\.?\d*)\s*/\s*(?:h|hr|hour)', "NVIDIA A40"),
    (r'T4\b(?!\d)',               r'€\s*(\d+\.?\d*)\s*/\s*(?:h|hr|hour)', "NVIDIA T4"),
    (r'V100\b',                   r'€\s*(\d+\.?\d*)\s*/\s*(?:h|hr|hour)', "NVIDIA V100"),
    (r'A6000\b.*?Ada',            r'€\s*(\d+\.?\d*)\s*/\s*(?:h|hr|hour)', "NVIDIA RTX 6000 Ada / A6000"),
    (r'RTX\s*A?6000\b(?!.*Ada)',  r'€\s*(\d+\.?\d*)\s*/\s*(?:h|hr|hour)', "NVIDIA RTX 6000 Ada / A6000"),
    (r'RTX\s*5090\b',             r'€\s*(\d+\.?\d*)\s*/\s*(?:h|hr|hour)', "RTX 5090"),
    (r'RTX\s*5080\b',             r'€\s*(\d+\.?\d*)\s*/\s*(?:h|hr|hour)', "RTX 5080"),
    (r'RTX\s*5070\s*Ti',         r'€\s*(\d+\.?\d*)\s*/\s*(?:h|hr|hour)', "RTX 5070 Ti"),
    (r'RTX\s*5070\b',             r'€\s*(\d+\.?\d*)\s*/\s*(?:h|hr|hour)', "RTX 5070"),
    (r'RTX\s*5060\s*Ti',         r'€\s*(\d+\.?\d*)\s*/\s*(?:h|hr|hour)', "RTX 5060 Ti"),
    (r'RTX\s*5060\b',             r'€\s*(\d+\.?\d*)\s*/\s*(?:h|hr|hour)', "RTX 5060"),
    (r'RTX\s*4090\b',             r'€\s*(\d+\.?\d*)\s*/\s*(?:h|hr|hour)', "NVIDIA RTX 4090"),
    (r'RTX\s*4080\b',             r'€\s*(\d+\.?\d*)\s*/\s*(?:h|hr|hour)', "NVIDIA RTX 4080 / 4080 Super"),
    (r'RTX\s*4070\s*Ti',         r'€\s*(\d+\.?\d*)\s*/\s*(?:h|hr|hour)', "NVIDIA RTX 4070 Ti / 4070"),
    (r'RTX\s*4070\b',             r'€\s*(\d+\.?\d*)\s*/\s*(?:h|hr|hour)', "NVIDIA RTX 4070 Ti / 4070"),
    (r'RTX\s*4060\s*Ti',         r'€\s*(\d+\.?\d*)\s*/\s*(?:h|hr|hour)', "NVIDIA RTX 4060 Ti"),
    (r'RTX\s*3090\b',             r'€\s*(\d+\.?\d*)\s*/\s*(?:h|hr|hour)', "NVIDIA RTX 3090 / 3090 Ti"),
    (r'RTX\s*3080\b',             r'€\s*(\d+\.?\d*)\s*/\s*(?:h|hr|hour)', "NVIDIA RTX 3080 / 3080 Ti"),
    (r'RTX\s*3070\b',             r'€\s*(\d+\.?\d*)\s*/\s*(?:h|hr|hour)', "NVIDIA RTX 3070 / 3070 Ti"),
    (r'RTX\s*3060\b',             r'€\s*(\d+\.?\d*)\s*/\s*(?:h|hr|hour)', "NVIDIA RTX 3060 / 3060 Ti"),
    (r'P100\b',                   r'€\s*(\d+\.?\d*)\s*/\s*(?:h|hr|hour)', "NVIDIA Tesla P100 / P40"),
    (r'P40\b',                    r'€\s*(\d+\.?\d*)\s*/\s*(?:h|hr|hour)', "NVIDIA Tesla P100 / P40"),
    (r'K80\b',                    r'€\s*(\d+\.?\d*)\s*/\s*(?:h|hr|hour)', "NVIDIA Tesla K80 / M40 / M60"),
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
    # 去除 VRAM 后缀，如 "RTX 5090 (32 GB)" → "RTX 5090"
    key = re.sub(r'\s*\(\d+\s*GB\)', '', key, flags=re.IGNORECASE).strip()
    # 去除 "Ti Super" → "Ti" (如 "RTX 4070 Ti Super" → "RTX 4070 Ti")
    key = re.sub(r'\s*Ti\s+Super', ' Ti', key, flags=re.IGNORECASE).strip()
    # 去除 "Super" 后缀
    key = re.sub(r'\s+Super', '', key, flags=re.IGNORECASE).strip()
    return mapping.get(key, raw)


# ============================================================
# 专用爬虫（需要特殊处理逻辑的平台）
# ============================================================

def scrape_lambda():
    """Lambda Labs → lambda.ai: 域名已迁移，多 URL 回退"""
    print("🔍 Lambda Labs (lambda.ai) ...")
    urls = [
        "https://lambda.ai/pricing",
        "https://lambdalabs.com/pricing",
        "https://lambdalabs.com/service/gpu-cloud/pricing",
        "https://lambdalabs.com/gpu-cloud",
    ]
    html = None
    for url in urls:
        html = get(url)
        if html:
            break
    if not html:
        return mark_failed("Lambda Labs", "所有 URL 均无法访问 (lambda.ai 需 JS 渲染)")

    results = extract_prices(html, COMMON_GPUS)
    if results:
        mark_ok("Lambda Labs", len(results))
        return results
    mark_failed("Lambda Labs", "未能解析价格数据（SPA 页面需 Playwright 渲染）")
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


def scrape_tensordock_dedicated():
    """TensorDock: 从 HTML 表格直接提取 GPU 价格 (<th>GPU名</th><td>\$X.XX</td>)"""
    print("🔍 TensorDock (dedicated) ...")
    html = get("https://www.tensordock.com/cloud-gpus.html")
    if not html:
        return mark_failed("TensorDock", "无法访问 cloud-gpus.html")

    results = []
    seen = set()

    # TensorDock 页面使用表格: <th>GPU名</th><td>$X.XX</td>
    # 直接匹配每一行的 GPU 名称和价格
    table_rows = re.findall(
        r'<th[^>]*>\s*([^<]+?)\s*</th>\s*<td[^>]*>\s*\$(\d+\.?\d{0,2})\s*</td>',
        html, re.IGNORECASE
    )

    for gpu_name, price_str in table_rows:
        gpu_name = gpu_name.strip()
        try:
            price = float(price_str)
        except ValueError:
            continue

        # 标准化 GPU 名称 (TensorDock 使用 "H100 SXM5 80GB" 等格式)
        gpu_label = normalize_gpu_name(gpu_name)
        # 处理 TensorDock 特有的命名: "H100 SXM5 80GB" → "NVIDIA H100 (80GB SXM)"
        # normalize_gpu_name 对某些名称可能不完美，手动映射
        name_lower = gpu_name.lower()
        if 'h100' in name_lower and 'sxm' in name_lower:
            gpu_label = "NVIDIA H100 (80GB SXM)"
        elif 'h100' in name_lower and 'pci' in name_lower:
            gpu_label = "NVIDIA H100 (80GB SXM)"
        elif 'a100' in name_lower and 'sxm' in name_lower:
            gpu_label = "NVIDIA A100 (80GB SXM)"
        elif 'a100' in name_lower and 'pci' in name_lower:
            gpu_label = "NVIDIA A100 (40GB PCIe)"
        elif 'v100' in name_lower:
            gpu_label = "NVIDIA V100"
        elif 'a6000' in name_lower:
            gpu_label = "NVIDIA RTX 6000 Ada / A6000"
        elif 'rtx 6000 ada' in name_lower:
            gpu_label = "NVIDIA RTX 6000 Ada / A6000"
        elif 'rtx 4090' in name_lower:
            gpu_label = "NVIDIA RTX 4090"
        elif 'rtx 3090' in name_lower:
            gpu_label = "NVIDIA RTX 3090 / 3090 Ti"
        elif 'l40' in name_lower:
            gpu_label = "NVIDIA L40S"
        else:
            gpu_label = normalize_gpu_name(gpu_name)

        lo, hi = PRICE_RANGES.get(gpu_label, (0.01, 1000))
        if lo <= price <= hi and gpu_label not in seen:
            seen.add(gpu_label)
            results.append({"gpu": gpu_label, "price_usd": price, "plan": "GPU起价"})

    if results:
        mark_ok("TensorDock", len(results))
        return results

    # 回退: 通用提取
    results = extract_prices(html, COMMON_GPUS)
    if results:
        mark_ok("TensorDock", len(results))
        return results
    mark_failed("TensorDock", "未能从表格提取价格")
    return []


# ============================================================
# JS 内嵌数据提取器（价格存在 <script> 标签的 JS 对象中）
# ============================================================

def extract_prices_from_js_object(html: str, obj_name: str,
                                   gpu_key: str = "name",
                                   price_key: str = "basePrice") -> list[dict]:
    """从 HTML 中提取 JS 对象里的 GPU 价格数据。
    适用于 Salad 等将价格嵌入 <script> 的平台。
    例如: const GPU_DATA = { gpus: [{ name: "RTX 4090", basePrice: 0.16 }] }"""
    # 匹配 JS 对象定义（支持 const/var/let）
    pat = rf'(?:const|var|let)\s+{obj_name}\s*=\s*(\{{.*?\}})\s*;'
    m = re.search(pat, html, re.DOTALL)
    if not m:
        return []

    obj_text = m.group(1)
    results = []
    seen = set()

    # 在每个对象中递归查找 GPU 条目
    # 匹配 { name: "...", basePrice: X.XX } 模式
    item_pat = r'\{\s*' + gpu_key + r'\s*:\s*["\']([^"\']+)["\'].*?' + price_key + r'\s*:\s*(\d+\.?\d*)'
    for item_m in re.finditer(item_pat, obj_text, re.IGNORECASE | re.DOTALL):
        gpu_raw = item_m.group(1).strip()
        try:
            price = float(item_m.group(2))
        except ValueError:
            continue
        gpu_label = normalize_gpu_name(gpu_raw)
        lo, hi = PRICE_RANGES.get(gpu_label, (0.01, 1000))
        if lo <= price <= hi and gpu_label not in seen:
            seen.add(gpu_label)
            results.append({"gpu": gpu_label, "price_usd": price, "plan": "市场价"})

    return results


# ============================================================
# Playwright 浏览器自动化抓取
# ============================================================

def extract_prices_from_text(text: str, currency: str = "USD") -> list[dict]:
    """从纯文本中提取 GPU 价格（Playwright 渲染后的文本）
    currency: "USD" 用 $ 匹配, "EUR" 用 € 匹配并转美元"""
    full_text = ' '.join(text.split('\n'))
    eur_to_usd = 1.08
    currency_char = '[$]' if currency == 'USD' else '[€]'

    patterns = [
        # $X.XX/hr or €X.XX/hr after GPU name
        (rf'(RTX\s*\d{{4}}(?:\s*Ti)?(?:Super)?)\b.*?{currency_char}(\d+\.?\d{{0,2}})\s*/\s*(?:hr|hour|h)', False),
        (rf'\b(H100|H200|A100|A6000|L40S?|A40|GH200|V100|T4|P100|P40)\b.*?{currency_char}(\d+\.?\d{{0,2}})\s*/\s*(?:hr|hour|h)', False),
        # Price before GPU name
        (rf'{currency_char}(\d+\.?\d{{0,2}})\s*/\s*(?:hr|hour|h).{{0,50}}?\b(RTX\s*\d{{4}}|H100|H200|A100|A6000|L40S?|A40|GH200|V100|T4)\b', True),
        # Per-second pricing: $0.000123/sec → convert to hourly
        (rf'(RTX\s*\d{{4}}(?:\s*Ti)?(?:Super)?)\b.*?{currency_char}(\d+\.?\d{{0,8}})\s*/\s*(?:sec|second|s)\b', False),
        (rf'\b(H100|H200|A100|A6000|L40S?|A40|GH200|V100|T4|P100|P40)\b.*?{currency_char}(\d+\.?\d{{0,8}})\s*/\s*(?:sec|second|s)\b', False),
    ]
    results = []
    seen = set()
    for pattern, swap_groups in patterns:
        is_per_sec = 'sec|second|s' in pattern.split('(?:')[-1] if '(?:' in pattern else False
        for m in re.finditer(pattern, full_text, re.IGNORECASE):
            gpu_raw = (m.group(2) if swap_groups else m.group(1)).strip()
            price_str = (m.group(1) if swap_groups else m.group(2)).strip()
            try:
                price = float(price_str.replace(',', ''))
            except ValueError:
                continue
            if is_per_sec:
                price = price * 3600  # 每秒 → 每小时
            if currency == 'EUR':
                price = price * eur_to_usd
            gpu_label = normalize_gpu_name(gpu_raw)
            lo, hi = PRICE_RANGES.get(gpu_label, (0.01, 1000))
            if not (lo <= price <= hi):
                continue
            if gpu_label in seen:
                continue
            seen.add(gpu_label)
            price = round(price, 2)
            results.append({"gpu": gpu_label, "price_usd": price, "plan": "市场价"})
    return results


def scrape_with_playwright(url: str, platform_name: str, wait_sec: int = 5,
                           wait_until: str = "load", is_eur: bool = False) -> list[dict]:
    """用 Playwright 无头浏览器访问页面，等待 JS 渲染后提取文本
    is_eur: 也尝试欧元价格模式"""
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
            page.set_default_timeout(60000)
            try:
                page.goto(url, timeout=60000, wait_until=wait_until)
            except Exception:
                pass  # 即使超时也继续
            page.wait_for_timeout(wait_sec * 1000)

            # 尝试关闭 Cookie / 弹窗
            dismiss_selectors = [
                "button:has-text('Accept All')",
                "button:has-text('Accept All Cookies')",
                "button:has-text('Accept')",
                "button:has-text('OK')",
                "button:has-text('Got it')",
                "button:has-text('Decline')",
                "button:has-text('Deny')",
                "[aria-label='Close']",
                "[aria-label='Dismiss']",
                ".cookie-accept",
                ".cc-btn",
                "#onetrust-accept-btn-handler",
            ]
            for sel in dismiss_selectors:
                try:
                    btn = page.locator(sel).first
                    if btn.is_visible(timeout=2000):
                        btn.click()
                        page.wait_for_timeout(2000)
                        break
                except Exception:
                    continue

            # 滚动页面以触发懒加载内容
            try:
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                page.wait_for_timeout(2000)
            except Exception:
                pass

            body_text = page.inner_text("body")
            try:
                main_text = (page.inner_text("main") or page.inner_text("#__next") or
                           page.inner_text("#root") or page.inner_text(".content") or
                           page.inner_text("[role='main']"))
                body_text = main_text + "\n" + body_text
            except Exception:
                pass
            browser.close()
            results = extract_prices_from_text(body_text)
            if not results and is_eur:
                results = extract_prices_from_text(body_text, currency="EUR")
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
    """Lambda.ai: Playwright 修复版 — 域名已迁移到 lambda.ai"""
    print("🔍 Lambda Labs (lambda.ai Playwright) ...")
    urls = [
        "https://lambda.ai/pricing",
        "https://lambdalabs.com/pricing",
        "https://lambdalabs.com/service/gpu-cloud/pricing",
    ]
    for url in urls:
        results = scrape_with_playwright(url, "Lambda Labs",
                                          wait_sec=14, wait_until="networkidle")
        if not results:
            results = scrape_with_playwright(url, "Lambda Labs",
                                              wait_sec=14, wait_until="load")
        if results:
            mark_ok("Lambda Labs", len(results))
            return results
    if scrape_log.get("Lambda Labs", {}).get("status") != "failed":
        mark_failed("Lambda Labs", "所有 URL 均未提取到价格数据（SPA 动态加载，可能需要更长的等待时间）")
    return []


def scrape_datacrunch_playwright() -> list[dict]:
    """DataCrunch → Verda: 已更名为 verda.com"""
    print("🔍 DataCrunch/Verda (Playwright) ...")
    urls = [
        "https://verda.com/pricing",
        "https://datacrunch.io/pricing",
        "https://verda.com/gpu-cloud",
    ]
    for url in urls:
        results = scrape_with_playwright(url, "DataCrunch",
                                          wait_sec=14, wait_until="networkidle")
        if not results:
            results = scrape_with_playwright(url, "DataCrunch",
                                              wait_sec=14, wait_until="load")
        if results:
            mark_ok("DataCrunch", len(results))
            return results
    if scrape_log.get("DataCrunch", {}).get("status") != "failed":
        mark_failed("DataCrunch", "Verda 页面未提取到价格数据（可能需要更长的 JS 等待时间）")
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
# 专用爬虫：JS 内嵌数据平台
# ============================================================

def scrape_salad():
    """Salad: https://salad.com/pricing — 价格在 GPU_DATA JS 对象中"""
    print("🔍 Salad ...")
    html = get("https://salad.com/pricing")
    if not html:
        return mark_failed("Salad", "无法访问定价页面")

    results = extract_prices_from_js_object(html, "GPU_DATA", "name", "basePrice")
    if results:
        mark_ok("Salad", len(results))
        return results

    # 回退: 试试通用提取
    results = extract_prices(html, COMMON_GPUS)
    if results:
        mark_ok("Salad", len(results))
        return results
    mark_failed("Salad", "未能解析 JS 内嵌价格数据")
    return []


def scrape_hostkey():
    """Hostkey: https://hostkey.com/gpu-dedicated-servers/ — JSON-LD 嵌入数据 + 欧元月租→小时转换"""
    print("🔍 Hostkey ...")
    html = get("https://hostkey.com/gpu-dedicated-servers/")
    if not html:
        return mark_failed("Hostkey", "无法访问定价页面")

    results = []
    seen = set()
    eur_to_usd = 1.08
    hours_per_month = 730  # 月租 → 时租 转换

    # 从 JSON-LD 提取产品数据
    for m in re.finditer(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>',
                         html, re.DOTALL):
        try:
            data = json.loads(m.group(1))
            if not isinstance(data, dict) or 'itemListElement' not in data:
                continue
            items = data['itemListElement']
            if len(items) < 10:
                continue  # 不是产品列表

            for item in items:
                prod = item.get('item', {})
                offers = prod.get('offers', {})
                if not isinstance(offers, dict):
                    continue
                price_eur = offers.get('price')
                if not price_eur:
                    continue
                try:
                    price_eur = float(price_eur)
                except (ValueError, TypeError):
                    continue

                # 从 additionalProperty 提取 GPU 型号
                gpu_raw = None
                for prop in prod.get('additionalProperty', []):
                    if prop.get('name', '').lower() == 'gpu':
                        val = str(prop.get('value', ''))
                        # 格式: "1xRTX 4090 24GB" → 提取 GPU 型号
                        # 去掉数量和 VRAM
                        gpu_part = re.sub(r'^\d+x\s*', '', val)
                        gpu_part = re.sub(r'\s*\d+\s*GB$', '', gpu_part, flags=re.IGNORECASE)
                        gpu_raw = gpu_part.strip()
                        break

                if not gpu_raw:
                    continue

                gpu_label = normalize_gpu_name(gpu_raw)
                lo, hi = PRICE_RANGES.get(gpu_label, (0.01, 1000))

                # 月租转时租
                price_hourly_eur = price_eur / hours_per_month
                price_hourly_usd = round(price_hourly_eur * eur_to_usd, 2)

                if lo <= price_hourly_usd <= hi and gpu_label not in seen:
                    seen.add(gpu_label)
                    results.append({
                        "gpu": gpu_label,
                        "price_usd": price_hourly_usd,
                        "plan": f"月租€{price_eur}/月 ≈ €{price_hourly_eur:.3f}/时"
                    })

        except (json.JSONDecodeError, ValueError, KeyError):
            continue

    if results:
        mark_ok("Hostkey", len(results))
        return results

    # 回退: 尝试 EUR 模式
    results = extract_prices(html, COMMON_GPUS_EUR, currency="EUR")
    if results:
        mark_ok("Hostkey", len(results))
        return results
    mark_failed("Hostkey", "未能解析 JSON-LD 价格数据")
    return []


def scrape_upcloud():
    """UpCloud: https://upcloud.com/pricing/ — 欧元定价"""
    print("🔍 UpCloud ...")
    html = get("https://upcloud.com/pricing/")
    if not html:
        return mark_failed("UpCloud", "无法访问定价页面")

    results = extract_prices(html, COMMON_GPUS_EUR, currency="EUR")
    if not results:
        results = extract_prices(html, COMMON_GPUS)
    if results:
        mark_ok("UpCloud", len(results))
        return results
    mark_failed("UpCloud", "未能解析价格数据")
    return []


def scrape_hetzner():
    """Hetzner: https://www.hetzner.com/cloud/gpu/ — requests 优先，失败回退 Playwright"""
    print("🔍 Hetzner ...")
    urls = [
        "https://www.hetzner.com/cloud/gpu/",
        "https://www.hetzner.com/cloud",
    ]
    # 第一步: 尝试 requests (Hetzner 部分页面仍可静态解析)
    for url in urls:
        html = get(url)
        if not html:
            continue
        results = extract_prices(html, COMMON_GPUS_EUR, currency="EUR")
        if not results:
            results = extract_prices(html, COMMON_GPUS)
        if results:
            mark_ok("Hetzner", len(results))
            return results

    # 第二步: requests 失败，回退到 Playwright 浏览器渲染
    if PLAYWRIGHT_AVAILABLE:
        print("  🔄 requests 未提取到数据，回退到 Playwright ...")
        for url in urls:
            results = scrape_with_playwright(url, "Hetzner", wait_sec=12, wait_until="networkidle")
            if not results:
                results = scrape_with_playwright(url, "Hetzner", wait_sec=12, wait_until="load")
            if results:
                # 欧元价格转换
                for r in results:
                    if r.get("plan") == "市场价":
                        r["plan"] = "€/时按需"
                mark_ok("Hetzner", len(results))
                return results

    mark_failed("Hetzner", "页面 JS 动态渲染，Playwright 也未提取到价格数据")
    return []


def scrape_nexgen_cloud():
    """NexGen Cloud / Hyperstack: 从各 GPU 独立页面提取准确价格。
    /gpu-pricing 页面 GPU 名称与价格卡片不在同一 DOM 区域，容易产生错误匹配。"""
    print("🔍 NexGen Cloud (Hyperstack) ...")

    # 各 GPU 的独立定价页面 (每个页面只列该 GPU 的价格，避免错配)
    GPU_PAGES = {
        "https://www.hyperstack.cloud/nvidia-h100-sxm":    "NVIDIA H100 (80GB SXM)",
        "https://www.hyperstack.cloud/h100-pcie":          "NVIDIA H100 (80GB SXM)",  # H100 PCIe variant
        "https://www.hyperstack.cloud/a100":               "NVIDIA A100 (80GB SXM)",
        "https://www.hyperstack.cloud/nvidia-hgx-b300":    "NVIDIA H200",            # B300 ≈ H200 tier
        "https://www.hyperstack.cloud/nvidia-gb300-nvl72": "NVIDIA GH200",           # GB300 ≈ GH200 tier
    }

    results = []
    seen = set()

    for url, gpu_label in GPU_PAGES.items():
        html = get(url)
        if not html:
            continue
        # 在独立页面中提取该 GPU 的价格 (页面只含一种 GPU, 避免导航菜单干扰)
        page_results = extract_prices(html, COMMON_GPUS)
        for r in page_results:
            # 修正 GPU 名称为预期型号 (页面内无其他 GPU 干扰)
            r["gpu"] = gpu_label
            # 取该 GPU 的最低价格
            if gpu_label not in seen:
                seen.add(gpu_label)
                results.append(r)
                print(f"    {gpu_label}: \${r['price_usd']}/hr from {url.split('/')[-1]}")

    if results:
        mark_ok("NexGen Cloud", len(results))
        return results

    # 回退: 尝试通用提取
    html = get("https://www.hyperstack.cloud/gpu-pricing")
    if html:
        results = extract_prices(html, COMMON_GPUS)
        if results:
            mark_ok("NexGen Cloud", len(results))
            return results

    mark_failed("NexGen Cloud", "所有页面均未提取到价格数据")
    return []


def scrape_cerebrium():
    """Cerebrium: https://www.cerebrium.ai/pricing — 按秒计费，需 Playwright + 特殊提取"""
    print("🔍 Cerebrium ...")
    html = get("https://www.cerebrium.ai/pricing")
    if html:
        # Cerebrium 的 price 可能在 JS 对象中（非标准格式）
        # 尝试从 JSON-LD 的 featureList 获取 GPU 列表 + 页面文本获取价格
        results = extract_prices(html, COMMON_GPUS)
        if results:
            mark_ok("Cerebrium", len(results))
            return results

    # Playwright 回退（Cerebrium 按秒计费，价格很低如 $0.0001/sec）
    results = scrape_with_playwright("https://www.cerebrium.ai/pricing",
                                      "Cerebrium", wait_sec=10,
                                      wait_until="networkidle")
    if results:
        mark_ok("Cerebrium", len(results))
        return results
    if scrape_log.get("Cerebrium", {}).get("status") != "failed":
        mark_failed("Cerebrium", "未提取到价格数据（按秒计费，格式特殊）")
    return []


def scrape_scaleway():
    """Scaleway: 通过 Next.js _next/data API 提取 GPU 实例价格"""
    print("🔍 Scaleway ...")
    eur_to_usd = 1.08

    # 通过 Scaleway 的 Next.js 数据端点获取 GPU 实例定价
    # 先获取当前 build ID (Next.js 每次部署会更新)
    html = get("https://www.scaleway.com/en/gpu-instances/")
    build_id = None
    if html:
        m = re.search(r'\"buildId\"\s*:\s*\"([^\"]+)\"', html)
        if m:
            build_id = m.group(1)
    if not build_id:
        return mark_failed("Scaleway", "无法获取 Next.js build ID")

    api_url = f"https://www.scaleway.com/_next/data/{build_id}/en/gpu-instances.json?slug=en&slug=gpu-instances"
    try:
        r = requests.get(api_url, timeout=TIMEOUT, headers={"User-Agent": UA})
        if r.status_code != 200:
            return mark_failed("Scaleway", f"API 返回 {r.status_code}")
        data = r.json()
    except Exception as e:
        return mark_failed("Scaleway", f"API 请求失败: {e}")

    data_str = json.dumps(data)

    # GPU 实例产品名格式: H100-SXM-8-80G, L40S-2-48G, L4-1-24G
    # 价格在 nanos/units 字段中。两阶段提取: 先找产品名, 再找其价格
    gpu_base_prices = {}  # {gpu_label: (min_price_eur, vcpus)}

    # 匹配所有 GPU 产品条目 (name + nanos + units)
    product_blocks = re.findall(
        r'"name"\s*:\s*"((?:H100-SXM|H100|L40S|L4|B300-SXM|GH200|A100|H200|B200)'
        r'-\d+-\d+G)".*?"nanos"\s*:\s*(\d+).*?"units"\s*:\s*(\d+)',
        data_str, re.IGNORECASE
    )

    for product_name, nanos_str, units_str in product_blocks:
        # 解析产品名: H100-SXM-8-80G → gpu_model=H100-SXM, vcpus=8, vram=80
        parts = product_name.split('-')
        if len(parts) < 3:
            continue
        # 重组 GPU 型号 (可能含 SXM 后缀)
        if parts[1].upper() == 'SXM' and len(parts) >= 4:
            gpu_model = f"{parts[0]}-{parts[1]}".upper()
            vcpus = int(parts[2])
        else:
            gpu_model = parts[0].upper()
            vcpus = int(parts[1])

        nanos = int(nanos_str)
        units = int(units_str)
        price_eur = (units * 1_000_000_000 + nanos) / 1_000_000_000

        # 标准化 GPU 名称
        gpu_label = normalize_gpu_name(gpu_model)

        if gpu_label not in gpu_base_prices or vcpus < gpu_base_prices[gpu_label][1]:
            gpu_base_prices[gpu_label] = (price_eur, vcpus)

    if not gpu_base_prices:
        # 回退到通用提取
        html = get("https://www.scaleway.com/en/pricing/")
        if html:
            results = extract_prices(html, COMMON_GPUS_EUR, currency="EUR")
            if results:
                mark_ok("Scaleway", len(results))
                return results
        return mark_failed("Scaleway", "未找到 GPU 产品价格数据")

    results = []
    seen = set()
    for gpu_label, (price_eur, _vcpus) in gpu_base_prices.items():
        price_usd = round(price_eur * eur_to_usd, 2)
        lo, hi = PRICE_RANGES.get(gpu_label, (0.01, 1000))
        if lo <= price_usd <= hi and gpu_label not in seen:
            seen.add(gpu_label)
            results.append({
                "gpu": gpu_label,
                "price_usd": price_usd,
                "plan": f"€{price_eur:.2f}/时 (最小配置)"
            })

    if results:
        mark_ok("Scaleway", len(results))
        return results
    mark_failed("Scaleway", "GPU 价格超出合理范围")
    return []


def scrape_cudo_compute():
    """Cudo Compute: 尝试定价页 + GPU 产品页，含 Playwright 交互回退."""
    print("🔍 Cudo Compute ...")
    # URL 列表 (pricing 页 + 直接 GPU 产品页)
    urls = [
        "https://www.cudocompute.com/pricing",
        "https://www.cudocompute.com/products/clusters",
        "https://www.cudocompute.com/products/gpu",
    ]
    # 第一步: 尝试 requests
    for url in urls:
        html = get(url)
        if not html:
            continue
        results = extract_prices(html, COMMON_GPUS)
        if not results:
            results = extract_prices(html, COMMON_GPUS_EUR, currency="EUR")
        if results:
            mark_ok("Cudo Compute", len(results))
            return results

    # 第二步: Playwright 回退 (尝试更全面的交互)
    if PLAYWRIGHT_AVAILABLE:
        print("  🌐 启动无头浏览器 (Cudo Compute) ...")
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                try:
                    page.goto("https://www.cudocompute.com/pricing",
                              timeout=45000, wait_until="networkidle")
                except Exception:
                    try:
                        page.goto("https://www.cudocompute.com/pricing",
                                  timeout=45000, wait_until="load")
                    except Exception:
                        pass
                page.wait_for_timeout(12000)
                # 接受 Cookie
                for btn_text in ['Accept', 'Accept All', 'OK', 'Got it', 'Decline']:
                    try:
                        btn = page.locator(f"button:has-text('{btn_text}')").first
                        if btn.is_visible(timeout=2000):
                            btn.click()
                            page.wait_for_timeout(2000)
                            break
                    except Exception:
                        continue
                # 点击所有可能的 GPU 选项卡
                page.evaluate("""() => {
                    document.querySelectorAll('[class*="tab"], [role="tab"], [class*="pricing"], .elementor-tab-title, .e-n-tab-title').forEach(e => { try { e.click(); } catch(ex) {} });
                }""")
                page.wait_for_timeout(10000)
                body_text = page.inner_text("body")
                browser.close()
                results = extract_prices_from_text(body_text)
                if not results:
                    results = extract_prices_from_text(body_text, currency="EUR")
        except Exception as e:
            print(f"  ⚠️ Playwright 异常: {e}")
            results = []

    if results:
        mark_ok("Cudo Compute", len(results))
        return results

    mark_failed("Cudo Compute", "Elementor 选项卡 AJAX 动态加载, 需手动交互或 API 授权")
    return []


def scrape_exoscale():
    """Exoscale: 通过公开 API https://portal.exoscale.com/api/pricing/ 提取 GPU 价格"""
    print("🔍 Exoscale ...")

    # GPU 型号映射: API key name → standard GPU label
    # ⚠️ 按 key 长度降序排列，避免短 key 错误匹配 (如 "gpu" 匹配到 "gpua5000")
    GPU_KEY_MAP = [
        ("gpurtx6000pro", "NVIDIA RTX 6000 Ada / A6000"),
        ("gpu3080ti",     "NVIDIA RTX 3080 / 3080 Ti"),
        ("gpua5000",      "NVIDIA RTX A5000"),
        ("gpua30",        "NVIDIA A30"),
        ("gpu3",          "NVIDIA T4"),
        ("gpu2",          "NVIDIA V100"),
        ("gpu",           "NVIDIA Tesla P100 / P40"),
    ]

    results = []
    seen = set()

    # 从 opencompute 端点获取 GPU 实例价格 (取 _small = 最小配置)
    endpoints = [
        ("https://portal.exoscale.com/api/pricing/opencompute", "_small"),
        ("https://portal.exoscale.com/api/pricing/ai", ""),  # AI 专用推理端点
    ]

    for api_url, size_suffix in endpoints:
        try:
            r = requests.get(api_url, timeout=TIMEOUT, headers={"User-Agent": UA})
            if r.status_code != 200:
                continue
            data = r.json()
        except Exception:
            continue

        # 优先用 USD，回退到 EUR
        prices = data.get("usd", data.get("eur", {}))
        for key, price_str in prices.items():
            # 只取 GPU 相关条目
            if not any(t in key.lower() for t in ['gpu', 'rtx', 'a5000', 'a30']):
                continue
            # 只取最小配置（_small 后缀或无后缀的 AI 专用）
            if size_suffix and not key.endswith(size_suffix):
                continue
            if key == "model":  # 跳过非 GPU 条目
                continue

            try:
                price_usd = float(price_str)
            except ValueError:
                continue

            # 根据 API key 找到标准 GPU 名称
            gpu_label = None
            for api_key, label in GPU_KEY_MAP:
                if api_key in key:
                    gpu_label = label
                    break
            if not gpu_label:
                continue

            lo, hi = PRICE_RANGES.get(gpu_label, (0.01, 1000))
            # Exoscale 含服务器硬件(vCPU+RAM), 放宽上限 50%
            hi = hi * 1.5
            if lo <= price_usd <= hi and gpu_label not in seen:
                seen.add(gpu_label)
                results.append({
                    "gpu": gpu_label,
                    "price_usd": round(price_usd, 2),
                    "plan": "最小配置 (API)"
                })

    if results:
        mark_ok("Exoscale", len(results))
        return results

    # 回退
    html = get("https://www.exoscale.com/pricing/")
    if html:
        results = extract_prices(html, COMMON_GPUS)
        if not results:
            results = extract_prices(html, COMMON_GPUS_EUR, currency="EUR")
        if results:
            mark_ok("Exoscale", len(results))
            return results

    mark_failed("Exoscale", "API 未提取到 GPU 价格")
    return []


# ============================================================
# 通用平台爬虫（requests 模式 or Playwright fallback）
# ============================================================

def scrape_tencent_cloud():
    """腾讯云: 通过 workbench API 获取 GPU 实例定价 (CNY/月 → USD/时)"""
    print("🔍 腾讯云 (Tencent Cloud) ...")
    if not PLAYWRIGHT_AVAILABLE:
        return mark_failed("腾讯云", "需要 Playwright 获取 API 数据")

    # GPU 实例族 → GPU 型号映射
    GPU_FAMILY_MAP = {
        "HCCG5v":   "NVIDIA H100 (80GB SXM)",   # H100
        "GT4":      "NVIDIA A100 (80GB SXM)",   # A100
        "GC50sg":   "NVIDIA L40S",              # L40S / L20
        "GI3X":     "NVIDIA L40S",              # L40S
        "GN10Xp":   "NVIDIA V100",              # V100
        "GN10X":    "NVIDIA V100",              # V100
        "GN7vi":    "NVIDIA T4",                # T4
        "GN7":      "NVIDIA T4",                # T4
        "PTX1":     "NVIDIA H200",              # H20/H800
        "BMG5t":    "NVIDIA Tesla P100 / P40",  # 旧 GPU
    }
    CNY_PER_USD = 7.25   # 人民币→美元汇率
    HOURS_PER_MONTH = 730

    results = []
    seen = set()

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            api_response = []

            def handle_response(response):
                if 'DescribeZoneInstanceConfigInfos' in response.url and response.ok:
                    try:
                        data = response.json()
                        instances = data.get('data', {}).get('Response', {}).get('InstanceTypeQuotaSet', [])
                        api_response.extend(instances)
                    except Exception:
                        pass

            page.on('response', handle_response)

            try:
                page.goto('https://buy.cloud.tencent.com/price/cvm/overview',
                          timeout=45000, wait_until='domcontentloaded')
            except Exception:
                pass
            page.wait_for_timeout(20000)  # 等待 API 响应 (腾讯云可能较慢)
            browser.close()

            if not api_response:
                return mark_failed("腾讯云", "未捕获到 API 响应")

            # 解析 GPU 实例, 取每族最小配置的价格
            family_min_price = {}  # {family: (min_price_cny_monthly, gpu_label, instance_type)}

            for inst in api_response:
                gpu_count = inst.get('Gpu', 0)
                if gpu_count <= 0:
                    continue
                itype = inst['InstanceType']
                # 提取实例族 (字母前缀)
                family_match = re.match(r'^([A-Z]+\d*[a-z]*)\.', itype)
                if not family_match:
                    continue
                family = family_match.group(1)
                gpu_label = GPU_FAMILY_MAP.get(family)
                if not gpu_label:
                    continue

                price_info = inst.get('Price', {})
                monthly_price = price_info.get('OriginalPrice', 0)
                if monthly_price <= 0:
                    continue

                # 取该族中单 GPU 价格最低的实例
                price_per_gpu = monthly_price / gpu_count
                if family not in family_min_price or price_per_gpu < family_min_price[family][0]:
                    family_min_price[family] = (price_per_gpu, gpu_label, itype)

            # 转换为 USD/小时
            for family, (price_cny_per_gpu_monthly, gpu_label, itype) in family_min_price.items():
                price_usd_hourly = round(price_cny_per_gpu_monthly / HOURS_PER_MONTH / CNY_PER_USD, 2)
                lo, hi = PRICE_RANGES.get(gpu_label, (0.01, 1000))
                if lo <= price_usd_hourly <= hi and gpu_label not in seen:
                    seen.add(gpu_label)
                    results.append({
                        "gpu": gpu_label,
                        "price_usd": price_usd_hourly,
                        "plan": f"月付¥{price_cny_per_gpu_monthly:.0f}/GPU ({itype})"
                    })

        if results:
            mark_ok("腾讯云", len(results))
            return results
        return mark_failed("腾讯云", "GPU 价格超出合理范围")

    except Exception as e:
        return mark_failed("腾讯云", f"Playwright 异常: {str(e)[:80]}")


def scrape_generic(name: str, url: str, use_pw: bool = False,
                   pw_fallback: bool = False, is_eur_platform: bool = False) -> list[dict]:
    """
    通用爬虫：默认用 requests，如果 use_pw=True 则用 Playwright。
    若 pw_fallback=True 且 requests 失败，自动回退到 Playwright。
    is_eur_platform: 额外尝试欧元价格模式
    """
    print(f"🔍 {name} ...")
    if use_pw:
        results = scrape_with_playwright(url, name, wait_sec=12, wait_until="networkidle")
        if results:
            mark_ok(name, len(results))
            return results
        if scrape_log.get(name, {}).get("status") != "failed":
            mark_failed(name, "Playwright 未提取到价格数据")
        return []

    # requests 模式
    html = get(url)
    if not html:
        # 有些 SPA 页面返回 404 但仍有内容 — 尝试宽容模式
        html = get(url, accept_any_status=True)
    if not html:
        if pw_fallback:
            # 回退到 Playwright
            print(f"  🔄 requests 失败，回退到 Playwright ...")
            results = scrape_with_playwright(url, name, wait_sec=12, wait_until="networkidle")
            if results:
                mark_ok(name, len(results))
                return results
        return mark_failed(name, "无法访问定价页面")

    # 尝试 USD 模式
    results = extract_prices(html, COMMON_GPUS)
    if not results and is_eur_platform:
        # 欧洲平台额外尝试 EUR 模式
        results = extract_prices(html, COMMON_GPUS_EUR, currency="EUR")
    if results:
        mark_ok(name, len(results))
        return results
    # 如果 requests 提取不到数据且允许回退，尝试 Playwright
    if pw_fallback:
        print(f"  🔄 requests 未提取到数据，回退到 Playwright ...")
        results = scrape_with_playwright(url, name, wait_sec=12, wait_until="networkidle")
        if results:
            mark_ok(name, len(results))
            return results
    mark_failed(name, "未能解析价格数据")
    return []


# ============================================================
# 平台 → 定价页面 URL 映射
# ============================================================
# 用于 "历史走势" 和 "查看价格" 链接，直接跳转到该平台的 GPU 价格文档
PRICING_URLS = {
    # --- 核心平台 ---
    "Vast.ai":          "https://vast.ai/pricing",
    "RunPod":           "https://www.runpod.io/pricing",
    "Lambda Labs":      "https://lambda.ai/pricing",
    "CoreWeave":        "https://www.coreweave.com/pricing",
    "TensorDock":       "https://www.tensordock.com/cloud-gpus.html",
    "Paperspace":       "https://www.paperspace.com/pricing",
    "JarvisLabs":       "https://jarvislabs.ai/pricing/",
    "DataCrunch":       "https://verda.com/pricing",
    "AutoDL":           "https://www.autodl.com/price",
    "Matpool":          "https://matpool.com/pricing",

    # --- 欧洲平台 ---
    "Hetzner":          "https://www.hetzner.com/cloud/gpu/",
    "OVHcloud":         "https://www.ovhcloud.com/en/public-cloud/prices/",
    "Scaleway":         "https://www.scaleway.com/en/pricing/",
    "Genesis Cloud":    "https://genesiscloud.com/pricing",
    "NexGen Cloud":     "https://www.hyperstack.cloud/gpu-pricing",
    "Cudo Compute":     "https://www.cudocompute.com/products/clusters",
    "G-Core Labs":      "https://gcore.com/cloud/gpu-cloud",
    "Cherry Servers":   "https://www.cherryservers.com/pricing/gpu-servers",
    "LeaderGPU":        "https://www.leadergpu.com/pricing",
    "Leaseweb":         "https://www.leaseweb.com/en/dedicated-servers/gpu",
    "Hostkey":          "https://hostkey.com/gpu-dedicated-servers/",
    "UpCloud":          "https://upcloud.com/pricing/",
    "Exoscale":         "https://www.exoscale.com/gpu/",
    "21Cloud":          "https://www.21cloud.com/cloud/gpu-cloud",
    "Servers.com":      "https://www.servers.com/gpu-servers/",
    "Mystic AI":        "https://mystic.ai/pricing",

    # --- 北美平台 ---
    "DigitalOcean":     "https://www.digitalocean.com/pricing/gpu-droplets",
    "Vultr":            "https://www.vultr.com/products/cloud-gpu/",
    "FluidStack":       "https://www.fluidstack.io/pricing",
    "Massed Compute":   "https://www.massedcompute.com/pricing",
    "Salad":            "https://salad.com/pricing",
    "Hivelocity":       "https://www.hivelocity.net/products/gpu-servers/",
    "SabrePC":          "https://www.sabrepc.com/hpc-cloud",
    "Bizon":            "https://bizon.ai/pricing",
    "DataPacket":       "https://www.datapacket.com/gpu-hosting",
    "ServerMania":      "https://www.servermania.com/gpu-servers.htm",
    "Monster API":      "https://monsterapi.ai/pricing",
    "Cerebrium":        "https://www.cerebrium.ai/pricing",

    # --- 大厂平台 ---
    "Google Cloud":     "https://cloud.google.com/compute/gpus-pricing",
    "IBM Cloud":        "https://www.ibm.com/cloud/gpu",
    "Oracle Cloud":     "https://www.oracle.com/cloud/compute/pricing/",

    # --- 中国平台 ---
    "腾讯云":            "https://buy.cloud.tencent.com/price/cvm/overview",
    "阿里云":            "https://www.aliyun.com/price/detail/ecs",
    "华为云":            "https://www.huaweicloud.com/pricing/calculator.html",
    "火山引擎":          "https://www.volcengine.com/product/gpu",
    "AutoDL":           "https://www.autodl.com/price",
}


# ============================================================
# 平台注册表
# ============================================================
# 格式: (平台名, URL, 是否需要 Playwright)
# 按优先级排序：越靠前越重要

CORE_PLATFORMS = [
    ("Vast.ai",      "https://vast.ai/pricing",                              True),
    ("RunPod",       "https://www.runpod.io/pricing",                        False),
    ("Lambda Labs",  "https://lambda.ai/pricing",                            True),
    ("CoreWeave",    "https://www.coreweave.com/pricing",                    False),
    ("TensorDock",   "https://www.tensordock.com/cloud-gpus.html",             False),
    ("Paperspace",   "https://www.paperspace.com/pricing",                   False),
    ("JarvisLabs",   "https://jarvislabs.ai/pricing/",                       False),
    ("DataCrunch",   "https://verda.com/pricing",                            True),
    # AutoDL 需要中国大陆 IP 才能访问，GitHub Actions 环境下自动跳过
    # ("AutoDL",     "https://www.autodl.com/price",                         True),
]

EXTENDED_PLATFORMS = [
    # --- 欧洲平台 ---
    ("Hetzner",         "https://www.hetzner.com/cloud/gpu/",                True),   # SPA, 需 Playwright
    ("OVHcloud",        "https://www.ovhcloud.com/en/public-cloud/prices/",  False),
    ("Scaleway",        "https://www.scaleway.com/en/gpu-instances/",        False),
    ("Genesis Cloud",   "https://genesiscloud.com/pricing",                  True),   # SPA, 需 Playwright
    ("NexGen Cloud",    "https://www.hyperstack.cloud/gpu-pricing",           False),
    ("Cudo Compute",    "https://www.cudocompute.com/products/clusters",     True),   # SPA, 需 Playwright
    ("G-Core Labs",     "https://gcore.com/cloud/gpu-cloud",                 True),   # SPA, 需 Playwright
    ("Cherry Servers",  "https://www.cherryservers.com/pricing/gpu-servers", True),   # SPA, 需 Playwright
    ("LeaderGPU",       "https://www.leadergpu.com/pricing",                 True),   # SPA, 需 Playwright
    ("Leaseweb",        "https://www.leaseweb.com/en/dedicated-servers/gpu", True),   # SPA, 需 Playwright
    ("Hostkey",         "https://hostkey.com/gpu-dedicated-servers/",        False),  # 已添加专用爬虫 (EUR)
    ("UpCloud",         "https://upcloud.com/pricing/",                      False),  # 已添加专用爬虫 (EUR)
    ("Exoscale",        "https://www.exoscale.com/gpu/",                     False),
    ("21Cloud",         "https://www.21cloud.com/cloud/gpu-cloud",           True),   # SPA, 需 Playwright
    ("Servers.com",     "https://www.servers.com/gpu-servers/",             True),   # SPA, 需 Playwright
    ("Mystic AI",       "https://www.mystic.ai/pricing",                      True),   # SPA, 需 Playwright

    # --- 北美平台 ---
    ("DigitalOcean",    "https://www.digitalocean.com/pricing/gpu-droplets", False),
    ("Vultr",           "https://www.vultr.com/products/cloud-gpu/",        True),   # SPA, 需 Playwright
    ("FluidStack",      "https://www.fluidstack.io/pricing",                 True),   # SPA, 需 Playwright
    ("Massed Compute",  "https://www.massedcompute.com/pricing",            False),
    ("Salad",           "https://salad.com/pricing",                         False),  # 已添加专用爬虫 (JS内嵌数据)
    ("Hivelocity",      "https://www.hivelocity.net/products/gpu-servers/", True),   # SPA, 需 Playwright
    ("SabrePC",         "https://www.sabrepc.com/hpc-cloud",                True),   # SPA, 需 Playwright
    ("Bizon",           "https://bizon.ai/pricing",                          True),   # SPA, 需 Playwright
    ("DataPacket",      "https://www.datapacket.com/gpu-hosting",           True),   # SPA, 需 Playwright
    ("ServerMania",     "https://www.servermania.com/gpu-servers.htm",      True),   # SPA, 需 Playwright
    ("Monster API",     "https://monsterapi.ai/pricing",                     True),   # SPA, 需 Playwright
    ("Cerebrium",       "https://www.cerebrium.ai/pricing",                  False),

    # --- 中国平台 (需要 Playwright 或 API 拦截) ---
    ("Matpool",         "https://matpool.com/pricing",                       True),
    ("腾讯云",          "https://buy.cloud.tencent.com/price/cvm/overview",  True),
    ("阿里云",          "https://www.alibabacloud.com/product/ecs/pricing",  True),   # 国际站, 海外IP可访问
    ("华为云",          "https://www.huaweicloud.com/pricing/calculator.html", True),
    ("火山引擎",        "https://www.volcengine.com/product/gpu",           True),
    # AutoDL 需要中国大陆 IP
    # ("AutoDL",        "https://www.autodl.com/price",                     True),

    # --- 大厂平台 (SPA 定价页面) ---
    ("Google Cloud",    "https://cloud.google.com/compute/gpus-pricing",    True),   # SPA, 需 Playwright
    ("IBM Cloud",       "https://www.ibm.com/cloud/gpu",                    True),   # SPA, 需 Playwright
    ("Oracle Cloud",    "https://www.oracle.com/cloud/compute/pricing/",    True),   # SPA, 需 Playwright
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
            "TensorDock":   (scrape_tensordock_dedicated, scrape_tensordock_dedicated),
            "DataCrunch":   (scrape_datacrunch, scrape_datacrunch_playwright),
            "Paperspace":   (scrape_paperspace, scrape_paperspace),
            "JarvisLabs":   (scrape_jarvislabs, scrape_jarvislabs),
            "AutoDL":       (None, scrape_autodl_playwright),  # 必须 Playwright
            "Matpool":      (None, scrape_matpool_playwright),  # 必须 Playwright
            # 新增专用爬虫 (v4.1)
            "Salad":        (scrape_salad, scrape_salad),       # JS 内嵌数据
            "Hostkey":      (scrape_hostkey, scrape_hostkey),   # JSON-LD 欧元月租
            "UpCloud":      (scrape_upcloud, scrape_upcloud),   # 欧元定价
            "Hetzner":      (scrape_hetzner, scrape_hetzner),   # 多URL/欧元
            "NexGen Cloud": (scrape_nexgen_cloud, scrape_nexgen_cloud),  # SPA+EUR
            "Cerebrium":    (scrape_cerebrium, scrape_cerebrium),        # 按秒计费
            "Scaleway":     (scrape_scaleway, scrape_scaleway),          # SPA+EUR
            "Cudo Compute": (scrape_cudo_compute, scrape_cudo_compute),  # SPA+EUR
            "Exoscale":     (scrape_exoscale, scrape_exoscale),          # SPA+EUR
            # 中国平台
            "腾讯云":       (None, scrape_tencent_cloud),             # Playwright API 拦截
        }

        # 欧元定价平台列表 (通用爬虫对这些平台额外尝试 EUR 模式)
        EUR_PLATFORMS = {"OVHcloud", "Scaleway", "Genesis Cloud", "NexGen Cloud",
                         "G-Core Labs", "Cherry Servers", "LeaderGPU", "Leaseweb",
                         "Exoscale", "Cudo Compute", "21Cloud", "Servers.com",
                         "Mystic AI", "Hetzner", "Hostkey", "UpCloud"}

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
                    # 通用爬虫 (欧洲平台额外尝试 EUR 模式)
                    is_eur = name in EUR_PLATFORMS
                    results = scrape_generic(name, url, use_pw=(use_pw and needs_pw),
                                             pw_fallback=use_pw, is_eur_platform=is_eur)

                if results:
                    all_data[name] = results
            except Exception as e:
                scrape_log[name] = {"status": "error", "gpu_count": 0, "error": str(e)}
                print(f"  ❌ 异常: {e}")

    # ============================================================
    # 抓取 GPU 租赁规模 (Vast.ai 公开 API: 总GPU / 已租 / 可租)
    # ============================================================
    try:
        import _availability
        _availability._vast_rental_scale.clear()
        _availability._vast_rental_scale.update(scrape_vast_rental_scale())
    except Exception as e:
        print(f"  ⚠️ 租赁规模抓取异常: {e}")

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
            pricing_url = PRICING_URLS.get(plat_name, "")
            avail_str = get_rental_scale_str(plat_name, label)
            gpu_categories[label].append({
                "platform": plat_name,
                "price_usd": entry["price_usd"],
                "plan": entry.get("plan", "按需"),
                "country": "",
                "region": "",
                "note": f"🟢 实时抓取 · {fetched_at}",
                "pricing_url": pricing_url,
                "availability": avail_str,
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
                        f'"note": "{e["note"]}", "pricing_url": "{e["pricing_url"]}", '
                        f'"availability": "{e.get("availability", "")}", "source": "{e["source"]}" }}{ec}\n')
            f.write(f"  ]{comma}\n")
        f.write("};\n")

    total = sum(len(v) for v in all_data.values())
    print(f"✅ {OUTPUT_LIVE.name}: {len(gpu_categories)} GPU 类别, {total} 条价格")

    # ============================================================
    # 保存/追加历史数据
    # ============================================================
    if "--save-history" in sys.argv:
        history_data = {"snapshots": []}
        if OUTPUT_HIST.exists():
            try:
                raw = OUTPUT_HIST.read_text(encoding="utf-8")
                m = re.search(r'PRICE_HISTORY_DATA\s*=\s*(\{.*\});', raw, re.DOTALL)
                if m:
                    history_data = json.loads(m.group(1))
            except Exception:
                pass

        # 兼容旧格式: {"date": ..., "prices": [{...}]} → {"ts": ..., "d": {...}}
        for snap in history_data.get("snapshots", []):
            if "date" in snap and "ts" not in snap:
                snap["ts"] = snap.pop("date") + "T00:00:00Z"
            if "prices" in snap and "d" not in snap:
                old_prices = snap.pop("prices")
                snap["d"] = {}
                for gpu_label, entries in old_prices.items():
                    if isinstance(entries, list):
                        snap["d"][gpu_label] = {e["platform"]: e["price_usd"] for e in entries}
                    else:
                        snap["d"][gpu_label] = entries  # already compact

        # 新快照 — 使用精确时间戳 + 压缩格式 (GPU → Platform → price_usd)
        snap = {"ts": fetched_at, "d": {}}
        for label, entries in gpu_categories.items():
            snap["d"][label] = {e["platform"]: e["price_usd"] for e in entries}

        # 始终追加，不覆盖
        history_data["snapshots"].append(snap)
        # 保留最近 1000 条（约 1 个月数据 @ 30次/天）
        if len(history_data["snapshots"]) > 1000:
            history_data["snapshots"] = history_data["snapshots"][-1000:]

        with open(OUTPUT_HIST, "w", encoding="utf-8") as f:
            f.write("var PRICE_HISTORY_DATA = ")
            json.dump(history_data, f, indent=2, ensure_ascii=False)
            f.write(";\n")

        with open(OUTPUT_HIST_JSON, "w", encoding="utf-8") as f:
            json.dump(history_data, f, indent=2, ensure_ascii=False)

        print(f"📝 历史数据已追加: {OUTPUT_HIST.name} (共 {len(history_data['snapshots'])} 个快照, "
              f"最新: {fetched_at})")

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
def scrape_coreweave():
    """CoreWeave: requests 优先, 失败回退 Playwright"""
    return scrape_generic("CoreWeave", "https://www.coreweave.com/pricing", use_pw=False, pw_fallback=True)
scrape_tensordock = lambda: scrape_generic("TensorDock", "https://www.tensordock.com/cloud-gpus.html", use_pw=False, pw_fallback=True)
# ⚠️ TensorDock 需要更精确的专用爬虫以避免抓取到资源总价而非GPU价格
# 见下方 scrape_tensordock_dedicated 函数
scrape_datacrunch = lambda: scrape_generic("DataCrunch", "https://datacrunch.io/pricing", use_pw=False, pw_fallback=True)
scrape_paperspace = lambda: scrape_generic("Paperspace", "https://www.paperspace.com/pricing", use_pw=False, pw_fallback=True)
scrape_jarvislabs = lambda: scrape_generic("JarvisLabs", "https://jarvislabs.ai/pricing/", use_pw=False, pw_fallback=True)


if __name__ == "__main__":
    sys.exit(main())
