#!/usr/bin/env python3
"""
Fast batch scraper — runs all working scrapers and generates pricing_live.js.
Only runs platforms that can complete quickly (< 30s each).
"""
import sys, json, re
from datetime import datetime, timezone, timedelta
from pathlib import Path

CODE_DIR = Path(__file__).parent
sys.path.insert(0, str(CODE_DIR))

from fetch_prices import (
    get, atomic_write_js, COMMON_GPUS, COMMON_GPUS_EUR, PRICE_RANGES,
    normalize_gpu_name, PLAYWRIGHT_AVAILABLE, scrape_with_playwright,
    scrape_generic, mark_failed, mark_ok, scrape_log,
    # Dedicated requests scrapers
    scrape_vast, scrape_runpod, scrape_lambda, scrape_coreweave,
    scrape_tensordock_dedicated, scrape_salad, scrape_hostkey, scrape_upcloud,
    scrape_hetzner, scrape_nexgen_cloud, scrape_cerebrium, scrape_scaleway,
    scrape_cudo_compute, scrape_exoscale, scrape_aws, scrape_azure, scrape_gcp,
    scrape_paperspace, scrape_jarvislabs, scrape_datacrunch,
    # Playwright scrapers
    scrape_vast_playwright, scrape_lambda_playwright,
    scrape_datacrunch_playwright, scrape_paperspace_playwright,
    # Platform registry
    CORE_PLATFORMS, EXTENDED_PLATFORMS, PRICING_URLS
)

OUTPUT_LIVE = CODE_DIR / "pricing_live.js"
BEIJING_TZ = timezone(timedelta(hours=8))
fetched_at = datetime.now(BEIJING_TZ).strftime("%Y-%m-%d %H:00")

def try_scrape(name, fn_req, fn_pw=None, timeout_sec=60):
    """Try a scraper, with timeout protection"""
    import signal
    results = []
    try:
        if fn_req:
            results = fn_req()
        if not results and fn_pw and PLAYWRIGHT_AVAILABLE:
            print(f"  -> Playwright fallback...")
            results = fn_pw()
    except Exception as e:
        print(f"  ERR: {str(e)[:80]}")
    if results:
        print(f"  OK: {len(results)} GPUs")
        for r in results[:5]:
            print(f"    {r['gpu']}: \${r['price_usd']}/hr")
        if len(results) > 5:
            print(f"    ... and {len(results) - 5} more")
    else:
        print(f"  -- no data")
    return results


def main():
    global scrape_log
    scrape_log.clear()
    all_data = {}

    print("=" * 60)
    print("FAST BATCH SCRAPER")
    print(f"Playwright: {'YES' if PLAYWRIGHT_AVAILABLE else 'NO'}")
    print(f"Time: {fetched_at} (Beijing)")
    print("=" * 60)

    # ====== DEDICATED SCRAPERS (REQUESTS MODE — FAST) ======
    print("\n--- DEDICATED SCRAPERS (requests) ---")
    dedicated = {
        "Vast.ai":      (scrape_vast, scrape_vast_playwright),
        "RunPod":       (scrape_runpod, None),
        "Lambda Labs":  (scrape_lambda, scrape_lambda_playwright),
        "CoreWeave":    (scrape_coreweave, None),
        "TensorDock":   (scrape_tensordock_dedicated, None),
        "Paperspace":   (scrape_paperspace, scrape_paperspace_playwright),
        "JarvisLabs":   (scrape_jarvislabs, None),
        "Salad":        (scrape_salad, None),
        "Hostkey":      (scrape_hostkey, None),
        "UpCloud":      (scrape_upcloud, None),
        "Hetzner":      (scrape_hetzner, None),
        "NexGen Cloud": (scrape_nexgen_cloud, None),
        "Cerebrium":    (scrape_cerebrium, None),
        "Scaleway":     (scrape_scaleway, None),
        "Cudo Compute": (scrape_cudo_compute, None),
        "Exoscale":     (scrape_exoscale, None),
        "DataCrunch":   (scrape_datacrunch, scrape_datacrunch_playwright),
    }
    for name, (fn_req, fn_pw) in dedicated.items():
        print(f"\n[{name}]")
        results = try_scrape(name, fn_req, fn_pw)
        if results:
            all_data[name] = results

    # ====== GENERIC PLATFORMS (requests mode + auto-Playwright-fallback) ======
    print("\n\n--- GENERIC PLATFORMS (requests + auto-PW-fallback) ---")
    EUR_PLATFORMS = {"OVHcloud", "Scaleway", "Genesis Cloud", "NexGen Cloud",
                     "G-Core Labs", "Cherry Servers", "LeaderGPU", "Leaseweb",
                     "Exoscale", "Cudo Compute", "21Cloud", "Servers.com",
                     "Mystic AI", "Hetzner", "Hostkey", "UpCloud"}

    for name, url, needs_pw in CORE_PLATFORMS + EXTENDED_PLATFORMS:
        if name in dedicated:
            continue
        is_eur = name in EUR_PLATFORMS
        print(f"\n[{name}]")
        results = try_scrape(name,
            lambda n=name, u=url, e=is_eur: scrape_generic(n, u, pw_fallback=PLAYWRIGHT_AVAILABLE, is_eur_platform=e))
        if results:
            all_data[name] = results

    # ====== AWS/Azure/GCP API SCRAPERS ======
    print("\n\n--- LARGE CLOUD API SCRAPERS ---")
    cloud_scrapers = {
        "AWS (Amazon EC2)": (scrape_aws, None),
        "Microsoft Azure":  (scrape_azure, None),
        "Google Cloud":     (scrape_gcp, None),
    }
    for name, (fn_req, fn_pw) in cloud_scrapers.items():
        print(f"\n[{name}]")
        results = try_scrape(name, fn_req)
        if results:
            all_data[name] = results

    # ====== GENERATE pricing_live.js ======
    print(f"\n\n{'='*60}")
    print(f"GENERATING pricing_live.js from {len(all_data)} platforms")

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
                "country": "", "region": "",
                "note": f"实时抓取 · {fetched_at} (北京时间)",
                "pricing_url": PRICING_URLS.get(plat_name, ""),
                "availability": "",
                "source": "scraped"
            })

    # Dedup: same platform + GPU → keep lowest price
    for label in gpu_categories:
        seen = {}
        for e in gpu_categories[label]:
            key = e["platform"]
            if key not in seen or e["price_usd"] < seen[key]["price_usd"]:
                seen[key] = e
        gpu_categories[label] = list(seen.values())

    # Write
    with open(OUTPUT_LIVE, "w", encoding="utf-8") as f:
        f.write("// 运算盘 · 实时 GPU 价格数据\n")
        f.write(f"// 自动生成于: {fetched_at} (北京时间)\n")
        f.write("// 由 fetch_prices.py 自动生成\n\n")
        f.write(f'var PRICE_FETCHED_AT = "{fetched_at} (北京时间)";\n')
        f.write(f"var PRICE_SCRAPE_SOURCES = {json.dumps(scrape_log, ensure_ascii=False, indent=2)};\n\n")
        f.write("var GPU_PRICING_LIVE = {\n")
        cats = sorted(gpu_categories.items())
        for i, (label, entries) in enumerate(cats):
            entries.sort(key=lambda x: x["price_usd"])
            f.write(f'  "{label}": [\n')
            for j, e in enumerate(entries):
                comma = "," if j < len(entries) - 1 else ""
                f.write(f'    {{ "platform": "{e["platform"]}", "price_usd": {e["price_usd"]}, '
                        f'"plan": "{e["plan"]}", "country": "{e["country"]}", "region": "{e["region"]}", '
                        f'"note": "{e["note"]}", "pricing_url": "{e["pricing_url"]}", '
                        f'"availability": "{e.get("availability", "")}", "source": "{e["source"]}" }}{comma}\n')
            comma = "," if i < len(cats) - 1 else ""
            f.write(f"  ]{comma}\n")
        f.write("};\n")

    total_new = sum(len(v) for v in all_data.values())
    total_all = sum(len(v) for v in gpu_categories.values())
    ok_count = sum(1 for v in scrape_log.values() if v.get("status") == "ok")

    print(f"\n{'='*60}")
    print(f"COMPLETE: {OUTPUT_LIVE.name}")
    print(f"  Platforms with data: {len(all_data)}")
    print(f"  Successful scrapers: {ok_count}/{len(scrape_log)}")
    print(f"  GPU categories: {len(gpu_categories)}")
    print(f"  Total entries: {total_all}")
    print(f"  Timestamp: {fetched_at} (北京时间)")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
