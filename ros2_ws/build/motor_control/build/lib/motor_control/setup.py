from setuptools import find_packages, setup

package_name = 'motor_control'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='wafeeqaj',
    maintainer_email='jaleel.5@osu.edu',
    description='Motor-control subscriber node',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': ['leftMotor = motor_control.leftMotorPublisher:main',
                            'movement = motor_control.movementSubscriber:main',
                            'rightMotor = motor_control.rightMotorPublisher:main',
        ],
    },
)
