# 🐛 Troubleshooting Guide

Common issues and solutions for the Cobot Digital Twin.

---

## ❌ Robot Not Visible in GUI

### Symptom
Gazebo opens but robot is invisible or shows as wireframe/broken.

### Solution
Set resource path before running:
```bash
cd ~/cobot_digital_twin
export GZ_SIM_RESOURCE_PATH=$(pwd):$(pwd)/meshes
gz sim worlds/cobot_world_position.sdf -r
```

---

## ❌ Commands Not Working

### Symptom
Publishing to ROS2 topics but robot doesn't move.

### Checklist

1. **Is bridge running?**
```bash
# Should show "Cobot Digital Twin Bridge"
python3 scripts/simple_bridge.py
```

2. **Correct world loaded?**
- Position commands → `cobot_world_position.sdf`
- Velocity commands → `cobot_world_velocity.sdf`

3. **ROS2 sourced?**
```bash
source /opt/ros/humble/setup.bash
```

---

## ❌ Mimic Constraint Error

### Symptom
```
[Err] Attempting to create a mimic constraint for joint [left_inner_knuckle_joint]...
```

### Solution
**This is harmless!** Gripper joints are fixed in simulation. The error doesn't affect robot arm functionality.

---

## ❌ OpenGL Error (VM/Remote Desktop)

### Symptom
```
OpenGL 3.3 not supported
```

### Solution
```bash
export LIBGL_ALWAYS_SOFTWARE=1
gz sim worlds/cobot_world_position.sdf -r
```

---

## ❌ GUI Not Opening

### Symptom
Gazebo runs but no window appears.

### Solution
Run with GUI flag:
```bash
gz sim worlds/cobot_world_position.sdf -r
# NOT: gz sim -s worlds/... (server only)
```

---

## ❌ Bridge Import Error

### Symptom
```
ModuleNotFoundError: No module named 'rclpy'
```

### Solution
```bash
source /opt/ros/humble/setup.bash
python3 scripts/simple_bridge.py
```

---

## 🔧 Debug Commands

### Check Gazebo Topics
```bash
gz topic -l | grep cobot
```

### Check ROS2 Topics
```bash
ros2 topic list | grep controller
```

### Test Direct Gazebo Control
```bash
gz topic -t "/model/cobot/joint/joint1/cmd_pos" -m gz.msgs.Double -p "data: 1.0"
```

### Check File Counts
```bash
echo "Meshes: $(ls meshes/*.STL | wc -l)"
echo "Robots: $(ls robots/*.sdf | wc -l)"
echo "Worlds: $(ls worlds/*.sdf | wc -l)"
```
