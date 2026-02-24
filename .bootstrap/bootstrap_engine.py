#!/usr/bin/env python3
"""
Skill Bootstrap Engine - 自动化 Skill 进化机制

核心功能：
1. 运行时感知 - 在使用 skill 时识别缺口
2. 自动记录 - 记录需要改进的地方
3. 自动完善 - 定期更新 skill 内容
4. 验证闭环 - 确保改进有效
"""

import os
import re
import json
import hashlib
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import Optional, List, Dict, Any
import yaml


@dataclass
class SkillGap:
    """记录 skill 的缺口信息"""
    skill_name: str
    gap_type: str  # 'missing_example', 'unclear_description', 'missing_param', 'edge_case', etc.
    context: str  # 触发场景
    suggestion: str  # 建议补充内容
    timestamp: str
    severity: str = "medium"  # low, medium, high
    resolved: bool = False
    resolution_commit: Optional[str] = None


class SkillBootstrapEngine:
    """Skill 自举引擎"""
    
    def __init__(self, skills_root: str):
        self.skills_root = Path(skills_root)
        self.bootstrap_dir = self.skills_root / ".bootstrap"
        self.pending_dir = self.bootstrap_dir / "pending"
        self.resolved_dir = self.bootstrap_dir / "resolved"
        self._ensure_dirs()
    
    def _ensure_dirs(self):
        """确保目录结构存在"""
        self.bootstrap_dir.mkdir(exist_ok=True)
        self.pending_dir.mkdir(exist_ok=True)
        self.resolved_dir.mkdir(exist_ok=True)
    
    def record_gap(self, skill_name: str, gap_type: str, context: str, 
                   suggestion: str, severity: str = "medium") -> str:
        """
        记录一个 skill 缺口
        
        返回: gap_id 用于后续追踪
        """
        gap = SkillGap(
            skill_name=skill_name,
            gap_type=gap_type,
            context=context,
            suggestion=suggestion,
            timestamp=datetime.now().isoformat(),
            severity=severity
        )
        
        # 生成唯一 ID
        gap_id = hashlib.md5(
            f"{skill_name}:{gap_type}:{context}".encode()
        ).hexdigest()[:12]
        
        # 保存到 pending
        gap_file = self.pending_dir / f"{skill_name}_{gap_id}.json"
        with open(gap_file, 'w', encoding='utf-8') as f:
            json.dump(asdict(gap), f, indent=2, ensure_ascii=False)
        
        return gap_id
    
    def list_pending_gaps(self, skill_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """列出所有待处理的缺口"""
        gaps = []
        pattern = f"{skill_name}_*.json" if skill_name else "*.json"
        
        for gap_file in self.pending_dir.glob(pattern):
            with open(gap_file, 'r', encoding='utf-8') as f:
                gap = json.load(f)
                gap['file'] = gap_file.name
                gaps.append(gap)
        
        return sorted(gaps, key=lambda x: x['timestamp'], reverse=True)
    
    def analyze_skill_coverage(self, skill_name: str, usage_context: str) -> Dict[str, Any]:
        """
        分析 skill 对特定使用场景的覆盖度
        
        返回: 覆盖度分析报告
        """
        skill_path = self.skills_root / "skills" / skill_name / "SKILL.md"
        if not skill_path.exists():
            return {"error": f"Skill {skill_name} not found"}
        
        with open(skill_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 解析 frontmatter
        frontmatter = self._parse_frontmatter(content)
        
        # 分析覆盖度
        analysis = {
            "skill_name": skill_name,
            "usage_context": usage_context,
            "description": frontmatter.get("description", ""),
            "sections": self._extract_sections(content),
            "examples_count": content.count("```"),
            "has_quick_start": "quick start" in content.lower() or "快速开始" in content,
            "has_troubleshooting": "troubleshoot" in content.lower() or "问题" in content or "debug" in content.lower(),
            "coverage_score": 0,  # 待计算
            "potential_gaps": []
        }
        
        # 基于使用场景检测潜在缺口
        analysis["potential_gaps"] = self._detect_gaps(usage_context, content)
        
        return analysis
    
    def _parse_frontmatter(self, content: str) -> Dict[str, Any]:
        """解析 YAML frontmatter"""
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                try:
                    return yaml.safe_load(parts[1]) or {}
                except yaml.YAMLError:
                    pass
        return {}
    
    def _extract_sections(self, content: str) -> List[str]:
        """提取文档中的章节标题"""
        sections = []
        for line in content.split("\n"):
            if line.startswith("## ") or line.startswith("### "):
                sections.append(line.strip("# "))
        return sections
    
    def _detect_gaps(self, usage_context: str, skill_content: str) -> List[Dict[str, str]]:
        """基于使用场景检测潜在缺口"""
        gaps = []
        content_lower = skill_content.lower()
        context_lower = usage_context.lower()
        
        # 检测常见缺口模式
        gap_patterns = [
            ("error", "missing_error_handling", "缺少错误处理示例"),
            ("config", "missing_config_example", "缺少配置示例"),
            ("install", "missing_installation", "缺少安装说明"),
            ("api", "missing_api_reference", "缺少 API 参考"),
            ("example", "more_examples_needed", "需要更多示例"),
            ("advanced", "missing_advanced_usage", "缺少高级用法"),
            ("performance", "missing_optimization", "缺少性能优化建议"),
            ("test", "missing_testing_guide", "缺少测试指南"),
        ]
        
        for keyword, gap_type, description in gap_patterns:
            if keyword in context_lower and keyword not in content_lower:
                gaps.append({
                    "type": gap_type,
                    "description": description,
                    "trigger": f"用户询问 '{keyword}' 相关内容"
                })
        
        return gaps
    
    def auto_enhance_skill(self, skill_name: str, gap_id: Optional[str] = None) -> Dict[str, Any]:
        """
        自动增强 skill
        
        基于记录的缺口自动更新 SKILL.md
        """
        result = {
            "skill_name": skill_name,
            "enhanced": False,
            "changes": [],
            "error": None
        }
        
        # 获取待处理的缺口
        if gap_id:
            gaps = [g for g in self.list_pending_gaps(skill_name) 
                   if g['file'].startswith(f"{skill_name}_{gap_id}")]
        else:
            gaps = self.list_pending_gaps(skill_name)
        
        if not gaps:
            result["message"] = "No pending gaps found"
            return result
        
        skill_path = self.skills_root / "skills" / skill_name / "SKILL.md"
        if not skill_path.exists():
            result["error"] = f"Skill {skill_name} not found"
            return result
        
        # 读取原始内容
        with open(skill_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        # 基于缺口生成增强内容
        enhanced_content = original_content
        for gap in gaps:
            enhancement = self._generate_enhancement(gap)
            if enhancement:
                enhanced_content = self._apply_enhancement(enhanced_content, enhancement)
                result["changes"].append({
                    "gap_type": gap["gap_type"],
                    "enhancement": enhancement["description"]
                })
                
                # 标记为已解决
                self._resolve_gap(gap["file"], "auto-enhanced")
        
        # 保存增强后的内容
        if result["changes"]:
            with open(skill_path, 'w', encoding='utf-8') as f:
                f.write(enhanced_content)
            result["enhanced"] = True
        
        return result
    
    def _generate_enhancement(self, gap: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """基于缺口生成增强内容"""
        gap_type = gap["gap_type"]
        suggestion = gap["suggestion"]
        
        enhancements = {
            "missing_example": {
                "section": "## 使用示例",
                "content": f"\n### 新增示例\n\n```python\n# {suggestion}\n```\n",
                "description": f"添加示例: {suggestion[:50]}..."
            },
            "unclear_description": {
                "section": "## 详细说明",
                "content": f"\n{suggestion}\n",
                "description": f"澄清描述: {suggestion[:50]}..."
            },
            "missing_param": {
                "section": "## 参数说明",
                "content": f"\n- `{suggestion}`: 参数说明待补充\n",
                "description": f"添加参数: {suggestion}"
            },
            "edge_case": {
                "section": "## 边界情况",
                "content": f"\n### {suggestion}\n\n处理方式...\n",
                "description": f"添加边界情况处理: {suggestion[:50]}..."
            },
        }
        
        return enhancements.get(gap_type, {
            "section": "## 补充说明",
            "content": f"\n{suggestion}\n",
            "description": f"补充: {suggestion[:50]}..."
        })
    
    def _apply_enhancement(self, content: str, enhancement: Dict[str, Any]) -> str:
        """将增强内容应用到 skill"""
        section = enhancement["section"]
        new_content = enhancement["content"]
        
        # 如果章节存在，在章节后添加内容
        if section in content:
            # 找到章节位置，在下一个 ## 之前插入
            pattern = f"({re.escape(section)}.*?)(\n## |\Z)"
            match = re.search(pattern, content, re.DOTALL)
            if match:
                insert_pos = match.end(1)
                return content[:insert_pos] + new_content + content[insert_pos:]
        
        # 如果章节不存在，在文件末尾添加
        return content + f"\n{section}\n{new_content}"
    
    def _resolve_gap(self, gap_file: str, resolution: str):
        """标记缺口为已解决"""
        pending_path = self.pending_dir / gap_file
        if not pending_path.exists():
            return
        
        with open(pending_path, 'r', encoding='utf-8') as f:
            gap = json.load(f)
        
        gap["resolved"] = True
        gap["resolution_commit"] = resolution
        gap["resolved_at"] = datetime.now().isoformat()
        
        # 移动到 resolved 目录
        resolved_path = self.resolved_dir / gap_file
        with open(resolved_path, 'w', encoding='utf-8') as f:
            json.dump(gap, f, indent=2, ensure_ascii=False)
        
        pending_path.unlink()
    
    def generate_skill_report(self, skill_name: Optional[str] = None) -> Dict[str, Any]:
        """生成 skill 进化报告"""
        report = {
            "generated_at": datetime.now().isoformat(),
            "skills": []
        }
        
        if skill_name:
            skills = [self.skills_root / "skills" / skill_name]
        else:
            skills = [d for d in (self.skills_root / "skills").iterdir() if d.is_dir()]
        
        for skill_dir in skills:
            skill_md = skill_dir / "SKILL.md"
            if not skill_md.exists():
                continue
            
            skill_info = {
                "name": skill_dir.name,
                "pending_gaps": len(self.list_pending_gaps(skill_dir.name)),
                "last_modified": datetime.fromtimestamp(skill_md.stat().st_mtime).isoformat()
            }
            report["skills"].append(skill_info)
        
        return report


# CLI 接口
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Skill Bootstrap Engine")
    parser.add_argument("--skills-root", default=".", help="Skills repository root")
    parser.add_argument("record-gap", dest="action", action="store_const", const="record")
    parser.add_argument("list-gaps", dest="action", action="store_const", const="list")
    parser.add_argument("analyze", dest="action", action="store_const", const="analyze")
    parser.add_argument("enhance", dest="action", action="store_const", const="enhance")
    parser.add_argument("report", dest="action", action="store_const", const="report")
    parser.add_argument("--skill", help="Skill name")
    parser.add_argument("--type", help="Gap type")
    parser.add_argument("--context", help="Usage context")
    parser.add_argument("--suggestion", help="Suggestion content")
    parser.add_argument("--severity", default="medium", help="Gap severity")
    
    args = parser.parse_args()
    
    engine = SkillBootstrapEngine(args.skills_root)
    
    if args.action == "record":
        gap_id = engine.record_gap(
            args.skill, args.type, args.context, args.suggestion, args.severity
        )
        print(f"Recorded gap: {gap_id}")
    
    elif args.action == "list":
        gaps = engine.list_pending_gaps(args.skill)
        for gap in gaps:
            print(f"[{gap['severity']}] {gap['skill_name']}: {gap['gap_type']}")
            print(f"  Context: {gap['context'][:80]}...")
            print()
    
    elif args.action == "analyze":
        analysis = engine.analyze_skill_coverage(args.skill, args.context or "")
        print(json.dumps(analysis, indent=2, ensure_ascii=False))
    
    elif args.action == "enhance":
        result = engine.auto_enhance_skill(args.skill)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif args.action == "report":
        report = engine.generate_skill_report(args.skill)
        print(json.dumps(report, indent=2, ensure_ascii=False))
