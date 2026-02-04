# Code Style Imitator

🔍 Analyze and extract coding patterns from existing codebases.

## Overview

Code Style Imitator learns the unique "personality" of your codebase—naming conventions, formatting preferences, and structural patterns—and helps you maintain consistency across new code.

## Features

- **Pattern Extraction**: Detect naming conventions (snake_case, camelCase, PascalCase)
- **Format Analysis**: Identify indentation, line length, spacing preferences
- **Statistical Reports**: Get quantitative style metrics with confidence scores
- **Multi-Language**: Python, JavaScript, TypeScript, C/C++, Java, Go

## Quick Start

### Analyze a Single File

```bash
python scripts/analyze_style.py path/to/file.py
```

Output:
```json
{
  "language": "python",
  "naming": {
    "variables": {"snake_case": 0.85, "camelCase": 0.10},
    "functions": {"snake_case": 0.95}
  },
  "formatting": {
    "indentation_type": "spaces",
    "indentation_size": 4,
    "line_length_mean": 78
  }
}
```

### Analyze Entire Project

```bash
python scripts/analyze_project.py --path ./src --output style-report.json
```

### Generate Style Guide

```bash
python scripts/generate_guide.py --input style-report.json --output STYLE_GUIDE.md
```

## Use Cases

- **Onboarding**: New team members learning existing code style
- **Code Reviews**: Verify new code matches project conventions
- **Documentation**: Generate team style guides automatically
- **Consistency**: Ensure new modules match existing patterns

## Scripts

| Script | Purpose |
|--------|---------|
| `analyze_style.py` | Analyze a single source file |
| `analyze_project.py` | Analyze entire project codebase |
| `generate_guide.py` | Generate markdown style guide |
| `check_style.py` | Compare code against extracted style |
| `compare_styles.py` | Compare styles between projects |

## References

- [Style Analysis Deep Dive](references/style-analysis.md) - Technical implementation details

## License

MIT License - See [LICENSE](../LICENSE) for details.
