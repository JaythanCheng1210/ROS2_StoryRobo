import time
import os
import sys
import socketio
import json

sys.path.append('/home/storyrobo/storyrobo_ws/ROS2_StoryRobo/storyrobo_service/driver')
from Storyrobo_ControlCmd import ControlCmd  # type: ignore

controlcmd = ControlCmd()

# Create a new Socket.IO client
sio = socketio.Client()

# Flag to control real-time data sending
send_real_time_data = False
replay_mode = False


def send_real_time_data_continuously():
    global send_real_time_data
    while send_real_time_data:
        message = controlcmd.read_all_motor_data()
        sio.emit('EchoBotMotor', message)


@sio.event
def connect():
    print('Connected to server')


@sio.on('ReplayOnEchoBot')
def on_replay_data(data):
    global replay_mode
    print('Received replay data:', data)
    if replay_mode:
        controlcmd.real_time_replay(data)


@sio.on('StatusOnEchoBot')
def StatusOnEchoBot(status):
    global send_real_time_data, replay_mode
    print('Received command:', status)
    
    if status == "Connect":
        send_real_time_data = True
        time.sleep(0.5)
        replay_mode = False
        controlcmd.disable_all_motor()
        send_real_time_data_continuously()
    elif status == "Replay":
        send_real_time_data = False
        time.sleep(0.5)
        controlcmd.enable_all_motor()
        replay_mode = True
    elif status == "Replay stop":
        replay_mode = False
        controlcmd.disable_all_motor()

@sio.event
def response(data):
    print('Server response:', data)


@sio.event
def disconnect():
    global send_real_time_data, replay_mode
    print('Disconnected from server')
    send_real_time_data = False
    replay_mode = False


if __name__ == '__main__':
    while True:
        try:
            sio.connect('http://10.100.3.116:5000')
            sio.wait()
        except socketio.exceptions.ConnectionError:
            print('Waiting for connection ~')
            time.sleep(2)  # Wait for 5 seconds before trying again
