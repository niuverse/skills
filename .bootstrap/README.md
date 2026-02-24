# Skill Bootstrap 机制

自动化 Skill 进化系统 —— 让 skills 在使用中不断自我完善。

## 核心概念

**Bootstrap** = 使用驱动的进化

传统的文档更新是「计划式」的：先规划，再编写。
Bootstrap 机制是「响应式」的：在使用中发现缺口，自动记录，定期完善。

## 工作原理

```
用户使用 Skill
    ↓
运行时监控检测缺口
    ↓
自动记录到 pending/
    ↓
定期运行 Auto-Enhancer
    ↓
自动更新 SKILL.md
    ↓
生成 PR 或直接提交
```

## 目录结构

```
.bootstrap/
├── bootstrap_engine.py      # 核心引擎
├── runtime_monitor.py       # 运行时监控
├── auto_enhancer.py         # 自动增强器
├── pending/                 # 待处理缺口
│   └── {skill}_{gap_id}.json
└── resolved/                # 已解决缺口
    └── {skill}_{gap_id}.json
```

## 缺口类型

| 类型 | 说明 | 自动处理 |
|------|------|----------|
| `missing_example` | 缺少示例 | ✅ 添加示例章节 |
| `unclear_description` | 描述不清 | ✅ 补充使用场景 |
| `missing_param` | 缺少参数说明 | ✅ 添加参数章节 |
| `edge_case` | 边界情况未覆盖 | ✅ 添加边界处理章节 |
| `performance` | 性能优化建议 | ⚠️ 手动处理 |
| `security` | 安全问题 | ⚠️ 手动处理 |

## 手动使用

### 记录缺口

```bash
python .bootstrap/bootstrap_engine.py record-gap \
  --skill robot-sim-expert \
  --type missing_example \
  --context "用户询问如何处理 Isaac Lab 的内存不足问题" \
  --suggestion "添加 GPU 内存优化的具体示例"
```

### 查看待处理缺口

```bash
python .bootstrap/bootstrap_engine.py list-gaps
python .bootstrap/bootstrap_engine.py list-gaps --skill robot-sim-expert
```

### 分析 Skill 覆盖度

```bash
python .bootstrap/bootstrap_engine.py analyze \
  --skill robot-sim-expert \
  --context "How to train quadruped with RL?"
```

### 手动触发增强

```bash
# 预览变更
python .bootstrap/auto_enhancer.py --skill robot-sim-expert --dry-run

# 应用变更
python .bootstrap/auto_enhancer.py --skill robot-sim-expert

# 增强所有 skills
python .bootstrap/auto_enhancer.py --all
```

## CI/CD 集成

自动运行（每天凌晨 2 点）：
- 检查 pending/ 中的缺口
- 自动生成增强内容
- 创建 Pull Request

手动触发：
- 访问 Actions → Auto Bootstrap CI
- 选择 "Run workflow"
- 可指定特定 skill 或全部

## 与 OpenClaw 集成

在 OpenClaw 中使用 skills 时，自动触发监控：

```python
from .bootstrap.runtime_monitor import skill_invoked, skill_responded

# 调用 skill 前
result = skill_invoked("robot-sim-expert", user_request)

# 调用 skill 后
gap_id = skill_responded("robot-sim-expert", user_request, response, confidence=0.8)
```

## 配置

环境变量：
- `NIUVERSE_SKILLS_ROOT`: skills 仓库根目录

## 工作流程

1. **日常使用**: 使用 skills，系统自动记录缺口
2. **定期审查**: 查看 pending/ 中的缺口
3. **自动增强**: CI 定期运行，生成更新
4. **人工审核**: 审查 PR，确认或调整变更
5. **迭代改进**: 合并后继续下一轮

## 注意事项

- 自动生成的内容需要人工审核
- 敏感变更（安全、架构）标记为 manual
- 定期清理 resolved/ 目录
- 保持 skill 的简洁性，避免过度膨胀
