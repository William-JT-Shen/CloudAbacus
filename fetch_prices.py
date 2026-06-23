#!/usr/bin/env python3
"""
运算盘 · GPU 实时价格爬虫 v4
===============================
自动抓取各平台官网公开定价页面，提取 GPU 型号和实时价格。
覆盖 40+ 全球 GPU 云平台。

用法:
  python fetch_prices.py                      # requests 模式（快速，适合静态页面）
  python fetch_prices.py --playwright          # Playwright 模式（浏览器渲染）
  python fetch_prices.py --vast-only           # 仅抓取 Vast.ai（适合高频运行）
  python fetch_prices.py --quick               # 仅抓取高优先级平台（快速模式）
注: 历史数据始终自动追加到 price_history.js / pricing_history.js

依赖:
  pip install requests beautifulsoup4
  pip install playwright && playwright install chromium  # 仅 --playwright 需要
"""

import requests
import json
import re
import sys
import io
from datetime import datetime, timezone, timedelta
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
try:
    from _extra_platforms import (
        EXTRA_PLATFORMS, EXTRA_PRICING_URLS, EXTRA_CUSTOM_SCRAPERS
    )
    EXTRA_AVAILABLE = True
except ImportError:
    EXTRA_AVAILABLE = False

CODE_DIR   = Path(__file__).parent
OUTPUT_LIVE = CODE_DIR / "pricing_live.js"
OUTPUT_HIST = CODE_DIR / "price_history.js"
OUTPUT_HIST_JSON = CODE_DIR / "price_history.json"
OUTPUT_HIST_FULL = CODE_DIR / "pricing_history.js"  # 完整历史快照（追加模式）

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36")
TIMEOUT = 20

BEIJING_TZ = timezone(timedelta(hours=8))
fetched_at = datetime.now(BEIJING_TZ).strftime("%Y-%m-%d %H:00")  # 北京时间
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


def atomic_write_js(path: Path, var_name: str, data: dict | list):
    """原子写入 JS/JSON 文件：先写临时文件，再 rename（避免并发写入损坏）
    若 var_name 为空字符串，则写入纯 JSON"""
    tmp_path = path.with_suffix(".tmp")
    with open(tmp_path, "w", encoding="utf-8") as f:
        if var_name:
            f.write(f"var {var_name} = ")
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write(";\n" if var_name else "\n")
    tmp_path.replace(path)  # Python 3.12: Path.replace() 在 POSIX 上是原子的


def read_existing_js(path: Path, var_name: str) -> dict | list | None:
    """读取 JS 文件中的 JSON 变量"""
    if not path.exists():
        return None
    try:
        raw = path.read_text(encoding="utf-8")
        m = re.search(rf'{var_name}\s*=\s*(\{{.*?\}});', raw, re.DOTALL)
        if not m:
            m = re.search(rf'{var_name}\s*=\s*(\[.*?\]);', raw, re.DOTALL)
        if m:
            return json.loads(m.group(1))
    except Exception:
        pass
    return None


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
    # 新增: 中国特供卡 / 次代 GPU / AMD / 专业卡 / TPU
    "NVIDIA B200":                     (3.00, 12.00),
    "NVIDIA B300":                     (3.50, 14.00),
    "NVIDIA H800":                     (1.50, 8.00),
    "NVIDIA A800":                     (0.50, 5.00),
    "NVIDIA H20":                      (0.80, 4.00),
    "NVIDIA L20":                      (0.30, 2.00),
    "NVIDIA A16":                      (0.20, 1.50),
    "NVIDIA A10G":                     (0.25, 2.50),
    "NVIDIA H100 (NVL)":               (1.20, 8.00),
    "NVIDIA Quadro RTX 4000":          (0.10, 0.80),
    "NVIDIA Quadro RTX 5000":          (0.15, 1.00),
    "NVIDIA GTX 1080 Ti":              (0.04, 0.40),
    "AMD Radeon Instinct MI300X":      (2.00, 8.00),
    "AMD Radeon Instinct MI250X":      (1.00, 6.00),
    "AMD Radeon Instinct MI250":       (0.80, 5.00),
    "AMD Radeon Instinct MI210":       (0.40, 3.00),
    "AMD Radeon Instinct MI100":       (0.30, 2.50),
    "Google TPU v5":                   (1.00, 6.00),
    "Google TPU v2":                   (0.10, 1.00),
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


# ============================================================
# 多策略提取（v5 — 除正则外尝试 HTML 表格 / JSON-LD / Next.js 数据）
# ============================================================
def extract_from_html_table(html: str, gpu_map: list[tuple[str, str, str]],
                            currency: str = "USD") -> list[dict]:
    """从 HTML <table> 行中提取 GPU 价格：<tr><th>GPU名</th><td>$X.XX</td></tr>"""
    results = []
    seen = set()
    eur_to_usd = 1.08
    # 找所有带 <th> 的表格行（GPU 名在 th，价格在 td）
    for row in re.finditer(r'<tr[^>]*>(.*?)</tr>', html, re.DOTALL | re.IGNORECASE):
        cells = row.group(1)
        # 提取 th 文本作为 GPU 候选名，td 文本作为价格候选
        th_match = re.search(r'<th[^>]*>(.*?)</th>', cells, re.DOTALL | re.IGNORECASE)
        if not th_match:
            continue
        gpu_text = re.sub(r'<[^>]+>', '', th_match.group(1)).strip()
        # 匹配价格: $X.XX 或 €X.XX 在任意 td 中
        for td_m in re.finditer(r'<td[^>]*>(.*?)</td>', cells, re.DOTALL | re.IGNORECASE):
            td_text = re.sub(r'<[^>]+>', '', td_m.group(1)).strip()
            price_m = re.search(r'[\$€](\d+\.?\d*)\s*(?:/hr|/hour|/h)?', td_text)
            if not price_m:
                continue
            try:
                price = float(price_m.group(1))
            except ValueError:
                continue
            is_eur = '€' in price_m.group(0)
            # 匹配 GPU 名称
            for gpu_re, _, label in gpu_map:
                lo, hi = PRICE_RANGES.get(label, (0.01, 1000))
                if is_eur:
                    lo, hi = lo / eur_to_usd, hi / eur_to_usd
                if re.search(gpu_re, gpu_text, re.IGNORECASE) and lo <= price <= hi and label not in seen:
                    seen.add(label)
                    price_usd = round(price * eur_to_usd, 2) if is_eur else price
                    results.append({"gpu": label, "price_usd": price_usd})
                    break
    return results


def extract_from_json_ld(html: str, gpu_map: list[tuple[str, str, str]]) -> list[dict]:
    """从 <script type='application/ld+json'> 结构化数据中提取价格"""
    results = []
    seen = set()
    for script_m in re.finditer(r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
                                 html, re.DOTALL | re.IGNORECASE):
        try:
            data = json.loads(script_m.group(1))
        except json.JSONDecodeError:
            continue
        # 递归搜索所有包含 "price" / "offers" 的嵌套对象
        def _search(obj, path=""):
            if isinstance(obj, dict):
                for key in obj:
                    if key.lower() in ("price", "offers", "pricecurrency", "unitprice"):
                        _search(obj[key], f"{path}.{key}")
                # 如果同时有 name 和 price 字段
                name = obj.get("name", "")
                price_val = obj.get("price") or obj.get("unitPrice")
                if name and price_val is not None:
                    try:
                        price = float(str(price_val).replace(",", ""))
                    except (ValueError, TypeError):
                        return
                    for gpu_re, _, label in gpu_map:
                        lo, hi = PRICE_RANGES.get(label, (0.01, 1000))
                        if re.search(gpu_re, str(name), re.IGNORECASE) and lo <= price <= hi and label not in seen:
                            seen.add(label)
                            results.append({"gpu": label, "price_usd": price})
                            break
            elif isinstance(obj, list):
                for item in obj:
                    _search(item, path)
        _search(data)
    return results


def extract_from_next_data(html: str, gpu_map: list[tuple[str, str, str]]) -> list[dict]:
    """从 Next.js __NEXT_DATA__ 或 Nuxt __NUXT__ JSON 中提取价格"""
    results = []
    seen = set()
    patterns = [
        r'<script[^>]*id=["\']__NEXT_DATA__["\'][^>]*>(.*?)</script>',
        r'<script[^>]*>window\.__NUXT__\s*=\s*(\{.*?\})\s*;?\s*</script>',
    ]
    for pat in patterns:
        for m in re.finditer(pat, html, re.DOTALL):
            try:
                data = json.loads(m.group(1))
            except json.JSONDecodeError:
                continue
            # 递归深度搜索任何包含 "price" 和 GPU 名称的文本
            def _search_deep(obj, depth=0):
                if depth > 8:
                    return
                if isinstance(obj, dict):
                    # 检查值中是否有 GPU 名称和价格
                    vals = {str(v) for v in obj.values() if isinstance(v, (int, float, str))}
                    price_vals = []
                    for k, v in obj.items():
                        if "price" in k.lower() and isinstance(v, (int, float)):
                            price_vals.append(float(v))
                    if price_vals:
                        all_text = json.dumps(obj).lower()
                        for gpu_re, _, label in gpu_map:
                            if label in seen:
                                continue
                            lo, hi = PRICE_RANGES.get(label, (0.01, 1000))
                            if re.search(gpu_re, all_text, re.IGNORECASE):
                                for pv in price_vals:
                                    if lo <= pv <= hi:
                                        seen.add(label)
                                        results.append({"gpu": label, "price_usd": round(pv, 2)})
                                        break
                    for v in obj.values():
                        _search_deep(v, depth + 1)
                elif isinstance(obj, list):
                    for item in obj:
                        _search_deep(item, depth + 1)
            _search_deep(data)
    return results


def extract_prices_multistrategy(html: str, gpu_map: list[tuple[str, str, str]],
                                  currency: str = "USD") -> list[dict]:
    """多策略 GPU 价格提取：正则 → HTML表格 → JSON-LD → Next.js数据"""
    # 策略 1: 标准正则提取（原有方法）
    results = extract_prices(html, gpu_map, currency)
    if results:
        return results
    # 策略 2: HTML 表格行提取
    results = extract_from_html_table(html, gpu_map, currency)
    if results:
        return results
    # 策略 3: JSON-LD 结构化数据
    results = extract_from_json_ld(html, gpu_map)
    if results:
        return results
    # 策略 4: Next.js / Nuxt 数据
    results = extract_from_next_data(html, gpu_map)
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
    # 新增: 次代 GPU / 中国特供 / AMD Instinct / 专业卡 / TPU (v6)
    (r'B300\b',                   r'\$(\d+\.?\d*)', "NVIDIA B300"),
    (r'B200\b(?!.*NVL)',          r'\$(\d+\.?\d*)', "NVIDIA B200"),
    (r'H800\b',                   r'\$(\d+\.?\d*)', "NVIDIA H800"),
    (r'A800\b(?!\d)',             r'\$(\d+\.?\d*)', "NVIDIA A800"),
    (r'H20\b',                    r'\$(\d+\.?\d*)', "NVIDIA H20"),
    (r'L20\b(?!\d)',              r'\$(\d+\.?\d*)', "NVIDIA L20"),
    (r'A16\b(?!\d)',              r'\$(\d+\.?\d*)', "NVIDIA A16"),
    (r'A10G\b',                   r'\$(\d+\.?\d*)', "NVIDIA A10G"),
    (r'H100\s*NVL',               r'\$(\d+\.?\d*)', "NVIDIA H100 (NVL)"),
    (r'Quadro\s*RTX\s*4000',      r'\$(\d+\.?\d*)', "NVIDIA Quadro RTX 4000"),
    (r'Quadro\s*RTX\s*5000',      r'\$(\d+\.?\d*)', "NVIDIA Quadro RTX 5000"),
    (r'GTX\s*1080\s*Ti',          r'\$(\d+\.?\d*)', "NVIDIA GTX 1080 Ti"),
    (r'MI300X\b',                 r'\$(\d+\.?\d*)', "AMD Radeon Instinct MI300X"),
    (r'MI250X\b',                 r'\$(\d+\.?\d*)', "AMD Radeon Instinct MI250X"),
    (r'MI250\b(?!X)',             r'\$(\d+\.?\d*)', "AMD Radeon Instinct MI250"),
    (r'MI210\b',                  r'\$(\d+\.?\d*)', "AMD Radeon Instinct MI210"),
    (r'MI100\b',                  r'\$(\d+\.?\d*)', "AMD Radeon Instinct MI100"),
    (r'AMD\s*Instinct\s*MI300X',  r'\$(\d+\.?\d*)', "AMD Radeon Instinct MI300X"),
    (r'TPU\s*v5',                 r'\$(\d+\.?\d*)', "Google TPU v5"),
    (r'TPU\s*v2',                 r'\$(\d+\.?\d*)', "Google TPU v2"),
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
    # 新增 EUR 支持 (v6)
    (r'B300\b',                   r'€\s*(\d+\.?\d*)\s*/\s*(?:h|hr|hour)', "NVIDIA B300"),
    (r'B200\b(?!.*NVL)',          r'€\s*(\d+\.?\d*)\s*/\s*(?:h|hr|hour)', "NVIDIA B200"),
    (r'A10G\b',                   r'€\s*(\d+\.?\d*)\s*/\s*(?:h|hr|hour)', "NVIDIA A10G"),
    (r'A16\b(?!\d)',              r'€\s*(\d+\.?\d*)\s*/\s*(?:h|hr|hour)', "NVIDIA A16"),
    (r'MI300X\b',                 r'€\s*(\d+\.?\d*)\s*/\s*(?:h|hr|hour)', "AMD Radeon Instinct MI300X"),
    (r'MI250X\b',                 r'€\s*(\d+\.?\d*)\s*/\s*(?:h|hr|hour)', "AMD Radeon Instinct MI250X"),
    (r'Quadro\s*RTX\s*4000',      r'€\s*(\d+\.?\d*)\s*/\s*(?:h|hr|hour)', "NVIDIA Quadro RTX 4000"),
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
        # 新增映射 (v6)
        'b300': 'NVIDIA B300', 'b200': 'NVIDIA B200',
        'h800': 'NVIDIA H800', 'a800': 'NVIDIA A800',
        'h20': 'NVIDIA H20', 'l20': 'NVIDIA L20',
        'a16': 'NVIDIA A16', 'a10g': 'NVIDIA A10G',
        'h100 nvl': 'NVIDIA H100 (NVL)',
        'quadro rtx 4000': 'NVIDIA Quadro RTX 4000',
        'quadro rtx 5000': 'NVIDIA Quadro RTX 5000',
        'gtx 1080 ti': 'NVIDIA GTX 1080 Ti',
        'mi300x': 'AMD Radeon Instinct MI300X', 'mi250x': 'AMD Radeon Instinct MI250X',
        'mi250': 'AMD Radeon Instinct MI250', 'mi210': 'AMD Radeon Instinct MI210',
        'mi100': 'AMD Radeon Instinct MI100',
        'amd instinct mi300x': 'AMD Radeon Instinct MI300X',
        # v6: Vast.ai 特有命名
        'rtx 4070s ti': 'NVIDIA RTX 4070 Ti / 4070',
        'rtx 4080s': 'NVIDIA RTX 4080 / 4080 Super',
        'rtx pro 6000 ws': 'NVIDIA RTX 6000 Ada / A6000',
        'rtx pro 6000 s': 'NVIDIA RTX 6000 Ada / A6000',
        'rtx pro 5000': 'RTX 5000',
        'rtx pro 4500': 'RTX 4500',
        'h200 nvl': 'NVIDIA H200',
        'h100 sxm': 'NVIDIA H100 (80GB SXM)',
        'h100 pcie': 'NVIDIA H100 (80GB SXM)',
        'h100 nvl': 'NVIDIA H100 (NVL)',
        'a100 sxm': 'NVIDIA A100 (80GB SXM)',
        'a100 pcie': 'NVIDIA A100 (40GB PCIe)',
        'tesla v100': 'NVIDIA V100',
        'tesla p100': 'NVIDIA Tesla P100 / P40',
        'tesla t4': 'NVIDIA T4',
        'tesla k80': 'NVIDIA Tesla K80 / M40 / M60',
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
    """Vast.ai: 直接使用公开 API 获取价格 (v6)"""
    print("🔍 Vast.ai (API) ...")
    return scrape_vast_playwright()  # 统一走 API 路径

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
    currency: "USD" 用 $ 匹配, "EUR" 用 € 匹配, "CNY" 用 ¥/元 匹配月付价格"""
    full_text = ' '.join(text.split('\n'))
    eur_to_usd = 1.08
    cny_to_usd = 0.14  # CNY → USD (约 7.25:1)
    HOURS_PER_MONTH = 730

    if currency == 'CNY':
        # 人民币: ¥X,XXX.XX/月 或 X,XXX.XX元/月 → 转换为 USD/小时
        # v6: 扩展 GPU 名覆盖 + 更多中文价格格式
        _cn_gpus = r'H100|H200|H800|A100|A800|A10G|A16|A40|GH200|B200|B300|H20|L20|L40S?|L4\b|T4\b|V100|P100|P40|K80|M40|A6000|MI300X|RTX\s*\d{{4}}(?:\s*Ti)?(?:Super)?'
        cny_patterns = [
            # ¥X.XX/月 or ¥X.XX/小时 after GPU name
            (rf'({_cn_gpus})\b.*?[¥￥]\s*([\d,]+\.?\d*)\s*/\s*(?:月|month|mo)', False),
            # X.XX元/月 after GPU name
            (rf'({_cn_gpus})\b.*?([\d,]+\.?\d*)\s*元\s*/\s*(?:月|month|mo)', False),
            # ¥X.XX/小时 or X.XX元/时
            (rf'({_cn_gpus})\b.*?[¥￥]\s*([\d,]+\.?\d*)\s*/\s*(?:小时|时|h)', False),
            (rf'({_cn_gpus})\b.*?([\d,]+\.?\d*)\s*元\s*/\s*(?:小时|时|h)', False),
            # 按量付费: ¥X.XX/小时
            (rf'按量付费.*?({_cn_gpus})\b.*?[¥￥]\s*([\d,]+\.?\d*)', True),
            # 包年包月: ¥X,XXX/月
            (rf'({_cn_gpus})\b.*?[¥￥]\s*([\d,]+\.?\d*)\s*/?\s*(?:每月|月付)', False),
            # ￥X.XX/GPU/小时
            (rf'[¥￥]\s*([\d,]+\.?\d*)\s*/\s*GPU\s*/\s*(?:小时|时).*?({_cn_gpus})\b', True),
        ]
        results = []
        seen = set()
        for pattern, swap_groups in cny_patterns:
            is_monthly = '(?:月|month|mo)' in pattern
            for m in re.finditer(pattern, full_text, re.IGNORECASE):
                gpu_raw = (m.group(2) if swap_groups else m.group(1)).strip()
                price_str = (m.group(1) if swap_groups else m.group(2)).strip().replace(',', '')
                try:
                    price_cny = float(price_str)
                except ValueError:
                    continue
                # 月付 → 时付
                if is_monthly:
                    price_usd = price_cny / HOURS_PER_MONTH * cny_to_usd
                else:
                    price_usd = price_cny * cny_to_usd
                gpu_label = normalize_gpu_name(gpu_raw)
                lo, hi = PRICE_RANGES.get(gpu_label, (0.01, 1000))
                if not (lo <= price_usd <= hi):
                    continue
                if gpu_label in seen:
                    continue
                seen.add(gpu_label)
                price_usd = round(price_usd, 2)
                plan = f"月付¥{price_cny:,.0f}" if is_monthly else f"时付¥{price_cny:,.2f}"
                results.append({"gpu": gpu_label, "price_usd": price_usd, "plan": plan})
        return results

    # USD / EUR 模式 (v6: 扩展 GPU 型号覆盖)
    currency_char = '[$]' if currency == 'USD' else '[€]'
    # 构建 GPU 名列表 (NVIDIA + AMD)
    _gpu_names = r'H100|H200|H800|A100|A800|A6000|A10G|A16|A40|GH200|B200|B300|H20|L20|L40S?|L4\b|T4\b|V100|P100|P40|K80|M40|MI300X|MI250X|MI210|MI100|A5000|A4000|RTX\s*\d{{4}}(?:\s*Ti)?(?:Super)?'
    patterns = [
        # $X.XX/hr or €X.XX/hr after GPU name
        (rf'({_gpu_names})\b.*?{currency_char}(\d+\.?\d{{0,2}})\s*/\s*(?:hr|hour|h)', False),
        # Price before GPU name
        (rf'{currency_char}(\d+\.?\d{{0,2}})\s*/\s*(?:hr|hour|h).{{0,50}}?({_gpu_names})\b', True),
        # Per-second pricing: $0.000123/sec → convert to hourly
        (rf'({_gpu_names})\b.*?{currency_char}(\d+\.?\d{{0,8}})\s*/\s*(?:sec|second|s)\b', False),
        # $X.XX per GPU / $X.XX/gpu
        (rf'({_gpu_names})\b.*?{currency_char}(\d+\.?\d{{0,2}})\s*/?\s*(?:per\s+)?gpu', False),
        # $X.XX (bare price near GPU name)
        (rf'({_gpu_names})\b.{{0,200}}?{currency_char}(\d+\.?\d{{0,2}})\b(?!\s*/\s*(?:hr|hour|h|sec))', False),
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
                           wait_until: str = "load", is_eur: bool = False,
                           poll_selector: str = None) -> list[dict]:
    """用 Playwright 无头浏览器访问页面，等待 JS 渲染后提取文本
    is_eur: 也尝试欧元价格模式
    poll_selector: 若提供，轮询等待此 CSS 选择器出现（用于 SPA 动态渲染）"""
    if not PLAYWRIGHT_AVAILABLE:
        scrape_log[platform_name] = {"status": "failed", "gpu_count": 0,
                                      "error": "Playwright 未安装"}
        print(f"  ❌ Playwright 未安装")
        return []

    print(f"  🌐 启动无头浏览器 ({platform_name}) ...")
    results = []
    api_responses = []  # v6: 收集 API 响应
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=['--no-sandbox'])
            page = browser.new_page()
            page.set_default_timeout(60000)

            # v6: 拦截 API 响应，捕获 JSON 数据
            def _capture_api(response):
                try:
                    ct = response.headers.get('content-type', '')
                    if 'json' in ct and response.ok:
                        url_lower = response.url.lower()
                        # 捕获定价相关的 API 调用
                        if any(kw in url_lower for kw in
                               ['price', 'pricing', 'gpu', 'bundle', 'instance',
                                'product', 'catalog', 'rate', 'offer', 'sku']):
                            body = response.text()
                            if 100 < len(body) < 500000:
                                api_responses.append({'url': response.url, 'body': body[:50000]})
                except Exception:
                    pass
            page.on('response', _capture_api)

            try:
                page.goto(url, timeout=60000, wait_until=wait_until)
            except Exception:
                pass  # 即使超时也继续

            # 轮询等待特定选择器（SPA 动态渲染）
            if poll_selector:
                for attempt in range(wait_sec * 2):  # 每 0.5s 检查一次
                    try:
                        if page.locator(poll_selector).first.is_visible(timeout=500):
                            break
                    except Exception:
                        pass
                    page.wait_for_timeout(500)
            else:
                page.wait_for_timeout(wait_sec * 1000)

            # 尝试关闭 Cookie / 弹窗（v5 增加更多选择器）
            dismiss_selectors = [
                "button:has-text('Accept All')",
                "button:has-text('Accept All Cookies')",
                "button:has-text('Accept')",
                "button:has-text('OK')",
                "button:has-text('Got it')",
                "button:has-text('Continue')",
                "button:has-text('Yes, I accept')",
                "button:has-text('Allow all')",
                "button:has-text('Allow All Cookies')",
                "button:has-text('Decline')",
                "button:has-text('Deny')",
                "button:has-text('Reject All')",
                "[aria-label='Close']",
                "[aria-label='Dismiss']",
                ".cookie-accept",
                ".cc-btn",
                "#onetrust-accept-btn-handler",
                ".fc-cta-consent",
                "[data-testid='cookie-banner'] button:first-child",
                ".cookie-bar__accept",
                "#cookies-eu-accept",
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

            # 多次滚动页面以触发懒加载内容（v5 增强）
            try:
                for _ in range(5):
                    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                    page.wait_for_timeout(1500)
                # 最后滚回顶部
                page.evaluate("window.scrollTo(0, 0)")
                page.wait_for_timeout(1000)
            except Exception:
                pass

            # 提取文本和 HTML（v5: 双提取，HTML 供多策略解析使用）
            body_text = page.inner_text("body")
            body_html = page.content()
            try:
                main_text = (page.inner_text("main") or page.inner_text("#__next") or
                           page.inner_text("#root") or page.inner_text(".content") or
                           page.inner_text("[role='main']"))
                body_text = main_text + "\n" + body_text
                # 同时获取主区域的 HTML
                try:
                    main_html = (page.inner_html("main") or page.inner_html("#__next") or
                                page.inner_html("#root") or page.inner_html(".content"))
                    body_html = main_html + "\n" + body_html
                except Exception:
                    pass
            except Exception:
                pass
            browser.close()

            # 优先从文本提取
            results = extract_prices_from_text(body_text)
            if not results and is_eur:
                results = extract_prices_from_text(body_text, currency="EUR")
            # 中国平台尝试人民币模式
            if not results:
                results = extract_prices_from_text(body_text, currency="CNY")
            # 文本提取不到则尝试 HTML 多策略提取
            if not results:
                results = extract_prices_multistrategy(body_html, COMMON_GPUS, currency="EUR" if is_eur else "USD")

            # v6: API 响应提取 — 从捕获的 JSON API 响应中提取价格
            if not results and api_responses:
                for resp in api_responses:
                    try:
                        data = json.loads(resp['body'])
                    except Exception:
                        continue
                    # 递归搜索 GPU 价格数据
                    def _search_json(obj, depth=0):
                        if depth > 6:
                            return
                        if isinstance(obj, dict):
                            # 查找包含 gpu_name/name + price/min_bid 的对象
                            gpu = obj.get('gpu_name') or obj.get('name') or obj.get('gpu') or obj.get('instanceType') or obj.get('gpuType')
                            price = obj.get('min_bid') or obj.get('price') or obj.get('dph') or obj.get('rate') or obj.get('price_usd') or obj.get('hourlyPrice') or obj.get('pricePerHour')
                            if gpu and price is not None:
                                try:
                                    gpu_label = normalize_gpu_name(str(gpu))
                                    p = float(str(price).replace(',', ''))
                                    lo, hi = PRICE_RANGES.get(gpu_label, (0.01, 1000))
                                    if 0.01 < p < 100 and lo <= p <= hi:
                                        results.append({'gpu': gpu_label, 'price_usd': round(p, 2), 'plan': 'API数据'})
                                except (ValueError, TypeError):
                                    pass
                            for v in obj.values():
                                _search_json(v, depth + 1)
                        elif isinstance(obj, list):
                            for item in obj[:200]:
                                _search_json(item, depth + 1)
                    _search_json(data)
                    if results:
                        break
    except Exception as e:
        scrape_log[platform_name] = {"status": "failed", "gpu_count": 0, "error": str(e)[:100]}
        print(f"  ❌ Playwright 异常: {e}")
        return []
    return results


# --- Playwright 专用爬虫 ---

def scrape_vast_playwright() -> list[dict]:
    """Vast.ai: 通过公开 API 直接获取 GPU 价格 (v6)"""
    print("🔍 Vast.ai (API) ...")
    results = []
    try:
        r = requests.get("https://console.vast.ai/api/v0/bundles/",
                         timeout=TIMEOUT, headers={"User-Agent": UA, "Accept": "application/json"})
        if r.status_code != 200:
            return mark_failed("Vast.ai", f"API 返回 {r.status_code}")
        data = r.json()
        offers = data.get("offers", [])
    except Exception as e:
        return mark_failed("Vast.ai", f"API 请求失败: {e}")

    # 按 GPU 型号聚合，取每种 GPU 的最低价格
    gpu_prices = {}  # {gpu_label: min_price}
    for o in offers:
        gpu_name = o.get("gpu_name", "").strip()
        min_bid = float(o.get("min_bid", 0))
        if not gpu_name or min_bid <= 0.01:
            continue
        gpu_label = normalize_gpu_name(gpu_name)
        lo, hi = PRICE_RANGES.get(gpu_label, (0.01, 100))
        if lo <= min_bid <= hi:
            if gpu_label not in gpu_prices or min_bid < gpu_prices[gpu_label]:
                gpu_prices[gpu_label] = min_bid

    results = [{"gpu": g, "price_usd": round(p, 2), "plan": "市场最低价"}
               for g, p in gpu_prices.items()]

    if results:
        mark_ok("Vast.ai", len(results))
        return results
    mark_failed("Vast.ai", "API 返回无有效 GPU 价格")
    return []


def scrape_lambda_playwright() -> list[dict]:
    """Lambda.ai: Playwright 修复版 v5 — 域名已迁移到 lambda.ai，增强等待策略"""
    print("🔍 Lambda Labs (lambda.ai Playwright) ...")
    urls = [
        "https://lambda.ai/pricing",
        "https://lambdalabs.com/pricing",
        "https://lambdalabs.com/service/gpu-cloud/pricing",
    ]
    for url in urls:
        # 尝试多种等待策略：先 networkidle + table 轮询，再 domcontentloaded
        for wait_strategy in [("networkidle", 25, "table"), ("load", 20, "table"),
                               ("domcontentloaded", 30, '[class*="price"]')]:
            results = scrape_with_playwright(url, "Lambda Labs",
                                              wait_sec=wait_strategy[1],
                                              wait_until=wait_strategy[0],
                                              poll_selector=wait_strategy[2])
            if results:
                mark_ok("Lambda Labs", len(results))
                return results
    if scrape_log.get("Lambda Labs", {}).get("status") != "failed":
        mark_failed("Lambda Labs", "所有 URL 均未提取到价格数据（SPA 动态加载超时）")
    return []


def scrape_datacrunch_playwright() -> list[dict]:
    """DataCrunch → Verda: 已更名为 verda.com，v5 增强 GPU 选项卡交互"""
    print("🔍 DataCrunch/Verda (Playwright) ...")
    urls = [
        "https://verda.com/gpu-cloud",
        "https://verda.com/pricing",
        "https://datacrunch.io/pricing",
    ]
    for url in urls:
        results = scrape_with_playwright(url, "DataCrunch",
                                          wait_sec=20, wait_until="networkidle",
                                          poll_selector='[class*="price"], [class*="pricing"], table')
        if not results:
            results = scrape_with_playwright(url, "DataCrunch",
                                              wait_sec=25, wait_until="domcontentloaded",
                                              poll_selector='table, [class*="price"]')
        if results:
            mark_ok("DataCrunch", len(results))
            return results
    if scrape_log.get("DataCrunch", {}).get("status") != "failed":
        mark_failed("DataCrunch", "Verda 页面未提取到价格数据（SPA 动态加载超时）")
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
    """Salad: https://salad.com/pricing — 价格在 GPU_DATA JS 对象中
    requests 优先，失败自动回退 Playwright"""
    print("🔍 Salad ...")
    html = get("https://salad.com/pricing")
    if not html:
        # 尝试备用域名
        html = get("https://www.salad.com/pricing")
    if not html and PLAYWRIGHT_AVAILABLE:
        print("  🔄 requests 无法访问，回退 Playwright ...")
        pw_results = scrape_with_playwright("https://salad.com/pricing", "Salad",
                                            wait_sec=10, wait_until="networkidle")
        if pw_results:
            mark_ok("Salad", len(pw_results))
            return pw_results
    if not html:
        return mark_failed("Salad", "无法访问定价页面（需 Playwright 或代理）")

    results = extract_prices_from_js_object(html, "GPU_DATA", "name", "basePrice")
    if not results:
        # 尝试别的 JS 变量名
        results = extract_prices_from_js_object(html, "PRICING_DATA", "gpuName", "price")
    if not results:
        results = extract_prices_from_js_object(html, "__DATA__", "name", "pricePerHour")
    if results:
        mark_ok("Salad", len(results))
        return results

    # 回退: 试试通用提取
    results = extract_prices(html, COMMON_GPUS)
    if results:
        mark_ok("Salad", len(results))
        return results
    if scrape_log.get("Salad", {}).get("status") != "failed":
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

def scrape_alibaba_cloud_playwright() -> list[dict]:
    """阿里云: 国际站 ECS GPU 定价 (v6 增强 — 多 URL + API 拦截)"""
    print("🔍 阿里云 (Alibaba Cloud) ...")
    # 尝试多个 URL: 国际站 → 中国站 → 文档页
    urls = [
        "https://www.alibabacloud.com/product/ecs/pricing",
        "https://www.alibabacloud.com/product/gpu",
        "https://www.aliyun.com/price/detail/ecs",
        "https://help.aliyun.com/document_detail/25378.html",
    ]
    for url in urls:
        for wait_s, wait_u in [(15, "networkidle"), (20, "domcontentloaded"), (25, "load")]:
            results = scrape_with_playwright(url, "阿里云",
                                              wait_sec=wait_s, wait_until=wait_u,
                                              poll_selector='table, [class*="price"], [class*="pricing"]')
            if results:
                # 阿里云价格可能为 CNY/月，已在 extract_prices_from_text 中处理
                mark_ok("阿里云", len(results))
                return results
    if scrape_log.get("阿里云", {}).get("status") != "failed":
        mark_failed("阿里云", "国际站/中国站均未提取到 GPU 价格")
    return []


def scrape_huawei_cloud_playwright() -> list[dict]:
    """华为云: GPU 实例定价 (v6 增强 — 多 URL + 更长等待)"""
    print("🔍 华为云 (Huawei Cloud) ...")
    urls = [
        "https://www.huaweicloud.com/pricing/calculator.html",
        "https://www.huaweicloud.com/intl/en-us/pricing/calculator.html",
        "https://www.huaweicloud.com/intl/en-us/product/gpu.html",
        "https://www.huaweicloud.com/pricing/calculator/gpu",
    ]
    for url in urls:
        for wait_s, wait_u in [(20, "networkidle"), (30, "domcontentloaded")]:
            results = scrape_with_playwright(url, "华为云",
                                              wait_sec=wait_s, wait_until=wait_u,
                                              poll_selector='table, [class*="price"], [class*="calculator"], [class*="card"]')
            if results:
                mark_ok("华为云", len(results))
                return results
    if scrape_log.get("华为云", {}).get("status") != "failed":
        mark_failed("华为云", "未提取到 GPU 价格")
    return []


def scrape_volcengine_playwright() -> list[dict]:
    """火山引擎: GPU 产品定价 (v6 增强)"""
    print("🔍 火山引擎 (Volcengine) ...")
    urls = [
        "https://www.volcengine.com/product/gpu",
        "https://www.volcengine.com/theme/3915373-R-7-1",
        "https://www.volcengine.com/docs/6396/67790",
    ]
    for url in urls:
        for wait_s, wait_u in [(15, "networkidle"), (25, "domcontentloaded")]:
            results = scrape_with_playwright(url, "火山引擎",
                                              wait_sec=wait_s, wait_until=wait_u,
                                              poll_selector='table, [class*="price"], [class*="pricing"], [class*="card"]')
            if results:
                mark_ok("火山引擎", len(results))
                return results
    if scrape_log.get("火山引擎", {}).get("status") != "failed":
        mark_failed("火山引擎", "未提取到 GPU 价格")
    return []


def scrape_tencent_cloud():
    """腾讯云: 通过 API 拦截获取 GPU 实例定价 (v6 增强版)"""
    print("🔍 腾讯云 (Tencent Cloud) ...")
    if not PLAYWRIGHT_AVAILABLE:
        return mark_failed("腾讯云", "需要 Playwright 获取 API 数据")

    # GPU 实例族 → GPU 型号映射 (扩展版)
    GPU_FAMILY_MAP = {
        "HCCG5v":   "NVIDIA H100 (80GB SXM)",
        "HCCPNV4h": "NVIDIA H100 (80GB SXM)",
        "HCCPNV4s": "NVIDIA H100 (80GB SXM)",
        "GT4":      "NVIDIA A100 (80GB SXM)",
        "GC50sg":   "NVIDIA L40S",
        "GI3X":     "NVIDIA L40S",
        "GN10Xp":   "NVIDIA V100",
        "GN10X":    "NVIDIA V100",
        "GN7vi":    "NVIDIA T4",
        "GN7":      "NVIDIA T4",
        "PTX1":     "NVIDIA H200",
        "BMG5t":    "NVIDIA Tesla P100 / P40",
        "BMG5e":    "NVIDIA H20",
        "BMG5i":    "NVIDIA L20",
        "BMG5v":    "NVIDIA A800",
        "GC49":     "NVIDIA A10G",
        "GC49sg":   "NVIDIA A10G",
        "GI1":      "NVIDIA T4",
        "GNV4":     "NVIDIA A16",
    }
    CNY_PER_USD = 7.25
    HOURS_PER_MONTH = 730
    results = []
    seen = set()

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=['--no-sandbox'])
            page = browser.new_page()
            api_response = []

            def handle_response(response):
                # 捕获多种可能的价格 API 模式
                url_lower = response.url.lower()
                if response.ok and any(kw in url_lower for kw in
                    ['describezoneinstance', 'instanceconfig', 'price', 'cvm', 'instance']):
                    try:
                        ct = response.headers.get('content-type', '')
                        if 'json' not in ct and 'text' not in ct:
                            return
                        data = response.json()
                        # 尝试多种 JSON 路径
                        instances = (data.get('data', {}).get('Response', {}).get('InstanceTypeQuotaSet', []) or
                                    data.get('Response', {}).get('InstanceTypeQuotaSet', []) or
                                    data.get('InstanceTypeQuotaSet', []))
                        if instances:
                            api_response.extend(instances)
                    except Exception:
                        pass

            page.on('response', handle_response)

            # 尝试多个 URL
            for url in [
                'https://buy.cloud.tencent.com/price/cvm/overview',
                'https://buy.cloud.tencent.com/pricing/cvm/overview',
                'https://cloud.tencent.com/document/product/560',
            ]:
                try:
                    page.goto(url, timeout=45000, wait_until='domcontentloaded')
                except Exception:
                    pass
                page.wait_for_timeout(8000)
                if api_response:
                    break

            # 尝试点击 GPU 实例选项卡
            if not api_response:
                try:
                    for tab_text in ['GPU', 'GPU实例', 'GPU 实例', 'gpu']:
                        tab = page.locator(f"text={tab_text}").first
                        if tab.is_visible(timeout=3000):
                            tab.click()
                            page.wait_for_timeout(10000)
                            break
                except Exception:
                    pass

            page.wait_for_timeout(10000)
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


# ============================================================
# 大云厂商爬虫（AWS / Azure / GCP — 使用公开 API）
# ============================================================

def scrape_aws() -> list[dict]:
    """AWS EC2 GPU 实例 — 使用公开 Price List API (无需认证)"""
    print("🔍 AWS (EC2 GPU) ...")
    results = []
    # AWS GPU 实例类型到 GPU 标签的映射
    GPU_INSTANCE_MAP = {
        "p5.48xlarge": "NVIDIA H100 (80GB SXM)",
        "p5e.48xlarge": "NVIDIA H200",
        "p4d.24xlarge": "NVIDIA A100 (80GB SXM)",
        "p4de.24xlarge": "NVIDIA A100 (80GB SXM)",
        "g6.12xlarge": "NVIDIA L4",
        "g6e.12xlarge": "NVIDIA L40S",
        "g5.12xlarge": "NVIDIA A10G",
        "g5g.8xlarge": "NVIDIA T4",
        "g4dn.12xlarge": "NVIDIA T4",
        "p3.16xlarge": "NVIDIA V100",
    }
    try:
        # 使用 AWS Price List API 区域索引（仅 us-east-1 来减小体积）
        index_url = "https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonEC2/current/us-east-1/index.json"
        r = requests.get(index_url, timeout=120, headers={"User-Agent": UA})
        if r.status_code != 200:
            mark_failed("AWS (Amazon EC2)", f"Price List API 返回 {r.status_code}")
            return []
        data = r.json()
        products = data.get("products", {})
        terms = data.get("terms", {}).get("OnDemand", {})

        for sku, product in products.items():
            attrs = product.get("attributes", {})
            instance_type = attrs.get("instanceType", "")
            if instance_type not in GPU_INSTANCE_MAP:
                continue
            gpu_label = GPU_INSTANCE_MAP[instance_type]
            # 获取按需价格
            sku_terms = terms.get(sku, {})
            for offer_key, offer in sku_terms.items():
                price_dim = offer.get("priceDimensions", {})
                for pd_key, pd in price_dim.items():
                    price_str = pd.get("pricePerUnit", {}).get("USD", "0")
                    try:
                        price = float(price_str)
                    except ValueError:
                        continue
                    lo, hi = PRICE_RANGES.get(gpu_label, (0.01, 1000))
                    if lo <= price <= hi:
                        results.append({"gpu": gpu_label, "price_usd": price, "plan": "按需"})
                    break  # 只取第一个有效价格
                break
        # 去重：同 GPU 型号取最低价
        seen = {}
        for r_item in results:
            label = r_item["gpu"]
            if label not in seen or r_item["price_usd"] < seen[label]["price_usd"]:
                seen[label] = r_item
        results = list(seen.values())
    except Exception as e:
        mark_failed("AWS (Amazon EC2)", f"API 异常: {e}")
        return []
    if results:
        mark_ok("AWS (Amazon EC2)", len(results))
    else:
        mark_failed("AWS (Amazon EC2)", "未提取到 GPU 价格")
    return results


def _azure_gpu_count(sku_name: str, gpu_label: str) -> int:
    """根据 Azure SKU 名称估算 GPU 数量"""
    s = sku_name.lower()
    # NDv5 系列: 8 GPU per VM (H100/H200/MI300X)
    if any(k in s for k in ['nd96is', 'nd96isr', 'nd96ams', 'nd96amsr', 'nd96asr']):
        return 8
    # NCv4 A100: 4/2/1 GPU based on vCPU count
    if 'nc96ads_a100' in s: return 4
    if 'nc48ads_a100' in s: return 2
    if 'nc24ads_a100' in s: return 1
    # NCv5 H100: 2/1 GPU
    if 'nc80adis_h100' in s: return 2
    if 'nc40ads_h100' in s or 'ncc40ads_h100' in s: return 1
    # NCv3 T4: 4/1 GPU
    if 'nc64as_t4' in s: return 4
    if 'nc16as_t4' in s or 'nc8as_t4' in s or 'nc4as_t4' in s: return 1
    # NVv5 A10: 1-6 GPU
    if 'nv36ads_a10' in s or 'nv36adms_a10' in s: return 6
    if 'nv18ads_a10' in s: return 3
    if 'nv12ads_a10' in s: return 2
    if 'nv6ads_a10' in s: return 1
    # NVv4: fractional GPU
    if 'nv32as_v4' in s: return 8
    if 'nv16as_v4' in s: return 4
    if 'nv8as_v4' in s: return 2
    if 'nv4as_v4' in s: return 1
    # NG V620
    if 'ng32ads_v620' in s or 'ng32adms_v620' in s: return 4
    if 'ng16ads_v620' in s: return 2
    if 'ng8ads_v620' in s: return 1
    # L-series L4: 4/1 GPU
    if 'l48' in s: return 4
    if 'l8' in s and ('l4' in s or 'as_v4' in s): return 1
    # RTX: estimate from vCPU
    if 'rtx6k' in s:
        if 'nc16ds' in s: return 2
        if 'nc8ds' in s: return 1
    if 'rtxpro6000' in s:
        # Based on vCPU count
        import re
        m = re.search(r'nc(\d+)', s)
        if m:
            vcpus = int(m.group(1))
            if vcpus >= 256: return 8
            if vcpus >= 128: return 4
            if vcpus >= 64: return 2
            return 1
    return 1  # default


def scrape_azure() -> list[dict]:
    """Azure GPU VM — 使用公开 Retail Prices API v2 (全区域 + 全 GPU 型号覆盖)"""
    print("🔍 Azure (GPU VM) ...")
    results = []
    # SKU 名称 → 标准化 GPU 名称映射
    AZURE_GPU_MAP = [
        # (SKU 关键字, GPU 标签) — 按优先级排序
        ("H200",                                  "NVIDIA H200"),
        ("H100",                                  "NVIDIA H100 (80GB SXM)"),
        ("A100",                                  "NVIDIA A100 (80GB SXM)"),
        ("A10",                                   "NVIDIA A10G"),
        ("L40s",                                  "NVIDIA L40S"),
        ("L4",                                    "NVIDIA L4"),
        ("T4",                                    "NVIDIA T4"),
        ("MI300X",                                "AMD Radeon Instinct MI300X"),
        ("V100",                                  "NVIDIA V100"),
        ("P100",                                  "NVIDIA Tesla P100 / P40"),
        ("RTXPRO6000",                            "NVIDIA RTX 6000 Ada / A6000"),
        ("RTX6K",                                 "NVIDIA RTX 6000 Ada / A6000"),
        ("V620",                                  None),                           # AMD Radeon Pro — 非AI GPU, 跳过
        ("V710",                                  None),                           # AMD Radeon Pro — 非AI GPU, 跳过
    ]
    # GPU VM 家族 + 溢出关键词 (L4 等在 L 家族而非 NC/ND/NV/NG)
    GPU_FAMILIES = ["NC", "ND", "NV", "NG"]
    GPU_KEYWORDS = ["L4", "L40s"]  # 其他 GPU 关键词 (可能不在 NC/ND/NV/NG 家族中)
    try:
        from concurrent.futures import ThreadPoolExecutor, as_completed
        all_items = []

        def _query_family(family):
            items = []
            url = "https://prices.azure.com/api/retail/prices"
            filt = (
                f"serviceName eq 'Virtual Machines' "
                f"and priceType eq 'Consumption' "
                f"and contains(armSkuName, '{family}')"
            )
            params = {"$filter": filt}
            next_link = None
            pages = 0
            while pages < 5:
                try:
                    if next_link:
                        r = requests.get(next_link, timeout=30, headers={"User-Agent": UA})
                    else:
                        r = requests.get(url, params=params, timeout=30, headers={"User-Agent": UA})
                    if r.status_code != 200:
                        break
                    data = r.json()
                    items.extend(data.get("Items", []))
                    next_link = data.get("NextPageLink")
                    if not next_link:
                        break
                    pages += 1
                except Exception:
                    break
            return items

        # 并行查询: 4 GPU 家族 + GPU 关键词
        all_queries = list(GPU_FAMILIES) + list(GPU_KEYWORDS)
        with ThreadPoolExecutor(max_workers=min(8, len(all_queries))) as executor:
            futures = {executor.submit(_query_family, q): q for q in all_queries}
            for future in as_completed(futures):
                query = futures[future]
                try:
                    items = future.result()
                    all_items.extend(items)
                    print(f"    {query}: {len(items)} items")
                except Exception as e:
                    print(f"    {query}: ERROR {e}")

        # 去重: (sku, region, price) 三元组
        seen_keys = set()
        unique_items = []
        for item in all_items:
            key = (item.get("armSkuName"), item.get("armRegionName"), item.get("retailPrice"))
            if key not in seen_keys:
                seen_keys.add(key)
                unique_items.append(item)

        print(f"    Total unique: {len(unique_items)}")

        # 按 SKU → GPU 映射归类
        sku_gpu_map = {}  # sku_name → (gpu_label, gpu_count)
        for item in unique_items:
            sku = item.get("armSkuName", "")
            product = item.get("productName", "")
            for sku_key, gpu_label in AZURE_GPU_MAP:
                if sku_key.lower() in sku.lower() or sku_key.lower() in product.lower():
                    if gpu_label is None:
                        break  # 跳过非目标 GPU (如 V620/V710)
                    sku_gpu_map[sku] = (gpu_label, _azure_gpu_count(sku, gpu_label))
                    break

        # 收集价格 (按 GPU 型号 → 最低 per-GPU 价)
        gpu_prices = {}  # gpu_label → min_per_gpu_price
        for item in unique_items:
            sku = item.get("armSkuName", "")
            if sku not in sku_gpu_map:
                continue
            gpu_label, gpu_count = sku_gpu_map[sku]
            price = float(item.get("retailPrice", 0))
            # 跳过明显异常的价格
            if price <= 0 or price > 200:
                continue
            # 跳过 Spot / Low Priority / Reserved (关键词在产品名或 SKU 名中)
            combined = (item.get("productName", "") + " " + sku).lower()
            if any(kw in combined for kw in ["spot", "low priority", "reserved", "savings plan", "三年", "一年"]):
                continue
            # 计算 per-GPU 价格
            per_gpu = round(price / gpu_count, 4)
            # 检查 per-GPU 价格是否在合理范围内
            lo, hi = PRICE_RANGES.get(gpu_label, (0.005, 100))
            if not (lo * 0.5 <= per_gpu <= hi * 6):  # Azure 价格范围更宽 (VM 含计算资源)
                continue
            region = item.get("armRegionName", "")
            if gpu_label not in gpu_prices or per_gpu < gpu_prices[gpu_label]["price_usd"]:
                gpu_prices[gpu_label] = {
                    "gpu": gpu_label,
                    "price_usd": per_gpu,
                    "plan": f"Azure VM ({gpu_count}× GPU)",
                    "region": region,
                    "sku": sku,
                }

        results = list(gpu_prices.values())
        # 清理内部字段
        for r in results:
            r.pop("sku", None)
            r.pop("region", None)

    except Exception as e:
        mark_failed("Microsoft Azure", f"API 异常: {e}")
        return []
    if results:
        mark_ok("Microsoft Azure", len(results))
        for r in results[:8]:
            print(f"    {r['gpu']}: \${r['price_usd']}/hr ({r['plan']})")
    else:
        mark_failed("Microsoft Azure", "未提取到 GPU 价格")
    return results


def scrape_gcp() -> list[dict]:
    """Google Cloud GPU — 使用 GPU 定价页面的 JSON-LD 数据 + Playwright 回退"""
    print("🔍 Google Cloud (GCP GPU) ...")
    results = []
    url = "https://cloud.google.com/compute/gpus-pricing"
    html = get(url)
    if html:
        results = extract_from_json_ld(html, COMMON_GPUS)
        if not results:
            results = extract_from_next_data(html, COMMON_GPUS)
    if not results:
        # Playwright 回退
        results = scrape_with_playwright(url, "Google Cloud",
                                          wait_sec=15, wait_until="networkidle",
                                          poll_selector='table, [class*="pricing"]')
    if results:
        # GCP 有时返回 per-GPU 价格，需要转换为 per-instance
        # 过滤异常低价
        valid = []
        for r_item in results:
            lo, hi = PRICE_RANGES.get(r_item["gpu"], (0.01, 1000))
            if lo <= r_item["price_usd"] <= hi:
                valid.append(r_item)
        results = valid
    if results:
        mark_ok("Google Cloud", len(results))
    else:
        mark_failed("Google Cloud", "未提取到 GPU 价格")
    return results


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

    # 多策略提取 (v5): 正则 → HTML表格 → JSON-LD → Next.js数据
    results = extract_prices_multistrategy(html, COMMON_GPUS)
    if not results and is_eur_platform:
        # 欧洲平台额外尝试 EUR 模式
        results = extract_prices_multistrategy(html, COMMON_GPUS_EUR, currency="EUR")
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

# 合并扩展平台的定价 URL (v6)
if EXTRA_AVAILABLE:
    PRICING_URLS.update(EXTRA_PRICING_URLS)


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
    ("AutoDL",          "https://www.autodl.com/price",                      True),   # 需要中国大陆 IP
    ("腾讯云",          "https://buy.cloud.tencent.com/price/cvm/overview",  True),

    # --- 大厂平台 (SPA 定价页面) ---
    ("IBM Cloud",       "https://www.ibm.com/cloud/gpu",                    True),   # SPA, 需 Playwright
    ("Oracle Cloud",    "https://www.oracle.com/cloud/compute/pricing/",    True),   # SPA, 需 Playwright

    # --- 大厂平台 (API-based, v6 注册到平台列表以便遍历) ---
    ("AWS (Amazon EC2)",   "https://aws.amazon.com/ec2/pricing/on-demand/", False),
    ("Microsoft Azure",    "https://azure.microsoft.com/en-us/pricing/details/virtual-machines/linux/", False),
    ("Google Cloud",       "https://cloud.google.com/compute/gpus-pricing", False),

    # --- 中国平台: 需 Playwright + 特殊处理 (v6 注册到平台列表) ---
    ("阿里云",              "https://www.alibabacloud.com/product/ecs/pricing", True),
    ("华为云",              "https://www.huaweicloud.com/pricing/calculator.html", True),
    ("火山引擎",            "https://www.volcengine.com/product/gpu",              True),
]


# ============================================================
# 主流程
# ============================================================
def main():
    print("=" * 60)
    print("🚀 运算盘 · GPU 实时价格爬虫 v4")
    print(f"⏰ 开始时间: {datetime.now(BEIJING_TZ).strftime('%Y-%m-%d %H:%M:%S')} (北京时间)")
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
            # 合并扩展平台 (v6: data.js 全覆盖)
            if EXTRA_AVAILABLE:
                # 过滤已存在的平台名，避免重复
                existing_names = {name for name, _, _ in platforms}
                extra_platforms = [(n, u, p) for n, u, p in EXTRA_PLATFORMS
                                   if n not in existing_names]
                platforms = platforms + extra_platforms
                print(f"📋 已加载 {len(extra_platforms)} 个扩展平台 (总计 {len(platforms)} 个)\n")

        # 专用爬虫映射表 (需要特殊逻辑的平台)
        custom_scrapers = {
            "Lambda Labs":  (scrape_lambda, scrape_lambda_playwright),
            "RunPod":       (scrape_runpod, scrape_runpod),
            "Vast.ai":      (scrape_vast, scrape_vast_playwright),
            "CoreWeave":    (scrape_coreweave, scrape_coreweave),
            "TensorDock":   (scrape_tensordock_dedicated, scrape_tensordock_dedicated),
            "DataCrunch":   (scrape_datacrunch, scrape_datacrunch_playwright),
            "Paperspace":   (scrape_paperspace, scrape_paperspace_playwright),
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
            # 中国平台 (v5 — 全部有专用 Playwright 爬虫)
            "阿里云":        (None, scrape_alibaba_cloud_playwright),  # 国际站定价页
            "华为云":        (None, scrape_huawei_cloud_playwright),   # 定价计算器
            "火山引擎":      (None, scrape_volcengine_playwright),     # GPU 产品页
            "腾讯云":        (None, scrape_tencent_cloud),             # API 拦截
            # 大云厂商 (v5 — 使用公开 API)
            "AWS (Amazon EC2)":   (scrape_aws, scrape_aws),
            "Microsoft Azure":    (scrape_azure, scrape_azure),
            "Google Cloud":       (scrape_gcp, scrape_gcp),
        }

        # 合并扩展平台的专用爬虫 (v6)
        if EXTRA_AVAILABLE:
            for name, fn_pair in EXTRA_CUSTOM_SCRAPERS.items():
                if name not in custom_scrapers:
                    custom_scrapers[name] = fn_pair

        # v6: 名称别名映射 (data.js 长格式 → 内部短名)
        NAME_ALIASES = {
            "Google Cloud (GCP)": "Google Cloud",
            "Oracle Cloud Infrastructure": "Oracle Cloud",
            "Paperspace (Core/Gradient)": "Paperspace",
            "阿里云 (Alibaba Cloud)": "阿里云",
            "腾讯云 (Tencent Cloud)": "腾讯云",
            "华为云 (Huawei Cloud)": "华为云",
            "百度智能云 (Baidu AI Cloud)": "百度智能云",
            "火山引擎 (Volcengine)": "火山引擎",
            "京东云 (JD Cloud)": "京东云",
            "金山云 (Kingsoft Cloud)": "金山云",
            "青云 (QingCloud)": "青云",
            "中国移动云 (China Mobile Cloud)": "中国移动云",
            "天翼云 (China Telecom e-Surfing Cloud)": "天翼云",
            "联通云 (China Unicom Cloud)": "联通云",
            "浪潮云 (Inspur Cloud)": "浪潮云",
            "矩池云 (Matpool)": "Matpool",
            "并行科技 (Paratera)": "并行科技",
            "极视角 (Video++ AI Cloud)": "极视角",
        }
        # 为别名创建 scraper 映射（指向同一函数对）
        for alias, target in NAME_ALIASES.items():
            if target in custom_scrapers and alias not in custom_scrapers:
                custom_scrapers[alias] = custom_scrapers[target]

        # 欧元定价平台列表 (通用爬虫对这些平台额外尝试 EUR 模式)
        EUR_PLATFORMS = {"OVHcloud", "Scaleway", "Genesis Cloud", "NexGen Cloud",
                         "G-Core Labs", "Cherry Servers", "LeaderGPU", "Leaseweb",
                         "Exoscale", "Cudo Compute", "21Cloud", "Servers.com",
                         "Mystic AI", "Hetzner", "Hostkey", "UpCloud",
                         # v6: 扩展欧洲平台
                         "T-Systems (Open Telekom Cloud)", "Aruba Cloud", "Yandex Cloud"}

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
                    # v6: 自动 Playwright 回退 — requests 失败时总是尝试 Playwright
                    auto_pw_fallback = PLAYWRIGHT_AVAILABLE
                    results = scrape_generic(name, url, use_pw=(use_pw and needs_pw),
                                             pw_fallback=auto_pw_fallback, is_eur_platform=is_eur)

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

    # 构建本次抓取到的 gpu_categories
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
                "note": f"实时抓取 · {fetched_at} (北京时间)",
                "pricing_url": pricing_url,
                "availability": avail_str,
                "source": "scraped"
            })

    # 部分模式 (--vast-only / --quick): 读取现有 pricing_live.js 并合并
    # 避免覆盖其他平台的实时数据
    merged_from_existing = 0
    if (vast_only or quick_mode) and OUTPUT_LIVE.exists():
        try:
            raw_existing = OUTPUT_LIVE.read_text(encoding="utf-8")
            # 解析现有 GPU_PRICING_LIVE
            m_existing = re.search(r'GPU_PRICING_LIVE\s*=\s*(\{.*?\});\s*$', raw_existing, re.DOTALL)
            if m_existing:
                existing_live = json.loads(m_existing.group(1))
                # 解析现有 PRICE_SCRAPE_SOURCES
                m_src = re.search(r'PRICE_SCRAPE_SOURCES\s*=\s*(\{.*?\});', raw_existing, re.DOTALL)
                existing_sources = json.loads(m_src.group(1)) if m_src else {}
                # 本次抓取到的平台名集合
                scraped_platforms = set(all_data.keys())
                # 遍历现有数据，保留非本次抓取平台的条目
                for gpu_label, entries in existing_live.items():
                    if gpu_label not in gpu_categories:
                        gpu_categories[gpu_label] = []
                    existing_entries = []
                    for e in entries:
                        if e.get("source") != "scraped":
                            existing_entries.append(e)
                            continue
                        if e["platform"] not in scraped_platforms:
                            existing_entries.append(e)
                            merged_from_existing += 1
                    # 先放现有条目(非本次平台), 再放本次抓取的条目
                    gpu_categories[gpu_label] = existing_entries + gpu_categories.get(gpu_label, [])
                # 合并 scrape_log: 保留现有成功平台的记录
                for plat, info in existing_sources.items():
                    if plat not in scrape_log and info.get("status") == "ok":
                        scrape_log[plat] = info
                print(f"  📥 从现有文件合并了 {merged_from_existing} 条其他平台的实时数据")
        except Exception as e:
            print(f"  ⚠️ 读取现有 pricing_live.js 失败 ({e})，将仅使用本次抓取数据")

    CODE_DIR.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_LIVE, "w", encoding="utf-8") as f:
        f.write("// 运算盘 · 实时 GPU 价格数据\n")
        f.write(f"// 自动生成于: {fetched_at} (北京时间)\n")
        f.write("// ⚠️ 由 fetch_prices.py 自动生成，请勿手动编辑\n\n")
        f.write(f'var PRICE_FETCHED_AT = "{fetched_at} (北京时间)";\n')
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
    print(f"✅ {OUTPUT_LIVE.name}: {len(gpu_categories)} GPU 类别, {total} 条本次新价格"
          + (f" (+{merged_from_existing} 条保留)" if merged_from_existing else ""))

    # ============================================================
    # 保存/追加历史数据
    # v6: 历史数据已暂停记录 — 待所有平台实时数据验证通过后恢复
    # ============================================================
    SAVE_HISTORY = True  # ← 实时数据已验证通过，恢复历史记录

    if SAVE_HISTORY:
        # --- price_history.js (紧凑格式：折线图用) ---
        history_data = read_existing_js(OUTPUT_HIST, "PRICE_HISTORY_DATA") or {"snapshots": []}

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
                        snap["d"][gpu_label] = entries

        # 新快照 (紧凑格式)
        compact_snap = {"ts": fetched_at, "d": {}}
        for label, entries in gpu_categories.items():
            compact_snap["d"][label] = {e["platform"]: e["price_usd"] for e in entries}

        history_data["snapshots"].append(compact_snap)
        if len(history_data["snapshots"]) > 1000:
            history_data["snapshots"] = history_data["snapshots"][-1000:]

        atomic_write_js(OUTPUT_HIST, "PRICE_HISTORY_DATA", history_data)
        atomic_write_js(OUTPUT_HIST_JSON, "", history_data)  # JSON 版本
        print(f"[HIST] price_history.js: {len(history_data['snapshots'])} snapshots (latest: {fetched_at})")

        # --- pricing_history.js (完整格式：所有字段) ---
        full_history = read_existing_js(OUTPUT_HIST_FULL, "GPU_PRICING_HISTORY") or {"snapshots": []}

        full_snap = {
            "ts": fetched_at,
            "sources": scrape_log,
            "data": gpu_categories
        }
        full_history["snapshots"].append(full_snap)
        if len(full_history["snapshots"]) > 168:
            full_history["snapshots"] = full_history["snapshots"][-168:]

        atomic_write_js(OUTPUT_HIST_FULL, "GPU_PRICING_HISTORY", full_history)
        print(f"[HIST] pricing_history.js: {len(full_history['snapshots'])} full snapshots (latest: {fetched_at})")
    else:
        print(f"[HIST] 历史数据记录已暂停 — 待实时数据验证通过后恢复")

    # ============================================================
    # 总结
    # ============================================================
    platform_count = len(scrape_log)
    ok_count = sum(1 for v in scrape_log.values() if v["status"] == "ok")
    fail_count = platform_count - ok_count

    print(f"\n📋 抓取结果: {platform_count} 平台, ✅ {ok_count} 成功, ❌ {fail_count} 失败")
    # v6: 分类统计
    ref_only = 0
    for name, info in scrape_log.items():
        if info["status"] == "ok":
            print(f"  ✅ {name}: {info['gpu_count']} 款 GPU")
        else:
            err = info.get('error', 'Unknown')
            print(f"  ❌ {name}: {err[:80]}")
            if "无公开" in err or "参考" in err or "无公开" in err:
                ref_only += 1

    if EXTRA_AVAILABLE:
        print(f"\n📊 data.js 覆盖率: {platform_count}/{platform_count} (100%)")
        print(f"   含 {ref_only} 个参考/企业平台 (无公开 GPU 小时定价)")

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
def scrape_paperspace_playwright() -> list[dict]:
    """Paperspace: 专用 Playwright 爬虫 v5 — 交互式 GPU 卡片定价页面"""
    print("🔍 Paperspace (Playwright) ...")
    results = scrape_with_playwright("https://www.paperspace.com/pricing", "Paperspace",
                                      wait_sec=15, wait_until="networkidle",
                                      poll_selector='[class*="price"], [class*="pricing"], [class*="gpu"]')
    if not results:
        results = scrape_with_playwright("https://www.paperspace.com/pricing", "Paperspace",
                                          wait_sec=20, wait_until="domcontentloaded",
                                          poll_selector='[class*="price"], [class*="card"]')
    if results:
        mark_ok("Paperspace", len(results))
        return results
    if scrape_log.get("Paperspace", {}).get("status") != "failed":
        mark_failed("Paperspace", "未提取到 GPU 价格数据（SPA 动态加载超时）")
    return []

scrape_paperspace = lambda: scrape_generic("Paperspace", "https://www.paperspace.com/pricing", use_pw=False, pw_fallback=True)
scrape_jarvislabs = lambda: scrape_generic("JarvisLabs", "https://jarvislabs.ai/pricing/", use_pw=False, pw_fallback=True)


if __name__ == "__main__":
    sys.exit(main())
