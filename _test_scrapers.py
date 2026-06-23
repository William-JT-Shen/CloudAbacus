#!/usr/bin/env python3
"""
Comprehensive scraper test harness.
Tests all platform scrapers from fetch_prices.py and _extra_platforms.py,
reports which work and which fail, and identifies failure patterns.
"""
import sys, json, re, time, os
from pathlib import Path

CODE_DIR = Path(__file__).parent
sys.path.insert(0, str(CODE_DIR))

from fetch_prices import (
    CORE_PLATFORMS, EXTENDED_PLATFORMS, PRICING_URLS,
    scrape_generic, scrape_vast, scrape_runpod, scrape_lambda,
    scrape_coreweave, scrape_tensordock_dedicated,
    scrape_salad, scrape_hostkey, scrape_upcloud, scrape_hetzner,
    scrape_nexgen_cloud, scrape_cerebrium, scrape_scaleway,
    scrape_cudo_compute, scrape_exoscale, scrape_aws, scrape_azure, scrape_gcp,
    scrape_paperspace, scrape_jarvislabs,
    PLAYWRIGHT_AVAILABLE
)

try:
    from _extra_platforms import EXTRA_CUSTOM_SCRAPERS, EXTRA_PLATFORMS
    EXTRA_OK = True
except ImportError:
    EXTRA_OK = False
    EXTRA_CUSTOM_SCRAPERS = {}
    EXTRA_PLATFORMS = []


def test_scraper(name, fn, timeout=30):
    """Test a single scraper function and return result."""
    print(f"  Testing {name}...", end=" ", flush=True)
    try:
        results = fn()
        if results and len(results) > 0:
            gpus = [r['gpu'] for r in results]
            prices = [r['price_usd'] for r in results]
            print(f"OK: {len(results)} GPUs ({', '.join(gpus)})")
            return {"status": "ok", "count": len(results), "gpus": gpus, "prices": prices}
        else:
            print("EMPTY")
            return {"status": "empty", "count": 0, "error": "no results"}
    except Exception as e:
        print(f"ERROR: {e}")
        return {"status": "error", "count": 0, "error": str(e)[:100]}


def main():
    print("=" * 60)
    print("Comprehensive Scraper Test Harness")
    print(f"Playwright: {'AVAILABLE' if PLAYWRIGHT_AVAILABLE else 'NOT AVAILABLE'}")
    print(f"Extra platforms: {'AVAILABLE' if EXTRA_OK else 'NOT AVAILABLE'}")
    print("=" * 60)

    results = {}

    # ---- Core Platforms (requests mode) ----
    print("\n--- CORE PLATFORMS (requests) ---")
    core_scrapers = {
        "Vast.ai": scrape_vast,
        "RunPod": scrape_runpod,
        "Lambda Labs": scrape_lambda,
        "CoreWeave": scrape_coreweave,
        "TensorDock": scrape_tensordock_dedicated,
    }
    for name, fn in core_scrapers.items():
        results[name] = test_scraper(name, fn)

    # ---- Extended platforms with dedicated scrapers ----
    print("\n--- EXTENDED DEDICATED (requests) ---")
    dedicated_scrapers = {
        "Paperspace": scrape_paperspace,
        "JarvisLabs": scrape_jarvislabs,
        "Salad": scrape_salad,
        "Hostkey": scrape_hostkey,
        "UpCloud": scrape_upcloud,
        "Hetzner": scrape_hetzner,
        "NexGen Cloud": scrape_nexgen_cloud,
        "Cerebrium": scrape_cerebrium,
        "Scaleway": scrape_scaleway,
        "Cudo Compute": scrape_cudo_compute,
        "Exoscale": scrape_exoscale,
        "AWS (Amazon EC2)": scrape_aws,
        "Microsoft Azure": scrape_azure,
        "Google Cloud": scrape_gcp,
    }
    for name, fn in dedicated_scrapers.items():
        results[name] = test_scraper(name, fn)

    # ---- Generic platforms (requests mode) ----
    print("\n--- GENERIC PLATFORMS (requests, no Playwright needed) ---")
    GENERIC_REQUESTS = [
        ("OVHcloud", "https://www.ovhcloud.com/en/public-cloud/prices/"),
        ("DigitalOcean", "https://www.digitalocean.com/pricing/gpu-droplets"),
        ("Massed Compute", "https://www.massedcompute.com/pricing"),
        ("Cerebrium", "https://www.cerebrium.ai/pricing"),
    ]
    for name, url in GENERIC_REQUESTS:
        results[name] = test_scraper(name, lambda n=name, u=url: scrape_generic(n, u))

    # ---- Extra platforms (requests mode) ----
    if EXTRA_OK:
        print("\n--- EXTRA PLATFORMS (requests) ---")
        extra_req = [
            ("Akamai Linode", "https://www.linode.com/pricing/#compute-gpu"),
            ("QuadraNet", "https://quadranet.com/gpu-dedicated-servers"),
            ("TurnKey Internet", "https://turnkeyinternet.net/gpu-dedicated-server/"),
            ("Dedicated.com", "https://dedicated.com/dedicated-servers/gpu"),
            ("Saturn Cloud", "https://saturncloud.io/pricing/"),
            ("Modal", "https://modal.com/pricing"),
            ("Replicate", "https://replicate.com/pricing"),
            ("Fireworks.ai", "https://fireworks.ai/pricing"),
            ("Together AI", "https://www.together.ai/pricing"),
            ("BentoML (BentoCloud)", "https://www.bentoml.com/pricing"),
            ("Deepnote", "https://deepnote.com/pricing"),
            ("Hugging Face (Inference Endpoints)", "https://huggingface.co/pricing#endpoints"),
            ("Aruba Cloud", "https://www.arubacloud.com/cloud-pricing.aspx"),
        ]
        for name, url in extra_req:
            results[name] = test_scraper(name, lambda n=name, u=url: scrape_generic(n, u))

    # ---- Summary ----
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    ok = [n for n, r in results.items() if r["status"] == "ok"]
    empty = [n for n, r in results.items() if r["status"] == "empty"]
    error = [n for n, r in results.items() if r["status"] == "error"]

    print(f"OK:     {len(ok)} platforms")
    print(f"Empty:  {len(empty)} platforms")
    print(f"Error:  {len(error)} platforms")

    if ok:
        total_gpus = sum(results[n]["count"] for n in ok)
        print(f"\nSuccessful scrapers produced {total_gpus} total GPU entries")
        for n in ok:
            r = results[n]
            print(f"  {n}: {r['count']} GPUs")

    if empty:
        print(f"\nEmpty results (no prices found):")
        for n in empty:
            print(f"  {n}: {results[n].get('error', 'no data')}")

    if error:
        print(f"\nErrors:")
        for n in error:
            print(f"  {n}: {results[n].get('error', 'unknown')}")

    # Write summary JSON
    with open(CODE_DIR / "_test_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False, default=str)
    print(f"\nResults written to _test_results.json")

    return 0


if __name__ == "__main__":
    main()
