# 🤖 Cobot Synchro 5 Digital Twin

A Gazebo Harmonic-based digital twin simulation for the **Cobot Synchro 5** robotic arm with ROS2 Humble integration.

![Gazebo](https://img.shields.io/badge/Gazebo-Harmonic-orange)
![ROS2](https://img.shields.io/badge/ROS2-Humble-blue)
![Ubuntu](https://img.shields.io/badge/Ubuntu-22.04%2F24.04-purple)

---

## 🎯 Overview

This digital twin implements **TRUE** control modes matching the real Synchro 5 robot:

| Controller | Control Flow | Description |
|------------|--------------|-------------|
| **Position** | position → PID → effort | Joint position control with PID feedback |
| **Velocity** | velocity → direct | Direct velocity control (NO kinematics conversion) |
| **Effort** | effort → direct | Direct torque control (NO gravity compensation) |

### ✨ Key Features

- ✅ **Three Control Modes** - Position, Velocity, and Effort
- ✅ **No Controller Overriding** - Separate world files for each control mode
- ✅ **Direct Velocity Control** - Not through inverse kinematics
- ✅ **Direct Effort Control** - Raw torque commands without gravity compensation
- ✅ **ROS2 Topic Bridging** - Standard Float64MultiArray interface
- ✅ **Same Interface as Real Robot** - Easy to switch between simulation and hardware

---

## 📁 Project Structure
```
cobot_digital_twin/
├── README.md
├── INSTALL.md
├── LICENSE
├── robots/
│   ├── heal_robot_position.sdf   # 6 JointPositionController
│   ├── heal_robot_velocity.sdf   # 6 JointController (velocity)
│   └── heal_robot_effort.sdf     # 6 JointController (force)
├── worlds/
│   ├── cobot_world_position.sdf
│   ├── cobot_world_velocity.sdf
│   └── cobot_world_effort.sdf
├── scripts/
│   ├── simple_bridge.py
│   ├── start_position.sh
│   └── start_velocity.sh
├── meshes/                       # 17 STL mesh files
└── docs/
    ├── ARCHITECTURE.md
    └── TROUBLESHOOTING.md
```

---

## 🔧 Requirements

| Software | Version |
|----------|---------|
| Ubuntu | 22.04 or 24.04 |
| Gazebo | Harmonic (gz-sim8) |
| ROS2 | Humble Hawksbill |

### Install Dependencies
```bash
sudo apt update
sudo apt install gz-harmonic ros-humble-desktop
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

---

## 🚀 Quick Start

### Clone Repository
```bash
cd ~
git clone https://github.com/jayInnovates/cobot_digital_twin.git
cd cobot_digital_twin
```

---

## 🎮 Position Control Mode

**Terminal 1 - Gazebo:**
```bash
cd ~/cobot_digital_twin
export GZ_SIM_RESOURCE_PATH=$(pwd):$(pwd)/meshes
gz sim worlds/cobot_world_position.sdf -r
```

**Terminal 2 - Bridge:**
```bash
cd ~/cobot_digital_twin
source /opt/ros/humble/setup.bash
python3 scripts/simple_bridge.py
```

**Terminal 3 - Commands:**
```bash
source /opt/ros/humble/setup.bash

# Move to position (radians)
ros2 topic pub --once /position_controller/commands std_msgs/msg/Float64MultiArray "{data: [0.5, -0.3, 0.2, 0.0, 0.1, 0.0]}"

# Return home
ros2 topic pub --once /position_controller/commands std_msgs/msg/Float64MultiArray "{data: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]}"
```

---

## 🎮 Velocity Control Mode

**Terminal 1 - Gazebo:**
```bash
cd ~/cobot_digital_twin
export GZ_SIM_RESOURCE_PATH=$(pwd):$(pwd)/meshes
gz sim worlds/cobot_world_velocity.sdf -r
```

**Terminal 2 - Bridge:**
```bash
cd ~/cobot_digital_twin
source /opt/ros/humble/setup.bash
python3 scripts/simple_bridge.py
```

**Terminal 3 - Commands:**
```bash
source /opt/ros/humble/setup.bash

# Rotate joint 1 at 0.3 rad/s (continuous)
ros2 topic pub /velocity_controller/commands std_msgs/msg/Float64MultiArray "{data: [0.3, 0.0, 0.0, 0.0, 0.0, 0.0]}" -r 10

# Stop (Ctrl+C then send zeros)
ros2 topic pub --once /velocity_controller/commands std_msgs/msg/Float64MultiArray "{data: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]}"
```

---

## 🎮 Effort Control Mode

⚠️ **Warning:** Robot will fall under gravity! No gravity compensation in this mode.

**Terminal 1 - Gazebo:**
```bash
cd ~/cobot_digital_twin
export GZ_SIM_RESOURCE_PATH=$(pwd):$(pwd)/meshes
gz sim worlds/cobot_world_effort.sdf -r
```

**Terminal 2 - Bridge:**
```bash
cd ~/cobot_digital_twin
source /opt/ros/humble/setup.bash
python3 scripts/simple_bridge.py
```

**Terminal 3 - Commands:**
```bash
source /opt/ros/humble/setup.bash

# Apply torque to joint 2 (Nm) - continuous
ros2 topic pub /effort_controller/commands std_msgs/msg/Float64MultiArray "{data: [0.0, 50.0, 0.0, 0.0, 0.0, 0.0]}" -r 10

# Stop
ros2 topic pub --once /effort_controller/commands std_msgs/msg/Float64MultiArray "{data: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]}"
```

---

## 🔌 ROS2 Topics

| Topic | Message Type | Description |
|-------|--------------|-------------|
| `/position_controller/commands` | `Float64MultiArray` | 6 joint positions (radians) |
| `/velocity_controller/commands` | `Float64MultiArray` | 6 joint velocities (rad/s) |
| `/effort_controller/commands` | `Float64MultiArray` | 6 joint torques (Nm) |

### Joint Order (Array Index)

| Index | Joint | Description |
|-------|-------|-------------|
| 0 | joint1 | Base rotation |
| 1 | joint2 | Shoulder |
| 2 | joint3 | Elbow |
| 3 | joint4 | Wrist 1 |
| 4 | joint5 | Wrist 2 |
| 5 | joint6 | Wrist 3 |

---

## 📊 Control Flow
```
Position Mode:  command → PID Controller → effort → joint
Velocity Mode:  command → direct velocity → joint
Effort Mode:    command → direct torque → joint (NO gravity comp)
```

---

## 🎮 Direct Gazebo Control (Without ROS2)
```bash
# Position
gz topic -t "/model/cobot/joint/joint1/cmd_pos" -m gz.msgs.Double -p "data: 1.0"

# Velocity
gz topic -t "/model/cobot/joint/joint1/cmd_vel" -m gz.msgs.Double -p "data: 0.5"

# Effort
gz topic -t "/model/cobot/joint/joint1/cmd_effort" -m gz.msgs.Double -p "data: 10.0"
```

---

## ⚠️ Known Limitations

1. **Mimic Constraint Warning** - Gripper shows mimic constraint error (harmless)
2. **Effort Mode Gravity** - Robot falls under gravity (by design, matches real robot)

---

## 🐛 Troubleshooting

**Robot not visible:**
```bash
export GZ_SIM_RESOURCE_PATH=$(pwd):$(pwd)/meshes
```

**Commands not working:**
- Ensure bridge is running
- Ensure correct world file is loaded

---

## 📜 License

MIT License

## 👤 Author

**Jay Vishwakarma** - [@jayInnovates](https://github.com/jayInnovates)

## 🙏 Acknowledgments

- Cobot Synchro 5 by Addverb Technologies
- Gazebo by Open Robotics
- ROS2 by Open Robotics
