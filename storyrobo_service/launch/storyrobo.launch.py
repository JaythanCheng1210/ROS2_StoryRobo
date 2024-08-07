import os

from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import TimerAction

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='storyrobo_service',
            executable='trigger_service_client',
            name='trigger_service_client',
            output='screen'
        ),
        Node(
            package='storyrobo_service',
            executable='rec_rep_service_server',
            name='rec_rep_service_server',
            output='screen'
        ),
    ])