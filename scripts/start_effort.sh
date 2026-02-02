#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export GZ_SIM_RESOURCE_PATH="$SCRIPT_DIR:$SCRIPT_DIR/meshes"
echo "Starting Effort Control Mode..."
echo "WARNING: Robot will fall under gravity (no gravity compensation)"
gz sim -s "$SCRIPT_DIR/worlds/cobot_world_effort.sdf" -r
