# mjlab Workflow Guide

mjlab combines Isaac Lab's proven API with MuJoCo-Warp physics for lightweight, modular RL robotics research.

## Overview

**mjlab** bridges the gap between Isaac Lab's excellent API design and MuJoCo's superior physics engine:
- Uses **Isaac Lab API** for environment and task configuration
- Powered by **MuJoCo Warp** for GPU-accelerated physics
- Lightweight and modular for rapid experimentation
- Focused on sim-to-real deployment

## Quick Start

### Installation

```bash
# Using uv (recommended)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Run demo without installation
uvx --from mjlab \
  --with "mujoco-warp @ git+https://github.com/google-deepmind/mujoco_warp@1dc288cf1fa819fc3346ec5c9546e2cc2b7be667" \
  demo

# Or install from source
git clone https://github.com/mujocolab/mjlab.git
cd mjlab
uv run demo
```

### Requirements

- **NVIDIA GPU** required for training (CUDA)
- **macOS** supported only for evaluation (CPU, slower)
- Python 3.10+

## Training Examples

### 1. Velocity Tracking

Train a Unitree G1 humanoid to follow velocity commands:

```bash
# Single GPU
uv run train Mjlab-Velocity-Flat-Unitree-G1 \
  --env.scene.num-envs 4096

# Multi-GPU
uv run train Mjlab-Velocity-Flat-Unitree-G1 \
  --gpu-ids 0 1 \
  --env.scene.num-envs 4096
```

### 2. Motion Imitation

Train humanoid to mimic reference motions:

```bash
# Setup WandB
export WANDB_ENTITY=your-organization-name

# Process motion data
MUJOCO_GL=egl uv run src/mjlab/scripts/csv_to_npz.py \
  --input-file /path/to/motion.csv \
  --output-name dance_motion \
  --input-fps 30 \
  --output-fps 50 \
  --render  # Optional: preview video

# Train
uv run train Mjlab-Motion-Imitation-Unitree-G1 \
  --motion dance_motion
```

### 3. Evaluation

```bash
# Evaluate trained policy from WandB
uv run play Mjlab-Velocity-Flat-Unitree-G1 \
  --wandb-run-path your-org/mjlab/run-id

# Or evaluate local checkpoint
uv run play Mjlab-Velocity-Flat-Unitree-G1 \
  --checkpoint path/to/checkpoint.pt
```

## Task Configuration

### Pre-defined Tasks

| Task | Description |
|------|-------------|
| `Mjlab-Velocity-Flat-Unitree-G1` | Velocity tracking on flat terrain |
| `Mjlab-Velocity-Rough-Unitree-G1` | Velocity tracking on rough terrain |
| `Mjlab-Motion-Imitation-Unitree-G1` | Motion imitation from reference |

### Custom Task

```python
from mjlab.envs import MjlabEnvCfg
from mjlab.tasks import LocomotionTaskCfg

@configclass
class MyCustomTaskCfg(LocomotionTaskCfg):
    """Custom task configuration."""
    
    # Scene configuration
    scene: SceneCfg = MySceneCfg()
    
    # Rewards
    rewards: RewardCfg = RewardCfg({
        "tracking": RewardTermCfg(func=mjlab_mdp.tracking_reward, weight=1.0),
        "energy": RewardTermCfg(func=mjlab_mdp.energy_penalty, weight=-0.01),
    })
    
    # Terminations
    terminations: TerminationCfg = TerminationCfg({
        "time_out": TerminationTermCfg(func=mjlab_mdp.time_out, time_limit=20.0),
        "fall": TerminationTermCfg(func=mjlab_mdp.fall_detection),
    })
```

## Multi-GPU Training

```bash
# Data parallel across multiple GPUs
uv run train Mjlab-Velocity-Flat-Unitree-G1 \
  --gpu-ids 0 1 2 3 \
  --env.scene.num-envs 16384 \
  --algo.ppo.num_steps 24 \
  --algo.ppo.batch_size 8192
```

## Motion Dataset Management

### Upload to WandB

1. Create a registry collection named `Motions` in your WandB workspace
2. Process motion files:

```bash
uv run src/mjlab/scripts/csv_to_npz.py \
  --input-file motion.csv \
  --output-name my_motion \
  --input-fps 30 \
  --output-fps 50
```

3. Dataset will be automatically uploaded to WandB registry

### Use in Training

```bash
uv run train Mjlab-Motion-Imitation-Unitree-G1 \
  --motion my_motion
```

## Sim-to-Real Tips

### Domain Randomization

```python
@configclass
class DomainRandomizationCfg:
    # Physics parameters
    randomize_friction = True
    friction_range = [0.5, 1.2]
    
    # Mass randomization
    randomize_base_mass = True
    added_mass_range = [-1.0, 3.0]
    
    # Sensor noise
    add_imu_noise = True
    imu_noise_std = 0.01
```

### Observation Normalization

```python
# Use running statistics for observation normalization
obs_normalizer = RunningMeanStd(shape=obs_shape)
```

## Debugging

### Visualize in Browser

```bash
# Run with interactive Viser viewer
uv run demo --viewer viser

# Or use native MuJoCo viewer
uv run demo --viewer native
```

### Profile Performance

```bash
# Enable profiling
uv run train Mjlab-Velocity-Flat-Unitree-G1 \
  --profile \
  --profile-output profile.json
```

## References

- **GitHub**: https://github.com/mujocolab/mjlab
- **Documentation**: https://mujocolab.github.io/mjlab/
- **MuJoCo Warp**: https://github.com/google-deepmind/mujoco_warp
- **Isaac Lab**: https://github.com/isaac-sim/IsaacLab

## Acknowledgments

mjlab is developed by the MuJoCo Community Lab, combining the best of Isaac Lab's API design with MuJoCo's physics excellence.
