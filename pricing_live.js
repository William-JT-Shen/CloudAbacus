// 运算盘 · 实时 GPU 价格数据
// 自动生成于: 2026-06-14T01:06:57Z
// ⚠️ 由 fetch_prices.py 自动生成，请勿手动编辑

var PRICE_FETCHED_AT = "2026-06-14T01:06:57Z";
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
  },
  "Paperspace": {
    "status": "ok",
    "gpu_count": 2
  },
  "JarvisLabs": {
    "status": "ok",
    "gpu_count": 4
  },
  "DataCrunch": {
    "status": "failed",
    "gpu_count": 0,
    "error": "Verda 页面未提取到价格数据（可能需要更长的 JS 等待时间）"
  },
  "Hetzner": {
    "status": "failed",
    "gpu_count": 0,
    "error": "未能解析价格数据"
  },
  "OVHcloud": {
    "status": "ok",
    "gpu_count": 5
  },
  "Scaleway": {
    "status": "failed",
    "gpu_count": 0,
    "error": "未能解析价格数据"
  },
  "Genesis Cloud": {
    "status": "failed",
    "gpu_count": 0,
    "error": "无法访问定价页面"
  },
  "NexGen Cloud": {
    "status": "failed",
    "gpu_count": 0,
    "error": "无法访问定价页面"
  },
  "Cudo Compute": {
    "status": "failed",
    "gpu_count": 0,
    "error": "未能解析价格数据"
  },
  "G-Core Labs": {
    "status": "failed",
    "gpu_count": 0,
    "error": "无法访问定价页面"
  },
  "Cherry Servers": {
    "status": "failed",
    "gpu_count": 0,
    "error": "无法访问定价页面"
  },
  "LeaderGPU": {
    "status": "failed",
    "gpu_count": 0,
    "error": "无法访问定价页面"
  },
  "Leaseweb": {
    "status": "failed",
    "gpu_count": 0,
    "error": "未能解析价格数据"
  },
  "Hostkey": {
    "status": "failed",
    "gpu_count": 0,
    "error": "未能解析价格数据"
  },
  "UpCloud": {
    "status": "failed",
    "gpu_count": 0,
    "error": "未能解析价格数据"
  },
  "Exoscale": {
    "status": "failed",
    "gpu_count": 0,
    "error": "未能解析价格数据"
  },
  "21Cloud": {
    "status": "failed",
    "gpu_count": 0,
    "error": "无法访问定价页面"
  },
  "Servers.com": {
    "status": "failed",
    "gpu_count": 0,
    "error": "无法访问定价页面"
  },
  "Mystic AI": {
    "status": "failed",
    "gpu_count": 0,
    "error": "无法访问定价页面"
  },
  "DigitalOcean": {
    "status": "ok",
    "gpu_count": 4
  },
  "Vultr": {
    "status": "failed",
    "gpu_count": 0,
    "error": "未能解析价格数据"
  },
  "FluidStack": {
    "status": "failed",
    "gpu_count": 0,
    "error": "无法访问定价页面"
  },
  "Massed Compute": {
    "status": "ok",
    "gpu_count": 8
  },
  "Salad": {
    "status": "failed",
    "gpu_count": 0,
    "error": "未能解析价格数据"
  },
  "Hivelocity": {
    "status": "failed",
    "gpu_count": 0,
    "error": "无法访问定价页面"
  },
  "SabrePC": {
    "status": "failed",
    "gpu_count": 0,
    "error": "无法访问定价页面"
  },
  "Bizon": {
    "status": "failed",
    "gpu_count": 0,
    "error": "无法访问定价页面"
  },
  "DataPacket": {
    "status": "failed",
    "gpu_count": 0,
    "error": "无法访问定价页面"
  },
  "ServerMania": {
    "status": "failed",
    "gpu_count": 0,
    "error": "无法访问定价页面"
  },
  "Monster API": {
    "status": "failed",
    "gpu_count": 0,
    "error": "无法访问定价页面"
  },
  "Cerebrium": {
    "status": "failed",
    "gpu_count": 0,
    "error": "未能解析价格数据"
  },
  "Matpool": {
    "status": "failed",
    "gpu_count": 0,
    "error": "未提取到价格数据"
  },
  "Google Cloud": {
    "status": "failed",
    "gpu_count": 0,
    "error": "未能解析价格数据"
  },
  "IBM Cloud": {
    "status": "failed",
    "gpu_count": 0,
    "error": "未能解析价格数据"
  },
  "Oracle Cloud": {
    "status": "failed",
    "gpu_count": 0,
    "error": "未能解析价格数据"
  }
};

var GPU_PRICING_LIVE = {
  "RTX 5090": [
    { "platform": "Vast.ai", "price_usd": 0.47, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T01:06:57Z", "pricing_url": "https://vast.ai/pricing", "source": "scraped" }
  ],
  "NVIDIA RTX 4090": [
    { "platform": "Vast.ai", "price_usd": 0.4, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T01:06:57Z", "pricing_url": "https://vast.ai/pricing", "source": "scraped" },
    { "platform": "RunPod", "price_usd": 0.34, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T01:06:57Z", "pricing_url": "https://www.runpod.io/pricing", "source": "scraped" },
    { "platform": "TensorDock", "price_usd": 0.35, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T01:06:57Z", "pricing_url": "https://www.tensordock.com/cloud-gpus.html", "source": "scraped" }
  ],
  "RTX 5080": [
    { "platform": "Vast.ai", "price_usd": 0.25, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T01:06:57Z", "pricing_url": "https://vast.ai/pricing", "source": "scraped" }
  ],
  "RTX 5070 Ti": [
    { "platform": "Vast.ai", "price_usd": 0.16, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T01:06:57Z", "pricing_url": "https://vast.ai/pricing", "source": "scraped" }
  ],
  "RTX 5070": [
    { "platform": "Vast.ai", "price_usd": 0.13, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T01:06:57Z", "pricing_url": "https://vast.ai/pricing", "source": "scraped" }
  ],
  "RTX 5060 Ti": [
    { "platform": "Vast.ai", "price_usd": 0.11, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T01:06:57Z", "pricing_url": "https://vast.ai/pricing", "source": "scraped" }
  ],
  "RTX 5060": [
    { "platform": "Vast.ai", "price_usd": 0.09, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T01:06:57Z", "pricing_url": "https://vast.ai/pricing", "source": "scraped" }
  ],
  "NVIDIA RTX 4080 / 4080 Super": [
    { "platform": "Vast.ai", "price_usd": 0.24, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T01:06:57Z", "pricing_url": "https://vast.ai/pricing", "source": "scraped" }
  ],
  "NVIDIA RTX 4060 Ti": [
    { "platform": "Vast.ai", "price_usd": 0.11, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T01:06:57Z", "pricing_url": "https://vast.ai/pricing", "source": "scraped" }
  ],
  "NVIDIA RTX 4070 Ti / 4070": [
    { "platform": "Vast.ai", "price_usd": 0.11, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T01:06:57Z", "pricing_url": "https://vast.ai/pricing", "source": "scraped" }
  ],
  "NVIDIA RTX 3090 / 3090 Ti": [
    { "platform": "Vast.ai", "price_usd": 0.2, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T01:06:57Z", "pricing_url": "https://vast.ai/pricing", "source": "scraped" },
    { "platform": "TensorDock", "price_usd": 0.35, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T01:06:57Z", "pricing_url": "https://www.tensordock.com/cloud-gpus.html", "source": "scraped" }
  ],
  "NVIDIA RTX 3080 / 3080 Ti": [
    { "platform": "Vast.ai", "price_usd": 0.12, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T01:06:57Z", "pricing_url": "https://vast.ai/pricing", "source": "scraped" }
  ],
  "NVIDIA RTX 3070 / 3070 Ti": [
    { "platform": "Vast.ai", "price_usd": 0.09, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T01:06:57Z", "pricing_url": "https://vast.ai/pricing", "source": "scraped" }
  ],
  "NVIDIA RTX 3060 / 3060 Ti": [
    { "platform": "Vast.ai", "price_usd": 0.08, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T01:06:57Z", "pricing_url": "https://vast.ai/pricing", "source": "scraped" }
  ],
  "RTX 8000": [
    { "platform": "Vast.ai", "price_usd": 0.24, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T01:06:57Z", "pricing_url": "https://vast.ai/pricing", "source": "scraped" }
  ],
  "RTX 6000": [
    { "platform": "Vast.ai", "price_usd": 0.13, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T01:06:57Z", "pricing_url": "https://vast.ai/pricing", "source": "scraped" }
  ],
  "NVIDIA RTX 2080 Ti": [
    { "platform": "Vast.ai", "price_usd": 0.08, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T01:06:57Z", "pricing_url": "https://vast.ai/pricing", "source": "scraped" }
  ],
  "RTX 5880": [
    { "platform": "Vast.ai", "price_usd": 0.48, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T01:06:57Z", "pricing_url": "https://vast.ai/pricing", "source": "scraped" }
  ],
  "NVIDIA H200": [
    { "platform": "Vast.ai", "price_usd": 3.29, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T01:06:57Z", "pricing_url": "https://vast.ai/pricing", "source": "scraped" },
    { "platform": "CoreWeave", "price_usd": 6.31, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T01:06:57Z", "pricing_url": "https://www.coreweave.com/pricing", "source": "scraped" },
    { "platform": "DigitalOcean", "price_usd": 3.44, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T01:06:57Z", "pricing_url": "https://www.digitalocean.com/pricing/gpu-droplets", "source": "scraped" },
    { "platform": "Massed Compute", "price_usd": 3.62, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T01:06:57Z", "pricing_url": "https://www.massedcompute.com/pricing", "source": "scraped" }
  ],
  "NVIDIA H100 (80GB SXM)": [
    { "platform": "Vast.ai", "price_usd": 2.39, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T01:06:57Z", "pricing_url": "https://vast.ai/pricing", "source": "scraped" },
    { "platform": "RunPod", "price_usd": 1.99, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T01:06:57Z", "pricing_url": "https://www.runpod.io/pricing", "source": "scraped" },
    { "platform": "CoreWeave", "price_usd": 6.16, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T01:06:57Z", "pricing_url": "https://www.coreweave.com/pricing", "source": "scraped" },
    { "platform": "TensorDock", "price_usd": 2.25, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T01:06:57Z", "pricing_url": "https://www.tensordock.com/cloud-gpus.html", "source": "scraped" },
    { "platform": "Paperspace", "price_usd": 2.24, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T01:06:57Z", "pricing_url": "https://www.paperspace.com/pricing", "source": "scraped" },
    { "platform": "JarvisLabs", "price_usd": 2.69, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T01:06:57Z", "pricing_url": "https://jarvislabs.ai/pricing/", "source": "scraped" },
    { "platform": "OVHcloud", "price_usd": 2.99, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T01:06:57Z", "pricing_url": "https://www.ovhcloud.com/en/public-cloud/prices/", "source": "scraped" },
    { "platform": "DigitalOcean", "price_usd": 3.39, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T01:06:57Z", "pricing_url": "https://www.digitalocean.com/pricing/gpu-droplets", "source": "scraped" },
    { "platform": "Massed Compute", "price_usd": 2.73, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T01:06:57Z", "pricing_url": "https://www.massedcompute.com/pricing", "source": "scraped" }
  ],
  "NVIDIA A100 (80GB SXM)": [
    { "platform": "Vast.ai", "price_usd": 0.87, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T01:06:57Z", "pricing_url": "https://vast.ai/pricing", "source": "scraped" },
    { "platform": "TensorDock", "price_usd": 2.25, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T01:06:57Z", "pricing_url": "https://www.tensordock.com/cloud-gpus.html", "source": "scraped" },
    { "platform": "JarvisLabs", "price_usd": 1.49, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T01:06:57Z", "pricing_url": "https://jarvislabs.ai/pricing/", "source": "scraped" },
    { "platform": "Massed Compute", "price_usd": 1.35, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T01:06:57Z", "pricing_url": "https://www.massedcompute.com/pricing", "source": "scraped" }
  ],
  "NVIDIA RTX 6000 Ada / A6000": [
    { "platform": "Vast.ai", "price_usd": 0.39, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T01:06:57Z", "pricing_url": "https://vast.ai/pricing", "source": "scraped" },
    { "platform": "TensorDock", "price_usd": 0.75, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T01:06:57Z", "pricing_url": "https://www.tensordock.com/cloud-gpus.html", "source": "scraped" },
    { "platform": "Massed Compute", "price_usd": 0.57, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T01:06:57Z", "pricing_url": "https://www.massedcompute.com/pricing", "source": "scraped" }
  ],
  "NVIDIA A40": [
    { "platform": "Vast.ai", "price_usd": 0.29, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T01:06:57Z", "pricing_url": "https://vast.ai/pricing", "source": "scraped" }
  ],
  "RTX 2080": [
    { "platform": "Vast.ai", "price_usd": 0.13, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T01:06:57Z", "pricing_url": "https://vast.ai/pricing", "source": "scraped" }
  ],
  "NVIDIA GH200": [
    { "platform": "CoreWeave", "price_usd": 6.5, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T01:06:57Z", "pricing_url": "https://www.coreweave.com/pricing", "source": "scraped" }
  ],
  "NVIDIA L40S": [
    { "platform": "CoreWeave", "price_usd": 2.25, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T01:06:57Z", "pricing_url": "https://www.coreweave.com/pricing", "source": "scraped" },
    { "platform": "OVHcloud", "price_usd": 1.8, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T01:06:57Z", "pricing_url": "https://www.ovhcloud.com/en/public-cloud/prices/", "source": "scraped" },
    { "platform": "DigitalOcean", "price_usd": 1.57, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T01:06:57Z", "pricing_url": "https://www.digitalocean.com/pricing/gpu-droplets", "source": "scraped" },
    { "platform": "Massed Compute", "price_usd": 0.88, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T01:06:57Z", "pricing_url": "https://www.massedcompute.com/pricing", "source": "scraped" }
  ],
  "NVIDIA V100": [
    { "platform": "TensorDock", "price_usd": 1.5, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T01:06:57Z", "pricing_url": "https://www.tensordock.com/cloud-gpus.html", "source": "scraped" },
    { "platform": "Paperspace", "price_usd": 1.84, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T01:06:57Z", "pricing_url": "https://www.paperspace.com/pricing", "source": "scraped" },
    { "platform": "OVHcloud", "price_usd": 0.77, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T01:06:57Z", "pricing_url": "https://www.ovhcloud.com/en/public-cloud/prices/", "source": "scraped" }
  ],
  "NVIDIA A100 (40GB PCIe)": [
    { "platform": "JarvisLabs", "price_usd": 1.49, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T01:06:57Z", "pricing_url": "https://jarvislabs.ai/pricing/", "source": "scraped" },
    { "platform": "Massed Compute", "price_usd": 1.35, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T01:06:57Z", "pricing_url": "https://www.massedcompute.com/pricing", "source": "scraped" }
  ],
  "NVIDIA L4": [
    { "platform": "JarvisLabs", "price_usd": 0.44, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T01:06:57Z", "pricing_url": "https://jarvislabs.ai/pricing/", "source": "scraped" },
    { "platform": "OVHcloud", "price_usd": 1.0, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T01:06:57Z", "pricing_url": "https://www.ovhcloud.com/en/public-cloud/prices/", "source": "scraped" },
    { "platform": "DigitalOcean", "price_usd": 1.0, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T01:06:57Z", "pricing_url": "https://www.digitalocean.com/pricing/gpu-droplets", "source": "scraped" },
    { "platform": "Massed Compute", "price_usd": 1.0, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T01:06:57Z", "pricing_url": "https://www.massedcompute.com/pricing", "source": "scraped" }
  ],
  "NVIDIA T4": [
    { "platform": "OVHcloud", "price_usd": 0.43, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T01:06:57Z", "pricing_url": "https://www.ovhcloud.com/en/public-cloud/prices/", "source": "scraped" },
    { "platform": "Massed Compute", "price_usd": 1.0, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-14T01:06:57Z", "pricing_url": "https://www.massedcompute.com/pricing", "source": "scraped" }
  ]
};
