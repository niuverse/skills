# Web Searcher 资源汇总

## 搜索引擎 API

### Brave Search (推荐)
- **文档**: https://api.search.brave.com/
- **定价**: 免费 2000 次/月，付费 $3/1000 次
- **特点**: 隐私优先，结果质量高，速度快
- **注册**: https://brave.com/search/api/

### Google Custom Search
- **文档**: https://developers.google.com/custom-search/v1/overview
- **定价**: 免费 100 次/天，付费 $5/1000 次
- **特点**: 覆盖最广，支持站点限制
- **注册**: 
  1. https://programmablesearchengine.google.com/ (获取 CX)
  2. https://console.cloud.google.com/ (获取 API Key)

### DuckDuckGo
- **文档**: https://duckduckgo.com/
- **定价**: 免费 (无需 API Key)
- **特点**: 隐私保护，无需注册
- **Python 库**: https://github.com/deedy5/duckduckgo-search

### Bing Search
- **文档**: https://www.microsoft.com/en-us/bing/apis/bing-web-search-api
- **定价**: 免费 1000 次/月
- **特点**: 微软生态，企业友好

### Perplexity
- **文档**: https://docs.perplexity.ai/
- **定价**: 付费，按 token 计费
- **特点**: AI 驱动，自动生成摘要

### SearXNG (自托管)
- **GitHub**: https://github.com/searxng/searxng
- **特点**: 完全隐私，自托管
- **部署**: Docker 一键部署

## 学术搜索

### arXiv
- **API**: https://arxiv.org/help/api
- **Python**: `pip install arxiv`

### Google Scholar
- **限制**: 无官方 API，需使用第三方库
- **Python**: `scholarly` 库

### Semantic Scholar
- **API**: https://api.semanticscholar.org/
- **特点**: 免费，支持引用图谱

## 新闻搜索

### NewsAPI
- **网站**: https://newsapi.org/
- **定价**: 免费 100 次/天

### HackerNews API
- **文档**: https://github.com/HackerNews/API
- **特点**: 技术新闻，免费

## 内容提取

### Newspaper3k
- **GitHub**: https://github.com/codelucas/newspaper
- **用途**: 新闻文章提取

### Trafilatura
- **GitHub**: https://github.com/adbar/trafilatura
- **用途**: 网页正文提取

### Readability
- **GitHub**: https://github.com/buriy/python-readability
- **用途**: 正文提取

## 相关 Skills

### OpenClaw 官方
- `web_search` - 内置 Brave Search
- `web_fetch` - 网页获取

### 社区 Skills
- `local-websearch` - SearXNG 自托管
- `multi-search-engine` - 多引擎聚合

## 最佳实践

1. **API Key 轮换**: 配置多个引擎避免单点故障
2. **结果去重**: 使用 URL 或内容相似度去重
3. **缓存结果**: 相同查询缓存 1 小时
4. **尊重 Robots**: 遵守网站的 robots.txt
5. **错误处理**: 一个引擎失败时自动切换
