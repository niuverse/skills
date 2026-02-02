---
name: python-architect
description: |
  Expert Python software architect for modern, production-grade Python development.
  Specializes in:
  - Modern Python project structure with uv package management
  - Ruff for linting and formatting (replacing flake8, black, isort)
  - pytest for test-driven development
  - Clean architecture patterns (repository, dependency injection, service layer)
  - Type hints with mypy static analysis
  - CI/CD with GitHub Actions
  - Documentation with MkDocs or Sphinx
  
  Use when: creating new Python projects, refactoring legacy code, setting up 
  development workflows, or ensuring code quality and maintainability.
  
  Triggers: python project, uv, ruff, pytest, clean architecture, tdd, modern python
---

# Python Architect

Expert-level Python software architecture with modern tooling and best practices.

## 🎯 Philosophy

- **Simplicity over complexity**: Simple solutions are easier to maintain
- **Tests as documentation**: Well-written tests explain intent
- **Type safety**: Use type hints to catch bugs early
- **Automation**: Automate checks, formatting, and releases

## 🛠️ Tech Stack

| Tool | Purpose | Replacement For |
|------|---------|-----------------|
| **uv** | Package management & virtual envs | pip, poetry, pipenv |
| **ruff** | Linting & formatting | flake8, black, isort, pydocstyle |
| **pytest** | Testing | unittest |
| **mypy** | Type checking | - |
| **pre-commit** | Git hooks | - |
| **GitHub Actions** | CI/CD | - |

## 📁 Project Structure

```
my-project/
├── src/
│   └── my_project/           # Source code
│       ├── __init__.py
│       ├── core/             # Domain logic
│       ├── services/         # Business logic
│       ├── repositories/     # Data access
│       └── api/              # Web interface
├── tests/
│   ├── unit/                 # Unit tests
│   ├── integration/          # Integration tests
│   └── conftest.py          # pytest fixtures
├── docs/                     # Documentation
├── scripts/                  # Utility scripts
├── .github/
│   └── workflows/           # CI/CD
├── pyproject.toml           # Project config (uv, ruff, pytest, mypy)
├── README.md
├── LICENSE
└── .pre-commit-config.yaml
```

## 🚀 Quick Start

```bash
# Create new project
python scripts/init_python_project.py my-project

# Setup existing project
python scripts/setup_modern_python.py

# Run all checks
python scripts/check_project.py
```

## 📋 Best Practices

### 1. Project Initialization with uv

```bash
# Create project
uv init my-project
cd my-project

# Add dependencies
uv add requests pydantic
uv add --dev pytest ruff mypy

# Sync environment
uv sync
```

### 2. pyproject.toml Configuration

```toml
[project]
name = "my-project"
version = "0.1.0"
description = "A modern Python project"
requires-python = ">=3.11"
dependencies = [
    "pydantic>=2.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-cov",
    "ruff>=0.1.0",
    "mypy>=1.0",
    "pre-commit",
]

[tool.ruff]
target-version = "py311"
line-length = 88
select = [
    "E",   # pycodestyle errors
    "F",   # Pyflakes
    "I",   # isort
    "N",   # pep8-naming
    "W",   # pycodestyle warnings
    "UP",  # pyupgrade
    "B",   # flake8-bugbear
    "C4",  # flake8-comprehensions
    "SIM", # flake8-simplify
]
ignore = ["E501"]  # Line too long (handled by formatter)

[tool.ruff.format]
quote-style = "double"
indent-style = "space"

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "-v --tb=short --strict-markers"
markers = [
    "unit: Unit tests",
    "integration: Integration tests",
    "slow: Slow tests",
]

[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
strict = true
```

### 3. Clean Architecture Pattern

```python
# src/my_project/core/domain.py
from dataclasses import dataclass
from typing import Protocol

@dataclass(frozen=True)
class User:
    id: int
    email: str
    name: str


# src/my_project/repositories/user_repo.py
class UserRepository(Protocol):
    def get_by_id(self, user_id: int) -> User | None: ...
    def save(self, user: User) -> None: ...


class InMemoryUserRepository:
    def __init__(self) -> None:
        self._users: dict[int, User] = {}
    
    def get_by_id(self, user_id: int) -> User | None:
        return self._users.get(user_id)
    
    def save(self, user: User) -> None:
        self._users[user.id] = user


# src/my_project/services/user_service.py
class UserService:
    def __init__(self, repo: UserRepository) -> None:
        self._repo = repo
    
    def get_user(self, user_id: int) -> User:
        user = self._repo.get_by_id(user_id)
        if user is None:
            raise UserNotFoundError(user_id)
        return user
```

### 4. Test-Driven Development

```python
# tests/unit/test_user_service.py
import pytest
from my_project.core.domain import User
from my_project.repositories.user_repo import InMemoryUserRepository
from my_project.services.user_service import UserService, UserNotFoundError


@pytest.fixture
def user_repo():
    return InMemoryUserRepository()


@pytest.fixture
def user_service(user_repo):
    return UserService(user_repo)


class TestUserService:
    def test_get_user_returns_user(self, user_service, user_repo):
        # Arrange
        user = User(id=1, email="test@example.com", name="Test")
        user_repo.save(user)
        
        # Act
        result = user_service.get_user(1)
        
        # Assert
        assert result == user
    
    def test_get_user_not_found_raises(self, user_service):
        with pytest.raises(UserNotFoundError):
            user_service.get_user(999)
```

### 5. Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
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
        additional_dependencies: [types-requests]
```

### 6. GitHub Actions CI

```yaml
# .github/workflows/ci.yml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Install uv
        uses: astral-sh/setup-uv@v1
      
      - name: Set up Python
        run: uv python install 3.11
      
      - name: Install dependencies
        run: uv sync --all-extras --dev
      
      - name: Run ruff
        run: uv run ruff check .
      
      - name: Run mypy
        run: uv run mypy src
      
      - name: Run tests
        run: uv run pytest --cov=src --cov-report=xml
```

## 🔧 Scripts

| Script | Purpose |
|--------|---------|
| `scripts/init_python_project.py` | Initialize new Python project |
| `scripts/setup_modern_python.py` | Setup existing project |
| `scripts/check_project.py` | Run all checks |
| `scripts/add_feature.py` | Add new feature with tests |

## 📚 References

- [Modern Python Development](references/modern-python.md)
- [Clean Architecture](references/clean-architecture.md)
- [Testing Patterns](references/testing-patterns.md)
- [uv Documentation](https://docs.astral.sh/uv/)
- [Ruff Rules](https://docs.astral.sh/ruff/rules/)

## 🙏 Acknowledgments

This skill draws inspiration from:
- [Hypermodern Python](https://cjolowicz.github.io/posts/hypermodern-python-01-setup/) by Claudio Jolowicz - For the foundation of modern Python tooling
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html) by Robert C. Martin - For architectural patterns
- [Astral](https://astral.sh/) - For uv and ruff, the modern Python toolchain
- [pytest](https://docs.pytest.org/) - For excellent testing patterns

---

*Built with modern Python best practices. Code should be simple, tested, and maintainable.*
