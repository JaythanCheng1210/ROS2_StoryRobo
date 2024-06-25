import rclpy
from rclpy.node import Node
from std_srvs.srv import Trigger

class ReplayServiceServer(Node):

    def __init__(self):
        super().__init__('replay_service_server')
        self.srv = self.create_service(Trigger, 'replay_service', self.replay_service_callback)
        self.get_logger().info('Replay Service Server is ready.')

    def replay_service_callback(self, request, response):
        self.get_logger().info('Replay service called.')
        response.success = True
        response.message = 'Replay started successfully.'
        return response

def main(args=None):
    rclpy.init(args=args)

    replay_service_server = ReplayServiceServer()

    rclpy.spin(replay_service_server)

    rclpy.shutdown()

if __name__ == '__main__':
    main()
