// 运算盘 · 实时 GPU 价格数据
// 自动生成于: 2026-06-24 00:00 (北京时间)
// 由 fetch_prices.py 自动生成

var PRICE_FETCHED_AT = "2026-06-24 00:00 (北京时间)";
var PRICE_SCRAPE_SOURCES = {
  "Vast.ai": {
    "status": "ok",
    "gpu_count": 12
  },
  "RunPod": {
    "status": "ok",
    "gpu_count": 2
  },
  "Lambda Labs": {
    "status": "ok",
    "gpu_count": 4
  },
  "CoreWeave": {
    "status": "ok",
    "gpu_count": 5
  },
  "TensorDock": {
    "status": "ok",
    "gpu_count": 9
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
    "error": "Verda 页面未提取到价格数据（SPA 动态加载超时）"
  },
  "Hetzner": {
    "status": "failed",
    "gpu_count": 0,
    "error": "页面 JS 动态渲染，Playwright 也未提取到价格数据"
  },
  "OVHcloud": {
    "status": "failed",
    "gpu_count": 0,
    "error": "无法访问定价页面"
  },
  "Scaleway": {
    "status": "ok",
    "gpu_count": 5
  },
  "Genesis Cloud": {
    "status": "failed",
    "gpu_count": 0,
    "error": "Playwright 未提取到价格数据"
  },
  "NexGen Cloud": {
    "status": "ok",
    "gpu_count": 3
  },
  "Cudo Compute": {
    "status": "failed",
    "gpu_count": 0,
    "error": "Elementor 选项卡 AJAX 动态加载, 需手动交互或 API 授权"
  },
  "G-Core Labs": {
    "status": "failed",
    "gpu_count": 0,
    "error": "Playwright 未提取到价格数据"
  },
  "Cherry Servers": {
    "status": "failed",
    "gpu_count": 0,
    "error": "Playwright 未提取到价格数据"
  },
  "LeaderGPU": {
    "status": "failed",
    "gpu_count": 0,
    "error": "Playwright 未提取到价格数据"
  },
  "Leaseweb": {
    "status": "failed",
    "gpu_count": 0,
    "error": "Playwright 未提取到价格数据"
  },
  "Hostkey": {
    "status": "ok",
    "gpu_count": 14
  },
  "UpCloud": {
    "status": "ok",
    "gpu_count": 4
  },
  "Exoscale": {
    "status": "ok",
    "gpu_count": 7
  },
  "21Cloud": {
    "status": "failed",
    "gpu_count": 0,
    "error": "Playwright 未提取到价格数据"
  },
  "Servers.com": {
    "status": "failed",
    "gpu_count": 0,
    "error": "Playwright 未提取到价格数据"
  },
  "Mystic AI": {
    "status": "failed",
    "gpu_count": 0,
    "error": "Playwright 未提取到价格数据"
  },
  "DigitalOcean": {
    "status": "ok",
    "gpu_count": 5
  },
  "Vultr": {
    "status": "failed",
    "gpu_count": 0,
    "error": "Playwright 未提取到价格数据"
  },
  "FluidStack": {
    "status": "failed",
    "gpu_count": 0,
    "error": "Playwright 未提取到价格数据"
  },
  "Massed Compute": {
    "status": "ok",
    "gpu_count": 8
  },
  "Salad": {
    "status": "ok",
    "gpu_count": 22
  },
  "Hivelocity": {
    "status": "failed",
    "gpu_count": 0,
    "error": "Playwright 未提取到价格数据"
  },
  "SabrePC": {
    "status": "failed",
    "gpu_count": 0,
    "error": "Playwright 未提取到价格数据"
  },
  "Bizon": {
    "status": "failed",
    "gpu_count": 0,
    "error": "Playwright 未提取到价格数据"
  },
  "DataPacket": {
    "status": "failed",
    "gpu_count": 0,
    "error": "Playwright 未提取到价格数据"
  },
  "ServerMania": {
    "status": "failed",
    "gpu_count": 0,
    "error": "Playwright 未提取到价格数据"
  },
  "Monster API": {
    "status": "failed",
    "gpu_count": 0,
    "error": "Playwright 未提取到价格数据"
  },
  "Cerebrium": {
    "status": "ok",
    "gpu_count": 7
  },
  "Matpool": {
    "status": "failed",
    "gpu_count": 0,
    "error": "未提取到价格数据"
  },
  "AutoDL": {
    "status": "failed",
    "gpu_count": 0,
    "error": "未提取到价格数据（可能需要调整 Playwright 等待时间）"
  },
  "腾讯云": {
    "status": "failed",
    "gpu_count": 0,
    "error": "未捕获到 API 响应"
  },
  "IBM Cloud": {
    "status": "failed",
    "gpu_count": 0,
    "error": "Playwright 未提取到价格数据"
  },
  "Oracle Cloud": {
    "status": "ok",
    "gpu_count": 8
  },
  "AWS (Amazon EC2)": {
    "status": "ok",
    "gpu_count": 5
  },
  "Microsoft Azure": {
    "status": "ok",
    "gpu_count": 8
  },
  "Google Cloud": {
    "status": "failed",
    "gpu_count": 0,
    "error": "未提取到 GPU 价格"
  },
  "阿里云": {
    "status": "failed",
    "gpu_count": 0,
    "error": "国际站/中国站均未提取到 GPU 价格"
  },
  "华为云": {
    "status": "failed",
    "gpu_count": 0,
    "error": "未提取到 GPU 价格"
  },
  "火山引擎": {
    "status": "failed",
    "gpu_count": 0,
    "error": "未提取到 GPU 价格"
  }
};

var GPU_PRICING_LIVE = {
  "1080": [
    { "platform": "Hostkey", "price_usd": 0.11, "plan": "月租€75.0/月 ≈ €0.103/时", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://hostkey.com/gpu-dedicated-servers/", "availability": "", "source": "scraped" }
  ],
  "1080Ti": [
    { "platform": "Hostkey", "price_usd": 0.1, "plan": "月租€70.0/月 ≈ €0.096/时", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://hostkey.com/gpu-dedicated-servers/", "availability": "", "source": "scraped" }
  ],
  "2000 PRO": [
    { "platform": "Hostkey", "price_usd": 0.26, "plan": "月租€179.0/月 ≈ €0.245/时", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://hostkey.com/gpu-dedicated-servers/", "availability": "", "source": "scraped" }
  ],
  "6000 PRO": [
    { "platform": "Hostkey", "price_usd": 2.81, "plan": "月租€1900.0/月 ≈ €2.603/时", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://hostkey.com/gpu-dedicated-servers/", "availability": "", "source": "scraped" }
  ],
  "7900XTX": [
    { "platform": "Hostkey", "price_usd": 1.18, "plan": "月租€800.0/月 ≈ €1.096/时", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://hostkey.com/gpu-dedicated-servers/", "availability": "", "source": "scraped" }
  ],
  "A100 SXM4": [
    { "platform": "Vast.ai", "price_usd": 1.07, "plan": "市场最低价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://vast.ai/pricing", "availability": "共8张", "source": "scraped" }
  ],
  "A4000": [
    { "platform": "Hostkey", "price_usd": 0.32, "plan": "月租€219.0/月 ≈ €0.300/时", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://hostkey.com/gpu-dedicated-servers/", "availability": "", "source": "scraped" }
  ],
  "A5000": [
    { "platform": "Hostkey", "price_usd": 0.41, "plan": "月租€279.0/月 ≈ €0.382/时", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://hostkey.com/gpu-dedicated-servers/", "availability": "", "source": "scraped" }
  ],
  "AMD R9700": [
    { "platform": "Hostkey", "price_usd": 0.5, "plan": "月租€339.0/月 ≈ €0.464/时", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://hostkey.com/gpu-dedicated-servers/", "availability": "", "source": "scraped" }
  ],
  "AMD Radeon Instinct MI300X": [
    { "platform": "Microsoft Azure", "price_usd": 1.1088, "plan": "Azure VM (8× GPU)", "country": "", "region": "", "note": "实时抓取 · 2026-06-24 00:00 (北京时间)", "pricing_url": "", "availability": "", "source": "scraped" },
    { "platform": "Oracle Cloud", "price_usd": 6.0, "plan": "市场价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.oracle.com/cloud/compute/pricing/", "availability": "", "source": "scraped" }
  ],
  "B300-SXM": [
    { "platform": "Scaleway", "price_usd": 64.8, "plan": "€60.00/时 (最小配置)", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.scaleway.com/en/pricing/", "availability": "", "source": "scraped" }
  ],
  "GTX 1050 Ti (4 GB)": [
    { "platform": "Salad", "price_usd": 0.015, "plan": "市场价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://salad.com/pricing", "availability": "", "source": "scraped" }
  ],
  "GTX 1060 (6 GB)": [
    { "platform": "Salad", "price_usd": 0.02, "plan": "市场价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://salad.com/pricing", "availability": "", "source": "scraped" }
  ],
  "GTX 1070 (8 GB)": [
    { "platform": "Salad", "price_usd": 0.02, "plan": "市场价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://salad.com/pricing", "availability": "", "source": "scraped" }
  ],
  "GTX 1080 (8 GB)": [
    { "platform": "Salad", "price_usd": 0.02, "plan": "市场价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://salad.com/pricing", "availability": "", "source": "scraped" }
  ],
  "GTX 1650 (4 GB)": [
    { "platform": "Salad", "price_usd": 0.02, "plan": "市场价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://salad.com/pricing", "availability": "", "source": "scraped" }
  ],
  "GTX 1660 (6 GB)": [
    { "platform": "Salad", "price_usd": 0.02, "plan": "市场价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://salad.com/pricing", "availability": "", "source": "scraped" }
  ],
  "GTX 1660 Super (6 GB)": [
    { "platform": "Salad", "price_usd": 0.02, "plan": "市场价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://salad.com/pricing", "availability": "", "source": "scraped" }
  ],
  "H100-SXM": [
    { "platform": "Scaleway", "price_usd": 7.15, "plan": "€6.62/时 (最小配置)", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.scaleway.com/en/pricing/", "availability": "", "source": "scraped" }
  ],
  "NVIDIA A100 (40GB PCIe)": [
    { "platform": "Massed Compute", "price_usd": 1.35, "plan": "按需", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.massedcompute.com/pricing", "availability": "", "source": "scraped" },
    { "platform": "JarvisLabs", "price_usd": 1.49, "plan": "按需", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://jarvislabs.ai/pricing/", "availability": "", "source": "scraped" },
    { "platform": "TensorDock", "price_usd": 1.5, "plan": "GPU起价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.tensordock.com/cloud-gpus.html", "availability": "", "source": "scraped" }
  ],
  "NVIDIA A100 (80GB SXM)": [
    { "platform": "Microsoft Azure", "price_usd": 0.6799, "plan": "Azure VM (8× GPU)", "country": "", "region": "", "note": "实时抓取 · 2026-06-24 00:00 (北京时间)", "pricing_url": "", "availability": "", "source": "scraped" },
    { "platform": "AWS (Amazon EC2)", "price_usd": 1.0368, "plan": "按需", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "", "availability": "", "source": "scraped" },
    { "platform": "NexGen Cloud", "price_usd": 1.35, "plan": "按需", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.hyperstack.cloud/gpu-pricing", "availability": "", "source": "scraped" },
    { "platform": "Massed Compute", "price_usd": 1.35, "plan": "按需", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.massedcompute.com/pricing", "availability": "", "source": "scraped" },
    { "platform": "JarvisLabs", "price_usd": 1.49, "plan": "按需", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://jarvislabs.ai/pricing/", "availability": "", "source": "scraped" },
    { "platform": "TensorDock", "price_usd": 1.8, "plan": "GPU起价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.tensordock.com/cloud-gpus.html", "availability": "", "source": "scraped" },
    { "platform": "Hostkey", "price_usd": 1.92, "plan": "月租€1300.0/月 ≈ €1.781/时", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://hostkey.com/gpu-dedicated-servers/", "availability": "", "source": "scraped" },
    { "platform": "Cerebrium", "price_usd": 2.1, "plan": "市场价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.cerebrium.ai/pricing", "availability": "", "source": "scraped" },
    { "platform": "Lambda Labs", "price_usd": 2.79, "plan": "市场价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://lambda.ai/pricing", "availability": "", "source": "scraped" },
    { "platform": "Oracle Cloud", "price_usd": 3.05, "plan": "市场价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.oracle.com/cloud/compute/pricing/", "availability": "", "source": "scraped" },
    { "platform": "Replicate", "price_usd": 3.51, "plan": "市场价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://replicate.com/pricing", "availability": "", "source": "scraped" }
  ],
  "NVIDIA A10G": [
    { "platform": "Microsoft Azure", "price_usd": 0.127, "plan": "Azure VM (2× GPU)", "country": "", "region": "", "note": "实时抓取 · 2026-06-24 00:00 (北京时间)", "pricing_url": "", "availability": "", "source": "scraped" },
    { "platform": "AWS (Amazon EC2)", "price_usd": 2.208, "plan": "按需", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "", "availability": "", "source": "scraped" }
  ],
  "NVIDIA A30": [
    { "platform": "Exoscale", "price_usd": 1.23, "plan": "最小配置 (API)", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.exoscale.com/gpu/", "availability": "", "source": "scraped" }
  ],
  "NVIDIA B200": [
    { "platform": "Oracle Cloud", "price_usd": 4.0, "plan": "市场价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.oracle.com/cloud/compute/pricing/", "availability": "", "source": "scraped" },
    { "platform": "UpCloud", "price_usd": 4.86, "plan": "按需", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://upcloud.com/pricing/", "availability": "", "source": "scraped" },
    { "platform": "Vast.ai", "price_usd": 5.62, "plan": "市场最低价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "scraped" },
    { "platform": "Cerebrium", "price_usd": 6.01, "plan": "市场价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.cerebrium.ai/pricing", "availability": "", "source": "scraped" },
    { "platform": "CoreWeave", "price_usd": 8.6, "plan": "按需", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.coreweave.com/pricing", "availability": "", "source": "scraped" },
    { "platform": "Lambda Labs", "price_usd": 9.86, "plan": "市场价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://lambda.ai/pricing", "availability": "", "source": "scraped" }
  ],
  "NVIDIA B300": [
    { "platform": "DigitalOcean", "price_usd": 5.65, "plan": "按需", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.digitalocean.com/pricing/gpu-droplets", "availability": "", "source": "scraped" }
  ],
  "NVIDIA GH200": [
    { "platform": "CoreWeave", "price_usd": 6.5, "plan": "按需", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.coreweave.com/pricing", "availability": "", "source": "scraped" }
  ],
  "NVIDIA H100 (80GB SXM)": [
    { "platform": "Microsoft Azure", "price_usd": 1.2899, "plan": "Azure VM (1× GPU)", "country": "", "region": "", "note": "实时抓取 · 2026-06-24 00:00 (北京时间)", "pricing_url": "", "availability": "", "source": "scraped" },
    { "platform": "Vast.ai", "price_usd": 1.47, "plan": "市场最低价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://vast.ai/pricing", "availability": "共2张", "source": "scraped" },
    { "platform": "AWS (Amazon EC2)", "price_usd": 1.8432, "plan": "按需", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "", "availability": "", "source": "scraped" },
    { "platform": "NexGen Cloud", "price_usd": 1.9, "plan": "按需", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.hyperstack.cloud/gpu-pricing", "availability": "", "source": "scraped" },
    { "platform": "UpCloud", "price_usd": 1.93, "plan": "按需", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://upcloud.com/pricing/", "availability": "", "source": "scraped" },
    { "platform": "RunPod", "price_usd": 1.99, "plan": "按需", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.runpod.io/pricing", "availability": "", "source": "scraped" },
    { "platform": "Paperspace", "price_usd": 2.24, "plan": "按需", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.paperspace.com/pricing", "availability": "", "source": "scraped" },
    { "platform": "TensorDock", "price_usd": 2.25, "plan": "GPU起价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.tensordock.com/cloud-gpus.html", "availability": "", "source": "scraped" },
    { "platform": "Hostkey", "price_usd": 2.35, "plan": "月租€1590.0/月 ≈ €2.178/时", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://hostkey.com/gpu-dedicated-servers/", "availability": "", "source": "scraped" },
    { "platform": "Oracle Cloud", "price_usd": 2.5, "plan": "市场价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.oracle.com/cloud/compute/pricing/", "availability": "", "source": "scraped" },
    { "platform": "JarvisLabs", "price_usd": 2.69, "plan": "按需", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://jarvislabs.ai/pricing/", "availability": "", "source": "scraped" },
    { "platform": "Massed Compute", "price_usd": 2.73, "plan": "按需", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.massedcompute.com/pricing", "availability": "", "source": "scraped" },
    { "platform": "Saturn Cloud", "price_usd": 2.95, "plan": "市场价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://saturncloud.io/pricing/", "availability": "", "source": "scraped" },
    { "platform": "Scaleway", "price_usd": 3.1, "plan": "€2.87/时 (最小配置)", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.scaleway.com/en/pricing/", "availability": "", "source": "scraped" },
    { "platform": "DigitalOcean", "price_usd": 3.39, "plan": "按需", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.digitalocean.com/pricing/gpu-droplets", "availability": "", "source": "scraped" },
    { "platform": "Cerebrium", "price_usd": 3.4, "plan": "市场价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.cerebrium.ai/pricing", "availability": "", "source": "scraped" },
    { "platform": "Lambda Labs", "price_usd": 3.99, "plan": "市场价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://lambda.ai/pricing", "availability": "", "source": "scraped" },
    { "platform": "Replicate", "price_usd": 5.49, "plan": "市场价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://replicate.com/pricing", "availability": "", "source": "scraped" },
    { "platform": "CoreWeave", "price_usd": 6.16, "plan": "按需", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.coreweave.com/pricing", "availability": "", "source": "scraped" }
  ],
  "NVIDIA H100 (NVL)": [
    { "platform": "Massed Compute", "price_usd": 5.84, "plan": "按需", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.massedcompute.com/pricing", "availability": "", "source": "scraped" }
  ],
  "NVIDIA H200": [
    { "platform": "Microsoft Azure", "price_usd": 2.12, "plan": "Azure VM (8× GPU)", "country": "", "region": "", "note": "实时抓取 · 2026-06-24 00:00 (北京时间)", "pricing_url": "", "availability": "", "source": "scraped" },
    { "platform": "Oracle Cloud", "price_usd": 2.5, "plan": "市场价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.oracle.com/cloud/compute/pricing/", "availability": "", "source": "scraped" },
    { "platform": "Saturn Cloud", "price_usd": 2.95, "plan": "市场价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://saturncloud.io/pricing/", "availability": "", "source": "scraped" },
    { "platform": "Vast.ai", "price_usd": 3.16, "plan": "市场最低价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://vast.ai/pricing", "availability": "共46张", "source": "scraped" },
    { "platform": "DigitalOcean", "price_usd": 3.44, "plan": "按需", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.digitalocean.com/pricing/gpu-droplets", "availability": "", "source": "scraped" },
    { "platform": "NexGen Cloud", "price_usd": 3.5, "plan": "按需", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.hyperstack.cloud/gpu-pricing", "availability": "", "source": "scraped" },
    { "platform": "Massed Compute", "price_usd": 3.62, "plan": "按需", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.massedcompute.com/pricing", "availability": "", "source": "scraped" },
    { "platform": "Cerebrium", "price_usd": 4.2, "plan": "市场价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.cerebrium.ai/pricing", "availability": "", "source": "scraped" },
    { "platform": "CoreWeave", "price_usd": 6.31, "plan": "按需", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.coreweave.com/pricing", "availability": "", "source": "scraped" }
  ],
  "NVIDIA L4": [
    { "platform": "Google Colab", "price_usd": 0.0, "plan": "订阅制 (Colab Pro+)", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://colab.research.google.com/signup", "availability": "", "source": "scraped" },
    { "platform": "Microsoft Azure", "price_usd": 0.075, "plan": "Azure VM (1× GPU)", "country": "", "region": "", "note": "实时抓取 · 2026-06-24 00:00 (北京时间)", "pricing_url": "", "availability": "", "source": "scraped" },
    { "platform": "JarvisLabs", "price_usd": 0.44, "plan": "按需", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://jarvislabs.ai/pricing/", "availability": "", "source": "scraped" },
    { "platform": "UpCloud", "price_usd": 0.63, "plan": "按需", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://upcloud.com/pricing/", "availability": "", "source": "scraped" },
    { "platform": "Cerebrium", "price_usd": 0.8, "plan": "市场价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.cerebrium.ai/pricing", "availability": "", "source": "scraped" },
    { "platform": "Scaleway", "price_usd": 0.85, "plan": "€0.79/时 (最小配置)", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.scaleway.com/en/pricing/", "availability": "", "source": "scraped" },
    { "platform": "DigitalOcean", "price_usd": 1.0, "plan": "按需", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.digitalocean.com/pricing/gpu-droplets", "availability": "", "source": "scraped" },
    { "platform": "Massed Compute", "price_usd": 1.0, "plan": "按需", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.massedcompute.com/pricing", "availability": "", "source": "scraped" }
  ],
  "NVIDIA L40S": [
    { "platform": "Massed Compute", "price_usd": 0.88, "plan": "按需", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.massedcompute.com/pricing", "availability": "", "source": "scraped" },
    { "platform": "Oracle Cloud", "price_usd": 0.88, "plan": "市场价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.oracle.com/cloud/compute/pricing/", "availability": "", "source": "scraped" },
    { "platform": "TensorDock", "price_usd": 0.95, "plan": "GPU起价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.tensordock.com/cloud-gpus.html", "availability": "", "source": "scraped" },
    { "platform": "UpCloud", "price_usd": 1.2, "plan": "按需", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://upcloud.com/pricing/", "availability": "", "source": "scraped" },
    { "platform": "DigitalOcean", "price_usd": 1.57, "plan": "按需", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.digitalocean.com/pricing/gpu-droplets", "availability": "", "source": "scraped" },
    { "platform": "Scaleway", "price_usd": 1.59, "plan": "€1.47/时 (最小配置)", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.scaleway.com/en/pricing/", "availability": "", "source": "scraped" },
    { "platform": "Cerebrium", "price_usd": 1.95, "plan": "市场价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.cerebrium.ai/pricing", "availability": "", "source": "scraped" },
    { "platform": "AWS (Amazon EC2)", "price_usd": 2.208, "plan": "按需", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "", "availability": "", "source": "scraped" },
    { "platform": "CoreWeave", "price_usd": 2.25, "plan": "按需", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.coreweave.com/pricing", "availability": "", "source": "scraped" }
  ],
  "NVIDIA RTX 2080 Ti": [
    { "platform": "Salad", "price_usd": 0.06, "plan": "市场价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://salad.com/pricing", "availability": "", "source": "scraped" }
  ],
  "NVIDIA RTX 3060 / 3060 Ti": [
    { "platform": "Salad", "price_usd": 0.04, "plan": "市场价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://salad.com/pricing", "availability": "", "source": "scraped" }
  ],
  "NVIDIA RTX 3070 / 3070 Ti": [
    { "platform": "Salad", "price_usd": 0.06, "plan": "市场价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://salad.com/pricing", "availability": "", "source": "scraped" }
  ],
  "NVIDIA RTX 3080 / 3080 Ti": [
    { "platform": "Salad", "price_usd": 0.08, "plan": "市场价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://salad.com/pricing", "availability": "", "source": "scraped" },
    { "platform": "Hostkey", "price_usd": 0.28, "plan": "月租€190.0/月 ≈ €0.260/时", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://hostkey.com/gpu-dedicated-servers/", "availability": "", "source": "scraped" },
    { "platform": "Exoscale", "price_usd": 0.92, "plan": "最小配置 (API)", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.exoscale.com/gpu/", "availability": "", "source": "scraped" }
  ],
  "NVIDIA RTX 3090 / 3090 Ti": [
    { "platform": "Salad", "price_usd": 0.1, "plan": "市场价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://salad.com/pricing", "availability": "", "source": "scraped" },
    { "platform": "TensorDock", "price_usd": 0.2, "plan": "GPU起价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.tensordock.com/cloud-gpus.html", "availability": "", "source": "scraped" },
    { "platform": "Hostkey", "price_usd": 0.47, "plan": "月租€319.0/月 ≈ €0.437/时", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://hostkey.com/gpu-dedicated-servers/", "availability": "", "source": "scraped" }
  ],
  "NVIDIA RTX 4060 Ti": [
    { "platform": "Salad", "price_usd": 0.08, "plan": "市场价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://salad.com/pricing", "availability": "", "source": "scraped" }
  ],
  "NVIDIA RTX 4070 Ti / 4070": [
    { "platform": "Salad", "price_usd": 0.08, "plan": "市场价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://salad.com/pricing", "availability": "", "source": "scraped" }
  ],
  "NVIDIA RTX 4080 / 4080 Super": [
    { "platform": "Salad", "price_usd": 0.11, "plan": "市场价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://salad.com/pricing", "availability": "", "source": "scraped" }
  ],
  "NVIDIA RTX 4090": [
    { "platform": "Salad", "price_usd": 0.16, "plan": "市场价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://salad.com/pricing", "availability": "", "source": "scraped" },
    { "platform": "Vast.ai", "price_usd": 0.17, "plan": "市场最低价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://vast.ai/pricing", "availability": "共6张", "source": "scraped" },
    { "platform": "RunPod", "price_usd": 0.34, "plan": "按需", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.runpod.io/pricing", "availability": "", "source": "scraped" },
    { "platform": "TensorDock", "price_usd": 0.35, "plan": "GPU起价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.tensordock.com/cloud-gpus.html", "availability": "", "source": "scraped" },
    { "platform": "Hostkey", "price_usd": 1.11, "plan": "月租€750.0/月 ≈ €1.027/时", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://hostkey.com/gpu-dedicated-servers/", "availability": "", "source": "scraped" }
  ],
  "NVIDIA RTX 6000 Ada / A6000": [
    { "platform": "Microsoft Azure", "price_usd": 0.1836, "plan": "Azure VM (1× GPU)", "country": "", "region": "", "note": "实时抓取 · 2026-06-24 00:00 (北京时间)", "pricing_url": "", "availability": "", "source": "scraped" },
    { "platform": "Massed Compute", "price_usd": 0.57, "plan": "按需", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.massedcompute.com/pricing", "availability": "", "source": "scraped" },
    { "platform": "TensorDock", "price_usd": 0.75, "plan": "GPU起价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.tensordock.com/cloud-gpus.html", "availability": "", "source": "scraped" },
    { "platform": "Vast.ai", "price_usd": 0.8, "plan": "市场最低价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://vast.ai/pricing", "availability": "共22张", "source": "scraped" },
    { "platform": "Exoscale", "price_usd": 2.15, "plan": "最小配置 (API)", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.exoscale.com/gpu/", "availability": "", "source": "scraped" }
  ],
  "NVIDIA RTX A5000": [
    { "platform": "Exoscale", "price_usd": 1.34, "plan": "最小配置 (API)", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.exoscale.com/gpu/", "availability": "", "source": "scraped" }
  ],
  "NVIDIA T4": [
    { "platform": "Google Colab", "price_usd": 0.0, "plan": "订阅制 (Colab Pro+)", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://colab.research.google.com/signup", "availability": "", "source": "scraped" },
    { "platform": "Microsoft Azure", "price_usd": 0.0684, "plan": "Azure VM (1× GPU)", "country": "", "region": "", "note": "实时抓取 · 2026-06-24 00:00 (北京时间)", "pricing_url": "", "availability": "", "source": "scraped" },
    { "platform": "Cerebrium", "price_usd": 0.59, "plan": "市场价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.cerebrium.ai/pricing", "availability": "", "source": "scraped" },
    { "platform": "Replicate", "price_usd": 0.81, "plan": "市场价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://replicate.com/pricing", "availability": "", "source": "scraped" },
    { "platform": "Saturn Cloud", "price_usd": 1.0, "plan": "市场价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://saturncloud.io/pricing/", "availability": "", "source": "scraped" },
    { "platform": "Exoscale", "price_usd": 1.05, "plan": "最小配置 (API)", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.exoscale.com/gpu/", "availability": "", "source": "scraped" }
  ],
  "NVIDIA Tesla P100 / P40": [
    { "platform": "Oracle Cloud", "price_usd": 1.0, "plan": "市场价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.oracle.com/cloud/compute/pricing/", "availability": "", "source": "scraped" },
    { "platform": "Exoscale", "price_usd": 1.17, "plan": "最小配置 (API)", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.exoscale.com/gpu/", "availability": "", "source": "scraped" }
  ],
  "NVIDIA V100": [
    { "platform": "Vast.ai", "price_usd": 0.11, "plan": "市场最低价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://vast.ai/pricing", "availability": "共30张", "source": "scraped" },
    { "platform": "TensorDock", "price_usd": 0.17, "plan": "GPU起价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.tensordock.com/cloud-gpus.html", "availability": "", "source": "scraped" },
    { "platform": "Lambda Labs", "price_usd": 0.79, "plan": "市场价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://lambda.ai/pricing", "availability": "", "source": "scraped" },
    { "platform": "Saturn Cloud", "price_usd": 1.095, "plan": "市场价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://saturncloud.io/pricing/", "availability": "", "source": "scraped" },
    { "platform": "Exoscale", "price_usd": 1.38, "plan": "最小配置 (API)", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.exoscale.com/gpu/", "availability": "", "source": "scraped" },
    { "platform": "Paperspace", "price_usd": 1.84, "plan": "按需", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.paperspace.com/pricing", "availability": "", "source": "scraped" },
    { "platform": "AWS (Amazon EC2)", "price_usd": 2.944, "plan": "按需", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "", "availability": "", "source": "scraped" },
    { "platform": "Oracle Cloud", "price_usd": 2.95, "plan": "市场价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.oracle.com/cloud/compute/pricing/", "availability": "", "source": "scraped" }
  ],
  "P100": [
    { "platform": "Google Colab", "price_usd": 0.0, "plan": "订阅制 (Colab Pro+)", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://colab.research.google.com/signup", "availability": "", "source": "scraped" }
  ],
  "RTX 2060 (6 GB)": [
    { "platform": "Salad", "price_usd": 0.02, "plan": "市场价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://salad.com/pricing", "availability": "", "source": "scraped" }
  ],
  "RTX 2070 (8 GB)": [
    { "platform": "Salad", "price_usd": 0.02, "plan": "市场价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://salad.com/pricing", "availability": "", "source": "scraped" }
  ],
  "RTX 2080": [
    { "platform": "Salad", "price_usd": 0.05, "plan": "市场价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://salad.com/pricing", "availability": "", "source": "scraped" }
  ],
  "RTX 3050 (8 GB)": [
    { "platform": "Salad", "price_usd": 0.03, "plan": "市场价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://salad.com/pricing", "availability": "", "source": "scraped" }
  ],
  "RTX 4070 Ti Super (16 GB)": [
    { "platform": "Salad", "price_usd": 0.09, "plan": "市场价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://salad.com/pricing", "availability": "", "source": "scraped" }
  ],
  "RTX 4500": [
    { "platform": "Vast.ai", "price_usd": 0.27, "plan": "市场最低价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "scraped" }
  ],
  "RTX 5000": [
    { "platform": "Vast.ai", "price_usd": 1.07, "plan": "市场最低价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "scraped" }
  ],
  "RTX 5070 Ti": [
    { "platform": "Vast.ai", "price_usd": 0.13, "plan": "市场最低价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://vast.ai/pricing", "availability": "共2张", "source": "scraped" }
  ],
  "RTX 5080": [
    { "platform": "Vast.ai", "price_usd": 0.21, "plan": "市场最低价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://vast.ai/pricing", "availability": "共4张", "source": "scraped" }
  ],
  "RTX 5090": [
    { "platform": "Vast.ai", "price_usd": 0.32, "plan": "市场最低价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://vast.ai/pricing", "availability": "共17张", "source": "scraped" },
    { "platform": "Hostkey", "price_usd": 0.75, "plan": "月租€510.0/月 ≈ €0.699/时", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://hostkey.com/gpu-dedicated-servers/", "availability": "", "source": "scraped" }
  ],
  "RTX A4000 16GB": [
    { "platform": "TensorDock", "price_usd": 0.1, "plan": "GPU起价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.tensordock.com/cloud-gpus.html", "availability": "", "source": "scraped" }
  ],
  "RTX A5000 (24 GB)": [
    { "platform": "Salad", "price_usd": 0.09, "plan": "市场价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://salad.com/pricing", "availability": "", "source": "scraped" }
  ],
  "T3": [
    { "platform": "Saturn Cloud", "price_usd": 0.15, "plan": "市场价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://saturncloud.io/pricing/", "availability": "", "source": "scraped" }
  ],
  "t3": [
    { "platform": "Saturn Cloud", "price_usd": 0.15, "plan": "市场价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://saturncloud.io/pricing/", "availability": "", "source": "scraped" }
  ]
};
