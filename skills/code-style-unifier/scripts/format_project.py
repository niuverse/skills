#!/usr/bin/env python3
"""
Format entire project to Google Style (or specified standard).

Usage:
    python format_project.py --path ./src
    python format_project.py --path ./src --languages python,cpp
    python format_project.py --path ./src --check
    python format_project.py --path ./src --apply
"""

import argparse
import sys
from pathlib import Path
from typing import Set

sys.path.insert(0, str(Path(__file__).parent))
from format_file import format_file, detect_language


# Default exclude patterns
DEFAULT_EXCLUDES = {
    'node_modules', 'vendor', 'third_party', 'build', 'dist',
    '__pycache__', '.git', '.venv', 'venv', '.tox', 
    '.pytest_cache', 'target', 'out', 'bin', 'obj',
    '*.pb.cc', '*.pb.h', '*_generated.py', '*_pb2.py'
}


def should_exclude(file_path: Path, exclude_patterns: Set[str]) -> bool:
    """Check if file should be excluded based on patterns."""
    # Check directory names
    for part in file_path.parts:
        if part in exclude_patterns:
            return True
    
    # Check file patterns
    for pattern in exclude_patterns:
        if pattern.startswith('*'):
            if file_path.name.endswith(pattern.lstrip('*')):
                return True
        elif file_path.name == pattern:
            return True
    
    return False


def collect_files(project_path: Path, languages: list[str] | None = None) -> dict[str, list[Path]]:
    """Collect all source files from project, grouped by language."""
    
    # Extension to language mapping
    ext_to_lang = {
        '.py': 'python',
        '.js': 'javascript',
        '.ts': 'typescript',
        '.cpp': 'cpp',
        '.cc': 'cpp',
        '.cxx': 'cpp',
        '.c': 'cpp',
        '.h': 'cpp',
        '.hpp': 'cpp',
        '.java': 'java',
        '.go': 'go',
    }
    
    if languages:
        # Filter to only requested languages
        ext_to_lang = {k: v for k, v in ext_to_lang.items() if v in languages}
    
    files_by_lang: dict[str, list[Path]] = {
        'python': [],
        'javascript': [],
        'typescript': [],
        'cpp': [],
        'java': [],
        'go': []
    }
    
    for ext, lang in ext_to_lang.items():
        for file_path in project_path.rglob(f'*{ext}'):
            if not should_exclude(file_path, DEFAULT_EXCLUDES):
                files_by_lang[lang].append(file_path)
    
    # Remove empty lists
    return {k: v for k, v in files_by_lang.items() if v}


def format_project(project_path: Path, 
                  languages: list[str] | None = None,
                  style: str = "google",
                  check_only: bool = False) -> tuple[int, int]:
    """Format entire project.
    
    Returns:
        Tuple of (success_count, total_count)
    """
    files_by_lang = collect_files(project_path, languages)
    
    total_files = sum(len(files) for files in files_by_lang.values())
    
    if total_files == 0:
        print("No source files found.")
        return 0, 0
    
    print(f"Found {total_files} source files")
    print(f"Languages: {', '.join(files_by_lang.keys())}")
    print(f"Style: {style}")
    print(f"Mode: {'Check' if check_only else 'Format'}")
    print()
    
    action = "Checking" if check_only else "Formatting"
    print(f"🔧 {action} files...")
    print("-" * 50)
    
    success_count = 0
    fail_count = 0
    skip_count = 0
    
    processed = 0
    for lang, files in files_by_lang.items():
        if not files:
            continue
        
        print(f"\n{lang.upper()} ({len(files)} files):")
        
        for file_path in files:
            processed += 1
            
            try:
                success = format_file(file_path, style, check_only)
                if success:
                    success_count += 1
                else:
                    fail_count += 1
            except Exception as e:
                print(f"  ❌ Error processing {file_path}: {e}")
                fail_count += 1
            
            # Progress indicator
            if processed % 10 == 0 or processed == total_files:
                print(f"  Progress: {processed}/{total_files}", end='\r')
    
    print()  # New line after progress
    print("-" * 50)
    
    return success_count, total_files


def main():
    parser = argparse.ArgumentParser(
        description='Format entire project to Google Style'
    )
    parser.add_argument('--path', '-p', required=True,
                       help='Path to project directory')
    parser.add_argument('--languages', '-l',
                       help='Comma-separated list of languages (python,cpp,java,js,ts,go)')
    parser.add_argument('--style', '-s', default='google',
                       help='Style to apply (default: google)')
    parser.add_argument('--check', '-c', action='store_true',
                       help='Check only, do not modify files')
    parser.add_argument('--apply', '-a', action='store_true',
                       help='Apply formatting (required to actually modify files)')
    
    args = parser.parse_args()
    
    project_path = Path(args.path)
    if not project_path.exists():
        print(f"Error: Path not found: {project_path}", file=sys.stderr)
        sys.exit(1)
    
    # Determine mode
    check_only = not args.apply
    
    if not args.apply and not args.check:
        print("Note: Running in check mode. Use --apply to actually format files.")
        print()
    
    # Parse languages
    languages = None
    if args.languages:
        languages = [lang.strip() for lang in args.languages.split(',')]
    
    # Run formatting
    success_count, total_count = format_project(
        project_path, languages, args.style, check_only
    )
    
    # Summary
    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)
    print(f"Total files: {total_count}")
    print(f"Passed: {success_count}")
    print(f"Need attention: {total_count - success_count}")
    
    if check_only:
        if success_count == total_count:
            print("\n✅ All files already follow the style guide!")
            sys.exit(0)
        else:
            print(f"\n⚠️  {total_count - success_count} files need formatting")
            print("   Run with --apply to format them")
            sys.exit(1)
    else:
        if success_count == total_count:
            print("\n✅ All files formatted successfully!")
            sys.exit(0)
        else:
            print(f"\n⚠️  {total_count - success_count} files could not be formatted")
            sys.exit(1)


if __name__ == '__main__':
    main()
