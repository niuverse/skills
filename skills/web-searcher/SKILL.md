---
name: web-searcher
description: |
  Comprehensive web search skill for OpenClaw. Aggregates results from multiple search engines
  including Brave, Google, DuckDuckGo, Bing, and SearXNG for maximum coverage.
  
  Features:
  - Multi-engine search aggregation
  - Content extraction and summarization
  - Academic paper search (arXiv, Google Scholar)
  - News search with time filtering
  - Image and video search
  - Privacy-focused options (DuckDuckGo, SearXNG)
  
  Triggers: web search, search internet, google search, brave search, 
  duckduckgo, find online, research, look up, search news, academic search
---

# Web Searcher

🔍 全面细致的互联网搜索工具 - 聚合多引擎结果

## 🎯 核心能力

| 能力 | 描述 |
|------|------|
| **多引擎聚合** | 同时查询 Brave、Google、DuckDuckGo、Bing |
| **内容提取** | 自动获取网页正文，去除广告和干扰 |
| **智能摘要** | 生成搜索结果的综合摘要 |
| **学术搜索** | 专门优化 arXiv、Google Scholar 搜索 |
| **新闻搜索** | 支持按时间筛选最新资讯 |
| **隐私保护** | 支持 DuckDuckGo、SearXNG 隐私搜索 |

## 🚀 支持的搜索引擎

| 引擎 | 特点 | 需要 API Key |
|------|------|--------------|
| **Brave** | 隐私优先，结果质量高 | ✅ |
| **Google** | 覆盖最广，实时性强 | ✅ (Custom Search) |
| **DuckDuckGo** | 隐私保护，无需注册 | ❌ |
| **Bing** | 微软生态，企业友好 | ✅ |
| **SearXNG** | 自托管，完全隐私 | ❌ (自托管) |
| **Perplexity** | AI 驱动，带摘要 | ✅ |

## 📖 使用模式

### 模式 1: 快速搜索 (默认)

```bash
python scripts/search.py "最新 AI 模型发布"
```

### 模式 2: 深度研究

```bash
python scripts/search.py "量子计算最新进展" --deep --engines brave,google,perplexity
```

### 模式 3: 学术搜索

```bash
python scripts/search.py "transformer architecture" --academic
```

### 模式 4: 新闻搜索

```bash
python scripts/search.py "OpenAI 新闻" --news --days 7
```

## 🛠️ 快速开始

### 1. 环境验证
```bash
python scripts/verify_env.py
```

### 2. 配置 API Keys (可选但推荐)
```bash
# Brave Search (推荐)
export BRAVE_API_KEY="your-key"

# Google Custom Search
export GOOGLE_API_KEY="your-key"
export GOOGLE_CX="your-cx"

# Perplexity
export PERPLEXITY_API_KEY="your-key"
```

### 3. 运行搜索
```bash
# 基础搜索
python scripts/search.py "Python 最佳实践"

# 深度搜索 (多引擎 + 内容提取)
python scripts/search.py "机器学习趋势" --deep --max-results 20

# 保存结果
python scripts/search.py "Rust vs Go" --output results.md
```

## 📋 详细用法

### Python API

```python
from scripts.search import WebSearcher

# 创建搜索器
searcher = WebSearcher()

# 基础搜索
results = searcher.search("最新 AI 新闻", max_results=10)

# 深度搜索 (提取内容)
results = searcher.search_deep(
    "量子计算突破",
    engines=["brave", "perplexity"],
    extract_content=True
)

# 学术搜索
papers = searcher.search_academic(
    "attention mechanism",
    sources=["arxiv", "scholar"]
)

# 新闻搜索
news = searcher.search_news(
    "科技行业",
    days=7,
    sources=["techcrunch", "verge"]
)
```

### 多引擎聚合

```python
from scripts.search import MultiEngineSearcher

# 创建多引擎搜索器
multi = MultiEngineSearcher([
    "brave",
    "duckduckgo", 
    "google"
])

# 并行搜索
results = multi.search_aggregate(
    "Python 3.12 新特性",
    deduplicate=True,  # 去重
    rank_by="relevance"  # 智能排序
)
```

## 🔧 配置

### config.yaml

```yaml
engines:
  brave:
    enabled: true
    api_key: ${BRAVE_API_KEY}
    priority: 1
    
  google:
    enabled: true
    api_key: ${GOOGLE_API_KEY}
    cx: ${GOOGLE_CX}
    priority: 2
    
  duckduckgo:
    enabled: true
    priority: 3
    
  perplexity:
    enabled: true
    api_key: ${PERPLEXITY_API_KEY}
    priority: 1

defaults:
  max_results: 10
  timeout: 30
  extract_content: false
  
academic_sources:
  - arxiv
  - scholar
  - semanticscholar
  
news_sources:
  - techcrunch
  - verge
  - hackernews
```

## 📊 搜索引擎对比

| 特性 | Brave | Google | DuckDuckGo | Perplexity |
|------|-------|--------|------------|------------|
| 结果质量 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 实时性 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| 隐私保护 | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 无需 API Key | ❌ | ❌ | ✅ | ❌ |
| 内容摘要 | ❌ | ❌ | ❌ | ✅ |
| 中文支持 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |

## 🎭 典型工作流

### 工作流 1: 研究新领域

```bash
# 1. 广泛搜索
python scripts/search.py "向量数据库对比" --deep --max-results 30

# 2. 学术补充
python scripts/search.py "vector database survey" --academic

# 3. 最新动态
python scripts/search.py "vector database news" --news --days 30
```

### 工作流 2: 技术调研

```bash
# 对比多个技术
python scripts/search.py "React vs Vue 2025" --deep --output comparison.md
```

### 工作流 3: 事实核查

```bash
# 多引擎交叉验证
python scripts/search.py "某新闻事件" --engines brave,google,duckduckgo --verify
```

## 🚨 故障排除

| 问题 | 解决方案 |
|------|----------|
| API 限制 | 切换到 DuckDuckGo 或配置多个 API key |
| 结果太少 | 启用更多引擎或放宽搜索词 |
| 内容提取失败 | 检查网络连接或尝试其他引擎 |
| 中文结果差 | 优先使用 Google 或添加中文关键词 |

## 📚 参考资料

- [resources.md](references/resources.md) - 搜索引擎 API 文档
- [engines.md](references/engines.md) - 各引擎详细配置

## 免费 API 获取

### Brave Search
1. 访问 https://brave.com/search/api/
2. 注册获取免费额度 (2000 次/月)

### Google Custom Search
1. 访问 https://programmablesearchengine.google.com/
2. 创建搜索引擎获取 CX ID
3. 访问 https://developers.google.com/custom-search/v1/overview 获取 API Key

### Perplexity
1. 访问 https://www.perplexity.ai/settings/api
2. 注册获取 API key

---

*Search smarter, not harder.* 🔎
