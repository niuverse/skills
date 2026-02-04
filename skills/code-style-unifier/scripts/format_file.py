#!/usr/bin/env python3
"""
Format a single file to Google Style (or specified standard).

Usage:
    python format_file.py path/to/file.py --style google
    python format_file.py path/to/file.py --style google --check
    python format_file.py path/to/file.cpp --style google
"""

import argparse
import subprocess
import sys
from pathlib import Path


# Configuration presets for different languages and styles
STYLE_PRESETS = {
    "python": {
        "google": {
            "yapf_args": [
                "--style", "{based_on_style: google, column_limit: 80}",
                "--recursive"
            ],
            "isort_args": ["--profile", "google", "--line-length", "80"]
        }
    },
    "cpp": {
        "google": {
            "clang_format_args": [
                "-style={BasedOnStyle: Google, IndentWidth: 2, ColumnLimit: 80}"
            ]
        }
    },
    "java": {
        "google": {
            "google_java_format_args": ["--replace", "--aosp"]
        }
    },
    "javascript": {
        "google": {
            "prettier_args": [
                "--single-quote", "--trailing-comma", "es5",
                "--print-width", "80", "--tab-width", "2"
            ]
        }
    }
}


def detect_language(file_path: Path) -> str:
    """Detect programming language from file extension."""
    extensions = {
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
    return extensions.get(file_path.suffix.lower(), 'unknown')


def format_python(file_path: Path, style: str, check_only: bool = False) -> bool:
    """Format Python file using yapf."""
    try:
        preset = STYLE_PRESETS["python"].get(style, STYLE_PRESETS["python"]["google"])
        
        # Check yapf is available
        yapf_result = subprocess.run(
            ["yapf", "--version"],
            capture_output=True,
            check=False
        )
        
        if yapf_result.returncode != 0:
            print("  Installing yapf...")
            subprocess.run([sys.executable, "-m", "pip", "install", "yapf", "-q"], check=True)
        
        cmd = ["yapf"] + preset["yapf_args"]
        
        if check_only:
            cmd.append("--diff")
        else:
            cmd.append("--in-place")
        
        cmd.append(str(file_path))
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if check_only:
            if result.stdout:
                print(f"  ⚠️  {file_path} would be reformatted")
                return False
            return True
        else:
            if result.returncode == 0:
                print(f"  ✅ Formatted {file_path}")
                return True
            else:
                print(f"  ❌ Error formatting {file_path}: {result.stderr}")
                return False
                
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def format_cpp(file_path: Path, style: str, check_only: bool = False) -> bool:
    """Format C/C++ file using clang-format."""
    try:
        preset = STYLE_PRESETS["cpp"].get(style, STYLE_PRESETS["cpp"]["google"])
        
        # Check clang-format is available
        clang_result = subprocess.run(
            ["clang-format", "--version"],
            capture_output=True,
            check=False
        )
        
        if clang_result.returncode != 0:
            print("  ⚠️  clang-format not found. Please install LLVM/Clang.")
            return False
        
        cmd = ["clang-format"] + preset["clang_format_args"]
        
        if check_only:
            cmd.append("--dry-run")
        else:
            cmd.append("-i")  # In-place
        
        cmd.append(str(file_path))
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if check_only:
            if "requires formatting" in result.stderr or result.returncode != 0:
                print(f"  ⚠️  {file_path} would be reformatted")
                return False
            return True
        else:
            if result.returncode == 0:
                print(f"  ✅ Formatted {file_path}")
                return True
            else:
                print(f"  ❌ Error formatting {file_path}")
                return False
                
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def format_java(file_path: Path, style: str, check_only: bool = False) -> bool:
    """Format Java file using google-java-format."""
    try:
        # google-java-format is a jar file
        jar_path = Path.home() / ".local" / "lib" / "google-java-format.jar"
        
        if not jar_path.exists():
            print(f"  ⚠️  google-java-format not found at {jar_path}")
            print("  Please download from: https://github.com/google/google-java-format")
            return False
        
        cmd = ["java", "-jar", str(jar_path)]
        
        if check_only:
            cmd.append("--dry-run")
        else:
            cmd.append("--replace")
        
        cmd.append(str(file_path))
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if check_only:
            if result.returncode != 0:
                print(f"  ⚠️  {file_path} would be reformatted")
                return False
            return True
        else:
            if result.returncode == 0:
                print(f"  ✅ Formatted {file_path}")
                return True
            else:
                print(f"  ❌ Error formatting {file_path}")
                return False
                
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def format_javascript(file_path: Path, style: str, check_only: bool = False) -> bool:
    """Format JavaScript/TypeScript file using prettier."""
    try:
        preset = STYLE_PRESETS["javascript"].get(style, STYLE_PRESETS["javascript"]["google"])
        
        # Check prettier is available
        prettier_result = subprocess.run(
            ["npx", "prettier", "--version"],
            capture_output=True,
            check=False
        )
        
        if prettier_result.returncode != 0:
            print("  Installing prettier...")
            subprocess.run(["npm", "install", "-g", "prettier"], check=False)
        
        cmd = ["npx", "prettier"] + preset["prettier_args"]
        
        if check_only:
            cmd.append("--check")
        else:
            cmd.append("--write")
        
        cmd.append(str(file_path))
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if check_only:
            if result.returncode != 0:
                print(f"  ⚠️  {file_path} would be reformatted")
                return False
            return True
        else:
            if result.returncode == 0:
                print(f"  ✅ Formatted {file_path}")
                return True
            else:
                print(f"  ❌ Error formatting {file_path}")
                return False
                
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def format_go(file_path: Path, style: str, check_only: bool = False) -> bool:
    """Format Go file using gofmt."""
    try:
        cmd = ["gofmt"]
        
        if check_only:
            cmd.append("-l")  # List files that would be formatted
        else:
            cmd.append("-w")  # Write result to file
        
        cmd.append(str(file_path))
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if check_only:
            if result.stdout.strip():
                print(f"  ⚠️  {file_path} would be reformatted")
                return False
            return True
        else:
            if result.returncode == 0:
                print(f"  ✅ Formatted {file_path}")
                return True
            else:
                print(f"  ❌ Error formatting {file_path}")
                return False
                
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def format_file(file_path: Path, style: str = "google", check_only: bool = False) -> bool:
    """Format a single file based on its language."""
    language = detect_language(file_path)
    
    formatters = {
        "python": format_python,
        "cpp": format_cpp,
        "c": format_cpp,
        "java": format_java,
        "javascript": format_javascript,
        "typescript": format_javascript,
        "go": format_go,
    }
    
    formatter = formatters.get(language)
    if not formatter:
        print(f"  ⚠️  No formatter available for {language} files")
        return False
    
    return formatter(file_path, style, check_only)


def main():
    parser = argparse.ArgumentParser(
        description='Format a single file to Google Style'
    )
    parser.add_argument('file', help='Path to the file to format')
    parser.add_argument('--style', '-s', default='google',
                       help='Style to apply (default: google)')
    parser.add_argument('--check', '-c', action='store_true',
                       help='Check only, do not modify files')
    
    args = parser.parse_args()
    
    file_path = Path(args.file)
    if not file_path.exists():
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        sys.exit(1)
    
    action = "Checking" if args.check else "Formatting"
    print(f"🔧 {action} {file_path} with {args.style} style...")
    
    success = format_file(file_path, args.style, args.check)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
