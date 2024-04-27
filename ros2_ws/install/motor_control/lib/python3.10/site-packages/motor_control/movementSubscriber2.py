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

from std_msgs.msg import Float32, Int32, Float32MultiArray

import threading
from gpiozero import Robot
from time import sleep
import numpy as np
import time

# from gpiozero import Motor
# from time import sleep

# motor = Motor(forward=5, backward=6)

# while True:
#     motor.forward()
#     sleep(5)
#     motor.backward()
#     sleep(5)

import pigpio
import time

GPIO = pigpio.pi()

# Pull down the GPIO-Pin and cleanup with stop()



class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        self.LeftmotorSub = self.create_subscription(Float32, 'motorLeft', self.left_motor,10)
        self.RightmotorSub = self.create_subscription(Float32, 'motorRight', self.right_motor,10)
        self.m1_speed= 0
        self.m2_speed =0
        self.total_meter =0
        self.distance =0.0
        self.turn =0.0
        self.speed = 0.0

      
        
        #self.subscription = self.create_subscription(Int32, 'motorcommand', self.left_motor,10)

        self.Extra = self.create_publisher(Int32, "extra", 10)
        #self.timer = self.create_timer(0.1, self.publish_motorcommand)

       

        self.timer = self.create_timer(0.1, self.publish_motorcommand)

    # def location(self,msg):
    #     self.distance = msg.data[0]
    #     self.turn = msg.data[1]
    #     self.get_logger().info('Location received: "%f"' % self.distance)
   
    # def position(self):
    #     diameter = 0.1524
        
    #     if self.turn ==1:
    #         self.m1_speed = self.m1_speed*1.5
    #     elif self.turn ==-1:
    #         self.m2_speed = self.m2_speed*1.5
    #     else:
    #         avg_speed = (self.m2_speed + self.m1_speed)/2000000
    #         RPM = avg_speed*600
    #         m_s = RPM*np.pi*diameter/60
    #         meter = m_s * 0.1 #measured every 0.1 second
            
    #         self.total_meter += meter/2
    #         self.get_logger().info('Publish position: "%f"' % self.total_meter)
    
    #     if self.total_meter>=self.distance: 
    #         self.m1_speed =0
    #         self.m2_speed =0
    #         self.total_meter =0
    #     else:
    #         self.timer = self.create_timer(0.1, self.publish_motorcommand)
    #     if self.total_meter<= self.distance and self.turn ==0:
    #         self.timer = self.create_timer(0.1, self.publish_motorcommand)
            
    #     elif self.total_meter>= self.distance-0.5 and self.turn ==1:        #right turn
    #         self.m1_speed =(avg_speed +0.1)*1000000
    #         self.m2_speed =avg_speed*1000000

    #     elif self.total_meter>= self.distance-0.5 and self.turn ==2 :       #left turn
    #         self.m2_speed =(avg_speed +0.1)*1000000
    #         self.m1_speed =avg_speed*1000000
    #     else:
    #         self.m1_speed =0
    #         self.m2_speed =0
    #         #self.destroy_node()

    def right_motor(self, msg):
        #self.get_logger().info('I heard: "%f"' % msg.data)
        self.m2_speed = msg.data*1000000

    def left_motor(self, msg):
        #self.get_logger().info('I heard: "%f"' % msg.data)
        self.m1_speed = msg.data*1000000

    def publish_motorcommand(self):
        
        freq=20000
        #
        # pigpio uses BROADCOM PIN NUMBERING !!!
        #

        PWMR = 19 # Physical Pin #35
        PWML = 18 # Physical Pin #12
        RevR = 17  # Physical Pin #29
        RevL = 27  # Physical Pin #31
                # Phyiscal pins 30 and 34 are ground


        # Set the GPIO-Mode to ALT5 for HW-PWM
        GPIO.set_mode(PWML, pigpio.ALT5)
        GPIO.set_mode(PWMR, pigpio.ALT5)
        GPIO.set_mode(RevL, pigpio.OUTPUT)
        GPIO.set_mode(RevR, pigpio.OUTPUT)
        GPIO.write(RevL,1)
        GPIO.write(RevR,1)

        # Start the signal geaneration

        # self.get_logger().info('left motor Speed: "%f"' % int(self.m1_speed))
        # self.get_logger().info('right motor Speed: "%f"' % int(self.m2_speed))
        GPIO.hardware_PWM(PWML, freq, int(self.m1_speed))
        GPIO.hardware_PWM(PWMR, freq, int(self.m2_speed))
        
        
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
    GPIO.write(PWMR, 0)
    GPIO.write(PWML, 0)
    GPIO.write(RevL,0)
    GPIO.write(RevR,0)
    GPIO.stop()
    rclpy.shutdown()
if __name__ == '__main__':
    main()
