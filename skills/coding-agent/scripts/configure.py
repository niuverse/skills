#!/usr/bin/env python3
"""
代理配置工具
管理 AI 代理的 API 密钥和配置
"""

import argparse
import os
import yaml
from pathlib import Path


DEFAULT_CONFIG = {
    "agents": {
        "codex": {
            "type": "openai",
            "model": "5.3-codex",
            "api_key": "${CODEX_API_KEY}",
            "max_tokens": 4000,
            "temperature": 0.2
        },
        "claude-opus": {
            "type": "anthropic",
            "model": "claude-opus-4.6",
            "api_key": "${ANTHROPIC_API_KEY}",
            "max_tokens": 8000,
            "temperature": 0.2
        },
        "claude-sonnet": {
            "type": "anthropic",
            "model": "claude-sonnet-4.6",
            "api_key": "${ANTHROPIC_API_KEY}",
            "max_tokens": 8000,
            "temperature": 0.2
        },
        "gemini": {
            "type": "google",
            "model": "gemini-2.5-pro",
            "api_key": "${GEMINI_API_KEY}",
            "max_tokens": 4000,
            "temperature": 0.2
        },
        "gpt4": {
            "type": "openai",
            "model": "gpt-4.5",
            "api_key": "${OPENAI_API_KEY}",
            "max_tokens": 4000,
            "temperature": 0.2
        },
        "kimi": {
            "type": "openai",
            "model": "kimi-k2.5",
            "api_key": "${KIMI_API_KEY}",
            "endpoint": "https://api.moonshot.cn/v1",
            "max_tokens": 4000,
            "temperature": 0.2
        },
        "opencode": {
            "type": "local",
            "model": "opencode-7b",
            "endpoint": "http://localhost:8080/v1/completions",
            "max_tokens": 4000,
            "temperature": 0.2
        }
    },
    "strategies": {
        "fast_coding": {
            "primary": "codex",
            "fallback": "gemini"
        },
        "deep_refactor": {
            "primary": "claude-opus",
            "review_by": "codex"
        },
        "parallel_implementation": {
            "agents": ["codex", "claude-sonnet", "gemini"],
            "selection": "best_of_three"
        }
    }
}


def init_config(path: str = "./agents.yaml"):
    """初始化配置文件"""
    config_path = Path(path)
    
    if config_path.exists():
        print(f"⚠️  配置文件已存在: {path}")
        return
    
    config_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(config_path, "w") as f:
        yaml.dump(DEFAULT_CONFIG, f, default_flow_style=False, allow_unicode=True)
    
    print(f"✅ 配置文件已创建: {path}")
    print("\n请设置以下环境变量:")
    print("  export CODEX_API_KEY='your-codex-key'")
    print("  export ANTHROPIC_API_KEY='your-anthropic-key'")
    print("  export GEMINI_API_KEY='your-gemini-key'")
    print("  export OPENAI_API_KEY='your-openai-key'")


def add_agent(path: str, name: str, agent_type: str, model: str, api_key: str = None):
    """添加代理"""
    config_path = Path(path)
    
    if not config_path.exists():
        print(f"❌ 配置文件不存在: {path}")
        print("请先运行: python configure.py --init")
        return
    
    with open(config_path) as f:
        config = yaml.safe_load(f)
    
    # 构建代理配置
    agent_config = {
        "type": agent_type,
        "model": model,
        "max_tokens": 4000,
        "temperature": 0.2
    }
    
    if api_key:
        agent_config["api_key"] = api_key
    else:
        env_var = f"{name.upper()}_API_KEY"
        agent_config["api_key"] = f"${{{env_var}}}"
        print(f"💡 请设置环境变量: export {env_var}='your-api-key'")
    
    if agent_type == "local":
        agent_config["endpoint"] = input("本地模型 endpoint (默认: http://localhost:8080/v1/completions): ") or "http://localhost:8080/v1/completions"
    
    config["agents"][name] = agent_config
    
    with open(config_path, "w") as f:
        yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
    
    print(f"✅ 代理已添加: {name}")


def list_agents(path: str = "./agents.yaml"):
    """列出所有代理"""
    config_path = Path(path)
    
    if not config_path.exists():
        print(f"❌ 配置文件不存在: {path}")
        return
    
    with open(config_path) as f:
        config = yaml.safe_load(f)
    
    print("\n🤖 已配置的代理:\n")
    for name, agent in config.get("agents", {}).items():
        api_status = "✅" if _check_api_key(agent.get("api_key", "")) else "❌"
        print(f"  {api_status} {name}")
        print(f"     类型: {agent['type']}")
        print(f"     模型: {agent['model']}")
        if agent.get("endpoint"):
            print(f"     端点: {agent['endpoint']}")
        print()
    
    print("\n📋 策略配置:\n")
    for name, strategy in config.get("strategies", {}).items():
        print(f"  {name}:")
        for k, v in strategy.items():
            print(f"     {k}: {v}")
        print()


def _check_api_key(key: str) -> bool:
    """检查 API key 是否已设置"""
    if not key:
        return False
    if key.startswith("${") and key.endswith("}"):
        env_var = key[2:-1]
        return os.getenv(env_var) is not None
    return True


def main():
    parser = argparse.ArgumentParser(description="代理配置工具")
    parser.add_argument("--config", "-c", default="./agents.yaml", help="配置文件路径")
    parser.add_argument("--init", action="store_true", help="初始化配置")
    parser.add_argument("--add", help="添加代理名称")
    parser.add_argument("--type", choices=["openai", "anthropic", "google", "local"],
                       help="代理类型")
    parser.add_argument("--model", help="模型名称")
    parser.add_argument("--api-key", help="API 密钥")
    parser.add_argument("--list", "-l", action="store_true", help="列出代理")
    
    args = parser.parse_args()
    
    if args.init:
        init_config(args.config)
    elif args.add:
        if not args.type or not args.model:
            print("❌ 添加代理需要指定 --type 和 --model")
            return
        add_agent(args.config, args.add, args.type, args.model, args.api_key)
    elif args.list:
        list_agents(args.config)
    else:
        list_agents(args.config)


if __name__ == "__main__":
    main()
