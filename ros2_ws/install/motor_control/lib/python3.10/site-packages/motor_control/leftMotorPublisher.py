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
import time
from std_msgs.msg import Int32,Float32, Float32MultiArray


class MinimalPublisher(Node):
    Target = 0.200 #0.200 = 0.95m/s
    currentVel =0
    stop = 0
    def __init__(self):

        #Publisher for sending speed information to motor
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(Float32, 'motorLeft', 10)
        timer_period = 0.1  # seconds
        self.timer = self.create_timer(timer_period, self.motor_callback)
        self.i = 0

        #Subscriber for getting the Target RPM (3.5 m/s ideal) from obstacle and weight nodes. 
        #self.subscription = self.create_subscription(Int32, 'target', self.target_callback, 10)
        self.subscription = self.create_subscription(Int32, 'stop', self.stop, 10)
        
        #Subscriber for getting the current RPM from encoder node
        self.subscription = self.create_subscription(Float32MultiArray, 'encoderValue', self.velocity_callback, 10)
    #     self.subscription = self.create_subscription(Int32, 'turn', self.turn, 10)


    def stop(self,msg):
        self.get_logger().info("command received(L): %d" % msg.data)
        self.stop = msg.data
    
    # def target_callback(self, msg):
    #     self.get_logger().info("Target velocity (RPM): %d" % msg.data)
    #     self.Target = msg.data

    def velocity_callback(self, msg):
        #self.get_logger().info('Publishing: "%d"' % msg.data[0]) 
        self.currentVel = msg.data[0]
        
    def motor_callback(self):
        msg = Float32()
        msg.data = self.PID(self.Target, self.currentVel)
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%f"' % msg.data)  
        self.i += 1
        # if self.i%10==0 and self.i<=41:
        #     self.Target +=10
         
        # if self.i>=1000:
        #     self.Target = 0   

    #PID function for calculating the value of motor
    def PID(self,Target, currentVel):
        SAMPLETIME = 0.5
        TARGET = Target #m/s
        KP = 0.9
        KD = 0.25
        KI = 0.25

        #m1 is left motor and m2 is right motor
        if self.stop == 1:
            m1_speed =0
        else:
            m1_speed = 0
            e1_prev_error = 0
            e1_sum_error = 0
            e1_error = TARGET - currentVel  
            m1_speed += (e1_error * KP) + (e1_prev_error * KD) + (e1_sum_error * KI)
            m1_speed = max(min(0.4, m1_speed), 0.08)
            e1_prev_error = e1_error 
            e1_sum_error += e1_error
    
        return m1_speed

def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()

    rclpy.spin(minimal_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
