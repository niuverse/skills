#!/bin/bash
# 示例：Kimi 主控 + Codex/Claude 协作开发

set -e

echo "🚀 启动多代理协作开发流程"
echo "=========================="

# 1. 验证环境
echo "📋 步骤 1: 验证环境"
python scripts/verify_env.py

# 2. 初始化配置（如果不存在）
if [ ! -f "agents.yaml" ]; then
    echo "📋 步骤 2: 初始化配置"
    python scripts/configure.py --init
    echo "⚠️  请编辑 agents.yaml 设置 API 密钥"
    exit 1
fi

# 3. 分析任务并选择代理
echo "📋 步骤 3: 分析任务"
TASK="实现一个 REST API 服务器"
echo "任务: $TASK"

SELECTED=$(python scripts/agent_selector.py "$TASK" --explain)
echo "$SELECTED"

# 4. 执行开发任务
echo "📋 步骤 4: 执行开发"

# 4.1 Kimi 设计架构
echo "🤖 Kimi 设计架构..."
python scripts/orchestrate.py \
    --mode single \
    --agent gpt4 \
    --task "设计 $TASK 的架构，包括路由、模型、控制器" \
    --output architecture.md

# 4.2 Codex 快速实现
echo "🤖 Codex 实现核心代码..."
python scripts/orchestrate.py \
    --mode single \
    --agent codex \
    --task "根据架构实现 $TASK" \
    --context architecture.md \
    --output implementation.py

# 4.3 Claude 优化重构
echo "🤖 Claude 优化代码..."
python scripts/orchestrate.py \
    --mode single \
    --agent claude \
    --task "优化代码性能和可读性，添加错误处理" \
    --context implementation.py \
    --output optimized.py

# 4.4 多代理代码审查
echo "🤖 多代理代码审查..."
python scripts/orchestrate.py \
    --mode review \
    --agents codex,claude \
    --file optimized.py \
    --output review.md

echo ""
echo "✅ 协作开发完成!"
echo "输出文件:"
echo "  - architecture.md (架构设计)"
echo "  - implementation.py (初始实现)"
echo "  - optimized.py (优化后代码)"
echo "  - review.md (代码审查)"
