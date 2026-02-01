# 📦 Installation Guide

Complete step-by-step guide to set up the Cobot Synchro 5 Digital Twin on Ubuntu.

---

## 🖥️ System Requirements

| Component | Requirement |
|-----------|-------------|
| OS | Ubuntu 22.04 LTS or 24.04 LTS |
| RAM | 8 GB minimum (16 GB recommended) |
| GPU | OpenGL 3.3+ compatible |
| Disk | 2 GB free space |

---

## 📥 Step 1: Install Gazebo Harmonic
```bash
# Update package list
sudo apt update

# Install Gazebo Harmonic
sudo apt install -y gz-harmonic

# Verify installation
gz sim --version
# Should show: Gazebo Sim, version 8.x.x
```

---

## 📥 Step 2: Install ROS2 Humble

### Option A: Full Desktop Install (Recommended)
```bash
# Set locale
sudo apt update && sudo apt install -y locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8

# Setup sources
sudo apt install -y software-properties-common
sudo add-apt-repository universe
sudo apt update && sudo apt install -y curl
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

# Install ROS2 Humble Desktop
sudo apt update
sudo apt install -y ros-humble-desktop

# Add to bashrc
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

### Option B: Minimal Install
```bash
sudo apt install -y ros-humble-ros-base
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

### Verify ROS2 Installation
```bash
ros2 --version
# Should show: ros2 0.x.x
```

---

## 📥 Step 3: Clone This Repository
```bash
cd ~
git clone https://github.com/jayInnovates/cobot_digital_twin.git
cd cobot_digital_twin
```

---

## 📥 Step 4: Verify Files
```bash
# Check all files present
echo "Meshes: $(ls meshes/*.STL | wc -l) (should be 17)"
echo "Robots: $(ls robots/*.sdf | wc -l) (should be 2)"
echo "Worlds: $(ls worlds/*.sdf | wc -l) (should be 2)"
echo "Scripts: $(ls scripts/*.py scripts/*.sh | wc -l) (should be 3)"
```

Expected output:
```
Meshes: 17 (should be 17)
Robots: 2 (should be 2)
Worlds: 2 (should be 2)
Scripts: 3 (should be 3)
```

---

## 🧪 Step 5: Test Installation

### Test 1: Gazebo Loads World
```bash
cd ~/cobot_digital_twin
export GZ_SIM_RESOURCE_PATH=$(pwd):$(pwd)/meshes
gz sim worlds/cobot_world_position.sdf -r
```

✅ **Success:** Gazebo GUI opens with robot visible on table

### Test 2: Bridge Runs

Open new terminal:
```bash
cd ~/cobot_digital_twin
source /opt/ros/humble/setup.bash
python3 scripts/simple_bridge.py
```

✅ **Success:** Shows "Cobot Digital Twin Bridge" and topic list

### Test 3: Robot Responds

Open new terminal:
```bash
source /opt/ros/humble/setup.bash
ros2 topic pub --once /position_controller/commands std_msgs/msg/Float64MultiArray "{data: [0.5, 0.0, 0.0, 0.0, 0.0, 0.0]}"
```

✅ **Success:** Robot joint 1 moves in Gazebo GUI

---

## 🎉 Installation Complete!

You're ready to use the Cobot Synchro 5 Digital Twin.

See [README.md](README.md) for usage instructions.
