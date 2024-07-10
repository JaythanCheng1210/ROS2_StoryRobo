# ros2-Echobot-robot

## **Requirements**

- Python 3.10
- [If ubunt 22.04 | ROS2 humble](https://docs.ros.org/en/humble/Installation.html)
- [If ubunt 20.04 | ROS2 foxy](https://docs.ros.org/en/foxy/Installation.html)

### environment setup
- [JETSON-ORIN-NANO-DEV-KIT Burning Systems Details](https://blog.cavedu.com/2023/05/09/jetson-orin-nano-boot/)
```
mkdir storyrobo_ws && cd storyrobo_ws
```
```
git clone https://github.com/JaythanCheng1210/ROS2_StoryRobo.git
```
```
sudo apt install python3-pip
sudo apt install python3-pyaudio
sudo pip3 install Jetson.GPIO
sudo pip3 install sounddevice
sudo pip3 install soundfile
```
### DynamixelSDK setup
- cd /home/user: 
```
git clone https://github.com/ROBOTIS-GIT/DynamixelSDK.git
```
```
cd /DynamixlSDK/python && sudo python setup.py install
```


- build: 
```
colcon build
```


### Start
```
ros2 launch storyrobo_service storyrobo.launch.py
```



