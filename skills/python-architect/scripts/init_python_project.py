#!/usr/bin/env python3
"""
Initialize a new Python project with modern tooling (uv, ruff, pytest, mypy)
Usage: python init_python_project.py my-project-name
"""

import argparse
import os
from pathlib import Path

PYPROJECT_TEMPLATE = '''[project]
name = "{project_name}"
version = "0.1.0"
description = "A modern Python project"
readme = "README.md"
requires-python = ">=3.11"
license = {{text = "MIT"}}
authors = [
    {{name = "Your Name", email = "you@example.com"}},
]
keywords = ["python", "modern"]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
]
dependencies = [
    "pydantic>=2.0",
    "structlog",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
    "pytest-xdist>=3.0",
    "ruff>=0.1.0",
    "mypy>=1.0",
    "pre-commit>=3.0",
    "mkdocs>=1.5",
]

[project.scripts]
{project_name} = "{module_name}.cli:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/{module_name}"]

# Ruff configuration
[tool.ruff]
target-version = "py311"
line-length = 88
indent-width = 4

[tool.ruff.lint]
select = [
    "E",    # pycodestyle errors
    "F",    # Pyflakes
    "I",    # isort
    "N",    # pep8-naming
    "W",    # pycodestyle warnings
    "UP",   # pyupgrade
    "B",    # flake8-bugbear
    "C4",   # flake8-comprehensions
    "SIM",  # flake8-simplify
    "ARG",  # flake8-unused-arguments
    "PTH",  # flake8-use-pathlib
]
ignore = ["E501"]  # Line too long (handled by formatter)

[tool.ruff.lint.pydocstyle]
convention = "google"

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
skip-magic-trailing-comma = false
line-ending = "auto"

# pytest configuration
[tool.pytest.ini_options]
minversion = "7.0"
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = """
    -v
    --tb=short
    --strict-markers
    --cov={module_name}
    --cov-report=term-missing
    --cov-report=html
"""
markers = [
    "unit: Unit tests",
    "integration: Integration tests",
    "slow: Slow tests",
]

# mypy configuration
[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
show_error_codes = true
show_column_numbers = true
'''

PRE_COMMIT_CONFIG = '''repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.9
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.7.1
    hooks:
      - id: mypy
        additional_dependencies: [types-all]

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
'''

GITIGNORE = '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
env/
ENV/
.venv

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# ruff
.ruff_cache/

# Project
.env
.env.local
*.log
'''

INIT_PY = '''"""{project_name} - A modern Python project."""

__version__ = "0.1.0"
'''

CLI_PY = '''"""Command-line interface."""

import argparse


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="{project_name} CLI")
    parser.add_argument("--version", action="version", version="%(prog)s 0.1.0")
    args = parser.parse_args()


if __name__ == "__main__":
    main()
'''

TEST_EXAMPLE = '''"""Example test."""

import pytest


class TestExample:
    """Example test class."""

    def test_simple(self):
        """A simple test."""
        assert True

    def test_with_fixture(self, tmp_path):
        """Test using pytest fixture."""
        assert tmp_path.exists()
'''

CONftest_PY = '''"""pytest configuration and fixtures."""

import pytest


# Add your fixtures here
@pytest.fixture
def sample_data():
    """Sample fixture."""
    return {{"key": "value"}}
'''

README_TEMPLATE = '''# {project_name}

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

A modern Python project using uv, ruff, pytest, and mypy.

## Setup

```bash
# Install dependencies
uv sync --all-extras --dev

# Activate virtual environment
source .venv/bin/activate

# Install pre-commit hooks
pre-commit install
```

## Development

```bash
# Run tests
uv run pytest

# Run linting
uv run ruff check .
uv run ruff format .

# Run type checking
uv run mypy src

# Run all checks
uv run ruff check . && uv run mypy src && uv run pytest
```

## Project Structure

```
{project_name}/
├── src/{module_name}/      # Source code
├── tests/                   # Test suite
├── docs/                    # Documentation
├── pyproject.toml          # Project config
└── README.md               # This file
```
'''


def create_project(project_name: str, base_path: Path) -> None:
    """Create a new Python project."""
    project_path = base_path / project_name
    module_name = project_name.replace("-", "_")
    
    # Create directories
    (project_path / "src" / module_name).mkdir(parents=True)
    (project_path / "tests" / "unit").mkdir(parents=True)
    (project_path / "tests" / "integration").mkdir(parents=True)
    (project_path / "docs").mkdir(parents=True)
    (project_path / ".github" / "workflows").mkdir(parents=True)
    
    # Write files
    (project_path / "pyproject.toml").write_text(
        PYPROJECT_TEMPLATE.format(project_name=project_name, module_name=module_name)
    )
    (project_path / ".pre-commit-config.yaml").write_text(PRE_COMMIT_CONFIG)
    (project_path / ".gitignore").write_text(GITIGNORE)
    
    # Source files
    (project_path / "src" / module_name / "__init__.py").write_text(
        INIT_PY.format(project_name=project_name)
    )
    (project_path / "src" / module_name / "cli.py").write_text(
        CLI_PY.format(project_name=project_name)
    )
    
    # Test files
    (project_path / "tests" / "__init__.py").write_text("")
    (project_path / "tests" / "unit" / "__init__.py").write_text("")
    (project_path / "tests" / "unit" / "test_example.py").write_text(TEST_EXAMPLE)
    (project_path / "tests" / "conftest.py").write_text(CONftest_PY)
    (project_path / "tests" / "integration" / "__init__.py").write_text("")
    
    # Documentation
    (project_path / "README.md").write_text(
        README_TEMPLATE.format(project_name=project_name, module_name=module_name)
    )
    (project_path / "LICENSE").write_text("MIT License\\n")
    
    print(f"✅ Created project: {project_path}")
    print(f"   cd {project_name}")
    print(f"   uv sync --all-extras --dev")
    print(f"   pre-commit install")


def main():
    parser = argparse.ArgumentParser(description="Initialize Python project")
    parser.add_argument("name", help="Project name")
    parser.add_argument("--path", default=".", help="Base path")
    args = parser.parse_args()
    
    create_project(args.name, Path(args.path))


if __name__ == "__main__":
    main()
