# Newton Workflow Guide

Newton is a GPU-accelerated physics simulation engine built on NVIDIA Warp, targeting roboticists and simulation researchers.

## Overview

**Newton** extends Warp's deprecated `warp.sim` module and integrates **MuJoCo Warp** as its primary backend:
- GPU-based computation with NVIDIA Warp
- OpenUSD support for scene composition
- Differentiable physics for gradient-based optimization
- User-defined extensibility
- Community-driven (Linux Foundation project)
- Initiated by Disney Research, Google DeepMind, and NVIDIA

**⚠️ Beta Status**: API is unstable, breaking changes expected.

## Quick Start

### Installation

```bash
# Using uv (recommended during alpha)
git clone git@github.com:newton-physics/newton.git
cd newton

# Sync environment
uv sync --extra examples

# Run basic example
uv run -m newton.examples basic_pendulum
```

### Requirements

- NVIDIA GPU (for GPU acceleration)
- Python 3.10+
- Linux recommended (Windows/macOS support limited)

## Basic Examples

### 1. Simple Pendulum

```bash
uv run -m newton.examples basic_pendulum
```

```python
import newton as nt

# Create simulation
sim = nt.Simulation()

# Add pendulum
pendulum = sim.add_articulation(
    xml="""
    <mujoco>
      <worldbody>
        <body name="pole" pos="0 0 1">
          <joint name="hinge" type="hinge" axis="0 1 0"/>
          <geom type="capsule" size="0.05" fromto="0 0 0 0 0 1"/>
        </body>
      </worldbody>
    </mujoco>
    """
)

# Run simulation
for _ in range(1000):
    sim.step()
```

### 2. Load URDF

```bash
uv run -m newton.examples basic_urdf
```

```python
import newton as nt

# Load robot from URDF
robot = nt.load_urdf("path/to/robot.urdf")

# Create simulation
sim = nt.Simulation()
sim.add_articulation(robot)

# Access joints
joints = robot.get_joints()
for joint in joints:
    print(f"{joint.name}: {joint.range}")
```

### 3. Interactive Viewer

```bash
uv run -m newton.examples basic_viewer
```

```python
import newton as nt

sim = nt.Simulation()
robot = sim.add_articulation(urdf_path)

# Launch viewer
with nt.Viewer(sim) as viewer:
    while viewer.is_running():
        sim.step()
        viewer.sync()
```

## OpenUSD Integration

### Create USD Scene

```python
from newton.usd import Stage, create_scene

# Create OpenUSD stage
stage = Stage.CreateNew("scene.usd")

# Add ground plane
ground = create_scene.add_ground_plane(stage, size=10.0)

# Add robot from MJCF
robot = create_scene.add_articulation(
    stage,
    xml_path="robot.mjcf",
    position=(0, 0, 1.0)
)

# Save stage
stage.Save()
```

### Import USD to Simulation

```python
import newton as nt

# Load USD scene
sim = nt.Simulation.from_usd("scene.usd")

# Run simulation
sim.run(duration=10.0)
```

## Differentiable Simulation

### Gradient-Based Optimization

```python
import newton as nt
import warp as wp

# Create differentiable sim
sim = nt.Simulation(requires_grad=True)
robot = sim.add_articulation(urdf_path)

# Define target
target_position = wp.vec3(1.0, 0.0, 0.5)

# Optimization loop
for iteration in range(100):
    # Forward simulation
    sim.reset()
    for _ in range(100):
        robot.set_joint_positions(actions)
        sim.step()
    
    # Compute loss
    end_effector_pos = robot.get_body("ee_link").position
    loss = wp.length(end_effector_pos - target_position)
    
    # Backward pass
    wp.backward(loss)
    
    # Update actions
    actions -= learning_rate * actions.grad
```

### System Identification

```python
# Optimize simulation parameters to match real data
params = sim.create_parameters([
    "friction",
    "mass",
    "damping"
])

for _ in range(iterations):
    sim.set_parameters(params)
    sim.run_trajectory(trajectory)
    
    loss = compute_mse(sim.states, real_data)
    wp.backward(loss)
    
    params -= lr * params.grad
```

## Advanced Features

### Custom Forces

```python
import warp as wp

@wp.kernel
def apply_wind_force(
    positions: wp.array(dtype=wp.vec3),
    forces: wp.array(dtype=wp.vec3),
    wind_direction: wp.vec3,
    wind_strength: float
):
    tid = wp.tid()
    # Custom wind force calculation
    forces[tid] = wind_direction * wind_strength * wp.length(positions[tid])

# Register custom force
sim.add_force_kernel(apply_wind_force)
```

### Sensors

```python
# Add IMU sensor
imu = robot.add_sensor(
    type="imu",
    body="torso",
    position=(0, 0, 0.1)
)

# Read sensor data
sim.step()
acceleration = imu.linear_acceleration
angular_vel = imu.angular_velocity
```

### Collision Detection

```python
# Enable collision detection
sim.enable_collision_detection()

# Define collision pairs
sim.add_collision_pair(
    body_a="robot/hand",
    body_b="object/box"
)

# Check contacts
contacts = sim.get_contacts()
for contact in contacts:
    print(f"Contact: {contact.body_a} - {contact.body_b}")
    print(f"Force: {contact.force}")
```

## Performance Optimization

### GPU Batch Simulation

```python
# Run multiple environments in parallel
num_envs = 1024
sim = nt.Simulation(batch_size=num_envs)

# Vectorized operations
actions = wp.array(actions, shape=(num_envs, num_actions))
robot.set_joint_positions(actions)  # Applied to all envs
```

### Memory Management

```python
# Pre-allocate buffers for better performance
sim.allocate_buffers(
    max_steps=1000,
    num_bodies=100
)

# Reuse simulation context
with sim.context() as ctx:
    for episode in range(1000):
        ctx.reset()
        for step in range(100):
            ctx.step()
```

## Debugging Tools

### Visualization

```python
# Enable debug visualization
sim.set_debug_mode(
    show_contacts=True,
    show_joints=True,
    show_collision_shapes=True
)
```

### State Inspection

```python
# Get full state
state = sim.get_state()
print(f"Positions: {state.q}")
print(f"Velocities: {state.qd}")
print(f"Accelerations: {state.qdd}")

# Set state (for debugging)
sim.set_state(initial_state)
```

## Sim-to-Real

### Domain Randomization

```python
@dataclass
class RandomizationCfg:
    randomize_friction: bool = True
    friction_range: tuple = (0.5, 1.5)
    
    randomize_mass: bool = True
    mass_range: tuple = (0.8, 1.2)
    
    randomize_damping: bool = True
    damping_range: tuple = (0.9, 1.1)

def apply_randomization(sim, cfg):
    if cfg.randomize_friction:
        friction = random.uniform(*cfg.friction_range)
        sim.set_friction(friction)
```

### Export to MuJoCo

```python
# Export Newton sim to MuJoCo XML
sim.export_to_mjcf("robot_export.xml")

# Or to URDF
sim.export_to_urdf("robot_export.urdf")
```

## References

- **GitHub**: https://github.com/newton-physics/newton
- **Documentation**: https://newton-physics.github.io/newton/
- **NVIDIA Warp**: https://github.com/NVIDIA/warp
- **MuJoCo Warp**: https://github.com/google-deepmind/mujoco_warp
- **OpenUSD**: https://openusd.org/

## Acknowledgments

Newton is a Linux Foundation project initiated by Disney Research, Google DeepMind, and NVIDIA. It represents a community-driven effort to advance GPU-accelerated robotics simulation.
