#!/bin/bash

echo "========================================"
echo "  Cobot Synchro 5 Digital Twin Setup"
echo "========================================"

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Set resource path
export GZ_SIM_RESOURCE_PATH="$SCRIPT_DIR:$SCRIPT_DIR/meshes"

echo ""
echo "Select control mode:"
echo "  1) Position Control"
echo "  2) Velocity Control"
echo ""
read -p "Enter choice (1 or 2): " choice

case $choice in
    1)
        echo "Starting Position Control Mode..."
        WORLD_FILE="worlds/cobot_world_position.sdf"
        ;;
    2)
        echo "Starting Velocity Control Mode..."
        WORLD_FILE="worlds/cobot_world_velocity.sdf"
        ;;
    *)
        echo "Invalid choice!"
        exit 1
        ;;
esac

echo ""
echo "Starting Gazebo server..."
echo "Open new terminals for:"
echo "  - Bridge: cd $SCRIPT_DIR && source /opt/ros/humble/setup.bash && python3 scripts/simple_bridge.py"
echo "  - Test:   source /opt/ros/humble/setup.bash && ros2 topic pub ..."
echo ""

gz sim -s "$WORLD_FILE" -r
