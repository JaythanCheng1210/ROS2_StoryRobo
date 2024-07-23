from DXL_motor_control import DXL_Conmunication

import time
import sys, tty, termios
import traceback
import json 
import threading

#For audio
import pyaudio
import wave
import sounddevice as sd
import soundfile as sf
from playsound import playsound

import os

# # Keyboard interrupt 
# fd = sys.stdin.fileno()
# old_settings = termios.tcgetattr(fd)
# def getch():
#     try:
#         tty.setraw(sys.stdin.fileno())
#         ch = sys.stdin.read(1)
#     finally:
#         termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
#     return ch


# main control command
DEVICE_NAME = "/dev/ttyUSB0"
B_RATE      = 57600
LED_ADDR_LEN = (65,1)
LED_ON = 1
LED_OFF = 0


class ControlCmd:
    def __init__(self):

        self.record_path = '/home/storyrobo/storyrobo_ws/ROS2_StoryRobo/storyrobo_service/driver/data/joint.json'
        self.audio_store_path = '/home/storyrobo/storyrobo_ws/ROS2_StoryRobo/storyrobo_service/driver/data'
        self.audio_path = os.path.join(self.audio_store_path, 'output.wav')

        self.recording = False
        self.replaying = False
        self.is_recording = False
        self.is_replaying = False
        
        self.dynamixel = DXL_Conmunication(DEVICE_NAME, B_RATE)
        self.dynamixel.activateDXLConnection()
        motor0 = self.dynamixel.createMotor('motor0', motor_number=0)
        motor1 = self.dynamixel.createMotor('motor1', motor_number=1)
        motor2 = self.dynamixel.createMotor('motor2', motor_number=2)
        motor3 = self.dynamixel.createMotor('motor3', motor_number=3)
        motor4 = self.dynamixel.createMotor('motor4', motor_number=4)
        motor5 = self.dynamixel.createMotor('motor5', motor_number=5)
        motor6 = self.dynamixel.createMotor('motor6', motor_number=6)
        motor7 = self.dynamixel.createMotor('motor7', motor_number=7)
        motor8 = self.dynamixel.createMotor('motor8', motor_number=8)
        motor9 = self.dynamixel.createMotor('motor9', motor_number=9)
        motor10 = self.dynamixel.createMotor('motor10', motor_number=10)
        motor11 = self.dynamixel.createMotor('motor11', motor_number=11)
        
        self.motor_list = [motor0, motor1, motor2, motor3, motor4, motor5, 
                           motor6, motor7, motor8, motor9, motor10, motor11]
        
        self.motor_position = {"motor0":0, "motor1":0, "motor2":0, "motor3":0, "motor4":0, "motor5":0,
                               "motor6":0, "motor7":0, "motor8":0, "motor9":0, "motor10":0, "motor11":0}
        
        self.dynamixel.rebootAllMotor()
        self.dynamixel.updateMotorData()


    def enable_all_motor(self):
        for motor in self.motor_list:
            motor.enableMotor()

    def disable_all_motor(self):
        for motor in self.motor_list:
            motor.disableMotor()
    
    def motor_led_control(self, state = LED_OFF):
        for motor in self.motor_list:
            led_on = motor.directWriteData(state, *LED_ADDR_LEN)
            
        return led_on
    
    def read_all_motor_data(self):
        self.dynamixel.updateMotorData()
        for motor in self.motor_list:
            position, _ = motor.directReadData(132, 4)
            # print("motor id:", motor.DXL_ID, "motor position:", position)
            while abs(position) > 4095:
                position = position - (position/abs(position)) * 4095
            self.motor_position[motor.name] = int(position*360/4095)
            print(self.motor_position)
        
        return self.motor_position   
    
    # Control position of all motors
    def motor_position_control(self, position =  {'motor0': 1642, 'motor1': 1864, 'motor2': 2208, 'motor3': 1846, 'motor4': 2183, 'motor5': 2382, 
                                                  'motor6': 2461, 'motor7': 2102, 'motor8': 1857, 'motor9': 2256, 'motor10': 1955, 'motor11': 1859}):
        for motor in self.motor_list:
            motor.writePosition(position[motor.name])
        self.dynamixel.sentAllCmd()
        time.sleep(0.1)
    
    # The process of the recording function
    def process_record_action_points(self):
        self.disable_all_motor()
        print("disabling")
        # self.dynamixel.rebootAllMotor()
        # print("rebooting")
        self.motor_led_control(LED_ON)
        
        with open(self.record_path, 'w') as f:
            print("start record the action points....")
            while self.is_recording:
                all_servo_position = self.read_all_motor_data()
                print(f"recording: {all_servo_position}")
                f.write(json.dumps(all_servo_position)+'\n')
                time.sleep(0.001)
            self.motor_led_control(LED_OFF)
        print("finish recording!")

    # Start recording the motors position
    def start_record_action_points(self):
        self.is_recording = True
        self.recording_thread = threading.Thread(target=self.process_record_action_points, args=(), daemon=True)
        self.record_audio_thread = threading.Thread(target=self.record_audio, args=(self.audio_path, ), daemon=True)

        self.recording_thread.start()
        self.record_audio_thread.start()

    # Stop recording
    def stop_record_action_points(self):
        self.is_recording = False


    # Replay the recording file
    def replay_recorded_data(self):
        self.enable_all_motor()
        time.sleep(0.55)
        with open(self.record_path) as f: 
            one_action_point = f.readline()
            while one_action_point:
                one_action_point = json.loads(one_action_point) 
                print(one_action_point)

                self.motor_position_control(position = {"motor0": int((one_action_point["motor0"] * 4095) / 360),
                                                        "motor1": int((one_action_point["motor1"] * 4095) / 360), 
                                                        "motor2": int((one_action_point["motor2"] * 4095) / 360), 
                                                        "motor3": int((one_action_point["motor3"] * 4095) / 360), 
                                                        "motor4": int((one_action_point["motor4"] * 4095) / 360), 
                                                        "motor5": int((one_action_point["motor5"] * 4095) / 360),
                                                        "motor6": int((one_action_point["motor6"] * 4095) / 360),
                                                        "motor7": int((one_action_point["motor7"] * 4095) / 360),
                                                        "motor8": int((one_action_point["motor8"] * 4095) / 360),
                                                        "motor9": int((one_action_point["motor9"] * 4095) / 360),
                                                        "motor10": int((one_action_point["motor10"] * 4095) / 360),
                                                        "motor11": int((one_action_point["motor11"] * 4095) / 360)})
                time.sleep(0.3)
                one_action_point = f.readline()
        self.disable_all_motor() 
    
    def real_time_replay(self, joint):
        self.motor_position_control(position = {    "motor0": int((joint["motor0"] * 4095) / 360),
                                                    "motor1": int((joint["motor1"] * 4095) / 360), 
                                                    "motor2": int((joint["motor2"] * 4095) / 360), 
                                                    "motor3": int((joint["motor3"] * 4095) / 360), 
                                                    "motor4": int((joint["motor4"] * 4095) / 360), 
                                                    "motor5": int((joint["motor5"] * 4095) / 360),
                                                    "motor6": int((joint["motor6"] * 4095) / 360),
                                                    "motor7": int((joint["motor7"] * 4095) / 360),
                                                    "motor8": int((joint["motor8"] * 4095) / 360),
                                                    "motor9": int((joint["motor9"] * 4095) / 360),
                                                    "motor10": int((joint["motor10"] * 4095) / 360),
                                                    "motor11": int((joint["motor11"] * 4095) / 360)})
        # time.sleep(0.3)
        

    def record_audio(self, audio_path):
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
        
        while self.is_recording:
            data = stream.read(FRAMES_PER_BUFFER)
            frames.append(data)
            
            # Check for event to stop recording
            if not self.is_recording:
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

    def replay_audio(self):
        playsound('/home/storyrobo/storyrobo_ws/ROS2_StoryRobo/storyrobo_service/driver/data/output.wav')

    def replay_all(self):
        self.replay_movement_thread = threading.Thread(target=self.replay_recorded_data)
        self.replay_audio_thread = threading.Thread(target=self.replay_audio)
        self.replay_movement_thread.start()
        self.replay_audio_thread.start()
        
if __name__ == "__main__":
    controlcmd = ControlCmd()

    # while True:
    #     print("Press any key to continue! (or press ESC to quit!)")
    #     if getch() == chr(0x1b):
    #         break
    #     all_servo_position = controlcmd.read_motor_data()
    #     print(all_servo_position)
    # controlcmd.disable_all_motor()

    command_dict = {
        "read":controlcmd.read_all_motor_data,
        "record":controlcmd.start_record_action_points,
        "stop":controlcmd.stop_record_action_points,
        "replay":controlcmd.replay_all,
        "disable":controlcmd.disable_all_motor,
        # "rcaudio":controlcmd.record_audio,
        # "rpaudio":controlcmd.replay_audio,

    }


    while True:
        try:
            cmd = input("CMD : ")
            if cmd in command_dict:
                command_dict[cmd]()
            elif cmd == "exit":
                break
        except Exception as e:
            traceback.print_exc()
            break