# ============================================================
# GPU 租赁可用量爬取 (Vast.ai 公开 API)
# ============================================================

import requests

TIMEOUT = 20
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36")


def _normalize_gpu_name(raw):
    """简化的 GPU 名称规范化 (避免循环导入)"""
    raw = raw.strip()
    mapping = {
        'h100 sxm': 'NVIDIA H100 (80GB SXM)', 'h100': 'NVIDIA H100 (80GB SXM)',
        'h200': 'NVIDIA H200', 'h200 nvl': 'NVIDIA H200',
        'gh200': 'NVIDIA GH200', 'a100': 'NVIDIA A100 (80GB SXM)',
        'a6000': 'NVIDIA RTX 6000 Ada / A6000',
        'rtx 6000 ada': 'NVIDIA RTX 6000 Ada / A6000',
        'rtx pro 6000 s': 'NVIDIA RTX 6000 Ada / A6000',
        'rtx pro 6000 ws': 'NVIDIA RTX 6000 Ada / A6000',
        'rtx 5090': 'RTX 5090', 'rtx 5080': 'RTX 5080',
        'rtx 5070 ti': 'RTX 5070 Ti', 'rtx 5070': 'RTX 5070',
        'rtx 5060 ti': 'RTX 5060 Ti', 'rtx 5060': 'RTX 5060',
        'rtx 4090': 'NVIDIA RTX 4090', 'rtx 4080': 'NVIDIA RTX 4080 / 4080 Super',
        'rtx 4080s': 'NVIDIA RTX 4080 / 4080 Super',
        'rtx 4070s ti': 'NVIDIA RTX 4070 Ti / 4070',
        'rtx 4070 ti': 'NVIDIA RTX 4070 Ti / 4070', 'rtx 4070': 'NVIDIA RTX 4070 Ti / 4070',
        'rtx 4060 ti': 'NVIDIA RTX 4060 Ti',
        'rtx 3090 ti': 'NVIDIA RTX 3090 / 3090 Ti', 'rtx 3090': 'NVIDIA RTX 3090 / 3090 Ti',
        'rtx a5000': 'RTX A4000', 'rtx a4000': 'RTX A4000',
        'rtx 2080 ti': 'NVIDIA RTX 2080 Ti',
        'l40s': 'NVIDIA L40S', 'l4': 'NVIDIA L4', 'a40': 'NVIDIA A40', 't4': 'NVIDIA T4',
        'v100': 'NVIDIA V100', 'tesla v100': 'NVIDIA V100',
        'p100': 'NVIDIA Tesla P100 / P40', 'p40': 'NVIDIA Tesla P100 / P40',
        'k80': 'NVIDIA Tesla K80 / M40 / M60', 'm40': 'NVIDIA Tesla K80 / M40 / M60',
        'b200': 'NVIDIA H200', 'b300': 'NVIDIA H200',
    }
    key = raw.lower().replace('nvidia ', '').replace('geforce ', '')
    return mapping.get(key, raw)


def scrape_vast_availability():
    """从 Vast.ai 公开 API (无需认证) 获取每种 GPU 的可租赁数量。
    返回: { gpu_normalized_name: {machines, total_gpus, rentable_machines, rentable_gpus} }"""
    print("📦 抓取 Vast.ai GPU 租赁可用量 ...")
    try:
        r = requests.get("https://console.vast.ai/api/v0/bundles/",
                         timeout=TIMEOUT, headers={"User-Agent": UA, "Accept": "application/json"})
        if r.status_code != 200:
            print(f"  ⚠️ API 返回 {r.status_code}，跳过")
            return {}
        data = r.json()
        offers = data.get("offers", [])
    except Exception as e:
        print(f"  ⚠️ API 请求失败: {e}")
        return {}

    gpu_stats = {}
    for o in offers:
        gpu_raw = o.get("gpu_name", "").strip()
        num_gpus = int(o.get("num_gpus", 1))
        rentable = o.get("rentable", False)
        if not gpu_raw:
            continue
        gpu_label = _normalize_gpu_name(gpu_raw)
        if gpu_label not in gpu_stats:
            gpu_stats[gpu_label] = {"machines": 0, "total_gpus": 0, "rentable_machines": 0, "rentable_gpus": 0}
        gpu_stats[gpu_label]["machines"] += 1
        gpu_stats[gpu_label]["total_gpus"] += num_gpus
        if rentable:
            gpu_stats[gpu_label]["rentable_machines"] += 1
            gpu_stats[gpu_label]["rentable_gpus"] += num_gpus

    total_m = sum(s["machines"] for s in gpu_stats.values())
    total_g = sum(s["total_gpus"] for s in gpu_stats.values())
    print(f"  ✅ Vast.ai: {total_m} 台机器 / {total_g} 张GPU / {len(gpu_stats)} 种GPU 可租赁")
    return gpu_stats


# 全局可用量数据
_vast_availability = {}


def get_availability_str(platform: str, gpu_label: str) -> str:
    """返回某平台某 GPU 的可用量描述字符串"""
    if platform == "Vast.ai" and _vast_availability:
        gpu_stats = _vast_availability.get(gpu_label, {})
        if gpu_stats:
            m = gpu_stats.get("rentable_machines", gpu_stats.get("machines", 0))
            g = gpu_stats.get("rentable_gpus", gpu_stats.get("total_gpus", 0))
            if m > 0:
                return f"{m}台机/{g}张卡"
    return ""
