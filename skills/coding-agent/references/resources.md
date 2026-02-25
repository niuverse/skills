# Coding Agent 资源汇总

## 国际模型

### OpenAI / GPT-5.3-Codex
- **文档**: https://platform.openai.com/docs
- **模型**: 
  - `gpt-5.3-codex` (最新，2026-02 发布)
  - `gpt-5.2-codex`
- **API**: https://api.openai.com/v1
- **发布说明**: https://openai.com/index/introducing-gpt-5-3-codex/
- **特点**: 目前最强大的 agentic 编程模型，支持低/中/高/xhigh 推理强度

### Anthropic / Claude Code
- **文档**: https://docs.anthropic.com/
- **模型**:
  - `claude-opus-4.6` (最强推理，2026-02 发布)
  - `claude-sonnet-4.6` (平衡性能)
  - `claude-haiku-4.6` (快速响应)
- **API**: https://api.anthropic.com/v1
- **CLI**: https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview

### Google / Gemini
- **文档**: https://ai.google.dev/
- **模型**:
  - `gemini-2.5-pro` (最新)
  - `gemini-2.5-flash` (快速)
- **API**: https://generativelanguage.googleapis.com

## 国产模型

### Moonshot / Kimi
- **文档**: https://platform.moonshot.cn/docs
- **模型**:
  - `kimi-k2.5` (最新，支持 Agent Swarm)
  - `kimi-k2`
- **API**: https://api.moonshot.cn/v1
- **发布说明**: https://www.kimi.com/blog/kimi-k2-5.html
- **特点**: Agent Swarm 技术，支持多达 100 个子智能体并行协作

### MiniMax
- **文档**: https://www.minimaxi.com/
- **模型**:
  - `minimax-m2.5` (最新，2026-02 发布)
- **API**: https://api.minimaxi.com/v1
- **发布说明**: https://minimaxi.com/news/minimax-m25
- **特点**: 架构师级编程能力，性价比极高 (1 美元/小时连续工作)

### Zhipu / 智谱 AI
- **文档**: https://open.bigmodel.cn/
- **模型**:
  - `glm-5` (最新，744B 参数)
  - `glm-4.7`
- **API**: https://open.bigmodel.cn/api/paas/v4
- **发布说明**: https://z.ai/blog/glm-5
- **特点**: 开源，编程与智能体能力均衡

## 本地模型

### OpenCode
- **GitHub**: https://github.com/opencode-ai/opencode
- **特点**: 本地部署，隐私保护
- **端点**: http://localhost:8080/v1/completions

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

## 模型性能对比 (2026-02)

| 模型 | SWE-Bench | HLE | 特点 |
|------|-----------|-----|------|
| Claude Opus 4.6 | 80.9% | 43.4 | 综合能力最强 |
| GPT-5.3-Codex | 80.0% | 45.5 | 编程专用最强 |
| MiniMax M2.5 | 80.2% | - | 性价比最高 |
| GLM-5 | 77.8% | 50.4 | 开源最强 |
| Kimi K2.5 | 76.8% | 50.2 | Agent 集群 |

## 最佳实践

1. **任务分解**: 将大任务拆分为小任务分配给不同代理
2. **结果验证**: 使用多个代理交叉验证结果
3. **故障转移**: 配置 fallback 代理应对 API 限制
4. **成本控制**: 
   - 简单任务: MiniMax (最便宜)
   - 复杂任务: Claude Opus / GPT-5.3-Codex
   - 国内访问: Kimi / MiniMax / GLM
5. **模型选择**:
   - 快速原型: Codex / MiniMax
   - 深度重构: Claude Opus
   - Agent 集群: Kimi K2.5
   - 长文档处理: Gemini / Kimi
   - 隐私敏感: OpenCode (本地)
   - 开源方案: GLM-5
