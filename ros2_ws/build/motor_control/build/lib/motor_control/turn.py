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

from std_msgs.msg import Int32,Float32, Int32MultiArray
import time


class MinimalPublisher(Node):
    Target = 200
    #currentVel =0
    def __init__(self):

        #Publisher for sending speed information to motor
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(Int32, 'turn', 10)
        timer_period = 0.1  # seconds
        self.timer = self.create_timer(timer_period, self.turn)
        self.i = 0


    def turn(self):
        timeout = time.time()   # 5 minutes from now
        while True:
            msg = Int32()
            time.sleep(10)
            msg.data = 1
            self.publisher_.publish(msg)
            self.get_logger().info('Publishing: "%d"' % msg.data)
            self.i += 1
            self.destroy_node()


def main(args=None):
    rclpy.init(args=args)
    
    minimal_publisher = MinimalPublisher()
    rclpy.spin(minimal_publisher)

    
    minimal_publisher.destroy_node()
    rclpy.shutdown()

   
    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    


if __name__ == '__main__':
    main()
