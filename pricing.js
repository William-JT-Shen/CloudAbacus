// GPU 算力平台参考价格数据（暗黑主题版 · 全面版）
// 数据来源：各平台官网公开定价页面 + vast.ai 市场价格参考（截至 2025-06-12）
// null 表示未公开定价/需询价
// 价格单位：美元/小时 (USD/hr) 除非特别说明

var GPU_PRICING = {

  // ==================== NVIDIA H100 / H200 ====================
  "NVIDIA H100 (80GB SXM)": [
    { platform: "Lambda Labs", price_usd: 2.49, plan: "按需", country: "美国", region: "北美", note: "预装 DL 框架", pricing_url: "https://lambda.ai/pricing" },
    { platform: "RunPod (Secure Cloud)", price_usd: 2.69, plan: "按需", country: "美国", region: "北美", note: "企业级安全云", pricing_url: "https://www.runpod.io/pricing" },
    { platform: "RunPod (Community Cloud)", price_usd: 1.99, plan: "社区云", country: "美国", region: "北美", note: "性价比方案", pricing_url: "https://www.runpod.io/pricing" },
    { platform: "Vast.ai", price_usd: 1.50, plan: "市场浮动价（起）", country: "美国", region: "北美", note: "去中心化市场，价格实时波动", pricing_url: "https://vast.ai/pricing" },
    { platform: "TensorDock", price_usd: 1.40, plan: "市场浮动价（起）", country: "美国", region: "北美", note: "裸金属即时部署", pricing_url: "https://www.tensordock.com/cloud-gpus.html" },
    { platform: "CoreWeave", price_usd: 2.06, plan: "按需", country: "美国", region: "北美", note: "Kubernetes 原生 GPU 云", pricing_url: "https://www.coreweave.com/pricing" },
    { platform: "Paperspace", price_usd: 3.18, plan: "按需", country: "美国", region: "北美", note: "集成 Gradient 笔记本", pricing_url: "https://www.paperspace.com/pricing" },
    { platform: "DataCrunch", price_usd: 2.10, plan: "按需", country: "芬兰", region: "欧洲", note: "欧洲高性价比 GPU 云", pricing_url: "https://verda.com/pricing" },
    { platform: "FluidStack", price_usd: 1.80, plan: "按需", country: "英国/美国", region: "北美", note: "液冷服务器集群", pricing_url: "https://www.fluidstack.io/pricing" },
    { platform: "Massed Compute", price_usd: 1.70, plan: "按需", country: "美国", region: "北美", note: "大内存配置可选", pricing_url: "https://www.massedcompute.com/pricing" },
    { platform: "Genesis Cloud", price_usd: 2.50, plan: "按需", country: "冰岛/德国", region: "欧洲", note: "100%可再生能源", pricing_url: "https://genesiscloud.com/pricing" },
    { platform: "NexGen Cloud", price_usd: 2.30, plan: "按需", country: "英国", region: "欧洲", note: "水力发电驱动", pricing_url: "https://www.nexgencloud.com/pricing" },
    { platform: "OVHcloud", price_usd: 2.40, plan: "按需", country: "法国", region: "欧洲", note: "欧洲数据主权合规", pricing_url: "https://www.ovhcloud.com/en/public-cloud/prices/" },
    { platform: "Scaleway", price_usd: 2.60, plan: "按需", country: "法国", region: "欧洲", note: "法国环保数据中心", pricing_url: "https://www.scaleway.com/en/gpu-instances/" },
    { platform: "Google Cloud (GCP)", price_usd: 3.50, plan: "按需", country: "美国", region: "北美", note: "承诺使用折扣可达40%+，含 Vertex AI", pricing_url: "https://cloud.google.com/compute/gpus-pricing" },
    { platform: "AWS (Amazon EC2)", price_usd: 4.90, plan: "按需(p5.48xlarge)", country: "美国", region: "北美", note: "8×H100 含主机，竞价可降60%", pricing_url: "https://aws.amazon.com/ec2/pricing/on-demand/" },
    { platform: "Microsoft Azure", price_usd: 4.30, plan: "按需(ND H100 v5)", country: "美国", region: "北美", note: "含 Azure ML，预留实例折扣", pricing_url: "https://azure.microsoft.com/en-us/pricing/details/virtual-machines/linux/" },
    { platform: "NVIDIA DGX Cloud", price_usd: 5.00, plan: "全托管（起）", country: "美国", region: "北美", note: "DGX 全栈 AI 超算服务", pricing_url: "https://www.nvidia.com/en-us/data-center/dgx-cloud/" },
    { platform: "DigitalOcean", price_usd: 3.20, plan: "按需(GPU Droplets)", country: "美国", region: "北美", note: "集成 Paperspace Gradient", pricing_url: "https://www.digitalocean.com/pricing/gpu-droplets" },
    { platform: "Vultr", price_usd: 2.99, plan: "按需", country: "美国", region: "北美", note: "全球30+数据中心", pricing_url: "https://www.vultr.com/products/cloud-gpu/" },
    { platform: "阿里云 (Alibaba Cloud)", price_usd: 3.80, plan: "按需", country: "中国", region: "亚太", note: "亚洲节点覆盖广，支持竞价", pricing_url: "https://www.alibabacloud.com/product/ecs/pricing" },
    { platform: "腾讯云 (Tencent Cloud)", price_usd: 3.60, plan: "按需", country: "中国", region: "亚太", note: "GN10Xp 系列实例", pricing_url: "https://buy.cloud.tencent.com/price/cvm/overview" },
    { platform: "华为云 (Huawei Cloud)", price_usd: 3.50, plan: "按需", country: "中国", region: "亚太", note: "集成 ModelArts AI 平台", pricing_url: "https://www.huaweicloud.com/intl/en-us/pricing.html#/ecs" },
    { platform: "火山引擎 (Volcengine)", price_usd: 3.20, plan: "按需", country: "中国", region: "亚太", note: "字节跳动旗下，弹性伸缩", pricing_url: "https://www.volcengine.com/product/gpu" },
    { platform: "Hetzner", price_usd: 2.20, plan: "按需", country: "德国", region: "欧洲", note: "德国高性价比方案", pricing_url: "https://www.hetzner.com/cloud/gpu/" },
    { platform: "IBM Cloud", price_usd: null, plan: "询价", country: "美国", region: "北美", note: "企业级 GPU 裸金属，需联系销售", pricing_url: "https://www.ibm.com/cloud/gpu" },
    { platform: "Oracle Cloud Infrastructure", price_usd: 3.00, plan: "按需", country: "美国", region: "北美", note: "低延迟 RDMA 网络", pricing_url: "https://www.oracle.com/cloud/compute/pricing/" },
    { platform: "Cudo Compute", price_usd: 1.90, plan: "市场浮动价", country: "英国", region: "欧洲", note: "去中心化云市场", pricing_url: "https://www.cudocompute.com/products/virtual-machines" },
    { platform: "Cirrascale", price_usd: null, plan: "询价", country: "美国", region: "北美", note: "大规模 GPU 集群，需联系销售", pricing_url: "https://www.cirrascale.com/cloud-services/" },
    { platform: "AutoDL", price_usd: 3.20, plan: "按需", country: "中国", region: "亚太", note: "国内领先 GPU 租赁，预装 DL 环境", pricing_url: "https://www.autodl.com/price" }
  ],

  "NVIDIA H200": [
    { platform: "Lambda Labs", price_usd: 3.29, plan: "按需", country: "美国", region: "北美", note: "最新一代 H200 GPU", pricing_url: "https://lambda.ai/pricing" },
    { platform: "CoreWeave", price_usd: 2.80, plan: "按需", country: "美国", region: "北美", note: "大规模 H200 集群", pricing_url: "https://www.coreweave.com/pricing" },
    { platform: "AWS (Amazon EC2)", price_usd: 5.50, plan: "按需(p5e)", country: "美国", region: "北美", note: "即将大规模可用", pricing_url: "https://aws.amazon.com/ec2/pricing/on-demand/" },
    { platform: "NVIDIA DGX Cloud", price_usd: 6.00, plan: "全托管（起）", country: "美国", region: "北美", note: "DGX GB200 系统", pricing_url: "https://www.nvidia.com/en-us/data-center/dgx-cloud/" },
    { platform: "Google Cloud (GCP)", price_usd: 4.50, plan: "按需", country: "美国", region: "北美", note: "A3 Mega 实例", pricing_url: "https://cloud.google.com/compute/gpus-pricing" }
  ],

  // ==================== NVIDIA A100 ====================
  "NVIDIA A100 (80GB SXM)": [
    { platform: "Lambda Labs", price_usd: 1.29, plan: "按需", country: "美国", region: "北美", note: "性价比突出的 A100", pricing_url: "https://lambda.ai/pricing" },
    { platform: "RunPod (Secure Cloud)", price_usd: 1.69, plan: "按需", country: "美国", region: "北美", note: "企业安全云", pricing_url: "https://www.runpod.io/pricing" },
    { platform: "RunPod (Community Cloud)", price_usd: 1.29, plan: "社区云", country: "美国", region: "北美", note: "高性价比", pricing_url: "https://www.runpod.io/pricing" },
    { platform: "Vast.ai", price_usd: 0.50, plan: "市场浮动价（起）", country: "美国", region: "北美", note: "全球最低 A100 价格之一", pricing_url: "https://vast.ai/pricing" },
    { platform: "TensorDock", price_usd: 0.80, plan: "市场浮动价（起）", country: "美国", region: "北美", note: "裸金属即时部署", pricing_url: "https://www.tensordock.com/cloud-gpus.html" },
    { platform: "CoreWeave", price_usd: 1.20, plan: "按需", country: "美国", region: "北美", note: "Kubernetes 原生", pricing_url: "https://www.coreweave.com/pricing" },
    { platform: "Paperspace", price_usd: 1.79, plan: "按需", country: "美国", region: "北美", note: "含 Gradient 平台", pricing_url: "https://www.paperspace.com/pricing" },
    { platform: "DataCrunch", price_usd: 1.10, plan: "按需", country: "芬兰", region: "欧洲", note: "欧洲低价 GPU 云", pricing_url: "https://verda.com/pricing" },
    { platform: "Genesis Cloud", price_usd: 0.90, plan: "按需", country: "冰岛/德国", region: "欧洲", note: "100%可再生能源", pricing_url: "https://genesiscloud.com/pricing" },
    { platform: "FluidStack", price_usd: 1.10, plan: "按需", country: "英国/美国", region: "北美", note: "液冷 GPU 集群", pricing_url: "https://www.fluidstack.io/pricing" },
    { platform: "Massed Compute", price_usd: 1.20, plan: "按需", country: "美国", region: "北美", note: "大内存配置", pricing_url: "https://www.massedcompute.com/pricing" },
    { platform: "JarvisLabs", price_usd: 1.10, plan: "按需", country: "印度", region: "亚太", note: "预装 DL 框架，即开即用", pricing_url: "https://jarvislabs.ai/pricing/" },
    { platform: "OVHcloud", price_usd: 1.50, plan: "按需", country: "法国", region: "欧洲", note: "欧洲数据主权", pricing_url: "https://www.ovhcloud.com/en/public-cloud/prices/" },
    { platform: "Hetzner", price_usd: 1.60, plan: "按需", country: "德国", region: "欧洲", note: "德国高性价比", pricing_url: "https://www.hetzner.com/cloud/gpu/" },
    { platform: "Google Cloud (GCP)", price_usd: 2.50, plan: "按需", country: "美国", region: "北美", note: "承诺使用折扣可达40%+", pricing_url: "https://cloud.google.com/compute/gpus-pricing" },
    { platform: "AWS (Amazon EC2)", price_usd: 3.00, plan: "按需(p4d.24xlarge)", country: "美国", region: "北美", note: "8×A100，竞价可降60%", pricing_url: "https://aws.amazon.com/ec2/pricing/on-demand/" },
    { platform: "Microsoft Azure", price_usd: 2.60, plan: "按需(ND A100 v4)", country: "美国", region: "北美", note: "含 Azure ML", pricing_url: "https://azure.microsoft.com/en-us/pricing/details/virtual-machines/linux/" },
    { platform: "阿里云 (Alibaba Cloud)", price_usd: 2.80, plan: "按需", country: "中国", region: "亚太", note: "亚洲区域覆盖广", pricing_url: "https://www.alibabacloud.com/product/ecs/pricing" },
    { platform: "DigitalOcean", price_usd: 2.00, plan: "按需(GPU Droplets)", country: "美国", region: "北美", note: "Paperspace 集成", pricing_url: "https://www.digitalocean.com/pricing/gpu-droplets" },
    { platform: "Vultr", price_usd: 1.90, plan: "按需", country: "美国", region: "北美", note: "全球多区域", pricing_url: "https://www.vultr.com/products/cloud-gpu/" },
    { platform: "Cudo Compute", price_usd: 0.85, plan: "市场浮动价", country: "英国", region: "欧洲", note: "去中心化云", pricing_url: "https://www.cudocompute.com/products/virtual-machines" },
    { platform: "腾讯云 (Tencent Cloud)", price_usd: 2.50, plan: "按需", country: "中国", region: "亚太", note: "GN 系列 GPU 实例", pricing_url: "https://buy.cloud.tencent.com/price/cvm/overview" },
    { platform: "华为云 (Huawei Cloud)", price_usd: 2.40, plan: "按需", country: "中国", region: "亚太", note: "集成 ModelArts", pricing_url: "https://www.huaweicloud.com/intl/en-us/pricing.html#/ecs" },
    { platform: "百度智能云 (Baidu AI Cloud)", price_usd: 2.30, plan: "按需", country: "中国", region: "亚太", note: "含昆仑芯片选项", pricing_url: "https://cloud.baidu.com/product/gpu.html" },
    { platform: "G-Core Labs", price_usd: 1.70, plan: "按需", country: "卢森堡", region: "欧洲", note: "全球边缘 GPU 优化", pricing_url: "https://gcore.com/cloud/gpu-cloud" },
    { platform: "LeaderGPU", price_usd: 1.60, plan: "按需", country: "法国", region: "欧洲", note: "欧洲/美国节点", pricing_url: "https://www.leadergpu.com/pricing" },
    { platform: "AutoDL", price_usd: 2.20, plan: "按需", country: "中国", region: "亚太", note: "国内领先 GPU 租赁，预装 DL 环境", pricing_url: "https://www.autodl.com/price" }
  ],

  "NVIDIA A100 (40GB PCIe)": [
    { platform: "Lambda Labs", price_usd: 1.09, plan: "按需", country: "美国", region: "北美", note: "经济型 A100", pricing_url: "https://lambda.ai/pricing" },
    { platform: "Vast.ai", price_usd: 0.40, plan: "市场浮动价（起）", country: "美国", region: "北美", note: "极低价格", pricing_url: "https://vast.ai/pricing" },
    { platform: "TensorDock", price_usd: 0.65, plan: "市场浮动价（起）", country: "美国", region: "北美", note: "裸金属部署", pricing_url: "https://www.tensordock.com/cloud-gpus.html" },
    { platform: "DataCrunch", price_usd: 0.90, plan: "按需", country: "芬兰", region: "欧洲", note: "欧洲 GPU 云", pricing_url: "https://verda.com/pricing" },
    { platform: "CoreWeave", price_usd: 1.00, plan: "按需", country: "美国", region: "北美", note: "", pricing_url: "https://www.coreweave.com/pricing" },
    { platform: "Google Cloud (GCP)", price_usd: 2.00, plan: "按需", country: "美国", region: "北美", note: "", pricing_url: "https://cloud.google.com/compute/gpus-pricing" },
    { platform: "Cudo Compute", price_usd: 0.60, plan: "市场浮动价", country: "英国", region: "欧洲", note: "", pricing_url: "https://www.cudocompute.com/products/virtual-machines" }
  ],

  // ==================== NVIDIA L40S / L4 ====================
  "NVIDIA L40S": [
    { platform: "CoreWeave", price_usd: 1.27, plan: "按需", country: "美国", region: "北美", note: "推理性价比突出", pricing_url: "https://www.coreweave.com/pricing" },
    { platform: "Lambda Labs", price_usd: 1.49, plan: "按需", country: "美国", region: "北美", note: "推理优化 GPU", pricing_url: "https://lambda.ai/pricing" },
    { platform: "RunPod (Community Cloud)", price_usd: 0.99, plan: "社区云", country: "美国", region: "北美", note: "推理优化方案", pricing_url: "https://www.runpod.io/pricing" },
    { platform: "Vast.ai", price_usd: 0.60, plan: "市场浮动价（起）", country: "美国", region: "北美", note: "", pricing_url: "https://vast.ai/pricing" },
    { platform: "NexGen Cloud", price_usd: 1.30, plan: "按需", country: "英国", region: "欧洲", note: "水力发电驱动", pricing_url: "https://www.nexgencloud.com/pricing" },
    { platform: "Scaleway", price_usd: 1.40, plan: "按需", country: "法国", region: "欧洲", note: "法国环保云", pricing_url: "https://www.scaleway.com/en/gpu-instances/" },
    { platform: "Vultr", price_usd: 1.50, plan: "按需", country: "美国", region: "北美", note: "", pricing_url: "https://www.vultr.com/products/cloud-gpu/" },
    { platform: "OVHcloud", price_usd: 1.60, plan: "按需", country: "法国", region: "欧洲", note: "", pricing_url: "https://www.ovhcloud.com/en/public-cloud/prices/" },
    { platform: "火山引擎 (Volcengine)", price_usd: 1.30, plan: "按需", country: "中国", region: "亚太", note: "", pricing_url: "https://www.volcengine.com/product/gpu" }
  ],

  "NVIDIA L4": [
    { platform: "Google Cloud (GCP)", price_usd: 0.55, plan: "按需", country: "美国", region: "北美", note: "推理优化 GPU", pricing_url: "https://cloud.google.com/compute/gpus-pricing" },
    { platform: "RunPod (Community Cloud)", price_usd: 0.49, plan: "社区云", country: "美国", region: "北美", note: "", pricing_url: "https://www.runpod.io/pricing" },
    { platform: "Vast.ai", price_usd: 0.20, plan: "市场浮动价（起）", country: "美国", region: "北美", note: "", pricing_url: "https://vast.ai/pricing" },
    { platform: "Scaleway", price_usd: 0.60, plan: "按需", country: "法国", region: "欧洲", note: "", pricing_url: "https://www.scaleway.com/en/gpu-instances/" },
    { platform: "CoreWeave", price_usd: 0.50, plan: "按需", country: "美国", region: "北美", note: "", pricing_url: "https://www.coreweave.com/pricing" }
  ],

  // ==================== NVIDIA RTX 6000 Ada / A6000 / A40 ====================
  "NVIDIA RTX 6000 Ada / A6000": [
    { platform: "Lambda Labs", price_usd: 0.79, plan: "按需", country: "美国", region: "北美", note: "入门级数据中心 GPU", pricing_url: "https://lambda.ai/pricing" },
    { platform: "RunPod (Secure Cloud)", price_usd: 0.99, plan: "按需", country: "美国", region: "北美", note: "", pricing_url: "https://www.runpod.io/pricing" },
    { platform: "RunPod (Community Cloud)", price_usd: 0.69, plan: "社区云", country: "美国", region: "北美", note: "", pricing_url: "https://www.runpod.io/pricing" },
    { platform: "Vast.ai", price_usd: 0.35, plan: "市场浮动价（起）", country: "美国", region: "北美", note: "", pricing_url: "https://vast.ai/pricing" },
    { platform: "Vast.ai (RTX 6000 Ada)", price_usd: 0.38, plan: "市场浮动价（起）", country: "美国", region: "北美", note: "Ada 架构，48GB 显存", pricing_url: "https://vast.ai/pricing" },
    { platform: "TensorDock", price_usd: 0.55, plan: "市场浮动价（起）", country: "美国", region: "北美", note: "", pricing_url: "https://www.tensordock.com/cloud-gpus.html" },
    { platform: "JarvisLabs", price_usd: 0.80, plan: "按需", country: "印度", region: "亚太", note: "预装 DL 框架", pricing_url: "https://jarvislabs.ai/pricing/" },
    { platform: "Paperspace", price_usd: 0.89, plan: "按需", country: "美国", region: "北美", note: "Gradient 集成", pricing_url: "https://www.paperspace.com/pricing" },
    { platform: "DataCrunch", price_usd: 0.70, plan: "按需", country: "芬兰", region: "欧洲", note: "", pricing_url: "https://verda.com/pricing" }
  ],

  "NVIDIA A40": [
    { platform: "Vast.ai", price_usd: 0.30, plan: "市场浮动价（起）", country: "美国", region: "北美", note: "48GB 显存，推理卡", pricing_url: "https://vast.ai/pricing" },
    { platform: "RunPod (Community Cloud)", price_usd: 0.59, plan: "社区云", country: "美国", region: "北美", note: "大显存推理方案", pricing_url: "https://www.runpod.io/pricing" },
    { platform: "CoreWeave", price_usd: 1.00, plan: "按需", country: "美国", region: "北美", note: "", pricing_url: "https://www.coreweave.com/pricing" }
  ],

  // ==================== NVIDIA RTX 4090 / 4080 / 4070 (消费级) ====================
  "NVIDIA RTX 4090": [
    { platform: "RunPod (Community Cloud)", price_usd: 0.69, plan: "社区云", country: "美国", region: "北美", note: "消费级 GPU 性价比之王，24GB 显存", pricing_url: "https://www.runpod.io/pricing" },
    { platform: "RunPod (Secure Cloud)", price_usd: 0.99, plan: "按需", country: "美国", region: "北美", note: "", pricing_url: "https://www.runpod.io/pricing" },
    { platform: "Vast.ai", price_usd: 0.25, plan: "市场浮动价（起）", country: "美国", region: "北美", note: "最低价但供给波动大", pricing_url: "https://vast.ai/pricing" },
    { platform: "TensorDock", price_usd: 0.40, plan: "市场浮动价（起）", country: "美国", region: "北美", note: "", pricing_url: "https://www.tensordock.com/cloud-gpus.html" },
    { platform: "Massed Compute", price_usd: 0.55, plan: "按需", country: "美国", region: "北美", note: "", pricing_url: "https://www.massedcompute.com/pricing" },
    { platform: "FluidStack", price_usd: 0.65, plan: "按需", country: "英国/美国", region: "北美", note: "", pricing_url: "https://www.fluidstack.io/pricing" },
    { platform: "Matpool (矩池云)", price_usd: 0.50, plan: "按需", country: "中国", region: "亚太", note: "国内高校和竞赛首选", pricing_url: "https://matpool.com/pricing" },
    { platform: "AutoDL", price_usd: 0.48, plan: "按需", country: "中国", region: "亚太", note: "国内领先 GPU 租赁，预装 DL 环境", pricing_url: "https://www.autodl.com/price" },
    { platform: "Cudo Compute", price_usd: 0.35, plan: "市场浮动价", country: "英国", region: "欧洲", note: "", pricing_url: "https://www.cudocompute.com/products/virtual-machines" },
    { platform: "Salad", price_usd: 0.20, plan: "分布式云", country: "美国", region: "北美", note: "利用闲置消费级 GPU", pricing_url: "https://salad.com/pricing" },
    { platform: "Vultr", price_usd: 0.79, plan: "按需", country: "美国", region: "北美", note: "", pricing_url: "https://www.vultr.com/products/cloud-gpu/" },
    { platform: "DataCrunch", price_usd: 0.60, plan: "按需", country: "芬兰", region: "欧洲", note: "", pricing_url: "https://verda.com/pricing" }
  ],

  // 以下消费级 GPU 型号主要来源于 vast.ai 市场
  "NVIDIA RTX 4080 / 4080 Super": [
    { platform: "Vast.ai", price_usd: 0.18, plan: "市场浮动价（起）", country: "美国", region: "北美", note: "16GB 显存，推理/微调好选择", pricing_url: "https://vast.ai/pricing" },
    { platform: "RunPod (Community Cloud)", price_usd: 0.49, plan: "社区云", country: "美国", region: "北美", note: "", pricing_url: "https://www.runpod.io/pricing" },
    { platform: "TensorDock", price_usd: 0.30, plan: "市场浮动价（起）", country: "美国", region: "北美", note: "", pricing_url: "https://www.tensordock.com/cloud-gpus.html" },
    { platform: "Cudo Compute", price_usd: 0.25, plan: "市场浮动价", country: "英国", region: "欧洲", note: "", pricing_url: "https://www.cudocompute.com/products/virtual-machines" },
    { platform: "Salad", price_usd: 0.15, plan: "分布式云", country: "美国", region: "北美", note: "闲置 GPU 分布式网络", pricing_url: "https://salad.com/pricing" }
  ],

  "NVIDIA RTX 4070 Ti / 4070 Ti Super": [
    { platform: "Vast.ai", price_usd: 0.13, plan: "市场浮动价（起）", country: "美国", region: "北美", note: "12GB/16GB 显存，轻量推理", pricing_url: "https://vast.ai/pricing" },
    { platform: "RunPod (Community Cloud)", price_usd: 0.39, plan: "社区云", country: "美国", region: "北美", note: "", pricing_url: "https://www.runpod.io/pricing" },
    { platform: "TensorDock", price_usd: 0.22, plan: "市场浮动价（起）", country: "美国", region: "北美", note: "", pricing_url: "https://www.tensordock.com/cloud-gpus.html" },
    { platform: "Salad", price_usd: 0.12, plan: "分布式云", country: "美国", region: "北美", note: "", pricing_url: "https://salad.com/pricing" }
  ],

  "NVIDIA RTX 4070 / 4070 Super": [
    { platform: "Vast.ai", price_usd: 0.10, plan: "市场浮动价（起）", country: "美国", region: "北美", note: "12GB 显存，最经济 Ada 架构卡", pricing_url: "https://vast.ai/pricing" },
    { platform: "RunPod (Community Cloud)", price_usd: 0.34, plan: "社区云", country: "美国", region: "北美", note: "", pricing_url: "https://www.runpod.io/pricing" },
    { platform: "Salad", price_usd: 0.10, plan: "分布式云", country: "美国", region: "北美", note: "", pricing_url: "https://salad.com/pricing" }
  ],

  "NVIDIA RTX 4060 Ti": [
    { platform: "Vast.ai", price_usd: 0.08, plan: "市场浮动价（起）", country: "美国", region: "北美", note: "8GB/16GB 显存，入门推理", pricing_url: "https://vast.ai/pricing" },
    { platform: "Salad", price_usd: 0.08, plan: "分布式云", country: "美国", region: "北美", note: "", pricing_url: "https://salad.com/pricing" }
  ],

  // ==================== NVIDIA RTX 3090 / 3080 / 3070 ====================
  "NVIDIA RTX 3090 / 3090 Ti": [
    { platform: "RunPod (Community Cloud)", price_usd: 0.39, plan: "社区云", country: "美国", region: "北美", note: "24GB 显存，极致性价比", pricing_url: "https://www.runpod.io/pricing" },
    { platform: "Vast.ai", price_usd: 0.15, plan: "市场浮动价（起）", country: "美国", region: "北美", note: "全球最低 GPU 价格之一", pricing_url: "https://vast.ai/pricing" },
    { platform: "TensorDock", price_usd: 0.30, plan: "市场浮动价（起）", country: "美国", region: "北美", note: "", pricing_url: "https://www.tensordock.com/cloud-gpus.html" },
    { platform: "Matpool (矩池云)", price_usd: 0.35, plan: "按需", country: "中国", region: "亚太", note: "", pricing_url: "https://matpool.com/pricing" },
    { platform: "AutoDL", price_usd: 0.30, plan: "按需", country: "中国", region: "亚太", note: "国内领先 GPU 租赁", pricing_url: "https://www.autodl.com/price" },
    { platform: "Cudo Compute", price_usd: 0.20, plan: "市场浮动价", country: "英国", region: "欧洲", note: "", pricing_url: "https://www.cudocompute.com/products/virtual-machines" },
    { platform: "Salad", price_usd: 0.12, plan: "分布式云", country: "美国", region: "北美", note: "", pricing_url: "https://salad.com/pricing" }
  ],

  "NVIDIA RTX 3080 / 3080 Ti": [
    { platform: "Vast.ai", price_usd: 0.10, plan: "市场浮动价（起）", country: "美国", region: "北美", note: "10GB/12GB 显存，Ampere 性价比款", pricing_url: "https://vast.ai/pricing" },
    { platform: "RunPod (Community Cloud)", price_usd: 0.29, plan: "社区云", country: "美国", region: "北美", note: "", pricing_url: "https://www.runpod.io/pricing" },
    { platform: "TensorDock", price_usd: 0.20, plan: "市场浮动价（起）", country: "美国", region: "北美", note: "", pricing_url: "https://www.tensordock.com/cloud-gpus.html" },
    { platform: "Salad", price_usd: 0.09, plan: "分布式云", country: "美国", region: "北美", note: "", pricing_url: "https://salad.com/pricing" }
  ],

  "NVIDIA RTX 3070 / 3070 Ti": [
    { platform: "Vast.ai", price_usd: 0.07, plan: "市场浮动价（起）", country: "美国", region: "北美", note: "8GB 显存，轻量级任务", pricing_url: "https://vast.ai/pricing" },
    { platform: "Salad", price_usd: 0.07, plan: "分布式云", country: "美国", region: "北美", note: "", pricing_url: "https://salad.com/pricing" }
  ],

  "NVIDIA RTX 3060 / 3060 Ti": [
    { platform: "Vast.ai", price_usd: 0.06, plan: "市场浮动价（起）", country: "美国", region: "北美", note: "12GB/8GB 显存，最低门槛", pricing_url: "https://vast.ai/pricing" },
    { platform: "Salad", price_usd: 0.05, plan: "分布式云", country: "美国", region: "北美", note: "", pricing_url: "https://salad.com/pricing" }
  ],

  // ==================== NVIDIA RTX 20 系列 ====================
  "NVIDIA RTX 2080 Ti": [
    { platform: "Vast.ai", price_usd: 0.08, plan: "市场浮动价（起）", country: "美国", region: "北美", note: "11GB 显存，Turing 旗舰", pricing_url: "https://vast.ai/pricing" },
    { platform: "TensorDock", price_usd: 0.18, plan: "市场浮动价（起）", country: "美国", region: "北美", note: "", pricing_url: "https://www.tensordock.com/cloud-gpus.html" }
  ],

  "NVIDIA RTX 2080 / 2070": [
    { platform: "Vast.ai", price_usd: 0.06, plan: "市场浮动价（起）", country: "美国", region: "北美", note: "Turing 架构中端卡", pricing_url: "https://vast.ai/pricing" }
  ],

  // ==================== NVIDIA Tesla / 旧款数据中心卡 ====================
  "NVIDIA T4": [
    { platform: "Google Cloud (GCP)", price_usd: 0.35, plan: "按需", country: "美国", region: "北美", note: "最便宜云端推理 GPU", pricing_url: "https://cloud.google.com/compute/gpus-pricing" },
    { platform: "AWS (Amazon EC2)", price_usd: 0.45, plan: "按需(g4dn)", country: "美国", region: "北美", note: "含主机费用", pricing_url: "https://aws.amazon.com/ec2/pricing/on-demand/" },
    { platform: "Microsoft Azure", price_usd: 0.40, plan: "按需", country: "美国", region: "北美", note: "", pricing_url: "https://azure.microsoft.com/en-us/pricing/details/virtual-machines/linux/" },
    { platform: "Vast.ai", price_usd: 0.15, plan: "市场浮动价（起）", country: "美国", region: "北美", note: "", pricing_url: "https://vast.ai/pricing" },
    { platform: "OVHcloud", price_usd: 0.45, plan: "按需", country: "法国", region: "欧洲", note: "", pricing_url: "https://www.ovhcloud.com/en/public-cloud/prices/" },
    { platform: "阿里云 (Alibaba Cloud)", price_usd: 0.40, plan: "按需", country: "中国", region: "亚太", note: "", pricing_url: "https://www.alibabacloud.com/product/ecs/pricing" },
    { platform: "腾讯云 (Tencent Cloud)", price_usd: 0.38, plan: "按需", country: "中国", region: "亚太", note: "", pricing_url: "https://buy.cloud.tencent.com/price/cvm/overview" },
    { platform: "Vultr", price_usd: 0.50, plan: "按需", country: "美国", region: "北美", note: "", pricing_url: "https://www.vultr.com/products/cloud-gpu/" },
    { platform: "Google Colab", price_usd: 0.00, plan: "免费层", country: "美国", region: "北美", note: "免费版提供 T4; Pro $9.99/月起", pricing_url: "https://colab.research.google.com/signup" }
  ],

  "NVIDIA V100": [
    { platform: "Google Cloud (GCP)", price_usd: 1.80, plan: "按需", country: "美国", region: "北美", note: "上一代旗舰 GPU", pricing_url: "https://cloud.google.com/compute/gpus-pricing" },
    { platform: "AWS (Amazon EC2)", price_usd: 2.20, plan: "按需(p3)", country: "美国", region: "北美", note: "含主机费用", pricing_url: "https://aws.amazon.com/ec2/pricing/on-demand/" },
    { platform: "Vast.ai", price_usd: 0.25, plan: "市场浮动价（起）", country: "美国", region: "北美", note: "", pricing_url: "https://vast.ai/pricing" },
    { platform: "Genesis Cloud", price_usd: 0.60, plan: "按需", country: "冰岛/德国", region: "欧洲", note: "可再生能源", pricing_url: "https://genesiscloud.com/pricing" },
    { platform: "JarvisLabs", price_usd: 0.70, plan: "按需", country: "印度", region: "亚太", note: "", pricing_url: "https://jarvislabs.ai/pricing/" },
    { platform: "Paperspace", price_usd: 0.80, plan: "按需", country: "美国", region: "北美", note: "", pricing_url: "https://www.paperspace.com/pricing" },
    { platform: "OVHcloud", price_usd: 0.90, plan: "按需", country: "法国", region: "欧洲", note: "", pricing_url: "https://www.ovhcloud.com/en/public-cloud/prices/" }
  ],

  "NVIDIA Tesla P100 / P40": [
    { platform: "Vast.ai (P100)", price_usd: 0.10, plan: "市场浮动价（起）", country: "美国", region: "北美", note: "Pascal 架构，16GB 显存", pricing_url: "https://vast.ai/pricing" },
    { platform: "Vast.ai (P40)", price_usd: 0.09, plan: "市场浮动价（起）", country: "美国", region: "北美", note: "24GB 显存，Pascal 推理卡", pricing_url: "https://vast.ai/pricing" },
    { platform: "Google Cloud (GCP)", price_usd: 0.95, plan: "按需(P100)", country: "美国", region: "北美", note: "", pricing_url: "https://cloud.google.com/compute/gpus-pricing" }
  ],

  "NVIDIA Tesla K80 / M40 / M60": [
    { platform: "Vast.ai (K80)", price_usd: 0.05, plan: "市场浮动价（起）", country: "美国", region: "北美", note: "Kepler 架构，12GB × 2，最廉价的 GPU", pricing_url: "https://vast.ai/pricing" },
    { platform: "Vast.ai (M40)", price_usd: 0.06, plan: "市场浮动价（起）", country: "美国", region: "北美", note: "Maxwell 架构，24GB 显存", pricing_url: "https://vast.ai/pricing" }
  ],

  // ==================== AMD GPU 系列 ====================
  "AMD Radeon RX 7900 XTX / 7900 XT": [
    { platform: "Vast.ai (7900 XTX)", price_usd: 0.15, plan: "市场浮动价（起）", country: "美国", region: "北美", note: "24GB/20GB 显存，AMD 旗舰消费卡", pricing_url: "https://vast.ai/pricing" },
    { platform: "Vast.ai (7900 XT)", price_usd: 0.12, plan: "市场浮动价（起）", country: "美国", region: "北美", note: "20GB 显存，性价比 AMD 方案", pricing_url: "https://vast.ai/pricing" },
    { platform: "RunPod (Community Cloud)", price_usd: 0.44, plan: "社区云", country: "美国", region: "北美", note: "", pricing_url: "https://www.runpod.io/pricing" }
  ],

  "AMD Radeon RX 7800 XT / 7700 XT": [
    { platform: "Vast.ai (7800 XT)", price_usd: 0.10, plan: "市场浮动价（起）", country: "美国", region: "北美", note: "16GB 显存，中端 AMD", pricing_url: "https://vast.ai/pricing" },
    { platform: "Vast.ai (7700 XT)", price_usd: 0.08, plan: "市场浮动价（起）", country: "美国", region: "北美", note: "12GB 显存", pricing_url: "https://vast.ai/pricing" }
  ],

  "AMD Radeon RX 6900 XT / 6800 XT": [
    { platform: "Vast.ai (6900 XT)", price_usd: 0.10, plan: "市场浮动价（起）", country: "美国", region: "北美", note: "16GB 显存，RDNA2 旗舰", pricing_url: "https://vast.ai/pricing" },
    { platform: "Vast.ai (6800 XT)", price_usd: 0.08, plan: "市场浮动价（起）", country: "美国", region: "北美", note: "16GB 显存", pricing_url: "https://vast.ai/pricing" }
  ],

  "AMD Radeon RX 6800 / 6700 XT": [
    { platform: "Vast.ai (6800)", price_usd: 0.07, plan: "市场浮动价（起）", country: "美国", region: "北美", note: "16GB 显存，RDNA2 中端", pricing_url: "https://vast.ai/pricing" },
    { platform: "Vast.ai (6700 XT)", price_usd: 0.06, plan: "市场浮动价（起）", country: "美国", region: "北美", note: "12GB 显存", pricing_url: "https://vast.ai/pricing" }
  ],

  "AMD Radeon RX 7600 / 6600 XT": [
    { platform: "Vast.ai (7600)", price_usd: 0.06, plan: "市场浮动价（起）", country: "美国", region: "北美", note: "8GB 显存，RDNA3 入门级", pricing_url: "https://vast.ai/pricing" },
    { platform: "Vast.ai (6600 XT)", price_usd: 0.05, plan: "市场浮动价（起）", country: "美国", region: "北美", note: "8GB 显存", pricing_url: "https://vast.ai/pricing" }
  ],

  "AMD Instinct MI300X / MI250X": [
    { platform: "Microsoft Azure", price_usd: null, plan: "预览/询价", country: "美国", region: "北美", note: "AMD 数据中心 AI 加速器，MI300X 192GB HBM3", pricing_url: "https://azure.microsoft.com/en-us/pricing/details/virtual-machines/linux/" },
    { platform: "Oracle Cloud Infrastructure", price_usd: null, plan: "预览/询价", country: "美国", region: "北美", note: "OCI BM.GPU.MI300X.8 实例", pricing_url: "https://www.oracle.com/cloud/compute/pricing/" }
  ],

  // ==================== GTX 系列（vast.ai 最低价选项） ====================
  "NVIDIA GTX 1660 / 1660 Ti / 1660 Super": [
    { platform: "Vast.ai", price_usd: 0.05, plan: "市场浮动价（起）", country: "美国", region: "北美", note: "Turing 架构无 RT 核心，6GB 显存，极低价格", pricing_url: "https://vast.ai/pricing" }
  ],

  "NVIDIA GTX 1080 / 1080 Ti": [
    { platform: "Vast.ai (1080 Ti)", price_usd: 0.07, plan: "市场浮动价（起）", country: "美国", region: "北美", note: "11GB 显存，Pascal 经典卡", pricing_url: "https://vast.ai/pricing" },
    { platform: "Vast.ai (1080)", price_usd: 0.05, plan: "市场浮动价（起）", country: "美国", region: "北美", note: "8GB 显存", pricing_url: "https://vast.ai/pricing" }
  ],

  "NVIDIA GTX 1070 / 1070 Ti": [
    { platform: "Vast.ai", price_usd: 0.04, plan: "市场浮动价（起）", country: "美国", region: "北美", note: "8GB 显存，最廉价 8GB 以上显存选项", pricing_url: "https://vast.ai/pricing" }
  ],

  // ==================== 华为昇腾 / 百度昆仑国产芯片 ====================
  "华为昇腾 Ascend 910B / 910C": [
    { platform: "华为云 (Huawei Cloud)", price_usd: 2.00, plan: "按需", country: "中国", region: "亚太", note: "昇腾 NPU 自研芯片，集成 ModelArts", pricing_url: "https://www.huaweicloud.com/intl/en-us/pricing.html#/ecs" },
    { platform: "鹏城云脑 (Pengcheng Cloud Brain)", price_usd: null, plan: "科研申请", country: "中国", region: "亚太", note: "国家级 AI 计算平台，需申请使用", pricing_url: "https://cloudbrain.pcl.ac.cn/" }
  ],

  "百度昆仑芯": [
    { platform: "百度智能云 (Baidu AI Cloud)", price_usd: 1.80, plan: "按需", country: "中国", region: "亚太", note: "昆仑芯2代 AI 加速芯片", pricing_url: "https://cloud.baidu.com/product/gpu.html" }
  ],

  // ==================== 无服务器/API 平台（按量计费模式） ====================
  "无服务器/API 平台（按量计费）": [
    { platform: "Modal", price_usd: null, plan: "按秒计费", country: "美国", region: "北美", note: "Python 无服务器云，GPU 按使用秒数+内存计费", pricing_url: "https://modal.com/pricing" },
    { platform: "Replicate", price_usd: null, plan: "按次/按时计费", country: "美国", region: "北美", note: "AI 模型 API，按 GPU 运行时间和请求次数计费", pricing_url: "https://replicate.com/pricing" },
    { platform: "Fireworks.ai", price_usd: null, plan: "按 token 计费", country: "美国", region: "北美", note: "GenAI 推理平台，按输入/输出 token 计费", pricing_url: "https://fireworks.ai/pricing" },
    { platform: "Together AI", price_usd: null, plan: "按 token/小时", country: "美国", region: "北美", note: "开源模型推理+训练，推理按 token，训练按 GPU 小时", pricing_url: "https://www.together.ai/pricing" },
    { platform: "BentoML (BentoCloud)", price_usd: null, plan: "按请求计费", country: "美国", region: "北美", note: "无服务器推理平台，自动伸缩，按 GPU 使用量计费", pricing_url: "https://www.bentoml.com/pricing" },
    { platform: "Cerebrium", price_usd: null, plan: "按使用量计费", country: "南非", region: "其他", note: "无服务器 GPU 推理，按 GPU 秒+数据传输计费", pricing_url: "https://www.cerebrium.ai/pricing" },
    { platform: "Monster API", price_usd: null, plan: "按 token/实例", country: "美国", region: "北美", note: "API 优先 GPU 云，推理按 token、训练按 GPU 小时", pricing_url: "https://monsterapi.ai/pricing" },
    { platform: "Mystic AI", price_usd: null, plan: "按使用量计费", country: "英国", region: "欧洲", note: "无服务器 GPU 推理，pip 部署模型", pricing_url: "https://mystic.ai/pricing" },
    { platform: "Hugging Face (Inference Endpoints)", price_usd: null, plan: "按秒计费", country: "美国/法国", region: "北美", note: "托管推理，按 GPU 秒计费，支持 A100/T4/L4", pricing_url: "https://huggingface.co/pricing#endpoints" },
    { platform: "OctoML (OctoAI)", price_usd: null, plan: "按使用量计费", country: "美国", region: "北美", note: "自动化模型优化+部署，按推理量计费", pricing_url: "https://octoml.ai/pricing/" },
    { platform: "Deepnote", price_usd: null, plan: "订阅制", country: "美国", region: "北美", note: "协作数据笔记本，含 GPU 加速额度", pricing_url: "https://deepnote.com/pricing" },
    { platform: "Saturn Cloud", price_usd: null, plan: "订阅制", country: "美国", region: "北美", note: "数据科学云，GPU/Dask 集群按席位+用量计费", pricing_url: "https://saturncloud.io/pricing/" },
    { platform: "Coiled", price_usd: null, plan: "按使用量计费", country: "美国", region: "北美", note: "托管 Dask，GPU 按云资源消耗计费", pricing_url: "https://www.coiled.io/pricing" },
    { platform: "Anyscale", price_usd: null, plan: "按使用量计费", country: "美国", region: "北美", note: "Ray 平台，GPU 按底层云资源+平台费计费", pricing_url: "https://www.anyscale.com/pricing" },
    { platform: "Databricks", price_usd: null, plan: "按 DBU 计费", country: "美国", region: "北美", note: "GPU 集群按 Databricks Unit (DBU) + 云资源费计费", pricing_url: "https://www.databricks.com/product/pricing" },
    { platform: "CodeOcean", price_usd: null, plan: "订阅制", country: "美国", region: "北美", note: "可复现研究平台，GPU 计算胶囊", pricing_url: "https://codeocean.com/pricing" },
    { platform: "Google Colab", price_usd: 0.00, plan: "免费+订阅", country: "美国", region: "北美", note: "免费 T4 GPU; Pro $9.99/月，Pro+ $49.99/月", pricing_url: "https://colab.research.google.com/signup" }
  ],

  // ==================== 去中心化/区块链 GPU 平台 ====================
  "去中心化/区块链 GPU 平台": [
    { platform: "Salad", price_usd: 0.20, plan: "分布式云（起）", country: "美国", region: "北美", note: "利用全球闲置消费级 GPU，适合推理批处理", pricing_url: "https://salad.com/pricing" },
    { platform: "Akash Network", price_usd: 0.15, plan: "反向拍卖（起）", country: "美国", region: "北美", note: "DePIN 去中心化云，GPU 容器通过竞拍定价，AKT 代币结算", pricing_url: "https://akash.network/pricing/" },
    { platform: "Render Network", price_usd: null, plan: "代币结算", country: "美国", region: "北美", note: "区块链 GPU 渲染网络，按 OctaneBench 定价，RNDR 代币", pricing_url: "https://rendertoken.com/" },
    { platform: "Golem Network", price_usd: null, plan: "P2P 议价", country: "瑞士", region: "欧洲", note: "P2P 去中心化算力网络，GLM 代币结算，渲染和计算", pricing_url: "https://www.golem.network/" },
    { platform: "NiceHash", price_usd: null, plan: "市场竞价", country: "斯洛文尼亚", region: "欧洲", note: "算力市场，按哈希率竞价，BTC 结算，主要面向挖矿", pricing_url: "https://www.nicehash.com/pricing" },
    { platform: "Mining Rig Rentals", price_usd: null, plan: "P2P 租赁", country: "美国", region: "北美", note: "矿机租赁平台，按算力和时长计费", pricing_url: "https://www.miningrigrentals.com/" },
    { platform: "Q Blocks", price_usd: null, plan: "去中心化云", country: "美国", region: "北美", note: "聚合数据中心和矿工 GPU，Web3 AI 生态", pricing_url: "https://qblocks.cloud/" }
  ],

  // ==================== 裸金属/托管 GPU（需询价） ====================
  "裸金属/托管 GPU（需询价）": [
    { platform: "PhoenixNAP", price_usd: null, plan: "询价", country: "美国", region: "北美", note: "专用 GPU 托管，裸金属/VM，DL/VDI/区块链", pricing_url: "https://phoenixnap.com/gpu-hosting" },
    { platform: "Equinix Metal", price_usd: null, plan: "询价", country: "美国", region: "北美", note: "全球 Equinix 数据中心裸金属 GPU", pricing_url: "https://metal.equinix.com/product/servers/" },
    { platform: "Hivelocity", price_usd: null, plan: "询价/按需", country: "美国", region: "北美", note: "40+ 数据中心，即时部署 GPU 裸金属", pricing_url: "https://www.hivelocity.net/products/gpu-servers/" },
    { platform: "QuadraNet", price_usd: null, plan: "询价", country: "美国", region: "北美", note: "洛杉矶 GPU 托管，含 DDoS 防护", pricing_url: "https://quadranet.com/gpu-dedicated-servers" },
    { platform: "Psychz", price_usd: null, plan: "询价", country: "美国", region: "北美", note: "高性价比 GPU 服务器，美国/亚洲节点", pricing_url: "https://www.psychz.net/" },
    { platform: "TurnKey Internet", price_usd: null, plan: "询价", country: "美国", region: "北美", note: "纽约绿色数据中心 GPU，定制硬件", pricing_url: "https://turnkeyinternet.net/gpu-dedicated-server/" },
    { platform: "Dedicated.com", price_usd: null, plan: "询价", country: "美国", region: "北美", note: "入门级 GPU 托管，低成本方案", pricing_url: "https://dedicated.com/dedicated-servers/gpu" },
    { platform: "Rackspace Technology", price_usd: null, plan: "询价", country: "美国", region: "北美", note: "托管 GPU 方案，支持 AI/ML/VDI", pricing_url: "https://www.rackspace.com/cloud/gpu" },
    { platform: "ServerMania", price_usd: null, plan: "询价", country: "加拿大", region: "北美", note: "可定制 GPU 专用服务器，10Gbps 网络", pricing_url: "https://www.servermania.com/gpu-servers.htm" },
    { platform: "DataPacket", price_usd: null, plan: "询价", country: "美国/英国", region: "北美", note: "裸金属 GPU，全球20+节点，不限流量", pricing_url: "https://www.datapacket.com/gpu-hosting" },
    { platform: "Servers.com", price_usd: null, plan: "按需/月付", country: "荷兰", region: "欧洲", note: "全球裸金属 GPU 实例，灵活计费", pricing_url: "https://www.servers.com/gpu-servers/" },
    { platform: "21Cloud", price_usd: null, plan: "询价", country: "荷兰", region: "欧洲", note: "荷兰 GPU 云和托管，合规 HPC", pricing_url: "https://www.21cloud.com/cloud/gpu-cloud" },
    { platform: "Hostkey", price_usd: null, plan: "询价", country: "荷兰", region: "欧洲", note: "即开 GPU 服务器，欧洲/美国节点", pricing_url: "https://www.hostkey.com/gpu-servers" },
    { platform: "Cherry Servers", price_usd: null, plan: "按需/预留", country: "立陶宛", region: "欧洲", note: "裸金属 GPU 可定制，全球 BGP", pricing_url: "https://www.cherryservers.com/pricing/gpu-servers" },
    { platform: "Leaseweb", price_usd: null, plan: "询价", country: "荷兰", region: "欧洲", note: "托管/非托管 GPU 服务器，欧/美/亚节点", pricing_url: "https://www.leaseweb.com/en/dedicated-servers/gpu" },
    { platform: "G-Core Labs", price_usd: null, plan: "询价", country: "卢森堡", region: "欧洲", note: "全球边缘 GPU 优化云", pricing_url: "https://gcore.com/cloud/gpu-cloud" },
    { platform: "UpCloud", price_usd: null, plan: "询价", country: "芬兰", region: "欧洲", note: "高性能 GPU 计算，MaxIOPS 存储", pricing_url: "https://upcloud.com/pricing/" },
    { platform: "Exoscale", price_usd: null, plan: "询价", country: "瑞士", region: "欧洲", note: "瑞士云 GPU，欧洲数据法规合规", pricing_url: "https://www.exoscale.com/gpu/" },
    { platform: "T-Systems (Open Telekom Cloud)", price_usd: null, plan: "询价", country: "德国", region: "欧洲", note: "欧洲主权云，严格 GDPR，德国电信", pricing_url: "https://open-telekom-cloud.com/en/pricing/" },
    { platform: "Aruba Cloud", price_usd: null, plan: "询价", country: "意大利", region: "欧洲", note: "意大利云，小型企业 GPU VPS", pricing_url: "https://www.arubacloud.com/cloud-pricing.aspx" },
    { platform: "LeaderGPU", price_usd: null, plan: "按月定价", country: "法国", region: "欧洲", note: "专用 GPU 服务器，欧洲/美国，统一定价", pricing_url: "https://www.leadergpu.com/pricing" },
    { platform: "SabrePC", price_usd: null, plan: "询价", country: "美国", region: "北美", note: "工作站级 GPU 云，可配置裸金属", pricing_url: "https://www.sabrepc.com/hpc-cloud" },
    { platform: "Applied Digital", price_usd: null, plan: "询价", country: "美国", region: "北美", note: "高密度 GPU 托管，液冷，HPC/挖矿", pricing_url: "https://www.applieddigital.com/" },
    { platform: "Rescale", price_usd: null, plan: "询价", country: "美国", region: "北美", note: "云 HPC 平台，多云端 GPU，航空航天/汽车仿真", pricing_url: "https://www.rescale.com/pricing/" },
    { platform: "Cirrascale", price_usd: null, plan: "询价", country: "美国", region: "北美", note: "大规模 GPU 集群，自动驾驶训练", pricing_url: "https://www.cirrascale.com/cloud-services/" },
    { platform: "Bizon", price_usd: null, plan: "询价", country: "美国", region: "北美", note: "液冷 GPU 云和工作站，深度学习优化", pricing_url: "https://bizon.ai/pricing" },
    { platform: "Akamai Linode", price_usd: null, plan: "询价", country: "美国", region: "北美", note: "GPU 实例（Quadro RTX），简单可预测定价", pricing_url: "https://www.linode.com/pricing/#compute-gpu" }
  ],

  // ==================== 中国云平台（部分需询价） ====================
  "中国云平台 GPU（部分需询价）": [
    { platform: "中国移动云 (China Mobile Cloud)", price_usd: null, plan: "询价", country: "中国", region: "亚太", note: "运营商云，GPU VM/容器，边缘 AI 推理", pricing_url: "https://ecloud.10086.cn/home/product-introduction/gpu" },
    { platform: "天翼云 (China Telecom e-Surfing Cloud)", price_usd: null, plan: "询价", country: "中国", region: "亚太", note: "中国电信云，全国基础设施 GPU 实例", pricing_url: "https://www.ctyun.cn/product/gpu" },
    { platform: "联通云 (China Unicom Cloud)", price_usd: null, plan: "询价", country: "中国", region: "亚太", note: "中国联通云，结合5G边缘低延迟推理", pricing_url: "https://www.cucloud.cn/product/gpu.html" },
    { platform: "浪潮云 (Inspur Cloud)", price_usd: null, plan: "询价", country: "中国", region: "亚太", note: "浪潮 HPC 传统优势，科学计算/AI 建模", pricing_url: "https://cloud.inspur.com/product/gpu/" },
    { platform: "京东云 (JD Cloud)", price_usd: null, plan: "询价", country: "中国", region: "亚太", note: "GPU VM/物理服务器，电商 AI/图像识别", pricing_url: "https://www.jdcloud.com/cn/public/compute/gpu" },
    { platform: "金山云 (Kingsoft Cloud)", price_usd: null, plan: "询价", country: "中国", region: "亚太", note: "KEC GPU 系列，游戏/媒体领域", pricing_url: "https://www.ksyun.com/post/product/KEC.html" },
    { platform: "UCloud", price_usd: null, plan: "询价", country: "中国", region: "亚太", note: "GPU 云主机和裸金属，中国/东南亚", pricing_url: "https://www.ucloud.cn/site/product/uhost.html" },
    { platform: "青云 (QingCloud)", price_usd: null, plan: "询价", country: "中国", region: "亚太", note: "GPU 计算实例，灵活 SDN 网络", pricing_url: "https://www.qingcloud.com/products/gpu_server/" },
    { platform: "并行科技 (Paratera)", price_usd: null, plan: "询价", country: "中国", region: "亚太", note: "HPC 云，可扩展 GPU 节点，高校/工业", pricing_url: "https://www.paratera.com/" },
    { platform: "极视角 (Video++ AI Cloud)", price_usd: null, plan: "询价", country: "中国", region: "亚太", note: "AI 视频识别 GPU 云", pricing_url: "https://www.videopuzzles.com/" }
  ],

  // ==================== 日韩平台 ====================
  "日韩云平台 GPU": [
    { platform: "Sakura Internet", price_usd: null, plan: "询价", country: "日本", region: "亚太", note: "日本云 GPU 实例，日本国内广泛使用", pricing_url: "https://www.sakura.ad.jp/services/cloud/gpu/" },
    { platform: "IIJ GIO", price_usd: null, plan: "询价", country: "日本", region: "亚太", note: "日本 IIJ 骨干网 GPU 云主机", pricing_url: "https://www.iij.ad.jp/biz/gio/" },
    { platform: "KT Cloud", price_usd: null, plan: "询价", country: "韩国", region: "亚太", note: "韩国电信 GPU 云，AI/媒体/游戏", pricing_url: "https://cloud.kt.com/" },
    { platform: "Naver Cloud", price_usd: null, plan: "询价", country: "韩国", region: "亚太", note: "韩国 Naver GPU 服务器，DL/VDI", pricing_url: "https://www.ncloud.com/product/compute/gpu" }
  ],

  // ==================== 其他地区 ====================
  "其他地区平台": [
    { platform: "Yandex Cloud", price_usd: null, plan: "询价", country: "俄罗斯", region: "亚太", note: "俄罗斯最大云平台，GPU VM/K8s", pricing_url: "https://cloud.yandex.com/en/services/compute#pricing" },
    { platform: "JarvisLabs", price_usd: 1.10, plan: "按需", country: "印度", region: "亚太", note: "印度 GPU 云，预装 DL 框架，即开即用", pricing_url: "https://jarvislabs.ai/pricing/" }
  ],

  // ==================== 中国超算中心（科研申请制） ====================
  "中国超算中心（申请制）": [
    { platform: "鹏城云脑 (Pengcheng Cloud Brain)", price_usd: null, plan: "科研申请", country: "中国", region: "亚太", note: "深圳国家级 AI 计算平台，华为昇腾 NPU 集群", pricing_url: "https://cloudbrain.pcl.ac.cn/" },
    { platform: "之江实验室 (Zhejiang Lab)", price_usd: null, plan: "科研合作", country: "中国", region: "亚太", note: "浙江省研究型 GPU 集群，AI/机器人", pricing_url: "https://www.zhejianglab.com/" },
    { platform: "国家超算深圳中心 (NSCC-SZ)", price_usd: null, plan: "申请制", country: "中国", region: "亚太", note: "公共超算中心，面向政府/学术界", pricing_url: "http://www.nsccsz.gov.cn/" },
    { platform: "国家超算广州中心 (NSCC-GZ)", price_usd: null, plan: "申请制", country: "中国", region: "亚太", note: "天河二号/天河星逸，气象/基因组/CAE", pricing_url: "https://www.nscc-gz.cn/" },
    { platform: "国家超算天津中心 (NSCC-TJ)", price_usd: null, plan: "申请制", country: "中国", region: "亚太", note: "天河系列超算，科学研究和创新项目", pricing_url: "https://nscc-tj.cn/" },
    { platform: "国家超算无锡中心 (NSCC-WX)", price_usd: null, plan: "申请制", country: "中国", region: "亚太", note: "神威太湖之光，AI/地球科学仿真", pricing_url: "http://www.nsccwx.cn/" },
    { platform: "上海超算中心 (SSCS)", price_usd: null, plan: "申请制", country: "中国", region: "亚太", note: "上海市级 HPC，药物/汽车/金融", pricing_url: "https://www.sscs.cn/" },
    { platform: "北京超级云计算中心 (BLSC)", price_usd: null, plan: "申请制", country: "中国", region: "亚太", note: "云化超算，弹性 GPU 深度学习", pricing_url: "https://www.blsc.cn/" },
    { platform: "合肥先进计算中心 (Hefei ACC)", price_usd: null, plan: "申请制", country: "中国", region: "亚太", note: "中科大 GPU 集群，量子化学/材料", pricing_url: "http://www.hpcc.ustc.edu.cn/" }
  ]
};

// 导出（Node.js 兼容），浏览器直接使用全局变量 window.GPU_PRICING
if (typeof module !== 'undefined' && module.exports) {
  module.exports = GPU_PRICING;
}
