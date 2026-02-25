# Paper Reading Skill

学术论文阅读与分析工具集

## 功能

- 📄 PDF 解析（文本、图像、表格、公式）
- 🧮 LaTeX 公式识别
- 📚 ArXiv 论文获取
- 📝 多风格总结生成

## 快速开始

```bash
# 验证环境
python scripts/verify_env.py

# 解析 PDF
python scripts/parse_paper.py paper.pdf -o ./output

# 获取 ArXiv 论文
python scripts/fetch_arxiv.py 1706.03762 --analyze --summarize

# 生成总结
python scripts/summarize.py paper.pdf -o summary.md --style academic
```

## 安装依赖

```bash
# 基础依赖
pip install pymupdf requests

# 完整依赖
pip install pymupdf pdfplumber arxiv markitdown
```

## 工具对比

| 工具 | 图像 | LaTeX | 速度 | 推荐 |
|------|------|-------|------|------|
| MinerU | ✅ | ✅ | 中 | ⭐⭐⭐⭐⭐ |
| PyMuPDF | ✅ | ❌ | 快 | ⭐⭐⭐⭐ |
| PDFPlumber | ⚠️ | ❌ | 中 | ⭐⭐⭐ |

## 参考

- [resources.md](references/resources.md) - 相关资源
