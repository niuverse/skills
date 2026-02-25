#!/usr/bin/env python3
"""
论文总结生成工具
支持多种风格：学术、故事、简洁
"""

import argparse
import os
import sys
from pathlib import Path
from typing import List, Optional


class PaperSummarizer:
    """论文总结器"""
    
    STYLES = ["academic", "storytelling", "concise", "bullet"]
    
    def __init__(self, style: str = "academic"):
        """
        初始化总结器
        
        Args:
            style: 总结风格 (academic|storytelling|concise|bullet)
        """
        if style not in self.STYLES:
            raise ValueError(f"不支持的风格: {style}. 可选: {self.STYLES}")
        
        self.style = style
    
    def summarize(self, pdf_path: str, embed_images: bool = False) -> "SummaryResult":
        """
        生成论文总结
        
        Args:
            pdf_path: PDF 文件路径
            embed_images: 是否嵌入图像
            
        Returns:
            SummaryResult: 总结结果
        """
        from parse_paper import PaperParser
        
        # 解析论文
        parser = PaperParser()
        content = parser.parse(pdf_path)
        
        # 根据风格生成总结
        if self.style == "academic":
            summary = self._academic_summary(content)
        elif self.style == "storytelling":
            summary = self._storytelling_summary(content)
        elif self.style == "concise":
            summary = self._concise_summary(content)
        elif self.style == "bullet":
            summary = self._bullet_summary(content)
        
        return SummaryResult(summary, content, embed_images)
    
    def _academic_summary(self, content) -> str:
        """学术风格总结"""
        return f"""# 论文总结 (学术风格)

## 摘要
{content.text[:500]}...

## 核心贡献
- 待补充

## 方法论
{self._extract_methodology(content.text)}

## 实验结果
- 待补充

## 结论
- 待补充

## 公式
""" + "\n".join(f"- `${f}`" for f in content.latex_formulas[:10])
    
    def _storytelling_summary(self, content) -> str:
        """故事风格总结"""
        return f"""# 论文解读 (故事风格)

## 背景故事
{content.text[:300]}...

## 研究动机
科学家们一直在探索...

## 核心突破
这篇论文提出了...

## 实际应用
这项技术可以应用于...

## 展望未来
未来的研究方向包括...
"""
    
    def _concise_summary(self, content) -> str:
        """简洁风格总结"""
        return f"""# 论文速览

**核心思想**: {content.text[:200]}...

**关键公式**: {content.latex_formulas[0] if content.latex_formulas else "N/A"}

**主要贡献**:
1. 待补充
2. 待补充
3. 待补充

**一句话总结**: 待补充
"""
    
    def _bullet_summary(self, content) -> str:
        """ bullet 风格总结"""
        return f"""# 论文要点

- 论文主题: 待补充
- 核心方法: 待补充
- 主要结果: 待补充
- 创新点: 待补充
- 局限性: 待补充
- 相关论文: 待补充

## 关键公式
""" + "\n".join(f"- `${f}`" for f in content.latex_formulas[:5])
    
    def _extract_methodology(self, text: str) -> str:
        """提取方法论部分"""
        # 简单的启发式提取
        keywords = ["method", "approach", "algorithm", "architecture", "model"]
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            if any(kw in line.lower() for kw in keywords):
                return '\n'.join(lines[i:i+5])
        
        return "待补充"


class SummaryResult:
    """总结结果"""
    
    def __init__(self, summary: str, content, embed_images: bool):
        self.summary = summary
        self.content = content
        self.embed_images = embed_images
    
    def save(self, output_path: str):
        """保存总结到文件"""
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        
        # 如果需要嵌入图像，添加图像引用
        content = self.summary
        if self.embed_images and self.content.images:
            content += "\n\n## 图表\n"
            for img in self.content.images[:5]:
                content += f"\n![Figure]({img})\n"
        
        output.write_text(content, encoding='utf-8')
        print(f"✅ 总结已保存: {output}")


def main():
    parser = argparse.ArgumentParser(description="生成论文总结")
    parser.add_argument("pdf_path", help="PDF 文件路径")
    parser.add_argument("--output", "-o", default="./summary.md", help="输出文件路径")
    parser.add_argument("--style", "-s", default="academic",
                       choices=["academic", "storytelling", "concise", "bullet"],
                       help="总结风格")
    parser.add_argument("--embed-images", "-i", action="store_true",
                       help="嵌入图像")
    
    args = parser.parse_args()
    
    try:
        summarizer = PaperSummarizer(style=args.style)
        result = summarizer.summarize(args.pdf_path, embed_images=args.embed_images)
        result.save(args.output)
        
        print(f"\n✅ 总结生成完成!")
        print(f"   风格: {args.style}")
        print(f"   字符数: {len(result.summary)}")
        
    except Exception as e:
        print(f"❌ 错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
