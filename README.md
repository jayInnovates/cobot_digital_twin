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

### ✨ Key Features

- ✅ **No Controller Overriding** - Separate world files for each control mode
- ✅ **Direct Velocity Control** - Not through inverse kinematics
- ✅ **ROS2 Topic Bridging** - Standard Float64MultiArray interface
- ✅ **Same Interface as Real Robot** - Easy to switch between simulation and hardware
- ✅ **Single System Ready** - Run everything on one Ubuntu machine with GUI

---

## 📁 Project Structure
```
cobot_digital_twin/
├── README.md                     # This file
├── INSTALL.md                    # Detailed installation guide
├── robots/
│   ├── heal_robot_position.sdf   # Robot with 6 JointPositionController
│   └── heal_robot_velocity.sdf   # Robot with 6 JointController
├── worlds/
│   ├── cobot_world_position.sdf  # World for position control mode
│   └── cobot_world_velocity.sdf  # World for velocity control mode
├── scripts/
│   ├── simple_bridge.py          # ROS2 <-> Gazebo bridge
│   ├── start_position.sh         # Quick start position mode
│   └── start_velocity.sh         # Quick start velocity mode
├── meshes/                       # 17 STL mesh files
│   ├── base_link.STL
│   ├── link1.STL - link5.STL
│   ├── end_effector.STL
│   └── (gripper meshes)
└── docs/
    ├── ARCHITECTURE.md           # System architecture
    └── TROUBLESHOOTING.md        # Common issues & solutions
```

---

## 🔧 Requirements

| Software | Version |
|----------|---------|
| Ubuntu | 22.04 or 24.04 |
| Gazebo | Harmonic (gz-sim8) |
| ROS2 | Humble Hawksbill |
| Python | 3.10+ |

---

## 🚀 Quick Start

### 1. Clone Repository
```bash
cd ~
git clone https://github.com/jayInnovates/cobot_digital_twin.git
cd cobot_digital_twin
```

### 2. Install Dependencies
```bash
# Install Gazebo Harmonic
sudo apt update
sudo apt install gz-harmonic

# Install ROS2 Humble (if not installed)
sudo apt install ros-humble-desktop

# Add ROS2 to bashrc
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

### 3. Run Position Control Mode

**Terminal 1 - Gazebo Server + GUI:**
```bash
cd ~/cobot_digital_twin
export GZ_SIM_RESOURCE_PATH=$(pwd):$(pwd)/meshes
gz sim worlds/cobot_world_position.sdf -r
```

**Terminal 2 - ROS2 Bridge:**
```bash
cd ~/cobot_digital_twin
source /opt/ros/humble/setup.bash
python3 scripts/simple_bridge.py
```

**Terminal 3 - Send Commands:**
```bash
source /opt/ros/humble/setup.bash

# Move robot to position (radians)
ros2 topic pub --once /position_controller/commands std_msgs/msg/Float64MultiArray "{data: [0.5, -0.3, 0.2, 0.0, 0.1, 0.0]}"

# Return to home
ros2 topic pub --once /position_controller/commands std_msgs/msg/Float64MultiArray "{data: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]}"
```

### 4. Run Velocity Control Mode

**Terminal 1 - Gazebo Server + GUI:**
```bash
cd ~/cobot_digital_twin
export GZ_SIM_RESOURCE_PATH=$(pwd):$(pwd)/meshes
gz sim worlds/cobot_world_velocity.sdf -r
```

**Terminal 2 - ROS2 Bridge:**
```bash
cd ~/cobot_digital_twin
source /opt/ros/humble/setup.bash
python3 scripts/simple_bridge.py
```

**Terminal 3 - Send Commands:**
```bash
source /opt/ros/humble/setup.bash

# Rotate joint 1 continuously at 0.3 rad/s
ros2 topic pub /velocity_controller/commands std_msgs/msg/Float64MultiArray "{data: [0.3, 0.0, 0.0, 0.0, 0.0, 0.0]}" -r 10

# Press Ctrl+C to stop
```

---

## 📊 Architecture
```
┌─────────────────────────────────────────────────────────────────┐
│                         USER COMMANDS                           │
│     ros2 topic pub /position_controller/commands ...            │
│     ros2 topic pub /velocity_controller/commands ...            │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                        ROS2 LAYER                               │
│  /position_controller/commands    /velocity_controller/commands │
│         (Float64MultiArray)              (Float64MultiArray)    │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    simple_bridge.py                             │
│         Splits array[6] → 6 individual Gazebo topics            │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                     GAZEBO LAYER                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Position Mode                      Velocity Mode               │
│  ┌───────────────────┐             ┌───────────────────┐       │
│  │JointPosition      │             │JointController    │       │
│  │Controller (x6)    │             │(x6)               │       │
│  │                   │             │                   │       │
│  │ position → PID    │             │ velocity → direct │       │
│  │         → effort  │             │                   │       │
│  └───────────────────┘             └───────────────────┘       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔌 ROS2 Topics

| Topic | Message Type | Description |
|-------|--------------|-------------|
| `/position_controller/commands` | `std_msgs/Float64MultiArray` | 6 joint positions (radians) |
| `/velocity_controller/commands` | `std_msgs/Float64MultiArray` | 6 joint velocities (rad/s) |

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

## 🎮 Direct Gazebo Control (Without ROS2)
```bash
# Position control - move joint 1 to 1.0 radian
gz topic -t "/model/cobot/joint/joint1/cmd_pos" -m gz.msgs.Double -p "data: 1.0"

# Velocity control - rotate joint 1 at 0.5 rad/s
gz topic -t "/model/cobot/joint/joint1/cmd_vel" -m gz.msgs.Double -p "data: 0.5"
```

---

## ⚙️ Controller Configuration

### Position Controller (PID Gains)

| Joints | P Gain | I Gain | D Gain |
|--------|--------|--------|--------|
| 1-3 | 1000 | 50 | 100 |
| 4-5 | 500 | 25 | 50 |
| 6 | 200 | 10 | 20 |

### Velocity Controller

Direct velocity control with `use_velocity_commands: true`

---

## ⚠️ Known Limitations

1. **Mimic Constraint Warning** - Gripper joints show mimic constraint error (harmless, gripper joints are fixed)
2. **DART Mesh Collision** - Mesh collisions not supported in DART physics (visual-only meshes work fine)

---

## 🐛 Troubleshooting

See [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) for common issues.

### Quick Fixes

**Robot not visible:**
```bash
export GZ_SIM_RESOURCE_PATH=$(pwd):$(pwd)/meshes
```

**Commands not working:**
```bash
# Check bridge is running
# Check correct world file loaded (position vs velocity)
```

---

## 📜 License

MIT License - See LICENSE file

---

## 👤 Author

**Jay Vishwakarma**
- GitHub: [@jayInnovates](https://github.com/jayInnovates)

---

## 🙏 Acknowledgments

- Cobot Synchro 5 by Addverb Technologies
- Gazebo by Open Robotics
- ROS2 Humble by Open Robotics
