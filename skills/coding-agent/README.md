# Coding Agent Orchestrator

多模型 AI 编程代理协调器

## 功能

- 🤖 支持 Kimi、Codex、Claude、Gemini、OpenCode 等代理
- 🔄 多代理协作模式（主控、并行、竞技场）
- 🎯 智能代理选择
- 🔍 跨模型代码审查

## 快速开始

```bash
# 验证环境
python scripts/verify_env.py

# 初始化配置
python scripts/configure.py --init

# 配置代理
export CODEX_API_KEY="your-key"
export ANTHROPIC_API_KEY="your-key"
export GEMINI_API_KEY="your-key"

# 运行单代理任务
python scripts/orchestrate.py --mode single --agent codex --task "实现快速排序"

# 运行多代理竞技场
python scripts/orchestrate.py --mode arena --task "优化算法" --agents codex,claude,gemini

# 代码审查
python scripts/orchestrate.py --mode review --file code.py --agents codex,claude
```

## 使用模式

| 模式 | 描述 | 示例 |
|------|------|------|
| `single` | 单代理执行 | `--mode single --agent codex` |
| `parallel` | 并行执行 | `--mode parallel --agents codex,claude` |
| `arena` | 代理竞争 | `--mode arena --agents codex,claude,gemini` |
| `review` | 代码审查 | `--mode review --file code.py` |

## 代理选择

```bash
# 智能选择代理
python scripts/agent_selector.py "重构代码" --explain

# 选择多个代理
python scripts/agent_selector.py "实现API" --multiple 3
```

## 配置

编辑 `agents.yaml`:

```yaml
agents:
  codex:
    type: openai
    model: codex-latest
    api_key: ${CODEX_API_KEY}
    
  claude:
    type: anthropic
    model: claude-sonnet-4-20250514
    api_key: ${ANTHROPIC_API_KEY}
```

## 参考

- [resources.md](references/resources.md) - API 文档和资源
