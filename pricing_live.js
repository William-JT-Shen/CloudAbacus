// 运算盘 · 实时 GPU 价格数据
// 自动生成于: 2026-06-14T03:14:54Z
// ⚠️ 由 fetch_prices.py 自动生成，请勿手动编辑

var PRICE_FETCHED_AT = "2026-06-14T03:14:54Z";
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
    "status": "ok",
    "gpu_count": 4
  },
  "TensorDock": {
    "status": "ok",
    "gpu_count": 6
  }
};

var GPU_PRICING_LIVE = {
  "RTX 5090": [
    { "platform": "Vast.ai", "price_usd": 0.47, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T03:14:54Z", "pricing_url": "https://vast.ai/pricing", "availability": "3台机/3张卡", "source": "scraped" }
  ],
  "NVIDIA RTX 4090": [
    { "platform": "Vast.ai", "price_usd": 0.4, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T03:14:54Z", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "scraped" },
    { "platform": "RunPod", "price_usd": 0.34, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T03:14:54Z", "pricing_url": "https://www.runpod.io/pricing", "availability": "", "source": "scraped" },
    { "platform": "TensorDock", "price_usd": 0.35, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T03:14:54Z", "pricing_url": "https://www.tensordock.com/cloud-gpus.html", "availability": "", "source": "scraped" }
  ],
  "RTX 5080": [
    { "platform": "Vast.ai", "price_usd": 0.25, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T03:14:54Z", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "scraped" }
  ],
  "RTX 5070 Ti": [
    { "platform": "Vast.ai", "price_usd": 0.16, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T03:14:54Z", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "scraped" }
  ],
  "RTX 5070": [
    { "platform": "Vast.ai", "price_usd": 0.13, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T03:14:54Z", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "scraped" }
  ],
  "RTX 5060 Ti": [
    { "platform": "Vast.ai", "price_usd": 0.11, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T03:14:54Z", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "scraped" }
  ],
  "RTX 5060": [
    { "platform": "Vast.ai", "price_usd": 0.09, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T03:14:54Z", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "scraped" }
  ],
  "NVIDIA RTX 4080 / 4080 Super": [
    { "platform": "Vast.ai", "price_usd": 0.24, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T03:14:54Z", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "scraped" }
  ],
  "NVIDIA RTX 4060 Ti": [
    { "platform": "Vast.ai", "price_usd": 0.11, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T03:14:54Z", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "scraped" }
  ],
  "NVIDIA RTX 4070 Ti / 4070": [
    { "platform": "Vast.ai", "price_usd": 0.11, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T03:14:54Z", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "scraped" }
  ],
  "NVIDIA RTX 3090 / 3090 Ti": [
    { "platform": "Vast.ai", "price_usd": 0.2, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T03:14:54Z", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "scraped" },
    { "platform": "TensorDock", "price_usd": 0.35, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T03:14:54Z", "pricing_url": "https://www.tensordock.com/cloud-gpus.html", "availability": "", "source": "scraped" }
  ],
  "NVIDIA RTX 3080 / 3080 Ti": [
    { "platform": "Vast.ai", "price_usd": 0.12, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T03:14:54Z", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "scraped" }
  ],
  "NVIDIA RTX 3070 / 3070 Ti": [
    { "platform": "Vast.ai", "price_usd": 0.09, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T03:14:54Z", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "scraped" }
  ],
  "NVIDIA RTX 3060 / 3060 Ti": [
    { "platform": "Vast.ai", "price_usd": 0.08, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T03:14:54Z", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "scraped" }
  ],
  "RTX 8000": [
    { "platform": "Vast.ai", "price_usd": 0.24, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T03:14:54Z", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "scraped" }
  ],
  "RTX 6000": [
    { "platform": "Vast.ai", "price_usd": 0.13, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T03:14:54Z", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "scraped" }
  ],
  "NVIDIA RTX 2080 Ti": [
    { "platform": "Vast.ai", "price_usd": 0.08, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T03:14:54Z", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "scraped" }
  ],
  "RTX 5880": [
    { "platform": "Vast.ai", "price_usd": 0.48, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T03:14:54Z", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "scraped" }
  ],
  "NVIDIA H200": [
    { "platform": "Vast.ai", "price_usd": 3.29, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T03:14:54Z", "pricing_url": "https://vast.ai/pricing", "availability": "7台机/15张卡", "source": "scraped" },
    { "platform": "CoreWeave", "price_usd": 6.31, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T03:14:54Z", "pricing_url": "https://www.coreweave.com/pricing", "availability": "", "source": "scraped" }
  ],
  "NVIDIA H100 (80GB SXM)": [
    { "platform": "Vast.ai", "price_usd": 2.34, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T03:14:54Z", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "scraped" },
    { "platform": "RunPod", "price_usd": 1.99, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T03:14:54Z", "pricing_url": "https://www.runpod.io/pricing", "availability": "", "source": "scraped" },
    { "platform": "CoreWeave", "price_usd": 6.16, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T03:14:54Z", "pricing_url": "https://www.coreweave.com/pricing", "availability": "", "source": "scraped" },
    { "platform": "TensorDock", "price_usd": 2.25, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T03:14:54Z", "pricing_url": "https://www.tensordock.com/cloud-gpus.html", "availability": "", "source": "scraped" }
  ],
  "NVIDIA A100 (80GB SXM)": [
    { "platform": "Vast.ai", "price_usd": 0.87, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T03:14:54Z", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "scraped" },
    { "platform": "TensorDock", "price_usd": 2.25, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T03:14:54Z", "pricing_url": "https://www.tensordock.com/cloud-gpus.html", "availability": "", "source": "scraped" }
  ],
  "NVIDIA RTX 6000 Ada / A6000": [
    { "platform": "Vast.ai", "price_usd": 0.39, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T03:14:54Z", "pricing_url": "https://vast.ai/pricing", "availability": "2台机/2张卡", "source": "scraped" },
    { "platform": "TensorDock", "price_usd": 0.75, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T03:14:54Z", "pricing_url": "https://www.tensordock.com/cloud-gpus.html", "availability": "", "source": "scraped" }
  ],
  "NVIDIA A40": [
    { "platform": "Vast.ai", "price_usd": 0.29, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T03:14:54Z", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "scraped" }
  ],
  "RTX 2080": [
    { "platform": "Vast.ai", "price_usd": 0.13, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T03:14:54Z", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "scraped" }
  ],
  "NVIDIA GH200": [
    { "platform": "CoreWeave", "price_usd": 6.5, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T03:14:54Z", "pricing_url": "https://www.coreweave.com/pricing", "availability": "", "source": "scraped" }
  ],
  "NVIDIA L40S": [
    { "platform": "CoreWeave", "price_usd": 2.25, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T03:14:54Z", "pricing_url": "https://www.coreweave.com/pricing", "availability": "", "source": "scraped" }
  ],
  "NVIDIA V100": [
    { "platform": "TensorDock", "price_usd": 1.5, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T03:14:54Z", "pricing_url": "https://www.tensordock.com/cloud-gpus.html", "availability": "", "source": "scraped" }
  ]
};
