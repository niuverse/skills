#!/usr/bin/env python3
"""
生成 Tailwind CSS 颜色调色板
用法: python generate-palette.py --base-color "#3b82f6" --name "primary"
"""

import argparse
import colorsys

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(*rgb)

def adjust_brightness(rgb, factor):
    """调整亮度，factor > 1 变亮，< 1 变暗"""
    r, g, b = rgb
    r = min(255, int(r * factor))
    g = min(255, int(g * factor))
    b = min(255, int(b * factor))
    return (r, g, b)

def generate_palette(base_hex):
    """生成完整的颜色调色板"""
    base_rgb = hex_to_rgb(base_hex)
    
    palette = {
        50: adjust_brightness(base_rgb, 1.9),
        100: adjust_brightness(base_rgb, 1.7),
        200: adjust_brightness(base_rgb, 1.5),
        300: adjust_brightness(base_rgb, 1.3),
        400: adjust_brightness(base_rgb, 1.1),
        500: base_rgb,
        600: adjust_brightness(base_rgb, 0.85),
        700: adjust_brightness(base_rgb, 0.7),
        800: adjust_brightness(base_rgb, 0.55),
        900: adjust_brightness(base_rgb, 0.4),
        950: adjust_brightness(base_rgb, 0.25),
    }
    
    return {k: rgb_to_hex(v) for k, v in palette.items()}

def print_tailwind_config(palette, name):
    """输出 Tailwind 配置格式"""
    print(f"// tailwind.config.js")
    print(f"module.exports = {{")
    print(f"  theme: {{")
    print(f"    extend: {{")
    print(f"      colors: {{")
    print(f"        {name}: {{")
    for shade, color in sorted(palette.items()):
        print(f"          {shade}: '{color}',")
    print(f"        }},")
    print(f"      }},")
    print(f"    }},")
    print(f"  }},")
    print(f"}}")

def print_css_variables(palette, name):
    """输出 CSS 变量格式"""
    print(f":root {{")
    for shade, color in sorted(palette.items()):
        print(f"  --{name}-{shade}: {color};")
    print(f"}}")

def main():
    parser = argparse.ArgumentParser(description='生成 Tailwind CSS 颜色调色板')
    parser.add_argument('--base-color', required=True, help='基础颜色 (如 #3b82f6)')
    parser.add_argument('--name', default='primary', help='颜色名称')
    parser.add_argument('--format', choices=['tailwind', 'css'], default='tailwind', 
                       help='输出格式')
    
    args = parser.parse_args()
    
    palette = generate_palette(args.base_color)
    
    if args.format == 'tailwind':
        print_tailwind_config(palette, args.name)
    else:
        print_css_variables(palette, args.name)

if __name__ == '__main__':
    main()
