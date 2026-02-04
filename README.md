# Niuverse Skills

[![Validate Skills](https://github.com/niuverse/skills/actions/workflows/validate.yml/badge.svg)](https://github.com/niuverse/skills/actions)
[![Update Catalog](https://github.com/niuverse/skills/actions/workflows/update-catalog.yml/badge.svg)](https://github.com/niuverse/skills/actions)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A curated collection of AI agent skills for robot simulation, development, and automation tasks.

## 🎯 Overview

Niuverse Skills is a modular skill library designed for AI agents (Claude, OpenClaw, etc.). Each skill provides domain-specific expertise, tools, and workflows for common robotics and development tasks.

## 📚 Skills Catalog

| Skill | Description | Category |
|-------|-------------|----------|
| [`code-simplifier`](./skills/code-simplifier/) | Simplify complex code. Remove over-engineering and duplication. | 🧹 Code Quality |
| [`code-style-imitator`](./skills/code-style-imitator/) | Extract and learn coding patterns from existing codebases. | 🎨 Code Style |
| [`code-style-unifier`](./skills/code-style-unifier/) | Format code to Google Style. Multi-language support. | 🎨 Code Style |
| [`robot-sim-expert`](./skills/robot-sim-expert/) | Robot simulation for Isaac Lab/Sim, MuJoCo, mjlab, Newton. | 🤖 Robotics |
| [`python-architect`](./skills/python-architect/) | Modern Python projects with uv, ruff, pytest, clean architecture. | 🐍 Python |
| [`mkdocs-creator`](./skills/mkdocs-creator/) | Create documentation sites with MkDocs and Material theme. | 🛠️ Tools |

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/niuverse/skills.git

# Use with Claude Code or OpenClaw
# Skills are auto-loaded when present in the workspace
```

### Using a Skill

Skills are automatically detected and loaded by compatible AI agents:

```
"Use the robot-sim-expert skill to create a MuJoCo quadruped model"
```

## 📁 Repository Structure

```
skills/
├── .github/
│   └── workflows/
│       └── validate.yml      # CI validation workflow
├── scripts/
│   └── validate_skills.py    # Skill validation script
├── skills/                    # Skill directory
│   └── robot-sim-expert/     # Individual skill
│       ├── SKILL.md          # Skill definition (required)
│       ├── README.md         # User documentation
│       ├── references/       # Reference docs
│       └── scripts/          # Executable scripts
├── LICENSE                    # License
└── README.md                  # This file
```

## 🛠️ Creating a New Skill

### Skill Structure

```
skills/your-skill-name/
├── SKILL.md              # Required: Skill definition with YAML frontmatter
├── README.md             # Optional: User-facing documentation
├── references/           # Optional: Documentation references
│   └── guide.md
├── scripts/              # Optional: Executable scripts
│   └── helper.py
└── assets/               # Optional: Static assets
    └── template.txt
```

### SKILL.md Template

```yaml
---
name: your-skill-name
description: |
  A clear description of what this skill does.
  
  Include triggers and use cases.
  
  Triggers: keywords that activate this skill
---

# Skill Title

Instructions and guidance...
```

## 📝 Contributing

1. Fork the repository
2. Create your skill in `skills/your-skill-name/`
3. Ensure `SKILL.md` has proper YAML frontmatter
4. Run validation: `python scripts/validate_skills.py`
5. Submit a pull request

## 🔗 Resources

- [Anthropic Skills Documentation](https://docs.anthropic.com/en/docs/skills)
- [OpenClaw Documentation](https://docs.openclaw.ai)

## 📄 License

[MIT License](LICENSE) - Copyright © 2026 Niuverse

## 🙏 Acknowledgments

- Inspired by [Anthropic Skills](https://github.com/anthropics/skills)
