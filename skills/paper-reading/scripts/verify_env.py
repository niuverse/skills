#!/usr/bin/env python3
"""
环境验证工具
检查 paper-reading skill 的依赖是否安装
"""

import sys


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
    print("🔍 检查 Paper Reading Skill 依赖...\n")
    
    # 必需依赖
    print("必需依赖:")
    required = [
        ("pymupdf", "fitz"),
        ("requests", "requests"),
    ]
    
    required_ok = all(check_module(name, imp) for name, imp in required)
    
    # 可选依赖
    print("\n可选依赖 (增强功能):")
    optional = [
        ("mineru", "mineru"),
        ("pdfplumber", "pdfplumber"),
        ("arxiv", "arxiv"),
        ("markitdown", "markitdown"),
    ]
    
    optional_ok = [check_module(name, imp) for name, imp in optional]
    
    # 总结
    print("\n" + "="*40)
    if required_ok:
        print("✅ 必需依赖已满足，可以基本使用")
    else:
        print("❌ 缺少必需依赖，请安装:")
        print("   pip install pymupdf requests")
    
    optional_count = sum(optional_ok)
    print(f"\n📊 可选依赖: {optional_count}/{len(optional)} 已安装")
    
    if optional_count < len(optional):
        print("\n💡 安装所有可选依赖以获得最佳体验:")
        print("   pip install mineru pdfplumber arxiv markitdown")
    
    return 0 if required_ok else 1


if __name__ == "__main__":
    from typing import Optional
    sys.exit(main())
