---
name: robot-sim-expert
description: |
  Expert-level robot simulation engineering skill for Isaac Lab, Isaac Sim, MuJoCo,
  MJX Lab, and Newton. Use when working with:
  - Isaac Lab/Sim robot simulation and RL training
  - MuJoCo physics simulation and model creation
  - MJX Lab (MuJoCo+Isaac Lab API hybrid) for RL research
  - Newton (GPU-accelerated physics with MuJoCo Warp)
  - Robot model design (URDF, MJCF, USD)
  - Reinforcement learning for robotics
  - Sim-to-real transfer
  - Multi-GPU parallel training
  
  Triggers: robot simulation, Isaac Lab, Isaac Sim, MuJoCo, MJX Lab, Newton,
  RL training, physics simulation, quadruped, humanoid, robotic arm, sim-to-real,
  MuJoCo Warp, GPU acceleration
---

# Robot Simulation Expert

顶级机器人仿真工程师，精通 Isaac Lab、Isaac Sim 和 MuJoCo。

## 核心能力

| 领域 | 能力 |
|------|------|
| **Isaac Lab** | RL训练、任务配置、奖励设计、并行环境 |
| **Isaac Sim** | USD场景、物理设置、传感器、ROS集成 |
| **MuJoCo** | MJCF建模、Python绑定、Gym集成、批量仿真 |
| **MJX Lab** | MuJoCo+Isaac Lab API混合，轻量级RL研究 |
| **Newton** | GPU加速物理仿真，OpenUSD，可微分仿真 |
| **通用** | 机器人动力学、控制算法、Sim-to-Real |

## 快速开始

### 1. 环境验证
```bash
python scripts/verify_env.py
```

### 2. 创建 Isaac Lab 任务
```bash
python scripts/create_isaaclab_task.py --name MyQuadruped --robot anymal_d
```

### 3. 创建 MuJoCo 机器人
```bash
python scripts/create_mujoco_robot.py --name my_robot --type quadruped
```

## 参考资料

| 文件 | 内容 |
|------|------|
| [resources.md](references/resources.md) | 官方文档链接、GitHub仓库、学习路径 |
| [isaaclab-workflow.md](references/isaaclab-workflow.md) | Isaac Lab 完整工作流指南 |
| [mujoco-workflow.md](references/mujoco-workflow.md) | MuJoCo 完整工作流指南 |
| [mjxlab-workflow.md](references/mjxlab-workflow.md) | MJX Lab 快速开始和训练指南 |
| [newton-workflow.md](references/newton-workflow.md) | Newton GPU仿真和OpenUSD指南 |

## 框架选择指南

### 选择 Isaac Lab 当:
- 需要 GPU 加速的大规模并行训练
- 使用 NVIDIA GPU 和 CUDA
- 追求高保真渲染（光线追踪）
- 需要完整的 RL 框架集成
- 处理复杂传感器（相机、激光雷达）

### 选择 MuJoCo 当:
- 需要快速原型验证
- 追求简洁的 Python API
- 需要完全开源方案
- 进行控制算法研究
- 预算有限的硬件环境

### 选择 MJX Lab 当:
- 熟悉 Isaac Lab API 但想用 MuJoCo 物理
- 需要轻量级模块化抽象
- 专注于 RL 研究和 sim-to-real
- 想用 MuJoCo Warp 进行 GPU 加速
- 需要运动模仿 (motion imitation) 功能

### 选择 Newton 当:
- 需要可微分物理仿真
- 要使用 OpenUSD 工作流
- 需要用户自定义扩展性
- 偏好社区驱动的开源项目 (Linux Foundation)
- 需要与 Warp 生态系统集成

## 典型工作流

### Isaac Lab 训练流程
```
1. 定义场景 (InteractiveSceneCfg)
2. 配置观测 (ObservationManagerCfg)
3. 设计奖励 (RewardManagerCfg)
4. 设置终止条件 (TerminationManagerCfg)
5. 运行训练 (RSL RL)
6. 评估和可视化
```

### MuJoCo 建模流程
```
1. 编写 MJCF XML
2. 验证模型加载
3. 创建 Gymnasium 环境
4. 实现控制策略
5. 训练和评估
```

### MJX Lab 训练流程
```
1. 安装 mjlab 和 mujoco-warp
2. 选择预定义任务 (Mjlab-Velocity-Flat-Unitree-G1)
3. 配置多GPU训练 (--gpu-ids 0 1)
4. 运行训练 (uv run train)
5. 从 WandB 评估策略 (uv run play)
```

### Newton 仿真流程
```
1. 设置 uv 环境 (uv sync --extra examples)
2. 加载 URDF 或创建基本模型
3. 配置 OpenUSD 场景 (可选)
4. 运行仿真 (uv run -m newton.examples)
5. 使用 Warp 进行可微分计算
```

## 常见任务模式

### 创建自定义奖励函数
```python
from omni.isaac.lab.managers import RewardTermCfg
from omni.isaac.lab_tasks.manager_based.locomotion.velocity.mdp import rewards

def custom_reward(env, asset_cfg):
    asset = env.scene[asset_cfg.name]
    # 实现奖励逻辑
    return reward

# 在 env_cfg.py 中使用
rewards: RewardManagerCfg = RewardManagerCfg({
    "custom": RewardTermCfg(func=custom_reward, weight=1.0),
})
```

### MuJoCo 与 Gymnasium 集成
```python
import gymnasium as gym
import mujoco

class MyRobotEnv(gym.Env):
    def __init__(self):
        self.model = mujoco.MjModel.from_xml_path("robot.xml")
        self.data = mujoco.MjData(self.model)
        
    def reset(self):
        mujoco.mj_resetData(self.model, self.data)
        return self._get_obs()
    
    def step(self, action):
        self.data.ctrl[:] = action
        mujoco.mj_step(self.model, self.data)
        return self._get_obs(), reward, done, {}
```

## 性能优化

### Isaac Lab
- 使用 `--headless` 进行无头训练
- 调整 `num_envs` 匹配 GPU 显存
- 启用 `use_gpu_pipeline` 和 `use_gpu`

### MuJoCo
- 使用 `mujoco.mj_stepN` 批量仿真
- 考虑 `mujoco_mjx` 用于 JAX/GPU 加速
- 减少渲染频率

## 调试技巧

| 问题 | 解决方案 |
|------|---------|
| 仿真不稳定 | 降低 timestep，增加 iterations |
| NaN 奖励 | 检查观测归一化，添加限幅 |
| GPU OOM | 减少并行环境数量，降低分辨率 |
| 训练不收敛 | 检查奖励设计，调整学习率 |

## Sim-to-Real 迁移

### 域随机化 (Isaac Lab)
```python
@configclass
class DomainRandCfg:
    push_robots = True
    randomize_base_mass = True
    randomize_friction = True
    randomize_restitution = True
```

### MuJoCo 参数调整
```xml
<option timestep="0.002">
  <flag warmstart="enable"/>
</option>
<default>
  <joint damping="0.5" armature="0.01"/>
</default>
```

## 扩展资源

- **Isaac Lab GitHub**: https://github.com/isaac-sim/IsaacLab
- **MuJoCo 文档**: https://mujoco.readthedocs.io/
- **NVIDIA 论坛**: https://forums.developer.nvidia.com/c/omniverse/isaac/
- **MuJoCo GitHub**: https://github.com/google-deepmind/mujoco
