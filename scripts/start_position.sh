#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export GZ_SIM_RESOURCE_PATH="$SCRIPT_DIR:$SCRIPT_DIR/meshes"
echo "Starting Position Control Mode..."
gz sim -s "$SCRIPT_DIR/worlds/cobot_world_position.sdf" -r
