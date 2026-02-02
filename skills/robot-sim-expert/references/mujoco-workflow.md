# MuJoCo 工作流指南

## 安装

### Python 安装（推荐）
```bash
pip install mujoco
```

### 系统要求
- Python 3.8+
- OpenGL (用于可视化)
- 可选: CUDA (用于GPU加速)

### 验证安装
```python
import mujoco
print(mujoco.__version__)
```

---

## 核心概念

### Model 和 Data
```python
import mujoco

# 从XML加载模型
model = mujoco.MjModel.from_xml_path("humanoid.xml")

# 创建数据实例
data = mujoco.MjData(model)

# 重置仿真状态
mujoco.mj_resetData(model, data)
```

### 仿真循环
```python
# 基本仿真循环
for _ in range(1000):
    # 设置控制输入
    data.ctrl[:] = computed_controls
    
    # 前进一步
    mujoco.mj_step(model, data)
    
    # 获取状态
    position = data.qpos.copy()
    velocity = data.qvel.copy()
```

---

## MJCF 模型定义

### 基本结构
```xml
<mujoco model="my_robot">
  <compiler angle="radian" meshdir="assets/" texturedir="assets/"/>
  
  <option timestep="0.002" iterations="50" solver="Newton">
    <flag warmstart="enable"/>
  </option>
  
  <default>
    <joint armature="0.01" damping="1" limited="true"/>
    <geom contype="1" conaffinity="1" friction="0.7 0.1 0.1"/>
  </default>
  
  <worldbody>
    <light diffuse="0.8 0.8 0.8" pos="0 0 5" dir="0 0 -1"/>
    <geom type="plane" size="50 50 0.1" rgba="0.9 0.9 0.9 1"/>
    
    <body name="base" pos="0 0 1">
      <freejoint/>
      <geom type="box" size="0.2 0.1 0.05" mass="5"/>
      
      <body name="leg1" pos="0.15 0 -0.1">
        <joint name="hip1" type="hinge" axis="0 1 0" range="-120 120"/>
        <geom type="capsule" size="0.04" fromto="0 0 0 0 0 -0.4"/>
        
        <body name="shin1" pos="0 0 -0.4">
          <joint name="knee1" type="hinge" axis="0 1 0" range="-140 0"/>
          <geom type="capsule" size="0.035" fromto="0 0 0 0 0 -0.4"/>
        </body>
      </body>
    </body>
  </worldbody>
  
  <actuator>
    <motor name="hip1_motor" joint="hip1" gear="100" ctrllimited="true" ctrlrange="-100 100"/>
    <motor name="knee1_motor" joint="knee1" gear="100" ctrllimited="true" ctrlrange="-100 100"/>
  </actuator>
</mujoco>
```

### 常见几何体
```xml
<!-- 球体 -->
<geom type="sphere" size="0.05"/>

<!-- 立方体 -->
<geom type="box" size="0.1 0.05 0.02"/>

<!-- 胶囊体 -->
<geom type="capsule" size="0.03" fromto="0 0 0 0 0 0.2"/>

<!-- 圆柱体 -->
<geom type="cylinder" size="0.05 0.1"/>

<!-- 椭球体 -->
<geom type="ellipsoid" size="0.1 0.05 0.02"/>
```

### 关节类型
```xml
<!-- 自由浮动 -->
<freejoint/>

<!-- 滑动关节 -->
<joint type="slide" axis="0 0 1" range="-0.5 0.5"/>

<!-- 旋转关节 -->
<joint type="hinge" axis="0 1 0" range="-90 90"/>

<!-- 球关节 -->
<joint type="ball"/>
```

---

## 可视化

### 交互式查看器
```python
import mujoco
import mujoco.viewer

with mujoco.viewer.launch_passive(model, data) as viewer:
    while viewer.is_running():
        # 设置控制
        data.ctrl[:] = policy(obs)
        
        # 前进步骤
        mujoco.mj_step(model, data)
        
        # 更新观测
        obs = get_obs(data)
        
        # 同步查看器
        viewer.sync()
```

### 程序化渲染
```python
import mediapy as media

# 创建渲染器
renderer = mujoco.Renderer(model, height=480, width=640)

# 渲染帧
renderer.update_scene(data)
frame = renderer.render()

# 保存视频
media.write_video("simulation.mp4", frames, fps=60)
```

---

## 强化学习集成

### Gymnasium 环境
```python
import gymnasium as gym
from gymnasium import spaces
import numpy as np

class MuJoCoEnv(gym.Env):
    def __init__(self, xml_path, frame_skip=2):
        self.model = mujoco.MjModel.from_xml_path(xml_path)
        self.data = mujoco.MjData(self.model)
        self.frame_skip = frame_skip
        
        # 定义空间
        self.observation_space = spaces.Box(
            low=-np.inf, high=np.inf, 
            shape=(self.model.nq + self.model.nv,), dtype=np.float32
        )
        self.action_space = spaces.Box(
            low=-1, high=1, shape=(self.model.nu,), dtype=np.float32
        )
    
    def reset(self, seed=None):
        super().reset(seed=seed)
        mujoco.mj_resetData(self.model, self.data)
        return self._get_obs(), {}
    
    def step(self, action):
        self.data.ctrl[:] = action
        for _ in range(self.frame_skip):
            mujoco.mj_step(self.model, self.data)
        
        obs = self._get_obs()
        reward = self._compute_reward()
        terminated = self._check_termination()
        
        return obs, reward, terminated, False, {}
    
    def _get_obs(self):
        return np.concatenate([self.data.qpos, self.data.qvel])
```

---

## 高级功能

### 传感器
```xml
<sensor>
  <!-- 关节位置传感器 -->
  <jointpos name="hip_pos" joint="hip"/>
  
  <!-- 关节速度传感器 -->
  <jointvel name="hip_vel" joint="hip"/>
  
  <!-- 陀螺仪 -->
  <gyro name="imu_gyro" site="imu"/>
  
  <!-- 加速度计 -->
  <accelerometer name="imu_acc" site="imu"/>
  
  <!-- 力传感器 -->
  <force name="foot_force" site="foot"/>
  
  <!-- 接触传感器 -->
  <touch name="foot_touch" site="foot"/>
</sensor>
```

### 接触检测
```python
# 获取接触信息
for i in range(data.ncon):
    contact = data.contact[i]
    geom1 = contact.geom1
    geom2 = contact.geom2
    
    # 获取接触力
    force = np.zeros(6)
    mujoco.mj_contactForce(model, data, i, force)
```

### 逆运动学
```python
from mujoco import minimize

# 定义目标
def residual(m, d):
    # 计算末端执行器与目标的距离
    ee_pos = d.site_xpos[ee_site_id]
    return ee_pos - target_pos

# 求解
minimize.least_squares(model, data, residual, 
                       target_qpos, 
                       regularization_strength=0.1)
```

---

## 最佳实践

### 性能优化
```python
# 使用批量仿真
batch_size = 1024

# 使用GPU加速（需要mujoco-mjx）
from mujoco import mjx
mjx_model = mjx.put_model(model)
```

### 数值稳定性
```xml
<option timestep="0.002" iterations="50" tolerance="1e-10">
  <flag warmstart="enable" filterparent="enable"/>
</option>
```

### 调试技巧
```python
# 打印模型信息
print(f"nq={model.nq}, nv={model.nv}, nu={model.nu}")

# 检查约束 violation
print(data.qfrc_constraint)

# 可视化接触点
from mujoco import viewer
viewer.launch(model, data)
```
