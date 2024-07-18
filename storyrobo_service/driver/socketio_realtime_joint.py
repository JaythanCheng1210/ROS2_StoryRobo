import time
import os, sys, math
import socketio
import json

sys.path.append('/home/storyrobo/storyrobo_ws/ROS2_StoryRobo/storyrobo_service/driver')
from Storyrobo_ControlCmd import ControlCmd # type: ignore
controlcmd = ControlCmd()

# Create a new Socket.IO client
sio = socketio.Client()

# Event handler for connection
@sio.event
def connect():
    print('Connected to server')
    while True:
        try:
            message = controlcmd.read_all_motor_data()
            # message = json.dumps(controlcmd.read_all_motor_data())
            sio.emit('EchoBotMotor', message)
        except KeyboardInterrupt:
            break
    
    sio.disconnect()
    

# Event handler for receiving response
@sio.event
def response(data):
    print('Server response:', data)

# Event handler for disconnection
@sio.event
def disconnect():
    print('Disconnected from server')

# @sio.on("MotorFromServer")
# async def EchoBotMotor(data):
#     print('Received message:', data)
#     # sio.emit('MotorFromServer',data)

if __name__ == '__main__':
    # Connect to the server
    sio.connect('http://10.100.3.116:5000')
    sio.wait()
