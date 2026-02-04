# AGENTS.md - Niuverse Skills

## Project Overview

Niuverse Skills is a curated collection of AI agent skills for robot simulation, development, and automation tasks. Each skill is a modular package providing domain-specific expertise for AI agents (Claude, OpenClaw, Kimi, etc.).

## Repository Structure

```
niuverse-skills/
├── skills/              # Individual skill directories
│   ├── code-simplifier/
│   ├── code-style-imitator/
│   ├── code-style-unifier/
│   ├── robot-sim-expert/
│   ├── python-architect/
│   └── mkdocs-creator/
├── scripts/             # Repository maintenance scripts
│   ├── validate_skills.py
│   └── update_catalog.py
├── .github/workflows/   # CI/CD automation
├── README.md            # Main documentation
├── DESIGN.md            # Design documentation
└── AGENTS.md           # This file
```

## Skill Anatomy

Each skill follows this structure:
```
skills/<skill-name>/
├── SKILL.md             # Required: Skill definition with YAML frontmatter
├── README.md            # Optional: User-facing documentation
├── references/          # Optional: Reference documentation
│   └── *.md
├── scripts/             # Optional: Executable scripts
│   └── *.py
└── assets/              # Optional: Static assets
    └── *
```

## SKILL.md Format

```yaml
---
name: skill-name
description: |
  Clear description of what this skill does.
  Include specific triggers and use cases.
  
  Use when: specific situations
  Triggers: keywords that activate this skill
---

# Skill Title

Instructions and guidance...
```

## Development Guidelines

### Adding a New Skill

1. Use the skill-creator tool:
   ```bash
   python /opt/homebrew/lib/node_modules/openclaw/skills/skill-creator/scripts/init_skill.py <skill-name> --path skills --resources scripts,references
   ```

2. Edit `SKILL.md` with proper frontmatter and instructions

3. Add relevant scripts to `scripts/`

4. Test the skill:
   ```bash
   python scripts/validate_skills.py
   ```

5. Update README.md catalog

6. Commit and push

### Code Style

- Follow Google Style Guide for Python
- Use type hints for all function signatures
- Maximum line length: 80 characters
- Indentation: 4 spaces (Python), 2 spaces (C/C++)

### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Skill name | kebab-case | `code-simplifier` |
| Script files | snake_case | `analyze_style.py` |
| Class names | PascalCase | `StyleAnalyzer` |
| Function names | snake_case | `analyze_file()` |

## Key Commands

```bash
# Validate all skills
python scripts/validate_skills.py

# Update catalog in README
python scripts/update_catalog.py

# Test a specific skill
python skills/<skill-name>/scripts/<script>.py
```

## CI/CD

GitHub Actions workflows:
- `validate.yml` - Validates skill structure on PR
- `update-catalog.yml` - Auto-updates skill catalog

## Related Documentation

- See [DESIGN.md](./DESIGN.md) for design decisions and architecture
- See individual skill READMEs for usage instructions
- See [SKILL.md](./skills/skill-creator/SKILL.md) for skill creation guide

## Contact

- Repository: https://github.com/niuverse/skills
- Maintained by: Niuverse Team
