import rclpy
from rclpy.node import Node
from std_srvs.srv import Trigger
import os, sys, math
import threading
import socketio
import time

sys.path.append('/home/storyrobo/storyrobo_ws/ROS2_StoryRobo/storyrobo_service/driver')
from Storyrobo_ControlCmd import ControlCmd        
controlcmd = ControlCmd()
# sio = socketio.Client()

class StoryRoboClient:
    def __init__(self, server_url):
        self.sio = socketio.Client()
        self.server_url = server_url

        self.send_real_time_data = False
        self.replay_mode = False

        # Register event handlers
        self.sio.on('connect', self.connect)
        self.sio.on('disconnect', self.disconnect)
        self.sio.on('response', self.response)
        self.sio.on('ReplayOnEchoBot', self.on_replay_data)
        self.sio.on('StatusOnEchoBot', self.StatusOnEchoBot)

    def connect(self):
        print('Connected to server')
        # if self.send_real_time_data:
        #     self.send_real_time_data_continuously()

    def send_real_time_data_continuously(self):
        while self.send_real_time_data:
            message = controlcmd.read_all_motor_data()
            self.sio.emit('EchoBotMotor', message)
            # time.sleep(1)  # Send data every second

    def on_replay_data(self, data):
        print('Received replay data:', data)
        if self.replay_mode:
            controlcmd.real_time_replay(data)

    def StatusOnEchoBot(self, status):
        print('Received command:', status)
        if status == "Connect" and controlcmd.recording == False and controlcmd.replaying == False:
            self.send_real_time_data = True
            time.sleep(0.5)
            self.replay_mode = False
            controlcmd.disable_all_motor()
            self.send_real_time_data_continuously()
        elif status == "Replay" and controlcmd.recording == False and controlcmd.replaying == False:
            self.send_real_time_data = False
            time.sleep(0.5)
            controlcmd.enable_all_motor()
            self.replay_mode = True
        elif status == "Replay stop":
            self.replay_mode = False
            controlcmd.disable_all_motor()

    def response(self, data):
        print('Server response:', data)

    def disconnect(self):
        print('Disconnected from server')

    def run(self):
        self.sio.connect(self.server_url)
        self.sio.wait()

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
            controlcmd.recording = False
            controlcmd.stop_record_action_points()
        else:
            self.get_logger().info('Starting recording.')
            response.success = True
            response.message = 'Recording started successfully.'
            controlcmd.recording = True
            time.sleep(3)
            controlcmd.start_record_action_points()
        
        return response

class ReplayServiceServer(Node):
    def __init__(self):
        super().__init__('replay_service_server')
        self.srv = self.create_service(Trigger, 'replay_service', self.replay_service_callback)
        self.get_logger().info('Replay Service Server is ready.')

    def replay_service_callback(self, request, response):
        self.get_logger().info('Replay service called.')
        if controlcmd.replaying:
            self.get_logger().info('Stopping replaying.')
            response.success = True
            response.message = 'Replaying stopped successfully.'
            controlcmd.replaying = False
            controlcmd.stop_replaying()
        else:
            response.success = True
            response.message = 'Replay started successfully.'
            controlcmd.replaying = True
            time.sleep(3)
            controlcmd.disable_all_motor()
        
        return response

def main(args=None):
    rclpy.init(args=args)

    record_service_server = RecordServiceServer()
    replay_service_server = ReplayServiceServer()

    # Initialize StoryRoboClient
    storyrobo_client = StoryRoboClient('http://10.100.3.116:5000')
    client_thread = threading.Thread(target=storyrobo_client.run)
    client_thread.start()

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
        storyrobo_client.sio.disconnect()  # Ensure the SocketIO client disconnects
        client_thread.join()

if __name__ == '__main__':
    main()

