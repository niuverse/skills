# Isaac Lab 工作流指南

## 安装

### 系统要求
- Ubuntu 22.04 / Windows 10+
- NVIDIA GPU (RTX 3060+)
- 32GB+ RAM
- 50GB+ 磁盘空间

### 安装步骤

```bash
# 1. 克隆仓库
git clone https://github.com/isaac-sim/IsaacLab.git
cd IsaacLab

# 2. 运行安装脚本
./isaaclab.sh --install

# 3. 验证安装
./isaaclab.sh --test
```

### 虚拟环境
```bash
# 使用 conda
conda create -n isaaclab python=3.10
conda activate isaaclab

# 安装依赖
pip install -e source/isaaclab
pip install -e source/isaaclab_tasks
```

---

## 核心工作流

### 1. Manager-Based Workflow

适合：快速原型，标准RL任务

```python
from omni.isaac.lab.envs import ManagerBasedRLEnvCfg
from omni.isaac.lab.managers import ObservationManager, RewardManager

@configclass
class MyEnvCfg(ManagerBasedRLEnvCfg):
    # 场景配置
    scene: InteractiveSceneCfg = MySceneCfg()
    
    # 观测管理
    observations: ObservationManagerCfg = ObservationManagerCfg({
        "policy": ObsTermCfg(func=mdp.joint_pos_rel),
    })
    
    # 奖励管理
    rewards: RewardManagerCfg = RewardManagerCfg({
        "track_pos": RewardTermCfg(func=mdp.track_pos, weight=1.0),
    })
```

### 2. Direct Workflow

适合：自定义逻辑，复杂控制

```python
from omni.isaac.lab.envs import DirectRLEnv

class MyDirectEnv(DirectRLEnv):
    def __init__(self, cfg, render_mode=None, **kwargs):
        super().__init__(cfg, render_mode, **kwargs)
        
    def _setup_scene(self):
        # 直接控制场景创建
        self.robot = Articulation(self.cfg.robot_cfg)
        self.scene.articulations["robot"] = self.robot
        
    def _get_observations(self) -> dict:
        # 自定义观测
        obs = torch.cat([self.robot.data.joint_pos, 
                         self.robot.data.joint_vel], dim=-1)
        return {"policy": obs}
        
    def _get_rewards(self) -> torch.Tensor:
        # 自定义奖励
        return self.cfg.reward_weights * self._compute_reward()
```

---

## 任务配置

### 创建新任务

```bash
# 在 source/isaaclab_tasks/isaaclab_tasks/manager_based/locomotion/ 下

my_robot/
├── __init__.py
├── env_cfg.py      # 环境配置
├── agent_cfg.py    # RL算法配置
└── mdp/
    ├── __init__.py
    ├── rewards.py   # 自定义奖励函数
    └── observations.py  # 自定义观测
```

### 奖励函数示例

```python
# mdp/rewards.py
import torch
from typing import Optional
from omni.isaac.lab.managers import SceneEntityCfg
from omni.isaac.lab.sensors import ContactSensor

def feet_air_time(
    env: ManagerBasedRLEnv,
    asset_cfg: SceneEntityCfg = SceneEntityCfg("robot"),
    sensor_cfg: SceneEntityCfg = SceneEntityCfg("contact_forces"),
    threshold: float = 1.0,
) -> torch.Tensor:
    """奖励足部在空中停留时间（步态训练）"""
    contact_sensor: ContactSensor = env.scene.sensors[sensor_cfg.name]
    
    # 计算每个足部的空中时间
    first_contact = contact_sensor.compute_first_contact(env.step_dt)
    last_air_time = contact_sensor.data.last_air_time
    
    # 只在接触地面时给予奖励
    reward = torch.where(first_contact, last_air_time, 0.0)
    return reward.clamp(max=threshold)
```

---

## 训练配置

### RSL RL 配置

```python
@configclass
class RslRlPpoActorCriticCfg:
    init_noise_std: float = 1.0
    actor_hidden_dims: list = [512, 256, 128]
    critic_hidden_dims: list = [512, 256, 128]
    activation: str = "elu"

@configclass
class RslRlPpoAlgorithmCfg:
    value_loss_coef: float = 1.0
    use_clipped_value_loss: bool = True
    clip_param: float = 0.2
    entropy_coef: float = 0.01
    num_learning_epochs: int = 5
    num_mini_batches: int = 4
    learning_rate: float = 1e-3
```

### 运行训练

```bash
# 单GPU训练
python scripts/rsl_rl/train.py --task Isaac-Velocity-Flat-Anymal-D-v0 --headless

# 多GPU并行
python scripts/rsl_rl/train.py --task Isaac-Velocity-Flat-Anymal-D-v0 --num_envs 4096 --headless

# 评估
python scripts/rsl_rl/play.py --task Isaac-Velocity-Flat-Anymal-D-v0 --checkpoint /path/to/checkpoint.pt
```

---

## 调试技巧

### 可视化
```python
# 启用实时渲染
cfg.viewer = ViewerCfg(eye=(5.0, 5.0, 5.0), lookat=(0.0, 0.0, 0.0))

# 添加调试绘制
from omni.isaac.lab.utils.warp import debug_draw_line
```

### 性能优化
```python
# 减少GPU内存占用
cfg.sim.device = "cuda:0"
cfg.sim.use_gpu_pipeline = True
cfg.sim.physx.use_gpu = True

# 控制并行环境数量
cfg.scene.num_envs = 2048  # 根据GPU内存调整
```

### 日志记录
```python
from tensorboardX import SummaryWriter

writer = SummaryWriter(log_dir="./runs")
writer.add_scalar("rewards/episode", episode_reward, episode)
```
