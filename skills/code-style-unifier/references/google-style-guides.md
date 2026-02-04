# Google Style Guide Reference

Complete reference for Google Style Guide rules and configurations.

## Python Style Guide

### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Module | `snake_case` | `my_module.py` |
| Package | `snake_case` | `my_package` |
| Class | `PascalCase` | `MyClass` |
| Exception | `PascalCase` + Error | `MyError` |
| Function | `snake_case` | `my_function()` |
| Global/Class Constant | `UPPER_SNAKE_CASE` | `MAX_COUNT` |
| Global/Class Variable | `snake_case` | `my_variable` |
| Instance Variable | `snake_case` | `my_variable` |
| Method | `snake_case` | `my_method()` |
| Local Variable | `snake_case` | `local_var` |
| Protected Instance Variable | `_snake_case` | `_protected_var` |
| Private Instance Variable | `__snake_case` | `__private_var` |
| Function Parameter | `snake_case` | `param_name` |

### Formatting Rules

```yaml
Indentation: 4 spaces
Line Length: 80 characters (max 100 with justification)
Blank Lines: 
  - 2 between top-level definitions
  - 1 between method definitions
Imports:
  - One per line
  - Grouped: stdlib > third-party > local
  - Sorted alphabetically within groups
Strings: Prefer single quotes for consistency
```

### Type Annotations

Required for all function signatures:

```python
def func(a: int) -> list[str]:
    ...

def func_no_return() -> None:
    ...

# For complex types
from typing import Optional, Union

def func_optional(a: Optional[int] = None) -> Union[str, int]:
    ...
```

### Docstring Format (Google Style)

```python
def fetch_data(url: str, timeout: int = 30) -> dict:
    """Fetch data from a URL.
    
    Args:
        url: The URL to fetch data from.
        timeout: Request timeout in seconds. Defaults to 30.
    
    Returns:
        A dictionary containing the response data.
    
    Raises:
        ConnectionError: If the connection fails.
        TimeoutError: If the request times out.
    """
    ...
```

## C++ Style Guide

### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Type Names | `PascalCase` | `MyClass`, `MyStruct` |
| Variable Names | `snake_case` | `my_variable` |
| Class Member Variables | `snake_case_` (trailing underscore) | `member_var_` |
| Struct Data Members | `snake_case` (no underscore) | `data_member` |
| Function Names | `PascalCase` | `MyFunction()` |
| Enum Names | `PascalCase` | `MyEnum` |
| Enum Values | `kPascalCase` (k prefix) | `kValueName` |
| Macros | `UPPER_SNAKE_CASE` | `MY_MACRO` |
| Constants | `kPascalCase` | `kMaxSize` |

### Formatting Rules

```yaml
Indentation: 2 spaces
Line Length: 80 characters
Access Modifiers: No extra indentation
Braces: Same line (Stroustrup style)
Pointer/Reference: Align with type (int* ptr, not int *ptr)
Namespaces: No extra indentation
```

### Example

```cpp
#ifndef MY_CLASS_H_
#define MY_CLASS_H_

#include <vector>
#include <string>

namespace myproject {

class DataProcessor {
 public:
  explicit DataProcessor(const std::vector<std::string>& data);
  
  // Delete copy constructor and assignment
  DataProcessor(const DataProcessor&) = delete;
  DataProcessor& operator=(const DataProcessor&) = delete;
  
  std::vector<std::string> Process();
  
  static constexpr int kMaxSize = 1000;

 private:
  std::vector<std::string> data_;
  int processed_count_ = 0;
};

}  // namespace myproject

#endif  // MY_CLASS_H_
```

## Java Style Guide

### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Package | `lowercase` (no underscores) | `com.example.myproject` |
| Class/Interface | `PascalCase` | `MyClass`, `MyInterface` |
| Method | `camelCase` | `myMethod()` |
| Variable | `camelCase` | `myVariable` |
| Constant | `UPPER_SNAKE_CASE` | `MAX_COUNT` |
| Type Parameter | `T`, `E`, `K`, `V` | `T item`, `K key` |

### Formatting Rules

```yaml
Indentation: 2 spaces
Line Length: 100 characters
Braces: Same line for classes/methods, may break for long lines
Imports: No wildcards, grouped by package
```

### Example

```java
package com.example.myproject;

import java.util.List;
import java.util.ArrayList;

public class DataProcessor {
  private static final int MAX_SIZE = 1000;
  
  private final List<String> data;
  
  public DataProcessor(List<String> data) {
    this.data = new ArrayList<>(data);
  }
  
  public List<String> process() {
    return data.stream()
        .filter(s -> !s.isEmpty())
        .map(String::toUpperCase)
        .toList();
  }
}
```

## JavaScript Style Guide

### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| File | `lowercase` or `camelCase` | `myfile.js` or `myFile.js` |
| Class | `PascalCase` | `MyClass` |
| Interface | `PascalCase` | `MyInterface` |
| Enum | `PascalCase` | `MyEnum` |
| Function | `camelCase` | `myFunction()` |
| Variable | `camelCase` | `myVariable` |
| Constant | `UPPER_SNAKE_CASE` | `MAX_COUNT` |
| Private Member | `trailingUnderscore_` | `privateVar_` |

### Formatting Rules

```yaml
Indentation: 2 spaces
Line Length: 80 characters
Quotes: Single quotes
Semicolons: Always required
Trailing Commas: Required for multiline
```

### Example

```javascript
/**
 * Processes data items.
 */
class DataProcessor {
  /**
   * @param {Array<string>} data - The data to process.
   */
  constructor(data) {
    /** @private @const */
    this.data_ = data;
  }
  
  /**
   * Processes all items.
   * @return {Array<string>}
   */
  process() {
    return this.data_
        .filter(item => item.length > 0)
        .map(item => item.toUpperCase());
  }
}

exports = {DataProcessor};
```

## Go Style Guide

Go uses `gofmt` for formatting - it's built into the language toolchain.

### Key Points

- **No debates**: `gofmt` is the standard
- **Tabs for indentation**: Displayed as 8 spaces by default
- **Line length**: No strict limit, but be reasonable

### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Package | `lowercase` (short, no underscores) | `parser`, `httputil` |
| Exported | `PascalCase` | `MyFunction` |
| Unexported | `camelCase` | `myFunction` |
| Interface | `-er` suffix | `Reader`, `Writer` |
| Acronyms | All caps | `URL`, `HTTP`, `ID` |

### Example

```go
package parser

import (
    "fmt"
    "strings"
)

// DataProcessor processes raw data.
type DataProcessor struct {
    Data []string
}

// Process transforms all data items.
func (dp *DataProcessor) Process() []string {
    result := make([]string, 0, len(dp.Data))
    for _, item := range dp.Data {
        if item != "" {
            result = append(result, strings.ToUpper(item))
        }
    }
    return result
}

// MaxSize is the maximum allowed size.
const MaxSize = 1000
```

## Tool Configurations

### yapf (Python)

```toml
# .style.yapf or pyproject.toml
[style]
based_on_style = google
column_limit = 80
dedent_closing_brackets = true
coalesce_brackets = true
split_before_logical_operator = true
```

### clang-format (C/C++)

```yaml
# .clang-format
BasedOnStyle: Google
IndentWidth: 2
ColumnLimit: 80
AllowShortFunctionsOnASingleLine: Empty
BreakBeforeBraces: Attach
PointerAlignment: Left
SortIncludes: true
```

### Prettier (JavaScript/TypeScript)

```json
// .prettierrc
{
  "singleQuote": true,
  "trailingComma": "es5",
  "printWidth": 80,
  "tabWidth": 2,
  "useTabs": false,
  "semi": true,
  "bracketSpacing": true
}
```

### isort (Python Imports)

```toml
# pyproject.toml
[tool.isort]
profile = "google"
line_length = 80
multi_line_output = 3
include_trailing_comma = true
force_grid_wrap = 0
use_parentheses = true
ensure_newline_before_comments = true
```

## Common Issues

### Python

**Issue**: yapf splits lines too aggressively
**Solution**: Add `# yapf: disable` comment for complex expressions

**Issue**: Long strings exceed line length
**Solution**: Use implicit string concatenation:
```python
long_string = (
    "This is a very long string that "
    "spans multiple lines using implicit "
    "concatenation"
)
```

### C++

**Issue**: Template formatting looks weird
**Solution**: Use trailing commas to force one-per-line:
```cpp
std::map<
    std::string,
    std::vector<std::unique_ptr<MyClass>>,
> my_map;  // Note trailing comma
```

### Java

**Issue**: Streams with many operations
**Solution**: Each operation on new line:
```java
list.stream()
    .filter(Objects::nonNull)
    .map(String::trim)
    .filter(s -> !s.isEmpty())
    .collect(Collectors.toList());
```

## References

- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [Google C++ Style Guide](https://google.github.io/styleguide/cppguide.html)
- [Google Java Style Guide](https://google.github.io/styleguide/javaguide.html)
- [Google JavaScript Style Guide](https://google.github.io/styleguide/jsguide.html)
- [Effective Go](https://golang.org/doc/effective_go.html) (Go's equivalent)
