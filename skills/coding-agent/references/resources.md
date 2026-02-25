# Coding Agent 资源汇总

## 国际模型

### OpenAI / GPT-5.3-Codex
- **官方文档**: https://platform.openai.com/docs
- **API 参考**: https://platform.openai.com/docs/api-reference
- **模型列表**:
  - `gpt-5.3-codex` (最新，2026-02-05 发布)
  - `gpt-5.2-codex`
  - `gpt-5.2` (通用推理)
- **API 端点**: `https://api.openai.com/v1/chat/completions`
- **发布说明**: https://openai.com/index/introducing-gpt-5-3-codex/
- **模型规格**: https://platform.openai.com/docs/models/gpt-5.3-codex
- **定价**: https://openai.com/api/pricing/
- **特点**: 
  - 目前最强大的 agentic 编程模型
  - 支持 reasoning_effort: low/medium/high/xhigh
  - 集成 GPT-5.2 的推理能力与 Codex 的编程专长

### Anthropic / Claude Code
- **官方文档**: https://docs.anthropic.com/en/docs
- **API 参考**: https://docs.anthropic.com/en/api/getting-started
- **模型列表**:
  - `claude-opus-4-20250514` (最强推理)
  - `claude-sonnet-4-20250514` (平衡性能)
  - `claude-haiku-4-20250514` (快速响应)
- **API 端点**: `https://api.anthropic.com/v1/messages`
- **Claude Code CLI**: https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview
- **模型规格**: https://docs.anthropic.com/en/docs/about-claude/models
- **定价**: https://www.anthropic.com/pricing
- **特点**:
  - 200K 上下文窗口
  - 出色的代码理解和重构能力
  - 强大的推理和调试能力

### Google / Gemini
- **官方文档**: https://ai.google.dev/gemini-api/docs
- **API 参考**: https://ai.google.dev/api
- **模型列表**:
  - `gemini-3.1-pro` (最新，2026-02-19 发布)
  - `gemini-3.1-flash` (快速版本)
  - `gemini-3.0-pro`
- **API 端点**: `https://generativelanguage.googleapis.com/v1beta`
- **发布说明**: https://ai.google.dev/gemini-api/docs/changelog
- **Gemini 3.1 Pro 文档**: https://ai.google.dev/gemini-api/docs/gemini-3
- **Vertex AI 文档**: https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models/gemini/3-1-pro
- **模型卡片**: https://deepmind.google/models/model-cards/gemini-3-1-pro/
- **定价**: https://ai.google.dev/pricing
- **特点**:
  - 原生多模态 (文本、图像、音频、视频)
  - 超长上下文 (2M tokens)
  - 强大的推理和代码生成能力

## 国产模型

### Moonshot / Kimi
- **官方文档**: https://platform.moonshot.cn/docs
- **API 参考**: https://platform.moonshot.cn/docs/api-reference
- **模型列表**:
  - `kimi-k2.5` (最新，支持 Agent Swarm)
  - `kimi-k2`
- **API 端点**: `https://api.moonshot.cn/v1`
- **发布说明**: https://www.kimi.com/blog/kimi-k2-5.html
- **定价**: https://platform.moonshot.cn/docs/pricing
- **特点**: 
  - Agent Swarm 技术，支持多达 100 个子智能体并行协作
  - 单次任务支持 1500 次工具调用
  - 原生多模态 (15T 视觉+文本 token 预训练)

### MiniMax
- **官方文档**: https://www.minimaxi.com/
- **API 参考**: https://www.minimaxi.com/platform/document
- **模型列表**:
  - `minimax-m2.5` (最新，2026-02-11 发布)
- **API 端点**: `https://api.minimaxi.com/v1`
- **发布说明**: https://minimaxi.com/news/minimax-m25
- **定价**: https://www.minimaxi.com/platform/price
- **特点**: 
  - 架构师级编程能力，主动进行功能拆解和结构设计
  - 性价比极高 (1 美元/小时连续工作)
  - 处理速度 100 TPS
  - 代码生成占公司内部提交 80%

### Zhipu / 智谱 AI
- **官方文档**: https://open.bigmodel.cn/dev/api
- **API 参考**: https://open.bigmodel.cn/dev/api#glm
- **模型列表**:
  - `glm-5` (最新，744B 参数，2026-02-11 发布)
  - `glm-4.7`
- **API 端点**: `https://open.bigmodel.cn/api/paas/v4`
- **发布说明**: https://z.ai/blog/glm-5
- **模型介绍**: https://www.bigmodel.cn/dev/activities/glm-5
- **定价**: https://open.bigmodel.cn/pricing
- **特点**: 
  - 开源 (MIT 协议)
  - 744B 参数，28.5T 预训练数据
  - SWE-Bench 77.8%，HLE 50.4%
  - 编程与智能体能力均衡

## 本地模型

### OpenCode
- **GitHub**: https://github.com/opencode-ai/opencode
- **文档**: https://github.com/opencode-ai/opencode#readme
- **特点**: 本地部署，隐私保护
- **端点**: `http://localhost:8080/v1/completions`
- **适用场景**: 隐私敏感、离线环境

## 相关项目

### Aider
- **GitHub**: https://github.com/Aider-AI/aider
- **文档**: https://aider.chat/docs/
- **描述**: AI 辅助编程工具，支持多模型

### Continue
- **GitHub**: https://github.com/continuedev/continue
- **文档**: https://docs.continue.dev/
- **描述**: IDE 插件，支持多代理切换

### MetaGPT
- **GitHub**: https://github.com/geekan/MetaGPT
- **文档**: https://docs.deepwisdom.ai/
- **描述**: 多代理协作框架

### AutoGen
- **GitHub**: https://github.com/microsoft/autogen
- **文档**: https://microsoft.github.io/autogen/
- **描述**: 微软多代理对话框架

### CrewAI
- **GitHub**: https://github.com/crewAIInc/crewAI
- **文档**: https://docs.crewai.com/
- **描述**: 多代理编排框架

## 模型性能对比 (2026-02)

| 模型 | SWE-Bench | HLE | 上下文 | 特点 |
|------|-----------|-----|--------|------|
| Claude Opus 4.6 | 80.9% | 43.4 | 200K | 综合能力最强 |
| GPT-5.3-Codex | 80.0% | 45.5 | 128K | 编程专用最强 |
| MiniMax M2.5 | 80.2% | - | 128K | 性价比最高 |
| GLM-5 | 77.8% | 50.4 | 128K | 开源最强 |
| Kimi K2.5 | 76.8% | 50.2 | 256K | Agent 集群 |
| Gemini 3.1 Pro | 76.2% | 45.8 | 2M | 多模态最强 |

## 选择指南

### 按任务类型
- **快速原型**: Codex / MiniMax
- **深度重构**: Claude Opus
- **Agent 集群**: Kimi K2.5
- **长文档处理**: Gemini 3.1 Pro (2M 上下文)
- **多模态**: Gemini 3.1 Pro
- **隐私敏感**: OpenCode (本地)
- **开源方案**: GLM-5

### 按成本
- **最便宜**: MiniMax (1 美元/小时)
- **性价比**: GLM-5 / Kimi
- **高性能**: Claude Opus / GPT-5.3-Codex

### 按国内访问
- **首选**: Kimi / MiniMax / GLM (国内服务器)
- **备选**: 国际模型 + 代理
