# Code Style Unifier

🎨 Format code to Google Style Guide compliance across multiple languages.

## Overview

Code Style Unifier transforms heterogeneous code into consistent, professional form following Google's battle-tested style guides. Supports Python, C/C++, Java, JavaScript/TypeScript, and Go.

## Features

- **Multi-Language**: One tool for all your code
- **Google Style**: Proven, readable conventions
- **Safe Defaults**: Check mode by default, `--apply` to modify
- **CI/CD Ready**: Easy integration into workflows

## Quick Start

### Format Single File

```bash
# Check what would change
python scripts/format_file.py path/to/file.py --style google

# Actually format
python scripts/format_file.py path/to/file.py --style google
```

### Format Entire Project

```bash
# Check mode (safe)
python scripts/format_project.py --path ./src --languages python,cpp

# Apply changes
python scripts/format_project.py --path ./src --languages python,cpp --apply
```

### Generate Config Files

```bash
python scripts/generate_config.py --languages python,cpp,java --output ./
```

Generates:
- `.editorconfig` - Editor configuration
- `pyproject.toml` - Python tooling config
- `.clang-format` - C/C++ formatter config
- `.prettierrc` - JavaScript/TypeScript config

## Supported Languages

| Language | Tool | Config |
|----------|------|--------|
| Python | yapf, isort | `pyproject.toml`, `.style.yapf` |
| C/C++ | clang-format | `.clang-format` |
| Java | google-java-format | built-in |
| JavaScript/TypeScript | prettier | `.prettierrc` |
| Go | gofmt | built-in |

## Use Cases

- **Team Standardization**: Unify code style across developers
- **Open Source Prep**: Prepare projects for public release
- **Legacy Modernization**: Update old codebases to modern standards
- **CI Enforcement**: Automated style checks in pipelines

## CI Integration

### GitHub Actions

```yaml
name: Code Style
on: [push, pull_request]
jobs:
  style:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Check style
        run: |
          python scripts/format_project.py --path . --check
```

### Pre-commit Hook

```yaml
repos:
  - repo: local
    hooks:
      - id: style-unifier
        entry: python scripts/format_project.py --check
        language: system
        files: \.(py|cpp|c|h|js|ts|java)$
```

## Scripts

| Script | Purpose |
|--------|---------|
| `format_file.py` | Format a single file |
| `format_project.py` | Batch format entire project |
| `generate_config.py` | Generate style config files |
| `check_style.py` | Check compliance without formatting |

## References

- [Google Style Guides](references/google-style-guides.md) - Complete style documentation

## License

MIT License - See [LICENSE](../LICENSE) for details.
