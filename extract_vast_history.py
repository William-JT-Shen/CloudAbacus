#!/usr/bin/env python3
"""
Vast.ai 历史价格数据提取器
============================
用 Playwright 深度抓取 Vast.ai 的内嵌 JSON 数据和 API 响应，
提取 GPU 价格历史记录，生成可用的历史折线图数据。

用法:
  python extract_vast_history.py

输出:
  code/price_history.js  — 多日真实历史数据
"""

import json
import re
import sys
import io
from datetime import datetime, timezone
from pathlib import Path

# Windows 编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("❌ 请先安装 Playwright: pip install playwright && playwright install chromium")
    sys.exit(1)

CODE_DIR = Path(__file__).parent  # 所有文件在项目根目录
OUTPUT_FILE = CODE_DIR / "price_history.js"


def main():
    print("=" * 60)
    print("🔬 Vast.ai 历史价格数据提取器")
    print("=" * 60)

    # 存储所有捕获的数据
    api_responses = []
    embedded_json = []
    page_text = ""

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # === 拦截网络请求，捕获 API 响应 ===
        def on_response(response):
            url = response.url
            if any(kw in url for kw in ['api', 'bundle', 'price', 'history', 'graph', 'machine']):
                try:
                    body = response.text()
                    if len(body) < 500000:  # 跳过太大的响应
                        api_responses.append({"url": url, "body": body[:50000]})
                except Exception:
                    pass

        page.on("response", on_response)

        # === 导航到 vast.ai ===
        print("\n📡 导航到 vast.ai/pricing ...")
        try:
            page.goto("https://vast.ai/pricing", timeout=30000, wait_until="load")
        except Exception:
            pass
        page.wait_for_timeout(8000)  # 等待 JS 完全渲染

        # === 获取完整页面文本 ===
        page_text = page.inner_text("body")
        print(f"   页面文本: {len(page_text):,} 字符")

        # === 提取内嵌 JSON 数据 ===
        html = page.content()
        print(f"   页面 HTML: {len(html):,} 字符")

        # 查找 __NEXT_DATA__
        m = re.search(r'__NEXT_DATA__\s*=\s*(\{.*?\})\s*</script>', html, re.DOTALL)
        if m:
            try:
                embedded_json.append({"source": "__NEXT_DATA__", "data": json.loads(m.group(1))})
                print("   ✅ 找到 __NEXT_DATA__")
            except Exception as e:
                print(f"   ⚠️ __NEXT_DATA__ 解析失败: {e}")

        # 查找 window.__INITIAL_STATE__ 或其他状态对象
        for state_var in ['__INITIAL_STATE__', '__NUXT__', '__APOLLO_STATE__', 'window.__DATA__']:
            m = re.search(rf'{state_var}\s*=\s*(\{{.*?\}});', html, re.DOTALL)
            if m:
                try:
                    embedded_json.append({"source": state_var, "data": json.loads(m.group(1))})
                    print(f"   ✅ 找到 {state_var}")
                except Exception:
                    pass

        # 查找内嵌的 bundles/pricing JSON
        json_like = re.findall(r'(\{(?:[^{}]|\{[^{}]*\})*\})', html)
        for candidate in json_like:
            if '"gpu_name"' in candidate and '"min_bid"' in candidate:
                try:
                    embedded_json.append({"source": "inline_bundle", "data": json.loads(candidate)})
                except Exception:
                    pass
        print(f"   内嵌 JSON 候选: {len(json_like)} 个")

        # === 尝试点击 GPU 详情获取更多数据 ===
        print("\n🔍 尝试提取历史图表数据 ...")

        # 查看是否有点击后显示历史价格的元素
        clickable = page.query_selector_all('[class*="price"], [class*="chart"], [class*="history"], [data-testid*="price"]')
        print(f"   可交互价格元素: {len(clickable)} 个")

        # 尝试查找 chart 相关的 canvas/svg
        charts = page.query_selector_all('canvas, svg, [class*="chart"], [class*="sparkline"], [class*="graph"]')
        print(f"   图表元素 (canvas/svg): {len(charts)} 个")

        # 截图留存
        page.screenshot(path=str(Path(__file__).parent / "vast_screenshot.png"), full_page=False)
        print("   📸 已截图: vast_screenshot.png")

        browser.close()

    # === 分析捕获的数据 ===
    print("\n" + "=" * 60)
    print("📊 分析捕获数据 ...")
    print(f"   API 响应: {len(api_responses)} 个")
    for r in api_responses:
        print(f"     - {r['url'][:100]} ({len(r['body']):,} bytes)")

    print(f"   内嵌 JSON: {len(embedded_json)} 个")
    for e in embedded_json:
        print(f"     - {e['source']}")

    # === 从 API 响应和内嵌数据中提取历史价格 ===
    history_data = {"snapshots": []}
    today_str = datetime.now().strftime("%Y-%m-%d")

    # 尝试从 API 或内嵌 JSON 提取历史价格
    all_price_entries = []

    # 1. 分析 API 响应
    for resp in api_responses:
        body = resp["body"]
        # 查找价格相关的 JSON
        try:
            if body.strip().startswith('[') or body.strip().startswith('{'):
                data = json.loads(body)
                if isinstance(data, list):
                    for item in data[:100]:
                        if isinstance(item, dict) and 'gpu_name' in item:
                            gpu = item.get('gpu_name', '')
                            price = float(item.get('min_bid', item.get('price', 0)))
                            if price > 0:
                                all_price_entries.append({"gpu": gpu, "price": price, "date": today_str})
        except Exception:
            pass

        # 从非 JSON 文本中提取 GPU 价格
        gpu_price_pairs = re.findall(
            r'("gpu_name"|"name"|"gpu"|"model")\s*:\s*"([^"]+)".{0,300}?("min_bid"|"price"|"dph"|"rate")\s*:\s*([\d.]+)',
            body, re.IGNORECASE
        )
        for _, gpu_raw, _, price_raw in gpu_price_pairs:
            try:
                price = float(price_raw)
                if 0.01 < price < 100:
                    all_price_entries.append({"gpu": gpu_raw, "price": price, "date": today_str})
            except ValueError:
                pass

        # 尝试另一种格式：models API 的模板数据
        models = re.findall(r'"name"\s*:\s*"((?:RTX|Tesla|GeForce|A100|H100|Titan|Radeon|RX)[^"]*)"', body)
        prices_from_models = re.findall(r'"dph"\s*:\s*([\d.]+)', body)  # dollars per hour
        if models and len(prices_from_models) >= len(models):
            for i, model in enumerate(models[:len(prices_from_models)]):
                try:
                    p = float(prices_from_models[i])
                    if 0.01 < p < 100:
                        all_price_entries.append({"gpu": model.strip(), "price": p, "date": today_str})
                except ValueError:
                    pass

    # 2. 从内嵌 JSON 提取
    for emb in embedded_json:
        data = emb["data"]
        # 递归搜索包含 gpu_name/min_bid 的对象
        def find_gpu_prices(obj, path=""):
            if isinstance(obj, dict):
                if 'gpu_name' in obj and ('min_bid' in obj or 'price' in obj or 'dph' in obj):
                    gpu = obj['gpu_name']
                    price = float(obj.get('min_bid', obj.get('price', obj.get('dph', 0))))
                    if price > 0:
                        all_price_entries.append({"gpu": str(gpu), "price": price, "date": today_str})
                # 递归搜索
                for k, v in obj.items():
                    if k in ['gpu_name', 'min_bid', 'price', 'dph', 'gpu', 'bundles', 'machines', 'offers']:
                        find_gpu_prices(v, f"{path}.{k}")
                    elif isinstance(v, (dict, list)):
                        find_gpu_prices(v, path)
            elif isinstance(obj, list):
                for i, item in enumerate(obj[:200]):  # 限制搜索深度
                    find_gpu_prices(item, f"{path}[{i}]")
        find_gpu_prices(data)

    # === 3. 从已有 pricing_live.js 和 pricing.js 读取今日真实价格 ===
    if not all_price_entries:
        for js_file in ["pricing_live.js", "pricing.js"]:
            fpath = CODE_DIR / js_file
            if not fpath.exists():
                continue
            live_text = fpath.read_text(encoding="utf-8")
            # 解析 GPU 类别块: "GPU_NAME": [ { "platform": "X", "price_usd": Y }, ... ]
            category_pattern = r'"((?:NVIDIA|AMD|华为|百度|无服务器|去中心化|裸金属|中国云|日韩云|其他|中国超算)[^"]*)"\s*:\s*\[(.*?)\](?=\s*[,}])'
            for cat_match in re.finditer(category_pattern, live_text, re.DOTALL):
                gpu_name = cat_match.group(1)
                block = cat_match.group(2)
                # 提取每个 entry
                for entry_match in re.finditer(r'\{\s*"platform":\s*"([^"]+)"[^}]*"price_usd":\s*([\d.]+)', block):
                    plat = entry_match.group(1)
                    try:
                        price = float(entry_match.group(2))
                        if 0.01 < price < 100:
                            all_price_entries.append({"gpu": gpu_name, "platform": plat, "price": price, "date": today_str})
                    except ValueError:
                        pass
            if all_price_entries:
                print(f"   ✅ 从 {js_file} 读取到 {len(all_price_entries)} 条今日价格")
                break

    # === 基于已有数据生成多日历史 ===
    print(f"\n   价格条目: {len(all_price_entries)} 条")

    if all_price_entries:
        # 按 GPU+Platform 分组
        gpu_plat_groups = {}
        for entry in all_price_entries:
            gpu = normalize_label(entry["gpu"])
            plat = entry.get("platform", "Unknown")
            key = (gpu, plat)
            if key not in gpu_plat_groups:
                gpu_plat_groups[key] = []
            gpu_plat_groups[key].append(entry)

        # 每组取最低价
        today_prices = {}
        for (gpu, plat), entries in gpu_plat_groups.items():
            today_prices[(gpu, plat)] = min(e["price"] for e in entries)

        print(f"   今日价格条目: {len(today_prices)} 个")
        for (gpu, plat), price in sorted(today_prices.items(), key=lambda x: x[1])[:10]:
            print(f"     {gpu[:40]:40s} | {plat:25s} | ${price:.2f}")

        # === 仅追加今日真实数据，不生成模拟历史 ===
        # 读取现有历史
        existing = {"snapshots": []}
        if OUTPUT_FILE.exists():
            try:
                raw = OUTPUT_FILE.read_text(encoding="utf-8")
                m = re.search(r'PRICE_HISTORY_DATA\s*=\s*(\{.*\});', raw, re.DOTALL)
                if m:
                    existing = json.loads(m.group(1))
            except Exception:
                pass

        today_str = datetime.now().strftime("%Y-%m-%d")
        today_snap = {"date": today_str, "prices": {}}
        for (gpu, plat), price in today_prices.items():
            if gpu not in today_snap["prices"]:
                today_snap["prices"][gpu] = []
            today_snap["prices"][gpu].append({"platform": plat, "price_usd": price})

        # 替换或追加今日快照
        replaced = False
        for i, s in enumerate(existing["snapshots"]):
            if s["date"] == today_str:
                existing["snapshots"][i] = today_snap
                replaced = True
                break
        if not replaced:
            existing["snapshots"].append(today_snap)

        # 保留 90 天
        if len(existing["snapshots"]) > 90:
            existing["snapshots"] = existing["snapshots"][-90:]

        history_data = existing
        action = "更新" if replaced else "追加"
        n_gpus = len(today_prices)
        print(f"   {action}今日数据: {n_gpus} GPU-平台组合")
        print(f"   历史总计: {len(history_data['snapshots'])} 天 (全部为真实抓取数据)")
    else:
        print("   ⚠️ 未提取到价格数据，保持现有历史不变")
        return 1

    # === 写入文件 ===
    CODE_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("var PRICE_HISTORY_DATA = ")
        json.dump(history_data, f, indent=2, ensure_ascii=False)
        f.write(";\n")

    print(f"\n✅ 输出: {OUTPUT_FILE}")
    print(f"   {len(history_data['snapshots'])} 天历史数据")

    # 也写 JSON 备份
    json_file = CODE_DIR / "price_history.json"
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(history_data, f, indent=2, ensure_ascii=False)
    print(f"   {json_file.name} (备份)")


def normalize_label(raw: str) -> str:
    """规范化 GPU 名称"""
    raw = raw.lower().strip()
    mapping = {
        'h100 sxm': 'NVIDIA H100 (80GB SXM)',
        'h100 pcie': 'NVIDIA H100 (80GB SXM)',
        'h100': 'NVIDIA H100 (80GB SXM)',
        'h200': 'NVIDIA H200',
        'a100 sxm': 'NVIDIA A100 (80GB SXM)',
        'a100 pcie': 'NVIDIA A100 (40GB PCIe)',
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
        'l40s': 'NVIDIA L40S',
        'l40': 'NVIDIA L40S',
        'l4': 'NVIDIA L4',
        'a40': 'NVIDIA A40',
        't4': 'NVIDIA T4',
        'v100': 'NVIDIA V100',
        'p100': 'NVIDIA Tesla P100 / P40',
        'p40': 'NVIDIA Tesla P100 / P40',
        'k80': 'NVIDIA Tesla K80 / M40 / M60',
        'rx 7900 xtx': 'AMD Radeon RX 7900 XTX / 7900 XT',
        'rx 7900 xt': 'AMD Radeon RX 7900 XTX / 7900 XT',
    }
    return mapping.get(raw, raw)


if __name__ == "__main__":
    main()
