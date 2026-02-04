# Code Style Skills - Design Summary

## 调研结果

### 市面上现有工具分析

#### 1. 代码风格分析工具

| 工具 | 语言 | 功能 | 局限性 |
|------|------|------|--------|
| **EditorConfig** | 通用 | 定义缩进、换行等基本格式 | 只检测，不分析模式 |
| **Prettier** | JS/TS/CSS/HTML | 格式化，有playground查看效果 | 无自定义风格提取 |
| **Black** | Python | 强制PEP 8风格 | 不可配置，无法模仿现有风格 |
| **yapf** | Python | 可配置格式化 | 无风格分析功能 |
| **clang-format** | C/C++ | 可配置格式化 | 无风格提取功能 |
| **ESLint** | JS/TS | 可配置规则检测 | 需要手动配置规则 |
| **RuboCop** | Ruby | 风格检测+格式化 | 仅限Ruby |

#### 2. 发现的市场空白

**没有一个工具能够：**
1. 自动分析现有代码库的风格模式
2. 生成描述性的风格报告
3. 基于分析结果生成格式化配置
4. 跨语言统一工具链

### 对标产品研究

#### Google 内部工具
- **Rosie**: 大规模代码变更工具（闭源）
- **clang-format**: 开源，格式化能力强大
- **google-java-format**: Java专用格式化

#### GitHub 生态
- **Prettier**: 前端生态标准
- **Black**: Python 生态标准
- **Super-linter**: GitHub 的多语言 linting action

## 设计决策

### Skill 1: Code Style Imitator

**核心设计理念：学习而非强制**

```
现有代码库 → 分析提取 → 风格报告 → 应用到新代码
```

**技术方案：**
- AST解析（Python）提取准确的命名和结构信息
- 正则表达式（C++等）轻量级分析
- 统计聚合，识别主导风格
- JSON报告格式，便于程序化使用

**创新点：**
1. **渐进式分析**：单文件 → 项目级 → 跨项目对比
2. **置信度评分**：每个检测到的模式都有置信度
3. **多语言支持**：统一接口，语言特定实现

### Skill 2: Code Style Unifier

**核心设计理念：标准化与自动化**

```
杂乱代码库 → Google Style → 统一、专业的代码
```

**技术方案：**
- 包装现有格式化工具（yapf, clang-format等）
- 预设Google Style配置
- 项目级批量处理
- CI/CD 集成支持

**创新点：**
1. **一键标准化**：自动检测语言，应用正确工具
2. **配置生成器**：自动生成所有格式化工具的配置
3. **安全检查**：默认检查模式，需显式 `--apply` 才修改文件

## 与现有 niuverse-skills 的协同

```
┌─────────────────────────────────────────────────────────┐
│                    niuverse-skills                      │
├─────────────────────────────────────────────────────────┤
│  python-architect  →  创建项目                          │
│         ↓                                               │
│  code-style-imitator → 分析/模仿现有项目风格             │
│         ↓                                               │
│  code-style-unifier  → 标准化为Google Style             │
│         ↓                                               │
│  code-simplifier     → 简化过度复杂的代码               │
│         ↓                                               │
│  mkdocs-creator      → 生成文档                         │
└─────────────────────────────────────────────────────────┘
```

## 使用场景

### 场景1：新成员加入团队
```bash
# 1. 分析现有项目风格
python analyze_project.py --path ./legacy-project --output style.json

# 2. 生成风格指南
python generate_guide.py --input style.json --output TEAM_STYLE.md

# 3. 检查新代码是否符合风格
python check_style.py --style style.json --file new_feature.py
```

### 场景2：开源项目准备发布
```bash
# 1. 生成Google Style配置
python generate_config.py --all --output ./

# 2. 格式化整个项目
python format_project.py --path ./src --apply

# 3. 在CI中添加检查
# .github/workflows/style.yml
```

### 场景3：并购后的代码整合
```bash
# 1. 分析两个代码库的风格差异
python analyze_project.py --path ./project-a --output style-a.json
python analyze_project.py --path ./project-b --output style-b.json

# 2. 对比风格
python compare_styles.py style-a.json style-b.json

# 3. 统一到一个标准
python format_project.py --path ./project-b --apply
```

## 实现质量

### 代码风格一致性
- 遵循 niuverse-skills 的 SKILL.md 格式
- 使用相同的 emoji 和表格风格
- 包含完整的 References 和 Scripts 文档

### 技术实现
- Python 3.9+ type hints
- 清晰的函数和类设计
- 完善的错误处理
- 符合 Google Style 的代码本身

### 测试验证
- ✅ 通过 validate_skills.py 验证
- ✅ 脚本可实际运行
- ✅ 生成有效的配置

## 未来扩展方向

### 短期 (1-3个月)
1. 添加更多语言支持（Rust, Kotlin, Swift）
2. 集成到 VS Code 扩展
3. 预提交钩子优化

### 中期 (3-6个月)
1. Web UI 展示风格分析报告
2. 风格演变历史追踪
3. 团队风格差异可视化

### 长期 (6-12个月)
1. ML-based 风格模式识别
2. 自然语言风格描述生成
3. 跨语言风格统一

## 致谢

这两个 skill 参考了以下优秀项目：
- Google Style Guides (风格规范标准)
- yapf / black / prettier (格式化工具)
- EditorConfig (跨编辑器配置)
- OpenClaw Skill Creator (skill 框架)

---

*Design completed: 2026-02-04*
*Author: Niubot for Ziniu*
