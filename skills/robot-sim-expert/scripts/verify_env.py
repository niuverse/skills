#!/usr/bin/env python3
"""
仿真环境验证工具
检查 Isaac Sim/Lab 和 MuJoCo 是否正确安装
"""

import sys


def check_isaac():
    """检查 Isaac Sim/Lab 安装状态"""
    print("🔍 检查 Isaac Sim/Lab...")
    
    results = []
    
    # 检查 omni.isaac
    try:
        import omni.isaac
        results.append(("✅", "omni.isaac 核心库"))
    except ImportError:
        results.append(("❌", "omni.isaac 未安装"))
    
    # 检查 Isaac Lab
    try:
        import omni.isaac.lab
        results.append(("✅", "Isaac Lab"))
    except ImportError:
        results.append(("❌", "Isaac Lab 未安装"))
    
    # 检查 torch
    try:
        import torch
        cuda = torch.cuda.is_available()
        results.append(("✅" if cuda else "⚠️", f"PyTorch (CUDA: {cuda})"))
    except ImportError:
        results.append(("❌", "PyTorch 未安装"))
    
    for status, name in results:
        print(f"   {status} {name}")
    
    return all(r[0] == "✅" for r in results)


def check_mujoco():
    """检查 MuJoCo 安装状态"""
    print("\n🔍 检查 MuJoCo...")
    
    results = []
    
    # 检查 mujoco
    try:
        import mujoco
        results.append(("✅", f"MuJoCo {mujoco.__version__}"))
    except ImportError:
        results.append(("❌", "MuJoCo 未安装"))
        return False
    
    # 检查 gymnasium
    try:
        import gymnasium
        results.append(("✅", f"Gymnasium {gymnasium.__version__}"))
    except ImportError:
        results.append(("⚠️", "Gymnasium (可选)"))
    
    # 检查 mediapy
    try:
        import mediapy
        results.append(("✅", "mediapy (渲染)"))
    except ImportError:
        results.append(("⚠️", "mediapy (可选)"))
    
    for status, name in results:
        print(f"   {status} {name}")
    
    return True


def check_gpu():
    """检查 GPU 可用性"""
    print("\n🔍 检查 GPU...")
    
    try:
        import torch
        if torch.cuda.is_available():
            print(f"   ✅ CUDA 可用")
            print(f"      GPU: {torch.cuda.get_device_name(0)}")
            print(f"      显存: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
        else:
            print("   ⚠️ CUDA 不可用 (CPU 模式)")
    except ImportError:
        print("   ❌ PyTorch 未安装")


def main():
    print("=" * 50)
    print("🤖 机器人仿真环境验证工具")
    print("=" * 50)
    
    check_isaac()
    check_mujoco()
    check_gpu()
    
    print("\n" + "=" * 50)
    print("提示: 如需安装缺失组件，参考 references/resources.md")
    print("=" * 50)


if __name__ == "__main__":
    main()
