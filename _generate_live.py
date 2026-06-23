#!/usr/bin/env python3
"""
Comprehensive pricing_live.js generator.
Runs all scrapers and produces a single output file with all real-time data.
Usage: python _generate_live.py
"""
import sys, json, re, time
from datetime import datetime, timezone
from pathlib import Path

CODE_DIR = Path(__file__).parent
sys.path.insert(0, str(CODE_DIR))

from fetch_prices import (
    get, atomic_write_js, read_existing_js, extract_prices,
    extract_prices_multistrategy, extract_prices_from_text,
    extract_prices_from_js_object, find_between,
    COMMON_GPUS, COMMON_GPUS_EUR, PRICE_RANGES, normalize_gpu_name,
    PLAYWRIGHT_AVAILABLE, scrape_with_playwright, scrape_generic,
    scrape_vast, scrape_vast_playwright,
    scrape_runpod, scrape_lambda, scrape_lambda_playwright,
    scrape_coreweave, scrape_tensordock_dedicated,
    scrape_salad, scrape_hostkey, scrape_upcloud, scrape_hetzner,
    scrape_nexgen_cloud, scrape_cerebrium, scrape_scaleway,
    scrape_cudo_compute, scrape_exoscale,
    scrape_aws, scrape_azure, scrape_gcp,
    scrape_paperspace, scrape_paperspace_playwright,
    scrape_jarvislabs, scrape_datacrunch, scrape_datacrunch_playwright,
    scrape_autodl_playwright, scrape_matpool_playwright,
    scrape_tencent_cloud, scrape_alibaba_cloud_playwright,
    scrape_huawei_cloud_playwright, scrape_volcengine_playwright,
    CORE_PLATFORMS, EXTENDED_PLATFORMS, PRICING_URLS,
    mark_failed, mark_ok, scrape_log
)

OUTPUT_LIVE = CODE_DIR / "pricing_live.js"
fetched_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def run_scraper(name, fn_req, fn_pw=None):
    """Run a scraper, try requests first, then Playwright if available"""
    print(f"[>] {name} ...")
    results = []
    try:
        # Try requests mode first
        if fn_req:
            results = fn_req()
        if not results and fn_pw and PLAYWRIGHT_AVAILABLE:
            print(f"  [PW] requests failed, trying Playwright...")
            results = fn_pw()
        if results:
            print(f"  [OK] {len(results)} GPUs")
        else:
            print(f"  [--] no data")
    except Exception as e:
        print(f"  [ERR] {str(e)[:80]}")
    return results


def main():
    global scrape_log
    scrape_log.clear()
    all_data = {}
    use_pw = "--playwright" in sys.argv

    # ============ DEDICATED SCRAPERS (requests + optional Playwright) ============
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
        "AWS (Amazon EC2)": (scrape_aws, None),
        "Microsoft Azure":  (scrape_azure, None),
        "Google Cloud":     (scrape_gcp, None),
    }

    for name, (fn_req, fn_pw) in dedicated.items():
        results = run_scraper(name, fn_req, fn_pw)
        if results:
            all_data[name] = results
        else:
            scrape_log.setdefault(name, {"status": "failed", "gpu_count": 0, "error": "no data"})

    # ============ GENERIC PLATFORMS (non-Playwright from registry) ============
    EUR_PLATFORMS = {"OVHcloud", "Scaleway", "Genesis Cloud", "NexGen Cloud",
                     "G-Core Labs", "Cherry Servers", "LeaderGPU", "Leaseweb",
                     "Exoscale", "Cudo Compute", "21Cloud", "Servers.com",
                     "Mystic AI", "Hetzner", "Hostkey", "UpCloud"}

    for name, url, needs_pw in CORE_PLATFORMS + EXTENDED_PLATFORMS:
        if name in dedicated:
            continue  # Already handled
        if use_pw and needs_pw:
            results = run_scraper(name, None, lambda n=name, u=url: scrape_with_playwright(u, n))
        elif not needs_pw:
            is_eur = name in EUR_PLATFORMS
            results = run_scraper(name, lambda n=name, u=url, e=is_eur: scrape_generic(n, u, is_eur_platform=e))
        else:
            print(f"[>] {name} ...")
            print(f"  [--] skipped (needs Playwright, use --playwright)")
            scrape_log[name] = {"status": "skipped", "gpu_count": 0, "error": "requires Playwright"}
            continue
        if results:
            all_data[name] = results

    # ============ CHINESE PLATFORMS (Playwright-only) ============
    chinese_platforms = {
        "阿里云":   (None, scrape_alibaba_cloud_playwright),
        "华为云":   (None, scrape_huawei_cloud_playwright),
        "火山引擎": (None, scrape_volcengine_playwright),
        "腾讯云":   (None, scrape_tencent_cloud),
        "Matpool":  (None, scrape_matpool_playwright),
        "AutoDL":   (None, scrape_autodl_playwright),
    }
    if use_pw:
        for name, (fn_req, fn_pw) in chinese_platforms.items():
            results = run_scraper(name, fn_req, fn_pw)
            if results:
                all_data[name] = results
    else:
        for name in chinese_platforms:
            scrape_log[name] = {"status": "skipped", "gpu_count": 0, "error": "Chinese platform, needs Playwright"}

    # ============ GENERATE pricing_live.js ============
    print(f"\n{'='*60}")
    print(f"Generating pricing_live.js from {len(all_data)} platforms...")

    gpu_categories = {}
    for plat_name, gpus in all_data.items():
        for entry in gpus:
            label = entry["gpu"]
            if label not in gpu_categories:
                gpu_categories[label] = []
            pricing_url = PRICING_URLS.get(plat_name, "")
            gpu_categories[label].append({
                "platform": plat_name,
                "price_usd": entry["price_usd"],
                "plan": entry.get("plan", "按需"),
                "country": "", "region": "",
                "note": f"实时抓取 · {fetched_at}",
                "pricing_url": pricing_url,
                "availability": "",
                "source": "scraped"
            })

    # Merge with existing live data for platforms NOT in current scrape
    merged = 0
    if OUTPUT_LIVE.exists():
        try:
            raw = OUTPUT_LIVE.read_text(encoding="utf-8")
            m = re.search(r'GPU_PRICING_LIVE\s*=\s*(\{.*?\});\s*$', raw, re.DOTALL)
            if m:
                existing = json.loads(m.group(1))
                scraped_now = set(all_data.keys())
                for gpu_label, entries in existing.items():
                    if gpu_label not in gpu_categories:
                        gpu_categories[gpu_label] = []
                    for e in entries:
                        if e.get("source") == "scraped" and e["platform"] not in scraped_now:
                            gpu_categories[gpu_label].append(e)
                            merged += 1
        except Exception:
            pass

    # Write
    with open(OUTPUT_LIVE, "w", encoding="utf-8") as f:
        f.write("// 运算盘 · 实时 GPU 价格数据\n")
        f.write(f"// 自动生成于: {fetched_at}\n")
        f.write("// 由 _generate_live.py 生成\n\n")
        f.write(f'var PRICE_FETCHED_AT = "{fetched_at}";\n')
        f.write(f"var PRICE_SCRAPE_SOURCES = {json.dumps(scrape_log, ensure_ascii=False, indent=2)};\n\n")
        f.write("var GPU_PRICING_LIVE = {\n")
        cats = list(gpu_categories.items())
        for i, (label, entries) in enumerate(cats):
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

    total = sum(len(v) for v in all_data.values())
    print(f"Output: {OUTPUT_LIVE.name}")
    print(f"  {len(gpu_categories)} GPU categories, {total} new entries (+{merged} preserved)")
    print(f"  {len(scrape_log)} platforms logged")

    ok_count = sum(1 for v in scrape_log.values() if v["status"] == "ok")
    print(f"  {ok_count}/{len(scrape_log)} platforms successful")


if __name__ == "__main__":
    main()
