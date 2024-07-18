import rclpy
from rclpy.node import Node
from std_srvs.srv import Trigger
import os, sys, math
import threading

sys.path.append('/home/storyrobo/storyrobo_ws/ROS2_StoryRobo/storyrobo_service/driver')
from Storyrobo_ControlCmd import ControlCmd        
controlcmd = ControlCmd()

class RecordServiceServer(Node):
    def __init__(self):
        super().__init__('record_service_server')
        self.srv = self.create_service(Trigger, 'record_service', self.record_service_callback)
        self.get_logger().info('Record Service Server is ready.')

    def record_service_callback(self, request, response):
        self.get_logger().info('Record service called.')
        if controlcmd.recording:
            self.get_logger().info('Stopping recording.')
            response.success = True
            response.message = 'Recording stopped successfully.'
            controlcmd.stop_record_action_points()
            controlcmd.recording = False
        else:
            self.get_logger().info('Starting recording.')
            response.success = True
            response.message = 'Recording started successfully.'
            controlcmd.start_record_action_points()
            controlcmd.recording = True
        
        return response

class ReplayServiceServer(Node):
    def __init__(self):
        super().__init__('replay_service_server')
        self.srv = self.create_service(Trigger, 'replay_service', self.replay_service_callback)
        self.get_logger().info('Replay Service Server is ready.')

    def replay_service_callback(self, request, response):
        self.get_logger().info('Replay service called.')
        response.success = True
        response.message = 'Replay started successfully.'
        controlcmd.replay_all()
        
        return response

def main(args=None):
    rclpy.init(args=args)

    record_service_server = RecordServiceServer()
    replay_service_server = ReplayServiceServer()

    # Using a MultiThreadedExecutor to handle both nodes
    executor = rclpy.executors.MultiThreadedExecutor()
    executor.add_node(record_service_server)
    executor.add_node(replay_service_server)

    try:
        executor.spin()
    finally:
        executor.shutdown()
        record_service_server.destroy_node()
        replay_service_server.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
