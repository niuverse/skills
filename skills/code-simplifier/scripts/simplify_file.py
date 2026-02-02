#!/usr/bin/env python3
"""
Simplify a Python file by applying common simplification patterns
Usage: python simplify_file.py src/my_module.py
"""

import re
import sys
from pathlib import Path


def simplify_list_comprehension(content: str) -> str:
    """Convert simple loops to list comprehensions."""
    # Pattern: for item in items: if condition: result.append(item)
    pattern = r'result = \[\]\nfor (\w+) in (\w+):\n    if ([^:]+):\n        result\.append\(([^)]+)\)'
    replacement = r'result = [\4 for \1 in \2 if \3]'
    return re.sub(pattern, replacement, content)


def simplify_dict_get(content: str) -> str:
    """Simplify dict.get() patterns."""
    # Pattern: if key in dict: value = dict[key] else: value = default
    pattern = r'if (\w+) in (\w+):\n    (\w+) = \2\[\1\]\nelse:\n    \3 = ([^\n]+)'
    replacement = r'\3 = \2.get(\1, \4)'
    return re.sub(pattern, replacement, content)


def remove_unnecessary_else(content: str) -> str:
    """Remove else after return/raise."""
    # Pattern: if x: return y else: ...
    pattern = r'(if .+:.*?\n    return [^\n]+)\nelse:([^\n]*\n)'
    replacement = r'\1\2'
    return re.sub(pattern, replacement, content, flags=re.DOTALL)


def simplify_boolean_return(content: str) -> str:
    """Simplify: if condition: return True else: return False."""
    pattern = r'if ([^:]+):\n    return True\n(?:else:\n)?    return False'
    replacement = r'return bool(\1)'
    return re.sub(pattern, replacement, content)


def simplify_file(filepath: str):
    """Apply simplifications to a file."""
    path = Path(filepath)
    content = path.read_text()
    original = content
    
    # Apply simplifications
    content = simplify_list_comprehension(content)
    content = simplify_dict_get(content)
    content = simplify_boolean_return(content)
    
    if content != original:
        # Backup original
        path.with_suffix('.py.bak').write_text(original)
        path.write_text(content)
        print(f"✅ Simplified {filepath}")
        print(f"   Backup saved to {filepath}.bak")
    else:
        print(f"ℹ️  No simplifications applied to {filepath}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python simplify_file.py <file.py>")
        sys.exit(1)
    
    simplify_file(sys.argv[1])


if __name__ == "__main__":
    main()
