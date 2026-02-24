#!/usr/bin/env python3
"""
OpenClaw Skill 运行时感知钩子

在 OpenClaw 调用 skill 时自动注入，检测使用场景与 skill 描述的匹配度
"""

import os
import sys
from pathlib import Path
from typing import Optional, Dict, Any

# 添加 bootstrap 引擎到路径
sys.path.insert(0, str(Path(__file__).parent))
from bootstrap_engine import SkillBootstrapEngine


class SkillRuntimeMonitor:
    """
    Skill 运行时监控器
    
    在每次 skill 调用时自动运行，检测：
    1. 用户请求是否超出 skill 描述范围
    2. 是否需要补充示例
    3. 是否需要澄清描述
    """
    
    def __init__(self, skills_root: Optional[str] = None):
        if skills_root is None:
            # 尝试从环境变量或默认位置获取
            skills_root = os.environ.get(
                "NIUVERSE_SKILLS_ROOT", 
                str(Path(__file__).parent.parent)
            )
        self.engine = SkillBootstrapEngine(skills_root)
        self.current_skill: Optional[str] = None
        self.conversation_context: list = []
    
    def on_skill_invoked(self, skill_name: str, user_request: str) -> Dict[str, Any]:
        """
        当 skill 被调用时触发
        
        返回: 是否需要记录缺口
        """
        self.current_skill = skill_name
        
        # 分析 skill 覆盖度
        analysis = self.engine.analyze_skill_coverage(skill_name, user_request)
        
        result = {
            "skill": skill_name,
            "gaps_detected": [],
            "auto_recorded": []
        }
        
        # 自动检测并记录缺口
        for gap in analysis.get("potential_gaps", []):
            gap_id = self.engine.record_gap(
                skill_name=skill_name,
                gap_type=gap["type"],
                context=user_request,
                suggestion=gap["description"],
                severity="medium"
            )
            result["auto_recorded"].append({
                "gap_id": gap_id,
                "type": gap["type"]
            })
        
        return result
    
    def on_skill_response(self, skill_name: str, user_request: str, 
                          response: str, confidence: float) -> Optional[str]:
        """
        当 skill 响应后触发
        
        如果响应置信度低，可能表示 skill 覆盖不足
        """
        if confidence < 0.7:  # 置信度阈值
            gap_id = self.engine.record_gap(
                skill_name=skill_name,
                gap_type="unclear_description",
                context=user_request,
                suggestion=f"低置信度响应，可能需要补充: {user_request}",
                severity="high" if confidence < 0.5 else "medium"
            )
            return gap_id
        return None
    
    def suggest_enhancement(self, skill_name: str) -> Dict[str, Any]:
        """
        基于积累的缺口建议增强方向
        """
        gaps = self.engine.list_pending_gaps(skill_name)
        
        if not gaps:
            return {"message": "No enhancement suggestions at this time"}
        
        # 按类型分组
        gap_types = {}
        for gap in gaps:
            gtype = gap["gap_type"]
            if gtype not in gap_types:
                gap_types[gtype] = []
            gap_types[gtype].append(gap)
        
        # 生成建议
        suggestions = []
        for gtype, type_gaps in gap_types.items():
            suggestions.append({
                "type": gtype,
                "count": len(type_gaps),
                "priority": "high" if len(type_gaps) > 2 else "medium",
                "example_contexts": [g["context"][:100] for g in type_gaps[:3]]
            })
        
        return {
            "skill": skill_name,
            "total_gaps": len(gaps),
            "suggestions": sorted(suggestions, key=lambda x: x["count"], reverse=True)
        }


# 便捷的装饰器/钩子函数
_monitor: Optional[SkillRuntimeMonitor] = None


def get_monitor() -> SkillRuntimeMonitor:
    """获取全局监控器实例"""
    global _monitor
    if _monitor is None:
        _monitor = SkillRuntimeMonitor()
    return _monitor


def skill_invoked(skill_name: str, user_request: str) -> Dict[str, Any]:
    """
    在 skill 被调用时调用此函数
    
    可以在 OpenClaw 的 skill 加载机制中集成
    """
    return get_monitor().on_skill_invoked(skill_name, user_request)


def skill_responded(skill_name: str, user_request: str, 
                    response: str, confidence: float = 1.0) -> Optional[str]:
    """
    在 skill 响应后调用此函数
    """
    return get_monitor().on_skill_response(skill_name, user_request, response, confidence)


def get_enhancement_suggestions(skill_name: str) -> Dict[str, Any]:
    """
    获取 skill 增强建议
    """
    return get_monitor().suggest_enhancement(skill_name)


if __name__ == "__main__":
    # 测试
    monitor = SkillRuntimeMonitor()
    
    # 模拟 skill 调用
    result = monitor.on_skill_invoked(
        "robot-sim-expert",
        "How do I handle errors in Isaac Lab when the simulation crashes?"
    )
    print("Detection result:", result)
    
    # 获取增强建议
    suggestions = monitor.suggest_enhancement("robot-sim-expert")
    print("\nEnhancement suggestions:", suggestions)
