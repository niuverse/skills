# MkDocs Creator

📚 Professional documentation site creation with MkDocs Material.

## Overview

Create beautiful, modern documentation sites with:
- **MkDocs**: Fast static site generator
- **Material Theme**: Professional black/white design
- **API Documentation**: Auto-generated from Python docstrings
- **Mermaid Diagrams**: Visual documentation

## Quick Start

```bash
# Initialize new docs site
python scripts/init_mkdocs.py my-project-docs

# Or setup existing project
python scripts/setup_mkdocs.py

# Build and preview
mkdocs serve
mkdocs build
mkdocs gh-deploy  # Deploy to GitHub Pages
```

## Features

### Black/White Color Scheme
```yaml
palette:
  - media: "(prefers-color-scheme: light)"
    scheme: default
    primary: black
    accent: black
  - media: "(prefers-color-scheme: dark)"
    scheme: slate
    primary: black
    accent: white
```

### Standard Structure
```
docs/
├── index.md
├── getting_started/
├── user_guide/
├── api/
└── stylesheets/
```

### Included Extensions
- **Code highlighting**: Line numbers, copy button
- **Mermaid diagrams**: Flowcharts, sequence diagrams
- **Admonitions**: Info, warning, tip boxes
- **Task lists**: Checkbox support
- **Emoji**: Modern emoji rendering

## Scripts

| Script | Purpose |
|--------|---------|
| `init_mkdocs.py` | Create new documentation site |
| `setup_mkdocs.py` | Setup mkdocs in existing project |

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
    paths: [public]
```

## References

- [SKILL.md](SKILL.md) - Complete documentation
- [mkdocs-config.md](references/mkdocs-config.md) - Configuration reference
- [material-theme.md](references/material-theme.md) - Theme customization
- [mkdocstrings-guide.md](references/mkdocstrings-guide.md) - API docs guide

## Resources

- [MkDocs](https://www.mkdocs.org/)
- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)

## Acknowledgments

- [MkDocs Material](https://squidfunk.github.io/mkdocs-material/) by Martin Donath
- [mkdocstrings](https://mkdocstrings.github.io/) by Timothée Mazzucotelli
- [PyMdown Extensions](https://facelessuser.github.io/pymdown-extensions/) by Isaac Muse

## License

MIT License - See [LICENSE](../LICENSE)
