---
name: coding-agent
description: |
  Multi-model coding agent orchestration skill. Enables coordination between different
  AI coding agents like Kimi, Codex, Claude Code, Gemini, OpenCode, etc.
  
  Use cases:
  - Kimi orchestrates Codex + Claude Code for development
  - Codex manages multiple Claude Code instances
  - Multi-agent parallel coding with task distribution
  - Agent selection based on task characteristics
  - Cross-model code review and validation
  
  Triggers: coding agent, multi-agent, codex, claude code, gemini, opencode,
  agent orchestration, parallel coding, distributed development, ai coding team
---

# Coding Agent Orchestrator

🤖 多模型 AI 编程代理协调器 - 让不同 AI 协同开发

## 🎯 核心能力

| 能力 | 描述 |
|------|------|
| **代理调度** | 根据任务特性选择最佳 AI 代理 |
| **多代理协作** | 协调多个 AI 代理并行工作 |
| **任务分发** | 将大任务拆分给多个代理 |
| **代码审查** | 跨模型代码评审 |
| **结果聚合** | 合并多个代理的输出 |
| **故障转移** | 代理失败时自动切换 |

## 🚀 支持的 AI 代理

| 代理 | 类型 | 最佳场景 |
|------|------|----------|
| **Kimi** | 大模型 | 架构设计、复杂推理 |
| **Codex** | 代码专用 | 快速编码、API 实现 |
| **Claude Code** | 代码专用 | 深度重构、调试 |
| **Gemini** | 大模型 | 多模态、长上下文 |
| **OpenCode** | 开源替代 | 本地部署、隐私敏感 |
| **GPT-4** | 大模型 | 通用任务 |

## 📖 使用模式

### 模式 1: Kimi 主控 + Codex/Claude 执行

```
┌─────────┐     ┌─────────────┐     ┌─────────────┐
│  User   │────▶│    Kimi     │────▶│  Architect  │
│ Request │     │  (Orchestrator)   │  │  Design     │
└─────────┘     └──────┬──────┘     └─────────────┘
                       │
       ┌───────────────┼───────────────┐
       ▼               ▼               ▼
  ┌─────────┐    ┌─────────┐    ┌─────────┐
  │  Codex  │    │ Claude  │    │  Gemini │
  │ (Fast)  │    │ (Deep)  │    │(Context)│
  └────┬────┘    └────┬────┘    └────┬────┘
       │               │               │
       └───────────────┼───────────────┘
                       ▼
              ┌─────────────────┐
              │  Result Merge   │
              └─────────────────┘
```

### 模式 2: Codex 主控 + 多 Claude 并行

```
┌─────────┐     ┌─────────────┐
│  Task   │────▶│    Codex    │
│         │     │ (Coordinator)│
└─────────┘     └──────┬──────┘
                       │
       ┌───────────────┼───────────────┐
       ▼               ▼               ▼
  ┌─────────┐    ┌─────────┐    ┌─────────┐
  │ Claude  │    │ Claude  │    │ Claude  │
  │  #1     │    │  #2     │    │  #3     │
  │(Frontend)│   │(Backend)│    │(Tests)  │
  └────┬────┘    └────┬────┘    └────┬────┘
       │               │               │
       └───────────────┼───────────────┘
                       ▼
              ┌─────────────────┐
              │  Integration    │
              └─────────────────┘
```

### 模式 3: 代理竞争 (Agent Arena)

```
┌─────────┐     ┌─────────────┐
│  Task   │────▶│  All Agents │
│         │     │  (Parallel) │
└─────────┘     └──────┬──────┘
                       │
       ┌───────────────┼───────────────┐
       ▼               ▼               ▼
  ┌─────────┐    ┌─────────┐    ┌─────────┐
  │  Codex  │    │ Claude  │    │  Gemini │
  │ Result  │    │ Result  │    │ Result  │
  └────┬────┘    └────┬────┘    └────┬────┘
       │               │               │
       └───────────────┼───────────────┘
                       ▼
              ┌─────────────────┐
              │  Best Result    │
              │  Selection      │
              └─────────────────┘
```

## 🛠️ 快速开始

### 1. 环境验证
```bash
python scripts/verify_env.py
```

### 2. 配置代理
```bash
python scripts/configure.py --add codex --api-key $CODEX_API_KEY
python scripts/configure.py --add claude --api-key $ANTHROPIC_API_KEY
python scripts/configure.py --add gemini --api-key $GEMINI_API_KEY
```

### 3. 运行多代理任务
```bash
# 模式 1: Kimi 主控
python scripts/orchestrate.py --mode kimi-led --task "实现一个 REST API" --agents codex,claude

# 模式 2: Codex 主控 + 并行 Claude
python scripts/orchestrate.py --mode codex-led --task "重构代码库" --parallel 3

# 模式 3: 代理竞争
python scripts/orchestrate.py --mode arena --task "优化算法" --agents codex,claude,gemini
```

## 📋 详细用法

### 单代理调用

```python
from scripts.agent_caller import AgentCaller

# 调用 Codex
codex = AgentCaller("codex", api_key="...")
result = codex.code("实现一个快速排序算法")

# 调用 Claude Code
claude = AgentCaller("claude", api_key="...")
result = claude.code("重构这个函数", context=code_context)
```

### 多代理协调

```python
from scripts.orchestrator import MultiAgentOrchestrator

# 创建协调器
orch = MultiAgentOrchestrator()

# 注册代理
orch.register("codex", codex_config)
orch.register("claude", claude_config)
orch.register("gemini", gemini_config)

# 分配任务
task = {
    "description": "实现用户认证系统",
    "subtasks": [
        {"agent": "codex", "task": "实现 JWT 生成和验证"},
        {"agent": "claude", "task": "设计数据库模型"},
        {"agent": "gemini", "task": "编写 API 文档"}
    ]
}

results = orch.execute_parallel(task)
```

### 智能代理选择

```python
from scripts.agent_selector import AgentSelector

selector = AgentSelector()

# 根据任务特性自动选择代理
agent = selector.select_for_task(
    task="优化 React 组件性能",
    criteria=["speed", "frontend_expertise"]
)

print(f"选择代理: {agent.name}")  # 可能输出: claude
```

## 🔧 配置示例

### agents.yaml

```yaml
agents:
  codex:
    type: openai
    model: codex-latest
    api_key: ${CODEX_API_KEY}
    max_tokens: 4000
    temperature: 0.2
    
  claude:
    type: anthropic
    model: claude-sonnet-4-20250514
    api_key: ${ANTHROPIC_API_KEY}
    max_tokens: 8000
    
  gemini:
    type: google
    model: gemini-2.0-flash
    api_key: ${GEMINI_API_KEY}
    
  opencode:
    type: local
    endpoint: http://localhost:8080/v1/completions
    model: opencode-7b

strategies:
  fast_coding:
    primary: codex
    fallback: gemini
    
  deep_refactor:
    primary: claude
    review_by: codex
    
  parallel_implementation:
    agents: [codex, claude, gemini]
    selection: best_of_three
```

## 🎭 典型工作流

### 工作流 1: 新功能开发

```bash
# 1. Kimi 设计架构
python scripts/orchestrate.py \
  --mode kimi-led \
  --task "设计一个实时聊天系统架构" \
  --output architecture.md

# 2. Codex 快速实现核心功能
python scripts/orchestrate.py \
  --mode single \
  --agent codex \
  --task "根据架构实现 WebSocket 服务器" \
  --context architecture.md

# 3. Claude 深度优化
python scripts/orchestrate.py \
  --mode single \
  --agent claude \
  --task "优化代码性能和可读性" \
  --context websocket_server.py

# 4. 多代理代码审查
python scripts/orchestrate.py \
  --mode review \
  --agents codex,claude,gemini \
  --file websocket_server.py
```

### 工作流 2: Bug 修复

```bash
# 并行诊断
python scripts/orchestrate.py \
  --mode arena \
  --task "诊断并修复这个 bug" \
  --context error_logs.txt \
  --agents codex,claude \
  --selection consensus
```

### 工作流 3: 代码迁移

```bash
# 多代理并行迁移不同模块
python scripts/orchestrate.py \
  --mode codex-led \
  --task "将 Python2 代码迁移到 Python3" \
  --parallel 4 \
  --split-by module
```

## 📊 代理能力矩阵

| 任务类型 | Kimi | Codex | Claude | Gemini | OpenCode |
|----------|------|-------|--------|--------|----------|
| 架构设计 | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| 快速编码 | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐ |
| 代码重构 | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐ |
| 调试排错 | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐ |
| 测试生成 | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐ |
| 文档编写 | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| 长上下文 | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| API 设计 | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐ |

## 🚨 故障排除

| 问题 | 解决方案 |
|------|----------|
| 代理超时 | 增加 timeout 配置，或启用 fallback |
| 结果不一致 | 使用 review 模式让多个代理投票 |
| 上下文过长 | 使用 Gemini 或启用上下文压缩 |
| API 限制 | 启用本地缓存，或使用 OpenCode |

## 📚 参考资料

- [resources.md](references/resources.md) - 各代理 API 文档
- [best-practices.md](references/best-practices.md) - 多代理协作最佳实践
- [examples/](templates/) - 示例配置和脚本

---

*Many agents, one goal: ship great code.* 🚀
