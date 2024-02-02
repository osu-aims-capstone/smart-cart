from setuptools import find_packages, setup

package_name = 'smartcart'

setup(
    name= package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='lauren',
    maintainer_email='laurendudgeon1@icloud.com',
    description='TODO: Package description',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'ultra_dist = smartcart.ultra_dist:main',
            'distance_calculation = smartcart.distance_calculation:main'
        ],
    },
)
