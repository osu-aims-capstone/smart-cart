from setuptools import find_packages, setup

package_name = 'encoder'

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
    description='TODO: Package description',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
                'encoder = encoder.publisher_encoder:main',
                'listener = encoder.subscriber_velocity_calculation:main',
        ],
    },
)
