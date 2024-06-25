import rclpy
from rclpy.node import Node
from std_srvs.srv import Trigger
import sys

class TriggerServiceClient(Node):

    def __init__(self, service_name):
        super().__init__('trigger_service_client')
        self.cli = self.create_client(Trigger, service_name)
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info(f'Service {service_name} not available, waiting again...')
        self.req = Trigger.Request()

    def send_request(self):
        self.future = self.cli.call_async(self.req)

def main(args=None):
    rclpy.init(args=args)

    if len(sys.argv) != 2 or sys.argv[1] not in ['record', 'replay']:
        print("Usage: ros2 run trigger_service_demo trigger_service_client [record|replay]")
        return

    service_name = f"{sys.argv[1]}_service"

    trigger_service_client = TriggerServiceClient(service_name)
    trigger_service_client.send_request()

    while rclpy.ok():
        rclpy.spin_once(trigger_service_client)
        if trigger_service_client.future.done():
            try:
                response = trigger_service_client.future.result()
            except Exception as e:
                trigger_service_client.get_logger().info('Service call failed %r' % (e,))
            else:
                trigger_service_client.get_logger().info('Service call success: %s' % (response.message,))
            break

    rclpy.shutdown()

if __name__ == '__main__':
    main()
