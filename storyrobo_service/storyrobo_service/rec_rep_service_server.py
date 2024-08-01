import rclpy
from rclpy.node import Node
from std_srvs.srv import Trigger
import os, sys, math
import threading
import socketio
import time

#For audio
import pyaudio
import wave
import sounddevice as sd
import soundfile as sf
from playsound import playsound

sys.path.append('/home/storyrobo/storyrobo_ws/ROS2_StoryRobo/storyrobo_service/driver')
from Storyrobo_ControlCmd import ControlCmd        
controlcmd = ControlCmd()

# sio = socketio.Client()
# class SharedState:
#     def __init__(self):
#         self.send_real_time_data= False

# sharedstate = SharedState()

# class StoryRoboClient:
    # def __init__(self, server_url):
    #     self.sio = socketio.Client()
    #     self.server_url = server_url
    #     self.unity_audio_store_path = '/home/storyrobo/storyrobo_ws/ROS2_StoryRobo/storyrobo_service/driver/data_unity'
    #     # self.unity_audio_path = os.path.join(self.unity_audio_store_path, 'output.wav')

    #     self.replay_mode = False
    #     self.record_mode = False
    #     self.unity_record = False

    #     # Register event handlers
    #     self.sio.on('connect', self.connect)
    #     self.sio.on('disconnect', self.disconnect)
    #     self.sio.on('response', self.response)
    #     self.sio.on('ReplayOnEchoBot', self.on_replay_data)
    #     self.sio.on('StatusOnEchoBot', self.StatusOnEchoBot)
    #     self.sio.on('NewAudioFromUnity', self.NewAudioFromUnity)
    #     self.sio.on('AudioToReplay', self.AudioToReplay)

    # def connect(self):
    #     print('Connected to server')
    #     # if self.send_real_time_data:
    #     #     self.send_real_time_data_continuously()

    # def send_real_time_data_continuously(self):
    #     while sharedstate.send_real_time_data:
    #         message = controlcmd.read_all_motor_data()
    #         self.sio.emit('EchoBotMotor', message)
    #         # time.sleep(1)  # Send data every second

    # def on_replay_data(self, data):
    #     print('Received replay data:', data)
    #     if self.replay_mode:
    #         controlcmd.real_time_replay(data)
    
    # def NewAudioFromUnity(self, newAudioname):
    #     print('Received replay data:', newAudioname)
    #     self.unity_audio_path = os.path.join(self.unity_audio_store_path, newAudioname + ".wav")

            
    # def AudioToReplay(self, Audioname):
    #     print('Received replay data:', Audioname)
    #     self.unity_audio_fiilename = Audioname

    # def StatusOnEchoBot(self, status):

    #     print('Received command:', status)
    #     # self.get_logger().info(f'Received command: {status}')
    #     if status == "Connect" :
    #         sharedstate.send_real_time_data = True
    #         time.sleep(0.5)
    #         self.replay_mode = False
    #         controlcmd.disable_all_motor()
    #         self.send_real_time_data_continuously()
    #     elif status == "Disconnect":
    #         sharedstate.send_real_time_data = False

    #     if status == "Replay" :
    #         sharedstate.send_real_time_data = False
    #         time.sleep(0.5)
    #         controlcmd.enable_all_motor()
    #         self.replay_mode = True
    #         self.replay_audio_thread = threading.Thread(target=self.unity_replay_audio, args=(self.unity_audio_fiilename, ), daemon=True)
    #         self.replay_audio_thread.start()

    #     elif status == "Replay stop":
    #         self.replay_mode = False
    #         controlcmd.disable_all_motor()
        
    #     if status == "Record":
    #         self.record_mode = True
    #         self.unity_record_audio(self.unity_audio_path)
    #         # controlcmd.start_record_audio_action_points()
    #     elif status == "Record stop":
    #         self.record_mode = False
    #         # controlcmd.stop_record_action_points()

    # def response(self, data):
    #     print('Server response:', data)

    # def disconnect(self):
    #     print('Disconnected from server')

    # def run(self):
    #     self.sio.connect(self.server_url)
    #     self.sio.wait()

    # def unity_record_audio(self, audio_path):
    #     # global recording
    #     FRAMES_PER_BUFFER = 4096
    #     FORMAT = pyaudio.paInt16
    #     CHANNELS = 1
    #     RATE = 48000
    #     p = pyaudio.PyAudio()
        
    #     stream = p.open(
    #                         format              =   FORMAT,
    #                         channels            =   CHANNELS,
    #                         rate                =   RATE,
    #                         input               =   True,
    #                         frames_per_buffer   =   FRAMES_PER_BUFFER,
    #                     )

    #     print("Start recording audio...")
    #     frames = []
    
    #     while self.record_mode == True :
    #         data = stream.read(FRAMES_PER_BUFFER)
    #         frames.append(data)
            
    #         # Check for event to stop recording
    #         if self.record_mode == False :
    #             break

    #     print("Stop recording audio!")
        
    #     stream.stop_stream()
    #     stream.close()
    #     p.terminate()

    #     obj = wave.open(audio_path, "wb")
    #     obj.setnchannels(CHANNELS)
    #     obj.setsampwidth(p.get_sample_size(FORMAT))
    #     obj.setframerate(RATE)
    #     obj.writeframes(b"".join(frames))
    #     obj.close()
            
    #     print("Audio stored...")
    #     return   

    # def unity_replay_audio(self, audio_path):
    #     playsound('/home/storyrobo/storyrobo_ws/ROS2_StoryRobo/storyrobo_service/driver/data_unity/' + audio_path + '.wav')

class RecordServiceServer(Node):
    def __init__(self, server_url):
        super().__init__('record_service_server')
        self.srv = self.create_service(Trigger, 'record_service', self.record_service_callback)
        self.get_logger().info('Record Service Server is ready.')

        self.sio = socketio.Client()
        self.server_url = server_url
        self.unity_audio_store_path = '/home/storyrobo/storyrobo_ws/ROS2_StoryRobo/storyrobo_service/driver/data_unity'
        # self.unity_audio_path = os.path.join(self.unity_audio_store_path, 'output.wav')

        self.replay_mode = False
        self.record_mode = False
        self.unity_record = False

        # Register event handlers
        self.sio.on('connect', self.connect)
        self.sio.on('disconnect', self.disconnect)
        self.sio.on('response', self.response)
        self.sio.on('ReplayOnEchoBot', self.on_replay_data)
        self.sio.on('StatusOnEchoBot', self.StatusOnEchoBot)
        self.sio.on('NewAudioFromUnity', self.NewAudioFromUnity)
        self.sio.on('AudioToReplay', self.AudioToReplay)

    def connect(self):
        print('Connected to server')
        # if self.send_real_time_data:
        #     self.send_real_time_data_continuously()

    def send_real_time_data_continuously(self):
        while controlcmd.send_real_time_data:
            message = controlcmd.read_all_motor_data()
            self.sio.emit('EchoBotMotor', message)
            # time.sleep(1)  # Send data every second

    def on_replay_data(self, data):
        print('Received replay data:', data)
        if self.replay_mode:
            # time.sleep(0.2)
            controlcmd.real_time_replay(data)
    
    def NewAudioFromUnity(self, newAudioname):
        print('Received replay data:', newAudioname)
        self.unity_audio_path = os.path.join(self.unity_audio_store_path, newAudioname + ".wav")

            
    def AudioToReplay(self, Audioname):
        print('Received replay data:', Audioname)
        self.unity_audio_fiilename = Audioname

    def StatusOnEchoBot(self, status):

        print('Received command:', status)
        # self.get_logger().info(f'Received command: {status}')
        if status == "Connect" :
            controlcmd.send_real_time_data = True
            time.sleep(0.5)
            self.replay_mode = False
            controlcmd.disable_all_motor()
            self.send_real_time_data_continuously()
        elif status == "Disconnect":
            controlcmd.send_real_time_data = False

        if status == "Replay" :
            controlcmd.send_real_time_data = False
            time.sleep(0.5)
            controlcmd.enable_all_motor()
            self.replay_mode = True
            self.replay_audio_thread = threading.Thread(target=self.unity_replay_audio, args=(self.unity_audio_fiilename, ), daemon=True)
            self.replay_audio_thread.start()

        elif status == "Replay stop":
            self.replay_mode = False
            controlcmd.disable_all_motor()

        if status == "Record":
            self.record_mode = True
            self.unity_record_audio(self.unity_audio_path)
            # controlcmd.start_record_audio_action_points()
        elif status == "Record stop":
            self.record_mode = False
            # controlcmd.stop_record_action_points()

    def response(self, data):
        print('Server response:', data)

    def disconnect(self):
        print('Disconnected from server')

    def run(self):
        self.sio.connect(self.server_url)
        self.sio.wait()

    def unity_record_audio(self, audio_path):
        # global recording
        FRAMES_PER_BUFFER = 4096
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 48000
        p = pyaudio.PyAudio()
        
        stream = p.open(
                            format              =   FORMAT,
                            channels            =   CHANNELS,
                            rate                =   RATE,
                            input               =   True,
                            frames_per_buffer   =   FRAMES_PER_BUFFER,
                        )

        print("Start recording audio...")
        frames = []
    
        while self.record_mode == True :
            data = stream.read(FRAMES_PER_BUFFER)
            frames.append(data)
            
            # Check for event to stop recording
            if self.record_mode == False :
                break

        print("Stop recording audio!")
        
        stream.stop_stream()
        stream.close()
        p.terminate()

        obj = wave.open(audio_path, "wb")
        obj.setnchannels(CHANNELS)
        obj.setsampwidth(p.get_sample_size(FORMAT))
        obj.setframerate(RATE)
        obj.writeframes(b"".join(frames))
        obj.close()
            
        print("Audio stored...")
        return   

    def unity_replay_audio(self, audio_path):
        playsound('/home/storyrobo/storyrobo_ws/ROS2_StoryRobo/storyrobo_service/driver/data_unity/' + audio_path + '.wav')

    def record_service_callback(self, request, response):
        self.get_logger().info('Record service called.')
        if controlcmd.recording:
            self.get_logger().info('Stopping recording.')
            response.success = True
            response.message = 'Recording stopped successfully.'
            controlcmd.recording = False
            controlcmd.send_real_time_data = True
            controlcmd.stop_record_action_points()
            time.sleep(0.5)
            # self.send_real_time_data_continuously()
        else:
            self.get_logger().info('Starting recording.')
            response.success = True
            response.message = 'Recording started successfully.'
            controlcmd.recording = True
            controlcmd.send_real_time_data = False
            time.sleep(0.5)
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
            controlcmd.stop_replay_all()
            controlcmd.disable_all_motor()
        else:
            response.success = True
            response.message = 'Replay started successfully.'
            controlcmd.replaying = True
            controlcmd.send_real_time_data = False
            time.sleep(0.5)
            controlcmd.replay_all()
            # self.replay_detect()
            # time.sleep(3)
            # controlcmd.disable_all_motor()
        
        return response
    
    # def replay_detect(self):
    #     while controlcmd.replaying:
    #         if controlcmd.send_real_time_data == True:
    #             self.send_real_time_data_continuously()
    #             pass

def main(args=None):
    rclpy.init(args=args)

    record_service_server = RecordServiceServer('http://10.100.3.116:5000')
    replay_service_server = ReplayServiceServer()

    # Initialize StoryRoboClient
    client_thread = threading.Thread(target=record_service_server.run, daemon=True)
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
        # storyrobo_client.sio.disconnect()  # Ensure the SocketIO client disconnects
        # client_thread.join()

if __name__ == '__main__':
    main()

