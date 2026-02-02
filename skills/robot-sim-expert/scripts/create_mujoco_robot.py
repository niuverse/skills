#!/usr/bin/env python3
"""
快速创建 MuJoCo XML 机器人模型
Usage: python create_mujoco_robot.py --name quadruped --type quadruped
"""

import argparse
from pathlib import Path

QUADRUPED_XML = '''<mujoco model="{robot_name}">
  <compiler angle="radian" meshdir="./"/>
  
  <option timestep="0.002" iterations="50" solver="Newton"/>
  
  <default>
    <joint armature="0.01" damping="2" limited="true"/>
    <geom contype="1" conaffinity="1" friction="1.0 0.005 0.001"/>
  </default>
  
  <worldbody>
    <light diffuse="0.8 0.8 0.8" pos="0 0 5" dir="0 0 -1"/>
    <geom type="plane" size="100 100 0.1" rgba="0.9 0.9 0.9 1"/>
    
    <!-- 躯干 -->
    <body name="trunk" pos="0 0 0.4">
      <freejoint name="root"/>
      <geom type="box" size="0.2 0.1 0.05" mass="10"/>
      
      <!-- 前左腿 -->
      <body name="fr_hip" pos="0.15 0.08 -0.05">
        <joint name="fr_hip_joint" type="hinge" axis="1 0 0" range="-0.8 0.8"/>
        <geom type="cylinder" size="0.04 0.02" quat="0.707 0 0.707 0"/>
        
        <body name="fr_thigh" pos="0 -0.02 -0.05">
          <joint name="fr_thigh_joint" type="hinge" axis="0 1 0" range="-1.5 0.5"/>
          <geom type="capsule" size="0.03" fromto="0 0 0 0 0 -0.25"/>
          
          <body name="fr_calf" pos="0 0 -0.25">
            <joint name="fr_calf_joint" type="hinge" axis="0 1 0" range="-2.5 -0.5"/>
            <geom type="capsule" size="0.025" fromto="0 0 0 0 0 -0.25"/>
            
            <body name="fr_foot" pos="0 0 -0.25">
              <geom type="sphere" size="0.02" pos="0 0 -0.02"/>
              <site name="fr_foot_site" pos="0 0 0" size="0.01"/>
            </body>
          </body>
        </body>
      </body>
      
      <!-- 复制其他三条腿（fr, fl, rr, rl） -->
      
    </body>
  </worldbody>
  
  <actuator>
    <motor name="fr_hip_motor" joint="fr_hip_joint" gear="20" ctrllimited="true" ctrlrange="-20 20"/>
    <motor name="fr_thigh_motor" joint="fr_thigh_joint" gear="20" ctrllimited="true" ctrlrange="-20 20"/>
    <motor name="fr_calf_motor" joint="fr_calf_joint" gear="16" ctrllimited="true" ctrlrange="-16 16"/>
  </actuator>
  
  <sensor>
    <gyro name="trunk_gyro" site="imu"/>
    <accelerometer name="trunk_accel" site="imu"/>
    <jointpos name="joint_pos" joint="fr_hip_joint"/>
    <jointvel name="joint_vel" joint="fr_hip_joint"/>
  </sensor>
</mujoco>
'''

ARM_XML = '''<mujoco model="{robot_name}">
  <compiler angle="radian"/>
  
  <option timestep="0.002" iterations="50" solver="Newton"/>
  
  <default>
    <joint armature="0.1" damping="1" limited="true"/>
    <geom contype="1" conaffinity="1" friction="0.7"/>
  </default>
  
  <worldbody>
    <light diffuse="0.8 0.8 0.8" pos="0 0 5"/>
    <geom type="plane" size="2 2 0.1" rgba="0.9 0.9 0.9 1"/>
    
    <!-- 基座 -->
    <body name="base" pos="0 0 0.5">
      <geom type="cylinder" size="0.08 0.1" mass="5"/>
      
      <!-- 关节1: 旋转 -->
      <body name="link1" pos="0 0 0.1">
        <joint name="joint1" type="hinge" axis="0 0 1" range="-3.14 3.14"/>
        <geom type="cylinder" size="0.05 0.15" pos="0.1 0 0" quat="0.707 0 0.707 0"/>
        
        <!-- 关节2: 肩部 -->
        <body name="link2" pos="0.2 0 0">
          <joint name="joint2" type="hinge" axis="0 1 0" range="-1.57 1.57"/>
          
          <geom type="capsule" size="0.04" fromto="0 0 0 0 0 0.3"/>
          
          <!-- 关节3: 肘部 -->
          <body name="link3" pos="0 0 0.3">
            <joint name="joint3" type="hinge" axis="0 1 0" range="-1.8 0.5"/>
            
            <geom type="capsule" size="0.035" fromto="0 0 0 0 0 0.25"/>
            
            <!-- 末端执行器 -->
            <body name="ee" pos="0 0 0.25">
              <joint name="joint4" type="hinge" axis="0 0 1" range="-3.14 3.14"/>
              
              <geom type="sphere" size="0.03" rgba="1 0 0 1"/>
              
              <site name="ee_site" pos="0 0 0" size="0.01"/>
            </body>
          </body>
        </body>
      </body>
    </body>
  </worldbody>
  
  <actuator>
    <motor name="motor1" joint="joint1" gear="100" ctrlrange="-100 100"/>
    <motor name="motor2" joint="joint2" gear="50" ctrlrange="-50 50"/>
    <motor name="motor3" joint="joint3" gear="30" ctrlrange="-30 30"/>
    <motor name="motor4" joint="joint4" gear="10" ctrlrange="-10 10"/>
  </actuator>
  
  <sensor>
    <jointpos name="joint_pos" joint="joint1"/>
    <jointvel name="joint_vel" joint="joint1"/>
  </sensor>
</mujoco>
'''

def main():
    parser = argparse.ArgumentParser(description="Create MuJoCo robot XML template")
    parser.add_argument("--name", required=True, help="Robot name")
    parser.add_argument("--type", choices=["quadruped", "arm", "humanoid"], default="quadruped",
                        help="Robot type")
    parser.add_argument("--out", default=".", help="Output directory")
    args = parser.parse_args()
    
    templates = {
        "quadruped": QUADRUPED_XML,
        "arm": ARM_XML,
    }
    
    if args.type not in templates:
        print(f"❌ Type '{args.type}' template not yet implemented")
        return
    
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    
    xml_content = templates[args.type].format(robot_name=args.name)
    out_file = out_dir / f"{args.name}.xml"
    
    with open(out_file, "w") as f:
        f.write(xml_content)
    
    print(f"✅ Created {args.type} robot model: {out_file}")
    print(f"   Load with: model = mujoco.MjModel.from_xml_path('{out_file}')")


if __name__ == "__main__":
    main()
