# Coding Agent 资源汇总

## 支持的 AI 代理

### OpenAI / Codex
- **文档**: https://platform.openai.com/docs
- **模型**: 
  - `5.3-codex` (最新)
  - `5.0-codex`
  - `codex-latest`
- **API**: https://api.openai.com/v1
- **CLI**: https://github.com/openai/codex

### Anthropic / Claude Code
- **文档**: https://docs.anthropic.com/
- **模型**:
  - `claude-opus-4.6` (最强推理)
  - `claude-sonnet-4.6` (平衡性能)
  - `claude-haiku-4.6` (快速响应)
- **API**: https://api.anthropic.com/v1
- **CLI**: https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview

### Google / Gemini
- **文档**: https://ai.google.dev/
- **模型**:
  - `gemini-2.5-pro` (最新)
  - `gemini-2.5-flash` (快速)
  - `gemini-2.0-pro`
- **API**: https://generativelanguage.googleapis.com

### 本地模型 / OpenCode
- **GitHub**: https://github.com/opencode-ai/opencode
- **特点**: 本地部署，隐私保护
- **端点**: http://localhost:8080/v1/completions

### Kimi (Moonshot AI)
- **文档**: https://platform.moonshot.cn/docs
- **模型**:
  - `kimi-k2.5` (最新)
  - `kimi-k2`
- **API**: https://api.moonshot.cn/v1

## 相关项目

### Aider
- **GitHub**: https://github.com/Aider-AI/aider
- **描述**: AI 辅助编程工具，支持多模型

### Continue
- **GitHub**: https://github.com/continuedev/continue
- **描述**: IDE 插件，支持多代理切换

### MetaGPT
- **GitHub**: https://github.com/geekan/MetaGPT
- **描述**: 多代理协作框架

### AutoGen
- **GitHub**: https://github.com/microsoft/autogen
- **描述**: 微软多代理对话框架

### CrewAI
- **GitHub**: https://github.com/crewAIInc/crewAI
- **描述**: 多代理编排框架

## 最佳实践

1. **任务分解**: 将大任务拆分为小任务分配给不同代理
2. **结果验证**: 使用多个代理交叉验证结果
3. **故障转移**: 配置 fallback 代理应对 API 限制
4. **成本控制**: 简单任务使用便宜模型，复杂任务使用强模型
5. **模型选择**: 
   - 快速原型: Codex / Claude Sonnet
   - 深度重构: Claude Opus
   - 长文档处理: Gemini / Kimi
   - 隐私敏感: OpenCode (本地)
