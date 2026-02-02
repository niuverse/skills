#!/usr/bin/env python3
"""
Skill validation script for niuverse/skills
Validates skill structure and metadata
"""

import os
import re
import sys
from pathlib import Path


def validate_skill_md(skill_path: Path) -> list[str]:
    """Validate SKILL.md file"""
    errors = []
    skill_md = skill_path / "SKILL.md"
    
    if not skill_md.exists():
        errors.append(f"Missing SKILL.md in {skill_path}")
        return errors
    
    content = skill_md.read_text()
    
    # Check for YAML frontmatter
    if not content.startswith("---"):
        errors.append(f"{skill_md}: Missing YAML frontmatter")
    
    # Check for required fields
    required_fields = ["name:", "description:"]
    for field in required_fields:
        if field not in content:
            errors.append(f"{skill_md}: Missing required field '{field}'")
    
    return errors


def validate_skill_structure(skill_path: Path) -> list[str]:
    """Validate overall skill structure"""
    errors = []
    
    # Check for at least one content directory
    content_dirs = ["references", "scripts", "assets"]
    has_content = any((skill_path / d).exists() for d in content_dirs)
    
    if not has_content:
        errors.append(f"{skill_path}: Skill should have at least one of: {content_dirs}")
    
    return errors


def main():
    skills_dir = Path("skills")
    
    if not skills_dir.exists():
        print("❌ No skills directory found")
        sys.exit(1)
    
    all_errors = []
    skill_count = 0
    
    for skill_path in skills_dir.iterdir():
        if skill_path.is_dir() and not skill_path.name.startswith("."):
            skill_count += 1
            print(f"\n🔍 Validating {skill_path.name}...")
            
            errors = validate_skill_md(skill_path)
            errors.extend(validate_skill_structure(skill_path))
            
            if errors:
                all_errors.extend(errors)
                for error in errors:
                    print(f"  ❌ {error}")
            else:
                print(f"  ✅ {skill_path.name} is valid")
    
    print(f"\n{'='*50}")
    print(f"Validated {skill_count} skill(s)")
    
    if all_errors:
        print(f"Found {len(all_errors)} error(s)")
        sys.exit(1)
    else:
        print("✅ All skills are valid!")
        sys.exit(0)


if __name__ == "__main__":
    main()
