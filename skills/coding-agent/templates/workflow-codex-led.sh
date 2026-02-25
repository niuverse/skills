#!/bin/bash
# 示例：Codex 主控 + 多 Claude 并行开发

set -e

echo "🚀 启动 Codex 主控并行开发"
echo "=========================="

TASK="重构一个遗留代码库"
echo "任务: $TASK"

# 1. Codex 分析并拆分任务
echo "🤖 Codex 分析任务并拆分..."
python scripts/orchestrate.py \
    --mode single \
    --agent codex \
    --task "分析 $TASK，拆分为 3 个并行子任务" \
    --output subtasks.md

# 2. 并行执行子任务
echo "🤖 并行执行子任务..."

# 启动 3 个 Claude 实例并行工作
python scripts/orchestrate.py \
    --mode parallel \
    --agents claude,claude,claude \
    --task "执行子任务" \
    --context subtasks.md

# 3. Codex 整合结果
echo "🤖 Codex 整合结果..."
python scripts/orchestrate.py \
    --mode single \
    --agent codex \
    --task "整合各子任务结果，确保一致性" \
    --output final_result.py

echo ""
echo "✅ 并行开发完成!"
