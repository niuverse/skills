#!/usr/bin/env python3
"""
Auto-update README.md Skills Catalog from skill directories
Usage: python scripts/update_catalog.py
"""

import re
from pathlib import Path


def parse_skill_md(skill_path: Path) -> dict | None:
    """Extract info from SKILL.md frontmatter."""
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return None
    
    content = skill_md.read_text()
    
    # Parse YAML frontmatter
    if not content.startswith("---"):
        return None
    
    try:
        # Extract frontmatter
        _, frontmatter, body = content.split("---", 2)
        
        # Extract name
        name_match = re.search(r'^name:\s*(.+)$', frontmatter, re.MULTILINE)
        name = name_match.group(1).strip() if name_match else skill_path.name
        
        # Extract first line of description (short desc)
        desc_match = re.search(r'^description:\s*\|\s*\n?\s*([^\n]+)', frontmatter, re.MULTILINE)
        if desc_match:
            short_desc = desc_match.group(1).strip()
        else:
            # Try inline description
            desc_match = re.search(r'^description:\s*(.+)$', frontmatter, re.MULTILINE)
            short_desc = desc_match.group(1).strip() if desc_match else "No description"
        
        # Limit description length
        if len(short_desc) > 60:
            short_desc = short_desc[:57] + "..."
        
        # Determine category from path or content
        category = "🛠️ Tools"  # default
        name_lower = name.lower()
        desc_lower = short_desc.lower()
        
        # Check name and description for keywords
        robotics_keywords = ['robot', 'sim', 'mujoco', 'isaac']
        python_keywords = ['python', 'architect', 'software']
        code_keywords = ['code', 'simplifier', 'cleanup', 'refactor']
        
        if any(k in name_lower or k in desc_lower for k in robotics_keywords):
            category = "🤖 Robotics"
        elif any(k in name_lower for k in python_keywords):
            category = "🐍 Python"
        elif any(k in name_lower for k in code_keywords):
            category = "✨ Code Quality"
        elif any(k in name_lower or k in desc_lower for k in ['web', 'api', 'http']):
            category = "🌐 Web"
        elif any(k in name_lower or k in desc_lower for k in ['data', 'ml', 'ai']):
            category = "🧠 AI/ML"
        
        return {
            "name": name,
            "path": skill_path.name,
            "description": short_desc,
            "category": category
        }
    except Exception as e:
        print(f"⚠️  Error parsing {skill_path}: {e}")
        return None


def generate_catalog(skills_dir: Path) -> str:
    """Generate Skills Catalog markdown table."""
    skills = []
    
    for skill_path in sorted(skills_dir.iterdir()):
        if skill_path.is_dir() and not skill_path.name.startswith("."):
            info = parse_skill_md(skill_path)
            if info:
                skills.append(info)
    
    if not skills:
        return "| Skill | Description | Category |\n|-------|-------------|----------|"
    
    # Group by category
    categories = {}
    for skill in skills:
        cat = skill["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(skill)
    
    # Generate table
    lines = ["| Skill | Description | Category |", "|-------|-------------|----------|"]
    
    # Sort categories for consistent order
    category_order = ["🤖 Robotics", "🐍 Python", "🧠 AI/ML", "🌐 Web", "🛠️ Tools", "📦 Other"]
    
    for category in category_order:
        if category in categories:
            for skill in sorted(categories[category], key=lambda x: x["name"]):
                lines.append(f"| [`{skill['name']}`](./skills/{skill['path']}/) | {skill['description']} | {category} |")
    
    # Add any remaining categories
    for category, cat_skills in sorted(categories.items()):
        if category not in category_order:
            for skill in sorted(cat_skills, key=lambda x: x["name"]):
                lines.append(f"| [`{skill['name']}`](./skills/{skill['path']}/) | {skill['description']} | {category} |")
    
    return "\n".join(lines)


def update_readme(readme_path: Path, catalog: str) -> bool:
    """Update README.md with new catalog."""
    content = readme_path.read_text()
    
    # Pattern to find Skills Catalog section
    pattern = r"(## 📚 Skills Catalog\n\n).*?(\n## |\n## 🚀|$)"
    
    # New section content
    new_section = f"## 📚 Skills Catalog\n\n{catalog}\n"
    
    # Check if section exists
    if "## 📚 Skills Catalog" not in content:
        print("⚠️  Skills Catalog section not found in README.md")
        return False
    
    # Replace the section
    updated = re.sub(
        r"(## 📚 Skills Catalog\n\n).*?(?=\n## |\Z)",
        new_section,
        content,
        flags=re.DOTALL
    )
    
    if updated == content:
        print("ℹ️  No changes needed")
        return False
    
    readme_path.write_text(updated)
    print("✅ Updated README.md Skills Catalog")
    return True


def main():
    """Main entry point."""
    skills_dir = Path("skills")
    readme_path = Path("README.md")
    
    if not skills_dir.exists():
        print("❌ skills/ directory not found")
        return 1
    
    if not readme_path.exists():
        print("❌ README.md not found")
        return 1
    
    print("🔍 Scanning skills...")
    catalog = generate_catalog(skills_dir)
    
    print("📝 Updating README.md...")
    updated = update_readme(readme_path, catalog)
    
    return 0 if updated else 0


if __name__ == "__main__":
    exit(main())
