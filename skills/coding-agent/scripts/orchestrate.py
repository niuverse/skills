#!/usr/bin/env python3
"""
多代理协调器
支持 Kimi/Codex/Claude/Gemini 等 AI 代理的协作
"""

import argparse
import asyncio
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Any
import yaml


@dataclass
class AgentConfig:
    """代理配置"""
    name: str
    type: str  # openai, anthropic, google, local
    model: str
    api_key: Optional[str] = None
    endpoint: Optional[str] = None
    max_tokens: int = 4000
    temperature: float = 0.2
    timeout: int = 120


@dataclass
class TaskResult:
    """任务结果"""
    agent: str
    task: str
    output: str
    success: bool
    duration: float
    metadata: Dict = field(default_factory=dict)


class AgentCaller:
    """单个代理调用器"""
    
    def __init__(self, config: AgentConfig):
        self.config = config
        self._client = None
    
    def _get_client(self):
        """获取或创建客户端"""
        if self._client is None:
            if self.config.type == "openai":
                import openai
                self._client = openai.OpenAI(api_key=self.config.api_key)
            elif self.config.type == "anthropic":
                import anthropic
                self._client = anthropic.Anthropic(api_key=self.config.api_key)
            elif self.config.type == "google":
                import google.generativeai as genai
                genai.configure(api_key=self.config.api_key)
                self._client = genai
            elif self.config.type == "local":
                # 本地模型通过 HTTP 调用
                import httpx
                self._client = httpx.Client(timeout=self.config.timeout)
        return self._client
    
    def code(self, task: str, context: Optional[str] = None) -> str:
        """
        执行编码任务
        
        Args:
            task: 任务描述
            context: 上下文信息
            
        Returns:
            生成的代码或分析结果
        """
        prompt = self._build_prompt(task, context)
        
        if self.config.type == "openai":
            return self._call_openai(prompt)
        elif self.config.type == "anthropic":
            return self._call_anthropic(prompt)
        elif self.config.type == "google":
            return self._call_google(prompt)
        elif self.config.type == "local":
            return self._call_local(prompt)
        else:
            raise ValueError(f"未知的代理类型: {self.config.type}")
    
    def _build_prompt(self, task: str, context: Optional[str]) -> str:
        """构建提示词"""
        system_msg = """You are an expert software engineer. 
Write clean, well-documented, production-ready code.
Follow best practices and include error handling."""
        
        if context:
            return f"{system_msg}\n\nContext:\n{context}\n\nTask:\n{task}"
        return f"{system_msg}\n\nTask:\n{task}"
    
    def _call_openai(self, prompt: str) -> str:
        """调用 OpenAI/Codex"""
        client = self._get_client()
        response = client.chat.completions.create(
            model=self.config.model,
            messages=[
                {"role": "system", "content": "You are a helpful coding assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=self.config.max_tokens,
            temperature=self.config.temperature
        )
        return response.choices[0].message.content
    
    def _call_anthropic(self, prompt: str) -> str:
        """调用 Anthropic/Claude"""
        client = self._get_client()
        response = client.messages.create(
            model=self.config.model,
            max_tokens=self.config.max_tokens,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
    
    def _call_google(self, prompt: str) -> str:
        """调用 Google/Gemini"""
        client = self._get_client()
        model = client.GenerativeModel(self.config.model)
        response = model.generate_content(prompt)
        return response.text
    
    def _call_local(self, prompt: str) -> str:
        """调用本地模型"""
        client = self._get_client()
        response = client.post(
            self.config.endpoint,
            json={
                "model": self.config.model,
                "prompt": prompt,
                "max_tokens": self.config.max_tokens
            }
        )
        return response.json()["choices"][0]["text"]


class MultiAgentOrchestrator:
    """多代理协调器"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.agents: Dict[str, AgentCaller] = {}
        self.configs: Dict[str, AgentConfig] = {}
        self.executor = ThreadPoolExecutor(max_workers=5)
        
        if config_path:
            self.load_config(config_path)
    
    def load_config(self, path: str):
        """加载配置文件"""
        with open(path) as f:
            config = yaml.safe_load(f)
        
        for name, agent_config in config.get("agents", {}).items():
            # 替换环境变量
            api_key = agent_config.get("api_key", "")
            if api_key.startswith("${") and api_key.endswith("}"):
                env_var = api_key[2:-1]
                api_key = os.getenv(env_var, "")
            
            cfg = AgentConfig(
                name=name,
                type=agent_config["type"],
                model=agent_config["model"],
                api_key=api_key,
                endpoint=agent_config.get("endpoint"),
                max_tokens=agent_config.get("max_tokens", 4000),
                temperature=agent_config.get("temperature", 0.2)
            )
            self.register(name, cfg)
    
    def register(self, name: str, config: AgentConfig):
        """注册代理"""
        self.configs[name] = config
        self.agents[name] = AgentCaller(config)
        print(f"✅ 注册代理: {name} ({config.type}/{config.model})")
    
    def execute_single(self, agent_name: str, task: str, context: Optional[str] = None) -> TaskResult:
        """执行单代理任务"""
        import time
        
        if agent_name not in self.agents:
            raise ValueError(f"未找到代理: {agent_name}")
        
        agent = self.agents[agent_name]
        start = time.time()
        
        try:
            output = agent.code(task, context)
            success = True
        except Exception as e:
            output = f"Error: {str(e)}"
            success = False
        
        duration = time.time() - start
        
        return TaskResult(
            agent=agent_name,
            task=task,
            output=output,
            success=success,
            duration=duration
        )
    
    def execute_parallel(self, tasks: List[Dict]) -> List[TaskResult]:
        """
        并行执行多个任务
        
        Args:
            tasks: 任务列表，每个任务包含 agent 和 task
            
        Returns:
            结果列表
        """
        futures = []
        for t in tasks:
            future = self.executor.submit(
                self.execute_single,
                t["agent"],
                t["task"],
                t.get("context")
            )
            futures.append(future)
        
        results = [f.result() for f in futures]
        return results
    
    def execute_arena(self, task: str, agents: List[str], context: Optional[str] = None) -> TaskResult:
        """
        代理竞技场模式 - 多个代理执行同一任务，选择最佳结果
        
        Args:
            task: 任务描述
            agents: 代理列表
            context: 上下文
            
        Returns:
            最佳结果
        """
        print(f"🏟️  启动代理竞技场: {len(agents)} 个代理")
        
        tasks = [{"agent": a, "task": task, "context": context} for a in agents]
        results = self.execute_parallel(tasks)
        
        # 过滤成功结果
        successful = [r for r in results if r.success]
        
        if not successful:
            print("❌ 所有代理都失败了")
            return results[0] if results else None
        
        # 简单启发式：选择输出最长的成功结果
        # 实际应用中可以使用 LLM 来评估质量
        best = max(successful, key=lambda r: len(r.output))
        
        print(f"🏆 最佳结果来自: {best.agent} (长度: {len(best.output)})")
        return best
    
    def execute_review(self, code: str, agents: List[str]) -> Dict[str, str]:
        """
        多代理代码审查
        
        Args:
            code: 待审查代码
            agents: 审查代理列表
            
        Returns:
            各代理的审查意见
        """
        review_task = f"""请审查以下代码，提供:
1. 代码质量评分 (1-10)
2. 潜在问题
3. 改进建议

代码:
```
{code}
```
"""
        
        tasks = [{"agent": a, "task": review_task} for a in agents]
        results = self.execute_parallel(tasks)
        
        reviews = {}
        for r in results:
            if r.success:
                reviews[r.agent] = r.output
        
        return reviews


def main():
    parser = argparse.ArgumentParser(description="多代理协调器")
    parser.add_argument("--config", "-c", default="./agents.yaml", help="配置文件路径")
    parser.add_argument("--mode", "-m", choices=["single", "parallel", "arena", "review"],
                       default="single", help="执行模式")
    parser.add_argument("--agent", "-a", help="单代理模式使用的代理")
    parser.add_argument("--agents", help="多代理模式使用的代理列表 (逗号分隔)")
    parser.add_argument("--task", "-t", help="任务描述")
    parser.add_argument("--context", help="上下文文件路径")
    parser.add_argument("--file", "-f", help="代码文件路径 (用于 review 模式)")
    parser.add_argument("--output", "-o", help="输出文件路径")
    
    args = parser.parse_args()
    
    # 初始化协调器
    orch = MultiAgentOrchestrator(args.config if os.path.exists(args.config) else None)
    
    # 加载上下文
    context = None
    if args.context:
        context = Path(args.context).read_text()
    
    # 执行
    if args.mode == "single":
        if not args.agent:
            print("❌ 单代理模式需要指定 --agent")
            sys.exit(1)
        result = orch.execute_single(args.agent, args.task, context)
        print(f"\n{'='*50}")
        print(f"代理: {result.agent}")
        print(f"成功: {result.success}")
        print(f"耗时: {result.duration:.2f}s")
        print(f"{'='*50}\n")
        print(result.output)
        
    elif args.mode == "parallel":
        if not args.agents:
            print("❌ 并行模式需要指定 --agents")
            sys.exit(1)
        agent_list = args.agents.split(",")
        tasks = [{"agent": a, "task": args.task, "context": context} for a in agent_list]
        results = orch.execute_parallel(tasks)
        
        for r in results:
            print(f"\n{'='*50}")
            print(f"代理: {r.agent} | 成功: {r.success} | 耗时: {r.duration:.2f}s")
            print(f"{'='*50}\n")
            print(r.output[:500] + "..." if len(r.output) > 500 else r.output)
    
    elif args.mode == "arena":
        if not args.agents:
            print("❌ 竞技场模式需要指定 --agents")
            sys.exit(1)
        agent_list = args.agents.split(",")
        result = orch.execute_arena(args.task, agent_list, context)
        print(f"\n{'='*50}")
        print(f"最佳代理: {result.agent}")
        print(f"{'='*50}\n")
        print(result.output)
    
    elif args.mode == "review":
        if not args.file:
            print("❌ 审查模式需要指定 --file")
            sys.exit(1)
        code = Path(args.file).read_text()
        agent_list = args.agents.split(",") if args.agents else list(orch.agents.keys())
        reviews = orch.execute_review(code, agent_list)
        
        for agent, review in reviews.items():
            print(f"\n{'='*50}")
            print(f"审查者: {agent}")
            print(f"{'='*50}\n")
            print(review)
    
    # 保存输出
    if args.output and 'result' in locals():
        Path(args.output).write_text(result.output)
        print(f"\n✅ 结果已保存: {args.output}")


if __name__ == "__main__":
    main()
