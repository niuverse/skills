---
name: mkdocs-creator
description: |
  Expert documentation site creator using MkDocs and Material theme.
  Specializes in:
  - Setting up professional documentation sites with MkDocs
  - Material theme customization with black/white color scheme
  - API documentation generation with mkdocstrings
  - Mermaid diagrams and code highlighting
  - Multi-language and versioning support
  - GitHub Pages / GitLab Pages deployment
  
  Use when: creating project documentation, API docs, tutorials,
  or migrating existing docs to MkDocs.
  
  Triggers: mkdocs, documentation, docs site, material theme, api docs,
  documentation generator, create docs
---

# MkDocs Creator

📚 Professional documentation site creation with MkDocs Material.

## Overview

This skill helps you create beautiful, modern documentation sites using:
- **MkDocs**: Fast, simple static site generator
- **Material for MkDocs**: Professional theme with advanced features
- **mkdocstrings**: Automatic API documentation from docstrings
- **Mermaid**: Diagrams and visualizations
- **Black/White color scheme**: Clean, professional aesthetic

## Quick Start

### Create New Documentation Site

```bash
# Initialize project
python scripts/init_mkdocs.py my-project-docs

# Setup existing project
python scripts/setup_mkdocs.py

# Build and serve
mkdocs serve
mkdocs build
```

## Features

### Material Theme Configuration
- **Color scheme**: Black/white professional palette
- **Auto dark/light mode**: Respects system preferences
- **Typography**: Fira Code (code) + Fira Sans (text)
- **Navigation**: Tabs, sections, expandable menus
- **Search**: Full-text search with highlighting

### Code Documentation
- **Syntax highlighting**: Line numbers, annotations
- **Copy button**: One-click code copying
- **Inline highlighting**: `code` within text
- **Superfences**: Advanced code blocks

### Diagrams & Visualizations
- **Mermaid**: Flowcharts, sequence diagrams, Gantt charts
- **Admonitions**: Callout boxes (info, warning, tip, danger)
- **Task lists**: Checkboxes in markdown
- **Emoji support**: Modern emoji rendering

### API Documentation (Python)
- **mkdocstrings**: Auto-generate from docstrings
- **Google style**: Support for Google docstring format
- **Type annotations**: Show type hints
- **Cross-references**: Link between API items

## Directory Structure

```
my-project-docs/
├── docs/
│   ├── index.md              # Home page
│   ├── getting_started/
│   │   ├── installation.md
│   │   └── quickstart.md
│   ├── user_guide/
│   │   └── usage.md
│   ├── api/                  # Auto-generated API docs
│   ├── stylesheets/
│   │   └── extra.css         # Custom styling
│   ├── javascripts/
│   │   └── extra.js          # Custom scripts
│   └── image/                # Logo and images
├── src/                      # Python source (for API docs)
├── mkdocs.yml                # Main configuration
├── requirements-docs.txt     # Documentation dependencies
└── README.md
```

## Standard Navigation Structure

```yaml
nav:
  - Home: index.md
  - Getting Started:
    - Installation: getting_started/installation.md
    - Quick Start: getting_started/quickstart.md
  - User Guide:
    - Basic Usage: user_guide/usage.md
    - Advanced Features: user_guide/advanced.md
  - API Reference:
    - Core API: api/core.md
    - Utilities: api/utils.md
  - Development:
    - Contributing: development/contributing.md
  - Troubleshooting: troubleshooting.md
```

## Color Scheme (Black/White)

```yaml
palette:
  # Auto mode (follows system)
  - media: "(prefers-color-scheme)"
    toggle:
      icon: material/brightness-auto
      name: Switch to light mode
  # Light mode
  - media: "(prefers-color-scheme: light)"
    scheme: default
    primary: black
    accent: black
    toggle:
      icon: material/weather-sunny
      name: Switch to dark mode
  # Dark mode
  - media: "(prefers-color-scheme: dark)"
    scheme: slate
    primary: black
    accent: white
    toggle:
      icon: material/weather-night
      name: Switch to system preference
```

## Dependencies

```txt
# requirements-docs.txt
mkdocs
mkdocs-material
mkdocstrings[python]
pymdown-extensions
mkdocs-minify-plugin
```

## Deployment

### GitHub Pages
```bash
mkdocs gh-deploy
```

### GitLab Pages
```yaml
# .gitlab-ci.yml
pages:
  script:
    - pip install mkdocs mkdocs-material
    - mkdocs build --site-dir public
  artifacts:
    paths:
      - public
```

### Local Preview
```bash
mkdocs serve          # Development server
mkdocs serve --livereload  # Auto-reload on changes
```

## Advanced Configuration

### Mermaid Diagrams
```yaml
markdown_extensions:
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid
          class: mermaid
```

### Python API Documentation
```yaml
plugins:
  - mkdocstrings:
      handlers:
        python:
          options:
            docstring_style: google
            show_source: true
```

### Custom Styling
```css
/* docs/stylesheets/extra.css */
:root {
  --md-primary-fg-color: #000000;
  --md-accent-fg-color: #000000;
}
```

## Best Practices

1. **Start simple**: Begin with basic markdown, add features gradually
2. **Structure logically**: Use clear navigation hierarchy
3. **Document APIs**: Use mkdocstrings for Python projects
4. **Version control**: Keep docs with code, use Git for history
5. **Deploy early**: Set up CI/CD for automatic updates

## References

| File | Content |
|------|---------|
| [mkdocs-config.md](references/mkdocs-config.md) | Complete configuration reference |
| [material-theme.md](references/material-theme.md) | Theme customization guide |
| [mkdocstrings-guide.md](references/mkdocstrings-guide.md) | API documentation setup |

## Resources

- **MkDocs**: https://www.mkdocs.org/
- **Material Theme**: https://squidfunk.github.io/mkdocs-material/
- **mkdocstrings**: https://mkdocstrings.github.io/
- **PyMdown Extensions**: https://facelessuser.github.io/pymdown-extensions/

## Acknowledgments

This skill draws inspiration from:
- [MkDocs Material](https://squidfunk.github.io/mkdocs-material/) by Martin Donath - For the excellent Material theme and comprehensive documentation
- [mkdocstrings](https://mkdocstrings.github.io/) by Timothée Mazzucotelli - For automatic API documentation generation
- [PyMdown Extensions](https://facelessuser.github.io/pymdown-extensions/) by Isaac Muse - For advanced Markdown extensions
