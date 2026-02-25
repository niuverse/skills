#!/usr/bin/env python3
"""
代理选择器
根据任务特性智能选择最佳 AI 代理
"""

from dataclasses import dataclass
from typing import List, Optional, Dict
import json


@dataclass
class AgentCapability:
    """代理能力评分"""
    architecture_design: int = 3  # 架构设计
    fast_coding: int = 3          # 快速编码
    code_refactor: int = 3        # 代码重构
    debugging: int = 3            # 调试排错
    test_generation: int = 3      # 测试生成
    documentation: int = 3        # 文档编写
    long_context: int = 3         # 长上下文
    api_design: int = 3           # API 设计


AGENT_CAPABILITIES = {
    "kimi": AgentCapability(
        architecture_design=5, fast_coding=4, code_refactor=5,
        debugging=5, test_generation=4, documentation=5,
        long_context=5, api_design=5
    ),
    "codex": AgentCapability(
        architecture_design=3, fast_coding=5, code_refactor=4,
        debugging=4, test_generation=5, documentation=3,
        long_context=3, api_design=5
    ),
    "claude-opus": AgentCapability(
        architecture_design=5, fast_coding=5, code_refactor=5,
        debugging=5, test_generation=5, documentation=5,
        long_context=5, api_design=5
    ),
    "claude-sonnet": AgentCapability(
        architecture_design=4, fast_coding=5, code_refactor=5,
        debugging=5, test_generation=5, documentation=4,
        long_context=4, api_design=5
    ),
    "gemini": AgentCapability(
        architecture_design=5, fast_coding=4, code_refactor=4,
        debugging=4, test_generation=4, documentation=5,
        long_context=5, api_design=4
    ),
    "opencode": AgentCapability(
        architecture_design=3, fast_coding=3, code_refactor=3,
        debugging=3, test_generation=3, documentation=3,
        long_context=3, api_design=3
    ),
    "gpt4": AgentCapability(
        architecture_design=5, fast_coding=4, code_refactor=5,
        debugging=5, test_generation=4, documentation=5,
        long_context=4, api_design=5
    )
}


class AgentSelector:
    """代理选择器"""
    
    TASK_PATTERNS = {
        "architecture_design": [
            "架构", "architecture", "design", "system design",
            "microservice", "distributed", "scalability"
        ],
        "fast_coding": [
            "快速", "quick", "implement", "coding",
            "feature", "add", "create"
        ],
        "code_refactor": [
            "重构", "refactor", "rewrite", "optimize",
            "clean up", "improve", "modernize"
        ],
        "debugging": [
            "调试", "debug", "fix", "bug", "error",
            "issue", "troubleshoot", "not working"
        ],
        "test_generation": [
            "测试", "test", "unit test", "integration test",
            "coverage", "pytest", "jest"
        ],
        "documentation": [
            "文档", "doc", "readme", "comment",
            "explain", "tutorial", "guide"
        ],
        "long_context": [
            "大文件", "large file", "codebase", "entire project",
            "many files", "complex project"
        ],
        "api_design": [
            "API", "interface", "endpoint", "REST",
            "GraphQL", "swagger", "openapi"
        ]
    }
    
    def __init__(self, available_agents: Optional[List[str]] = None):
        self.available_agents = available_agents or list(AGENT_CAPABILITIES.keys())
    
    def analyze_task(self, task: str) -> Dict[str, float]:
        """
        分析任务特性
        
        Args:
            task: 任务描述
            
        Returns:
            各维度的重要性评分 (0-1)
        """
        task_lower = task.lower()
        scores = {}
        
        for dimension, patterns in self.TASK_PATTERNS.items():
            score = 0
            for pattern in patterns:
                if pattern.lower() in task_lower:
                    score += 1
            scores[dimension] = min(score / 2, 1.0)  # 归一化到 0-1
        
        return scores
    
    def select_for_task(self, task: str, criteria: Optional[List[str]] = None) -> str:
        """
        为任务选择最佳代理
        
        Args:
            task: 任务描述
            criteria: 优先考虑的能力维度
            
        Returns:
            最佳代理名称
        """
        task_scores = self.analyze_task(task)
        
        # 如果指定了 criteria，提高这些维度的权重
        if criteria:
            for c in criteria:
                if c in task_scores:
                    task_scores[c] *= 2
        
        # 计算每个代理的匹配分数
        best_agent = None
        best_score = -1
        
        for agent_name in self.available_agents:
            if agent_name not in AGENT_CAPABILITIES:
                continue
            
            capabilities = AGENT_CAPABILITIES[agent_name]
            score = 0
            
            for dimension, importance in task_scores.items():
                cap_value = getattr(capabilities, dimension, 3)
                score += cap_value * importance
            
            if score > best_score:
                best_score = score
                best_agent = agent_name
        
        return best_agent
    
    def select_multiple(self, task: str, n: int = 3) -> List[str]:
        """
        选择多个合适的代理（用于并行或竞技场模式）
        
        Args:
            task: 任务描述
            n: 选择的代理数量
            
        Returns:
            代理名称列表
        """
        task_scores = self.analyze_task(task)
        
        agent_scores = []
        for agent_name in self.available_agents:
            if agent_name not in AGENT_CAPABILITIES:
                continue
            
            capabilities = AGENT_CAPABILITIES[agent_name]
            score = 0
            
            for dimension, importance in task_scores.items():
                cap_value = getattr(capabilities, dimension, 3)
                score += cap_value * importance
            
            agent_scores.append((agent_name, score))
        
        # 按分数排序，取前 n 个
        agent_scores.sort(key=lambda x: x[1], reverse=True)
        return [a[0] for a in agent_scores[:n]]
    
    def explain_selection(self, task: str, agent: str) -> str:
        """
        解释为什么选择这个代理
        
        Args:
            task: 任务描述
            agent: 选中的代理
            
        Returns:
            解释文本
        """
        task_scores = self.analyze_task(task)
        capabilities = AGENT_CAPABILITIES.get(agent, AgentCapability())
        
        # 找出最重要的维度
        top_dimensions = sorted(task_scores.items(), key=lambda x: x[1], reverse=True)[:3]
        
        explanation = f"选择 {agent} 的原因:\n"
        for dim, score in top_dimensions:
            if score > 0:
                cap_value = getattr(capabilities, dim, 3)
                explanation += f"  - {dim}: 任务重要性 {score:.1f}, {agent} 能力 {cap_value}/5\n"
        
        return explanation


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="代理选择器")
    parser.add_argument("task", help="任务描述")
    parser.add_argument("--agents", "-a", help="可用代理列表 (逗号分隔)")
    parser.add_argument("--criteria", "-c", help="优先考虑的能力 (逗号分隔)")
    parser.add_argument("--multiple", "-n", type=int, help="选择多个代理")
    parser.add_argument("--explain", "-e", action="store_true", help="解释选择原因")
    
    args = parser.parse_args()
    
    available = args.agents.split(",") if args.agents else None
    criteria = args.criteria.split(",") if args.criteria else None
    
    selector = AgentSelector(available_agents=available)
    
    if args.multiple:
        agents = selector.select_multiple(args.task, n=args.multiple)
        print(f"推荐代理: {', '.join(agents)}")
    else:
        agent = selector.select_for_task(args.task, criteria)
        print(f"推荐代理: {agent}")
        
        if args.explain:
            print("\n" + selector.explain_selection(args.task, agent))


if __name__ == "__main__":
    main()
