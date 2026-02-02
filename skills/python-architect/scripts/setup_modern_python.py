#!/usr/bin/env python3
"""
Setup modern Python tooling in an existing project
Usage: python setup_modern_python.py
"""

import subprocess
from pathlib import Path

PYPROJECT_UPDATE = '''

[tool.ruff]
target-version = "py311"
line-length = 88
indent-width = 4

[tool.ruff.lint]
select = [
    "E", "F", "I", "N", "W", "UP", "B", "C4", "SIM", "ARG", "PTH",
]
ignore = ["E501"]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
addopts = "-v --tb=short --strict-markers --cov"

[tool.mypy]
python_version = "3.11"
warn_return_any = true
disallow_untyped_defs = true
strict = true
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
'''


def setup_project():
    """Setup modern tooling."""
    print("🔧 Setting up modern Python tooling...")
    
    # Check for pyproject.toml
    if Path("pyproject.toml").exists():
        print("   Appending config to pyproject.toml...")
        with open("pyproject.toml", "a") as f:
            f.write(PYPROJECT_UPDATE)
    else:
        print("   Creating pyproject.toml...")
        Path("pyproject.toml").write_text('[project]\nname = "my-project"\nversion = "0.1.0"' + PYPROJECT_UPDATE)
    
    # Create .pre-commit-config.yaml
    if not Path(".pre-commit-config.yaml").exists():
        print("   Creating .pre-commit-config.yaml...")
        Path(".pre-commit-config.yaml").write_text(PRE_COMMIT_CONFIG)
    
    # Install dependencies
    print("   Installing dependencies...")
    try:
        subprocess.run(["uv", "add", "--dev", "pytest", "ruff", "mypy", "pre-commit"], check=True)
    except:
        print("   ⚠️  uv not found, please install: curl -LsSf https://astral.sh/uv/install.sh | sh")
    
    print("✅ Setup complete!")
    print("   Run: pre-commit install")


if __name__ == "__main__":
    setup_project()
