# Web Searcher

🔍 全面细致的互联网搜索工具

## 功能

- 多引擎搜索聚合 (Brave, Google, DuckDuckGo)
- 内容提取和摘要
- 学术搜索 (arXiv, Google Scholar)
- 新闻搜索

## 快速开始

```bash
# 验证环境
python scripts/verify_env.py

# 基础搜索
python scripts/search.py "Python 教程"

# 深度搜索
python scripts/search.py "AI 最新进展" --deep --max-results 20

# 保存结果
python scripts/search.py "Rust vs Go" --output results.json
```

## 配置 API Keys

```bash
# Brave Search (推荐)
export BRAVE_API_KEY="your-key"

# Google Custom Search
export GOOGLE_API_KEY="your-key"
export GOOGLE_CX="your-cx"
```

## 依赖

```bash
pip install requests duckduckgo-search
```

## 参考

- [resources.md](references/resources.md) - API 文档和资源
