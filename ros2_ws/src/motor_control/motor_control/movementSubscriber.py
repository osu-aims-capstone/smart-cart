#Controls the motors with PWM signal

import rclpy
from rclpy.node import Node

from std_msgs.msg import Float32, Int32, Float32MultiArray

import threading
from gpiozero import Robot
from time import sleep
import numpy as np
import time

import pigpio
import time

GPIO = pigpio.pi()

class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        self.LeftmotorSub = self.create_subscription(Float32, 'motorLeft', self.left_motor,10)
        self.RightmotorSub = self.create_subscription(Float32, 'motorRight', self.right_motor,10)
        self.m1_speed= 0
        self.m2_speed =0

        self.Extra = self.create_publisher(Int32, "extra", 10)
        self.timer = self.create_timer(0.1, self.publish_motorcommand)

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


def main(args=None):
    rclpy.init(args=args)
    

    minimal_subscriber = MinimalSubscriber()
    rclpy.spin(minimal_subscriber)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()
if __name__ == '__main__':
    main()
