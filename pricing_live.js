// 运算盘 · 实时 GPU 价格数据
// 自动生成于: 2026-06-23T08:53:46Z
// ⚠️ 由 fetch_prices.py 自动生成，请勿手动编辑

var PRICE_FETCHED_AT = "2026-06-23T08:53:46Z";
var PRICE_SCRAPE_SOURCES = {
  "Vast.ai": {
    "status": "failed",
    "gpu_count": 0,
    "error": "无法访问定价页面"
  },
  "RunPod": {
    "status": "ok",
    "gpu_count": 2
  },
  "Lambda Labs": {
    "status": "ok",
    "gpu_count": 9
  },
  "CoreWeave": {
    "status": "ok",
    "gpu_count": 5
  },
  "TensorDock": {
    "status": "ok",
    "gpu_count": 9
  }
};

var GPU_PRICING_LIVE = {
  "NVIDIA H100 (80GB SXM)": [
    { "platform": "Vast.ai", "price_usd": 2.31, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-17T10:47:13Z", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "scraped" },
    { "platform": "RunPod", "price_usd": 1.99, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-23T08:53:46Z", "pricing_url": "https://www.runpod.io/pricing", "availability": "", "source": "scraped" },
    { "platform": "Lambda Labs", "price_usd": 6.69, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-23T08:53:46Z", "pricing_url": "https://lambda.ai/pricing", "availability": "", "source": "scraped" },
    { "platform": "CoreWeave", "price_usd": 6.16, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-23T08:53:46Z", "pricing_url": "https://www.coreweave.com/pricing", "availability": "", "source": "scraped" },
    { "platform": "TensorDock", "price_usd": 2.25, "plan": "GPU起价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-23T08:53:46Z", "pricing_url": "https://www.tensordock.com/cloud-gpus.html", "availability": "", "source": "scraped" }
  ],
  "NVIDIA RTX 4090": [
    { "platform": "Vast.ai", "price_usd": 0.36, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-17T10:47:13Z", "pricing_url": "https://vast.ai/pricing", "availability": "共10张", "source": "scraped" },
    { "platform": "RunPod", "price_usd": 0.34, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-23T08:53:46Z", "pricing_url": "https://www.runpod.io/pricing", "availability": "", "source": "scraped" },
    { "platform": "TensorDock", "price_usd": 0.35, "plan": "GPU起价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-23T08:53:46Z", "pricing_url": "https://www.tensordock.com/cloud-gpus.html", "availability": "", "source": "scraped" }
  ],
  "NVIDIA H200": [
    { "platform": "Vast.ai", "price_usd": 3.21, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-17T10:47:13Z", "pricing_url": "https://vast.ai/pricing", "availability": "共83张", "source": "scraped" },
    { "platform": "Lambda Labs", "price_usd": 6.99, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-23T08:53:46Z", "pricing_url": "https://lambda.ai/pricing", "availability": "", "source": "scraped" },
    { "platform": "CoreWeave", "price_usd": 6.31, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-23T08:53:46Z", "pricing_url": "https://www.coreweave.com/pricing", "availability": "", "source": "scraped" }
  ],
  "NVIDIA GH200": [
    { "platform": "Lambda Labs", "price_usd": 6.99, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-23T08:53:46Z", "pricing_url": "https://lambda.ai/pricing", "availability": "", "source": "scraped" },
    { "platform": "CoreWeave", "price_usd": 6.5, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-23T08:53:46Z", "pricing_url": "https://www.coreweave.com/pricing", "availability": "", "source": "scraped" }
  ],
  "NVIDIA A100 (80GB SXM)": [
    { "platform": "Vast.ai", "price_usd": 0.8, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-17T10:47:13Z", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "scraped" },
    { "platform": "Lambda Labs", "price_usd": 3.99, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-23T08:53:46Z", "pricing_url": "https://lambda.ai/pricing", "availability": "", "source": "scraped" },
    { "platform": "TensorDock", "price_usd": 1.8, "plan": "GPU起价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-23T08:53:46Z", "pricing_url": "https://www.tensordock.com/cloud-gpus.html", "availability": "", "source": "scraped" }
  ],
  "NVIDIA A100 (40GB PCIe)": [
    { "platform": "Lambda Labs", "price_usd": 2.79, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-23T08:53:46Z", "pricing_url": "https://lambda.ai/pricing", "availability": "", "source": "scraped" },
    { "platform": "TensorDock", "price_usd": 1.5, "plan": "GPU起价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-23T08:53:46Z", "pricing_url": "https://www.tensordock.com/cloud-gpus.html", "availability": "", "source": "scraped" }
  ],
  "NVIDIA V100": [
    { "platform": "Lambda Labs", "price_usd": 1.99, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-23T08:53:46Z", "pricing_url": "https://lambda.ai/pricing", "availability": "", "source": "scraped" },
    { "platform": "TensorDock", "price_usd": 0.17, "plan": "GPU起价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-23T08:53:46Z", "pricing_url": "https://www.tensordock.com/cloud-gpus.html", "availability": "", "source": "scraped" }
  ],
  "NVIDIA RTX 6000 Ada / A6000": [
    { "platform": "Vast.ai", "price_usd": 0.39, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-17T10:47:13Z", "pricing_url": "https://vast.ai/pricing", "availability": "共13张", "source": "scraped" },
    { "platform": "Lambda Labs", "price_usd": 1.99, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-23T08:53:46Z", "pricing_url": "https://lambda.ai/pricing", "availability": "", "source": "scraped" },
    { "platform": "TensorDock", "price_usd": 0.75, "plan": "GPU起价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-23T08:53:46Z", "pricing_url": "https://www.tensordock.com/cloud-gpus.html", "availability": "", "source": "scraped" }
  ],
  "RTX 6000": [
    { "platform": "Vast.ai", "price_usd": 0.6, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-17T10:47:13Z", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "scraped" },
    { "platform": "Lambda Labs", "price_usd": 1.09, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-23T08:53:46Z", "pricing_url": "https://lambda.ai/pricing", "availability": "", "source": "scraped" }
  ],
  "NVIDIA B200": [
    { "platform": "Lambda Labs", "price_usd": 9.86, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-23T08:53:46Z", "pricing_url": "https://lambda.ai/pricing", "availability": "", "source": "scraped" },
    { "platform": "CoreWeave", "price_usd": 8.6, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-23T08:53:46Z", "pricing_url": "https://www.coreweave.com/pricing", "availability": "", "source": "scraped" }
  ],
  "NVIDIA L40S": [
    { "platform": "CoreWeave", "price_usd": 2.25, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-23T08:53:46Z", "pricing_url": "https://www.coreweave.com/pricing", "availability": "", "source": "scraped" },
    { "platform": "TensorDock", "price_usd": 0.95, "plan": "GPU起价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-23T08:53:46Z", "pricing_url": "https://www.tensordock.com/cloud-gpus.html", "availability": "", "source": "scraped" }
  ],
  "NVIDIA RTX 3090 / 3090 Ti": [
    { "platform": "Vast.ai", "price_usd": 0.2, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-17T10:47:13Z", "pricing_url": "https://vast.ai/pricing", "availability": "共8张", "source": "scraped" },
    { "platform": "TensorDock", "price_usd": 0.2, "plan": "GPU起价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-23T08:53:46Z", "pricing_url": "https://www.tensordock.com/cloud-gpus.html", "availability": "", "source": "scraped" }
  ],
  "RTX A4000 16GB": [
    { "platform": "TensorDock", "price_usd": 0.1, "plan": "GPU起价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-23T08:53:46Z", "pricing_url": "https://www.tensordock.com/cloud-gpus.html", "availability": "", "source": "scraped" }
  ],
  "RTX 5090": [
    { "platform": "Vast.ai", "price_usd": 0.44, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-17T10:47:13Z", "pricing_url": "https://vast.ai/pricing", "availability": "共12张", "source": "scraped" }
  ],
  "RTX 5080": [
    { "platform": "Vast.ai", "price_usd": 0.23, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-17T10:47:13Z", "pricing_url": "https://vast.ai/pricing", "availability": "共3张", "source": "scraped" }
  ],
  "RTX 5070 Ti": [
    { "platform": "Vast.ai", "price_usd": 0.15, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-17T10:47:13Z", "pricing_url": "https://vast.ai/pricing", "availability": "共4张", "source": "scraped" }
  ],
  "RTX 5070": [
    { "platform": "Vast.ai", "price_usd": 0.13, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-17T10:47:13Z", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "scraped" }
  ],
  "RTX 5060 Ti": [
    { "platform": "Vast.ai", "price_usd": 0.1, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-17T10:47:13Z", "pricing_url": "https://vast.ai/pricing", "availability": "共1张", "source": "scraped" }
  ],
  "RTX 5060": [
    { "platform": "Vast.ai", "price_usd": 0.08, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-17T10:47:13Z", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "scraped" }
  ],
  "NVIDIA RTX 4080 / 4080 Super": [
    { "platform": "Vast.ai", "price_usd": 0.2, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-17T10:47:13Z", "pricing_url": "https://vast.ai/pricing", "availability": "共2张", "source": "scraped" }
  ],
  "NVIDIA RTX 4070 Ti / 4070": [
    { "platform": "Vast.ai", "price_usd": 0.11, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-17T10:47:13Z", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "scraped" }
  ],
  "NVIDIA RTX 4060 Ti": [
    { "platform": "Vast.ai", "price_usd": 0.09, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-17T10:47:13Z", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "scraped" }
  ],
  "NVIDIA RTX 3080 / 3080 Ti": [
    { "platform": "Vast.ai", "price_usd": 0.11, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-17T10:47:13Z", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "scraped" }
  ],
  "NVIDIA RTX 3070 / 3070 Ti": [
    { "platform": "Vast.ai", "price_usd": 0.08, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-17T10:47:13Z", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "scraped" }
  ],
  "NVIDIA RTX 3060 / 3060 Ti": [
    { "platform": "Vast.ai", "price_usd": 0.08, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-17T10:47:13Z", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "scraped" }
  ],
  "RTX 8000": [
    { "platform": "Vast.ai", "price_usd": 0.24, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-17T10:47:13Z", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "scraped" }
  ],
  "NVIDIA RTX 2080 Ti": [
    { "platform": "Vast.ai", "price_usd": 0.07, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-17T10:47:13Z", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "scraped" }
  ],
  "RTX 5880": [
    { "platform": "Vast.ai", "price_usd": 0.48, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-17T10:47:13Z", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "scraped" }
  ],
  "NVIDIA A40": [
    { "platform": "Vast.ai", "price_usd": 0.29, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-17T10:47:13Z", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "scraped" }
  ],
  "RTX 2080": [
    { "platform": "Vast.ai", "price_usd": 0.07, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-17T10:47:13Z", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "scraped" }
  ]
};
