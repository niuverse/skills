---
name: code-style-imitator
description: |
  AI-powered code style analyzer and imitator. Extracts coding patterns, conventions,
  and stylistic preferences from existing codebase to generate style guides and 
  transformation rules.
  
  Capabilities:
  - Analyze existing codebase to extract style patterns (naming, formatting, structure)
  - Generate custom style guides based on actual code usage
  - Create transformation rules to apply detected style to new code
  - Compare code snippets against extracted style patterns
  - Produce style reports with statistics and examples
  
  Use when: onboarding to existing codebase, maintaining consistency across projects,
  creating team style guides, or ensuring new code matches existing patterns.
  
  Triggers: analyze code style, extract style patterns, mimic codebase style,
  generate style guide, code style analysis, learn from existing code, style extraction
---

# Code Style Imitator

🔍 Analyze and extract coding patterns from existing codebases to generate custom style guides.

## 🎯 Philosophy

> "Code style is the fingerprint of a development team." 

Every codebase has its own personality—naming conventions, indentation preferences,
abstraction patterns, and idiomatic expressions. This skill captures that personality
and helps you maintain it.

**Core principles:**
1. **Learn from reality**: Extract patterns from actual working code, not theoretical ideals
2. **Quantify style**: Measure and document style with concrete metrics
3. **Enable consistency**: Help new code blend seamlessly with old code
4. **Preserve team identity**: Maintain the unique character of your codebase

## 🔍 What Gets Analyzed

### 1. Naming Conventions
- Variable naming (camelCase, snake_case, PascalCase, etc.)
- Function naming patterns
- Class/struct naming
- Constant naming (UPPER_SNAKE, kCamelCase, etc.)
- File naming conventions

### 2. Code Formatting
- Indentation style and size (spaces vs tabs)
- Line length preferences
- Brace placement (same-line vs new-line)
- Spacing around operators and punctuation
- Blank line usage

### 3. Structural Patterns
- Function length and organization
- Class design patterns
- Import/include ordering
- Comment styles and placement
- Documentation conventions

### 4. Language-Specific Idioms
- Python: Type hint usage, f-string vs .format, list comprehensions
- C++: Smart pointer usage, RAII patterns, template conventions
- JavaScript: ES6+ features, async patterns, module systems
- Java: Stream API usage, Optional patterns, lombok annotations

## 🛠️ Usage

### Analyze Single File
```bash
python scripts/analyze_style.py path/to/file.py
```

### Analyze Entire Project
```bash
python scripts/analyze_project.py --path ./src --output style-report.json
```

### Generate Style Guide
```bash
python scripts/generate_guide.py --input style-report.json --output STYLE_GUIDE.md
```

### Compare Code Against Style
```bash
python scripts/check_style.py --style style-report.json --file new_code.py
```

## 📊 Output Format

### Style Report (JSON)
```json
{
  "project": "my-project",
  "languages": ["python", "cpp"],
  "naming": {
    "variables": {
      "snake_case": 0.85,
      "camelCase": 0.10,
      "other": 0.05
    },
    "functions": {
      "snake_case": 0.95,
      "camelCase": 0.05
    },
    "classes": {
      "PascalCase": 0.98
    }
  },
  "formatting": {
    "indentation": {
      "type": "spaces",
      "size": 4
    },
    "line_length": {
      "mean": 78,
      "max": 120,
      "preferred": 88
    },
    "brace_style": "same_line"
  },
  "patterns": {
    "function_length": {
      "mean_lines": 12,
      "max_lines": 45
    },
    "type_hints": {
      "usage_rate": 0.72,
      "strictness": "partial"
    }
  },
  "examples": {
    "typical_function": "def process_data(data: list[dict]) -> Result:\n    ...",
    "typical_class": "class DataProcessor:\n    def __init__(self, config: Config):\n        ..."
  }
}
```

## 🎯 Analysis Examples

### Example 1: Detecting Naming Patterns

**Input code:**
```python
class DataProcessor:
    def __init__(self, raw_data):
        self.raw_data = raw_data
        self.MAX_RETRIES = 3
    
    def process_items(self):
        for item in self.raw_data:
            self._handle_item(item)
    
    def _handle_item(self, item):
        pass
```

**Detected patterns:**
```yaml
naming:
  classes: PascalCase (DataProcessor)
  methods: snake_case (process_items, _handle_item)
  private_methods: _snake_case with underscore prefix
  instance_vars: snake_case (raw_data)
  constants: UPPER_SNAKE (MAX_RETRIES)
  parameters: snake_case (raw_data, item)
```

### Example 2: Detecting Formatting Patterns

**Input code:**
```python
def calculate_total(items, tax_rate=0.08):
    """Calculate total with tax."""
    subtotal = sum(item.price for item in items)
    tax = subtotal * tax_rate
    return subtotal + tax


class Order:
    def __init__(self, items):
        self.items = items
```

**Detected patterns:**
```yaml
formatting:
  indentation: 4 spaces
  line_ending: no trailing spaces
  blank_lines: 2 between top-level definitions
  docstrings: used for public functions
  spacing: space after commas, no space around = in kwargs
```

### Example 3: Detecting Structural Patterns

**Analysis output:**
```yaml
structure:
  function_length:
    average: 15 lines
    median: 12 lines
    max: 89 lines
    recommendations: "Functions are generally concise"
  
  class_patterns:
    dataclass_usage: 35%
    slots_usage: 12%
    property_usage: 28%
    
  import_style:
    organization: stdlib -> third_party -> local
    sorting: alphabetical within groups
```

## 📋 Analysis Checklist

The analyzer checks for:

- [ ] **Naming consistency**: Are naming conventions applied uniformly?
- [ ] **Formatting patterns**: What's the preferred indentation, spacing, etc.?
- [ ] **Code organization**: How are files and modules structured?
- [ ] **Documentation style**: How is code documented?
- [ ] **Error handling**: What patterns are used for errors?
- [ ] **Type usage**: How are types used (if applicable)?
- [ ] **Language idioms**: Are there preferred language-specific patterns?

## 🔧 Scripts Reference

| Script | Purpose |
|--------|---------|
| `scripts/analyze_style.py` | Analyze style of a single file |
| `scripts/analyze_project.py` | Analyze entire project codebase |
| `scripts/generate_guide.py` | Generate markdown style guide from analysis |
| `scripts/check_style.py` | Check if code matches extracted style |
| `scripts/compare_styles.py` | Compare styles between two codebases |

## 📚 References

- [Style Analysis Deep Dive](references/style-analysis.md) - Technical details of analysis algorithms
- [Supported Languages](references/languages.md) - Language-specific analysis capabilities
- [Style Report Schema](references/report-schema.md) - JSON schema for style reports

## 🙏 Acknowledgments

This skill draws inspiration from:
- [EditorConfig](https://editorconfig.org/) - For defining and maintaining consistent coding styles
- [Prettier](https://prettier.io/) - For opinionated code formatting analysis
- [Black](https://black.readthedocs.io/) - For uncompromising Python code style detection
- [clang-format](https://clang.llvm.org/docs/ClangFormat.html) - For C/C++/Obj-C style analysis
- [ESLint](https://eslint.org/) - For JavaScript/TypeScript pattern detection
- [RuboCop](https://rubocop.org/) - For Ruby style guide enforcement patterns

---

*Style is the visible expression of team culture.*
