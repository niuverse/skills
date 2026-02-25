#!/usr/bin/env python3
"""
PDF 论文解析工具
支持文本、图像、表格、公式提取
"""

import argparse
import json
import os
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Optional, Dict, Any


@dataclass
class ParseResult:
    """解析结果数据结构"""
    text: str
    markdown: str
    latex_formulas: List[str]
    images: List[str]
    tables: List[Dict]
    metadata: Dict[str, Any]
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    def save(self, output_dir: str):
        """保存解析结果到目录"""
        out_path = Path(output_dir)
        out_path.mkdir(parents=True, exist_ok=True)
        
        # 保存文本
        (out_path / "text.txt").write_text(self.text, encoding='utf-8')
        
        # 保存 Markdown
        (out_path / "content.md").write_text(self.markdown, encoding='utf-8')
        
        # 保存结构化数据
        (out_path / "data.json").write_text(
            json.dumps(self.to_dict(), ensure_ascii=False, indent=2),
            encoding='utf-8'
        )
        
        print(f"✅ 结果已保存到: {out_path}")


class PaperParser:
    """论文解析器"""
    
    def __init__(self, backend: str = "auto"):
        """
        初始化解析器
        
        Args:
            backend: 解析后端 ("auto", "mineru", "pymupdf", "pdfplumber")
        """
        self.backend = backend
        self._check_dependencies()
    
    def _check_dependencies(self):
        """检查依赖库"""
        self.has_mineru = self._check_module("mineru")
        self.has_pymupdf = self._check_module("fitz")
        self.has_pdfplumber = self._check_module("pdfplumber")
        
        if self.backend == "auto":
            if self.has_mineru:
                self.backend = "mineru"
            elif self.has_pymupdf:
                self.backend = "pymupdf"
            elif self.has_pdfplumber:
                self.backend = "pdfplumber"
            else:
                raise ImportError("未找到可用的 PDF 解析库，请安装: pip install pymupdf")
        
        print(f"✅ 使用后端: {self.backend}")
    
    def _check_module(self, name: str) -> bool:
        """检查模块是否可用"""
        try:
            __import__(name)
            return True
        except ImportError:
            return False
    
    def parse(self, pdf_path: str) -> ParseResult:
        """
        解析 PDF 文件
        
        Args:
            pdf_path: PDF 文件路径
            
        Returns:
            ParseResult: 解析结果
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"文件不存在: {pdf_path}")
        
        if self.backend == "mineru":
            return self._parse_with_mineru(pdf_path)
        elif self.backend == "pymupdf":
            return self._parse_with_pymupdf(pdf_path)
        elif self.backend == "pdfplumber":
            return self._parse_with_pdfplumber(pdf_path)
        else:
            raise ValueError(f"未知后端: {self.backend}")
    
    def _parse_with_pymupdf(self, pdf_path: str) -> ParseResult:
        """使用 PyMuPDF 解析"""
        import fitz
        
        doc = fitz.open(pdf_path)
        
        text_parts = []
        images = []
        tables = []
        
        for page_num, page in enumerate(doc):
            # 提取文本
            text_parts.append(page.get_text())
            
            # 提取图像
            img_list = page.get_images()
            for img_index, img in enumerate(img_list, start=1):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                ext = base_image["ext"]
                
                img_filename = f"page{page_num+1}_img{img_index}.{ext}"
                images.append(img_filename)
        
        doc.close()
        
        full_text = "\n\n".join(text_parts)
        
        return ParseResult(
            text=full_text,
            markdown=f"# PDF Content\n\n{full_text}",
            latex_formulas=self._extract_latex(full_text),
            images=images,
            tables=tables,
            metadata={"pages": len(text_parts), "backend": "pymupdf"}
        )
    
    def _parse_with_pdfplumber(self, pdf_path: str) -> ParseResult:
        """使用 PDFPlumber 解析"""
        import pdfplumber
        
        text_parts = []
        tables = []
        
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text_parts.append(page.extract_text() or "")
                
                # 提取表格
                page_tables = page.extract_tables()
                for table in page_tables:
                    tables.append({"data": table})
        
        full_text = "\n\n".join(text_parts)
        
        return ParseResult(
            text=full_text,
            markdown=f"# PDF Content\n\n{full_text}",
            latex_formulas=self._extract_latex(full_text),
            images=[],
            tables=tables,
            metadata={"pages": len(text_parts), "backend": "pdfplumber"}
        )
    
    def _parse_with_mineru(self, pdf_path: str) -> ParseResult:
        """使用 MinerU 解析 (需要安装 mineru)"""
        # MinerU 解析逻辑
        # 这里只是一个占位符，实际使用需要调用 MinerU API
        raise NotImplementedError("MinerU 解析需要配置 API Token")
    
    def _extract_latex(self, text: str) -> List[str]:
        """从文本中提取 LaTeX 公式"""
        import re
        
        # 匹配 $...$ 和 $$...$$ 格式的公式
        patterns = [
            r'\$\$(.+?)\$\$',
            r'\$(.+?)\$',
            r'\\begin\{equation\}(.+?)\\end\{equation\}',
            r'\\\[(.+?)\\\]',
            r'\\\((.+?)\\\)'
        ]
        
        formulas = []
        for pattern in patterns:
            matches = re.findall(pattern, text, re.DOTALL)
            formulas.extend(matches)
        
        return formulas


def main():
    parser = argparse.ArgumentParser(description="解析 PDF 论文")
    parser.add_argument("pdf_path", help="PDF 文件路径")
    parser.add_argument("--output-dir", "-o", default="./output", help="输出目录")
    parser.add_argument("--backend", "-b", default="auto", 
                       choices=["auto", "mineru", "pymupdf", "pdfplumber"],
                       help="解析后端")
    
    args = parser.parse_args()
    
    try:
        paper_parser = PaperParser(backend=args.backend)
        result = paper_parser.parse(args.pdf_path)
        result.save(args.output_dir)
        
        print(f"\n📄 解析完成!")
        print(f"   - 页数: {result.metadata.get('pages', 'N/A')}")
        print(f"   - 字符数: {len(result.text)}")
        print(f"   - 公式数: {len(result.latex_formulas)}")
        print(f"   - 图像数: {len(result.images)}")
        print(f"   - 表格数: {len(result.tables)}")
        
    except Exception as e:
        print(f"❌ 错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
