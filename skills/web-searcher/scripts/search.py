#!/usr/bin/env python3
"""
Web Search 核心模块
支持多引擎搜索和内容提取
"""

import argparse
import json
import os
import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, asdict
from typing import List, Optional, Dict, Any
from urllib.parse import quote_plus, urlparse

import requests
from datetime import datetime, timedelta


@dataclass
class SearchResult:
    """搜索结果数据结构"""
    title: str
    url: str
    snippet: str
    source: str  # 搜索引擎来源
    rank: int
    content: Optional[str] = None  # 提取的完整内容
    published_date: Optional[str] = None
    
    def to_dict(self) -> Dict:
        return asdict(self)


class BaseSearchEngine:
    """搜索引擎基类"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
    
    def search(self, query: str, max_results: int = 10) -> List[SearchResult]:
        """执行搜索，子类必须实现"""
        raise NotImplementedError


class BraveSearchEngine(BaseSearchEngine):
    """Brave Search API"""
    
    API_URL = "https://api.search.brave.com/res/v1/web/search"
    
    def search(self, query: str, max_results: int = 10) -> List[SearchResult]:
        if not self.api_key:
            raise ValueError("Brave Search 需要 API key")
        
        headers = {
            "X-Subscription-Token": self.api_key,
            "Accept": "application/json"
        }
        
        params = {
            "q": query,
            "count": min(max_results, 20),
            "offset": 0
        }
        
        try:
            response = self.session.get(
                self.API_URL,
                headers=headers,
                params=params,
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            
            results = []
            for i, item in enumerate(data.get("web", {}).get("results", [])):
                results.append(SearchResult(
                    title=item.get("title", ""),
                    url=item.get("url", ""),
                    snippet=item.get("description", ""),
                    source="brave",
                    rank=i + 1
                ))
            
            return results
            
        except Exception as e:
            print(f"Brave Search 错误: {e}", file=sys.stderr)
            return []


class DuckDuckGoSearchEngine(BaseSearchEngine):
    """DuckDuckGo 搜索 (无需 API key)"""
    
    def search(self, query: str, max_results: int = 10) -> List[SearchResult]:
        try:
            # 使用 duckduckgo-search 库
            from duckduckgo_search import DDGS
            
            with DDGS() as ddgs:
                results = []
                for i, r in enumerate(ddgs.text(query, max_results=max_results)):
                    results.append(SearchResult(
                        title=r.get("title", ""),
                        url=r.get("href", ""),
                        snippet=r.get("body", ""),
                        source="duckduckgo",
                        rank=i + 1
                    ))
                return results
                
        except ImportError:
            print("请安装 duckduckgo-search: pip install duckduckgo-search", file=sys.stderr)
            return []
        except Exception as e:
            print(f"DuckDuckGo 错误: {e}", file=sys.stderr)
            return []


class GoogleSearchEngine(BaseSearchEngine):
    """Google Custom Search API"""
    
    API_URL = "https://www.googleapis.com/customsearch/v1"
    
    def __init__(self, api_key: Optional[str] = None, cx: Optional[str] = None):
        super().__init__(api_key)
        self.cx = cx
    
    def search(self, query: str, max_results: int = 10) -> List[SearchResult]:
        if not self.api_key or not self.cx:
            raise ValueError("Google Search 需要 API key 和 CX")
        
        params = {
            "key": self.api_key,
            "cx": self.cx,
            "q": query,
            "num": min(max_results, 10)
        }
        
        try:
            response = self.session.get(
                self.API_URL,
                params=params,
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            
            results = []
            for i, item in enumerate(data.get("items", [])):
                results.append(SearchResult(
                    title=item.get("title", ""),
                    url=item.get("link", ""),
                    snippet=item.get("snippet", ""),
                    source="google",
                    rank=i + 1
                ))
            
            return results
            
        except Exception as e:
            print(f"Google Search 错误: {e}", file=sys.stderr)
            return []


class WebSearcher:
    """网页搜索器"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.engines: Dict[str, BaseSearchEngine] = {}
        self._init_engines()
    
    def _init_engines(self):
        """初始化搜索引擎"""
        # Brave
        brave_key = os.getenv("BRAVE_API_KEY")
        if brave_key:
            self.engines["brave"] = BraveSearchEngine(brave_key)
        
        # Google
        google_key = os.getenv("GOOGLE_API_KEY")
        google_cx = os.getenv("GOOGLE_CX")
        if google_key and google_cx:
            self.engines["google"] = GoogleSearchEngine(google_key, google_cx)
        
        # DuckDuckGo (无需 API key)
        self.engines["duckduckgo"] = DuckDuckGoSearchEngine()
    
    def search(self, query: str, engines: Optional[List[str]] = None, 
               max_results: int = 10) -> List[SearchResult]:
        """
        执行搜索
        
        Args:
            query: 搜索查询
            engines: 指定引擎列表，None 则使用所有可用引擎
            max_results: 每个引擎的最大结果数
            
        Returns:
            搜索结果列表
        """
        if not engines:
            engines = list(self.engines.keys())
        
        all_results = []
        
        for engine_name in engines:
            if engine_name not in self.engines:
                print(f"警告: 引擎 {engine_name} 未配置", file=sys.stderr)
                continue
            
            engine = self.engines[engine_name]
            try:
                results = engine.search(query, max_results)
                all_results.extend(results)
                print(f"✅ {engine_name}: {len(results)} 条结果")
            except Exception as e:
                print(f"❌ {engine_name}: {e}", file=sys.stderr)
        
        # 按排名排序
        all_results.sort(key=lambda x: x.rank)
        
        return all_results
    
    def search_deep(self, query: str, max_results: int = 10,
                   extract_content: bool = False) -> List[SearchResult]:
        """
        深度搜索 - 聚合多引擎结果并可提取内容
        
        Args:
            query: 搜索查询
            max_results: 最大结果数
            extract_content: 是否提取网页内容
            
        Returns:
            搜索结果列表
        """
        results = self.search(query, max_results=max_results)
        
        if extract_content:
            print("📄 提取网页内容...")
            for result in results:
                try:
                    result.content = self._extract_content(result.url)
                except Exception as e:
                    print(f"  无法提取 {result.url}: {e}")
        
        return results
    
    def _extract_content(self, url: str) -> Optional[str]:
        """提取网页正文内容"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            # 简单的文本提取
            text = response.text
            # 移除 script 和 style
            text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL)
            text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
            # 提取文本
            text = re.sub(r'<[^>]+>', ' ', text)
            # 清理空白
            text = ' '.join(text.split())
            
            return text[:5000]  # 限制长度
            
        except Exception:
            return None
    
    def save_results(self, results: List[SearchResult], output_path: str):
        """保存结果到文件"""
        output = {
            "query": "",
            "timestamp": datetime.now().isoformat(),
            "total_results": len(results),
            "results": [r.to_dict() for r in results]
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 结果已保存: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="网页搜索工具")
    parser.add_argument("query", help="搜索查询")
    parser.add_argument("--engines", "-e", help="搜索引擎 (逗号分隔)")
    parser.add_argument("--max-results", "-n", type=int, default=10, help="最大结果数")
    parser.add_argument("--deep", "-d", action="store_true", help="深度搜索")
    parser.add_argument("--extract", action="store_true", help="提取网页内容")
    parser.add_argument("--output", "-o", help="输出文件路径")
    
    args = parser.parse_args()
    
    searcher = WebSearcher()
    
    engines = args.engines.split(",") if args.engines else None
    
    if args.deep or args.extract:
        results = searcher.search_deep(
            args.query,
            max_results=args.max_results,
            extract_content=args.extract
        )
    else:
        results = searcher.search(
            args.query,
            engines=engines,
            max_results=args.max_results
        )
    
    # 显示结果
    print(f"\n🔍 找到 {len(results)} 条结果:\n")
    for r in results[:10]:
        print(f"[{r.source}] {r.title}")
        print(f"  {r.url}")
        print(f"  {r.snippet[:150]}...")
        print()
    
    # 保存结果
    if args.output:
        searcher.save_results(results, args.output)


if __name__ == "__main__":
    main()
