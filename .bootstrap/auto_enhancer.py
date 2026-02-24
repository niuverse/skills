#!/usr/bin/env python3
"""
自动增强 Skill 内容

基于记录的缺口，自动生成增强内容并更新 SKILL.md
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional

sys.path.insert(0, str(Path(__file__).parent))
from bootstrap_engine import SkillBootstrapEngine


class SkillAutoEnhancer:
    """Skill 自动增强器"""
    
    def __init__(self, skills_root: str):
        self.engine = SkillBootstrapEngine(skills_root)
        self.skills_root = Path(skills_root)
    
    def enhance_skill(self, skill_name: str, dry_run: bool = False) -> Dict[str, Any]:
        """
        自动增强指定 skill
        """
        result = {
            "skill": skill_name,
            "enhanced": False,
            "changes": [],
            "warnings": []
        }
        
        skill_dir = self.skills_root / "skills" / skill_name
        skill_md = skill_dir / "SKILL.md"
        
        if not skill_md.exists():
            result["error"] = f"Skill {skill_name} not found"
            return result
        
        # 读取原始内容
        with open(skill_md, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        # 获取待处理缺口
        gaps = self.engine.list_pending_gaps(skill_name)
        
        if not gaps:
            result["message"] = "No pending gaps to process"
            return result
        
        # 按类型分组处理
        content = original_content
        
        # 1. 处理 missing_example 类型
        example_gaps = [g for g in gaps if g["gap_type"] == "missing_example"]
        if example_gaps:
            content = self._add_examples_section(content, example_gaps)
            result["changes"].append(f"Added {len(example_gaps)} example(s)")
        
        # 2. 处理 unclear_description 类型
        desc_gaps = [g for g in gaps if g["gap_type"] == "unclear_description"]
        if desc_gaps:
            content = self._enhance_description(content, desc_gaps)
            result["changes"].append(f"Enhanced description based on {len(desc_gaps)} feedback(s)")
        
        # 3. 处理 missing_param 类型
        param_gaps = [g for g in gaps if g["gap_type"] == "missing_param"]
        if param_gaps:
            content = self._add_params_section(content, param_gaps)
            result["changes"].append(f"Added {len(param_gaps)} parameter(s)")
        
        # 4. 处理 edge_case 类型
        edge_gaps = [g for g in gaps if g["gap_type"] == "edge_case"]
        if edge_gaps:
            content = self._add_edge_cases_section(content, edge_gaps)
            result["changes"].append(f"Added {len(edge_gaps)} edge case(s)")
        
        # 5. 处理其他类型
        other_gaps = [g for g in gaps if g["gap_type"] not in 
                     ["missing_example", "unclear_description", "missing_param", "edge_case"]]
        if other_gaps:
            content = self._add_notes_section(content, other_gaps)
            result["changes"].append(f"Added {len(other_gaps)} note(s)")
        
        # 保存更新后的内容
        if content != original_content:
            if not dry_run:
                with open(skill_md, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                # 标记所有缺口为已解决
                for gap in gaps:
                    self.engine._resolve_gap(gap["file"], "auto-enhanced")
                
                result["enhanced"] = True
            else:
                result["dry_run"] = True
                # 保存到临时文件供查看
                preview_path = skill_dir / "SKILL.md.preview"
                with open(preview_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                result["preview_path"] = str(preview_path)
        
        return result
    
    def _add_examples_section(self, content: str, gaps: List[Dict]) -> str:
        """添加示例章节"""
        examples = []
        for gap in gaps:
            ctx = gap["context"]
            sug = gap["suggestion"]
            examples.append(f"""
### {ctx[:50]}{'...' if len(ctx) > 50 else ''}

{sug}

```python
# 示例代码待补充
```
""")
        
        section_content = "## 补充示例\n\n" + "\n".join(examples)
        
        # 查找插入位置（在 ## 常见问题 或文件末尾之前）
        if "## 常见问题" in content:
            content = content.replace("## 常见问题", section_content + "\n## 常见问题")
        elif "## Troubleshooting" in content:
            content = content.replace("## Troubleshooting", section_content + "\n## Troubleshooting")
        else:
            content = content + "\n" + section_content
        
        return content
    
    def _enhance_description(self, content: str, gaps: List[Dict]) -> str:
        """增强描述"""
        # 在 frontmatter 后添加补充说明
        if "---" in content:
            parts = content.split("---", 2)
            if len(parts) >= 3:
                additions = "\n\n## 使用场景补充\n\n基于实际使用反馈，本 skill 还适用于以下场景：\n\n"
                for gap in gaps:
                    ctx = gap["context"]
                    additions += f"- {ctx}\n"
                additions += "\n"
                return parts[0] + "---" + parts[1] + "---" + additions + parts[2]
        
        return content
    
    def _add_params_section(self, content: str, gaps: List[Dict]) -> str:
        """添加参数说明"""
        params = []
        for gap in gaps:
            sug = gap["suggestion"]
            params.append(f"- `{sug}`: 参数说明待补充")
        
        section = "## 参数说明补充\n\n" + "\n".join(params) + "\n"
        
        # 插入到合适位置
        if "## 快速开始" in content:
            content = content.replace("## 快速开始", section + "\n## 快速开始")
        elif "## Quick Start" in content:
            content = content.replace("## Quick Start", section + "\n## Quick Start")
        else:
            content = content + "\n" + section
        
        return content
    
    def _add_edge_cases_section(self, content: str, gaps: List[Dict]) -> str:
        """添加边界情况章节"""
        cases = []
        for gap in gaps:
            ctx = gap["context"]
            cases.append(f"""
### {ctx[:50]}{'...' if len(ctx) > 50 else ''}

**问题**: {ctx}

**解决方案**: 待补充具体处理方式
""")
        
        section = "## 边界情况处理\n\n" + "\n".join(cases)
        
        if "## 调试技巧" in content:
            content = content.replace("## 调试技巧", section + "\n## 调试技巧")
        elif "## Debugging" in content:
            content = content.replace("## Debugging", section + "\n## Debugging")
        else:
            content = content + "\n" + section
        
        return content
    
    def _add_notes_section(self, content: str, gaps: List[Dict]) -> str:
        """添加备注章节"""
        notes = []
        for gap in gaps:
            notes.append(f"- **{gap['gap_type']}**: {gap['suggestion']}")
        
        section = "## 补充说明\n\n> 以下内容由自动 bootstrap 机制基于使用反馈生成：\n\n" + "\n".join(notes)
        
        # 添加到文件末尾
        content = content + "\n" + section
        
        return content
    
    def enhance_all_skills(self, dry_run: bool = False) -> List[Dict[str, Any]]:
        """增强所有有缺口的 skills"""
        results = []
        
        skills_dir = self.skills_root / "skills"
        for skill_dir in skills_dir.iterdir():
            if not skill_dir.is_dir():
                continue
            
            gaps = self.engine.list_pending_gaps(skill_dir.name)
            if gaps:
                result = self.enhance_skill(skill_dir.name, dry_run)
                results.append(result)
        
        return results


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Auto-enhance skills")
    parser.add_argument("--skills-root", default=".", help="Skills root directory")
    parser.add_argument("--skill", help="Specific skill to enhance")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without applying")
    parser.add_argument("--all", action="store_true", help="Enhance all skills with pending gaps")
    
    args = parser.parse_args()
    
    enhancer = SkillAutoEnhancer(args.skills_root)
    
    if args.all:
        results = enhancer.enhance_all_skills(args.dry_run)
        for r in results:
            print(f"\n{r['skill']}:")
            if r.get('error'):
                print(f"  Error: {r['error']}")
            elif r['enhanced']:
                print(f"  Enhanced: {', '.join(r['changes'])}")
            else:
                print(f"  {r.get('message', 'No changes')}")
    elif args.skill:
        result = enhancer.enhance_skill(args.skill, args.dry_run)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("Use --skill <name> or --all")
