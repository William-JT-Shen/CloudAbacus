// 运算盘 · 实时 GPU 价格数据
// 自动生成于: 2026-06-16T14:43:53Z
// ⚠️ 由 fetch_prices.py 自动生成，请勿手动编辑

var PRICE_FETCHED_AT = "2026-06-16T14:43:53Z";
var PRICE_SCRAPE_SOURCES = {
  "Vast.ai": {
    "status": "ok",
    "gpu_count": 24
  },
  "RunPod": {
    "status": "ok",
    "gpu_count": 2
  },
  "Lambda Labs": {
    "status": "failed",
    "gpu_count": 0,
    "error": "所有 URL 均未提取到价格数据（SPA 动态加载，可能需要更长的等待时间）"
  },
  "CoreWeave": {
    "status": "failed",
    "gpu_count": 0,
    "error": "未能解析价格数据"
  },
  "TensorDock": {
    "status": "ok",
    "gpu_count": 9
  }
};

var GPU_PRICING_LIVE = {
  "RTX 5090": [
    { "platform": "Vast.ai", "price_usd": 0.44, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-16T14:43:53Z", "pricing_url": "https://vast.ai/pricing", "availability": "共12张", "source": "scraped" }
  ],
  "NVIDIA RTX 4090": [
    { "platform": "Vast.ai", "price_usd": 0.36, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-16T14:43:53Z", "pricing_url": "https://vast.ai/pricing", "availability": "共14张", "source": "scraped" },
    { "platform": "RunPod", "price_usd": 0.34, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-16T14:43:53Z", "pricing_url": "https://www.runpod.io/pricing", "availability": "", "source": "scraped" },
    { "platform": "TensorDock", "price_usd": 0.35, "plan": "GPU起价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-16T14:43:53Z", "pricing_url": "https://www.tensordock.com/cloud-gpus.html", "availability": "", "source": "scraped" }
  ],
  "RTX 5080": [
    { "platform": "Vast.ai", "price_usd": 0.24, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-16T14:43:53Z", "pricing_url": "https://vast.ai/pricing", "availability": "共3张", "source": "scraped" }
  ],
  "RTX 5070 Ti": [
    { "platform": "Vast.ai", "price_usd": 0.15, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-16T14:43:53Z", "pricing_url": "https://vast.ai/pricing", "availability": "共2张", "source": "scraped" }
  ],
  "RTX 5070": [
    { "platform": "Vast.ai", "price_usd": 0.13, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-16T14:43:53Z", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "scraped" }
  ],
  "RTX 5060 Ti": [
    { "platform": "Vast.ai", "price_usd": 0.1, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-16T14:43:53Z", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "scraped" }
  ],
  "RTX 5060": [
    { "platform": "Vast.ai", "price_usd": 0.08, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-16T14:43:53Z", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "scraped" }
  ],
  "NVIDIA RTX 4080 / 4080 Super": [
    { "platform": "Vast.ai", "price_usd": 0.2, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-16T14:43:53Z", "pricing_url": "https://vast.ai/pricing", "availability": "共3张", "source": "scraped" }
  ],
  "NVIDIA RTX 4070 Ti / 4070": [
    { "platform": "Vast.ai", "price_usd": 0.11, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-16T14:43:53Z", "pricing_url": "https://vast.ai/pricing", "availability": "共1张", "source": "scraped" }
  ],
  "NVIDIA RTX 4060 Ti": [
    { "platform": "Vast.ai", "price_usd": 0.1, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-16T14:43:53Z", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "scraped" }
  ],
  "NVIDIA RTX 3090 / 3090 Ti": [
    { "platform": "Vast.ai", "price_usd": 0.2, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-16T14:43:53Z", "pricing_url": "https://vast.ai/pricing", "availability": "共7张", "source": "scraped" },
    { "platform": "TensorDock", "price_usd": 0.2, "plan": "GPU起价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-16T14:43:53Z", "pricing_url": "https://www.tensordock.com/cloud-gpus.html", "availability": "", "source": "scraped" }
  ],
  "NVIDIA RTX 3080 / 3080 Ti": [
    { "platform": "Vast.ai", "price_usd": 0.11, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-16T14:43:53Z", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "scraped" }
  ],
  "NVIDIA RTX 3070 / 3070 Ti": [
    { "platform": "Vast.ai", "price_usd": 0.08, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-16T14:43:53Z", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "scraped" }
  ],
  "NVIDIA RTX 3060 / 3060 Ti": [
    { "platform": "Vast.ai", "price_usd": 0.08, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-16T14:43:53Z", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "scraped" }
  ],
  "RTX 8000": [
    { "platform": "Vast.ai", "price_usd": 0.24, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-16T14:43:53Z", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "scraped" }
  ],
  "NVIDIA RTX 2080 Ti": [
    { "platform": "Vast.ai", "price_usd": 0.07, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-16T14:43:53Z", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "scraped" }
  ],
  "RTX 6000": [
    { "platform": "Vast.ai", "price_usd": 0.63, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-16T14:43:53Z", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "scraped" }
  ],
  "RTX 5880": [
    { "platform": "Vast.ai", "price_usd": 0.48, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-16T14:43:53Z", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "scraped" }
  ],
  "NVIDIA H200": [
    { "platform": "Vast.ai", "price_usd": 3.17, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-16T14:43:53Z", "pricing_url": "https://vast.ai/pricing", "availability": "共36张", "source": "scraped" }
  ],
  "NVIDIA H100 (80GB SXM)": [
    { "platform": "Vast.ai", "price_usd": 2.39, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-16T14:43:53Z", "pricing_url": "https://vast.ai/pricing", "availability": "共2张", "source": "scraped" },
    { "platform": "RunPod", "price_usd": 1.99, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-16T14:43:53Z", "pricing_url": "https://www.runpod.io/pricing", "availability": "", "source": "scraped" },
    { "platform": "TensorDock", "price_usd": 2.25, "plan": "GPU起价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-16T14:43:53Z", "pricing_url": "https://www.tensordock.com/cloud-gpus.html", "availability": "", "source": "scraped" }
  ],
  "NVIDIA A100 (80GB SXM)": [
    { "platform": "Vast.ai", "price_usd": 0.8, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-16T14:43:53Z", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "scraped" },
    { "platform": "TensorDock", "price_usd": 1.8, "plan": "GPU起价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-16T14:43:53Z", "pricing_url": "https://www.tensordock.com/cloud-gpus.html", "availability": "", "source": "scraped" }
  ],
  "NVIDIA RTX 6000 Ada / A6000": [
    { "platform": "Vast.ai", "price_usd": 0.39, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-16T14:43:53Z", "pricing_url": "https://vast.ai/pricing", "availability": "共14张", "source": "scraped" },
    { "platform": "TensorDock", "price_usd": 0.75, "plan": "GPU起价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-16T14:43:53Z", "pricing_url": "https://www.tensordock.com/cloud-gpus.html", "availability": "", "source": "scraped" }
  ],
  "NVIDIA A40": [
    { "platform": "Vast.ai", "price_usd": 0.29, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-16T14:43:53Z", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "scraped" }
  ],
  "RTX 2080": [
    { "platform": "Vast.ai", "price_usd": 0.24, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-16T14:43:53Z", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "scraped" }
  ],
  "NVIDIA A100 (40GB PCIe)": [
    { "platform": "TensorDock", "price_usd": 1.5, "plan": "GPU起价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-16T14:43:53Z", "pricing_url": "https://www.tensordock.com/cloud-gpus.html", "availability": "", "source": "scraped" }
  ],
  "NVIDIA V100": [
    { "platform": "TensorDock", "price_usd": 0.17, "plan": "GPU起价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-16T14:43:53Z", "pricing_url": "https://www.tensordock.com/cloud-gpus.html", "availability": "", "source": "scraped" }
  ],
  "NVIDIA L40S": [
    { "platform": "TensorDock", "price_usd": 0.95, "plan": "GPU起价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-16T14:43:53Z", "pricing_url": "https://www.tensordock.com/cloud-gpus.html", "availability": "", "source": "scraped" }
  ],
  "RTX A4000 16GB": [
    { "platform": "TensorDock", "price_usd": 0.1, "plan": "GPU起价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-16T14:43:53Z", "pricing_url": "https://www.tensordock.com/cloud-gpus.html", "availability": "", "source": "scraped" }
  ]
};
