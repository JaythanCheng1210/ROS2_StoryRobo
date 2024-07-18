import rclpy
from rclpy.node import Node
from std_srvs.srv import Trigger
import os, sys, math
import threading

sys.path.append('/home/storyrobo/storyrobo_ws/ROS2_StoryRobo/storyrobo_service/driver')
from Storyrobo_ControlCmd import ControlCmd

class ReplayServiceServer(Node):

    def __init__(self):
        super().__init__('replay_service_server')
        self.srv = self.create_service(Trigger, 'replay_service', self.replay_service_callback)
        self.get_logger().info('Replay Service Server is ready.')

        self.controlcmd = ControlCmd()

    def replay_service_callback(self, request, response):
        self.get_logger().info('Replay service called.')
        self.controlcmd.replaying = True
        response.success = True
        response.message = 'Replay started successfully.'
        self.controlcmd.replay_all()
        
        return response

def main(args=None):
    rclpy.init(args=args)

    replay_service_server = ReplayServiceServer() 

    rclpy.spin(replay_service_server)

    rclpy.shutdown()

if __name__ == '__main__':
    main()
