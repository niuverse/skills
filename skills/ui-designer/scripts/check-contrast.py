#!/usr/bin/env python3
"""
检查颜色对比度是否符合 WCAG 标准
用法: python check-contrast.py --foreground "#ffffff" --background "#000000"
"""

import argparse
import math

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def relative_luminance(rgb):
    """计算相对亮度"""
    def channel_luminance(c):
        c = c / 255.0
        if c <= 0.03928:
            return c / 12.92
        else:
            return math.pow((c + 0.055) / 1.055, 2.4)
    
    r, g, b = rgb
    return 0.2126 * channel_luminance(r) + 0.7152 * channel_luminance(g) + 0.0722 * channel_luminance(b)

def contrast_ratio(color1, color2):
    """计算两个颜色的对比度"""
    rgb1 = hex_to_rgb(color1)
    rgb2 = hex_to_rgb(color2)
    
    lum1 = relative_luminance(rgb1)
    lum2 = relative_luminance(rgb2)
    
    lighter = max(lum1, lum2)
    darker = min(lum1, lum2)
    
    return (lighter + 0.05) / (darker + 0.05)

def check_wcag(ratio):
    """检查 WCAG 合规性"""
    results = {
        'AA_normal': ratio >= 4.5,
        'AA_large': ratio >= 3.0,
        'AAA_normal': ratio >= 7.0,
        'AAA_large': ratio >= 4.5,
    }
    return results

def main():
    parser = argparse.ArgumentParser(description='检查颜色对比度 WCAG 合规性')
    parser.add_argument('--foreground', required=True, help='前景色 (如 #ffffff)')
    parser.add_argument('--background', required=True, help='背景色 (如 #000000)')
    
    args = parser.parse_args()
    
    ratio = contrast_ratio(args.foreground, args.background)
    results = check_wcag(ratio)
    
    print(f"对比度: {ratio:.2f}:1")
    print()
    print("WCAG 合规性:")
    print(f"  AA (普通文本): {'✅ 通过' if results['AA_normal'] else '❌ 失败'} (需要 4.5:1)")
    print(f"  AA (大文本):   {'✅ 通过' if results['AA_large'] else '❌ 失败'} (需要 3.0:1)")
    print(f"  AAA (普通文本): {'✅ 通过' if results['AAA_normal'] else '❌ 失败'} (需要 7.0:1)")
    print(f"  AAA (大文本):  {'✅ 通过' if results['AAA_large'] else '❌ 失败'} (需要 4.5:1)")
    
    if not results['AA_normal']:
        print()
        print("⚠️  警告: 对比度不符合 WCAG AA 标准，可能影响可访问性")

if __name__ == '__main__':
    main()
