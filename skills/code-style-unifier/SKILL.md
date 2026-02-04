---
name: code-style-unifier
description: |
  Universal code style formatter and unifier. Transforms codebases to conform to
  Google Style Guide (or other specified standards) across multiple languages.
  
  Capabilities:
  - Format code to Google Style Guide compliance
  - Support multiple languages: Python, C/C++, Java, JavaScript/TypeScript, Go
  - Batch format entire projects with configuration
  - Generate .editorconfig, .clang-format, pyproject.toml configs
  - CI/CD integration for automated style enforcement
  - Smart formatting that preserves semantics
  
  Use when: standardizing code style across teams, adopting Google Style Guide,
  onboarding new projects to organization standards, or preparing for open source release.
  
  Triggers: format code, Google Style, standardize code, unify style, apply style guide,
  code formatting, style enforcement, clang-format, yapf, prettier
---

# Code Style Unifier

🎨 Unify code style across your entire codebase with Google Style Guide compliance.

## 🎯 Philosophy

> "Consistency is the hallmark of professional code."

Code style unification transforms heterogeneous code into a consistent, readable,
and maintainable form. Following established standards like Google Style Guide
ensures your code is immediately familiar to other developers.

**Core principles:**
1. **Standardize on proven patterns**: Google Style Guide is battle-tested
2. **Automate enforcement**: Style should be applied automatically, not manually
3. **Preserve semantics**: Formatting changes should never alter behavior
4. **Enable collaboration**: Consistent style removes friction in code reviews

## 📋 Supported Languages & Standards

| Language | Standard | Tool | Config File |
|----------|----------|------|-------------|
| **Python** | Google Python Style | yapf / black + isort | `.style.yapf`, `pyproject.toml` |
| **C/C++** | Google C++ Style | clang-format | `.clang-format` |
| **Java** | Google Java Style | google-java-format | (built-in) |
| **JavaScript/TypeScript** | Google JS Style | prettier + eslint | `.prettierrc`, `.eslintrc` |
| **Go** | gofmt (official) | gofmt | (built-in) |
| **JSON/YAML** | Standard | prettier | `.prettierrc` |
| **Markdown** | Google Markdown | prettier | `.prettierrc` |

## 🚀 Quick Start

### 1. Format Single File
```bash
python scripts/format_file.py path/to/file.py --style google
```

### 2. Format Entire Project
```bash
python scripts/format_project.py --path ./src --languages python,cpp --apply
```

### 3. Generate Config Files
```bash
python scripts/generate_config.py --languages python,cpp,java --output ./
```

### 4. Check Without Applying
```bash
python scripts/format_project.py --path ./src --check
```

## ⚙️ Configuration

### Google Style Presets

#### Python (Google Style)
```toml
# pyproject.toml
[tool.yapf]
based_on_style = "google"
column_limit = 80
dedent_closing_brackets = true
coalesce_brackets = true

[tool.isort]
profile = "google"
line_length = 80
multi_line_output = 3
```

#### C/C++ (Google Style)
```yaml
# .clang-format
BasedOnStyle: Google
IndentWidth: 2
ColumnLimit: 80
AllowShortFunctionsOnASingleLine: Empty
BreakBeforeBraces: Attach
```

#### JavaScript/TypeScript (Google Style)
```json
// .prettierrc
{
  "singleQuote": true,
  "trailingComma": "es5",
  "printWidth": 80,
  "tabWidth": 2,
  "useTabs": false
}
```

### Custom Overrides

Create `.style-unifier.toml` for project-specific overrides:
```toml
[global]
target_style = "google"
exclude_dirs = ["vendor", "third_party", "build"]
exclude_patterns = ["*_generated.py", "*.pb.cc"]

[python]
line_length = 100  # Override default 80
use_black = false  # Use yapf instead

[cpp]
indent_width = 4   # Team prefers 4 spaces
```

## 🔄 Workflow Integration

### Pre-commit Hook
```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: style-unifier
        name: Style Unifier
        entry: python scripts/format_project.py --check
        language: system
        files: \\.(py|cpp|c|h|js|ts|java)$
```

### GitHub Actions
```yaml
# .github/workflows/style.yml
name: Code Style

on: [push, pull_request]

jobs:
  style:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Check style
        run: |
          pip install style-unifier
          python -m style_unifier.check --path . --fail-on-change
```

### VS Code Extension (Conceptual)
```json
// .vscode/settings.json
{
  "editor.formatOnSave": true,
  "python.formatting.provider": "yapf",
  "python.formatting.yapfArgs": ["--style", "{based_on_style: google}"],
  "C_Cpp.clang_format_style": "{BasedOnStyle: Google}"
}
```

## 📊 Before/After Examples

### Python Example

❌ **Before** (Inconsistent):
```python
class dataProcessor:
    def __init__(self,raw_data):
        self.raw_data=raw_data
        self.MAX_SIZE=1000
    
    def processItems(self,items):
        result=[]
        for item in items:
            if item.isValid():
                processed=self._transform(item)
                result.append(processed)
        return result
    
    def _transform(self,item):
        return item.data.upper()
```

✅ **After** (Google Style):
```python
"""Data processing module."""

from typing import List


class DataProcessor:
    """Processes raw data into standardized format."""
    
    def __init__(self, raw_data: dict) -> None:
        self.raw_data = raw_data
        self.max_size = 1000
    
    def process_items(self, items: List[dict]) -> List[str]:
        """Process items and return transformed results."""
        return [
            self._transform(item)
            for item in items
            if item.is_valid()
        ]
    
    def _transform(self, item: dict) -> str:
        """Transform a single item."""
        return item['data'].upper()
```

**Changes applied:**
- Class name: `dataProcessor` → `DataProcessor` (PascalCase)
- Method names: `processItems` → `process_items` (snake_case)
- Constants: `MAX_SIZE` → `max_size` (Google prefers non-constant naming)
- Spacing: Added proper spacing around operators
- Type hints: Added type annotations
- Docstrings: Added module, class, and function docstrings
- Comprehensions: Replaced loop with list comprehension
- Line length: Wrapped to 80 characters

### C++ Example

❌ **Before** (Inconsistent):
```cpp
class DataProcessor {
    public:
        DataProcessor(const std::vector<std::string>& data) 
            : data_(data) {}
        
        std::vector<std::string> process() {
            std::vector<std::string> result;
            for (const auto& item : data_) {
                if (item.length() > 0) {
                    result.push_back(transform(item));
                }
            }
            return result;
        }
    private:
        std::vector<std::string> data_;
        std::string transform(const std::string& s) {
            std::string result = s;
            std::transform(result.begin(), result.end(), 
                          result.begin(), ::toupper);
            return result;
        }
};
```

✅ **After** (Google Style):
```cpp
#ifndef DATA_PROCESSOR_H_
#define DATA_PROCESSOR_H_

#include <algorithm>
#include <cctype>
#include <string>
#include <vector>

namespace myproject {

class DataProcessor {
 public:
  explicit DataProcessor(const std::vector<std::string>& data)
      : data_(data) {}
  
  std::vector<std::string> Process() {
    std::vector<std::string> result;
    for (const auto& item : data_) {
      if (!item.empty()) {
        result.push_back(Transform(item));
      }
    }
    return result;
  }

 private:
  std::vector<std::string> data_;
  
  std::string Transform(const std::string& str) {
    std::string result = str;
    std::transform(result.begin(), result.end(), result.begin(),
                   [](unsigned char c) { return std::toupper(c); });
    return result;
  }
};

}  // namespace myproject

#endif  // DATA_PROCESSOR_H_
```

**Changes applied:**
- Indentation: 2 spaces (Google standard)
- Access specifiers: No extra indentation
- Function names: `process` → `Process` (PascalCase for functions)
- Constructor: Added `explicit`
- Line length: Max 80 characters
- Header guard: Added proper include guard
- Lambda: Modernized with explicit unsigned char cast
- Namespace: Wrapped in namespace

## 🔧 Scripts Reference

| Script | Purpose |
|--------|---------|
| `scripts/format_file.py` | Format a single file |
| `scripts/format_project.py` | Batch format entire project |
| `scripts/generate_config.py` | Generate style config files |
| `scripts/check_style.py` | Check compliance without formatting |
| `scripts/migrate_style.py` | Migrate from one style to another |
| `scripts/install_hooks.py` | Install git hooks for automatic formatting |

## 📚 Google Style Guide Quick Reference

### Python
- **Indentation**: 4 spaces
- **Line length**: 80 characters
- **Naming**: snake_case for functions/variables, PascalCase for classes
- **Type hints**: Required for function signatures
- **Docstrings**: Google format (Args:, Returns:, Raises:)

### C++
- **Indentation**: 2 spaces
- **Line length**: 80 characters
- **Naming**: PascalCase for types/functions, snake_case for variables
- **Headers**: Use #ifndef/#define/#endif guards
- **Namespaces**: Wrap in namespaces

### Java
- **Indentation**: 2 spaces
- **Line length**: 100 characters
- **Naming**: PascalCase for types, camelCase for methods/variables
- **Imports**: No wildcard imports, grouped by package

### JavaScript
- **Indentation**: 2 spaces
- **Line length**: 80 characters
- **Quotes**: Single quotes
- **Semicolons**: Required
- **ES6**: Prefer const/let over var

## 📚 References

- [Google Style Guides](references/google-style-guides.md) - Complete Google style documentation
- [Language-Specific Rules](references/language-rules.md) - Detailed rules per language
- [Migration Guide](references/migration.md) - Migrating existing codebases
- [CI/CD Integration](references/ci-integration.md) - Setting up automated style checks

## 🙏 Acknowledgments

This skill draws inspiration from:
- [Google Style Guides](https://google.github.io/styleguide/) - The gold standard for code style
- [yapf](https://github.com/google/yapf) - Google's Python formatter
- [google-java-format](https://github.com/google/google-java-format) - Google's Java formatter
- [clang-format](https://clang.llvm.org/docs/ClangFormat.html) - LLVM's universal formatter
- [Prettier](https://prettier.io/) - Opinionated code formatter
- [EditorConfig](https://editorconfig.org/) - Cross-editor style consistency

---

*Good code is consistently styled code.*
