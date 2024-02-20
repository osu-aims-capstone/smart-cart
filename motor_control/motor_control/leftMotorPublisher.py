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

from std_msgs.msg import Int32


class MinimalPublisher(Node):
    Target = -1
    currentVel =0
    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(Int32, 'motor', 10)
        self.subscription = self.create_subscription(
            Int32, 
            'target', 
            self.target_callback, 
            10)

        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

        self.subscription = self.create_subscription(
            Int32, 
            'velocity', 
            self.velocity_callback, 
            10)

        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def target_callback(self, msg):
        self.get_logger().info("Distance received: %d" % msg.data)
        self.Target = msg.data

    def velocity_callback(self, msg):
        self.get_logger().info("Distance received: %d" % msg.data)
        self.currentVel = msg.data

    def timer_callback(self):
        msg = Int32()
        msg.data = PID(self.Target, self.currentVel)
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1

    def PID(Target, currentVel):
        SAMPLETIME = 0.5
        TARGET = Target #m/s
        KP = 0.0001
        KD = 0.0005
        KI = 0.00005

        #m1 is left motor and m2 is right motor

        m1_speed = 0
        e1_prev_error = 0
        e1_sum_error = 0
        e1_error = TARGET - currentVel  
        m1_speed += (e1_error * KP) + (e1_prev_error * KD) + (e1_sum_error * KI)
        m1_speed = max(min(1, m1_speed), 0)
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
