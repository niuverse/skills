#!/usr/bin/env python3
"""
环境验证工具
检查 coding-agent skill 的依赖是否安装
"""

import sys
from typing import Optional


def check_module(name: str, import_name: Optional[str] = None) -> bool:
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
    print("🔍 检查 Coding Agent Skill 依赖...\n")
    
    # 必需依赖
    print("必需依赖:")
    required = [
        ("pyyaml", "yaml"),
        ("requests", "requests"),
    ]
    
    required_ok = all(check_module(name, imp) for name, imp in required)
    
    # API 客户端依赖
    print("\nAPI 客户端 (至少安装一个):")
    clients = [
        ("openai", "openai"),
        ("anthropic", "anthropic"),
        ("google-generativeai", "google.generativeai"),
        ("httpx", "httpx"),
    ]
    
    clients_ok = [check_module(name, imp) for name, imp in clients]
    
    # 可选依赖
    print("\n可选依赖:")
    optional = [
        ("aiohttp", "aiohttp"),
        ("rich", "rich"),
    ]
    
    optional_ok = [check_module(name, imp) for name, imp in optional]
    
    # 总结
    print("\n" + "="*40)
    if required_ok:
        print("✅ 必需依赖已满足")
    else:
        print("❌ 缺少必需依赖，请安装:")
        print("   pip install pyyaml requests")
    
    if any(clients_ok):
        print(f"✅ API 客户端: {sum(clients_ok)}/{len(clients_ok)} 已安装")
    else:
        print("⚠️  未安装任何 API 客户端，请至少安装一个:")
        print("   pip install openai  # 用于 Codex/GPT-4")
        print("   pip install anthropic  # 用于 Claude")
        print("   pip install google-generativeai  # 用于 Gemini")
    
    print(f"\n📊 可选依赖: {sum(optional_ok)}/{len(optional_ok)} 已安装")
    
    # 配置检查
    print("\n" + "="*40)
    print("配置检查:")
    
    env_vars = ["CODEX_API_KEY", "ANTHROPIC_API_KEY", "GEMINI_API_KEY", "OPENAI_API_KEY"]
    for var in env_vars:
        import os
        if os.getenv(var):
            print(f"  ✅ {var}")
        else:
            print(f"  ⚠️  {var} (未设置)")
    
    print("\n💡 快速开始:")
    print("   1. python scripts/configure.py --init")
    print("   2. 设置 API 密钥环境变量")
    print("   3. python scripts/orchestrate.py --mode single --agent codex --task 'Hello World'")
    
    return 0 if required_ok and any(clients_ok) else 1


if __name__ == "__main__":
    sys.exit(main())
