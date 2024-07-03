import rclpy
from rclpy.node import Node
from std_srvs.srv import Trigger
import RPi.GPIO as GPIO
import time

class TriggerServiceClient(Node):

    def __init__(self):
        super().__init__('trigger_service_client')

        # GPIO setup
        self.button1_pin = 16  # GPIO pin for button 1
        self.button2_pin = 18  # GPIO pin for button 2

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.button1_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.button2_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # Service clients
        self.record_client = self.create_client(Trigger, 'record_service')
        self.replay_client = self.create_client(Trigger, 'replay_service')

        while not self.record_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for record_service to become available...')
        while not self.replay_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for replay_service to become available...')

        self.recording = False
        self.get_logger().info('Trigger Service Client is ready.')

    def send_record_request(self):
        req = Trigger.Request()
        future = self.record_client.call_async(req)
        rclpy.spin_until_future_complete(self, future)
        return future.result()

    def send_replay_request(self):
        req = Trigger.Request()
        future = self.replay_client.call_async(req)
        rclpy.spin_until_future_complete(self, future)
        return future.result()

    def button_callback(self):
        while rclpy.ok():
            if GPIO.input(self.button1_pin) == GPIO.LOW:
                time.sleep(0.1)  # debounce
                if GPIO.input(self.button1_pin) == GPIO.LOW:
                    if not self.recording:
                        self.get_logger().info('Record Button pressed: Starting recording.')
                        response = self.send_record_request()
                        self.get_logger().info('Record response: %s' % response.message)
                        self.recording = True
                    else:
                        self.get_logger().info('Record Button second pressed: Stopping recording.')
                        response = self.send_record_request()
                        self.get_logger().info('Record response: %s' % response.message)
                        self.recording = False
                    time.sleep(1)  # delay to avoid multiple triggers

            if GPIO.input(self.button2_pin) == GPIO.LOW:
                time.sleep(0.1)  # debounce
                if GPIO.input(self.button2_pin) == GPIO.LOW:
                    self.get_logger().info('Button 2 pressed: Starting replay.')
                    response = self.send_replay_request()
                    self.get_logger().info('Replay response: %s' % response.message)
                    time.sleep(1)  # delay to avoid multiple triggers

def main(args=None):
    rclpy.init(args=args)

    trigger_service_client = TriggerServiceClient()

    try:
        trigger_service_client.button_callback()
    except KeyboardInterrupt:
        pass

    GPIO.cleanup()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
