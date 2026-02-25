#!/usr/bin/env python3
"""
环境验证工具
检查 web-searcher skill 的依赖和 API 配置
"""

import sys
import os


def check_module(name: str, import_name: str = None) -> bool:
    """检查模块是否安装"""
    import_name = import_name or name
    try:
        __import__(import_name)
        print(f"  ✅ {name}")
        return True
    except ImportError:
        print(f"  ❌ {name} (未安装)")
        return False


def main():
    print("🔍 检查 Web Searcher Skill 依赖...\n")
    
    # 必需依赖
    print("必需依赖:")
    required = [
        ("requests", "requests"),
    ]
    
    required_ok = all(check_module(name, imp) for name, imp in required)
    
    # 可选依赖
    print("\n可选依赖 (增强功能):")
    optional = [
        ("duckduckgo-search", "duckduckgo_search"),
        ("beautifulsoup4", "bs4"),
        ("lxml", "lxml"),
    ]
    
    optional_ok = [check_module(name, imp) for name, imp in optional]
    
    # API Key 检查
    print("\nAPI 配置:")
    apis = {
        "BRAVE_API_KEY": "Brave Search (推荐)",
        "GOOGLE_API_KEY": "Google Custom Search",
        "GOOGLE_CX": "Google Search Engine ID",
        "PERPLEXITY_API_KEY": "Perplexity API",
    }
    
    for env_var, description in apis.items():
        if os.getenv(env_var):
            print(f"  ✅ {description}")
        else:
            print(f"  ⚠️  {description} (未设置)")
    
    # 总结
    print("\n" + "="*40)
    if required_ok:
        print("✅ 必需依赖已满足，可以基本使用")
    else:
        print("❌ 缺少必需依赖，请安装:")
        print("   pip install requests")
    
    optional_count = sum(optional_ok)
    print(f"\n📊 可选依赖: {optional_count}/{len(optional)} 已安装")
    
    if optional_count < len(optional):
        print("\n💡 安装所有可选依赖以获得最佳体验:")
        print("   pip install duckduckgo-search beautifulsoup4 lxml")
    
    print("\n🔑 API Key 获取:")
    print("   Brave: https://brave.com/search/api/ (免费 2000 次/月)")
    print("   Google: https://developers.google.com/custom-search/v1/overview")
    print("   Perplexity: https://www.perplexity.ai/settings/api")
    
    print("\n💡 快速开始:")
    print("   python scripts/search.py 'Python 教程'")
    
    return 0 if required_ok else 1


if __name__ == "__main__":
    sys.exit(main())
