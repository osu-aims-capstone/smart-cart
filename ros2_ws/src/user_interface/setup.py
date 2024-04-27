from setuptools import find_packages, setup

package_name = 'user_interface'

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
    maintainer='smartcart',
    maintainer_email='smartcart@todo.todo',
    description='User interface sends location and speed information to the motor control based on button pressesss',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
                'user_interface = user_interface.user_interface:main',
        ],
    },
)
