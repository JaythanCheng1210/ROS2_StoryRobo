import rclpy
from rclpy.node import Node
from std_srvs.srv import Trigger
import os, sys, math
import threading

sys.path.append('/home/storyrobo/storyrobo_ws/ROS2_StoryRobo/storyrobo_service/driver')
from Storyrobo_ControlCmd import ControlCmd

class RecordServiceServer(Node):
    def __init__(self):
        super().__init__('record_service_server')
        self.srv = self.create_service(Trigger, 'record_service', self.record_service_callback)
        self.get_logger().info('Record Service Server is ready.')

        self.controlcmd = ControlCmd()


    def record_service_callback(self, request, response):
        self.get_logger().info('Record service called.')
        if self.controlcmd.recording:
            self.get_logger().info('Stoping recording.')
            response.success = True
            response.message = 'Recording stopped successfully.'
            self.controlcmd.stop_record_action_points()
            self.controlcmd.recording = False
        else:
            self.get_logger().info('Starting recording.')
            response.success = True
            response.message = 'Recording started successfully.'
            self.controlcmd.start_record_action_points()
            self.controlcmd.recording = True
        
        return response


def main(args=None):
    rclpy.init(args=args)

    record_service_server = RecordServiceServer()

    rclpy.spin(record_service_server)

    rclpy.shutdown()

if __name__ == '__main__':
    main()
