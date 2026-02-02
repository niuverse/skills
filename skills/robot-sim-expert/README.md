# Robot Simulation Expert

🤖 Expert-level skill for robot simulation with Isaac Lab, Isaac Sim, MuJoCo, mjlab, and Newton.

## Overview

This skill provides comprehensive expertise for:
- **Isaac Lab/Sim**: NVIDIA's high-fidelity robotics simulation platform
- **MuJoCo**: DeepMind's physics engine for robotics
- **mjlab**: Isaac Lab API + MuJoCo Warp for lightweight RL research
- **Newton**: GPU-accelerated differentiable physics with OpenUSD
- **RL Training**: Reinforcement learning for robot control
- **Model Creation**: URDF, MJCF, and USD robot models

## Quick Start

### Verify Environment
```bash
python scripts/verify_env.py
```

### Create Isaac Lab Task
```bash
python scripts/create_isaaclab_task.py --name MyQuadruped --robot anymal_d
```

### Create MuJoCo Robot
```bash
python scripts/create_mujoco_robot.py --name my_robot --type quadruped
```

### mjlab Quick Start
```bash
# Install and run demo
uvx --from mjlab demo

# Train velocity tracking
uv run train Mjlab-Velocity-Flat-Unitree-G1 --env.scene.num-envs 4096
```

### Newton Quick Start
```bash
# Setup environment
uv sync --extra examples

# Run basic example
uv run -m newton.examples basic_pendulum
```

## Framework Comparison

| Feature | Isaac Lab | MuJoCo | mjlab | Newton |
|---------|-----------|--------|---------|--------|
| GPU Acceleration | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Rendering | ⭐⭐⭐⭐⭐ (Ray-traced) | ⭐⭐⭐ (Basic) | ⭐⭐⭐ | ⭐⭐⭐ |
| Differentiability | ❌ | ✅ (MJX) | ✅ | ✅ |
| RL Framework | Built-in (RSL RL) | External | Built-in | External |
| OpenUSD | ✅ | ❌ | ❌ | ✅ |
| Open Source | Partial | Full | Full | Full (Apache 2.0) |
| Learning Curve | Steep | Gentle | Moderate | Moderate |

## Capabilities

### Isaac Lab Expertise
- Manager-based and Direct workflows
- Custom reward and observation functions
- Multi-GPU parallel training
- Domain randomization
- Sim-to-real transfer

### Isaac Sim Expertise
- USD scene composition
- Sensor integration (camera, lidar, IMU)
- ROS/ROS2 bridge
- Physics configuration

### MuJoCo Expertise
- MJCF model definition
- Python API and Gymnasium integration
- Batch simulation
- Inverse kinematics
- Custom controllers

### mjlab Expertise
- Isaac Lab API with MuJoCo physics
- Motion imitation learning
- Multi-GPU distributed training
- WandB integration for motion datasets
- Sim-to-real deployment

### Newton Expertise
- GPU-accelerated physics with Warp
- Differentiable simulation
- OpenUSD scene composition
- Custom force kernels
- System identification

## Directory Structure

```
robot-sim-expert/
├── SKILL.md                      # Skill definition
├── README.md                     # This file
├── scripts/
│   ├── create_isaaclab_task.py   # Isaac Lab task generator
│   ├── create_mujoco_robot.py    # MuJoCo robot generator
│   └── verify_env.py             # Environment checker
└── references/
    ├── resources.md              # Links and documentation
    ├── isaaclab-workflow.md      # Isaac Lab guide
    ├── mujoco-workflow.md        # MuJoCo guide
    ├── mjlab-workflow.md        # mjlab guide (NEW)
    └── newton-workflow.md        # Newton guide (NEW)
```

## References

### Isaac Lab
- [GitHub](https://github.com/isaac-sim/IsaacLab)
- [Docs](https://isaac-sim.github.io/IsaacLab/)

### MuJoCo
- [GitHub](https://github.com/google-deepmind/mujoco)
- [Docs](https://mujoco.readthedocs.io/)

### mjlab
- [GitHub](https://github.com/mujocolab/mjlab)
- [Docs](https://mujocolab.github.io/mjlab/)

### Newton
- [GitHub](https://github.com/newton-physics/newton)
- [Docs](https://newton-physics.github.io/newton/)

## Acknowledgments

This skill incorporates knowledge from:
- **MuJoCo Community Lab** - For mjlab, combining Isaac Lab API with MuJoCo Warp
- **Newton Project** - A Linux Foundation initiative by Disney Research, Google DeepMind, and NVIDIA
- **NVIDIA** - For Isaac Lab/Sim and Warp
- **Google DeepMind** - For MuJoCo and MuJoCo Warp

## License

MIT License - See [LICENSE](../LICENSE)
