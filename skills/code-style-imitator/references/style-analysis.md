# Style Analysis Deep Dive

This document provides technical details about the style analysis algorithms used by the Code Style Imitator.

## Naming Convention Detection

### Algorithm Overview

The naming convention detection uses pattern matching to classify identifiers into categories:

1. **Tokenize** the identifier
2. **Analyze case patterns**
3. **Check for separators** (underscores)
4. **Classify** into known patterns

### Naming Pattern Categories

| Pattern | Example | Detection Rule |
|---------|---------|----------------|
| `UPPER_SNAKE_CASE` | `MAX_SIZE` | All uppercase with underscores |
| `snake_case` | `process_data` | All lowercase with underscores |
| `PascalCase` | `DataProcessor` | Starts uppercase, no separators |
| `camelCase` | `processData` | Starts lowercase, contains uppercase |
| `_private` | `_internal_var` | Leading underscore |
| `__dunder__` | `__init__` | Double leading/trailing underscores |

### Detection Heuristics

```python
def detect_naming_style(name: str) -> str:
    if not name:
        return "unknown"
    
    # Priority order matters
    if name.startswith('__') and name.endswith('__'):
        return "dunder"
    if name.startswith('_'):
        return "_private"
    if name.isupper() and '_' in name:
        return "UPPER_SNAKE_CASE"
    if name.islower() and '_' in name:
        return "snake_case"
    if name[0].isupper() and '_' not in name:
        return "PascalCase"
    if name[0].islower() and '_' not in name:
        if any(c.isupper() for c in name):
            return "camelCase"
    
    return "other"
```

## Indentation Analysis

### Detecting Indentation Type

The algorithm counts leading whitespace characters:

```python
def analyze_indentation(lines: list[str]) -> dict:
    spaces_count = 0
    tabs_count = 0
    
    for line in lines:
        if line.startswith(' '):
            spaces_count += 1
        elif line.startswith('\t'):
            tabs_count += 1
    
    if spaces_count > 0 and tabs_count == 0:
        return {"type": "spaces", "confidence": 1.0}
    elif tabs_count > 0 and spaces_count == 0:
        return {"type": "tabs", "confidence": 1.0}
    elif spaces_count > 0 and tabs_count > 0:
        return {"type": "mixed", "confidence": spaces_count / (spaces_count + tabs_count)}
    else:
        return {"type": "unknown", "confidence": 0.0}
```

### Calculating Indentation Size

Uses the Greatest Common Divisor (GCD) of indentation levels:

```python
import math

def calculate_indent_size(indentations: list[int]) -> int:
    """Calculate indentation size from observed levels."""
    if not indentations:
        return 0
    
    unique_indents = sorted(set(indentations))
    
    if len(unique_indents) == 1:
        return unique_indents[0]
    
    # Calculate GCD of differences
    diffs = [unique_indents[i+1] - unique_indents[i] 
             for i in range(len(unique_indents)-1)]
    
    return math.gcd(*diffs)
```

## Language-Specific Analysis

### Python Analysis

Using Python's `ast` module for accurate parsing:

```python
import ast

def analyze_python_file(content: str) -> dict:
    tree = ast.parse(content)
    
    analysis = {
        "functions": [],
        "classes": [],
        "imports": [],
        "type_hints": 0,
        "docstrings": 0
    }
    
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            analysis["functions"].append({
                "name": node.name,
                "lineno": node.lineno,
                "has_type_hints": bool(node.returns or 
                    any(arg.annotation for arg in node.args.args)),
                "has_docstring": has_docstring(node)
            })
        elif isinstance(node, ast.ClassDef):
            analysis["classes"].append({
                "name": node.name,
                "lineno": node.lineno,
                "bases": [base.id for base in node.bases 
                         if isinstance(base, ast.Name)]
            })
    
    return analysis
```

### C++ Analysis

Using regex-based analysis (lightweight, no full parser):

```python
import re

def analyze_cpp_file(content: str) -> dict:
    patterns = {
        "functions": re.compile(r'\b(\w+)\s*\([^)]*\)\s*\{'),
        "classes": re.compile(r'\bclass\s+(\w+)'),
        "includes": re.compile(r'#include\s+["<]([^">]+)[">]'),
        "namespaces": re.compile(r'\bnamespace\s+(\w+)'),
    }
    
    return {
        key: pattern.findall(content)
        for key, pattern in patterns.items()
    }
```

## Statistical Aggregation

### Merging Multiple Reports

When analyzing a project, individual file reports are merged:

```python
def merge_reports(reports: list[StyleReport]) -> StyleReport:
    """Merge multiple style reports into a single aggregate."""
    
    # For distributions, calculate weighted average
    merged = StyleReport()
    
    all_naming = [r.naming for r in reports]
    merged.naming = merge_naming_patterns(all_naming)
    
    all_formatting = [r.formatting for r in reports]
    merged.formatting = merge_formatting_patterns(all_formatting)
    
    return merged

def merge_naming_patterns(patterns: list[NamingPatterns]) -> NamingPatterns:
    """Merge naming patterns by weighted frequency."""
    
    def merge_style_dict(style_dicts: list[dict]) -> dict:
        totals = {}
        counts = {}
        
        for d in style_dicts:
            for style, freq in d.items():
                totals[style] = totals.get(style, 0) + freq
                counts[style] = counts.get(style, 0) + 1
        
        return {
            style: round(totals[style] / counts[style], 2)
            for style in totals
        }
    
    return NamingPatterns(
        variables=merge_style_dict([p.variables for p in patterns]),
        functions=merge_style_dict([p.functions for p in patterns]),
        classes=merge_style_dict([p.classes for p in patterns]),
    )
```

## Confidence Scoring

Each detected pattern includes a confidence score:

```python
def calculate_confidence(observations: int, consistency: float) -> float:
    """Calculate confidence based on sample size and consistency.
    
    Args:
        observations: Number of times pattern was observed
        consistency: How consistently pattern was applied (0.0 - 1.0)
    
    Returns:
        Confidence score (0.0 - 1.0)
    """
    # More observations = higher confidence
    sample_confidence = min(1.0, observations / 10)
    
    # Weight by consistency
    return round(sample_confidence * consistency, 2)
```

## Edge Cases

### Ambiguous Patterns

Some patterns may be ambiguous:

| Pattern | Could Be | Resolution |
|---------|----------|------------|
| `XMLHttpRequest` | PascalCase | First letter uppercase |
| `innerHTML` | camelCase | First letter lowercase |
| `MAX` | UPPER_SNAKE or Pascal | Context analysis |

### Mixed Styles

When a codebase uses multiple styles:

1. **Dominant style**: Most frequently used (>70%)
2. **Secondary style**: Occasionally used (20-70%)
3. **Outliers**: Rare deviations (<20%)

The report highlights these as potential inconsistencies.

## Performance Considerations

### Large Codebases

For projects with 1000+ files:

1. **Sampling**: Analyze representative subset
2. **Parallel processing**: Use multiprocessing
3. **Caching**: Cache parsed ASTs
4. **Incremental**: Only analyze changed files

### Memory Optimization

```python
# Stream large files instead of loading entirely
def analyze_large_file(file_path: Path, chunk_size: int = 1000):
    with open(file_path, 'r', encoding='utf-8') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            # Process chunk
```

## Future Enhancements

1. **Machine Learning**: Train models on style patterns
2. **Semantic Analysis**: Understand intent behind patterns
3. **Historical Analysis**: Track style evolution over time
4. **Cross-language**: Unified style across polyglot projects
