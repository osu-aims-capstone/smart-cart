# Copyright 2016 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import rclpy
from rclpy.node import Node

from std_msgs.msg import Float32, Int32

import threading
from gpiozero import Robot
from time import sleep

import time

# from gpiozero import Motor
# from time import sleep

# motor = Motor(forward=5, backward=6)

# while True:
#     motor.forward()
#     sleep(5)
#     motor.backward()
#     sleep(5)

r = Robot((19,16), (13,17)) 


class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(Float32, 'motorLeft', self.left_motor,10)
        self.subscription = self.create_subscription(Float32, 'motorRight', self.right_motor,10)
        self.m1_speed= 0
        self.m2_speed =0
        #self.subscription = self.create_subscription(Int32, 'motorcommand', self.obstacle,10)
        #self.subscription = self.create_subscription(Int32, 'motorcommand', self.left_motor,10)

        self.publisher_ = self.create_publisher(Int32, "extra", 10)
        self.timer = self.create_timer(0.5, self.publish_motorcommand)

    def right_motor(self, msg):
        self.get_logger().info('I heard: "%f"' % msg.data)
        self.m2_speed = msg.data

    def left_motor(self, msg):
        self.get_logger().info('I heard: "%f"' % msg.data)
        self.m1_speed = msg.data

    def publish_motorcommand(self):
        r .value = (self.m1_speed, self.m2_speed)
        
# def move():
#     while True:
        

def main(args=None):
    rclpy.init(args=args)
    

    minimal_subscriber = MinimalSubscriber()
    rclpy.spin(minimal_subscriber)
    #move()
    # # Destroy the node explicitly
    # # (optional - otherwise it will be done automatically
    # # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()
if __name__ == '__main__':
    main()
