# Isaac Lab / Isaac Sim / MuJoCo 参考资源

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

## 对比总结

| 特性 | Isaac Sim/Lab | MuJoCo |
|------|---------------|--------|
| 渲染质量 | ⭐⭐⭐⭐⭐ (光线追踪) | ⭐⭐⭐ (基础) |
| 物理精度 | ⭐⭐⭐⭐⭐ (PhysX 5) | ⭐⭐⭐⭐⭐ (广义坐标) |
| 学习曲线 | ⭐⭐ (陡峭) | ⭐⭐⭐⭐ (平缓) |
| GPU加速 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| RL框架 | 内置完整 | 需配合Gymnasium |
| 开源程度 | 部分开源 | 完全开源 |

---

## 推荐学习路径

### 初学者
1. **MuJoCo** - 理解基础物理仿真
2. **Isaac Sim** - 学习 USD 和可视化
3. **Isaac Lab** - 强化学习和机器人任务

### 进阶
- 自定义机器人模型
- 多GPU并行训练
- 域随机化 (Domain Randomization)
- Sim-to-Real 迁移

---

## 社区资源

### Isaac Lab/Sim
- **论坛**: https://forums.developer.nvidia.com/c/omniverse/isaac/
- **Discord**: NVIDIA Omniverse Discord

### MuJoCo
- **GitHub Discussions**: https://github.com/google-deepmind/mujoco/discussions
- **Awesome MuJoCo**: https://github.com/erwincoumans/awesome-mujoco
