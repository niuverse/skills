#!/usr/bin/env python3
"""
Analyze entire project codebase for style patterns.

Usage:
    python analyze_project.py --path ./src
    python analyze_project.py --path ./src --output style-report.json
"""

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any

# Import the analyze_style module
sys.path.insert(0, str(Path(__file__).parent))
from analyze_style import analyze_file, detect_language, NamingPatterns, FormattingPatterns


def collect_files(project_path: Path, extensions: list[str] | None = None) -> list[Path]:
    """Collect all source files from project."""
    if extensions is None:
        extensions = ['.py', '.js', '.ts', '.cpp', '.cc', '.c', '.h', '.hpp', '.java', '.go']
    
    files = []
    for ext in extensions:
        files.extend(project_path.rglob(f'*{ext}'))
    
    # Filter out common exclude directories
    exclude_dirs = {
        'node_modules', 'vendor', 'third_party', 'build', 'dist',
        '__pycache__', '.git', '.venv', 'venv', '.tox', '.pytest_cache'
    }
    
    filtered_files = [
        f for f in files 
        if not any(part in exclude_dirs for part in f.parts)
    ]
    
    return filtered_files


def merge_naming_patterns(patterns: list[NamingPatterns]) -> NamingPatterns:
    """Merge multiple naming pattern reports."""
    merged = NamingPatterns()
    
    def merge_dicts(dicts: list[dict]) -> dict:
        result: dict[str, list] = {}
        for d in dicts:
            for key, value in d.items():
                if key not in result:
                    result[key] = []
                result[key].append(value)
        
        # Calculate weighted average
        final: dict[str, float] = {}
        for key, values in result.items():
            final[key] = round(sum(values) / len(values), 2)
        return final
    
    all_vars = [p.variables for p in patterns if p.variables]
    all_funcs = [p.functions for p in patterns if p.functions]
    all_classes = [p.classes for p in patterns if p.classes]
    all_consts = [p.constants for p in patterns if p.constants]
    all_privates = [p.private_vars for p in patterns if p.private_vars]
    
    if all_vars:
        merged.variables = merge_dicts(all_vars)
    if all_funcs:
        merged.functions = merge_dicts(all_funcs)
    if all_classes:
        merged.classes = merge_dicts(all_classes)
    if all_consts:
        merged.constants = merge_dicts(all_consts)
    if all_privates:
        merged.private_vars = merge_dicts(all_privates)
    
    return merged


def merge_formatting_patterns(patterns: list[FormattingPatterns]) -> FormattingPatterns:
    """Merge multiple formatting pattern reports."""
    if not patterns:
        return FormattingPatterns()
    
    # Determine most common indentation
    indent_types: dict[str, int] = {}
    indent_sizes: dict[int, int] = {}
    quote_styles: dict[str, int] = {}
    
    line_lengths_mean: list[int] = []
    line_lengths_max: list[int] = []
    
    for p in patterns:
        indent_types[p.indentation_type] = indent_types.get(p.indentation_type, 0) + 1
        if p.indentation_size > 0:
            indent_sizes[p.indentation_size] = indent_sizes.get(p.indentation_size, 0) + 1
        quote_styles[p.quote_style] = quote_styles.get(p.quote_style, 0) + 1
        line_lengths_mean.append(p.line_length_mean)
        line_lengths_max.append(p.line_length_max)
    
    return FormattingPatterns(
        indentation_type=max(indent_types, key=indent_types.get) if indent_types else "unknown",
        indentation_size=max(indent_sizes, key=indent_sizes.get) if indent_sizes else 0,
        line_length_mean=int(sum(line_lengths_mean) / len(line_lengths_mean)) if line_lengths_mean else 0,
        line_length_max=max(line_lengths_max) if line_lengths_max else 0,
        quote_style=max(quote_styles, key=quote_styles.get) if quote_styles else "unknown",
        trailing_newline=all(p.trailing_newline for p in patterns)
    )


def analyze_project(project_path: Path, extensions: list[str] | None = None) -> dict[str, Any]:
    """Analyze entire project and aggregate results."""
    files = collect_files(project_path, extensions)
    
    if not files:
        print("No source files found.", file=sys.stderr)
        return {}
    
    print(f"Found {len(files)} source files")
    
    # Analyze each file
    reports_by_lang: dict[str, list] = {
        'python': [],
        'javascript': [],
        'typescript': [],
        'cpp': [],
        'c': [],
        'java': [],
        'go': []
    }
    
    for i, file_path in enumerate(files, 1):
        if i % 10 == 0 or i == len(files):
            print(f"  Analyzed {i}/{len(files)} files...", end='\r')
        
        try:
            report = analyze_file(file_path)
            if report.language in reports_by_lang:
                reports_by_lang[report.language].append(report)
        except Exception as e:
            print(f"Warning: Could not analyze {file_path}: {e}", file=sys.stderr)
    
    print()  # New line after progress
    
    # Aggregate results
    aggregated: dict[str, Any] = {
        "project": str(project_path.name),
        "total_files": len(files),
        "languages": {}
    }
    
    for lang, reports in reports_by_lang.items():
        if not reports:
            continue
        
        aggregated["languages"][lang] = {
            "file_count": len(reports),
            "naming": asdict(merge_naming_patterns([r.naming for r in reports])),
            "formatting": asdict(merge_formatting_patterns([r.formatting for r in reports]))
        }
    
    return aggregated


def main():
    parser = argparse.ArgumentParser(
        description='Analyze project codebase for style patterns'
    )
    parser.add_argument('--path', '-p', required=True, 
                       help='Path to project directory')
    parser.add_argument('--output', '-o', 
                       help='Output JSON file path')
    parser.add_argument('--extensions', '-e',
                       help='Comma-separated list of extensions (default: .py,.js,.ts,.cpp,.c,.h,.java,.go)')
    
    args = parser.parse_args()
    
    project_path = Path(args.path)
    if not project_path.exists():
        print(f"Error: Path not found: {project_path}", file=sys.stderr)
        sys.exit(1)
    
    extensions = None
    if args.extensions:
        extensions = [f'.{ext.lstrip(".")}' for ext in args.extensions.split(',')]
    
    print(f"🔍 Analyzing project: {project_path}")
    report = analyze_project(project_path, extensions)
    
    if not report:
        sys.exit(1)
    
    json_output = json.dumps(report, indent=2)
    
    if args.output:
        output_path = Path(args.output)
        output_path.write_text(json_output)
        print(f"✅ Report saved to {output_path}")
    else:
        print("\n" + "="*50)
        print("STYLE ANALYSIS REPORT")
        print("="*50)
        print(json_output)


if __name__ == '__main__':
    main()
