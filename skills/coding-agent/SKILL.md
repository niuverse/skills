---
name: coding-agent
description: |
  Multi-model coding agent orchestration skill. Enables coordination between different
  AI coding agents like Kimi, Codex, Claude Code, Gemini, MiniMax, GLM, etc.
  
  Use cases:
  - Multi-agent parallel coding with task distribution
  - Agent selection based on task characteristics
  - Cross-model code review and validation
  
  Triggers: coding agent, multi-agent, codex, claude code, gemini, minimax, glm,
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

### 国际模型

| 代理 | 类型 | 最佳场景 | 最新模型 |
|------|------|----------|----------|
| **Codex** | 代码专用 | 快速编码、API 实现 | `gpt-5.3-codex` |
| **Claude** | 代码专用 | 深度重构、调试 | `claude-opus-4.6` |
| **Gemini** | 大模型 | 多模态、长上下文 | `gemini-3.1-pro` |

### 国产模型

| 代理 | 类型 | 最佳场景 | 最新模型 |
|------|------|----------|----------|
| **Kimi** | 大模型 | 架构设计、Agent 集群 | `kimi-k2.5` |
| **MiniMax** | 代码专用 | 高性价比、架构师级编程 | `minimax-m2.5` |
| **GLM** | 大模型 | 编程与智能体能力 | `glm-5` |
| **OpenCode** | 开源替代 | 本地部署、隐私敏感 | 本地模型 |

## 📖 使用模式

### 模式 1: 单代理执行

```bash
python scripts/orchestrate.py --mode single --agent codex --task "实现快速排序"
```

### 模式 2: 多代理并行

```bash
python scripts/orchestrate.py --mode parallel --agents codex,claude --task "实现 REST API"
```

### 模式 3: 代理竞技场 (Agent Arena)

多个代理执行同一任务，自动选择最佳结果。

```bash
python scripts/orchestrate.py --mode arena --task "优化算法" --agents codex,claude,gemini
```

### 模式 4: 代码审查

```bash
python scripts/orchestrate.py --mode review --file code.py --agents codex,claude
```

## 🛠️ 快速开始

### 1. 环境验证
```bash
python scripts/verify_env.py
```

### 2. 配置代理
```bash
python scripts/configure.py --init

# 设置环境变量
export OPENAI_API_KEY="your-key"      # For Codex
export ANTHROPIC_API_KEY="your-key"   # For Claude
export GEMINI_API_KEY="your-key"      # For Gemini
export KIMI_API_KEY="your-key"        # For Kimi (Moonshot)
export MINIMAX_API_KEY="your-key"     # For MiniMax
export GLM_API_KEY="your-key"         # For GLM (Zhipu)
```

### 3. 运行任务
```bash
# 单代理
python scripts/orchestrate.py --mode single --agent codex --task "实现快速排序"

# 多代理竞技场
python scripts/orchestrate.py --mode arena --task "优化算法" --agents codex,claude,gemini
```

## 📋 详细用法

### 单代理调用

```python
from scripts.orchestrate import AgentCaller, AgentConfig

# 配置代理
config = AgentConfig(
    name="codex",
    type="openai",
    model="gpt-5.3-codex",
    api_key="your-key"
)

# 调用代理
agent = AgentCaller(config)
result = agent.code("实现一个快速排序算法")
```

### 多代理协调

```python
from scripts.orchestrate import MultiAgentOrchestrator

# 创建协调器
orch = MultiAgentOrchestrator("./agents.yaml")

# 并行执行多个任务
tasks = [
    {"agent": "codex", "task": "实现 JWT 生成"},
    {"agent": "claude", "task": "设计数据库模型"},
    {"agent": "gemini", "task": "编写 API 文档"}
]

results = orch.execute_parallel(tasks)
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

print(f"选择代理: {agent}")
```

## 🔧 配置示例

### agents.yaml

```yaml
agents:
  # OpenAI / Codex
  codex:
    type: openai
    model: gpt-5.3-codex
    api_key: ${OPENAI_API_KEY}
    max_tokens: 4000
    temperature: 0.2
    
  # Anthropic / Claude
  claude-opus:
    type: anthropic
    model: claude-opus-4.6
    api_key: ${ANTHROPIC_API_KEY}
    max_tokens: 8000
    temperature: 0.2
    
  claude-sonnet:
    type: anthropic
    model: claude-sonnet-4.6
    api_key: ${ANTHROPIC_API_KEY}
    max_tokens: 8000
    temperature: 0.2
    
  # Google / Gemini
  gemini:
    type: google
    model: gemini-3.1-pro
    api_key: ${GEMINI_API_KEY}
    max_tokens: 4000
    temperature: 0.2
    
  # Moonshot / Kimi
  kimi:
    type: openai  # OpenAI compatible API
    model: kimi-k2.5
    api_key: ${KIMI_API_KEY}
    endpoint: https://api.moonshot.cn/v1
    max_tokens: 4000
    temperature: 0.2
    
  # MiniMax
  minimax:
    type: openai  # OpenAI compatible API
    model: minimax-m2.5
    api_key: ${MINIMAX_API_KEY}
    endpoint: https://api.minimaxi.com/v1
    max_tokens: 4000
    temperature: 0.2
    
  # Zhipu / GLM
  glm:
    type: openai  # OpenAI compatible API
    model: glm-5
    api_key: ${GLM_API_KEY}
    endpoint: https://open.bigmodel.cn/api/paas/v4
    max_tokens: 4000
    temperature: 0.2
    
  # Local / OpenCode
  opencode:
    type: local
    model: opencode-7b
    endpoint: http://localhost:8080/v1/completions
    max_tokens: 4000
    temperature: 0.2

strategies:
  fast_coding:
    primary: codex
    fallback: minimax
    
  deep_refactor:
    primary: claude-opus
    review_by: codex
    
  parallel_implementation:
    agents: [codex, claude-sonnet, minimax]
    selection: best_of_three
    
  code_review:
    agents: [claude-opus, codex]
    mode: consensus
```

## 📊 代理能力矩阵

| 任务类型 | Kimi K2.5 | Codex 5.3 | Claude Opus 4.6 | MiniMax M2.5 | GLM-5 | Gemini 3.1 Pro |
|----------|-----------|-----------|-----------------|--------------|-------|----------------|
| 架构设计 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 快速编码 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 代码重构 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 调试排错 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Agent 集群 | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| 长上下文 | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 多模态 | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| 性价比 | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |

## 🚨 故障排除

| 问题 | 解决方案 |
|------|----------|
| 代理超时 | 增加 timeout 配置，或启用 fallback |
| 结果不一致 | 使用 review 模式让多个代理投票 |
| 上下文过长 | 使用 Gemini 或启用上下文压缩 |
| API 限制 | 启用本地缓存，或使用国产模型 |
| 国内访问慢 | 使用 Kimi、MiniMax、GLM 等国产模型 |

## 📚 参考资料

- [resources.md](references/resources.md) - 各代理 API 文档和最新模型信息
- [templates/](templates/) - 示例配置和脚本

### 模型发布信息

- **GPT-5.3-Codex**: https://openai.com/index/introducing-gpt-5-3-codex/
- **Claude 4.6**: https://docs.anthropic.com/
- **Kimi K2.5**: https://www.kimi.com/blog/kimi-k2-5.html
- **MiniMax M2.5**: https://minimaxi.com/news/minimax-m25
- **GLM-5**: https://z.ai/blog/glm-5

---

*Many agents, one goal: ship great code.* 🚀
