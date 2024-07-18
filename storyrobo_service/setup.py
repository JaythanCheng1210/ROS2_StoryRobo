import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'storyrobo_service'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[pxy][yma]*')))
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='hsun',
    maintainer_email='209410314@gms.tku.edu.tw',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            # 'record_service_server = storyrobo_service.record_service_server:main',
            # # 'replay_service_server = storyrobo_service.replay_service_server:main',
            'trigger_service_client = storyrobo_service.trigger_service_client_button:main',
            'rec_rep_service_server = storyrobo_service.rec_rep_service_server:main'
        ],
    },
)
