#!/usr/bin/env python3
"""
Analyze code style patterns from a single file.

Usage:
    python analyze_style.py path/to/file.py
    python analyze_style.py path/to/file.py --output style.json
"""

import argparse
import ast
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class NamingPatterns:
    """Naming convention patterns."""
    variables: dict[str, float] = field(default_factory=dict)
    functions: dict[str, float] = field(default_factory=dict)
    classes: dict[str, float] = field(default_factory=dict)
    constants: dict[str, float] = field(default_factory=dict)
    private_vars: dict[str, float] = field(default_factory=dict)


@dataclass
class FormattingPatterns:
    """Code formatting patterns."""
    indentation_type: str = "unknown"  # spaces, tabs, mixed
    indentation_size: int = 0
    line_length_mean: int = 0
    line_length_max: int = 0
    quote_style: str = "unknown"  # single, double, mixed
    trailing_newline: bool = True


@dataclass
class StyleReport:
    """Complete style analysis report."""
    file_path: str = ""
    language: str = ""
    naming: NamingPatterns = field(default_factory=NamingPatterns)
    formatting: FormattingPatterns = field(default_factory=FormattingPatterns)
    patterns: dict[str, Any] = field(default_factory=dict)
    examples: dict[str, str] = field(default_factory=dict)


def detect_naming_style(name: str) -> str:
    """Detect the naming style of a given name."""
    if not name:
        return "unknown"
    
    # Check for UPPER_SNAKE_CASE (constants)
    if name.isupper() and '_' in name:
        return "UPPER_SNAKE_CASE"
    
    # Check for snake_case
    if name.islower() and '_' in name:
        return "snake_case"
    
    # Check for PascalCase
    if name[0].isupper() and '_' not in name:
        return "PascalCase"
    
    # Check for camelCase
    if name[0].islower() and '_' not in name and any(c.isupper() for c in name):
        return "camelCase"
    
    # Check for _private (leading underscore)
    if name.startswith('_'):
        return "_private"
    
    return "other"


def analyze_naming_python(content: str) -> NamingPatterns:
    """Analyze naming patterns in Python code."""
    try:
        tree = ast.parse(content)
    except SyntaxError:
        return NamingPatterns()
    
    var_styles: list[str] = []
    func_styles: list[str] = []
    class_styles: list[str] = []
    const_styles: list[str] = []
    private_styles: list[str] = []
    
    for node in ast.walk(tree):
        # Function definitions
        if isinstance(node, ast.FunctionDef):
            func_styles.append(detect_naming_style(node.name))
            if node.name.startswith('_'):
                private_styles.append(detect_naming_style(node.name[1:]))
            
            # Function arguments
            for arg in node.args.args:
                var_styles.append(detect_naming_style(arg.arg))
        
        # Class definitions
        elif isinstance(node, ast.ClassDef):
            class_styles.append(detect_naming_style(node.name))
        
        # Variable assignments
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    style = detect_naming_style(target.id)
                    # Constants are usually at module level and UPPER
                    if target.id.isupper():
                        const_styles.append(style)
                    else:
                        var_styles.append(style)
                    
                    if target.id.startswith('_'):
                        private_styles.append(detect_naming_style(target.id[1:]))
    
    def calc_distribution(styles: list[str]) -> dict[str, float]:
        if not styles:
            return {}
        total = len(styles)
        return {style: round(count / total, 2) 
                for style, count in sorted(
                    {s: styles.count(s) for s in set(styles)}.items(),
                    key=lambda x: -x[1]
                )}
    
    return NamingPatterns(
        variables=calc_distribution(var_styles),
        functions=calc_distribution(func_styles),
        classes=calc_distribution(class_styles),
        constants=calc_distribution(const_styles),
        private_vars=calc_distribution(private_styles)
    )


def analyze_formatting(content: str) -> FormattingPatterns:
    """Analyze formatting patterns."""
    lines = content.split('\n')
    
    # Analyze indentation
    indentations: list[int] = []
    spaces_count = 0
    tabs_count = 0
    
    for line in lines:
        if not line.strip():
            continue
        stripped = line.lstrip()
        indent = len(line) - len(stripped)
        if indent > 0:
            indentations.append(indent)
            if line.startswith(' '):
                spaces_count += 1
            elif line.startswith('\t'):
                tabs_count += 1
    
    # Determine indentation type
    if spaces_count > 0 and tabs_count == 0:
        indent_type = "spaces"
    elif tabs_count > 0 and spaces_count == 0:
        indent_type = "tabs"
    elif spaces_count > 0 and tabs_count > 0:
        indent_type = "mixed"
    else:
        indent_type = "unknown"
    
    # Calculate indentation size (GCD of non-zero indentations)
    indent_size = 0
    if indentations:
        import math
        indent_size = math.gcd(*set(indentations)) if len(set(indentations)) > 1 else indentations[0]
    
    # Analyze line lengths
    line_lengths = [len(line) for line in lines if line.strip()]
    
    # Analyze quote style
    single_quotes = len(re.findall(r"'[^']*'", content))
    double_quotes = len(re.findall(r'"[^"]*"', content))
    
    if single_quotes > 0 and double_quotes == 0:
        quote_style = "single"
    elif double_quotes > 0 and single_quotes == 0:
        quote_style = "double"
    elif single_quotes > 0 and double_quotes > 0:
        quote_style = "mixed"
    else:
        quote_style = "unknown"
    
    return FormattingPatterns(
        indentation_type=indent_type,
        indentation_size=indent_size,
        line_length_mean=int(sum(line_lengths) / len(line_lengths)) if line_lengths else 0,
        line_length_max=max(line_lengths) if line_lengths else 0,
        quote_style=quote_style,
        trailing_newline=content.endswith('\n')
    )


def analyze_patterns_python(content: str) -> dict[str, Any]:
    """Analyze structural patterns in Python code."""
    try:
        tree = ast.parse(content)
    except SyntaxError:
        return {}
    
    func_lengths: list[int] = []
    class_count = 0
    function_count = 0
    type_hint_usage = 0
    docstring_usage = 0
    
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            function_count += 1
            func_lengths.append(len(node.body))
            
            # Check type hints
            if node.returns or any(arg.annotation for arg in node.args.args):
                type_hint_usage += 1
            
            # Check docstring
            if (node.body and 
                isinstance(node.body[0], ast.Expr) and 
                isinstance(node.body[0].value, ast.Constant) and
                isinstance(node.body[0].value.value, str)):
                docstring_usage += 1
        
        elif isinstance(node, ast.ClassDef):
            class_count += 1
    
    return {
        "function_count": function_count,
        "class_count": class_count,
        "function_length": {
            "mean": round(sum(func_lengths) / len(func_lengths), 1) if func_lengths else 0,
            "max": max(func_lengths) if func_lengths else 0,
            "min": min(func_lengths) if func_lengths else 0
        },
        "type_hint_usage": {
            "count": type_hint_usage,
            "rate": round(type_hint_usage / function_count, 2) if function_count else 0
        },
        "docstring_usage": {
            "count": docstring_usage,
            "rate": round(docstring_usage / function_count, 2) if function_count else 0
        }
    }


def detect_language(file_path: Path) -> str:
    """Detect programming language from file extension."""
    extensions = {
        '.py': 'python',
        '.js': 'javascript',
        '.ts': 'typescript',
        '.cpp': 'cpp',
        '.cc': 'cpp',
        '.cxx': 'cpp',
        '.c': 'c',
        '.h': 'cpp',
        '.hpp': 'cpp',
        '.java': 'java',
        '.go': 'go',
        '.rs': 'rust',
    }
    return extensions.get(file_path.suffix.lower(), 'unknown')


def analyze_file(file_path: Path) -> StyleReport:
    """Analyze a single file and return style report."""
    content = file_path.read_text(encoding='utf-8')
    language = detect_language(file_path)
    
    report = StyleReport(
        file_path=str(file_path),
        language=language,
        formatting=analyze_formatting(content)
    )
    
    if language == 'python':
        report.naming = analyze_naming_python(content)
        report.patterns = analyze_patterns_python(content)
    
    return report


def main():
    parser = argparse.ArgumentParser(
        description='Analyze code style patterns from a file'
    )
    parser.add_argument('file', help='Path to the file to analyze')
    parser.add_argument('--output', '-o', help='Output JSON file path')
    
    args = parser.parse_args()
    
    file_path = Path(args.file)
    if not file_path.exists():
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        sys.exit(1)
    
    print(f"🔍 Analyzing {file_path}...")
    report = analyze_file(file_path)
    
    # Convert to dict for JSON serialization
    report_dict = {
        "file_path": report.file_path,
        "language": report.language,
        "naming": asdict(report.naming),
        "formatting": asdict(report.formatting),
        "patterns": report.patterns,
        "examples": report.examples
    }
    
    json_output = json.dumps(report_dict, indent=2)
    
    if args.output:
        output_path = Path(args.output)
        output_path.write_text(json_output)
        print(f"✅ Report saved to {output_path}")
    else:
        print(json_output)


if __name__ == '__main__':
    main()
