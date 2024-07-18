import time
import os
import sys
import math
import json
import asyncio
import websockets

sys.path.append('/home/storyrobo/storyrobo_ws/ROS2_StoryRobo/storyrobo_service/driver')
from Storyrobo_ControlCmd import ControlCmd # type: ignore
controlcmd = ControlCmd()

async def send_motor_data(uri):
    async with websockets.connect(uri) as websocket:
        while True:
            try:
                message = controlcmd.read_all_motor_data()
                await websocket.send(json.dumps(message))
                response = await websocket.recv()
                print('Server response:', response)
            except KeyboardInterrupt:
                print("Interrupted by user")
                break

if __name__ == '__main__':
    uri = 'ws://192.168.1.114:5000'
    asyncio.get_event_loop().run_until_complete(send_motor_data(uri))


import asyncio
import websockets
async def send_messages(websocket):
    while True:
        message = "Hello, Server!"
        await websocket.send(message)
        print(f"Sent: {message}")
        await asyncio.sleep(1)  # 每秒發送一次訊息
async def receive_messages(websocket):
    while True:
        message = await websocket.recv()
        print(f"Received: {message}")
async def main():
    uri = "ws://192.168.1.114:5000/"
    async with websockets.connect(uri) as websocket:
        send_task = asyncio.create_task(send_messages(websocket))
        receive_task = asyncio.create_task(receive_messages(websocket))
        await asyncio.gather(send_task, receive_task)
if __name__ == "__main__":
    asyncio.run(main())
