// 运算盘 · 实时 GPU 价格数据
// 自动生成于: 2026-06-15T12:12:59Z
// ⚠️ 由 fetch_prices.py 自动生成，请勿手动编辑

var PRICE_FETCHED_AT = "2026-06-15T12:12:59Z";
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
    "error": "页面可能为 JS 动态渲染，需 Playwright"
  },
  "OVHcloud": {
    "status": "ok",
    "gpu_count": 5
  },
  "Scaleway": {
    "status": "failed",
    "gpu_count": 0,
    "error": "API 返回 404"
  },
  "Genesis Cloud": {
    "status": "failed",
    "gpu_count": 0,
    "error": "未能解析价格数据"
  },
  "NexGen Cloud": {
    "status": "ok",
    "gpu_count": 2
  },
  "Cudo Compute": {
    "status": "failed",
    "gpu_count": 0,
    "error": "Elementor 选项卡 AJAX 动态加载, 需手动交互或 API 授权"
  },
  "G-Core Labs": {
    "status": "failed",
    "gpu_count": 0,
    "error": "未能解析价格数据"
  },
  "Cherry Servers": {
    "status": "failed",
    "gpu_count": 0,
    "error": "未能解析价格数据"
  },
  "LeaderGPU": {
    "status": "failed",
    "gpu_count": 0,
    "error": "未能解析价格数据"
  },
  "Leaseweb": {
    "status": "failed",
    "gpu_count": 0,
    "error": "未能解析价格数据"
  },
  "Hostkey": {
    "status": "ok",
    "gpu_count": 13
  },
  "UpCloud": {
    "status": "ok",
    "gpu_count": 3
  },
  "Exoscale": {
    "status": "ok",
    "gpu_count": 7
  },
  "21Cloud": {
    "status": "failed",
    "gpu_count": 0,
    "error": "无法访问定价页面"
  },
  "Servers.com": {
    "status": "failed",
    "gpu_count": 0,
    "error": "未能解析价格数据"
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
    "error": "未能解析价格数据"
  },
  "Massed Compute": {
    "status": "ok",
    "gpu_count": 8
  },
  "Salad": {
    "status": "ok",
    "gpu_count": 23
  },
  "Hivelocity": {
    "status": "failed",
    "gpu_count": 0,
    "error": "未能解析价格数据"
  },
  "SabrePC": {
    "status": "failed",
    "gpu_count": 0,
    "error": "未能解析价格数据"
  },
  "Bizon": {
    "status": "failed",
    "gpu_count": 0,
    "error": "无法访问定价页面"
  },
  "DataPacket": {
    "status": "failed",
    "gpu_count": 0,
    "error": "未能解析价格数据"
  },
  "ServerMania": {
    "status": "failed",
    "gpu_count": 0,
    "error": "未能解析价格数据"
  },
  "Monster API": {
    "status": "failed",
    "gpu_count": 0,
    "error": "无法访问定价页面"
  },
  "Cerebrium": {
    "status": "ok",
    "gpu_count": 5
  },
  "Matpool": {
    "status": "failed",
    "gpu_count": 0,
    "error": "未提取到价格数据"
  },
  "腾讯云": {
    "status": "ok",
    "gpu_count": 4
  },
  "阿里云": {
    "status": "failed",
    "gpu_count": 0,
    "error": "Playwright 未提取到价格数据"
  },
  "华为云": {
    "status": "failed",
    "gpu_count": 0,
    "error": "Playwright 未提取到价格数据"
  },
  "火山引擎": {
    "status": "failed",
    "gpu_count": 0,
    "error": "Playwright 未提取到价格数据"
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
    { "platform": "Vast.ai", "price_usd": 0.45, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://vast.ai/pricing", "availability": "共14张", "source": "scraped" },
    { "platform": "Hostkey", "price_usd": 0.75, "plan": "月租€510.0/月 ≈ €0.699/时", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://hostkey.com/gpu-dedicated-servers/", "availability": "", "source": "scraped" }
  ],
  "NVIDIA RTX 4090": [
    { "platform": "Vast.ai", "price_usd": 0.37, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://vast.ai/pricing", "availability": "共10张", "source": "scraped" },
    { "platform": "RunPod", "price_usd": 0.34, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://www.runpod.io/pricing", "availability": "", "source": "scraped" },
    { "platform": "TensorDock", "price_usd": 0.35, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://www.tensordock.com/cloud-gpus.html", "availability": "", "source": "scraped" },
    { "platform": "Hostkey", "price_usd": 1.11, "plan": "月租€750.0/月 ≈ €1.027/时", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://hostkey.com/gpu-dedicated-servers/", "availability": "", "source": "scraped" },
    { "platform": "Salad", "price_usd": 0.16, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://salad.com/pricing", "availability": "", "source": "scraped" }
  ],
  "RTX 5080": [
    { "platform": "Vast.ai", "price_usd": 0.24, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://vast.ai/pricing", "availability": "共3张", "source": "scraped" }
  ],
  "RTX 5070 Ti": [
    { "platform": "Vast.ai", "price_usd": 0.16, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://vast.ai/pricing", "availability": "共3张", "source": "scraped" }
  ],
  "RTX 5070": [
    { "platform": "Vast.ai", "price_usd": 0.13, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "scraped" }
  ],
  "RTX 5060 Ti": [
    { "platform": "Vast.ai", "price_usd": 0.11, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://vast.ai/pricing", "availability": "共3张", "source": "scraped" }
  ],
  "RTX 5060": [
    { "platform": "Vast.ai", "price_usd": 0.09, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "scraped" }
  ],
  "NVIDIA RTX 4080 / 4080 Super": [
    { "platform": "Vast.ai", "price_usd": 0.21, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://vast.ai/pricing", "availability": "共3张", "source": "scraped" },
    { "platform": "Salad", "price_usd": 0.11, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://salad.com/pricing", "availability": "", "source": "scraped" }
  ],
  "NVIDIA RTX 4060 Ti": [
    { "platform": "Vast.ai", "price_usd": 0.11, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "scraped" },
    { "platform": "Salad", "price_usd": 0.08, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://salad.com/pricing", "availability": "", "source": "scraped" }
  ],
  "NVIDIA RTX 4070 Ti / 4070": [
    { "platform": "Vast.ai", "price_usd": 0.11, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://vast.ai/pricing", "availability": "共2张", "source": "scraped" },
    { "platform": "Salad", "price_usd": 0.08, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://salad.com/pricing", "availability": "", "source": "scraped" }
  ],
  "NVIDIA RTX 3090 / 3090 Ti": [
    { "platform": "Vast.ai", "price_usd": 0.19, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://vast.ai/pricing", "availability": "共4张", "source": "scraped" },
    { "platform": "TensorDock", "price_usd": 0.35, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://www.tensordock.com/cloud-gpus.html", "availability": "", "source": "scraped" },
    { "platform": "Hostkey", "price_usd": 0.47, "plan": "月租€319.0/月 ≈ €0.437/时", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://hostkey.com/gpu-dedicated-servers/", "availability": "", "source": "scraped" },
    { "platform": "Salad", "price_usd": 0.1, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://salad.com/pricing", "availability": "", "source": "scraped" }
  ],
  "NVIDIA RTX 3080 / 3080 Ti": [
    { "platform": "Vast.ai", "price_usd": 0.11, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "scraped" },
    { "platform": "Hostkey", "price_usd": 0.28, "plan": "月租€190.0/月 ≈ €0.260/时", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://hostkey.com/gpu-dedicated-servers/", "availability": "", "source": "scraped" },
    { "platform": "Exoscale", "price_usd": 0.92, "plan": "最小配置 (API)", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://www.exoscale.com/gpu/", "availability": "", "source": "scraped" },
    { "platform": "Salad", "price_usd": 0.08, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://salad.com/pricing", "availability": "", "source": "scraped" }
  ],
  "NVIDIA RTX 3070 / 3070 Ti": [
    { "platform": "Vast.ai", "price_usd": 0.09, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "scraped" },
    { "platform": "Salad", "price_usd": 0.06, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://salad.com/pricing", "availability": "", "source": "scraped" }
  ],
  "NVIDIA RTX 3060 / 3060 Ti": [
    { "platform": "Vast.ai", "price_usd": 0.08, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "scraped" },
    { "platform": "Salad", "price_usd": 0.04, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://salad.com/pricing", "availability": "", "source": "scraped" }
  ],
  "RTX 8000": [
    { "platform": "Vast.ai", "price_usd": 0.24, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "scraped" }
  ],
  "RTX 6000": [
    { "platform": "Vast.ai", "price_usd": 0.13, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "scraped" }
  ],
  "NVIDIA RTX 2080 Ti": [
    { "platform": "Vast.ai", "price_usd": 0.07, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "scraped" },
    { "platform": "Salad", "price_usd": 0.06, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://salad.com/pricing", "availability": "", "source": "scraped" }
  ],
  "RTX 5880": [
    { "platform": "Vast.ai", "price_usd": 0.48, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "scraped" }
  ],
  "NVIDIA H200": [
    { "platform": "Vast.ai", "price_usd": 3.29, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://vast.ai/pricing", "availability": "共68张", "source": "scraped" },
    { "platform": "CoreWeave", "price_usd": 6.31, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://www.coreweave.com/pricing", "availability": "", "source": "scraped" },
    { "platform": "DigitalOcean", "price_usd": 3.44, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://www.digitalocean.com/pricing/gpu-droplets", "availability": "", "source": "scraped" },
    { "platform": "Massed Compute", "price_usd": 3.62, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://www.massedcompute.com/pricing", "availability": "", "source": "scraped" },
    { "platform": "Cerebrium", "price_usd": 4.2, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://www.cerebrium.ai/pricing", "availability": "", "source": "scraped" }
  ],
  "NVIDIA H100 (80GB SXM)": [
    { "platform": "Vast.ai", "price_usd": 2.39, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://vast.ai/pricing", "availability": "共3张", "source": "scraped" },
    { "platform": "RunPod", "price_usd": 1.99, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://www.runpod.io/pricing", "availability": "", "source": "scraped" },
    { "platform": "CoreWeave", "price_usd": 6.16, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://www.coreweave.com/pricing", "availability": "", "source": "scraped" },
    { "platform": "TensorDock", "price_usd": 2.25, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://www.tensordock.com/cloud-gpus.html", "availability": "", "source": "scraped" },
    { "platform": "Paperspace", "price_usd": 2.24, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://www.paperspace.com/pricing", "availability": "", "source": "scraped" },
    { "platform": "JarvisLabs", "price_usd": 2.69, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://jarvislabs.ai/pricing/", "availability": "", "source": "scraped" },
    { "platform": "OVHcloud", "price_usd": 2.99, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://www.ovhcloud.com/en/public-cloud/prices/", "availability": "", "source": "scraped" },
    { "platform": "NexGen Cloud", "price_usd": 1.37, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://www.hyperstack.cloud/gpu-pricing", "availability": "", "source": "scraped" },
    { "platform": "Hostkey", "price_usd": 2.35, "plan": "月租€1590.0/月 ≈ €2.178/时", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://hostkey.com/gpu-dedicated-servers/", "availability": "", "source": "scraped" },
    { "platform": "UpCloud", "price_usd": 1.93, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://upcloud.com/pricing/", "availability": "", "source": "scraped" },
    { "platform": "DigitalOcean", "price_usd": 3.39, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://www.digitalocean.com/pricing/gpu-droplets", "availability": "", "source": "scraped" },
    { "platform": "Massed Compute", "price_usd": 2.73, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://www.massedcompute.com/pricing", "availability": "", "source": "scraped" },
    { "platform": "Cerebrium", "price_usd": 3.4, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://www.cerebrium.ai/pricing", "availability": "", "source": "scraped" },
    { "platform": "腾讯云", "price_usd": 1.89, "plan": "月付¥9995/GPU (HCCG5v.24XLARGE384)", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://buy.cloud.tencent.com/price/cvm/overview", "availability": "", "source": "scraped" }
  ],
  "NVIDIA A100 (80GB SXM)": [
    { "platform": "Vast.ai", "price_usd": 0.87, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "scraped" },
    { "platform": "TensorDock", "price_usd": 2.25, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://www.tensordock.com/cloud-gpus.html", "availability": "", "source": "scraped" },
    { "platform": "JarvisLabs", "price_usd": 1.49, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://jarvislabs.ai/pricing/", "availability": "", "source": "scraped" },
    { "platform": "Hostkey", "price_usd": 1.92, "plan": "月租€1300.0/月 ≈ €1.781/时", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://hostkey.com/gpu-dedicated-servers/", "availability": "", "source": "scraped" },
    { "platform": "Massed Compute", "price_usd": 1.35, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://www.massedcompute.com/pricing", "availability": "", "source": "scraped" },
    { "platform": "Cerebrium", "price_usd": 2.1, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://www.cerebrium.ai/pricing", "availability": "", "source": "scraped" },
    { "platform": "腾讯云", "price_usd": 2.45, "plan": "月付¥12948/GPU (GT4.4XLARGE96)", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://buy.cloud.tencent.com/price/cvm/overview", "availability": "", "source": "scraped" }
  ],
  "NVIDIA RTX 6000 Ada / A6000": [
    { "platform": "Vast.ai", "price_usd": 0.39, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://vast.ai/pricing", "availability": "共16张", "source": "scraped" },
    { "platform": "TensorDock", "price_usd": 0.75, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://www.tensordock.com/cloud-gpus.html", "availability": "", "source": "scraped" },
    { "platform": "Exoscale", "price_usd": 2.15, "plan": "最小配置 (API)", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://www.exoscale.com/gpu/", "availability": "", "source": "scraped" },
    { "platform": "Massed Compute", "price_usd": 0.57, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://www.massedcompute.com/pricing", "availability": "", "source": "scraped" }
  ],
  "NVIDIA A40": [
    { "platform": "Vast.ai", "price_usd": 0.29, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "scraped" }
  ],
  "RTX 2080": [
    { "platform": "Vast.ai", "price_usd": 0.13, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "scraped" },
    { "platform": "Salad", "price_usd": 0.05, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://salad.com/pricing", "availability": "", "source": "scraped" }
  ],
  "NVIDIA GH200": [
    { "platform": "CoreWeave", "price_usd": 6.5, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://www.coreweave.com/pricing", "availability": "", "source": "scraped" }
  ],
  "NVIDIA L40S": [
    { "platform": "CoreWeave", "price_usd": 2.25, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://www.coreweave.com/pricing", "availability": "", "source": "scraped" },
    { "platform": "OVHcloud", "price_usd": 1.8, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://www.ovhcloud.com/en/public-cloud/prices/", "availability": "", "source": "scraped" },
    { "platform": "UpCloud", "price_usd": 1.2, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://upcloud.com/pricing/", "availability": "", "source": "scraped" },
    { "platform": "DigitalOcean", "price_usd": 1.57, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://www.digitalocean.com/pricing/gpu-droplets", "availability": "", "source": "scraped" },
    { "platform": "Massed Compute", "price_usd": 0.88, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://www.massedcompute.com/pricing", "availability": "", "source": "scraped" },
    { "platform": "Cerebrium", "price_usd": 1.95, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://www.cerebrium.ai/pricing", "availability": "", "source": "scraped" },
    { "platform": "腾讯云", "price_usd": 2.22, "plan": "月付¥11750/GPU (GC50sg.12XLARGE192)", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://buy.cloud.tencent.com/price/cvm/overview", "availability": "", "source": "scraped" }
  ],
  "NVIDIA V100": [
    { "platform": "TensorDock", "price_usd": 1.5, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://www.tensordock.com/cloud-gpus.html", "availability": "", "source": "scraped" },
    { "platform": "Paperspace", "price_usd": 1.84, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://www.paperspace.com/pricing", "availability": "", "source": "scraped" },
    { "platform": "OVHcloud", "price_usd": 0.77, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://www.ovhcloud.com/en/public-cloud/prices/", "availability": "", "source": "scraped" },
    { "platform": "Exoscale", "price_usd": 1.38, "plan": "最小配置 (API)", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://www.exoscale.com/gpu/", "availability": "", "source": "scraped" }
  ],
  "NVIDIA A100 (40GB PCIe)": [
    { "platform": "JarvisLabs", "price_usd": 1.49, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://jarvislabs.ai/pricing/", "availability": "", "source": "scraped" },
    { "platform": "Massed Compute", "price_usd": 1.35, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://www.massedcompute.com/pricing", "availability": "", "source": "scraped" }
  ],
  "NVIDIA L4": [
    { "platform": "JarvisLabs", "price_usd": 0.44, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://jarvislabs.ai/pricing/", "availability": "", "source": "scraped" },
    { "platform": "OVHcloud", "price_usd": 1.0, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://www.ovhcloud.com/en/public-cloud/prices/", "availability": "", "source": "scraped" },
    { "platform": "NexGen Cloud", "price_usd": 1.4, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://www.hyperstack.cloud/gpu-pricing", "availability": "", "source": "scraped" },
    { "platform": "UpCloud", "price_usd": 0.63, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://upcloud.com/pricing/", "availability": "", "source": "scraped" },
    { "platform": "DigitalOcean", "price_usd": 1.0, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://www.digitalocean.com/pricing/gpu-droplets", "availability": "", "source": "scraped" },
    { "platform": "Massed Compute", "price_usd": 1.0, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://www.massedcompute.com/pricing", "availability": "", "source": "scraped" }
  ],
  "NVIDIA T4": [
    { "platform": "OVHcloud", "price_usd": 0.43, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://www.ovhcloud.com/en/public-cloud/prices/", "availability": "", "source": "scraped" },
    { "platform": "Exoscale", "price_usd": 1.05, "plan": "最小配置 (API)", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://www.exoscale.com/gpu/", "availability": "", "source": "scraped" },
    { "platform": "Massed Compute", "price_usd": 1.0, "plan": "按需", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://www.massedcompute.com/pricing", "availability": "", "source": "scraped" },
    { "platform": "Cerebrium", "price_usd": 0.59, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://www.cerebrium.ai/pricing", "availability": "", "source": "scraped" },
    { "platform": "腾讯云", "price_usd": 0.47, "plan": "月付¥2500/GPU (GN7.2XLARGE32)", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://buy.cloud.tencent.com/price/cvm/overview", "availability": "", "source": "scraped" }
  ],
  "6000 PRO": [
    { "platform": "Hostkey", "price_usd": 2.81, "plan": "月租€1900.0/月 ≈ €2.603/时", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://hostkey.com/gpu-dedicated-servers/", "availability": "", "source": "scraped" }
  ],
  "7900XTX": [
    { "platform": "Hostkey", "price_usd": 1.18, "plan": "月租€800.0/月 ≈ €1.096/时", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://hostkey.com/gpu-dedicated-servers/", "availability": "", "source": "scraped" }
  ],
  "A5000": [
    { "platform": "Hostkey", "price_usd": 0.41, "plan": "月租€279.0/月 ≈ €0.382/时", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://hostkey.com/gpu-dedicated-servers/", "availability": "", "source": "scraped" }
  ],
  "AMD R9700": [
    { "platform": "Hostkey", "price_usd": 0.5, "plan": "月租€339.0/月 ≈ €0.464/时", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://hostkey.com/gpu-dedicated-servers/", "availability": "", "source": "scraped" }
  ],
  "2000 PRO": [
    { "platform": "Hostkey", "price_usd": 0.26, "plan": "月租€179.0/月 ≈ €0.245/时", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://hostkey.com/gpu-dedicated-servers/", "availability": "", "source": "scraped" }
  ],
  "A4000": [
    { "platform": "Hostkey", "price_usd": 0.32, "plan": "月租€219.0/月 ≈ €0.300/时", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://hostkey.com/gpu-dedicated-servers/", "availability": "", "source": "scraped" }
  ],
  "1080Ti": [
    { "platform": "Hostkey", "price_usd": 0.1, "plan": "月租€70.0/月 ≈ €0.096/时", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://hostkey.com/gpu-dedicated-servers/", "availability": "", "source": "scraped" }
  ],
  "NVIDIA Tesla P100 / P40": [
    { "platform": "Exoscale", "price_usd": 1.17, "plan": "最小配置 (API)", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://www.exoscale.com/gpu/", "availability": "", "source": "scraped" }
  ],
  "NVIDIA RTX A5000": [
    { "platform": "Exoscale", "price_usd": 1.34, "plan": "最小配置 (API)", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://www.exoscale.com/gpu/", "availability": "", "source": "scraped" }
  ],
  "NVIDIA A30": [
    { "platform": "Exoscale", "price_usd": 1.23, "plan": "最小配置 (API)", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://www.exoscale.com/gpu/", "availability": "", "source": "scraped" }
  ],
  "RTX A5000 (24 GB)": [
    { "platform": "Salad", "price_usd": 0.09, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://salad.com/pricing", "availability": "", "source": "scraped" }
  ],
  "RTX 4070 Ti Super (16 GB)": [
    { "platform": "Salad", "price_usd": 0.09, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://salad.com/pricing", "availability": "", "source": "scraped" }
  ],
  "RTX 3050 (8 GB)": [
    { "platform": "Salad", "price_usd": 0.03, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://salad.com/pricing", "availability": "", "source": "scraped" }
  ],
  "RTX 2070 (8 GB)": [
    { "platform": "Salad", "price_usd": 0.02, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://salad.com/pricing", "availability": "", "source": "scraped" }
  ],
  "RTX 2060 (6 GB)": [
    { "platform": "Salad", "price_usd": 0.02, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://salad.com/pricing", "availability": "", "source": "scraped" }
  ],
  "GTX 1660 Super (6 GB)": [
    { "platform": "Salad", "price_usd": 0.02, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://salad.com/pricing", "availability": "", "source": "scraped" }
  ],
  "GTX 1660 (6 GB)": [
    { "platform": "Salad", "price_usd": 0.02, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://salad.com/pricing", "availability": "", "source": "scraped" }
  ],
  "GTX 1650 (4 GB)": [
    { "platform": "Salad", "price_usd": 0.02, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://salad.com/pricing", "availability": "", "source": "scraped" }
  ],
  "GTX 1080 Ti (8 GB)": [
    { "platform": "Salad", "price_usd": 0.02, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://salad.com/pricing", "availability": "", "source": "scraped" }
  ],
  "GTX 1080 (8 GB)": [
    { "platform": "Salad", "price_usd": 0.02, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://salad.com/pricing", "availability": "", "source": "scraped" }
  ],
  "GTX 1070 (8 GB)": [
    { "platform": "Salad", "price_usd": 0.02, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://salad.com/pricing", "availability": "", "source": "scraped" }
  ],
  "GTX 1060 (6 GB)": [
    { "platform": "Salad", "price_usd": 0.02, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://salad.com/pricing", "availability": "", "source": "scraped" }
  ],
  "GTX 1050 Ti (4 GB)": [
    { "platform": "Salad", "price_usd": 0.015, "plan": "市场价", "country": "", "region": "", "note": "🟢 实时抓取 · 2026-06-15T12:12:59Z", "pricing_url": "https://salad.com/pricing", "availability": "", "source": "scraped" }
  ]
};
