#!/usr/bin/env python3
"""
Analyze code complexity and suggest simplifications
Usage: python analyze_complexity.py src/my_module.py
"""

import ast
import sys
from pathlib import Path


class ComplexityAnalyzer(ast.NodeVisitor):
    """Analyze code complexity."""
    
    def __init__(self):
        self.max_depth = 0
        self.current_depth = 0
        self.function_count = 0
        self.class_count = 0
        self.nested_function_count = 0
        self.complex_functions = []
    
    def visit_FunctionDef(self, node):
        self.current_depth += 1
        self.max_depth = max(self.max_depth, self.current_depth)
        
        if self.current_depth > 1:
            self.nested_function_count += 1
        
        # Calculate cyclomatic complexity (simplified)
        complexity = 1
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                complexity += 1
        
        if complexity > 10:
            self.complex_functions.append((node.name, complexity))
        
        self.function_count += 1
        self.generic_visit(node)
        self.current_depth -= 1
    
    def visit_ClassDef(self, node):
        self.class_count += 1
        self.generic_visit(node)


def analyze_file(filepath: str):
    """Analyze a Python file."""
    code = Path(filepath).read_text()
    tree = ast.parse(code)
    
    analyzer = ComplexityAnalyzer()
    analyzer.visit(tree)
    
    print(f"\n📊 Complexity Analysis: {filepath}")
    print(f"   Classes: {analyzer.class_count}")
    print(f"   Functions: {analyzer.function_count}")
    print(f"   Max nesting depth: {analyzer.max_depth}")
    print(f"   Nested functions: {analyzer.nested_function_count}")
    
    if analyzer.complex_functions:
        print(f"\n⚠️  Complex functions (cyclomatic complexity > 10):")
        for name, complexity in analyzer.complex_functions:
            print(f"   - {name}: {complexity}")
    else:
        print(f"\n✅ No overly complex functions found")
    
    # Suggestions
    suggestions = []
    if analyzer.max_depth > 3:
        suggestions.append("Consider flattening nested structures with early returns")
    if analyzer.nested_function_count > 0:
        suggestions.append("Consider moving nested functions to module level")
    if analyzer.class_count == 0 and analyzer.function_count > 10:
        suggestions.append("Consider organizing functions into classes or modules")
    
    if suggestions:
        print(f"\n💡 Suggestions:")
        for s in suggestions:
            print(f"   - {s}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python analyze_complexity.py <file.py>")
        sys.exit(1)
    
    analyze_file(sys.argv[1])


if __name__ == "__main__":
    main()
