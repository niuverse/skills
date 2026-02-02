# Code Simplifier

🧹 Transform complex, messy code into clean, elegant solutions.

## Overview

Code Simplifier helps you transform:
- Over-engineered code → Simple, direct solutions
- Deep nesting → Flat, readable structures
- Redundant abstractions → Essential functionality
- Verbose patterns → Idiomatic expressions
- AI "vibe coding" → Production-ready code

## Quick Start

```bash
# Analyze file complexity
python scripts/analyze_complexity.py src/my_module.py

# Simplify a file
python scripts/simplify_file.py src/my_module.py

# Find and remove duplicate code
python scripts/remove_duplicates.py src/
```

## Common Transformations

### 1. Remove Over-Engineering
```python
# Before: Unnecessary class hierarchy
class AbstractProcessor: pass
class ConcreteProcessor(AbstractProcessor): pass
processor = ConcreteProcessor()
result = processor.process(data)

# After: Simple function
result = process(data)
```

### 2. Flatten Nesting
```python
# Before: Deep nesting
def get_user(id):
    if id:
        user = db.get(id)
        if user:
            if user.active:
                return user.email

# After: Early returns
def get_user(id):
    if not id:
        return None
    user = db.get(id)
    if not user or not user.active:
        return None
    return user.email
```

### 3. Use Built-ins
```python
# Before: Verbose loop
result = []
for item in items:
    if item.valid:
        result.append(item.value)

# After: List comprehension
result = [item.value for item in items if item.valid]
```

## Simplification Patterns

| Pattern | When to Use |
|---------|-------------|
| **Early Returns** | Deeply nested conditionals |
| **Guard Clauses** | Pre-condition checks |
| **Extract Functions** | Duplicate logic |
| **Use Dataclasses** | Simple data containers |
| **Built-in Functions** | map, filter, any, all |

## Examples

See [SKILL.md](SKILL.md) for complete before/after examples.

## Scripts

| Script | Description |
|--------|-------------|
| `analyze_complexity.py` | Find complex code sections |
| `simplify_file.py` | Apply simplifications to file |
| `remove_duplicates.py` | Consolidate duplicate code |

## Philosophy

> "Perfection is achieved not when there is nothing more to add, but when there is nothing left to take away."

**Core Principles:**
1. Clarity over cleverness
2. Less code = fewer bugs
3. Direct is better than indirect
4. Standard library > custom

## Acknowledgments

This skill draws inspiration from:
- [Anthropic Code Simplifier Plugin](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/code-simplifier) - For the core philosophy of reducing complexity and removing unnecessary abstraction in AI-generated code
- [Refactoring](https://refactoring.com/) by Martin Fowler - For systematic code improvement patterns and catalog of refactorings
- [Simple Made Easy](https://www.infoq.com/presentations/Simple-Made-Easy/) by Rich Hickey - For the distinction between simple and easy, and why simplicity matters
- [A Philosophy of Software Design](https://web.stanford.edu/~ouster/cgi-bin/book.php) by John Ousterhout - For principles on managing complexity in software systems
