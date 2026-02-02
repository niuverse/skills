# Robot Simulation Resources

Complete reference for Isaac Lab, Isaac Sim, MuJoCo, MJX Lab, and Newton.

---

## Isaac Lab

### 官方资源
- **文档**: https://isaac-sim.github.io/IsaacLab/
- **GitHub**: https://github.com/isaac-sim/IsaacLab
- **NVIDIA 官方**: https://developer.nvidia.com/isaac-lab

### 核心概念
- **RL Games**: 强化学习训练框架
- **RSL RL**: 机器人学习库
- **Manager-Based / Direct**: 两种工作流模式
- **Scene**: 场景管理
- **Environment**: 环境配置
- **Observation / Action**: 观测和动作空间

### 关键API
```python
from omni.isaac.lab.envs import ManagerBasedRLEnv
from omni.isaac.lab.scene import InteractiveSceneCfg
from omni.isaac.lab.utils import configclass
```

### 目录结构
```
IsaacLab/
├── source/isaaclab/          # 核心库
├── source/isaaclab_rl/       # RL 算法
├── source/isaaclab_tasks/    # 任务示例
└── scripts/                  # 工具脚本
```

---

## Isaac Sim

### 官方资源
- **文档**: https://docs.omniverse.nvidia.com/isaacsim/
- **GitHub**: https://github.com/NVIDIA-Omniverse/IsaacSim-ros_workspaces
- **下载**: https://developer.nvidia.com/isaac-sim

### 核心概念
- **USD (Universal Scene Description)**: 场景描述格式
- **Stage**: 当前场景
- **Prim**: USD 基本单元
- **Xform**: 变换节点
- **Physics Scene**: 物理场景设置
- **Articulation**: 关节链

### 关键API
```python
from omni.isaac.core import World
from omni.isaac.core.prims import XFormPrim, RigidPrim
from omni.isaac.core.articulations import Articulation
from pxr import Usd, UsdGeom, Gf
```

### 常用功能
- **传感器**: Camera, Lidar, IMU, Contact Sensor
- **控制器**: Position/Velocity/Torque control
- **导入**: URDF, MJCF, USD
- **ROS/ROS2**: 集成支持

---

## MuJoCo

### 官方资源
- **文档**: https://mujoco.readthedocs.io/
- **GitHub**: https://github.com/google-deepmind/mujoco
- **Python Bindings**: https://github.com/google-deepmind/mujoco/tree/main/python

### 核心概念
- **Model**: XML定义的机器人模型
- **Data**: 仿真状态数据
- **Scene**: 渲染场景
- **Context**: 渲染上下文
- **Option**: 仿真选项

### 关键API
```python
import mujoco
import mujoco.viewer

# 加载模型
model = mujoco.MjModel.from_xml_path("model.xml")
data = mujoco.MjData(model)

# 运行仿真
with mujoco.viewer.launch_passive(model, data) as viewer:
    while viewer.is_running():
        mujoco.mj_step(model, data)
        viewer.sync()
```

### XML结构
```xml
<mujoco model="example">
  <compiler angle="degree" coordinate="local"/>
  <option timestep="0.002"/>
  <worldbody>
    <body name="base" pos="0 0 0">
      <joint name="joint1" type="hinge" axis="0 0 1"/>
      <geom type="box" size="0.1 0.1 0.1"/>
    </body>
  </worldbody>
  <actuator>
    <motor name="motor1" joint="joint1"/>
  </actuator>
</mujoco>
```

### MJCF vs URDF
- **MJCF**: MuJoCo原生格式，功能更丰富
- **URDF**: 通用格式，MuJoCo支持导入

---

## MJX Lab

### 官方资源
- **GitHub**: https://github.com/mujocolab/mjlab
- **文档**: https://mujocolab.github.io/mjlab/
- **Colab Demo**: https://colab.research.google.com/github/mujocolab/mjlab/blob/main/notebooks/demo.ipynb

### 核心特点
- **Isaac Lab API** + **MuJoCo Warp** 物理引擎
- 轻量级模块化设计
- 专注于 RL 和 sim-to-real
- 运动模仿 (Motion Imitation) 支持
- 多 GPU 训练

### 关键API
```python
from mjlab.envs import MjlabEnvCfg
from mjlab.tasks import LocomotionTaskCfg

# 训练
uv run train Mjlab-Velocity-Flat-Unitree-G1

# 评估
uv run play Mjlab-Velocity-Flat-Unitree-G1
```

---

## Newton

### 官方资源
- **GitHub**: https://github.com/newton-physics/newton
- **文档**: https://newton-physics.github.io/newton/
- **NVIDIA Warp**: https://github.com/NVIDIA/warp

### 核心特点
- **GPU加速**: 基于 NVIDIA Warp
- **可微分物理**: 支持梯度计算
- **OpenUSD**: 原生 USD 支持
- **社区驱动**: Linux Foundation 项目
- **发起方**: Disney Research, Google DeepMind, NVIDIA

### 关键API
```python
import newton as nt

# 创建仿真
sim = nt.Simulation()
robot = sim.add_articulation(urdf_path)

# 可微分仿真
sim = nt.Simulation(requires_grad=True)
loss = compute_loss(sim)
wp.backward(loss)
```

### ⚠️ 注意事项
- 目前处于 Beta 阶段，API 不稳定
- 频繁的重大更新

---

## 对比总结

| 特性 | Isaac Sim/Lab | MuJoCo | MJX Lab | Newton |
|------|---------------|--------|---------|--------|
| 渲染质量 | ⭐⭐⭐⭐⭐ (光线追踪) | ⭐⭐⭐ (基础) | ⭐⭐⭐ | ⭐⭐⭐ |
| 物理精度 | ⭐⭐⭐⭐⭐ (PhysX 5) | ⭐⭐⭐⭐⭐ (广义坐标) | ⭐⭐⭐⭐⭐ (MuJoCo) | ⭐⭐⭐⭐⭐ (MuJoCo) |
| 学习曲线 | ⭐⭐ (陡峭) | ⭐⭐⭐⭐ (平缓) | ⭐⭐⭐ | ⭐⭐⭐ |
| GPU加速 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| RL框架 | 内置完整 | 需配合Gymnasium | 内置 (RSL RL) | 需配合 |
| 可微分 | ❌ | ✅ (MJX) | ✅ | ✅ |
| 开源程度 | 部分开源 | 完全开源 | 开源 | 开源 (Apache 2.0) |
| OpenUSD | ⭐⭐⭐⭐⭐ | ❌ | ❌ | ⭐⭐⭐⭐⭐ |

---

## 框架选择指南

### 选择 Isaac Lab 当:
- 需要完整的企业级 RL 解决方案
- 有高保真渲染需求
- 使用 NVIDIA Omniverse 生态

### 选择 MJX Lab 当:
- 熟悉 Isaac Lab API 但想用 MuJoCo 物理
- 需要轻量级、快速迭代的 RL 研究
- 专注 sim-to-real 部署

### 选择 Newton 当:
- 需要可微分物理仿真
- 要使用 OpenUSD 工作流
- 偏好社区驱动的开源项目

### 选择 MuJoCo 当:
- 需要稳定、成熟的物理引擎
- 快速原型验证
- 控制算法研究

---

## 推荐学习路径

### 初学者
1. **MuJoCo** - 理解基础物理仿真
2. **MJX Lab** - 快速开始 GPU 加速 RL
3. **Isaac Sim** - 学习 USD 和高级可视化
4. **Isaac Lab** - 完整 RL 训练工作流
5. **Newton** - 可微分仿真 (进阶)

### 进阶
- 自定义机器人模型
- 多GPU并行训练 (MJX Lab/Isaac Lab)
- 域随机化 (Domain Randomization)
- Sim-to-Real 迁移
- 可微分控制优化 (Newton)

---

## 社区资源

### Isaac Lab/Sim
- **论坛**: https://forums.developer.nvidia.com/c/omniverse/isaac/
- **Discord**: NVIDIA Omniverse Discord

### MuJoCo
- **GitHub Discussions**: https://github.com/google-deepmind/mujoco/discussions
- **Awesome MuJoCo**: https://github.com/erwincoumans/awesome-mujoco

### MJX Lab
- **GitHub Issues**: https://github.com/mujocolab/mjlab/issues
- **文档反馈**: https://mujocolab.github.io/mjlab/source/faq.html

### Newton
- **GitHub Discussions**: https://github.com/newton-physics/newton/discussions
- **Linux Foundation**: https://www.linuxfoundation.org/projects
