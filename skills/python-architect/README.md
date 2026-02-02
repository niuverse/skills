# Python Architect

🐍 Expert-level Python software architecture with modern tooling.

## Overview

Python Architect is a skill for creating production-grade Python projects using modern best practices:

- **uv** for fast, reliable package management
- **ruff** for all-in-one linting and formatting
- **pytest** for test-driven development
- **Clean Architecture** patterns for maintainable code
- **Type hints** with mypy for static analysis

## Quick Start

```bash
# Initialize new project
python scripts/init_python_project.py my-awesome-project

# Setup existing project with modern tooling
python scripts/setup_modern_python.py

# Run all quality checks
python scripts/check_project.py
```

## Why This Stack?

| Traditional | Modern | Benefit |
|-------------|--------|---------|
| pip + venv | **uv** | 10-100x faster, unified tool |
| black + flake8 + isort | **ruff** | Single tool, 10-100x faster |
| unittest | **pytest** | Better ergonomics, fixtures |
| No types | **mypy** | Catch bugs early |
| Manual checks | **pre-commit** | Automated quality gates |

## Project Structure

```
my-project/
├── src/my_project/          # Source code
├── tests/                   # Test suite
├── docs/                    # Documentation
├── pyproject.toml          # Single config file
└── .pre-commit-config.yaml # Git hooks
```

## Key Features

### 1. Single pyproject.toml
All configuration in one place:
- Project metadata
- Dependencies
- ruff rules
- pytest settings
- mypy configuration

### 2. Clean Architecture
```
src/my_project/
├── core/           # Domain models (pure Python)
├── repositories/   # Data access abstraction
├── services/       # Business logic
└── api/           # Web interface (FastAPI/Flask)
```

### 3. Test-First Development
- Write tests before implementation
- Use fixtures for test setup
- Mock external dependencies
- Aim for high coverage

## Example

```python
# src/my_project/core/user.py
from dataclasses import dataclass

@dataclass(frozen=True)
class User:
    id: int
    email: str

# src/my_project/services/user_service.py
class UserService:
    def __init__(self, repo: UserRepository) -> None:
        self._repo = repo
    
    def get_user(self, user_id: int) -> User:
        user = self._repo.get_by_id(user_id)
        if user is None:
            raise UserNotFoundError(user_id)
        return user

# tests/test_user_service.py
def test_get_user_not_found(user_service):
    with pytest.raises(UserNotFoundError):
        user_service.get_user(999)
```

## Scripts

| Script | Description |
|--------|-------------|
| `init_python_project.py` | Create new project with all tooling |
| `setup_modern_python.py` | Add modern tooling to existing project |
| `check_project.py` | Run ruff, mypy, and tests |
| `add_feature.py` | Scaffold new feature with tests |

## References

- [SKILL.md](SKILL.md) - Complete documentation
- [Modern Python Guide](references/modern-python.md)
- [Clean Architecture](references/clean-architecture.md)
- [Testing Patterns](references/testing-patterns.md)

## Resources

- [uv documentation](https://docs.astral.sh/uv/)
- [ruff documentation](https://docs.astral.sh/ruff/)
- [pytest documentation](https://docs.pytest.org/)

## Acknowledgments

This skill draws inspiration from:
- [Hypermodern Python](https://cjolowicz.github.io/posts/hypermodern-python-01-setup/) by Claudio Jolowicz - For the foundation of modern Python tooling patterns
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html) by Robert C. Martin - For architectural principles
- [Astral](https://astral.sh/) - For uv and ruff, the modern Python toolchain that replaces multiple legacy tools
