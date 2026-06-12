#!/usr/bin/env python3
"""
运算盘 · GPU 实时价格爬虫 v3
===============================
自动抓取各平台官网公开定价页面，提取 GPU 型号和实时价格。

用法:
  python fetch_prices.py                # requests 模式（快速，适合静态页面）
  python fetch_prices.py --save-history  # + 追加历史快照
  python fetch_prices.py --playwright    # Playwright 模式（浏览器渲染，抓 Vast.ai 等）
  python fetch_prices.py --playwright --save-history  # 全功能

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
CODE_DIR   = Path(__file__).parent / "code"
OUTPUT_LIVE = CODE_DIR / "pricing_live.js"
OUTPUT_HIST = CODE_DIR / "price_history.js"
OUTPUT_HIST_JSON = CODE_DIR / "price_history.json"

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36")
TIMEOUT = 20

fetched_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
scrape_log = {}  # platform -> {status, gpu_count, error?}


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
    except Exception as e:
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
}


def extract_prices(html: str, gpu_map: list[tuple[str, str, str]]) -> list[dict]:
    """
    从 HTML 中提取 GPU 价格（带合理性校验）。
    gpu_map: [(gpu_regex, price_context_regex, display_label), ...]
    """
    results = []
    seen = set()
    for gpu_re, price_re, label in gpu_map:
        lo, hi = PRICE_RANGES.get(label, (0.01, 1000))
        for gpu_match in re.finditer(gpu_re, html, re.IGNORECASE):
            ctx_start = max(0, gpu_match.start() - 100)
            ctx_end = min(len(html), gpu_match.end() + 500)
            context = html[ctx_start:ctx_end]
            # 找所有价格匹配，选第一个在合理范围内的
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
# 各平台爬虫
# ============================================================

# --- 通用 GPU 名称映射（用于 regex 匹配）---
COMMON_GPUS = [
    # (页面中可能出现的 GPU 名称正则, 价格匹配正则, 统一标签)
    (r'H200\b',         r'\$(\d+\.?\d*)',  "NVIDIA H200"),
    (r'H100\b.*?80\s*GB', r'\$(\d+\.?\d*)', "NVIDIA H100 (80GB SXM)"),
    (r'H100\b(?!.*SXM)', r'\$(\d+\.?\d*)',  "NVIDIA H100 (80GB SXM)"),
    (r'A100\b.*?80\s*GB', r'\$(\d+\.?\d*)', "NVIDIA A100 (80GB SXM)"),
    (r'A100\b.*?40\s*GB', r'\$(\d+\.?\d*)', "NVIDIA A100 (40GB PCIe)"),
    (r'L40S\b',         r'\$(\d+\.?\d*)',  "NVIDIA L40S"),
    (r'A6000\b.*?Ada',  r'\$(\d+\.?\d*)',  "NVIDIA RTX 6000 Ada / A6000"),
    (r'RTX\s*A?6000\b(?!.*Ada)', r'\$(\d+\.?\d*)', "NVIDIA RTX 6000 Ada / A6000"),
    (r'RTX\s*4090\b',   r'\$(\d+\.?\d*)',  "NVIDIA RTX 4090"),
    (r'RTX\s*4080\b',   r'\$(\d+\.?\d*)',  "NVIDIA RTX 4080 / 4080 Super"),
    (r'RTX\s*4070\b',   r'\$(\d+\.?\d*)',  "NVIDIA RTX 4070 Ti / 4070"),
    (r'RTX\s*3090\b',   r'\$(\d+\.?\d*)',  "NVIDIA RTX 3090 / 3090 Ti"),
    (r'L4\b(?!\d)',     r'\$(\d+\.?\d*)',  "NVIDIA L4"),
    (r'A40\b(?!\d)',    r'\$(\d+\.?\d*)',  "NVIDIA A40"),
    (r'T4\b(?!\d)',     r'\$(\d+\.?\d*)',  "NVIDIA T4"),
    (r'V100\b',         r'\$(\d+\.?\d*)',  "NVIDIA V100"),
    (r'GH200\b',        r'\$(\d+\.?\d*)',  "NVIDIA GH200"),
]


def scrape_lambda():
    """Lambda Labs: https://lambdalabs.com/service/gpu-cloud/pricing"""
    print("🔍 Lambda Labs ...")
    html = get("https://lambdalabs.com/service/gpu-cloud/pricing")
    if not html:
        html = get("https://lambdalabs.com/gpu-cloud")
    if not html:
        return mark_failed("Lambda Labs", "无法访问定价页面")

    results = extract_prices(html, COMMON_GPUS)
    if results:
        mark_ok("Lambda Labs", len(results))
        return results
    mark_failed("Lambda Labs", "未能解析价格数据")
    return []


def scrape_runpod():
    """RunPod: https://www.runpod.io/pricing"""
    print("🔍 RunPod ...")
    html = get("https://www.runpod.io/pricing")
    if not html:
        return mark_failed("RunPod", "无法访问定价页面")

    # RunPod 页面结构: GPU 名后紧跟 $X.XX/hr
    results = extract_prices(html, COMMON_GPUS)
    # RunPod 有 Secure Cloud 和 Community Cloud 两套价格
    # 尝试区分
    secure_section = find_between(html, r'Secure\s*Cloud', r'Community\s*Cloud')
    community_section = find_between(html, r'Community\s*Cloud', r'(?:FAQ|footer|</main>)')

    if secure_section:
        secure_results = extract_prices(secure_section, COMMON_GPUS)
        for r in secure_results:
            r["gpu"] = r["gpu"]  # 保持原标签
            r["plan_note"] = "Secure Cloud"

    if community_section:
        comm_results = extract_prices(community_section, COMMON_GPUS)
        for r in comm_results:
            r["gpu"] = r["gpu"]
            r["plan_note"] = "Community Cloud"

    if results:
        mark_ok("RunPod", len(results))
        return results
    mark_failed("RunPod", "未能解析价格数据")
    return []


def scrape_vast():
    """
    Vast.ai: https://vast.ai/pricing
    JS 渲染的页面，但可能内嵌 JSON 数据。
    尝试多种提取策略。
    """
    print("🔍 Vast.ai ...")
    html = get("https://vast.ai/pricing")
    if not html:
        return mark_failed("Vast.ai", "无法访问定价页面")

    results = []

    # 策略 1: 提取内嵌的 JSON 数据 (__NEXT_DATA__ 或 window.__INITIAL_STATE__)
    json_patterns = [
        r'__NEXT_DATA__\s*=\s*(\{.*?\})\s*</script>',
        r'window\.__INITIAL_STATE__\s*=\s*(\{.*?\});',
        r'"gpu_name"\s*:\s*"([^"]+)".*?"min_bid"\s*:\s*([\d.]+)',
        r'"name"\s*:\s*"([^"]*(?:RTX|Tesla|A100|H100|L40|A40|V100|T4|P100|K80|M40|Radeon|RX)[^"]*)".*?"price"\s*:\s*([\d.]+)',
    ]

    for pattern in json_patterns:
        for m in re.finditer(pattern, html, re.IGNORECASE | re.DOTALL):
            # 尝试从 JSON 提取
            pass  # JSON 提取逻辑较复杂，用 regex 方式

    # 策略 2: 用 regex 直接从 HTML 找 GPU 名+价格对
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
                    # 规范化 GPU 名
                    gpu_label = normalize_gpu_name(gpu_raw)
                    results.append({"gpu": gpu_label, "price_usd": p, "plan": "市场起价"})
            except ValueError:
                continue

    # 策略 3: 如果上面都没找到，尝试更宽松的匹配
    if not results:
        results = extract_prices(html, COMMON_GPUS)

    if results:
        mark_ok("Vast.ai", len(results))
        return results
    mark_failed("Vast.ai", "未能解析价格数据（页面可能为 JS 动态渲染，需 Playwright）")
    return []


def normalize_gpu_name(raw: str) -> str:
    """将 vast.ai 等平台的原始 GPU 名规范化"""
    raw = raw.strip()
    mapping = {
        'h100': 'NVIDIA H100 (80GB SXM)',
        'h200': 'NVIDIA H200',
        'a100': 'NVIDIA A100 (80GB SXM)',
        'a6000': 'NVIDIA RTX 6000 Ada / A6000',
        'rtx 6000 ada': 'NVIDIA RTX 6000 Ada / A6000',
        'rtx 4090': 'NVIDIA RTX 4090',
        'rtx 4080': 'NVIDIA RTX 4080 / 4080 Super',
        'rtx 4070 ti': 'NVIDIA RTX 4070 Ti / 4070',
        'rtx 4070': 'NVIDIA RTX 4070 Ti / 4070',
        'rtx 4060 ti': 'NVIDIA RTX 4060 Ti',
        'rtx 3090 ti': 'NVIDIA RTX 3090 / 3090 Ti',
        'rtx 3090': 'NVIDIA RTX 3090 / 3090 Ti',
        'rtx 3080 ti': 'NVIDIA RTX 3080 / 3080 Ti',
        'rtx 3080': 'NVIDIA RTX 3080 / 3080 Ti',
        'rtx 3070 ti': 'NVIDIA RTX 3070 / 3070 Ti',
        'rtx 3070': 'NVIDIA RTX 3070 / 3070 Ti',
        'rtx 3060 ti': 'NVIDIA RTX 3060 / 3060 Ti',
        'rtx 3060': 'NVIDIA RTX 3060 / 3060 Ti',
        'rtx 2080 ti': 'NVIDIA RTX 2080 Ti',
        'l40s': 'NVIDIA L40S',
        'l40': 'NVIDIA L40S',
        'l4': 'NVIDIA L4',
        'a40': 'NVIDIA A40',
        't4': 'NVIDIA T4',
        'v100': 'NVIDIA V100',
        'p100': 'NVIDIA Tesla P100 / P40',
        'p40': 'NVIDIA Tesla P100 / P40',
        'k80': 'NVIDIA Tesla K80 / M40 / M60',
        'm40': 'NVIDIA Tesla K80 / M40 / M60',
        'rx 7900 xtx': 'AMD Radeon RX 7900 XTX / 7900 XT',
        'rx 7900 xt': 'AMD Radeon RX 7900 XTX / 7900 XT',
        'rx 7800 xt': 'AMD Radeon RX 7800 XT / 7700 XT',
        'rx 6900 xt': 'AMD Radeon RX 6900 XT / 6800 XT',
        'rx 6800 xt': 'AMD Radeon RX 6900 XT / 6800 XT',
        'rx 6800': 'AMD Radeon RX 6800 / 6700 XT',
        'rx 6700 xt': 'AMD Radeon RX 6800 / 6700 XT',
    }
    key = raw.lower().replace('nvidia', '').replace('geforce', '').replace('amd', '').strip()
    return mapping.get(key, raw)


def scrape_coreweave():
    """CoreWeave: https://www.coreweave.com/pricing"""
    print("🔍 CoreWeave ...")
    html = get("https://www.coreweave.com/pricing")
    if not html:
        return mark_failed("CoreWeave", "无法访问定价页面")
    results = extract_prices(html, COMMON_GPUS)
    if results:
        mark_ok("CoreWeave", len(results))
        return results
    mark_failed("CoreWeave", "未能解析价格数据")
    return []


def scrape_tensordock():
    """TensorDock: https://www.tensordock.com/"""
    print("🔍 TensorDock ...")
    html = get("https://www.tensordock.com/")
    if not html:
        html = get("https://tensordock.com/")
    if not html:
        return mark_failed("TensorDock", "无法访问定价页面")
    results = extract_prices(html, COMMON_GPUS)
    if results:
        mark_ok("TensorDock", len(results))
        return results
    mark_failed("TensorDock", "未能解析价格数据")
    return []


def scrape_datacrunch():
    """DataCrunch: https://datacrunch.io/pricing"""
    print("🔍 DataCrunch ...")
    html = get("https://datacrunch.io/pricing")
    if not html:
        html = get("https://datacrunch.io/")
    if not html:
        return mark_failed("DataCrunch", "无法访问定价页面")
    results = extract_prices(html, COMMON_GPUS)
    if results:
        mark_ok("DataCrunch", len(results))
        return results
    mark_failed("DataCrunch", "未能解析价格数据")
    return []


def scrape_paperspace():
    """Paperspace: https://www.paperspace.com/pricing"""
    print("🔍 Paperspace ...")
    html = get("https://www.paperspace.com/pricing")
    if not html:
        return mark_failed("Paperspace", "无法访问定价页面")
    results = extract_prices(html, COMMON_GPUS)
    if results:
        mark_ok("Paperspace", len(results))
        return results
    mark_failed("Paperspace", "未能解析价格数据")
    return []


def scrape_jarvislabs():
    """JarvisLabs: https://jarvislabs.ai/pricing/"""
    print("🔍 JarvisLabs ...")
    html = get("https://jarvislabs.ai/pricing/")
    if not html:
        return mark_failed("JarvisLabs", "无法访问定价页面")
    results = extract_prices(html, COMMON_GPUS)
    if results:
        mark_ok("JarvisLabs", len(results))
        return results
    mark_failed("JarvisLabs", "未能解析价格数据")
    return []


# ============================================================
# Playwright 浏览器自动化抓取（解决 JS 渲染页面）
# ============================================================

def extract_prices_from_text(text: str) -> list[dict]:
    """从纯文本中提取 GPU 价格（Playwright 渲染后的文本）"""
    # 去除多余空白，按行分割
    lines = text.split('\n')
    full_text = ' '.join(lines)

    # 更精确的 GPU+价格匹配模式
    # 常见格式: "GPU Name ... $X.XX/hr" 或 "GPU Name $X.XX"
    patterns = [
        # RTX 4090 等消费卡: $0.XX/hr
        (r'(RTX\s*\d{4}(?:\s*Ti)?(?:Super)?)\b.*?\$(\d+\.?\d{0,2})\s*/\s*(?:hr|hour|h)', False),
        # H100/A100 数据中心卡: $X.XX/hr
        (r'\b(H100|H200|A100|A6000|L40S?|A40|GH200|V100|T4|P100|P40)\b.*?\$(\d+\.?\d{0,2})\s*/\s*(?:hr|hour|h)', False),
        # 通用: $X.XX/hr 附近找 GPU 名
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

            # 合理性校验
            lo, hi = PRICE_RANGES.get(gpu_label, (0.01, 1000))
            if not (lo <= price <= hi):
                continue
            if gpu_label in seen:
                continue
            seen.add(gpu_label)
            results.append({"gpu": gpu_label, "price_usd": price, "plan": "市场价"})

    return results


def scrape_with_playwright(url: str, platform_name: str, wait_sec: int = 5) -> list[dict]:
    """
    用 Playwright 无头浏览器访问页面，等待 JS 渲染后提取文本。
    """
    if not PLAYWRIGHT_AVAILABLE:
        scrape_log[platform_name] = {"status": "failed", "gpu_count": 0,
                                      "error": "Playwright 未安装。运行: pip install playwright && playwright install chromium"}
        print(f"  ❌ Playwright 未安装")
        return []

    print(f"  🌐 启动无头浏览器 ...")
    results = []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            try:
                page.goto(url, timeout=30000, wait_until="load")
            except Exception:
                pass  # 即使超时也继续，页面可能已部分加载
            page.wait_for_timeout(wait_sec * 1000)  # 额外等待 JS 渲染

            # 获取页面文本
            body_text = page.inner_text("body")
            # 也可尝试获取特定元素
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


def scrape_vast_playwright() -> list[dict]:
    """Vast.ai: 用 Playwright 抓取 https://vast.ai/pricing"""
    print("🔍 Vast.ai (Playwright) ...")
    results = scrape_with_playwright("https://vast.ai/pricing", "Vast.ai", wait_sec=8)
    if results:
        mark_ok("Vast.ai", len(results))
        return results
    if scrape_log.get("Vast.ai", {}).get("status") != "failed":
        mark_failed("Vast.ai", "未提取到价格数据")
    return []


def scrape_lambda_playwright() -> list[dict]:
    """Lambda Labs: 用 Playwright 抓取"""
    print("🔍 Lambda Labs (Playwright) ...")
    results = scrape_with_playwright("https://lambdalabs.com/service/gpu-cloud/pricing",
                                      "Lambda Labs", wait_sec=5)
    if not results:
        # 尝试备用 URL
        results = scrape_with_playwright("https://lambdalabs.com/gpu-cloud",
                                          "Lambda Labs", wait_sec=5)
    if results:
        mark_ok("Lambda Labs", len(results))
        return results
    if scrape_log.get("Lambda Labs", {}).get("status") != "failed":
        mark_failed("Lambda Labs", "未提取到价格数据")
    return []


def scrape_datacrunch_playwright() -> list[dict]:
    """DataCrunch: 用 Playwright 抓取"""
    print("🔍 DataCrunch (Playwright) ...")
    results = scrape_with_playwright("https://datacrunch.io/pricing", "DataCrunch", wait_sec=5)
    if results:
        mark_ok("DataCrunch", len(results))
        return results
    if scrape_log.get("DataCrunch", {}).get("status") != "failed":
        mark_failed("DataCrunch", "未提取到价格数据")
    return []


# ============================================================
# 主流程
# ============================================================
def main():
    print("=" * 60)
    print("🚀 运算盘 · GPU 实时价格爬虫 v2")
    print(f"⏰ 开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print()

    use_pw = "--playwright" in sys.argv

    if use_pw and not PLAYWRIGHT_AVAILABLE:
        print("⚠️ Playwright 未安装！请先运行:")
        print("   pip install playwright")
        print("   playwright install chromium")
        print()
        print("将使用 requests 模式继续...\n")
        use_pw = False

    if use_pw:
        print("🌐 Playwright 浏览器模式已启用\n")

    scrapers = [
        # (名称,      requests 模式,              Playwright 模式)
        ("Lambda Labs", scrape_lambda if not use_pw else scrape_lambda_playwright,
                        scrape_lambda_playwright if use_pw else scrape_lambda),
        ("RunPod",      scrape_runpod,             scrape_runpod),  # requests 已够
        ("Vast.ai",     scrape_vast if not use_pw else scrape_vast_playwright,
                        scrape_vast_playwright if use_pw else scrape_vast),
        ("CoreWeave",   scrape_coreweave,          scrape_coreweave),
        ("TensorDock",  scrape_tensordock,         scrape_tensordock),
        ("DataCrunch",  scrape_datacrunch if not use_pw else scrape_datacrunch_playwright,
                        scrape_datacrunch_playwright if use_pw else scrape_datacrunch),
        ("Paperspace",  scrape_paperspace,         scrape_paperspace),
        ("JarvisLabs",  scrape_jarvislabs,         scrape_jarvislabs),
    ]

    # 解析为 (name, function) 列表
    scrapers = [(s[0], s[1]) for s in scrapers]

    all_data = {}  # platform -> [gpu entries]

    for name, scraper in scrapers:
        try:
            results = scraper()
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

    # 按 GPU 型号重新组织
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
                # 尝试从 JS 变量文件读取
                raw = OUTPUT_HIST.read_text(encoding="utf-8")
                m = re.search(r'PRICE_HISTORY_DATA\s*=\s*(\{.*\});', raw, re.DOTALL)
                if m:
                    history_data = json.loads(m.group(1))
            except Exception:
                pass

        # 构建今日快照
        snap = {"date": today_str, "prices": {}}
        for label, entries in gpu_categories.items():
            snap["prices"][label] = [
                {"platform": e["platform"], "price_usd": e["price_usd"]}
                for e in entries
            ]

        # 替换或追加
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

        # 写入 JS 变量文件
        with open(OUTPUT_HIST, "w", encoding="utf-8") as f:
            f.write("var PRICE_HISTORY_DATA = ")
            json.dump(history_data, f, indent=2, ensure_ascii=False)
            f.write(";\n")

        # 也写 JSON 备份
        with open(OUTPUT_HIST_JSON, "w", encoding="utf-8") as f:
            json.dump(history_data, f, indent=2, ensure_ascii=False)

        action = "更新" if replaced else "追加"
        print(f"📝 历史数据已{action}: {OUTPUT_HIST.name} (共 {len(history_data['snapshots'])} 天)")

    # ============================================================
    # 总结
    # ============================================================
    print("\n📋 抓取结果:")
    for name, info in scrape_log.items():
        if info["status"] == "ok":
            print(f"  ✅ {name}: {info['gpu_count']} 款 GPU")
        else:
            print(f"  ❌ {name}: {info.get('error', 'Unknown')}")

    if total == 0:
        print("\n⚠️ 警告: 未抓取到任何价格数据！")
        print("   可能原因: 1) 网络问题 2) 平台页面结构变更 3) 需要浏览器渲染")
        print("   建议: 使用参考数据 pricing.js 作为 fallback")
    else:
        print(f"\n✅ 共抓取 {total} 条实时价格，刷新页面即可查看 🟢 实时标记的数据")

    return 0


if __name__ == "__main__":
    sys.exit(main())
