#!/usr/bin/env python3
"""
Setup MkDocs in an existing project
Usage: python setup_mkdocs.py [--with-api]
"""

import argparse
from pathlib import Path

MKDOCS_MINIMAL = '''site_name: My Project
site_url: https://example.com/docs
repo_url: https://github.com/user/repo

nav:
  - Home: index.md
  - Getting Started:
    - Installation: getting_started/installation.md

theme:
  name: material
  palette:
    - media: "(prefers-color-scheme: light)"
      scheme: default
      primary: black
      accent: black
      toggle:
        icon: material/weather-sunny
        name: Switch to dark mode
    - media: "(prefers-color-scheme: dark)"
      scheme: slate
      primary: black
      accent: white
      toggle:
        icon: material/weather-night
        name: Switch to light mode
  font:
    code: Fira Code
    text: Fira Sans
  features:
    - content.code.copy
    - navigation.tabs
    - search.highlight

markdown_extensions:
  - pymdownx.highlight
  - pymdownx.superfences
  - admonition
  - attr_list

plugins:
  - search
'''

INDEX_TEMPLATE = '''# Welcome

## Overview

Add your project description here.

## Quick Start

```bash
pip install your-package
```

## Documentation

- [Installation](getting_started/installation.md)
'''

INSTALL_TEMPLATE = '''# Installation

## From PyPI

```bash
pip install your-package
```

## From Source

```bash
git clone https://github.com/user/repo.git
cd repo
pip install -e .
```
'''


def setup_mkdocs(with_api: bool = False):
    """Setup MkDocs in current directory."""
    
    if Path("mkdocs.yml").exists():
        print("⚠️  mkdocs.yml already exists")
        return
    
    # Create docs directory
    docs_dir = Path("docs")
    docs_dir.mkdir(exist_ok=True)
    (docs_dir / "getting_started").mkdir(exist_ok=True)
    
    # Write mkdocs.yml
    Path("mkdocs.yml").write_text(MKDOCS_MINIMAL)
    
    # Write initial docs
    (docs_dir / "index.md").write_text(INDEX_TEMPLATE)
    (docs_dir / "getting_started" / "installation.md").write_text(INSTALL_TEMPLATE)
    
    # Create requirements
    req_content = "mkdocs\\nmkdocs-material\\n"
    if with_api:
        req_content += "mkdocstrings[python]\\n"
    
    if not Path("requirements-docs.txt").exists():
        Path("requirements-docs.txt").write_text(req_content)
    
    print("✅ MkDocs setup complete!")
    print("\\n   pip install -r requirements-docs.txt")
    print("   mkdocs serve")
    print("\\n   # Deploy")
    print("   mkdocs gh-deploy")


def main():
    parser = argparse.ArgumentParser(description="Setup MkDocs in existing project")
    parser.add_argument("--with-api", action="store_true", help="Include API documentation")
    args = parser.parse_args()
    
    setup_mkdocs(args.with_api)


if __name__ == "__main__":
    main()
