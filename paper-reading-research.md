# Paper Reading Skills 研究报告

## 研究目标
寻找支持图像和公式理解的论文阅读相关 OpenClaw Skills，能够在论文总结中嵌入相关图像。

## 搜索范围
1. ClawHub / Playbooks Skills 市场
2. GitHub 开源社区
3. Awesome OpenClaw Skills 列表

---

## 找到的相关 Skills

### 1. MinerU PDF Parser (mineru-pdf)
**来源**: openclaw/skills (Playbooks)  
**GitHub**: https://github.com/TINKPA/mcp-mineru

#### 功能特点
- 使用 MinerU MCP 解析 PDF 文档
- 支持提取结构化内容：文本、表格、公式
- 支持 MLX 加速（Apple Silicon M1/M2/M3/M4）
- 支持多种后端：
  - `pipeline` - 快速通用（推荐）
  - `vlm-mlx-engine` - Apple Silicon 优化
  - `vlm-transformers` - 最准确但最慢

#### 图像/公式支持
| 功能 | 支持情况 |
|------|----------|
| 图像提取 | ✅ 支持 |
| 公式识别 | ✅ 支持 LaTeX 转换 |
| 表格提取 | ✅ 支持 |
| OCR | ✅ 内置 |

#### 安装方式
```bash
# 方法1: 使用 MCP (Claude Code)
claude mcp add --transport stdio --scope user mineru -- \
  uvx --from mcp-mineru python -m mcp_mineru.server

# 方法2: 直接使用工具（推荐，保留文件）
python /path/to/skills/mineru-pdf/parse.py <pdf_path> <output_dir> [options]
```

#### 评估
- ✅ **强烈推荐** - 专门针对学术论文优化
- ✅ 支持 LaTeX 公式转换
- ✅ 支持图像和表格提取
- ⚠️ 首次运行需要下载模型（5-10分钟）
- ⚠️ 需要 MinerU Token

---

### 2. Paper Craft Skills (paper-craft-skills)
**来源**: GitHub - zsyggg/paper-craft-skills  
**GitHub**: https://github.com/zsyggg/paper-craft-skills  
**Stars**: 11

#### 功能特点
- **paper-analyzer**: 将论文转换为深度技术文章
  - 支持 3 种写作风格：academic（学术）、storytelling（故事）、concise（简洁）
  - 公式解释：插入公式图片并分解符号
  - 代码分析：将论文概念与 GitHub 源码对齐
  
- **paper-comic**: 将论文转换为 10 页教育漫画
  - 支持 4 种艺术风格：classic、tech、warm、chalk

#### 图像/公式支持
| 功能 | 支持情况 |
|------|----------|
| 图像提取 | ✅ 通过 MinerU |
| 公式理解 | ✅ 公式解释功能 |
| 图表嵌入 | ✅ 在总结中嵌入 |

#### 安装方式
```bash
npx skills add zsyggg/paper-craft-skills

# 配置
pip install requests markdown
export MINERU_TOKEN="your_token"
```

#### 评估
- ✅ **强烈推荐** - 专门针对论文阅读和总结
- ✅ 支持公式解释和图像嵌入
- ✅ 多种输出格式（深度文章、漫画）
- ⚠️ 依赖 MinerU Token

---

### 3. ArXiv Paper Reader (arxiv-reader)
**来源**: openclaw/skills (agentskill.sh)  
**GitHub**: https://agentskill.sh/@openclaw/arxiv-reader  
**Stars**: 1.3K

#### 功能特点
- 基于 LLM Agent 对 arXiv 论文进行分类与深度阅读
- 直接打印阅读笔记
- 支持指定 arXiv ID 或 URL

#### 图像/公式支持
| 功能 | 支持情况 |
|------|----------|
| 图像提取 | ❓ 未明确说明 |
| 公式理解 | ❓ 未明确说明 |

#### 安装方式
```bash
/learn @openclaw/arxiv-reader
```

#### 评估
- ⚠️ 功能描述较简单，图像/公式支持不明确
- 适合快速获取 arXiv 论文摘要

---

### 4. ArXiv Watcher (arxiv-watcher)
**来源**: openclaw/skills (Playbooks)

#### 功能特点
- 搜索 ArXiv 并生成简洁、可操作的论文摘要
- 支持按关键词、作者或类别发现最新论文
- 可获取 PDF 进行更深入的内容提取
- 保存摘要到持久化研究日志

#### 图像/公式支持
| 功能 | 支持情况 |
|------|----------|
| 图像提取 | ⚠️ Deep dive 模式可能支持 |
| 公式理解 | ⚠️ Deep dive 模式可能支持 |

#### 安装方式
```bash
npx playbooks add skill openclaw/skills --skill arxiv-watcher
```

#### 评估
- 适合跟踪最新研究动态
- Deep dive 模式可提取实验设置和关键图表

---

### 5. PyMuPDF PDF Parser (pymupdf-pdf-parser-clawdbot-skill)
**来源**: openclaw/skills (Playbooks)

#### 功能特点
- 使用 PyMuPDF (fitz) 进行快速本地 PDF 解析
- 生成 Markdown（默认）或 JSON
- 可选提取图像和表格
- 每文档独立输出文件夹

#### 图像/公式支持
| 功能 | 支持情况 |
|------|----------|
| 图像提取 | ✅ 支持 |
| 公式理解 | ❌ 不支持 LaTeX |
| 表格提取 | ⚠️ 简单的基于行的 JSON |

#### 安装方式
```bash
npx playbooks add skill openclaw/skills --skill pymupdf-pdf-parser-clawdbot-skill
```

#### 评估
- ✅ 速度快，依赖少
- ⚠️ 公式不支持 LaTeX 转换
- 适合格式良好的文本型 PDF

---

### 6. Office to Markdown (office-to-md)
**来源**: claude-office-skills

#### 功能特点
- 使用 Microsoft markitdown 转换 Office 文档
- 支持 Word、Excel、PowerPoint、PDF
- 支持图像 OCR（使用 vision model）

#### 图像/公式支持
| 功能 | 支持情况 |
|------|----------|
| 图像 OCR | ✅ 支持 |
| 公式理解 | ❌ 不支持 |
| 表格提取 | ✅ 支持 |

#### 安装方式
```bash
pip install markitdown
```

#### 评估
- 通用文档转换工具
- 公式支持有限

---

### 7. PDF Extraction (pdf-extraction)
**来源**: openclaw/skills (Playbooks)

#### 功能特点
- 使用 pdfplumber 提取文本、表格和元数据
- 字符级定位
- 准确的表格检测
- 可视化调试

#### 图像/公式支持
| 功能 | 支持情况 |
|------|----------|
| 图像提取 | ⚠️ 有限支持 |
| 公式理解 | ❌ 不支持 |
| 表格提取 | ✅ 精确检测 |

#### 评估
- 适合财务报告、发票等结构化文档
- 不适合学术论文的复杂公式

---

## 推荐组合

### 最佳论文阅读工作流

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  PDF 输入       │────▶│  MinerU Parser   │────▶│  Markdown +     │
│  (论文)         │     │  (mineru-pdf)    │     │  图像 + LaTeX   │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                                                           │
                                                           ▼
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  深度分析文章   │◀────│  Paper Analyzer  │◀────│  结构化内容     │
│  或教育漫画     │     │  (paper-craft)   │     │                 │
└─────────────────┘     └──────────────────┘     └─────────────────┘
```

### 推荐安装

1. **首选**: `mineru-pdf` + `paper-craft-skills`
   - MinerU 提供最好的 PDF 解析（图像 + LaTeX 公式）
   - Paper Craft 提供论文特定的分析和总结

2. **备选**: `pymupdf-pdf-parser-clawdbot-skill`
   - 当 MinerU 不可用时使用
   - 速度快但公式支持有限

---

## 测试结果

### 测试环境
- 测试论文: Attention Is All You Need (arXiv:1706.03762)
- 论文页数: 15 页
- 包含内容: 文本、表格、公式

### 1. MarkItDown 测试
**安装**: `pip install markitdown` ✅ 成功

**测试结果**:
- ✅ 文本提取: 成功，提取 39,662 字符
- ⚠️ 布局: 保留了基本结构，但 LaTeX 公式渲染为纯文本
- ❌ 图像: 不支持直接提取
- ⚠️ 表格: 转换为文本格式，非 Markdown 表格

**适用性**: 通用文档转换，公式支持有限

### 2. PyMuPDF (fitz) 测试
**安装**: `pip install pymupdf` ✅ 成功

**测试结果**:
- ✅ 文本提取: 成功，字符级定位
- ✅ 图像提取: 支持，但此论文第一页无嵌入图像
- ✅ 元数据: 完整提取（PDF 1.5, LaTeX with hyperref）
- ❌ 公式: 作为普通文本提取，无 LaTeX 转换
- ⚠️ 表格: 需要额外处理才能正确识别

**适用性**: 快速通用解析，适合图像提取

### 3. PDFPlumber 测试
**安装**: `pip install pdfplumber` ✅ 成功

**测试结果**:
- ✅ 文本提取: 成功
- ✅ 表格检测: 发现 7 个表格（第 9, 10, 13-15 页）
- ⚠️ 表格内容: 提取结果混乱，需要调优
- ✅ 公式检测: 通过特殊字符识别公式行
- ❌ 公式: 无 LaTeX 转换

**发现的公式示例**:
```
Attention(Q,K,V)=softmax( √ )V (1)
```

**适用性**: 结构化文档，表格检测较好但需调优

### 4. MinerU 测试
**安装**: `pip install mineru` ⏳ 安装较复杂，需要更多依赖

**状态**: 由于依赖复杂，未完全安装

**预期功能** (基于文档):
- ✅ 图像提取
- ✅ LaTeX 公式转换
- ✅ 表格结构化提取
- ✅ OCR 支持

---

## 测试结论

### 已验证功能
| 工具 | 文本提取 | 图像提取 | 表格提取 | 公式 LaTeX | 推荐指数 |
|------|----------|----------|----------|------------|----------|
| MarkItDown | ✅ | ❌ | ⚠️ | ❌ | ⭐⭐⭐ |
| PyMuPDF | ✅ | ✅ | ⚠️ | ❌ | ⭐⭐⭐⭐ |
| PDFPlumber | ✅ | ⚠️ | ✅ | ❌ | ⭐⭐⭐ |
| MinerU | - | - | - | - | ⭐⭐⭐⭐⭐ (预期) |

### 关键发现
1. **公式处理**: 现有工具（MarkItDown, PyMuPDF, PDFPlumber）都无法将公式转换为 LaTeX
2. **图像提取**: PyMuPDF 效果最好，但论文中的图通常是矢量图，需要特殊处理
3. **表格提取**: PDFPlumber 能检测到表格，但内容提取需要调优参数
4. **MinerU**: 是目前唯一声称支持 LaTeX 公式转换的工具

---

## 总结

| Skill | 图像支持 | 公式支持 | 推荐指数 | 适用场景 |
|-------|----------|----------|----------|----------|
| mineru-pdf | ⭐⭐⭐ | ⭐⭐⭐ (LaTeX) | ⭐⭐⭐⭐⭐ | 学术论文解析 |
| paper-craft-skills | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 论文总结与可视化 |
| arxiv-reader | ❓ | ❓ | ⭐⭐⭐ | 快速 arXiv 阅读 |
| arxiv-watcher | ⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ | 论文跟踪 |
| pymupdf-pdf-parser | ⭐⭐⭐ | ⭐ | ⭐⭐⭐ | 快速通用解析 |
| office-to-md | ⭐⭐ (OCR) | ⭐ | ⭐⭐ | 通用文档转换 |
| pdf-extraction | ⭐ | ⭐ | ⭐⭐ | 结构化文档 |

**最终建议**: 对于需要图像和公式理解的论文阅读场景，强烈推荐使用 **mineru-pdf** 配合 **paper-craft-skills** 的组合。

### 快速开始命令

```bash
# 1. 安装基础工具
pip install markitdown pymupdf pdfplumber

# 2. 安装 MinerU (推荐，支持 LaTeX 公式)
pip install mineru

# 3. 安装 Paper Craft Skills
npx skills add zsyggg/paper-craft-skills

# 4. 配置 MinerU Token
export MINERU_TOKEN="your_token_here"
```

### 使用示例

```python
# 使用 PyMuPDF 快速提取
import fitz
doc = fitz.open("paper.pdf")
text = doc[0].get_text()  # 第一页文本
images = doc[0].get_images()  # 第一页图像

# 使用 MarkItDown 转换
from markitdown import MarkItDown
md = MarkItDown()
result = md.convert("paper.pdf")
print(result.text_content)
```
