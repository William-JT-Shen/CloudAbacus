// 运算盘 · GPU 价格数据 (实时 + 参考)
// 生成时间: 2026-06-24 18:00 (北京时间)
// 实时平台: 21 | 参考平台: 122 | GPU分类: 83 | 总条目: 364
// 覆盖 data.js 全部 106 个平台

var PRICE_FETCHED_AT = "2026-06-24 18:00 (北京时间)";
var PRICE_SCRAPE_SOURCES = {
  "AWS (Amazon EC2)": {
    "status": "ok",
    "gpu_count": 10
  },
  "Cerebrium": {
    "status": "reference",
    "gpu_count": 8
  },
  "CoreWeave": {
    "status": "reference",
    "gpu_count": 9
  },
  "DigitalOcean": {
    "status": "reference",
    "gpu_count": 6
  },
  "Exoscale": {
    "status": "reference",
    "gpu_count": 8
  },
  "Hostkey": {
    "status": "reference",
    "gpu_count": 15
  },
  "JarvisLabs": {
    "status": "reference",
    "gpu_count": 7
  },
  "Lambda Labs": {
    "status": "reference",
    "gpu_count": 8
  },
  "Massed Compute": {
    "status": "reference",
    "gpu_count": 9
  },
  "Microsoft Azure": {
    "status": "reference",
    "gpu_count": 9
  },
  "NexGen Cloud": {
    "status": "reference",
    "gpu_count": 4
  },
  "Oracle Cloud": {
    "status": "ok",
    "gpu_count": 8
  },
  "Paperspace": {
    "status": "reference",
    "gpu_count": 4
  },
  "Replicate": {
    "status": "reference",
    "gpu_count": 4
  },
  "RunPod": {
    "status": "ok",
    "gpu_count": 2
  },
  "Salad": {
    "status": "reference",
    "gpu_count": 25
  },
  "Saturn Cloud": {
    "status": "reference",
    "gpu_count": 7
  },
  "Scaleway": {
    "status": "ok",
    "gpu_count": 5
  },
  "TensorDock": {
    "status": "reference",
    "gpu_count": 13
  },
  "UpCloud": {
    "status": "reference",
    "gpu_count": 5
  },
  "Vast.ai": {
    "status": "reference",
    "gpu_count": 30
  },
  "21Cloud": {
    "status": "reference",
    "gpu_count": 1
  },
  "Akamai Linode": {
    "status": "reference",
    "gpu_count": 1
  },
  "Akash Network": {
    "status": "reference",
    "gpu_count": 1
  },
  "Anyscale": {
    "status": "reference",
    "gpu_count": 1
  },
  "Applied Digital": {
    "status": "reference",
    "gpu_count": 1
  },
  "Aruba Cloud": {
    "status": "reference",
    "gpu_count": 1
  },
  "AutoDL": {
    "status": "reference",
    "gpu_count": 4
  },
  "BentoML (BentoCloud)": {
    "status": "reference",
    "gpu_count": 1
  },
  "Bizon": {
    "status": "reference",
    "gpu_count": 1
  },
  "Cherry Servers": {
    "status": "reference",
    "gpu_count": 1
  },
  "Cirrascale": {
    "status": "reference",
    "gpu_count": 2
  },
  "CodeOcean": {
    "status": "reference",
    "gpu_count": 1
  },
  "Coiled": {
    "status": "reference",
    "gpu_count": 1
  },
  "Cudo Compute": {
    "status": "reference",
    "gpu_count": 6
  },
  "DataCrunch": {
    "status": "reference",
    "gpu_count": 5
  },
  "DataPacket": {
    "status": "reference",
    "gpu_count": 1
  },
  "Databricks": {
    "status": "reference",
    "gpu_count": 1
  },
  "Dedicated.com": {
    "status": "reference",
    "gpu_count": 1
  },
  "Deepnote": {
    "status": "reference",
    "gpu_count": 1
  },
  "Equinix Metal": {
    "status": "reference",
    "gpu_count": 1
  },
  "Fireworks.ai": {
    "status": "reference",
    "gpu_count": 1
  },
  "FluidStack": {
    "status": "reference",
    "gpu_count": 3
  },
  "G-Core Labs": {
    "status": "reference",
    "gpu_count": 2
  },
  "Genesis Cloud": {
    "status": "reference",
    "gpu_count": 3
  },
  "Golem Network": {
    "status": "reference",
    "gpu_count": 1
  },
  "Google Cloud (GCP)": {
    "status": "reference",
    "gpu_count": 8
  },
  "Google Colab": {
    "status": "reference",
    "gpu_count": 2
  },
  "Hetzner": {
    "status": "reference",
    "gpu_count": 2
  },
  "Hivelocity": {
    "status": "reference",
    "gpu_count": 1
  },
  "Hugging Face (Inference Endpoints)": {
    "status": "reference",
    "gpu_count": 1
  },
  "IBM Cloud": {
    "status": "reference",
    "gpu_count": 1
  },
  "IIJ GIO": {
    "status": "reference",
    "gpu_count": 1
  },
  "KT Cloud": {
    "status": "reference",
    "gpu_count": 1
  },
  "LeaderGPU": {
    "status": "reference",
    "gpu_count": 2
  },
  "Leaseweb": {
    "status": "reference",
    "gpu_count": 1
  },
  "Matpool (矩池云)": {
    "status": "reference",
    "gpu_count": 2
  },
  "Mining Rig Rentals": {
    "status": "reference",
    "gpu_count": 1
  },
  "Modal": {
    "status": "reference",
    "gpu_count": 1
  },
  "Monster API": {
    "status": "reference",
    "gpu_count": 1
  },
  "Mystic AI": {
    "status": "reference",
    "gpu_count": 1
  },
  "NVIDIA DGX Cloud": {
    "status": "reference",
    "gpu_count": 2
  },
  "Naver Cloud": {
    "status": "reference",
    "gpu_count": 1
  },
  "NiceHash": {
    "status": "reference",
    "gpu_count": 1
  },
  "OVHcloud": {
    "status": "reference",
    "gpu_count": 5
  },
  "OctoML (OctoAI)": {
    "status": "reference",
    "gpu_count": 1
  },
  "Oracle Cloud Infrastructure": {
    "status": "reference",
    "gpu_count": 2
  },
  "PhoenixNAP": {
    "status": "reference",
    "gpu_count": 1
  },
  "Psychz": {
    "status": "reference",
    "gpu_count": 1
  },
  "Q Blocks": {
    "status": "reference",
    "gpu_count": 1
  },
  "QuadraNet": {
    "status": "reference",
    "gpu_count": 1
  },
  "Rackspace Technology": {
    "status": "reference",
    "gpu_count": 1
  },
  "Render Network": {
    "status": "reference",
    "gpu_count": 1
  },
  "Rescale": {
    "status": "reference",
    "gpu_count": 1
  },
  "RunPod (Community Cloud)": {
    "status": "reference",
    "gpu_count": 13
  },
  "RunPod (Secure Cloud)": {
    "status": "reference",
    "gpu_count": 4
  },
  "SabrePC": {
    "status": "reference",
    "gpu_count": 1
  },
  "Sakura Internet": {
    "status": "reference",
    "gpu_count": 1
  },
  "ServerMania": {
    "status": "reference",
    "gpu_count": 1
  },
  "Servers.com": {
    "status": "reference",
    "gpu_count": 1
  },
  "T-Systems (Open Telekom Cloud)": {
    "status": "reference",
    "gpu_count": 1
  },
  "Together AI": {
    "status": "reference",
    "gpu_count": 1
  },
  "TurnKey Internet": {
    "status": "reference",
    "gpu_count": 1
  },
  "UCloud": {
    "status": "reference",
    "gpu_count": 1
  },
  "Vast.ai (1080 Ti)": {
    "status": "reference",
    "gpu_count": 1
  },
  "Vast.ai (1080)": {
    "status": "reference",
    "gpu_count": 1
  },
  "Vast.ai (6600 XT)": {
    "status": "reference",
    "gpu_count": 1
  },
  "Vast.ai (6700 XT)": {
    "status": "reference",
    "gpu_count": 1
  },
  "Vast.ai (6800 XT)": {
    "status": "reference",
    "gpu_count": 1
  },
  "Vast.ai (6800)": {
    "status": "reference",
    "gpu_count": 1
  },
  "Vast.ai (6900 XT)": {
    "status": "reference",
    "gpu_count": 1
  },
  "Vast.ai (7600)": {
    "status": "reference",
    "gpu_count": 1
  },
  "Vast.ai (7700 XT)": {
    "status": "reference",
    "gpu_count": 1
  },
  "Vast.ai (7800 XT)": {
    "status": "reference",
    "gpu_count": 1
  },
  "Vast.ai (7900 XT)": {
    "status": "reference",
    "gpu_count": 1
  },
  "Vast.ai (7900 XTX)": {
    "status": "reference",
    "gpu_count": 1
  },
  "Vast.ai (K80)": {
    "status": "reference",
    "gpu_count": 1
  },
  "Vast.ai (M40)": {
    "status": "reference",
    "gpu_count": 1
  },
  "Vast.ai (P100)": {
    "status": "reference",
    "gpu_count": 1
  },
  "Vast.ai (P40)": {
    "status": "reference",
    "gpu_count": 1
  },
  "Vast.ai (RTX 6000 Ada)": {
    "status": "reference",
    "gpu_count": 1
  },
  "Vultr": {
    "status": "reference",
    "gpu_count": 5
  },
  "Yandex Cloud": {
    "status": "reference",
    "gpu_count": 1
  },
  "上海超算中心 (SSCS)": {
    "status": "reference",
    "gpu_count": 1
  },
  "中国移动云 (China Mobile Cloud)": {
    "status": "reference",
    "gpu_count": 1
  },
  "之江实验室 (Zhejiang Lab)": {
    "status": "reference",
    "gpu_count": 1
  },
  "京东云 (JD Cloud)": {
    "status": "reference",
    "gpu_count": 1
  },
  "北京超级云计算中心 (BLSC)": {
    "status": "reference",
    "gpu_count": 1
  },
  "华为云 (Huawei Cloud)": {
    "status": "reference",
    "gpu_count": 3
  },
  "合肥先进计算中心 (Hefei ACC)": {
    "status": "reference",
    "gpu_count": 1
  },
  "国家超算天津中心 (NSCC-TJ)": {
    "status": "reference",
    "gpu_count": 1
  },
  "国家超算广州中心 (NSCC-GZ)": {
    "status": "reference",
    "gpu_count": 1
  },
  "国家超算无锡中心 (NSCC-WX)": {
    "status": "reference",
    "gpu_count": 1
  },
  "国家超算深圳中心 (NSCC-SZ)": {
    "status": "reference",
    "gpu_count": 1
  },
  "天翼云 (China Telecom e-Surfing Cloud)": {
    "status": "reference",
    "gpu_count": 1
  },
  "并行科技 (Paratera)": {
    "status": "reference",
    "gpu_count": 1
  },
  "极视角 (Video++ AI Cloud)": {
    "status": "reference",
    "gpu_count": 1
  },
  "浪潮云 (Inspur Cloud)": {
    "status": "reference",
    "gpu_count": 1
  },
  "火山引擎 (Volcengine)": {
    "status": "reference",
    "gpu_count": 2
  },
  "百度智能云 (Baidu AI Cloud)": {
    "status": "reference",
    "gpu_count": 2
  },
  "联通云 (China Unicom Cloud)": {
    "status": "reference",
    "gpu_count": 1
  },
  "腾讯云 (Tencent Cloud)": {
    "status": "reference",
    "gpu_count": 3
  },
  "金山云 (Kingsoft Cloud)": {
    "status": "reference",
    "gpu_count": 1
  },
  "阿里云 (Alibaba Cloud)": {
    "status": "reference",
    "gpu_count": 3
  },
  "青云 (QingCloud)": {
    "status": "reference",
    "gpu_count": 1
  },
  "鹏城云脑 (Pengcheng Cloud Brain)": {
    "status": "reference",
    "gpu_count": 2
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
  "AMD Instinct MI300X / MI250X": [
    { "platform": "Microsoft Azure", "price_usd": 0, "plan": "询价", "country": "美国", "region": "北美", "note": "需询价 · AMD 数据中心 AI 加速器，MI300X 192GB HBM3", "pricing_url": "https://azure.microsoft.com/en-us/pricing/details/virtual-machines/linux/", "availability": "", "source": "reference" },
    { "platform": "Oracle Cloud Infrastructure", "price_usd": 0, "plan": "询价", "country": "美国", "region": "北美", "note": "需询价 · OCI BM.GPU.MI300X.8 实例", "pricing_url": "https://www.oracle.com/cloud/compute/pricing/", "availability": "", "source": "reference" }
  ],
  "AMD R9700": [
    { "platform": "Hostkey", "price_usd": 0.5, "plan": "月租€339.0/月 ≈ €0.464/时", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://hostkey.com/gpu-dedicated-servers/", "availability": "", "source": "scraped" }
  ],
  "AMD Radeon Instinct MI300X": [
    { "platform": "Microsoft Azure", "price_usd": 1.1088, "plan": "Azure VM (8× GPU)", "country": "", "region": "", "note": "实时抓取 · 2026-06-24 09:00 (北京时间)", "pricing_url": "", "availability": "", "source": "scraped" },
    { "platform": "Oracle Cloud", "price_usd": 6.0, "plan": "市场价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.oracle.com/cloud/compute/pricing/", "availability": "", "source": "scraped" }
  ],
  "AMD Radeon RX 6800 / 6700 XT": [
    { "platform": "Vast.ai (6700 XT)", "price_usd": 0.06, "plan": "市场浮动价（起）", "country": "美国", "region": "北美", "note": "参考数据 · 12GB 显存", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "reference" },
    { "platform": "Vast.ai (6800)", "price_usd": 0.07, "plan": "市场浮动价（起）", "country": "美国", "region": "北美", "note": "参考数据 · 16GB 显存，RDNA2 中端", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "reference" }
  ],
  "AMD Radeon RX 6900 XT / 6800 XT": [
    { "platform": "Vast.ai (6800 XT)", "price_usd": 0.08, "plan": "市场浮动价（起）", "country": "美国", "region": "北美", "note": "参考数据 · 16GB 显存", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "reference" },
    { "platform": "Vast.ai (6900 XT)", "price_usd": 0.1, "plan": "市场浮动价（起）", "country": "美国", "region": "北美", "note": "参考数据 · 16GB 显存，RDNA2 旗舰", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "reference" }
  ],
  "AMD Radeon RX 7600 / 6600 XT": [
    { "platform": "Vast.ai (6600 XT)", "price_usd": 0.05, "plan": "市场浮动价（起）", "country": "美国", "region": "北美", "note": "参考数据 · 8GB 显存", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "reference" },
    { "platform": "Vast.ai (7600)", "price_usd": 0.06, "plan": "市场浮动价（起）", "country": "美国", "region": "北美", "note": "参考数据 · 8GB 显存，RDNA3 入门级", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "reference" }
  ],
  "AMD Radeon RX 7800 XT / 7700 XT": [
    { "platform": "Vast.ai (7700 XT)", "price_usd": 0.08, "plan": "市场浮动价（起）", "country": "美国", "region": "北美", "note": "参考数据 · 12GB 显存", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "reference" },
    { "platform": "Vast.ai (7800 XT)", "price_usd": 0.1, "plan": "市场浮动价（起）", "country": "美国", "region": "北美", "note": "参考数据 · 16GB 显存，中端 AMD", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "reference" }
  ],
  "AMD Radeon RX 7900 XTX / 7900 XT": [
    { "platform": "Vast.ai (7900 XT)", "price_usd": 0.12, "plan": "市场浮动价（起）", "country": "美国", "region": "北美", "note": "参考数据 · 20GB 显存，性价比 AMD 方案", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "reference" },
    { "platform": "Vast.ai (7900 XTX)", "price_usd": 0.15, "plan": "市场浮动价（起）", "country": "美国", "region": "北美", "note": "参考数据 · 24GB/20GB 显存，AMD 旗舰消费卡", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "reference" },
    { "platform": "RunPod (Community Cloud)", "price_usd": 0.44, "plan": "社区云", "country": "美国", "region": "北美", "note": "参考数据", "pricing_url": "https://www.runpod.io/pricing", "availability": "", "source": "reference" }
  ],
  "AWS Trainium": [
    { "platform": "AWS (Amazon EC2)", "price_usd": 21.5, "plan": "AWS EC2 (us-east-1)", "country": "", "region": "", "note": "实时抓取 · 2026-06-24 09:00 (北京时间)", "pricing_url": "", "availability": "", "source": "scraped" }
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
    { "platform": "TensorDock", "price_usd": 1.5, "plan": "GPU起价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.tensordock.com/cloud-gpus.html", "availability": "", "source": "scraped" },
    { "platform": "Vast.ai", "price_usd": 0.4, "plan": "市场浮动价（起）", "country": "美国", "region": "北美", "note": "参考数据 · 极低价格", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "reference" },
    { "platform": "Cudo Compute", "price_usd": 0.6, "plan": "市场浮动价", "country": "英国", "region": "欧洲", "note": "参考数据", "pricing_url": "https://www.cudocompute.com/products/virtual-machines", "availability": "", "source": "reference" },
    { "platform": "DataCrunch", "price_usd": 0.9, "plan": "按需", "country": "芬兰", "region": "欧洲", "note": "参考数据 · 欧洲 GPU 云", "pricing_url": "https://verda.com/pricing", "availability": "", "source": "reference" },
    { "platform": "CoreWeave", "price_usd": 1.0, "plan": "按需", "country": "美国", "region": "北美", "note": "参考数据", "pricing_url": "https://www.coreweave.com/pricing", "availability": "", "source": "reference" },
    { "platform": "Lambda Labs", "price_usd": 1.09, "plan": "按需", "country": "美国", "region": "北美", "note": "参考数据 · 经济型 A100", "pricing_url": "https://lambda.ai/pricing", "availability": "", "source": "reference" },
    { "platform": "Google Cloud (GCP)", "price_usd": 2.0, "plan": "按需", "country": "美国", "region": "北美", "note": "参考数据", "pricing_url": "https://cloud.google.com/compute/gpus-pricing", "availability": "", "source": "reference" }
  ],
  "NVIDIA A100 (80GB SXM)": [
    { "platform": "Microsoft Azure", "price_usd": 0.6799, "plan": "Azure VM (8× GPU)", "country": "", "region": "", "note": "实时抓取 · 2026-06-24 09:00 (北京时间)", "pricing_url": "", "availability": "", "source": "scraped" },
    { "platform": "AWS (Amazon EC2)", "price_usd": 1.0368, "plan": "AWS EC2 (us-east-1)", "country": "", "region": "", "note": "实时抓取 · 2026-06-24 09:00 (北京时间)", "pricing_url": "", "availability": "", "source": "scraped" },
    { "platform": "NexGen Cloud", "price_usd": 1.35, "plan": "按需", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.hyperstack.cloud/gpu-pricing", "availability": "", "source": "scraped" },
    { "platform": "Massed Compute", "price_usd": 1.35, "plan": "按需", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.massedcompute.com/pricing", "availability": "", "source": "scraped" },
    { "platform": "JarvisLabs", "price_usd": 1.49, "plan": "按需", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://jarvislabs.ai/pricing/", "availability": "", "source": "scraped" },
    { "platform": "TensorDock", "price_usd": 1.8, "plan": "GPU起价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.tensordock.com/cloud-gpus.html", "availability": "", "source": "scraped" },
    { "platform": "Hostkey", "price_usd": 1.92, "plan": "月租€1300.0/月 ≈ €1.781/时", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://hostkey.com/gpu-dedicated-servers/", "availability": "", "source": "scraped" },
    { "platform": "Cerebrium", "price_usd": 2.1, "plan": "市场价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.cerebrium.ai/pricing", "availability": "", "source": "scraped" },
    { "platform": "Lambda Labs", "price_usd": 2.79, "plan": "市场价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://lambda.ai/pricing", "availability": "", "source": "scraped" },
    { "platform": "Oracle Cloud", "price_usd": 3.05, "plan": "市场价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.oracle.com/cloud/compute/pricing/", "availability": "", "source": "scraped" },
    { "platform": "Replicate", "price_usd": 3.51, "plan": "市场价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://replicate.com/pricing", "availability": "", "source": "scraped" },
    { "platform": "Vast.ai", "price_usd": 0.5, "plan": "市场浮动价（起）", "country": "美国", "region": "北美", "note": "参考数据 · 全球最低 A100 价格之一", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "reference" },
    { "platform": "Cudo Compute", "price_usd": 0.85, "plan": "市场浮动价", "country": "英国", "region": "欧洲", "note": "参考数据 · 去中心化云", "pricing_url": "https://www.cudocompute.com/products/virtual-machines", "availability": "", "source": "reference" },
    { "platform": "Genesis Cloud", "price_usd": 0.9, "plan": "按需", "country": "冰岛/德国", "region": "欧洲", "note": "参考数据 · 100%可再生能源", "pricing_url": "https://genesiscloud.com/pricing", "availability": "", "source": "reference" },
    { "platform": "DataCrunch", "price_usd": 1.1, "plan": "按需", "country": "芬兰", "region": "欧洲", "note": "参考数据 · 欧洲低价 GPU 云", "pricing_url": "https://verda.com/pricing", "availability": "", "source": "reference" },
    { "platform": "FluidStack", "price_usd": 1.1, "plan": "按需", "country": "英国/美国", "region": "北美", "note": "参考数据 · 液冷 GPU 集群", "pricing_url": "https://www.fluidstack.io/pricing", "availability": "", "source": "reference" },
    { "platform": "CoreWeave", "price_usd": 1.2, "plan": "按需", "country": "美国", "region": "北美", "note": "参考数据 · Kubernetes 原生", "pricing_url": "https://www.coreweave.com/pricing", "availability": "", "source": "reference" },
    { "platform": "RunPod (Community Cloud)", "price_usd": 1.29, "plan": "社区云", "country": "美国", "region": "北美", "note": "参考数据 · 高性价比", "pricing_url": "https://www.runpod.io/pricing", "availability": "", "source": "reference" },
    { "platform": "OVHcloud", "price_usd": 1.5, "plan": "按需", "country": "法国", "region": "欧洲", "note": "参考数据 · 欧洲数据主权", "pricing_url": "https://www.ovhcloud.com/en/public-cloud/prices/", "availability": "", "source": "reference" },
    { "platform": "Hetzner", "price_usd": 1.6, "plan": "按需", "country": "德国", "region": "欧洲", "note": "参考数据 · 德国高性价比", "pricing_url": "https://www.hetzner.com/cloud/gpu/", "availability": "", "source": "reference" },
    { "platform": "LeaderGPU", "price_usd": 1.6, "plan": "按需", "country": "法国", "region": "欧洲", "note": "参考数据 · 欧洲/美国节点", "pricing_url": "https://www.leadergpu.com/pricing", "availability": "", "source": "reference" },
    { "platform": "RunPod (Secure Cloud)", "price_usd": 1.69, "plan": "按需", "country": "美国", "region": "北美", "note": "参考数据 · 企业安全云", "pricing_url": "https://www.runpod.io/pricing", "availability": "", "source": "reference" },
    { "platform": "G-Core Labs", "price_usd": 1.7, "plan": "按需", "country": "卢森堡", "region": "欧洲", "note": "参考数据 · 全球边缘 GPU 优化", "pricing_url": "https://gcore.com/cloud/gpu-cloud", "availability": "", "source": "reference" },
    { "platform": "Paperspace", "price_usd": 1.79, "plan": "按需", "country": "美国", "region": "北美", "note": "参考数据 · 含 Gradient 平台", "pricing_url": "https://www.paperspace.com/pricing", "availability": "", "source": "reference" },
    { "platform": "Vultr", "price_usd": 1.9, "plan": "按需", "country": "美国", "region": "北美", "note": "参考数据 · 全球多区域", "pricing_url": "https://www.vultr.com/products/cloud-gpu/", "availability": "", "source": "reference" },
    { "platform": "DigitalOcean", "price_usd": 2.0, "plan": "按需(GPU Droplets)", "country": "美国", "region": "北美", "note": "参考数据 · Paperspace 集成", "pricing_url": "https://www.digitalocean.com/pricing/gpu-droplets", "availability": "", "source": "reference" },
    { "platform": "AutoDL", "price_usd": 2.2, "plan": "按需", "country": "中国", "region": "亚太", "note": "参考数据 · 国内领先 GPU 租赁，预装 DL 环境", "pricing_url": "https://www.autodl.com/price", "availability": "", "source": "reference" },
    { "platform": "百度智能云 (Baidu AI Cloud)", "price_usd": 2.3, "plan": "按需", "country": "中国", "region": "亚太", "note": "参考数据 · 含昆仑芯片选项", "pricing_url": "https://cloud.baidu.com/product/gpu.html", "availability": "", "source": "reference" },
    { "platform": "华为云 (Huawei Cloud)", "price_usd": 2.4, "plan": "按需", "country": "中国", "region": "亚太", "note": "参考数据 · 集成 ModelArts", "pricing_url": "https://www.huaweicloud.com/intl/en-us/pricing.html#/ecs", "availability": "", "source": "reference" },
    { "platform": "Google Cloud (GCP)", "price_usd": 2.5, "plan": "按需", "country": "美国", "region": "北美", "note": "参考数据 · 承诺使用折扣可达40%+", "pricing_url": "https://cloud.google.com/compute/gpus-pricing", "availability": "", "source": "reference" },
    { "platform": "腾讯云 (Tencent Cloud)", "price_usd": 2.5, "plan": "按需", "country": "中国", "region": "亚太", "note": "参考数据 · GN 系列 GPU 实例", "pricing_url": "https://buy.cloud.tencent.com/price/cvm/overview", "availability": "", "source": "reference" },
    { "platform": "阿里云 (Alibaba Cloud)", "price_usd": 2.8, "plan": "按需", "country": "中国", "region": "亚太", "note": "参考数据 · 亚洲区域覆盖广", "pricing_url": "https://www.alibabacloud.com/product/ecs/pricing", "availability": "", "source": "reference" }
  ],
  "NVIDIA A10G": [
    { "platform": "Microsoft Azure", "price_usd": 0.127, "plan": "Azure VM (2× GPU)", "country": "", "region": "", "note": "实时抓取 · 2026-06-24 09:00 (北京时间)", "pricing_url": "", "availability": "", "source": "scraped" },
    { "platform": "AWS (Amazon EC2)", "price_usd": 0.184, "plan": "AWS EC2 (eu-west-1)", "country": "", "region": "", "note": "实时抓取 · 2026-06-24 09:00 (北京时间)", "pricing_url": "", "availability": "", "source": "scraped" }
  ],
  "NVIDIA A30": [
    { "platform": "Exoscale", "price_usd": 1.23, "plan": "最小配置 (API)", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.exoscale.com/gpu/", "availability": "", "source": "scraped" }
  ],
  "NVIDIA A40": [
    { "platform": "Vast.ai", "price_usd": 0.3, "plan": "市场浮动价（起）", "country": "美国", "region": "北美", "note": "参考数据 · 48GB 显存，推理卡", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "reference" },
    { "platform": "RunPod (Community Cloud)", "price_usd": 0.59, "plan": "社区云", "country": "美国", "region": "北美", "note": "参考数据 · 大显存推理方案", "pricing_url": "https://www.runpod.io/pricing", "availability": "", "source": "reference" },
    { "platform": "CoreWeave", "price_usd": 1.0, "plan": "按需", "country": "美国", "region": "北美", "note": "参考数据", "pricing_url": "https://www.coreweave.com/pricing", "availability": "", "source": "reference" }
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
  "NVIDIA GTX 1070 / 1070 Ti": [
    { "platform": "Vast.ai", "price_usd": 0.04, "plan": "市场浮动价（起）", "country": "美国", "region": "北美", "note": "参考数据 · 8GB 显存，最廉价 8GB 以上显存选项", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "reference" }
  ],
  "NVIDIA GTX 1080 / 1080 Ti": [
    { "platform": "Vast.ai (1080)", "price_usd": 0.05, "plan": "市场浮动价（起）", "country": "美国", "region": "北美", "note": "参考数据 · 8GB 显存", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "reference" },
    { "platform": "Vast.ai (1080 Ti)", "price_usd": 0.07, "plan": "市场浮动价（起）", "country": "美国", "region": "北美", "note": "参考数据 · 11GB 显存，Pascal 经典卡", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "reference" }
  ],
  "NVIDIA GTX 1660 / 1660 Ti / 1660 Super": [
    { "platform": "Vast.ai", "price_usd": 0.05, "plan": "市场浮动价（起）", "country": "美国", "region": "北美", "note": "参考数据 · Turing 架构无 RT 核心，6GB 显存，极低价格", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "reference" }
  ],
  "NVIDIA H100 (80GB SXM)": [
    { "platform": "Microsoft Azure", "price_usd": 1.2899, "plan": "Azure VM (1× GPU)", "country": "", "region": "", "note": "实时抓取 · 2026-06-24 09:00 (北京时间)", "pricing_url": "", "availability": "", "source": "scraped" },
    { "platform": "Vast.ai", "price_usd": 1.47, "plan": "市场最低价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://vast.ai/pricing", "availability": "共2张", "source": "scraped" },
    { "platform": "AWS (Amazon EC2)", "price_usd": 1.8432, "plan": "AWS EC2 (us-east-1)", "country": "", "region": "", "note": "实时抓取 · 2026-06-24 09:00 (北京时间)", "pricing_url": "", "availability": "", "source": "scraped" },
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
    { "platform": "CoreWeave", "price_usd": 6.16, "plan": "按需", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.coreweave.com/pricing", "availability": "", "source": "scraped" },
    { "platform": "IBM Cloud", "price_usd": 0, "plan": "询价", "country": "美国", "region": "北美", "note": "需询价 · 企业级 GPU 裸金属，需联系销售", "pricing_url": "https://www.ibm.com/cloud/gpu", "availability": "", "source": "reference" },
    { "platform": "Cirrascale", "price_usd": 0, "plan": "询价", "country": "美国", "region": "北美", "note": "需询价 · 大规模 GPU 集群，需联系销售", "pricing_url": "https://www.cirrascale.com/cloud-services/", "availability": "", "source": "reference" },
    { "platform": "FluidStack", "price_usd": 1.8, "plan": "按需", "country": "英国/美国", "region": "北美", "note": "参考数据 · 液冷服务器集群", "pricing_url": "https://www.fluidstack.io/pricing", "availability": "", "source": "reference" },
    { "platform": "Cudo Compute", "price_usd": 1.9, "plan": "市场浮动价", "country": "英国", "region": "欧洲", "note": "参考数据 · 去中心化云市场", "pricing_url": "https://www.cudocompute.com/products/virtual-machines", "availability": "", "source": "reference" },
    { "platform": "RunPod (Community Cloud)", "price_usd": 1.99, "plan": "社区云", "country": "美国", "region": "北美", "note": "参考数据 · 性价比方案", "pricing_url": "https://www.runpod.io/pricing", "availability": "", "source": "reference" },
    { "platform": "DataCrunch", "price_usd": 2.1, "plan": "按需", "country": "芬兰", "region": "欧洲", "note": "参考数据 · 欧洲高性价比 GPU 云", "pricing_url": "https://verda.com/pricing", "availability": "", "source": "reference" },
    { "platform": "Hetzner", "price_usd": 2.2, "plan": "按需", "country": "德国", "region": "欧洲", "note": "参考数据 · 德国高性价比方案", "pricing_url": "https://www.hetzner.com/cloud/gpu/", "availability": "", "source": "reference" },
    { "platform": "OVHcloud", "price_usd": 2.4, "plan": "按需", "country": "法国", "region": "欧洲", "note": "参考数据 · 欧洲数据主权合规", "pricing_url": "https://www.ovhcloud.com/en/public-cloud/prices/", "availability": "", "source": "reference" },
    { "platform": "Genesis Cloud", "price_usd": 2.5, "plan": "按需", "country": "冰岛/德国", "region": "欧洲", "note": "参考数据 · 100%可再生能源", "pricing_url": "https://genesiscloud.com/pricing", "availability": "", "source": "reference" },
    { "platform": "RunPod (Secure Cloud)", "price_usd": 2.69, "plan": "按需", "country": "美国", "region": "北美", "note": "参考数据 · 企业级安全云", "pricing_url": "https://www.runpod.io/pricing", "availability": "", "source": "reference" },
    { "platform": "Vultr", "price_usd": 2.99, "plan": "按需", "country": "美国", "region": "北美", "note": "参考数据 · 全球30+数据中心", "pricing_url": "https://www.vultr.com/products/cloud-gpu/", "availability": "", "source": "reference" },
    { "platform": "Oracle Cloud Infrastructure", "price_usd": 3.0, "plan": "按需", "country": "美国", "region": "北美", "note": "参考数据 · 低延迟 RDMA 网络", "pricing_url": "https://www.oracle.com/cloud/compute/pricing/", "availability": "", "source": "reference" },
    { "platform": "火山引擎 (Volcengine)", "price_usd": 3.2, "plan": "按需", "country": "中国", "region": "亚太", "note": "参考数据 · 字节跳动旗下，弹性伸缩", "pricing_url": "https://www.volcengine.com/product/gpu", "availability": "", "source": "reference" },
    { "platform": "AutoDL", "price_usd": 3.2, "plan": "按需", "country": "中国", "region": "亚太", "note": "参考数据 · 国内领先 GPU 租赁，预装 DL 环境", "pricing_url": "https://www.autodl.com/price", "availability": "", "source": "reference" },
    { "platform": "Google Cloud (GCP)", "price_usd": 3.5, "plan": "按需", "country": "美国", "region": "北美", "note": "参考数据 · 承诺使用折扣可达40%+，含 Vertex AI", "pricing_url": "https://cloud.google.com/compute/gpus-pricing", "availability": "", "source": "reference" },
    { "platform": "华为云 (Huawei Cloud)", "price_usd": 3.5, "plan": "按需", "country": "中国", "region": "亚太", "note": "参考数据 · 集成 ModelArts AI 平台", "pricing_url": "https://www.huaweicloud.com/intl/en-us/pricing.html#/ecs", "availability": "", "source": "reference" },
    { "platform": "腾讯云 (Tencent Cloud)", "price_usd": 3.6, "plan": "按需", "country": "中国", "region": "亚太", "note": "参考数据 · GN10Xp 系列实例", "pricing_url": "https://buy.cloud.tencent.com/price/cvm/overview", "availability": "", "source": "reference" },
    { "platform": "阿里云 (Alibaba Cloud)", "price_usd": 3.8, "plan": "按需", "country": "中国", "region": "亚太", "note": "参考数据 · 亚洲节点覆盖广，支持竞价", "pricing_url": "https://www.alibabacloud.com/product/ecs/pricing", "availability": "", "source": "reference" },
    { "platform": "NVIDIA DGX Cloud", "price_usd": 5.0, "plan": "全托管（起）", "country": "美国", "region": "北美", "note": "参考数据 · DGX 全栈 AI 超算服务", "pricing_url": "https://www.nvidia.com/en-us/data-center/dgx-cloud/", "availability": "", "source": "reference" }
  ],
  "NVIDIA H100 (NVL)": [
    { "platform": "Massed Compute", "price_usd": 5.84, "plan": "按需", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.massedcompute.com/pricing", "availability": "", "source": "scraped" }
  ],
  "NVIDIA H200": [
    { "platform": "AWS (Amazon EC2)", "price_usd": 1.8432, "plan": "AWS EC2 (us-east-1)", "country": "", "region": "", "note": "实时抓取 · 2026-06-24 09:00 (北京时间)", "pricing_url": "", "availability": "", "source": "scraped" },
    { "platform": "Microsoft Azure", "price_usd": 2.12, "plan": "Azure VM (8× GPU)", "country": "", "region": "", "note": "实时抓取 · 2026-06-24 09:00 (北京时间)", "pricing_url": "", "availability": "", "source": "scraped" },
    { "platform": "Oracle Cloud", "price_usd": 2.5, "plan": "市场价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.oracle.com/cloud/compute/pricing/", "availability": "", "source": "scraped" },
    { "platform": "Saturn Cloud", "price_usd": 2.95, "plan": "市场价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://saturncloud.io/pricing/", "availability": "", "source": "scraped" },
    { "platform": "Vast.ai", "price_usd": 3.16, "plan": "市场最低价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://vast.ai/pricing", "availability": "共46张", "source": "scraped" },
    { "platform": "DigitalOcean", "price_usd": 3.44, "plan": "按需", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.digitalocean.com/pricing/gpu-droplets", "availability": "", "source": "scraped" },
    { "platform": "NexGen Cloud", "price_usd": 3.5, "plan": "按需", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.hyperstack.cloud/gpu-pricing", "availability": "", "source": "scraped" },
    { "platform": "Massed Compute", "price_usd": 3.62, "plan": "按需", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.massedcompute.com/pricing", "availability": "", "source": "scraped" },
    { "platform": "Cerebrium", "price_usd": 4.2, "plan": "市场价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.cerebrium.ai/pricing", "availability": "", "source": "scraped" },
    { "platform": "CoreWeave", "price_usd": 6.31, "plan": "按需", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.coreweave.com/pricing", "availability": "", "source": "scraped" },
    { "platform": "Lambda Labs", "price_usd": 3.29, "plan": "按需", "country": "美国", "region": "北美", "note": "参考数据 · 最新一代 H200 GPU", "pricing_url": "https://lambda.ai/pricing", "availability": "", "source": "reference" },
    { "platform": "Google Cloud (GCP)", "price_usd": 4.5, "plan": "按需", "country": "美国", "region": "北美", "note": "参考数据 · A3 Mega 实例", "pricing_url": "https://cloud.google.com/compute/gpus-pricing", "availability": "", "source": "reference" },
    { "platform": "NVIDIA DGX Cloud", "price_usd": 6.0, "plan": "全托管（起）", "country": "美国", "region": "北美", "note": "参考数据 · DGX GB200 系统", "pricing_url": "https://www.nvidia.com/en-us/data-center/dgx-cloud/", "availability": "", "source": "reference" }
  ],
  "NVIDIA L4": [
    { "platform": "Microsoft Azure", "price_usd": 0.075, "plan": "Azure VM (1× GPU)", "country": "", "region": "", "note": "实时抓取 · 2026-06-24 09:00 (北京时间)", "pricing_url": "", "availability": "", "source": "scraped" },
    { "platform": "AWS (Amazon EC2)", "price_usd": 0.184, "plan": "AWS EC2 (us-east-1)", "country": "", "region": "", "note": "实时抓取 · 2026-06-24 09:00 (北京时间)", "pricing_url": "", "availability": "", "source": "scraped" },
    { "platform": "JarvisLabs", "price_usd": 0.44, "plan": "按需", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://jarvislabs.ai/pricing/", "availability": "", "source": "scraped" },
    { "platform": "UpCloud", "price_usd": 0.63, "plan": "按需", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://upcloud.com/pricing/", "availability": "", "source": "scraped" },
    { "platform": "Cerebrium", "price_usd": 0.8, "plan": "市场价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.cerebrium.ai/pricing", "availability": "", "source": "scraped" },
    { "platform": "Scaleway", "price_usd": 0.85, "plan": "€0.79/时 (最小配置)", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.scaleway.com/en/pricing/", "availability": "", "source": "scraped" },
    { "platform": "DigitalOcean", "price_usd": 1.0, "plan": "按需", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.digitalocean.com/pricing/gpu-droplets", "availability": "", "source": "scraped" },
    { "platform": "Massed Compute", "price_usd": 1.0, "plan": "按需", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.massedcompute.com/pricing", "availability": "", "source": "scraped" },
    { "platform": "Vast.ai", "price_usd": 0.2, "plan": "市场浮动价（起）", "country": "美国", "region": "北美", "note": "参考数据", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "reference" },
    { "platform": "RunPod (Community Cloud)", "price_usd": 0.49, "plan": "社区云", "country": "美国", "region": "北美", "note": "参考数据", "pricing_url": "https://www.runpod.io/pricing", "availability": "", "source": "reference" },
    { "platform": "CoreWeave", "price_usd": 0.5, "plan": "按需", "country": "美国", "region": "北美", "note": "参考数据", "pricing_url": "https://www.coreweave.com/pricing", "availability": "", "source": "reference" },
    { "platform": "Google Cloud (GCP)", "price_usd": 0.55, "plan": "按需", "country": "美国", "region": "北美", "note": "参考数据 · 推理优化 GPU", "pricing_url": "https://cloud.google.com/compute/gpus-pricing", "availability": "", "source": "reference" }
  ],
  "NVIDIA L40S": [
    { "platform": "AWS (Amazon EC2)", "price_usd": 0.368, "plan": "AWS EC2 (us-east-1)", "country": "", "region": "", "note": "实时抓取 · 2026-06-24 09:00 (北京时间)", "pricing_url": "", "availability": "", "source": "scraped" },
    { "platform": "Massed Compute", "price_usd": 0.88, "plan": "按需", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.massedcompute.com/pricing", "availability": "", "source": "scraped" },
    { "platform": "Oracle Cloud", "price_usd": 0.88, "plan": "市场价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.oracle.com/cloud/compute/pricing/", "availability": "", "source": "scraped" },
    { "platform": "TensorDock", "price_usd": 0.95, "plan": "GPU起价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.tensordock.com/cloud-gpus.html", "availability": "", "source": "scraped" },
    { "platform": "UpCloud", "price_usd": 1.2, "plan": "按需", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://upcloud.com/pricing/", "availability": "", "source": "scraped" },
    { "platform": "DigitalOcean", "price_usd": 1.57, "plan": "按需", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.digitalocean.com/pricing/gpu-droplets", "availability": "", "source": "scraped" },
    { "platform": "Scaleway", "price_usd": 1.59, "plan": "€1.47/时 (最小配置)", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.scaleway.com/en/pricing/", "availability": "", "source": "scraped" },
    { "platform": "Cerebrium", "price_usd": 1.95, "plan": "市场价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.cerebrium.ai/pricing", "availability": "", "source": "scraped" },
    { "platform": "CoreWeave", "price_usd": 2.25, "plan": "按需", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.coreweave.com/pricing", "availability": "", "source": "scraped" },
    { "platform": "Vast.ai", "price_usd": 0.6, "plan": "市场浮动价（起）", "country": "美国", "region": "北美", "note": "参考数据", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "reference" },
    { "platform": "RunPod (Community Cloud)", "price_usd": 0.99, "plan": "社区云", "country": "美国", "region": "北美", "note": "参考数据 · 推理优化方案", "pricing_url": "https://www.runpod.io/pricing", "availability": "", "source": "reference" },
    { "platform": "NexGen Cloud", "price_usd": 1.3, "plan": "按需", "country": "英国", "region": "欧洲", "note": "参考数据 · 水力发电驱动", "pricing_url": "https://www.nexgencloud.com/pricing", "availability": "", "source": "reference" },
    { "platform": "火山引擎 (Volcengine)", "price_usd": 1.3, "plan": "按需", "country": "中国", "region": "亚太", "note": "参考数据", "pricing_url": "https://www.volcengine.com/product/gpu", "availability": "", "source": "reference" },
    { "platform": "Lambda Labs", "price_usd": 1.49, "plan": "按需", "country": "美国", "region": "北美", "note": "参考数据 · 推理优化 GPU", "pricing_url": "https://lambda.ai/pricing", "availability": "", "source": "reference" },
    { "platform": "Vultr", "price_usd": 1.5, "plan": "按需", "country": "美国", "region": "北美", "note": "参考数据", "pricing_url": "https://www.vultr.com/products/cloud-gpu/", "availability": "", "source": "reference" },
    { "platform": "OVHcloud", "price_usd": 1.6, "plan": "按需", "country": "法国", "region": "欧洲", "note": "参考数据", "pricing_url": "https://www.ovhcloud.com/en/public-cloud/prices/", "availability": "", "source": "reference" }
  ],
  "NVIDIA RTX 2080 / 2070": [
    { "platform": "Vast.ai", "price_usd": 0.06, "plan": "市场浮动价（起）", "country": "美国", "region": "北美", "note": "参考数据 · Turing 架构中端卡", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "reference" }
  ],
  "NVIDIA RTX 2080 Ti": [
    { "platform": "Salad", "price_usd": 0.06, "plan": "市场价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://salad.com/pricing", "availability": "", "source": "scraped" },
    { "platform": "Vast.ai", "price_usd": 0.08, "plan": "市场浮动价（起）", "country": "美国", "region": "北美", "note": "参考数据 · 11GB 显存，Turing 旗舰", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "reference" },
    { "platform": "TensorDock", "price_usd": 0.18, "plan": "市场浮动价（起）", "country": "美国", "region": "北美", "note": "参考数据", "pricing_url": "https://www.tensordock.com/cloud-gpus.html", "availability": "", "source": "reference" }
  ],
  "NVIDIA RTX 3060 / 3060 Ti": [
    { "platform": "Salad", "price_usd": 0.04, "plan": "市场价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://salad.com/pricing", "availability": "", "source": "scraped" },
    { "platform": "Vast.ai", "price_usd": 0.06, "plan": "市场浮动价（起）", "country": "美国", "region": "北美", "note": "参考数据 · 12GB/8GB 显存，最低门槛", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "reference" }
  ],
  "NVIDIA RTX 3070 / 3070 Ti": [
    { "platform": "Salad", "price_usd": 0.06, "plan": "市场价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://salad.com/pricing", "availability": "", "source": "scraped" },
    { "platform": "Vast.ai", "price_usd": 0.07, "plan": "市场浮动价（起）", "country": "美国", "region": "北美", "note": "参考数据 · 8GB 显存，轻量级任务", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "reference" }
  ],
  "NVIDIA RTX 3080 / 3080 Ti": [
    { "platform": "Salad", "price_usd": 0.08, "plan": "市场价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://salad.com/pricing", "availability": "", "source": "scraped" },
    { "platform": "Hostkey", "price_usd": 0.28, "plan": "月租€190.0/月 ≈ €0.260/时", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://hostkey.com/gpu-dedicated-servers/", "availability": "", "source": "scraped" },
    { "platform": "Exoscale", "price_usd": 0.92, "plan": "最小配置 (API)", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.exoscale.com/gpu/", "availability": "", "source": "scraped" },
    { "platform": "Vast.ai", "price_usd": 0.1, "plan": "市场浮动价（起）", "country": "美国", "region": "北美", "note": "参考数据 · 10GB/12GB 显存，Ampere 性价比款", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "reference" },
    { "platform": "TensorDock", "price_usd": 0.2, "plan": "市场浮动价（起）", "country": "美国", "region": "北美", "note": "参考数据", "pricing_url": "https://www.tensordock.com/cloud-gpus.html", "availability": "", "source": "reference" },
    { "platform": "RunPod (Community Cloud)", "price_usd": 0.29, "plan": "社区云", "country": "美国", "region": "北美", "note": "参考数据", "pricing_url": "https://www.runpod.io/pricing", "availability": "", "source": "reference" }
  ],
  "NVIDIA RTX 3090 / 3090 Ti": [
    { "platform": "Salad", "price_usd": 0.1, "plan": "市场价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://salad.com/pricing", "availability": "", "source": "scraped" },
    { "platform": "TensorDock", "price_usd": 0.2, "plan": "GPU起价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.tensordock.com/cloud-gpus.html", "availability": "", "source": "scraped" },
    { "platform": "Hostkey", "price_usd": 0.47, "plan": "月租€319.0/月 ≈ €0.437/时", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://hostkey.com/gpu-dedicated-servers/", "availability": "", "source": "scraped" },
    { "platform": "Vast.ai", "price_usd": 0.15, "plan": "市场浮动价（起）", "country": "美国", "region": "北美", "note": "参考数据 · 全球最低 GPU 价格之一", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "reference" },
    { "platform": "Cudo Compute", "price_usd": 0.2, "plan": "市场浮动价", "country": "英国", "region": "欧洲", "note": "参考数据", "pricing_url": "https://www.cudocompute.com/products/virtual-machines", "availability": "", "source": "reference" },
    { "platform": "AutoDL", "price_usd": 0.3, "plan": "按需", "country": "中国", "region": "亚太", "note": "参考数据 · 国内领先 GPU 租赁", "pricing_url": "https://www.autodl.com/price", "availability": "", "source": "reference" },
    { "platform": "Matpool (矩池云)", "price_usd": 0.35, "plan": "按需", "country": "中国", "region": "亚太", "note": "参考数据", "pricing_url": "https://matpool.com/pricing", "availability": "", "source": "reference" },
    { "platform": "RunPod (Community Cloud)", "price_usd": 0.39, "plan": "社区云", "country": "美国", "region": "北美", "note": "参考数据 · 24GB 显存，极致性价比", "pricing_url": "https://www.runpod.io/pricing", "availability": "", "source": "reference" }
  ],
  "NVIDIA RTX 4060 Ti": [
    { "platform": "Salad", "price_usd": 0.08, "plan": "市场价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://salad.com/pricing", "availability": "", "source": "scraped" },
    { "platform": "Vast.ai", "price_usd": 0.08, "plan": "市场浮动价（起）", "country": "美国", "region": "北美", "note": "参考数据 · 8GB/16GB 显存，入门推理", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "reference" }
  ],
  "NVIDIA RTX 4070 / 4070 Super": [
    { "platform": "Vast.ai", "price_usd": 0.1, "plan": "市场浮动价（起）", "country": "美国", "region": "北美", "note": "参考数据 · 12GB 显存，最经济 Ada 架构卡", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "reference" },
    { "platform": "Salad", "price_usd": 0.1, "plan": "分布式云", "country": "美国", "region": "北美", "note": "参考数据", "pricing_url": "https://salad.com/pricing", "availability": "", "source": "reference" },
    { "platform": "RunPod (Community Cloud)", "price_usd": 0.34, "plan": "社区云", "country": "美国", "region": "北美", "note": "参考数据", "pricing_url": "https://www.runpod.io/pricing", "availability": "", "source": "reference" }
  ],
  "NVIDIA RTX 4070 Ti / 4070": [
    { "platform": "Salad", "price_usd": 0.08, "plan": "市场价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://salad.com/pricing", "availability": "", "source": "scraped" }
  ],
  "NVIDIA RTX 4070 Ti / 4070 Ti Super": [
    { "platform": "Salad", "price_usd": 0.12, "plan": "分布式云", "country": "美国", "region": "北美", "note": "参考数据", "pricing_url": "https://salad.com/pricing", "availability": "", "source": "reference" },
    { "platform": "Vast.ai", "price_usd": 0.13, "plan": "市场浮动价（起）", "country": "美国", "region": "北美", "note": "参考数据 · 12GB/16GB 显存，轻量推理", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "reference" },
    { "platform": "TensorDock", "price_usd": 0.22, "plan": "市场浮动价（起）", "country": "美国", "region": "北美", "note": "参考数据", "pricing_url": "https://www.tensordock.com/cloud-gpus.html", "availability": "", "source": "reference" },
    { "platform": "RunPod (Community Cloud)", "price_usd": 0.39, "plan": "社区云", "country": "美国", "region": "北美", "note": "参考数据", "pricing_url": "https://www.runpod.io/pricing", "availability": "", "source": "reference" }
  ],
  "NVIDIA RTX 4080 / 4080 Super": [
    { "platform": "Salad", "price_usd": 0.11, "plan": "市场价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://salad.com/pricing", "availability": "", "source": "scraped" },
    { "platform": "Vast.ai", "price_usd": 0.18, "plan": "市场浮动价（起）", "country": "美国", "region": "北美", "note": "参考数据 · 16GB 显存，推理/微调好选择", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "reference" },
    { "platform": "Cudo Compute", "price_usd": 0.25, "plan": "市场浮动价", "country": "英国", "region": "欧洲", "note": "参考数据", "pricing_url": "https://www.cudocompute.com/products/virtual-machines", "availability": "", "source": "reference" },
    { "platform": "TensorDock", "price_usd": 0.3, "plan": "市场浮动价（起）", "country": "美国", "region": "北美", "note": "参考数据", "pricing_url": "https://www.tensordock.com/cloud-gpus.html", "availability": "", "source": "reference" },
    { "platform": "RunPod (Community Cloud)", "price_usd": 0.49, "plan": "社区云", "country": "美国", "region": "北美", "note": "参考数据", "pricing_url": "https://www.runpod.io/pricing", "availability": "", "source": "reference" }
  ],
  "NVIDIA RTX 4090": [
    { "platform": "Salad", "price_usd": 0.16, "plan": "市场价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://salad.com/pricing", "availability": "", "source": "scraped" },
    { "platform": "Vast.ai", "price_usd": 0.17, "plan": "市场最低价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://vast.ai/pricing", "availability": "共6张", "source": "scraped" },
    { "platform": "RunPod", "price_usd": 0.34, "plan": "按需", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.runpod.io/pricing", "availability": "", "source": "scraped" },
    { "platform": "TensorDock", "price_usd": 0.35, "plan": "GPU起价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.tensordock.com/cloud-gpus.html", "availability": "", "source": "scraped" },
    { "platform": "Hostkey", "price_usd": 1.11, "plan": "月租€750.0/月 ≈ €1.027/时", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://hostkey.com/gpu-dedicated-servers/", "availability": "", "source": "scraped" },
    { "platform": "Cudo Compute", "price_usd": 0.35, "plan": "市场浮动价", "country": "英国", "region": "欧洲", "note": "参考数据", "pricing_url": "https://www.cudocompute.com/products/virtual-machines", "availability": "", "source": "reference" },
    { "platform": "AutoDL", "price_usd": 0.48, "plan": "按需", "country": "中国", "region": "亚太", "note": "参考数据 · 国内领先 GPU 租赁，预装 DL 环境", "pricing_url": "https://www.autodl.com/price", "availability": "", "source": "reference" },
    { "platform": "Matpool (矩池云)", "price_usd": 0.5, "plan": "按需", "country": "中国", "region": "亚太", "note": "参考数据 · 国内高校和竞赛首选", "pricing_url": "https://matpool.com/pricing", "availability": "", "source": "reference" },
    { "platform": "Massed Compute", "price_usd": 0.55, "plan": "按需", "country": "美国", "region": "北美", "note": "参考数据", "pricing_url": "https://www.massedcompute.com/pricing", "availability": "", "source": "reference" },
    { "platform": "DataCrunch", "price_usd": 0.6, "plan": "按需", "country": "芬兰", "region": "欧洲", "note": "参考数据", "pricing_url": "https://verda.com/pricing", "availability": "", "source": "reference" },
    { "platform": "FluidStack", "price_usd": 0.65, "plan": "按需", "country": "英国/美国", "region": "北美", "note": "参考数据", "pricing_url": "https://www.fluidstack.io/pricing", "availability": "", "source": "reference" },
    { "platform": "RunPod (Community Cloud)", "price_usd": 0.69, "plan": "社区云", "country": "美国", "region": "北美", "note": "参考数据 · 消费级 GPU 性价比之王，24GB 显存", "pricing_url": "https://www.runpod.io/pricing", "availability": "", "source": "reference" },
    { "platform": "Vultr", "price_usd": 0.79, "plan": "按需", "country": "美国", "region": "北美", "note": "参考数据", "pricing_url": "https://www.vultr.com/products/cloud-gpu/", "availability": "", "source": "reference" },
    { "platform": "RunPod (Secure Cloud)", "price_usd": 0.99, "plan": "按需", "country": "美国", "region": "北美", "note": "参考数据", "pricing_url": "https://www.runpod.io/pricing", "availability": "", "source": "reference" }
  ],
  "NVIDIA RTX 6000 Ada / A6000": [
    { "platform": "Microsoft Azure", "price_usd": 0.1836, "plan": "Azure VM (1× GPU)", "country": "", "region": "", "note": "实时抓取 · 2026-06-24 09:00 (北京时间)", "pricing_url": "", "availability": "", "source": "scraped" },
    { "platform": "Massed Compute", "price_usd": 0.57, "plan": "按需", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.massedcompute.com/pricing", "availability": "", "source": "scraped" },
    { "platform": "TensorDock", "price_usd": 0.75, "plan": "GPU起价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.tensordock.com/cloud-gpus.html", "availability": "", "source": "scraped" },
    { "platform": "Vast.ai", "price_usd": 0.8, "plan": "市场最低价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://vast.ai/pricing", "availability": "共22张", "source": "scraped" },
    { "platform": "Exoscale", "price_usd": 2.15, "plan": "最小配置 (API)", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.exoscale.com/gpu/", "availability": "", "source": "scraped" },
    { "platform": "Vast.ai (RTX 6000 Ada)", "price_usd": 0.38, "plan": "市场浮动价（起）", "country": "美国", "region": "北美", "note": "参考数据 · Ada 架构，48GB 显存", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "reference" },
    { "platform": "RunPod (Community Cloud)", "price_usd": 0.69, "plan": "社区云", "country": "美国", "region": "北美", "note": "参考数据", "pricing_url": "https://www.runpod.io/pricing", "availability": "", "source": "reference" },
    { "platform": "DataCrunch", "price_usd": 0.7, "plan": "按需", "country": "芬兰", "region": "欧洲", "note": "参考数据", "pricing_url": "https://verda.com/pricing", "availability": "", "source": "reference" },
    { "platform": "Lambda Labs", "price_usd": 0.79, "plan": "按需", "country": "美国", "region": "北美", "note": "参考数据 · 入门级数据中心 GPU", "pricing_url": "https://lambda.ai/pricing", "availability": "", "source": "reference" },
    { "platform": "JarvisLabs", "price_usd": 0.8, "plan": "按需", "country": "印度", "region": "亚太", "note": "参考数据 · 预装 DL 框架", "pricing_url": "https://jarvislabs.ai/pricing/", "availability": "", "source": "reference" },
    { "platform": "Paperspace", "price_usd": 0.89, "plan": "按需", "country": "美国", "region": "北美", "note": "参考数据 · Gradient 集成", "pricing_url": "https://www.paperspace.com/pricing", "availability": "", "source": "reference" },
    { "platform": "RunPod (Secure Cloud)", "price_usd": 0.99, "plan": "按需", "country": "美国", "region": "北美", "note": "参考数据", "pricing_url": "https://www.runpod.io/pricing", "availability": "", "source": "reference" }
  ],
  "NVIDIA RTX A5000": [
    { "platform": "Exoscale", "price_usd": 1.34, "plan": "最小配置 (API)", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.exoscale.com/gpu/", "availability": "", "source": "scraped" }
  ],
  "NVIDIA T4": [
    { "platform": "Microsoft Azure", "price_usd": 0.0684, "plan": "Azure VM (1× GPU)", "country": "", "region": "", "note": "实时抓取 · 2026-06-24 09:00 (北京时间)", "pricing_url": "", "availability": "", "source": "scraped" },
    { "platform": "AWS (Amazon EC2)", "price_usd": 0.184, "plan": "AWS EC2 (eu-west-1)", "country": "", "region": "", "note": "实时抓取 · 2026-06-24 09:00 (北京时间)", "pricing_url": "", "availability": "", "source": "scraped" },
    { "platform": "Cerebrium", "price_usd": 0.59, "plan": "市场价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.cerebrium.ai/pricing", "availability": "", "source": "scraped" },
    { "platform": "Replicate", "price_usd": 0.81, "plan": "市场价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://replicate.com/pricing", "availability": "", "source": "scraped" },
    { "platform": "Saturn Cloud", "price_usd": 1.0, "plan": "市场价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://saturncloud.io/pricing/", "availability": "", "source": "scraped" },
    { "platform": "Exoscale", "price_usd": 1.05, "plan": "最小配置 (API)", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.exoscale.com/gpu/", "availability": "", "source": "scraped" },
    { "platform": "Google Colab", "price_usd": 0, "plan": "询价", "country": "美国", "region": "北美", "note": "需询价 · 免费版提供 T4; Pro $9.99/月起", "pricing_url": "https://colab.research.google.com/signup", "availability": "", "source": "reference" },
    { "platform": "Vast.ai", "price_usd": 0.15, "plan": "市场浮动价（起）", "country": "美国", "region": "北美", "note": "参考数据", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "reference" },
    { "platform": "Google Cloud (GCP)", "price_usd": 0.35, "plan": "按需", "country": "美国", "region": "北美", "note": "参考数据 · 最便宜云端推理 GPU", "pricing_url": "https://cloud.google.com/compute/gpus-pricing", "availability": "", "source": "reference" },
    { "platform": "腾讯云 (Tencent Cloud)", "price_usd": 0.38, "plan": "按需", "country": "中国", "region": "亚太", "note": "参考数据", "pricing_url": "https://buy.cloud.tencent.com/price/cvm/overview", "availability": "", "source": "reference" },
    { "platform": "阿里云 (Alibaba Cloud)", "price_usd": 0.4, "plan": "按需", "country": "中国", "region": "亚太", "note": "参考数据", "pricing_url": "https://www.alibabacloud.com/product/ecs/pricing", "availability": "", "source": "reference" },
    { "platform": "OVHcloud", "price_usd": 0.45, "plan": "按需", "country": "法国", "region": "欧洲", "note": "参考数据", "pricing_url": "https://www.ovhcloud.com/en/public-cloud/prices/", "availability": "", "source": "reference" },
    { "platform": "Vultr", "price_usd": 0.5, "plan": "按需", "country": "美国", "region": "北美", "note": "参考数据", "pricing_url": "https://www.vultr.com/products/cloud-gpu/", "availability": "", "source": "reference" }
  ],
  "NVIDIA Tesla K80 / M40 / M60": [
    { "platform": "Vast.ai (K80)", "price_usd": 0.05, "plan": "市场浮动价（起）", "country": "美国", "region": "北美", "note": "参考数据 · Kepler 架构，12GB × 2，最廉价的 GPU", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "reference" },
    { "platform": "Vast.ai (M40)", "price_usd": 0.06, "plan": "市场浮动价（起）", "country": "美国", "region": "北美", "note": "参考数据 · Maxwell 架构，24GB 显存", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "reference" }
  ],
  "NVIDIA Tesla P100 / P40": [
    { "platform": "AWS (Amazon EC2)", "price_usd": 0.184, "plan": "AWS EC2 (eu-west-1)", "country": "", "region": "", "note": "实时抓取 · 2026-06-24 09:00 (北京时间)", "pricing_url": "", "availability": "", "source": "scraped" },
    { "platform": "Oracle Cloud", "price_usd": 1.0, "plan": "市场价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.oracle.com/cloud/compute/pricing/", "availability": "", "source": "scraped" },
    { "platform": "Exoscale", "price_usd": 1.17, "plan": "最小配置 (API)", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.exoscale.com/gpu/", "availability": "", "source": "scraped" },
    { "platform": "Vast.ai (P40)", "price_usd": 0.09, "plan": "市场浮动价（起）", "country": "美国", "region": "北美", "note": "参考数据 · 24GB 显存，Pascal 推理卡", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "reference" },
    { "platform": "Vast.ai (P100)", "price_usd": 0.1, "plan": "市场浮动价（起）", "country": "美国", "region": "北美", "note": "参考数据 · Pascal 架构，16GB 显存", "pricing_url": "https://vast.ai/pricing", "availability": "", "source": "reference" },
    { "platform": "Google Cloud (GCP)", "price_usd": 0.95, "plan": "按需(P100)", "country": "美国", "region": "北美", "note": "参考数据", "pricing_url": "https://cloud.google.com/compute/gpus-pricing", "availability": "", "source": "reference" }
  ],
  "NVIDIA V100": [
    { "platform": "Vast.ai", "price_usd": 0.11, "plan": "市场最低价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://vast.ai/pricing", "availability": "共30张", "source": "scraped" },
    { "platform": "TensorDock", "price_usd": 0.17, "plan": "GPU起价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.tensordock.com/cloud-gpus.html", "availability": "", "source": "scraped" },
    { "platform": "AWS (Amazon EC2)", "price_usd": 0.368, "plan": "AWS EC2 (eu-west-1)", "country": "", "region": "", "note": "实时抓取 · 2026-06-24 09:00 (北京时间)", "pricing_url": "", "availability": "", "source": "scraped" },
    { "platform": "Lambda Labs", "price_usd": 0.79, "plan": "市场价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://lambda.ai/pricing", "availability": "", "source": "scraped" },
    { "platform": "Saturn Cloud", "price_usd": 1.095, "plan": "市场价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://saturncloud.io/pricing/", "availability": "", "source": "scraped" },
    { "platform": "Exoscale", "price_usd": 1.38, "plan": "最小配置 (API)", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.exoscale.com/gpu/", "availability": "", "source": "scraped" },
    { "platform": "Paperspace", "price_usd": 1.84, "plan": "按需", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.paperspace.com/pricing", "availability": "", "source": "scraped" },
    { "platform": "Oracle Cloud", "price_usd": 2.95, "plan": "市场价", "country": "", "region": "", "note": "实时抓取 · 2026-06-23 21:00 (北京时间)", "pricing_url": "https://www.oracle.com/cloud/compute/pricing/", "availability": "", "source": "scraped" },
    { "platform": "Genesis Cloud", "price_usd": 0.6, "plan": "按需", "country": "冰岛/德国", "region": "欧洲", "note": "参考数据 · 可再生能源", "pricing_url": "https://genesiscloud.com/pricing", "availability": "", "source": "reference" },
    { "platform": "JarvisLabs", "price_usd": 0.7, "plan": "按需", "country": "印度", "region": "亚太", "note": "参考数据", "pricing_url": "https://jarvislabs.ai/pricing/", "availability": "", "source": "reference" },
    { "platform": "OVHcloud", "price_usd": 0.9, "plan": "按需", "country": "法国", "region": "欧洲", "note": "参考数据", "pricing_url": "https://www.ovhcloud.com/en/public-cloud/prices/", "availability": "", "source": "reference" },
    { "platform": "Google Cloud (GCP)", "price_usd": 1.8, "plan": "按需", "country": "美国", "region": "北美", "note": "参考数据 · 上一代旗舰 GPU", "pricing_url": "https://cloud.google.com/compute/gpus-pricing", "availability": "", "source": "reference" }
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
  ],
  "中国云平台 GPU（部分需询价）": [
    { "platform": "中国移动云 (China Mobile Cloud)", "price_usd": 0, "plan": "询价", "country": "中国", "region": "亚太", "note": "需询价 · 运营商云，GPU VM/容器，边缘 AI 推理", "pricing_url": "https://ecloud.10086.cn/home/product-introduction/gpu", "availability": "", "source": "reference" },
    { "platform": "天翼云 (China Telecom e-Surfing Cloud)", "price_usd": 0, "plan": "询价", "country": "中国", "region": "亚太", "note": "需询价 · 中国电信云，全国基础设施 GPU 实例", "pricing_url": "https://www.ctyun.cn/product/gpu", "availability": "", "source": "reference" },
    { "platform": "联通云 (China Unicom Cloud)", "price_usd": 0, "plan": "询价", "country": "中国", "region": "亚太", "note": "需询价 · 中国联通云，结合5G边缘低延迟推理", "pricing_url": "https://www.cucloud.cn/product/gpu.html", "availability": "", "source": "reference" },
    { "platform": "浪潮云 (Inspur Cloud)", "price_usd": 0, "plan": "询价", "country": "中国", "region": "亚太", "note": "需询价 · 浪潮 HPC 传统优势，科学计算/AI 建模", "pricing_url": "https://cloud.inspur.com/product/gpu/", "availability": "", "source": "reference" },
    { "platform": "京东云 (JD Cloud)", "price_usd": 0, "plan": "询价", "country": "中国", "region": "亚太", "note": "需询价 · GPU VM/物理服务器，电商 AI/图像识别", "pricing_url": "https://www.jdcloud.com/cn/public/compute/gpu", "availability": "", "source": "reference" },
    { "platform": "金山云 (Kingsoft Cloud)", "price_usd": 0, "plan": "询价", "country": "中国", "region": "亚太", "note": "需询价 · KEC GPU 系列，游戏/媒体领域", "pricing_url": "https://www.ksyun.com/post/product/KEC.html", "availability": "", "source": "reference" },
    { "platform": "UCloud", "price_usd": 0, "plan": "询价", "country": "中国", "region": "亚太", "note": "需询价 · GPU 云主机和裸金属，中国/东南亚", "pricing_url": "https://www.ucloud.cn/site/product/uhost.html", "availability": "", "source": "reference" },
    { "platform": "青云 (QingCloud)", "price_usd": 0, "plan": "询价", "country": "中国", "region": "亚太", "note": "需询价 · GPU 计算实例，灵活 SDN 网络", "pricing_url": "https://www.qingcloud.com/products/gpu_server/", "availability": "", "source": "reference" },
    { "platform": "并行科技 (Paratera)", "price_usd": 0, "plan": "询价", "country": "中国", "region": "亚太", "note": "需询价 · HPC 云，可扩展 GPU 节点，高校/工业", "pricing_url": "https://www.paratera.com/", "availability": "", "source": "reference" },
    { "platform": "极视角 (Video++ AI Cloud)", "price_usd": 0, "plan": "询价", "country": "中国", "region": "亚太", "note": "需询价 · AI 视频识别 GPU 云", "pricing_url": "https://www.videopuzzles.com/", "availability": "", "source": "reference" }
  ],
  "中国超算中心（申请制）": [
    { "platform": "鹏城云脑 (Pengcheng Cloud Brain)", "price_usd": 0, "plan": "询价", "country": "中国", "region": "亚太", "note": "需询价 · 深圳国家级 AI 计算平台，华为昇腾 NPU 集群", "pricing_url": "https://cloudbrain.pcl.ac.cn/", "availability": "", "source": "reference" },
    { "platform": "之江实验室 (Zhejiang Lab)", "price_usd": 0, "plan": "询价", "country": "中国", "region": "亚太", "note": "需询价 · 浙江省研究型 GPU 集群，AI/机器人", "pricing_url": "https://www.zhejianglab.com/", "availability": "", "source": "reference" },
    { "platform": "国家超算深圳中心 (NSCC-SZ)", "price_usd": 0, "plan": "询价", "country": "中国", "region": "亚太", "note": "需询价 · 公共超算中心，面向政府/学术界", "pricing_url": "http://www.nsccsz.gov.cn/", "availability": "", "source": "reference" },
    { "platform": "国家超算广州中心 (NSCC-GZ)", "price_usd": 0, "plan": "询价", "country": "中国", "region": "亚太", "note": "需询价 · 天河二号/天河星逸，气象/基因组/CAE", "pricing_url": "https://www.nscc-gz.cn/", "availability": "", "source": "reference" },
    { "platform": "国家超算天津中心 (NSCC-TJ)", "price_usd": 0, "plan": "询价", "country": "中国", "region": "亚太", "note": "需询价 · 天河系列超算，科学研究和创新项目", "pricing_url": "https://nscc-tj.cn/", "availability": "", "source": "reference" },
    { "platform": "国家超算无锡中心 (NSCC-WX)", "price_usd": 0, "plan": "询价", "country": "中国", "region": "亚太", "note": "需询价 · 神威太湖之光，AI/地球科学仿真", "pricing_url": "http://www.nsccwx.cn/", "availability": "", "source": "reference" },
    { "platform": "上海超算中心 (SSCS)", "price_usd": 0, "plan": "询价", "country": "中国", "region": "亚太", "note": "需询价 · 上海市级 HPC，药物/汽车/金融", "pricing_url": "https://www.sscs.cn/", "availability": "", "source": "reference" },
    { "platform": "北京超级云计算中心 (BLSC)", "price_usd": 0, "plan": "询价", "country": "中国", "region": "亚太", "note": "需询价 · 云化超算，弹性 GPU 深度学习", "pricing_url": "https://www.blsc.cn/", "availability": "", "source": "reference" },
    { "platform": "合肥先进计算中心 (Hefei ACC)", "price_usd": 0, "plan": "询价", "country": "中国", "region": "亚太", "note": "需询价 · 中科大 GPU 集群，量子化学/材料", "pricing_url": "http://www.hpcc.ustc.edu.cn/", "availability": "", "source": "reference" }
  ],
  "其他地区平台": [
    { "platform": "Yandex Cloud", "price_usd": 0, "plan": "询价", "country": "俄罗斯", "region": "亚太", "note": "需询价 · 俄罗斯最大云平台，GPU VM/K8s", "pricing_url": "https://cloud.yandex.com/en/services/compute#pricing", "availability": "", "source": "reference" },
    { "platform": "JarvisLabs", "price_usd": 1.1, "plan": "按需", "country": "印度", "region": "亚太", "note": "参考数据 · 印度 GPU 云，预装 DL 框架，即开即用", "pricing_url": "https://jarvislabs.ai/pricing/", "availability": "", "source": "reference" }
  ],
  "华为昇腾 Ascend 910B / 910C": [
    { "platform": "鹏城云脑 (Pengcheng Cloud Brain)", "price_usd": 0, "plan": "询价", "country": "中国", "region": "亚太", "note": "需询价 · 国家级 AI 计算平台，需申请使用", "pricing_url": "https://cloudbrain.pcl.ac.cn/", "availability": "", "source": "reference" },
    { "platform": "华为云 (Huawei Cloud)", "price_usd": 2.0, "plan": "按需", "country": "中国", "region": "亚太", "note": "参考数据 · 昇腾 NPU 自研芯片，集成 ModelArts", "pricing_url": "https://www.huaweicloud.com/intl/en-us/pricing.html#/ecs", "availability": "", "source": "reference" }
  ],
  "去中心化/区块链 GPU 平台": [
    { "platform": "Render Network", "price_usd": 0, "plan": "询价", "country": "美国", "region": "北美", "note": "需询价 · 区块链 GPU 渲染网络，按 OctaneBench 定价，RNDR 代币", "pricing_url": "https://rendertoken.com/", "availability": "", "source": "reference" },
    { "platform": "Golem Network", "price_usd": 0, "plan": "询价", "country": "瑞士", "region": "欧洲", "note": "需询价 · P2P 去中心化算力网络，GLM 代币结算，渲染和计算", "pricing_url": "https://www.golem.network/", "availability": "", "source": "reference" },
    { "platform": "NiceHash", "price_usd": 0, "plan": "询价", "country": "斯洛文尼亚", "region": "欧洲", "note": "需询价 · 算力市场，按哈希率竞价，BTC 结算，主要面向挖矿", "pricing_url": "https://www.nicehash.com/pricing", "availability": "", "source": "reference" },
    { "platform": "Mining Rig Rentals", "price_usd": 0, "plan": "询价", "country": "美国", "region": "北美", "note": "需询价 · 矿机租赁平台，按算力和时长计费", "pricing_url": "https://www.miningrigrentals.com/", "availability": "", "source": "reference" },
    { "platform": "Q Blocks", "price_usd": 0, "plan": "询价", "country": "美国", "region": "北美", "note": "需询价 · 聚合数据中心和矿工 GPU，Web3 AI 生态", "pricing_url": "https://qblocks.cloud/", "availability": "", "source": "reference" },
    { "platform": "Akash Network", "price_usd": 0.15, "plan": "反向拍卖（起）", "country": "美国", "region": "北美", "note": "参考数据 · DePIN 去中心化云，GPU 容器通过竞拍定价，AKT 代币结算", "pricing_url": "https://akash.network/pricing/", "availability": "", "source": "reference" },
    { "platform": "Salad", "price_usd": 0.2, "plan": "分布式云（起）", "country": "美国", "region": "北美", "note": "参考数据 · 利用全球闲置消费级 GPU，适合推理批处理", "pricing_url": "https://salad.com/pricing", "availability": "", "source": "reference" }
  ],
  "无服务器/API 平台（按量计费）": [
    { "platform": "Modal", "price_usd": 0, "plan": "询价", "country": "美国", "region": "北美", "note": "需询价 · Python 无服务器云，GPU 按使用秒数+内存计费", "pricing_url": "https://modal.com/pricing", "availability": "", "source": "reference" },
    { "platform": "Replicate", "price_usd": 0, "plan": "询价", "country": "美国", "region": "北美", "note": "需询价 · AI 模型 API，按 GPU 运行时间和请求次数计费", "pricing_url": "https://replicate.com/pricing", "availability": "", "source": "reference" },
    { "platform": "Fireworks.ai", "price_usd": 0, "plan": "询价", "country": "美国", "region": "北美", "note": "需询价 · GenAI 推理平台，按输入/输出 token 计费", "pricing_url": "https://fireworks.ai/pricing", "availability": "", "source": "reference" },
    { "platform": "Together AI", "price_usd": 0, "plan": "询价", "country": "美国", "region": "北美", "note": "需询价 · 开源模型推理+训练，推理按 token，训练按 GPU 小时", "pricing_url": "https://www.together.ai/pricing", "availability": "", "source": "reference" },
    { "platform": "BentoML (BentoCloud)", "price_usd": 0, "plan": "询价", "country": "美国", "region": "北美", "note": "需询价 · 无服务器推理平台，自动伸缩，按 GPU 使用量计费", "pricing_url": "https://www.bentoml.com/pricing", "availability": "", "source": "reference" },
    { "platform": "Cerebrium", "price_usd": 0, "plan": "询价", "country": "南非", "region": "其他", "note": "需询价 · 无服务器 GPU 推理，按 GPU 秒+数据传输计费", "pricing_url": "https://www.cerebrium.ai/pricing", "availability": "", "source": "reference" },
    { "platform": "Monster API", "price_usd": 0, "plan": "询价", "country": "美国", "region": "北美", "note": "需询价 · API 优先 GPU 云，推理按 token、训练按 GPU 小时", "pricing_url": "https://monsterapi.ai/pricing", "availability": "", "source": "reference" },
    { "platform": "Mystic AI", "price_usd": 0, "plan": "询价", "country": "英国", "region": "欧洲", "note": "需询价 · 无服务器 GPU 推理，pip 部署模型", "pricing_url": "https://mystic.ai/pricing", "availability": "", "source": "reference" },
    { "platform": "Hugging Face (Inference Endpoints)", "price_usd": 0, "plan": "询价", "country": "美国/法国", "region": "北美", "note": "需询价 · 托管推理，按 GPU 秒计费，支持 A100/T4/L4", "pricing_url": "https://huggingface.co/pricing#endpoints", "availability": "", "source": "reference" },
    { "platform": "OctoML (OctoAI)", "price_usd": 0, "plan": "询价", "country": "美国", "region": "北美", "note": "需询价 · 自动化模型优化+部署，按推理量计费", "pricing_url": "https://octoml.ai/pricing/", "availability": "", "source": "reference" },
    { "platform": "Deepnote", "price_usd": 0, "plan": "询价", "country": "美国", "region": "北美", "note": "需询价 · 协作数据笔记本，含 GPU 加速额度", "pricing_url": "https://deepnote.com/pricing", "availability": "", "source": "reference" },
    { "platform": "Saturn Cloud", "price_usd": 0, "plan": "询价", "country": "美国", "region": "北美", "note": "需询价 · 数据科学云，GPU/Dask 集群按席位+用量计费", "pricing_url": "https://saturncloud.io/pricing/", "availability": "", "source": "reference" },
    { "platform": "Coiled", "price_usd": 0, "plan": "询价", "country": "美国", "region": "北美", "note": "需询价 · 托管 Dask，GPU 按云资源消耗计费", "pricing_url": "https://www.coiled.io/pricing", "availability": "", "source": "reference" },
    { "platform": "Anyscale", "price_usd": 0, "plan": "询价", "country": "美国", "region": "北美", "note": "需询价 · Ray 平台，GPU 按底层云资源+平台费计费", "pricing_url": "https://www.anyscale.com/pricing", "availability": "", "source": "reference" },
    { "platform": "Databricks", "price_usd": 0, "plan": "询价", "country": "美国", "region": "北美", "note": "需询价 · GPU 集群按 Databricks Unit (DBU) + 云资源费计费", "pricing_url": "https://www.databricks.com/product/pricing", "availability": "", "source": "reference" },
    { "platform": "CodeOcean", "price_usd": 0, "plan": "询价", "country": "美国", "region": "北美", "note": "需询价 · 可复现研究平台，GPU 计算胶囊", "pricing_url": "https://codeocean.com/pricing", "availability": "", "source": "reference" },
    { "platform": "Google Colab", "price_usd": 0, "plan": "询价", "country": "美国", "region": "北美", "note": "需询价 · 免费 T4 GPU; Pro $9.99/月，Pro+ $49.99/月", "pricing_url": "https://colab.research.google.com/signup", "availability": "", "source": "reference" }
  ],
  "日韩云平台 GPU": [
    { "platform": "Sakura Internet", "price_usd": 0, "plan": "询价", "country": "日本", "region": "亚太", "note": "需询价 · 日本云 GPU 实例，日本国内广泛使用", "pricing_url": "https://www.sakura.ad.jp/services/cloud/gpu/", "availability": "", "source": "reference" },
    { "platform": "IIJ GIO", "price_usd": 0, "plan": "询价", "country": "日本", "region": "亚太", "note": "需询价 · 日本 IIJ 骨干网 GPU 云主机", "pricing_url": "https://www.iij.ad.jp/biz/gio/", "availability": "", "source": "reference" },
    { "platform": "KT Cloud", "price_usd": 0, "plan": "询价", "country": "韩国", "region": "亚太", "note": "需询价 · 韩国电信 GPU 云，AI/媒体/游戏", "pricing_url": "https://cloud.kt.com/", "availability": "", "source": "reference" },
    { "platform": "Naver Cloud", "price_usd": 0, "plan": "询价", "country": "韩国", "region": "亚太", "note": "需询价 · 韩国 Naver GPU 服务器，DL/VDI", "pricing_url": "https://www.ncloud.com/product/compute/gpu", "availability": "", "source": "reference" }
  ],
  "百度昆仑芯": [
    { "platform": "百度智能云 (Baidu AI Cloud)", "price_usd": 1.8, "plan": "按需", "country": "中国", "region": "亚太", "note": "参考数据 · 昆仑芯2代 AI 加速芯片", "pricing_url": "https://cloud.baidu.com/product/gpu.html", "availability": "", "source": "reference" }
  ],
  "裸金属/托管 GPU（需询价）": [
    { "platform": "PhoenixNAP", "price_usd": 0, "plan": "询价", "country": "美国", "region": "北美", "note": "需询价 · 专用 GPU 托管，裸金属/VM，DL/VDI/区块链", "pricing_url": "https://phoenixnap.com/gpu-hosting", "availability": "", "source": "reference" },
    { "platform": "Equinix Metal", "price_usd": 0, "plan": "询价", "country": "美国", "region": "北美", "note": "需询价 · 全球 Equinix 数据中心裸金属 GPU", "pricing_url": "https://metal.equinix.com/product/servers/", "availability": "", "source": "reference" },
    { "platform": "Hivelocity", "price_usd": 0, "plan": "询价", "country": "美国", "region": "北美", "note": "需询价 · 40+ 数据中心，即时部署 GPU 裸金属", "pricing_url": "https://www.hivelocity.net/products/gpu-servers/", "availability": "", "source": "reference" },
    { "platform": "QuadraNet", "price_usd": 0, "plan": "询价", "country": "美国", "region": "北美", "note": "需询价 · 洛杉矶 GPU 托管，含 DDoS 防护", "pricing_url": "https://quadranet.com/gpu-dedicated-servers", "availability": "", "source": "reference" },
    { "platform": "Psychz", "price_usd": 0, "plan": "询价", "country": "美国", "region": "北美", "note": "需询价 · 高性价比 GPU 服务器，美国/亚洲节点", "pricing_url": "https://www.psychz.net/", "availability": "", "source": "reference" },
    { "platform": "TurnKey Internet", "price_usd": 0, "plan": "询价", "country": "美国", "region": "北美", "note": "需询价 · 纽约绿色数据中心 GPU，定制硬件", "pricing_url": "https://turnkeyinternet.net/gpu-dedicated-server/", "availability": "", "source": "reference" },
    { "platform": "Dedicated.com", "price_usd": 0, "plan": "询价", "country": "美国", "region": "北美", "note": "需询价 · 入门级 GPU 托管，低成本方案", "pricing_url": "https://dedicated.com/dedicated-servers/gpu", "availability": "", "source": "reference" },
    { "platform": "Rackspace Technology", "price_usd": 0, "plan": "询价", "country": "美国", "region": "北美", "note": "需询价 · 托管 GPU 方案，支持 AI/ML/VDI", "pricing_url": "https://www.rackspace.com/cloud/gpu", "availability": "", "source": "reference" },
    { "platform": "ServerMania", "price_usd": 0, "plan": "询价", "country": "加拿大", "region": "北美", "note": "需询价 · 可定制 GPU 专用服务器，10Gbps 网络", "pricing_url": "https://www.servermania.com/gpu-servers.htm", "availability": "", "source": "reference" },
    { "platform": "DataPacket", "price_usd": 0, "plan": "询价", "country": "美国/英国", "region": "北美", "note": "需询价 · 裸金属 GPU，全球20+节点，不限流量", "pricing_url": "https://www.datapacket.com/gpu-hosting", "availability": "", "source": "reference" },
    { "platform": "Servers.com", "price_usd": 0, "plan": "询价", "country": "荷兰", "region": "欧洲", "note": "需询价 · 全球裸金属 GPU 实例，灵活计费", "pricing_url": "https://www.servers.com/gpu-servers/", "availability": "", "source": "reference" },
    { "platform": "21Cloud", "price_usd": 0, "plan": "询价", "country": "荷兰", "region": "欧洲", "note": "需询价 · 荷兰 GPU 云和托管，合规 HPC", "pricing_url": "https://www.21cloud.com/cloud/gpu-cloud", "availability": "", "source": "reference" },
    { "platform": "Hostkey", "price_usd": 0, "plan": "询价", "country": "荷兰", "region": "欧洲", "note": "需询价 · 即开 GPU 服务器，欧洲/美国节点", "pricing_url": "https://www.hostkey.com/gpu-servers", "availability": "", "source": "reference" },
    { "platform": "Cherry Servers", "price_usd": 0, "plan": "询价", "country": "立陶宛", "region": "欧洲", "note": "需询价 · 裸金属 GPU 可定制，全球 BGP", "pricing_url": "https://www.cherryservers.com/pricing/gpu-servers", "availability": "", "source": "reference" },
    { "platform": "Leaseweb", "price_usd": 0, "plan": "询价", "country": "荷兰", "region": "欧洲", "note": "需询价 · 托管/非托管 GPU 服务器，欧/美/亚节点", "pricing_url": "https://www.leaseweb.com/en/dedicated-servers/gpu", "availability": "", "source": "reference" },
    { "platform": "G-Core Labs", "price_usd": 0, "plan": "询价", "country": "卢森堡", "region": "欧洲", "note": "需询价 · 全球边缘 GPU 优化云", "pricing_url": "https://gcore.com/cloud/gpu-cloud", "availability": "", "source": "reference" },
    { "platform": "UpCloud", "price_usd": 0, "plan": "询价", "country": "芬兰", "region": "欧洲", "note": "需询价 · 高性能 GPU 计算，MaxIOPS 存储", "pricing_url": "https://upcloud.com/pricing/", "availability": "", "source": "reference" },
    { "platform": "Exoscale", "price_usd": 0, "plan": "询价", "country": "瑞士", "region": "欧洲", "note": "需询价 · 瑞士云 GPU，欧洲数据法规合规", "pricing_url": "https://www.exoscale.com/gpu/", "availability": "", "source": "reference" },
    { "platform": "T-Systems (Open Telekom Cloud)", "price_usd": 0, "plan": "询价", "country": "德国", "region": "欧洲", "note": "需询价 · 欧洲主权云，严格 GDPR，德国电信", "pricing_url": "https://open-telekom-cloud.com/en/pricing/", "availability": "", "source": "reference" },
    { "platform": "Aruba Cloud", "price_usd": 0, "plan": "询价", "country": "意大利", "region": "欧洲", "note": "需询价 · 意大利云，小型企业 GPU VPS", "pricing_url": "https://www.arubacloud.com/cloud-pricing.aspx", "availability": "", "source": "reference" },
    { "platform": "LeaderGPU", "price_usd": 0, "plan": "询价", "country": "法国", "region": "欧洲", "note": "需询价 · 专用 GPU 服务器，欧洲/美国，统一定价", "pricing_url": "https://www.leadergpu.com/pricing", "availability": "", "source": "reference" },
    { "platform": "SabrePC", "price_usd": 0, "plan": "询价", "country": "美国", "region": "北美", "note": "需询价 · 工作站级 GPU 云，可配置裸金属", "pricing_url": "https://www.sabrepc.com/hpc-cloud", "availability": "", "source": "reference" },
    { "platform": "Applied Digital", "price_usd": 0, "plan": "询价", "country": "美国", "region": "北美", "note": "需询价 · 高密度 GPU 托管，液冷，HPC/挖矿", "pricing_url": "https://www.applieddigital.com/", "availability": "", "source": "reference" },
    { "platform": "Rescale", "price_usd": 0, "plan": "询价", "country": "美国", "region": "北美", "note": "需询价 · 云 HPC 平台，多云端 GPU，航空航天/汽车仿真", "pricing_url": "https://www.rescale.com/pricing/", "availability": "", "source": "reference" },
    { "platform": "Cirrascale", "price_usd": 0, "plan": "询价", "country": "美国", "region": "北美", "note": "需询价 · 大规模 GPU 集群，自动驾驶训练", "pricing_url": "https://www.cirrascale.com/cloud-services/", "availability": "", "source": "reference" },
    { "platform": "Bizon", "price_usd": 0, "plan": "询价", "country": "美国", "region": "北美", "note": "需询价 · 液冷 GPU 云和工作站，深度学习优化", "pricing_url": "https://bizon.ai/pricing", "availability": "", "source": "reference" },
    { "platform": "Akamai Linode", "price_usd": 0, "plan": "询价", "country": "美国", "region": "北美", "note": "需询价 · GPU 实例（Quadro RTX），简单可预测定价", "pricing_url": "https://www.linode.com/pricing/#compute-gpu", "availability": "", "source": "reference" }
  ]
};
