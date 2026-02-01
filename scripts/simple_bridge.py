#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
import subprocess
import os

class SimpleBridge(Node):
    def __init__(self):
        super().__init__('simple_bridge')
        self.env = os.environ.copy()
        
        self.create_subscription(Float64MultiArray, '/position_controller/commands', self.position_cb, 10)
        self.create_subscription(Float64MultiArray, '/velocity_controller/commands', self.velocity_cb, 10)
        self.create_subscription(Float64MultiArray, '/effort_controller/commands', self.effort_cb, 10)
        
        self.get_logger().info('='*50)
        self.get_logger().info('Cobot Synchro 5 Digital Twin Bridge')
        self.get_logger().info('='*50)
        self.get_logger().info('Topics:')
        self.get_logger().info('  /position_controller/commands')
        self.get_logger().info('  /velocity_controller/commands')
        self.get_logger().info('  /effort_controller/commands')
        self.get_logger().info('='*50)
        
    def send_gz(self, topic, value):
        subprocess.Popen(['gz', 'topic', '-t', topic, '-m', 'gz.msgs.Double', '-p', f'data: {value}'],
            env=self.env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    def position_cb(self, msg):
        if len(msg.data) >= 6:
            self.get_logger().info(f'Position: {[round(x,2) for x in msg.data[:6]]}')
            for i, val in enumerate(msg.data[:6]):
                self.send_gz(f'/model/cobot/joint/joint{i+1}/cmd_pos', val)
    
    def velocity_cb(self, msg):
        if len(msg.data) >= 6:
            self.get_logger().info(f'Velocity: {[round(x,2) for x in msg.data[:6]]}')
            for i, val in enumerate(msg.data[:6]):
                self.send_gz(f'/model/cobot/joint/joint{i+1}/cmd_vel', val)

    def effort_cb(self, msg):
        if len(msg.data) >= 6:
            self.get_logger().info(f'Effort: {[round(x,2) for x in msg.data[:6]]}')
            for i, val in enumerate(msg.data[:6]):
                self.send_gz(f'/model/cobot/joint/joint{i+1}/cmd_effort', val)

def main():
    rclpy.init()
    rclpy.spin(SimpleBridge())
    rclpy.shutdown()

if __name__ == '__main__':
    main()
