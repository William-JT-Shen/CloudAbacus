#!/usr/bin/env python3
"""
CloudAbacus 扩展平台爬虫 v1
============================
覆盖 data.js 中所有尚未在 fetch_prices.py 中注册的平台。
每个平台按抓取策略分类：
  A) 静态 HTML 页面 (requests)
  B) SPA 动态页面 (Playwright)
  C) API 端点
  D) 参考用途 (无公开定价页面)

导入方式:
  from _extra_platforms import (
      EXTRA_PLATFORMS, EXTRA_PRICING_URLS,
      scrape_extra_or_ref, EXTRA_CUSTOM_SCRAPERS
  )
"""

import json
import re
import requests
from pathlib import Path

# 复用 fetch_prices.py 中的工具函数
try:
    from _availability import scrape_vast_rental_scale, get_rental_scale_str
except ImportError:
    pass

TIMEOUT = 20
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36")

# Playwright 可用性
PLAYWRIGHT_AVAILABLE = False
try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    pass


# ============================================================
# 工具函数（轻量本地副本，避免循环导入）
# ============================================================

def _get(url: str, accept_any_status: bool = False) -> str | None:
    """HTTP GET，返回文本或 None"""
    try:
        r = requests.get(url, timeout=TIMEOUT,
                         headers={"User-Agent": UA}, allow_redirects=True)
        if r.status_code == 200:
            return r.text
        if accept_any_status and len(r.text) > 5000:
            return r.text
        return None
    except Exception:
        return None


# ============================================================
# GPU 名称本地规范化 (精简版，避免循环导入)
# ============================================================

def _normalize(raw: str) -> str:
    """本地 GPU 名称规范化，覆盖最常用型号"""
    raw = raw.strip()
    mapping = {
        'h100': 'NVIDIA H100 (80GB SXM)', 'h200': 'NVIDIA H200',
        'gh200': 'NVIDIA GH200',
        'a100': 'NVIDIA A100 (80GB SXM)',
        'a6000': 'NVIDIA RTX 6000 Ada / A6000',
        'rtx 6000 ada': 'NVIDIA RTX 6000 Ada / A6000',
        'rtx 5090': 'RTX 5090', 'rtx 5080': 'RTX 5080',
        'rtx 4090': 'NVIDIA RTX 4090', 'rtx 4080': 'NVIDIA RTX 4080 / 4080 Super',
        'rtx 3090': 'NVIDIA RTX 3090 / 3090 Ti',
        'rtx 3080': 'NVIDIA RTX 3080 / 3080 Ti',
        'l40s': 'NVIDIA L40S', 'l4': 'NVIDIA L4', 'a40': 'NVIDIA A40',
        't4': 'NVIDIA T4', 'v100': 'NVIDIA V100',
        'b200': 'NVIDIA B200', 'b300': 'NVIDIA B300',
        'a10g': 'NVIDIA A10G', 'a16': 'NVIDIA A16',
        'h20': 'NVIDIA H20', 'l20': 'NVIDIA L20',
        'a800': 'NVIDIA A800', 'h800': 'NVIDIA H800',
        'mi300x': 'AMD Radeon Instinct MI300X', 'mi250x': 'AMD Radeon Instinct MI250X',
    }
    key = raw.lower().replace('nvidia ', '').replace('geforce ', '').replace('amd ', '').strip()
    key = re.sub(r'\s*\(\d+\s*GB\)', '', key, flags=re.IGNORECASE).strip()
    key = re.sub(r'\s*Ti\s+Super', ' Ti', key, flags=re.IGNORECASE).strip()
    key = re.sub(r'\s+Super', '', key, flags=re.IGNORECASE).strip()
    return mapping.get(key, raw)


# 合理的价格范围 (美元/小时) — 本地副本
_PRICE_RANGES = {
    "NVIDIA H100 (80GB SXM)": (1.20, 8.00), "NVIDIA H200": (2.50, 8.00),
    "NVIDIA GH200": (3.00, 10.00), "NVIDIA A100 (80GB SXM)": (0.40, 5.00),
    "NVIDIA A100 (40GB PCIe)": (0.30, 3.50), "NVIDIA L40S": (0.50, 3.00),
    "NVIDIA L4": (0.15, 1.50), "NVIDIA A40": (0.25, 2.00),
    "NVIDIA T4": (0.10, 1.00), "NVIDIA V100": (0.10, 3.00),
    "NVIDIA RTX 6000 Ada / A6000": (0.25, 2.00),
    "NVIDIA RTX 4090": (0.15, 1.50), "NVIDIA RTX 3090 / 3090 Ti": (0.08, 0.80),
    "NVIDIA RTX 3080 / 3080 Ti": (0.06, 1.20),
    "RTX 5090": (0.30, 3.00), "RTX 5080": (0.20, 2.00),
    "RTX 5070 Ti": (0.12, 1.20), "RTX 5070": (0.10, 1.00),
    "NVIDIA B200": (3.00, 12.00), "NVIDIA B300": (3.50, 14.00),
    "NVIDIA H800": (1.50, 8.00), "NVIDIA A800": (0.50, 5.00),
    "NVIDIA H20": (0.80, 4.00), "NVIDIA L20": (0.30, 2.00),
    "NVIDIA A16": (0.20, 1.50), "NVIDIA A10G": (0.25, 2.50),
    "NVIDIA Quadro RTX 4000": (0.10, 0.80), "NVIDIA GTX 1080 Ti": (0.04, 0.40),
    "AMD Radeon Instinct MI300X": (2.00, 8.00), "AMD Radeon Instinct MI250X": (1.00, 6.00),
    "NVIDIA Tesla P100 / P40": (0.05, 1.00),
}


def _extract(html: str, gpu_names: list[str], currency: str = "USD") -> list[dict]:
    """简化版价格提取：从 HTML 文本中搜索 GPU 名称 + $ 价格"""
    results = []
    seen = set()
    eur_to_usd = 1.08
    cny_to_usd = 0.14
    hours_per_month = 730

    if currency == "EUR":
        price_pat = r'€\s*(\d+\.?\d*)\s*/\s*(?:h|hr|hour)'
    elif currency == "CNY":
        price_pat = r'[¥￥]\s*([\d,]+\.?\d*)\s*/\s*(?:月|month|mo)'
    else:
        price_pat = r'\$\s*(\d+\.?\d*)\s*/\s*(?:h|hr|hour)'

    for gpu_name in gpu_names:
        gpu_label = _normalize(gpu_name)
        lo, hi = _PRICE_RANGES.get(gpu_label, (0.01, 1000))
        for gpu_m in re.finditer(re.escape(gpu_name), html, re.IGNORECASE):
            ctx = html[gpu_m.start():gpu_m.end() + 600]
            for price_m in re.finditer(price_pat, ctx, re.IGNORECASE):
                try:
                    price = float(price_m.group(1).replace(',', ''))
                except ValueError:
                    continue
                if currency == "EUR":
                    price = round(price * eur_to_usd, 2)
                elif currency == "CNY":
                    price = round(price / hours_per_month * cny_to_usd, 2)
                if lo <= price <= hi and gpu_label not in seen:
                    seen.add(gpu_label)
                    results.append({"gpu": gpu_label, "price_usd": price, "plan": "按需"})
                    break
            if gpu_label in seen:
                break
    return results


def _scrape_playwright(url: str, name: str, wait_sec: int = 10,
                       wait_until: str = "networkidle") -> list[dict]:
    """用 Playwright 无头浏览器抓取 SPA 页面"""
    if not PLAYWRIGHT_AVAILABLE:
        print(f"  [FAIL] Playwright 未安装")
        return []

    print(f"  [PW] Playwright ({name}) ...")
    results = []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=['--no-sandbox'])
            page = browser.new_page()
            page.set_default_timeout(60000)
            try:
                page.goto(url, timeout=60000, wait_until=wait_until)
            except Exception:
                pass
            page.wait_for_timeout(wait_sec * 1000)

            # 关闭 Cookie 弹窗
            for sel in ["button:has-text('Accept')", "button:has-text('Accept All')",
                         "button:has-text('OK')", "button:has-text('Got it')",
                         "[aria-label='Close']", "#onetrust-accept-btn-handler"]:
                try:
                    btn = page.locator(sel).first
                    if btn.is_visible(timeout=2000):
                        btn.click()
                        page.wait_for_timeout(1500)
                        break
                except Exception:
                    continue

            # 滚动触发懒加载
            try:
                for _ in range(4):
                    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                    page.wait_for_timeout(1000)
                page.evaluate("window.scrollTo(0, 0)")
                page.wait_for_timeout(500)
            except Exception:
                pass

            body_text = page.inner_text("body")
            browser.close()

            # 从文本提取价格
            eur_to_usd = 1.08
            text = ' '.join(body_text.split('\n'))
            for pat in [
                r'(\b[A-Z]\d{3,4}\b|\bRTX\s*\d{4}(?:\s*Ti)?|\bH\d{3}\b|\bB\d{3}\b|\bA\d{3,4}\b|\bL\d{1,2}S?\b|\bT\d\b|\bV\d{3}\b|\bMI\d{3}X?\b).*?\$(\d+\.?\d*)\s*/\s*(?:hr|hour|h)',
                r'\$(\d+\.?\d*)\s*/\s*(?:hr|hour|h).*?(\b[A-Z]\d{3,4}\b|\bRTX\s*\d{4}(?:\s*Ti)?|\bH\d{3}\b|\bB\d{3}\b)',
                r'€(\d+\.?\d*)\s*/\s*(?:hr|hour|h).*?(\b[A-Z]\d{3,4}\b|\bRTX\s*\d{4}(?:\s*Ti)?|\bH\d{3}\b)',
            ]:
                seen = set()
                for m in re.finditer(pat, text, re.IGNORECASE):
                    groups = m.groups()
                    if '$' in pat and '€' not in pat:
                        if groups[0].replace('.', '').replace(',', '').isdigit():
                            price_str, gpu_raw = groups[0], groups[1]
                        else:
                            gpu_raw, price_str = groups[0], groups[1]
                    elif '€' in pat:
                        price_str, gpu_raw = groups[0], groups[1]
                    else:
                        gpu_raw, price_str = groups[0], groups[1]
                    try:
                        price = float(price_str.replace(',', ''))
                        if '€' in m.group(0):
                            price = round(price * eur_to_usd, 2)
                    except ValueError:
                        continue
                    gpu_label = _normalize(gpu_raw)
                    lo, hi = _PRICE_RANGES.get(gpu_label, (0.01, 1000))
                    if lo <= price <= hi and gpu_label not in seen:
                        seen.add(gpu_label)
                        results.append({"gpu": gpu_label, "price_usd": price, "plan": "按需"})
                if results:
                    break
    except Exception as e:
        print(f"  [FAIL] Playwright 异常: {e}")
        return []
    return results


def _generic_scrape(name: str, url: str, use_pw: bool = False,
                    is_eur: bool = False, gpu_list: list[str] = None) -> list[dict]:
    """通用爬虫：先 requests，失败可尝试 Playwright"""
    print(f"[>] {name} ...")

    # requests 模式
    if not use_pw:
        html = _get(url)
        if not html:
            html = _get(url, accept_any_status=True)
        if not html:
            if PLAYWRIGHT_AVAILABLE:
                print(f"  [RETRY] requests 失败，回退 Playwright ...")
                use_pw = True
            else:
                print(f"  [FAIL] 无法访问: {url}")
                return []

    if use_pw:
        results = _scrape_playwright(url, name)
        if results:
            print(f"  [OK] {len(results)} 款 GPU")
            return results
        print(f"  [FAIL] Playwright 未提取到价格")
        return []

    # 多策略提取
    currency = "EUR" if is_eur else "USD"
    eur_to_usd = 1.08
    results = []

    # 策略 1: $X.XX/hr 模式
    text = ' '.join(re.sub(r'<[^>]+>', ' ', html).split('\n'))
    seen = set()
    for pat in [
        r'(\b[A-Z]\d{3,4}\b|\bRTX\s*\d{4}(?:\s*Ti)?|\bH\d{3,4}\b|\bB\d{3}\b|\bA\d{3,4}\b|\bL\d{1,2}S?\b|\bT\d\b|\bV\d{3}\b|\bMI\d{3}X?\b).{0,300}?[\$€]\s*(\d+\.?\d*)\s*/\s*(?:hr|hour|h)',
        r'[\$€]\s*(\d+\.?\d*)\s*/\s*(?:hr|hour|h).{0,300}?(\b[A-Z]\d{3,4}\b|\bRTX\s*\d{4}(?:\s*Ti)?|\bH\d{3,4}\b|\bB\d{3}\b)',
    ]:
        for m in re.finditer(pat, text, re.IGNORECASE):
            groups = m.groups()
            gpu_raw = groups[0] if not groups[0][0].replace('.', '').replace(',', '').isdigit() else groups[1]
            price_str = groups[1] if groups[0] == gpu_raw else groups[0]
            try:
                price = float(price_str.replace(',', ''))
            except ValueError:
                continue
            is_eur_price = '€' in m.group(0)
            if is_eur_price:
                price = round(price * eur_to_usd, 2)
            gpu_label = _normalize(gpu_raw)
            lo, hi = _PRICE_RANGES.get(gpu_label, (0.01, 1000))
            if lo <= price <= hi and gpu_label not in seen:
                seen.add(gpu_label)
                results.append({"gpu": gpu_label, "price_usd": price, "plan": "市场价"})

    # 策略 2: HTML table 提取
    if not results:
        for row_m in re.finditer(r'<tr[^>]*>(.*?)</tr>', html, re.DOTALL | re.IGNORECASE):
            cells = row_m.group(1)
            th_m = re.search(r'<th[^>]*>(.*?)</th>', cells, re.DOTALL | re.IGNORECASE)
            if not th_m:
                continue
            gpu_text = re.sub(r'<[^>]+>', '', th_m.group(1)).strip()
            for td_m in re.finditer(r'<td[^>]*>(.*?)</td>', cells, re.DOTALL | re.IGNORECASE):
                td_text = re.sub(r'<[^>]+>', '', td_m.group(1)).strip()
                p_m = re.search(r'[\$€](\d+\.?\d*)\s*/\s*(?:hr|hour|h)?', td_text)
                if not p_m:
                    continue
                try:
                    price = float(p_m.group(1))
                except ValueError:
                    continue
                is_eur_price = '€' in p_m.group(0)
                if is_eur_price:
                    price = round(price * eur_to_usd, 2)
                gpu_label = _normalize(gpu_text)
                lo, hi = _PRICE_RANGES.get(gpu_label, (0.01, 1000))
                if lo <= price <= hi and gpu_label not in seen:
                    seen.add(gpu_label)
                    results.append({"gpu": gpu_label, "price_usd": price, "plan": "按需"})

    if results:
        print(f"  [OK] {len(results)} 款 GPU")
        return results

    # requests 失败，回退 Playwright
    if PLAYWRIGHT_AVAILABLE:
        print(f"  [RETRY] 文本提取失败，回退 Playwright ...")
        results = _scrape_playwright(url, name)
        if results:
            print(f"  [OK] {len(results)} 款 GPU (Playwright)")
            return results

    print(f"  [FAIL] 未能提取价格")
    return []


# ============================================================
# 专用爬虫函数
# ============================================================

# --- 北美平台 ---

def scrape_akamai_linode():
    """Akamai Linode: https://www.linode.com/pricing/#compute-gpu"""
    return _generic_scrape("Akamai Linode", "https://www.linode.com/pricing/#compute-gpu")

def scrape_phoenixnap():
    """PhoenixNAP: https://phoenixnap.com/gpu-hosting"""
    return _generic_scrape("PhoenixNAP", "https://phoenixnap.com/gpu-hosting", use_pw=True)

def scrape_equinix_metal():
    """Equinix Metal: GPU 服务器规格页面 — 需要联系销售获取价格"""
    print("[>] Equinix Metal ...")
    print("  [i]️ 企业销售模式，无公开小时价格（参考: metal.equinix.com/product/servers/）")
    return []  # 企业销售，无公开定价

def scrape_quadranet():
    """QuadraNet: https://quadranet.com/gpu-dedicated-servers"""
    return _generic_scrape("QuadraNet", "https://quadranet.com/gpu-dedicated-servers")

def scrape_psychz():
    """Psychz: https://www.psychz.net/"""
    return _generic_scrape("Psychz", "https://www.psychz.net/", use_pw=True)

def scrape_turnkey_internet():
    """TurnKey Internet: https://turnkeyinternet.net/gpu-dedicated-server/"""
    return _generic_scrape("TurnKey Internet", "https://turnkeyinternet.net/gpu-dedicated-server/")

def scrape_dedicated_com():
    """Dedicated.com: https://dedicated.com/dedicated-servers/gpu"""
    return _generic_scrape("Dedicated.com", "https://dedicated.com/dedicated-servers/gpu")

def scrape_rackspace():
    """Rackspace Technology: https://www.rackspace.com/cloud/gpu"""
    return _generic_scrape("Rackspace Technology", "https://www.rackspace.com/cloud/gpu", use_pw=True)

def scrape_nvidia_dgx_cloud():
    """NVIDIA DGX Cloud: 企业全托管 AI 超级计算云"""
    print("[>] NVIDIA DGX Cloud ...")
    print("  [i]️ 企业销售模式，起价 ~$37,000/月/集群（无公开小时价格）")
    return []

def scrape_cirrascale():
    """Cirrascale: https://www.cirrascale.com/cloud-services/"""
    return _generic_scrape("Cirrascale", "https://www.cirrascale.com/cloud-services/", use_pw=True)

def scrape_applied_digital():
    """Applied Digital: 企业 GPU 托管"""
    print("[>] Applied Digital ...")
    print("  [i]️ 企业定制 GPU 托管，无公开定价页面")
    return []

def scrape_rescale():
    """Rescale: https://www.rescale.com/pricing/"""
    return _generic_scrape("Rescale", "https://www.rescale.com/pricing/", use_pw=True)

def scrape_databricks():
    """Databricks: ML 平台，GPU 集群通过云合作伙伴提供（AWS/Azure/GCP）"""
    print("[>] Databricks ...")
    print("  [i]️ GPU 通过 AWS/Azure/GCP 提供（DBU 定价模式，非 GPU 小时定价）")
    return []

def scrape_anyscale():
    """Anyscale: Ray ML 平台"""
    print("[>] Anyscale ...")
    print("  [i]️ GPU 通过 AWS/GCP 提供，按 Ray 任务计费")
    return []

def scrape_saturn_cloud():
    """Saturn Cloud: https://saturncloud.io/pricing/"""
    return _generic_scrape("Saturn Cloud", "https://saturncloud.io/pricing/")

def scrape_coiled():
    """Coiled: 托管 Dask 服务"""
    print("[>] Coiled ...")
    print("  [i]️ GPU 通过 AWS/GCP 提供，按 Dask worker 计费")
    return []

def scrape_modal():
    """Modal: https://modal.com/pricing — 无服务器 GPU"""
    return _generic_scrape("Modal", "https://modal.com/pricing")

def scrape_replicate():
    """Replicate: https://replicate.com/pricing — ML 模型推理"""
    return _generic_scrape("Replicate", "https://replicate.com/pricing")

def scrape_fireworks_ai():
    """Fireworks.ai: https://fireworks.ai/pricing — 生成式 AI 推理"""
    return _generic_scrape("Fireworks.ai", "https://fireworks.ai/pricing")

def scrape_together_ai():
    """Together AI: https://www.together.ai/pricing"""
    return _generic_scrape("Together AI", "https://www.together.ai/pricing")

def scrape_octoml():
    """OctoML (OctoAI): 已被 NVIDIA 收购"""
    print("[>] OctoML (OctoAI) ...")
    print("  [i]️ 已被 NVIDIA 收购，原独立定价页面可能不再更新")
    return _generic_scrape("OctoML (OctoAI)", "https://octoml.ai/pricing/")

def scrape_bentoml():
    """BentoML (BentoCloud): https://www.bentoml.com/pricing"""
    return _generic_scrape("BentoML (BentoCloud)", "https://www.bentoml.com/pricing")

def scrape_deepnote():
    """Deepnote: https://deepnote.com/pricing — 协作笔记本"""
    return _generic_scrape("Deepnote", "https://deepnote.com/pricing")

def scrape_codeocean():
    """CodeOcean: https://codeocean.com/pricing"""
    return _generic_scrape("CodeOcean", "https://codeocean.com/pricing", use_pw=True)

def scrape_google_colab():
    """Google Colab: https://colab.research.google.com/signup"""
    print("[>] Google Colab ...")
    html = _get("https://colab.research.google.com/signup")
    if html:
        # Colab 定价: Pro+ $9.99/mo, Pro $49.99/mo — 非 GPU 小时定价
        print("  [i]️ 订阅制（免费/Pro/Pro+），非 GPU 小时定价")
        # 返回 T4/L4/P100/TPU v2 作为可用 GPU 列表（价格为 0 标记为订阅制）
        results = []
        for gpu_name in ["T4", "L4", "P100"]:
            label = _normalize(gpu_name)
            results.append({"gpu": label, "price_usd": 0.0, "plan": "订阅制 (Colab Pro+)"})
        return results
    return []

def scrape_huggingface_endpoints():
    """Hugging Face Inference Endpoints: https://huggingface.co/pricing#endpoints"""
    return _generic_scrape("Hugging Face (Inference Endpoints)",
                           "https://huggingface.co/pricing#endpoints")

# --- 去中心化平台 (无公开小时价格) ---

DECENTRALIZED_NOTE = "[i]️ 去中心化市场，价格由供需动态浮动，无可抓取的固定定价页面"

def scrape_akash_network():
    """Akash Network: 去中心化云计算市场"""
    print("[>] Akash Network ...")
    print(f"  {DECENTRALIZED_NOTE}")
    return []

def scrape_render_network():
    """Render Network: 区块链 GPU 渲染"""
    print("[>] Render Network ...")
    print(f"  {DECENTRALIZED_NOTE}")
    return []

def scrape_mining_rig_rentals():
    """Mining Rig Rentals: P2P 矿机租赁"""
    print("[>] Mining Rig Rentals ...")
    print(f"  [i]️ P2P 矿机租赁市场，无统一 GPU 小时定价")
    return []

def scrape_q_blocks():
    """Q Blocks: 去中心化 GPU 云"""
    print("[>] Q Blocks ...")
    print(f"  {DECENTRALIZED_NOTE}")
    return []

def scrape_golem_network():
    """Golem Network: P2P 算力网络"""
    print("[>] Golem Network ...")
    print(f"  [i]️ P2P 算力网络，GLM 代币结算，无美元定价")
    return []

def scrape_nicehash():
    """NiceHash: 算力市场"""
    print("[>] NiceHash ...")
    print(f"  [i]️ 算力市场（挖矿导向），按哈希率定价，非 GPU 小时定价")
    return []


# --- 欧洲平台 ---

def scrape_t_systems():
    """T-Systems (Open Telekom Cloud): https://open-telekom-cloud.com/en/pricing/"""
    return _generic_scrape("T-Systems (Open Telekom Cloud)",
                           "https://open-telekom-cloud.com/en/pricing/", is_eur=True)

def scrape_aruba_cloud():
    """Aruba Cloud: https://www.arubacloud.com/cloud-pricing.aspx"""
    return _generic_scrape("Aruba Cloud", "https://www.arubacloud.com/cloud-pricing.aspx", is_eur=True)


# --- 日韩平台 ---

def scrape_sakura_internet():
    """Sakura Internet: https://www.sakura.ad.jp/services/cloud/gpu/"""
    return _generic_scrape("Sakura Internet", "https://www.sakura.ad.jp/services/cloud/gpu/",
                           use_pw=True, is_eur=False)

def scrape_iij_gio():
    """IIJ GIO: https://www.iij.ad.jp/biz/gio/"""
    return _generic_scrape("IIJ GIO", "https://www.iij.ad.jp/biz/gio/", use_pw=True)

def scrape_kt_cloud():
    """KT Cloud: https://cloud.kt.com/"""
    return _generic_scrape("KT Cloud", "https://cloud.kt.com/", use_pw=True)

def scrape_naver_cloud():
    """Naver Cloud: https://www.ncloud.com/product/compute/gpu"""
    return _generic_scrape("Naver Cloud", "https://www.ncloud.com/product/compute/gpu",
                           use_pw=True)

def scrape_yandex_cloud():
    """Yandex Cloud: https://cloud.yandex.com/en/services/compute#pricing"""
    return _generic_scrape("Yandex Cloud", "https://cloud.yandex.com/en/services/compute#pricing",
                           use_pw=True)


# --- 中国平台 ---

def scrape_baidu_ai_cloud():
    """百度智能云: https://cloud.baidu.com/product/gpu.html"""
    return _generic_scrape("百度智能云", "https://cloud.baidu.com/product/gpu.html", use_pw=True)

def scrape_jd_cloud():
    """京东云: https://www.jdcloud.com/cn/public/compute/gpu"""
    return _generic_scrape("京东云", "https://www.jdcloud.com/cn/public/compute/gpu", use_pw=True)

def scrape_kingsoft_cloud():
    """金山云: https://www.ksyun.com/post/product/KEC.html"""
    return _generic_scrape("金山云", "https://www.ksyun.com/post/product/KEC.html", use_pw=True)

def scrape_ucloud():
    """UCloud: https://www.ucloud.cn/site/product/uhost.html"""
    return _generic_scrape("UCloud", "https://www.ucloud.cn/site/product/uhost.html", use_pw=True)

def scrape_qingcloud():
    """青云: https://www.qingcloud.com/products/gpu_server/"""
    return _generic_scrape("青云", "https://www.qingcloud.com/products/gpu_server/", use_pw=True)

def scrape_china_mobile_cloud():
    """中国移动云: https://ecloud.10086.cn/home/product-introduction/gpu"""
    return _generic_scrape("中国移动云", "https://ecloud.10086.cn/home/product-introduction/gpu",
                           use_pw=True)

def scrape_ctyun():
    """天翼云: https://www.ctyun.cn/product/gpu"""
    return _generic_scrape("天翼云", "https://www.ctyun.cn/product/gpu", use_pw=True)

def scrape_cucloud():
    """联通云: https://www.cucloud.cn/product/gpu.html"""
    return _generic_scrape("联通云", "https://www.cucloud.cn/product/gpu.html", use_pw=True)

def scrape_inspur_cloud():
    """浪潮云: https://cloud.inspur.com/product/gpu/"""
    return _generic_scrape("浪潮云", "https://cloud.inspur.com/product/gpu/", use_pw=True)

def scrape_paratera():
    """并行科技: https://www.paratera.com/"""
    return _generic_scrape("并行科技", "https://www.paratera.com/", use_pw=True)

def scrape_videopp_ai_cloud():
    """极视角: https://www.videopuzzles.com/"""
    return _generic_scrape("极视角", "https://www.videopuzzles.com/", use_pw=True)


# --- 中国超算中心 (无公开 GPU 小时定价) ---

SUPERCOMPUTING_NOTE = "[i]️ 国家级/省级超算中心，需申请账号（非公开 GPU 小时租赁市场）"

def _sc_ref(name: str):
    """超算中心参考条目 — 无公开定价"""
    print(f"[>] {name} ...")
    print(f"  {SUPERCOMPUTING_NOTE}")
    return []

def scrape_pengcheng_cloud_brain(): return _sc_ref("鹏城云脑")
def scrape_zhejiang_lab(): return _sc_ref("之江实验室")
def scrape_nscc_sz(): return _sc_ref("国家超算深圳中心 (NSCC-SZ)")
def scrape_nscc_gz(): return _sc_ref("国家超算广州中心 (NSCC-GZ)")
def scrape_nscc_tj(): return _sc_ref("国家超算天津中心 (NSCC-TJ)")
def scrape_nscc_wx(): return _sc_ref("国家超算无锡中心 (NSCC-WX)")
def scrape_sscs(): return _sc_ref("上海超算中心 (SSCS)")
def scrape_blsc(): return _sc_ref("北京超级云计算中心 (BLSC)")
def scrape_hefei_acc(): return _sc_ref("合肥先进计算中心 (Hefei ACC)")


# ============================================================
# 扩展平台注册表
# 格式: (平台名, URL, 是否需要 Playwright)
# ============================================================

EXTRA_PLATFORMS = [
    # ============ 北美 — 独立 GPU 云 ============
    ("Akamai Linode",           "https://www.linode.com/pricing/#compute-gpu",     False),
    ("PhoenixNAP",              "https://phoenixnap.com/gpu-hosting",              True),
    ("Equinix Metal",           "https://metal.equinix.com/product/servers/",      False),
    ("QuadraNet",               "https://quadranet.com/gpu-dedicated-servers",      False),
    ("Psychz",                  "https://www.psychz.net/",                          True),
    ("TurnKey Internet",        "https://turnkeyinternet.net/gpu-dedicated-server/", False),
    ("Dedicated.com",           "https://dedicated.com/dedicated-servers/gpu",      False),
    ("Rackspace Technology",    "https://www.rackspace.com/cloud/gpu",              True),
    ("NVIDIA DGX Cloud",        "https://www.nvidia.com/en-us/data-center/dgx-cloud/", False),
    ("Cirrascale",              "https://www.cirrascale.com/cloud-services/",       True),
    ("Applied Digital",         "https://www.applieddigital.com/",                  False),
    ("Rescale",                 "https://www.rescale.com/pricing/",                 True),
    ("SabrePC",                 "https://www.sabrepc.com/hpc-cloud",                True),  # 已在 EXTENDED 中，此处重复注册会被跳过

    # ============ 北美 — ML/SaaS 平台（按 GPU 小时计费） ============
    ("Databricks",              "https://www.databricks.com/product/pricing",      True),
    ("Anyscale",                "https://www.anyscale.com/pricing",                True),
    ("Saturn Cloud",            "https://saturncloud.io/pricing/",                 False),
    ("Coiled",                  "https://www.coiled.io/pricing",                   False),
    ("Modal",                   "https://modal.com/pricing",                       False),
    ("Replicate",               "https://replicate.com/pricing",                   False),
    ("Fireworks.ai",            "https://fireworks.ai/pricing",                    False),
    ("Together AI",             "https://www.together.ai/pricing",                 False),
    ("OctoML (OctoAI)",         "https://octoml.ai/pricing/",                      False),
    ("BentoML (BentoCloud)",    "https://www.bentoml.com/pricing",                 False),
    ("Deepnote",                "https://deepnote.com/pricing",                    False),
    ("CodeOcean",               "https://codeocean.com/pricing",                   True),
    ("Google Colab",            "https://colab.research.google.com/signup",        False),
    ("Hugging Face (Inference Endpoints)", "https://huggingface.co/pricing#endpoints", False),

    # ============ 北美/欧洲 — 去中心化/P2P 平台 ============
    ("Akash Network",           "https://akash.network/pricing/",                  False),
    ("Render Network",          "https://rendertoken.com/",                        False),
    ("Mining Rig Rentals",      "https://www.miningrigrentals.com/",               False),
    ("Q Blocks",                "https://qblocks.cloud/",                           False),
    ("Golem Network",           "https://www.golem.network/",                      False),
    ("NiceHash",                "https://www.nicehash.com/pricing",                False),

    # ============ 欧洲 ============
    ("T-Systems (Open Telekom Cloud)", "https://open-telekom-cloud.com/en/pricing/", True),
    ("Aruba Cloud",             "https://www.arubacloud.com/cloud-pricing.aspx",    False),

    # ============ 日韩 ============
    ("Sakura Internet",         "https://www.sakura.ad.jp/services/cloud/gpu/",    True),
    ("IIJ GIO",                 "https://www.iij.ad.jp/biz/gio/",                  True),
    ("KT Cloud",                "https://cloud.kt.com/",                           True),
    ("Naver Cloud",             "https://www.ncloud.com/product/compute/gpu",      True),
    ("Yandex Cloud",            "https://cloud.yandex.com/en/services/compute#pricing", True),

    # ============ 中国 ============
    ("百度智能云",               "https://cloud.baidu.com/product/gpu.html",        True),
    ("京东云",                   "https://www.jdcloud.com/cn/public/compute/gpu",   True),
    ("金山云",                   "https://www.ksyun.com/post/product/KEC.html",     True),
    ("UCloud",                  "https://www.ucloud.cn/site/product/uhost.html",    True),
    ("青云",                     "https://www.qingcloud.com/products/gpu_server/",   True),
    ("中国移动云",               "https://ecloud.10086.cn/home/product-introduction/gpu", True),
    ("天翼云",                   "https://www.ctyun.cn/product/gpu",                True),
    ("联通云",                   "https://www.cucloud.cn/product/gpu.html",          True),
    ("浪潮云",                   "https://cloud.inspur.com/product/gpu/",            True),
    ("并行科技",                 "https://www.paratera.com/",                        True),
    ("极视角",                   "https://www.videopuzzles.com/",                    True),

    # ============ 中国超算中心 (参考用途) ============
    ("鹏城云脑 (Pengcheng Cloud Brain)", "https://cloudbrain.pcl.ac.cn/",         False),
    ("之江实验室 (Zhejiang Lab)",        "https://www.zhejianglab.com/",            False),
    ("国家超算深圳中心 (NSCC-SZ)",       "http://www.nsccsz.gov.cn/",               False),
    ("国家超算广州中心 (NSCC-GZ)",       "https://www.nscc-gz.cn/",                 False),
    ("国家超算天津中心 (NSCC-TJ)",       "https://nscc-tj.cn/",                     False),
    ("国家超算无锡中心 (NSCC-WX)",       "http://www.nsccwx.cn/",                   False),
    ("上海超算中心 (SSCS)",             "https://www.sscs.cn/",                    False),
    ("北京超级云计算中心 (BLSC)",       "https://www.blsc.cn/",                     False),
    ("合肥先进计算中心 (Hefei ACC)",    "http://www.hpcc.ustc.edu.cn/",             False),
]

# ============================================================
# 定价 URL 映射
# ============================================================

EXTRA_PRICING_URLS = {
    # 北美 — 独立 GPU 云
    "Akamai Linode":            "https://www.linode.com/pricing/#compute-gpu",
    "PhoenixNAP":               "https://phoenixnap.com/gpu-hosting",
    "Equinix Metal":            "https://metal.equinix.com/product/servers/",
    "QuadraNet":                "https://quadranet.com/gpu-dedicated-servers",
    "Psychz":                   "https://www.psychz.net/",
    "TurnKey Internet":         "https://turnkeyinternet.net/gpu-dedicated-server/",
    "Dedicated.com":            "https://dedicated.com/dedicated-servers/gpu",
    "Rackspace Technology":     "https://www.rackspace.com/cloud/gpu",
    "NVIDIA DGX Cloud":         "https://www.nvidia.com/en-us/data-center/dgx-cloud/",
    "Cirrascale":               "https://www.cirrascale.com/cloud-services/",
    "Applied Digital":          "https://www.applieddigital.com/",
    "Rescale":                  "https://www.rescale.com/pricing/",
    # 北美 — ML/SaaS
    "Databricks":               "https://www.databricks.com/product/pricing",
    "Anyscale":                 "https://www.anyscale.com/pricing",
    "Saturn Cloud":             "https://saturncloud.io/pricing/",
    "Coiled":                   "https://www.coiled.io/pricing",
    "Modal":                    "https://modal.com/pricing",
    "Replicate":                "https://replicate.com/pricing",
    "Fireworks.ai":             "https://fireworks.ai/pricing",
    "Together AI":              "https://www.together.ai/pricing",
    "OctoML (OctoAI)":          "https://octoml.ai/pricing/",
    "BentoML (BentoCloud)":     "https://www.bentoml.com/pricing",
    "Deepnote":                 "https://deepnote.com/pricing",
    "CodeOcean":                "https://codeocean.com/pricing",
    "Google Colab":             "https://colab.research.google.com/signup",
    "Hugging Face (Inference Endpoints)": "https://huggingface.co/pricing#endpoints",
    # 去中心化
    "Akash Network":            "https://akash.network/pricing/",
    "Render Network":           "https://rendertoken.com/",
    "Mining Rig Rentals":       "https://www.miningrigrentals.com/",
    "Q Blocks":                 "https://qblocks.cloud/",
    "Golem Network":            "https://www.golem.network/",
    "NiceHash":                 "https://www.nicehash.com/pricing",
    # 欧洲
    "T-Systems (Open Telekom Cloud)": "https://open-telekom-cloud.com/en/pricing/",
    "Aruba Cloud":              "https://www.arubacloud.com/cloud-pricing.aspx",
    # 日韩
    "Sakura Internet":          "https://www.sakura.ad.jp/services/cloud/gpu/",
    "IIJ GIO":                  "https://www.iij.ad.jp/biz/gio/",
    "KT Cloud":                 "https://cloud.kt.com/",
    "Naver Cloud":              "https://www.ncloud.com/product/compute/gpu",
    "Yandex Cloud":             "https://cloud.yandex.com/en/services/compute#pricing",
    # 中国
    "百度智能云":                "https://cloud.baidu.com/product/gpu.html",
    "京东云":                    "https://www.jdcloud.com/cn/public/compute/gpu",
    "金山云":                    "https://www.ksyun.com/post/product/KEC.html",
    "UCloud":                   "https://www.ucloud.cn/site/product/uhost.html",
    "青云":                      "https://www.qingcloud.com/products/gpu_server/",
    "中国移动云":                "https://ecloud.10086.cn/home/product-introduction/gpu",
    "天翼云":                    "https://www.ctyun.cn/product/gpu",
    "联通云":                    "https://www.cucloud.cn/product/gpu.html",
    "浪潮云":                    "https://cloud.inspur.com/product/gpu/",
    "并行科技":                  "https://www.paratera.com/",
    "极视角":                    "https://www.videopuzzles.com/",
    # 中国超算中心
    "鹏城云脑 (Pengcheng Cloud Brain)": "https://cloudbrain.pcl.ac.cn/",
    "之江实验室 (Zhejiang Lab)":        "https://www.zhejianglab.com/",
    "国家超算深圳中心 (NSCC-SZ)":       "http://www.nsccsz.gov.cn/",
    "国家超算广州中心 (NSCC-GZ)":       "https://www.nscc-gz.cn/",
    "国家超算天津中心 (NSCC-TJ)":       "https://nscc-tj.cn/",
    "国家超算无锡中心 (NSCC-WX)":       "http://www.nsccwx.cn/",
    "上海超算中心 (SSCS)":             "https://www.sscs.cn/",
    "北京超级云计算中心 (BLSC)":       "https://www.blsc.cn/",
    "合肥先进计算中心 (Hefei ACC)":    "http://www.hpcc.ustc.edu.cn/",
}


# ============================================================
# 定制爬虫映射 (平台名 → scraping 函数)
# ============================================================

# 对于不需要特殊 cookie/登录即可爬取的平台，用 _make_generic 包装
def _make_generic(name, url, use_pw=False, is_eur=False):
    """返回一个闭包函数（而非函数调用结果），供 custom_scrapers 延迟调用"""
    def _fn():
        return _generic_scrape(name, url, use_pw=use_pw, is_eur=is_eur)
    _fn.__name__ = f"scrape_{name.replace(' ', '_').replace('(', '').replace(')', '')}"
    return _fn

# 只包含需要特殊逻辑的平台（每个值必须是 (callable, callable) 或 (None, callable)）
EXTRA_CUSTOM_SCRAPERS = {
    # --- 有专用爬虫函数的平台 ---
    "Akamai Linode":            (scrape_akamai_linode, scrape_akamai_linode),
    "PhoenixNAP":               (None, _make_generic("PhoenixNAP", "https://phoenixnap.com/gpu-hosting", use_pw=True)),
    "Equinix Metal":            (scrape_equinix_metal, scrape_equinix_metal),
    "QuadraNet":                (scrape_quadranet, scrape_quadranet),
    "Psychz":                   (None, _make_generic("Psychz", "https://www.psychz.net/", use_pw=True)),
    "TurnKey Internet":         (scrape_turnkey_internet, scrape_turnkey_internet),
    "Dedicated.com":            (scrape_dedicated_com, scrape_dedicated_com),
    "Rackspace Technology":     (None, _make_generic("Rackspace Technology", "https://www.rackspace.com/cloud/gpu", use_pw=True)),
    "NVIDIA DGX Cloud":         (scrape_nvidia_dgx_cloud, scrape_nvidia_dgx_cloud),
    "Cirrascale":               (None, _make_generic("Cirrascale", "https://www.cirrascale.com/cloud-services/", use_pw=True)),
    "Applied Digital":          (scrape_applied_digital, scrape_applied_digital),
    "Rescale":                  (None, _make_generic("Rescale", "https://www.rescale.com/pricing/", use_pw=True)),
    # ML/SaaS 平台
    "Databricks":               (scrape_databricks, scrape_databricks),
    "Anyscale":                 (scrape_anyscale, scrape_anyscale),
    "Saturn Cloud":             (scrape_saturn_cloud, scrape_saturn_cloud),
    "Coiled":                   (scrape_coiled, scrape_coiled),
    "Modal":                    (scrape_modal, scrape_modal),
    "Replicate":                (scrape_replicate, scrape_replicate),
    "Fireworks.ai":             (scrape_fireworks_ai, scrape_fireworks_ai),
    "Together AI":              (scrape_together_ai, scrape_together_ai),
    "OctoML (OctoAI)":          (scrape_octoml, scrape_octoml),
    "BentoML (BentoCloud)":     (scrape_bentoml, scrape_bentoml),
    "Deepnote":                 (scrape_deepnote, scrape_deepnote),
    "CodeOcean":                (None, _make_generic("CodeOcean", "https://codeocean.com/pricing", use_pw=True)),
    "Google Colab":             (scrape_google_colab, scrape_google_colab),
    "Hugging Face (Inference Endpoints)": (scrape_huggingface_endpoints, scrape_huggingface_endpoints),
    # 去中心化平台
    "Akash Network":            (scrape_akash_network, scrape_akash_network),
    "Render Network":           (scrape_render_network, scrape_render_network),
    "Mining Rig Rentals":       (scrape_mining_rig_rentals, scrape_mining_rig_rentals),
    "Q Blocks":                 (scrape_q_blocks, scrape_q_blocks),
    "Golem Network":            (scrape_golem_network, scrape_golem_network),
    "NiceHash":                 (scrape_nicehash, scrape_nicehash),
    # 欧洲
    "T-Systems (Open Telekom Cloud)": (scrape_t_systems, scrape_t_systems),
    "Aruba Cloud":              (scrape_aruba_cloud, scrape_aruba_cloud),
    # 日韩
    "Sakura Internet":          (scrape_sakura_internet, scrape_sakura_internet),
    "IIJ GIO":                  (scrape_iij_gio, scrape_iij_gio),
    "KT Cloud":                 (scrape_kt_cloud, scrape_kt_cloud),
    "Naver Cloud":              (scrape_naver_cloud, scrape_naver_cloud),
    "Yandex Cloud":             (scrape_yandex_cloud, scrape_yandex_cloud),
    # 中国
    "百度智能云":                (None, _make_generic("百度智能云", "https://cloud.baidu.com/product/gpu.html", use_pw=True)),
    "京东云":                    (None, _make_generic("京东云", "https://www.jdcloud.com/cn/public/compute/gpu", use_pw=True)),
    "金山云":                    (None, _make_generic("金山云", "https://www.ksyun.com/post/product/KEC.html", use_pw=True)),
    "UCloud":                   (None, _make_generic("UCloud", "https://www.ucloud.cn/site/product/uhost.html", use_pw=True)),
    "青云":                      (None, _make_generic("青云", "https://www.qingcloud.com/products/gpu_server/", use_pw=True)),
    "中国移动云":                (None, _make_generic("中国移动云", "https://ecloud.10086.cn/home/product-introduction/gpu", use_pw=True)),
    "天翼云":                    (None, _make_generic("天翼云", "https://www.ctyun.cn/product/gpu", use_pw=True)),
    "联通云":                    (None, _make_generic("联通云", "https://www.cucloud.cn/product/gpu.html", use_pw=True)),
    "浪潮云":                    (None, _make_generic("浪潮云", "https://cloud.inspur.com/product/gpu/", use_pw=True)),
    "并行科技":                  (None, _make_generic("并行科技", "https://www.paratera.com/", use_pw=True)),
    "极视角":                    (None, _make_generic("极视角", "https://www.videopuzzles.com/", use_pw=True)),
    # 中国超算中心
    "鹏城云脑 (Pengcheng Cloud Brain)": (scrape_pengcheng_cloud_brain, scrape_pengcheng_cloud_brain),
    "之江实验室 (Zhejiang Lab)":        (scrape_zhejiang_lab, scrape_zhejiang_lab),
    "国家超算深圳中心 (NSCC-SZ)":       (scrape_nscc_sz, scrape_nscc_sz),
    "国家超算广州中心 (NSCC-GZ)":       (scrape_nscc_gz, scrape_nscc_gz),
    "国家超算天津中心 (NSCC-TJ)":       (scrape_nscc_tj, scrape_nscc_tj),
    "国家超算无锡中心 (NSCC-WX)":       (scrape_nscc_wx, scrape_nscc_wx),
    "上海超算中心 (SSCS)":             (scrape_sscs, scrape_sscs),
    "北京超级云计算中心 (BLSC)":       (scrape_blsc, scrape_blsc),
    "合肥先进计算中心 (Hefei ACC)":    (scrape_hefei_acc, scrape_hefei_acc),
}


# ============================================================
# 公共接口
# ============================================================

def get_extra_platforms():
    """返回扩展平台列表"""
    return EXTRA_PLATFORMS


def get_extra_pricing_urls():
    """返回扩展定价 URL 映射"""
    return EXTRA_PRICING_URLS


def get_extra_custom_scrapers():
    """返回扩展专用爬虫映射"""
    return EXTRA_CUSTOM_SCRAPERS
