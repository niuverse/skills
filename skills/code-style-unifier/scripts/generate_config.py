#!/usr/bin/env python3
"""
Generate configuration files for various formatters.

Usage:
    python generate_config.py --languages python,cpp,java --output ./
    python generate_config.py --all --output ./
"""

import argparse
from pathlib import Path


CONFIG_TEMPLATES = {
    "python": {
        "pyproject.toml": '''[build-system]
requires = ["setuptools>=45", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "my-project"
version = "0.1.0"
description = "My project description"
requires-python = ">=3.9"
dependencies = []

[project.optional-dependencies]
dev = [
    "yapf>=0.40",
    "isort>=5.12",
    "mypy>=1.0",
]

# Google Style Python formatting
[tool.yapf]
based_on_style = "google"
column_limit = 80
dedent_closing_brackets = true
coalesce_brackets = true
split_before_logical_operator = true
split_before_named_assigns = true

[tool.isort]
profile = "google"
line_length = 80
multi_line_output = 3
include_trailing_comma = true
force_grid_wrap = 0
use_parentheses = true
ensure_newline_before_comments = true

[tool.mypy]
python_version = "3.9"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
strict = true
''',
        ".style.yapf": '''[style]
based_on_style = google
column_limit = 80
dedent_closing_brackets = true
coalesce_brackets = true
'''
    },
    
    "cpp": {
        ".clang-format": '''# Google C++ Style
BasedOnStyle: Google
IndentWidth: 2
ColumnLimit: 80
AllowShortFunctionsOnASingleLine: Empty
BreakBeforeBraces: Attach
PointerAlignment: Left
ReferenceAlignment: Left
SortIncludes: true
IncludeBlocks: Preserve
SpaceAfterCStyleCast: false
SpaceAfterTemplateKeyword: true
SpaceBeforeRangeBasedForLoopColon: true
SpacesInParentheses: false
'''
    },
    
    "java": {
        ".java-format": '''# Use google-java-format
# Download from: https://github.com/google/google-java-format
# java -jar google-java-format.jar --replace --aosp $(find . -name "*.java")
'''
    },
    
    "javascript": {
        ".prettierrc": '''{
  "singleQuote": true,
  "trailingComma": "es5",
  "printWidth": 80,
  "tabWidth": 2,
  "useTabs": false,
  "semi": true,
  "bracketSpacing": true,
  "arrowParens": "always",
  "endOfLine": "lf"
}
''',
        ".prettierignore": '''# Dependencies
node_modules/
package-lock.json
yarn.lock

# Build outputs
dist/
build/
coverage/

# Generated files
*.min.js
*.min.css
'''
    },
    
    "editorconfig": {
        ".editorconfig": '''# EditorConfig is awesome: https://EditorConfig.org

root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true

[*.py]
indent_style = space
indent_size = 4
max_line_length = 80

[*.{js,ts,jsx,tsx}]
indent_style = space
indent_size = 2
max_line_length = 80

[*.{cpp,cc,c,h,hpp}]
indent_style = space
indent_size = 2
max_line_length = 80

[*.java]
indent_style = space
indent_size = 2
max_line_length = 100

[*.go]
indent_style = tab

[*.{json,yml,yaml}]
indent_style = space
indent_size = 2

[*.md]
trim_trailing_whitespace = false
max_line_length = off
'''
    }
}


def generate_config(languages: list[str], output_dir: Path) -> None:
    """Generate configuration files for specified languages."""
    
    generated = []
    
    for lang in languages:
        if lang == "all":
            # Generate all configs
            for l, configs in CONFIG_TEMPLATES.items():
                for filename, content in configs.items():
                    file_path = output_dir / filename
                    if not file_path.exists():
                        file_path.write_text(content)
                        generated.append(file_path)
            break
        
        if lang in CONFIG_TEMPLATES:
            for filename, content in CONFIG_TEMPLATES[lang].items():
                file_path = output_dir / filename
                if not file_path.exists():
                    file_path.write_text(content)
                    generated.append(file_path)
    
    # Always generate EditorConfig
    if "editorconfig" in CONFIG_TEMPLATES:
        for filename, content in CONFIG_TEMPLATES["editorconfig"].items():
            file_path = output_dir / filename
            if not file_path.exists():
                file_path.write_text(content)
                generated.append(file_path)
    
    return generated


def main():
    parser = argparse.ArgumentParser(
        description='Generate style configuration files'
    )
    parser.add_argument('--languages', '-l',
                       help='Comma-separated list of languages (python,cpp,java,js,all)')
    parser.add_argument('--output', '-o', default='.',
                       help='Output directory (default: current)')
    parser.add_argument('--all', '-a', action='store_true',
                       help='Generate all configuration files')
    
    args = parser.parse_args()
    
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if args.all:
        languages = ["all"]
    elif args.languages:
        languages = [lang.strip() for lang in args.languages.split(',')]
    else:
        print("Error: Specify --languages or --all", file=sys.stderr)
        sys.exit(1)
    
    print(f"🔧 Generating configs for: {', '.join(languages)}")
    print(f"   Output: {output_dir.absolute()}")
    print()
    
    generated = generate_config(languages, output_dir)
    
    if generated:
        print("Generated files:")
        for file_path in generated:
            print(f"  ✅ {file_path.name}")
        print()
        print(f"Total: {len(generated)} file(s)")
    else:
        print("No new files generated (files already exist)")


if __name__ == '__main__':
    import sys
    main()
