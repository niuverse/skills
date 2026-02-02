#!/usr/bin/env python3
"""
Initialize a new MkDocs documentation site
Usage: python init_mkdocs.py my-project-docs [--with-api]
"""

import argparse
import os
from pathlib import Path

MKDOCS_TEMPLATE = '''# Herman Ye@Galbot Created on $(date +%Y-%m-%d)

########################### Edit these lines for your project #######################
site_name: {project_name}
site_url: https://your-org.github.io/{project_slug}
repo_name: {project_name}
repo_url: https://github.com/your-org/{project_slug}

########################### Do not modify below this line ###########################
nav:
  - Home: index.md
  - Getting Started:
    - Installation: getting_started/installation.md
    - Quick Start: getting_started/quickstart.md
  - User Guide:
    - Basic Usage: user_guide/usage.md
    - Advanced Features: user_guide/advanced.md
{api_nav}
  - Development:
    - Contributing: development/contributing.md
  - Troubleshooting: troubleshooting.md

theme:
  language: en
  name: material
  icon:
    repo: fontawesome/brands/git-alt
  font:
    code: Fira Code
    text: Fira Sans
  palette:
    # Palette toggle for automatic mode
    - media: "(prefers-color-scheme)"
      toggle:
        icon: material/brightness-auto
        name: Switch to light mode
    # Palette toggle for light mode
    - media: "(prefers-color-scheme: light)"
      scheme: default
      primary: black
      accent: black
      toggle:
        icon: material/weather-sunny
        name: Switch to dark mode
    # Palette toggle for dark mode
    - media: "(prefers-color-scheme: dark)"
      scheme: slate
      primary: black
      accent: white
      toggle:
        icon: material/weather-night
        name: Switch to system preference
  features:
    - content.code.copy
    - content.code.annotate
    - navigation.tabs
    - navigation.sections
    - navigation.expand
    - navigation.top
    - search.highlight
    - search.suggest

markdown_extensions:
  - pymdownx.highlight:
      anchor_linenums: true
      line_spans: __span
      pygments_lang_class: true
  - pymdownx.tasklist:
      custom_checkbox: true
  - pymdownx.inlinehilite
  - pymdownx.snippets
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid
          class: mermaid
  - pymdownx.details
  - admonition
  - attr_list
  - md_in_html
  - def_list
  - toc:
      permalink: true

copyright: Copyright \u0026copy; $(date +%Y) Your Organization. All rights reserved.

extra_css:
  - stylesheets/extra.css

extra_javascript:
  - https://unpkg.com/mermaid@10/dist/mermaid.min.js

plugins:
  - search
{api_plugin}
extra:
  generator: false
'''

INDEX_MD = '''# Welcome to {project_name}

## Overview

{description}

## Features

- ✨ Feature 1
- 🚀 Feature 2
- 📚 Feature 3

## Quick Start

```bash
pip install {project_slug}
```

## Documentation Structure

- **Getting Started**: Installation and basic usage
- **User Guide**: Detailed usage instructions
- **API Reference**: Auto-generated API documentation
- **Development**: Contributing guidelines

## Support

For questions and issues, please visit our [GitHub repository]({repo_url}).
'''

INSTALLATION_MD = '''# Installation

## Requirements

- Python 3.9+
- pip or uv

## Install from PyPI

```bash
pip install {project_slug}
```

## Install from Source

```bash
git clone {repo_url}.git
cd {project_slug}
pip install -e .
```

## Development Installation

```bash
git clone {repo_url}.git
cd {project_slug}
pip install -e ".[dev]"
```

## Verify Installation

```bash
python -c "import {module_name}; print({module_name}.__version__)"
```
'''

QUICKSTART_MD = '''# Quick Start

## Basic Usage

```python
import {module_name}

# Your code here
```

## Next Steps

- Read the [User Guide](usage.md)
- Check [API Reference](../api/core.md)
- See [Examples](../examples.md)
'''

USAGE_MD = '''# Basic Usage

## Getting Started

This guide covers the basic usage of {project_name}.

## Examples

### Example 1: Basic Operation

```python
# Your example code
```

### Example 2: Advanced Features

```python
# Advanced example
```

## Best Practices

1. Practice 1
2. Practice 2
3. Practice 3
'''

ADVANCED_MD = '''# Advanced Features

## Feature 1

Detailed explanation of feature 1.

## Feature 2

Detailed explanation of feature 2.

## Tips and Tricks

!!! tip "Pro Tip"
    This is a helpful tip for advanced users.

!!! warning "Caution"
    Be careful with this operation.
'''

CONTRIBUTING_MD = '''# Contributing

Thank you for your interest in contributing!

## Development Setup

```bash
git clone {repo_url}.git
cd {project_slug}
pip install -e ".[dev]"
```

## Code Style

- Follow PEP 8
- Use type hints
- Write docstrings

## Testing

```bash
pytest
```

## Submitting Changes

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request
'''

TROUBLESHOOTING_MD = '''# Troubleshooting

## Common Issues

### Issue 1: Problem Description

**Solution**: Steps to resolve.

### Issue 2: Another Problem

**Solution**: Steps to resolve.

## Getting Help

- Check the [documentation](https://your-org.github.io/{project_slug})
- Open an issue on [GitHub]({repo_url}/issues)
'''

API_CORE_MD = '''# Core API

::: {module_name}.core

::: {module_name}.utils
'''

EXTRA_CSS = '''/* Custom styles for {project_name} documentation */

:root {
  --md-primary-fg-color: #000000;
  --md-accent-fg-color: #000000;
}

/* Code block styling */
.md-typeset code {
  border-radius: 4px;
}

/* Admonition styling */
.md-typeset .admonition {
  border-radius: 8px;
}
'''

REQUIREMENTS_TXT = '''# Documentation dependencies
mkdocs
mkdocs-material
pymdown-extensions
mkdocs-minify-plugin
'''

API_REQUIREMENTS = '''mkdocstrings[python]
'''

GITIGNORE = '''# MkDocs
site/

# Python
__pycache__/
*.py[cod]
*.egg-info/
.venv/
venv/

# IDE
.vscode/
.idea/

# OS
.DS_Store
'''


def create_docs_site(project_name: str, with_api: bool = False, base_path: Path = Path(".")):
    """Create a new MkDocs documentation site."""
    project_slug = project_name.lower().replace(" ", "-").replace("_", "-")
    module_name = project_slug.replace("-", "_")
    project_path = base_path / project_slug
    docs_path = project_path / "docs"
    
    # Create directories
    (docs_path / "getting_started").mkdir(parents=True)
    (docs_path / "user_guide").mkdir(parents=True)
    (docs_path / "development").mkdir(parents=True)
    (docs_path / "stylesheets").mkdir(parents=True)
    
    if with_api:
        (docs_path / "api").mkdir(parents=True)
        (project_path / "src" / module_name).mkdir(parents=True)
    
    # Prepare API sections if needed
    api_nav = "  - API Reference:\\n    - Core API: api/core.md\\n" if with_api else ""
    api_plugin = '''  - mkdocstrings:
      handlers:
        python:
          options:
            docstring_style: google
            show_source: true
''' if with_api else ""
    
    # Write files
    (project_path / "mkdocs.yml").write_text(
        MKDOCS_TEMPLATE.format(
            project_name=project_name,
            project_slug=project_slug,
            api_nav=api_nav,
            api_plugin=api_plugin
        )
    )
    
    (docs_path / "index.md").write_text(
        INDEX_MD.format(
            project_name=project_name,
            project_slug=project_slug,
            description="A brief description of your project.",
            repo_url=f"https://github.com/your-org/{project_slug}"
        )
    )
    
    (docs_path / "getting_started" / "installation.md").write_text(
        INSTALLATION_MD.format(
            project_slug=project_slug,
            module_name=module_name,
            repo_url=f"https://github.com/your-org/{project_slug}"
        )
    )
    
    (docs_path / "getting_started" / "quickstart.md").write_text(
        QUICKSTART_MD.format(module_name=module_name)
    )
    
    (docs_path / "user_guide" / "usage.md").write_text(
        USAGE_MD.format(project_name=project_name)
    )
    
    (docs_path / "user_guide" / "advanced.md").write_text(ADVANCED_MD)
    
    (docs_path / "development" / "contributing.md").write_text(
        CONTRIBUTING_MD.format(
            project_slug=project_slug,
            repo_url=f"https://github.com/your-org/{project_slug}"
        )
    )
    
    (docs_path / "troubleshooting.md").write_text(
        TROUBLESHOOTING_MD.format(
            project_slug=project_slug,
            repo_url=f"https://github.com/your-org/{project_slug}"
        )
    )
    
    (docs_path / "stylesheets" / "extra.css").write_text(
        EXTRA_CSS.format(project_name=project_name)
    )
    
    # API documentation
    if with_api:
        (docs_path / "api" / "core.md").write_text(
            API_CORE_MD.format(module_name=module_name)
        )
        (docs_path / "stylesheets" / "extra.css").write_text(
            EXTRA_CSS.format(project_name=project_name)
        )
    
    # Requirements
    req_content = REQUIREMENTS_TXT
    if with_api:
        req_content += API_REQUIREMENTS
    (project_path / "requirements-docs.txt").write_text(req_content)
    
    # .gitignore
    (project_path / ".gitignore").write_text(GITIGNORE)
    
    # README
    (project_path / "README.md").write_text(f"# {project_name} Documentation\\n\\nSee [Getting Started](docs/getting_started/installation.md)\\n")
    
    print(f"✅ Created documentation site: {project_path}")
    print(f"\\n   cd {project_slug}")
    print(f"   pip install -r requirements-docs.txt")
    print(f"   mkdocs serve")
    print(f"\\n   # Deploy to GitHub Pages")
    print(f"   mkdocs gh-deploy")


def main():
    parser = argparse.ArgumentParser(description="Initialize MkDocs documentation site")
    parser.add_argument("name", help="Project name")
    parser.add_argument("--with-api", action="store_true", help="Include API documentation setup")
    parser.add_argument("--path", default=".", help="Base path")
    args = parser.parse_args()
    
    create_docs_site(args.name, args.with_api, Path(args.path))


if __name__ == "__main__":
    main()
