# ros2-pangolin-robot

## **Requirements**

- Python 3.10
- [If ubunt 22.04 | ROS2 humble](https://docs.ros.org/en/humble/Installation.html)
- [If ubunt 20.04 | ROS2 foxy](https://docs.ros.org/en/foxy/Installation.html)

### environment setup
- [GPIO root setup](https://forum.up-community.org/discussion/2141/solved-tutorial-gpio-i2c-spi-access-without-root-permissions)
- [JETSON-ORIN-NANO-DEV-KIT Burning Systems Details](https://blog.cavedu.com/2023/05/09/jetson-orin-nano-boot/)
```
mkdir storyrobo_ws && cd storyrobo_ws
```
```
git clone https://github.com/JaythanCheng1210/ROS2_StoryRobo.git
```
```
sudo apt install python3-pip
sudo pip3 install Jetson.GPIO
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

```



