#!/usr/bin/env python3
"""
ArXiv 论文获取工具
支持下载、解析、分析 ArXiv 论文
"""

import argparse
import os
import re
import sys
import urllib.request
from pathlib import Path
from typing import Optional


class ArxivFetcher:
    """ArXiv 论文获取器"""
    
    ARXIV_URL = "https://arxiv.org/abs/"
    ARXIV_PDF_URL = "https://arxiv.org/pdf/"
    
    def __init__(self, mirror: Optional[str] = None):
        """
        初始化获取器
        
        Args:
            mirror: ArXiv 镜像地址 (中国大陆用户可能需要)
        """
        self.mirror = mirror
        if mirror:
            self.ARXIV_URL = f"{mirror}/abs/"
            self.ARXIV_PDF_URL = f"{mirror}/pdf/"
    
    def _extract_arxiv_id(self, input_str: str) -> str:
        """从输入字符串中提取 ArXiv ID"""
        # 支持多种格式:
        # 1706.03762
        # arxiv:1706.03762
        # https://arxiv.org/abs/1706.03762
        # https://arxiv.org/pdf/1706.03762.pdf
        
        patterns = [
            r'arxiv[:/]+(\d+\.\d+)',
            r'arxiv\.org/abs/(\d+\.\d+)',
            r'arxiv\.org/pdf/(\d+\.\d+)',
            r'^(\d{4}\.\d{4,5})$'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, input_str, re.IGNORECASE)
            if match:
                return match.group(1)
        
        # 如果输入是纯数字格式，直接返回
        if re.match(r'^\d+\.\d+$', input_str):
            return input_str
        
        raise ValueError(f"无法识别 ArXiv ID: {input_str}")
    
    def fetch(self, arxiv_input: str, output_dir: str = "./papers") -> "ArxivPaper":
        """
        获取 ArXiv 论文
        
        Args:
            arxiv_input: ArXiv ID 或 URL
            output_dir: 输出目录
            
        Returns:
            ArxivPaper: 论文对象
        """
        arxiv_id = self._extract_arxiv_id(arxiv_input)
        
        print(f"📥 获取论文: arXiv:{arxiv_id}")
        
        # 创建输出目录
        out_path = Path(output_dir)
        out_path.mkdir(parents=True, exist_ok=True)
        
        # 下载 PDF
        pdf_url = f"{self.ARXIV_PDF_URL}{arxiv_id}.pdf"
        pdf_path = out_path / f"{arxiv_id}.pdf"
        
        try:
            print(f"   下载: {pdf_url}")
            urllib.request.urlretrieve(pdf_url, pdf_path)
            print(f"   保存: {pdf_path}")
        except Exception as e:
            raise RuntimeError(f"下载失败: {e}")
        
        return ArxivPaper(arxiv_id, pdf_path)


class ArxivPaper:
    """ArXiv 论文对象"""
    
    def __init__(self, arxiv_id: str, pdf_path: Path):
        self.arxiv_id = arxiv_id
        self.pdf_path = pdf_path
        self._content = None
    
    def parse(self) -> dict:
        """解析论文内容"""
        # 这里可以集成 parse_paper.py 的功能
        from parse_paper import PaperParser
        
        parser = PaperParser()
        result = parser.parse(str(self.pdf_path))
        
        self._content = result
        return result.to_dict()
    
    def analyze(self) -> "PaperAnalysis":
        """分析论文"""
        if not self._content:
            self.parse()
        
        return PaperAnalysis(self)
    
    def summarize(self, style: str = "academic") -> str:
        """生成论文总结"""
        if not self._content:
            self.parse()
        
        # 这里可以调用 LLM 进行总结
        # 简化版本：返回基本信息
        return f"""# ArXiv:{self.arxiv_id} 论文总结

## 基本信息
- ArXiv ID: {self.arxiv_id}
- PDF 路径: {self.pdf_path}
- 字符数: {len(self._content.text)}
- 公式数: {len(self._content.latex_formulas)}

## 内容预览
{self._content.text[:1000]}...

## LaTeX 公式
""" + "\n".join(f"- ${f}$" for f in self._content.latex_formulas[:5])


class PaperAnalysis:
    """论文分析结果"""
    
    def __init__(self, paper: ArxivPaper):
        self.paper = paper
        self.summary = ""
        self.key_contributions = []
        self.methodology = ""
    
    def to_dict(self) -> dict:
        return {
            "arxiv_id": self.paper.arxiv_id,
            "summary": self.summary,
            "key_contributions": self.key_contributions,
            "methodology": self.methodology
        }


def main():
    parser = argparse.ArgumentParser(description="获取 ArXiv 论文")
    parser.add_argument("arxiv_id", help="ArXiv ID 或 URL")
    parser.add_argument("--output-dir", "-o", default="./papers", help="输出目录")
    parser.add_argument("--analyze", "-a", action="store_true", help="分析论文")
    parser.add_argument("--summarize", "-s", action="store_true", help="生成总结")
    parser.add_argument("--mirror", "-m", help="ArXiv 镜像地址")
    
    args = parser.parse_args()
    
    try:
        fetcher = ArxivFetcher(mirror=args.mirror)
        paper = fetcher.fetch(args.arxiv_id, args.output_dir)
        
        if args.analyze:
            print("\n🔍 分析论文...")
            analysis = paper.analyze()
            print(f"✅ 分析完成")
        
        if args.summarize:
            print("\n📝 生成总结...")
            summary = paper.summarize()
            summary_path = paper.pdf_path.parent / f"{paper.arxiv_id}_summary.md"
            summary_path.write_text(summary, encoding='utf-8')
            print(f"✅ 总结已保存: {summary_path}")
        
        print(f"\n✅ 完成!")
        print(f"   ArXiv ID: {paper.arxiv_id}")
        print(f"   PDF 路径: {paper.pdf_path}")
        
    except Exception as e:
        print(f"❌ 错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
