# Robot Simulation Expert

🤖 Expert-level skill for robot simulation with Isaac Lab, Isaac Sim, and MuJoCo.

## Overview

This skill provides comprehensive expertise for:
- **Isaac Lab/Sim**: NVIDIA's high-fidelity robotics simulation platform
- **MuJoCo**: DeepMind's physics engine for robotics
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

## Framework Comparison

| Feature | Isaac Lab/Sim | MuJoCo |
|---------|---------------|--------|
| GPU Acceleration | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Rendering Quality | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Open Source | Partial | Full |
| Learning Curve | Steep | Gentle |
| RL Framework | Built-in | External |

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
    └── mujoco-workflow.md        # MuJoCo guide
```

## References

- [Isaac Lab GitHub](https://github.com/isaac-sim/IsaacLab)
- [Isaac Lab Docs](https://isaac-sim.github.io/IsaacLab/)
- [MuJoCo Docs](https://mujoco.readthedocs.io/)
- [MuJoCo GitHub](https://github.com/google-deepmind/mujoco)

## License

MIT License - See [LICENSE](../LICENSE)
