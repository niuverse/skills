---
name: paper-reading
description: |
  Academic paper reading and analysis expert. Specializes in:
  - PDF parsing with image and formula extraction
  - LaTeX formula recognition and conversion
  - Paper summarization with embedded figures
  - ArXiv paper fetching and analysis
  - Multi-format output (markdown, structured JSON)
  - Research paper tracking and organization
  
  Triggers: paper reading, PDF parsing, arxiv, academic paper, 
  formula extraction, LaTeX, research summary, paper analysis,
  mineru, attention is all you need, transformer, deep learning paper
---

# Paper Reading Expert

📚 学术论文阅读与分析专家 - 支持图像、公式、表格提取

## 🎯 核心能力

| 功能 | 描述 |
|------|------|
| **PDF 解析** | 提取文本、图像、表格、公式 |
| **LaTeX 公式** | 识别并转换数学公式为 LaTeX |
| **图像嵌入** | 在总结中嵌入论文图表 |
| **ArXiv 集成** | 直接获取和分析 ArXiv 论文 |
| **多格式输出** | Markdown、JSON、结构化数据 |
| **研究跟踪** | 论文收藏、分类、笔记管理 |

## 🚀 快速开始

### 1. 环境验证
```bash
python scripts/verify_env.py
```

### 2. 解析本地 PDF
```bash
python scripts/parse_paper.py <pdf_path> --output-dir ./output
```

### 3. 获取 ArXiv 论文
```bash
python scripts/fetch_arxiv.py <arxiv_id> --analyze
```

### 4. 生成论文总结
```bash
python scripts/summarize.py <pdf_path> --style academic --embed-images
```

## 📖 使用指南

### 解析 PDF 论文

```python
from scripts.parse_paper import PaperParser

parser = PaperParser()
result = parser.parse("paper.pdf")

# 获取结构化内容
print(result.text)           # 纯文本
print(result.markdown)       # Markdown 格式
print(result.latex_formulas) # LaTeX 公式列表
print(result.images)         # 提取的图像路径
print(result.tables)         # 表格数据
```

### 分析 ArXiv 论文

```python
from scripts.fetch_arxiv import ArxivFetcher

fetcher = ArxivFetcher()
paper = fetcher.fetch("1706.03762")  # Attention Is All You Need

# 获取分析
analysis = paper.analyze()
print(analysis.summary)
print(analysis.key_contributions)
print(analysis.methodology)
```

### 生成视觉化总结

```python
from scripts.summarize import PaperSummarizer

summarizer = PaperSummarizer(style="academic")  # academic | storytelling | concise
summary = summarizer.summarize("paper.pdf", embed_images=True)

# 保存为 Markdown
summary.save("summary.md")
```

## 🛠️ 工具对比

| 工具 | 图像 | LaTeX 公式 | 速度 | 推荐指数 |
|------|------|------------|------|----------|
| **MinerU** | ✅ | ✅ | 中 | ⭐⭐⭐⭐⭐ |
| **PyMuPDF** | ✅ | ❌ | 快 | ⭐⭐⭐⭐ |
| **PDFPlumber** | ⚠️ | ❌ | 中 | ⭐⭐⭐ |
| **MarkItDown** | ❌ | ❌ | 快 | ⭐⭐⭐ |

## 📁 工作流推荐

### 完整论文分析流程

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  PDF /      │───▶│   MinerU    │───▶│  Markdown   │
│  ArXiv ID   │    │   Parser    │    │  + Images   │
└─────────────┘    └─────────────┘    └──────┬──────┘
                                              │
                                              ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Visual    │◀───│  Summarize  │◀───│  Analysis   │
│   Output    │    │   (LLM)     │    │  (Structure)│
└─────────────┘    └─────────────┘    └─────────────┘
```

## 🔧 配置

### MinerU Token (推荐)
```bash
export MINERU_TOKEN="your_token_here"
```

### 代理设置 (中国大陆)
```bash
export ARXIV_MIRROR="https://xxx.arxiv.org"
```

## 📚 参考资料

- [resources.md](references/resources.md) - 相关工具和库
- [comparison.md](references/comparison.md) - 详细工具对比
- [latex-guide.md](references/latex-guide.md) - LaTeX 公式处理指南

## 📝 示例

### 输入: Attention Is All You Need

```bash
python scripts/fetch_arxiv.py 1706.03762 --analyze --summarize
```

### 输出: 结构化分析

```markdown
# Attention Is All You Need

## 核心贡献
- 提出 Transformer 架构，完全基于注意力机制
- 摒弃 RNN/CNN，实现并行化训练
- 在机器翻译任务上达到 SOTA

## 关键创新
### Multi-Head Attention
```latex
\text{Attention}(Q,K,V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V
```

### 架构图
![Transformer Architecture](extracted_images/fig1.png)

## 实验结果
- WMT 2014 英德翻译: BLEU 28.4 (SOTA)
- 训练时间: 12 小时 (8 P100)
```

## 🙏 致谢

- [MinerU](https://github.com/opendatalab/MinerU) - 优秀的 PDF 解析工具
- [Paper Craft Skills](https://github.com/zsyggg/paper-craft-skills) - 论文分析灵感
- [ArXiv](https://arxiv.org/) - 开放获取的学术论文平台

---

*Read papers, extract knowledge, advance science.* 🔬
