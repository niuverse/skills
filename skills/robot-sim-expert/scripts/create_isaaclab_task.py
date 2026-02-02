#!/usr/bin/env python3
"""
快速创建 Isaac Lab 任务模板
Usage: python create_isaaclab_task.py --name MyTask --robot anymal_d
"""

import argparse
import os
from pathlib import Path

TASK_TEMPLATE = '''"""{task_name} Task Configuration for Isaac Lab."""

from omni.isaac.lab.utils import configclass
from omni.isaac.lab.envs import ManagerBasedRLEnvCfg
from omni.isaac.lab.scene import InteractiveSceneCfg
from omni.isaac.lab.managers import ObservationManagerCfg, RewardManagerCfg, TerminationManagerCfg
from omni.isaac.lab_tasks.manager_based.locomotion.velocity.velocity_env_cfg import LocomotionVelocityRoughEnvCfg


@configclass
class {task_class}Cfg(LocomotionVelocityRoughEnvCfg):
    """Configuration for the {task_name} task."""
    
    def __post_init__(self):
        """Post initialization."""
        super().__post_init__()
        
        # Scene config
        self.scene.num_envs = 4096
        self.scene.env_spacing = 4.0
        
        # Observation space
        self.observations.policy.height_scan = None
        
        # Rewards
        self.rewards.track_lin_vel_xy_exp.weight = 1.5
        self.rewards.track_ang_vel_z_exp.weight = 0.75
        
        # Terminations
        self.terminations.base_contact.params["sensor_cfg"].body_names = ["base"]


@configclass
class {task_class}AgileCfg({task_class}Cfg):
    """Agile version with higher rewards for speed."""
    
    def __post_init__(self):
        super().__post_init__()
        self.rewards.track_lin_vel_xy_exp.weight = 3.0
        self.rewards.track_ang_vel_z_exp.weight = 1.5
'''

MDP_TEMPLATE = '''"""MDP functions for {task_name} task."""

import torch
from typing import Optional

from omni.isaac.lab.envs import ManagerBasedRLEnv
from omni.isaac.lab.managers import SceneEntityCfg


def custom_reward(env: ManagerBasedRLEnv, asset_cfg: SceneEntityCfg = SceneEntityCfg("robot")) -> torch.Tensor:
    """Custom reward function template."""
    asset = env.scene[asset_cfg.name]
    # Implement your reward logic here
    reward = torch.zeros(env.num_envs, device=env.device)
    return reward


def custom_termination(env: ManagerBasedRLEnv, asset_cfg: SceneEntityCfg = SceneEntityCfg("robot"), max_height: float = 2.0) -> torch.Tensor:
    """Custom termination condition."""
    asset = env.scene[asset_cfg.name]
    height = asset.data.root_pos_w[:, 2]
    return height > max_height
'''

def main():
    parser = argparse.ArgumentParser(description="Create Isaac Lab task template")
    parser.add_argument("--name", required=True, help="Task name (e.g., MyTask)")
    parser.add_argument("--robot", default="anymal_d", help="Robot asset name")
    parser.add_argument("--out", default=".", help="Output directory")
    args = parser.parse_args()
    
    task_class = args.name.replace("_", " ").title().replace(" ", "")
    out_dir = Path(args.out) / f"{args.name.lower()}_task"
    
    # Create directories
    (out_dir / "mdp").mkdir(parents=True, exist_ok=True)
    
    # Write files
    with open(out_dir / "env_cfg.py", "w") as f:
        f.write(TASK_TEMPLATE.format(task_name=args.name, task_class=task_class))
    
    with open(out_dir / "mdp" / "__init__.py", "w") as f:
        f.write('"""MDP functions."""\n')
    
    with open(out_dir / "mdp" / "rewards.py", "w") as f:
        f.write(MDP_TEMPLATE.format(task_name=args.name))
    
    print(f"✅ Created task template at: {out_dir}")
    print(f"   - env_cfg.py: Environment configuration")
    print(f"   - mdp/rewards.py: Custom reward functions")


if __name__ == "__main__":
    main()
