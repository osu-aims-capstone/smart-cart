#The node uses pigpio module to read the encoder value from the quadrature encoder and published as an array

import rclpy
from rclpy.node import Node

from std_msgs.msg import Float32MultiArray

from .decoder import Decoder
import time
import pigpio

pi = pigpio.pi()

def callback(self,way):
    self.pos += way

e1 = Decoder(pi, 6,5, callback)     #left
e2 = Decoder(pi, 26, 22, callback)  #right

class EncoderPublisher(Node):

    def __init__(self):
        
        super().__init__('encoder_publisher')
        self.publisher_ = self.create_publisher(Float32MultiArray, 'encoderValue', 10)
        timer_period = 0.1  # seconds
        
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = Float32MultiArray()
        msg.data = [e1.pos/6000.0,e2.pos/6000.0]            #Divided by 6000 because it publishes rotations every 0.1 secoonds              
        
        self.publisher_.publish(msg)
        print("publishing")
        self.get_logger().info('Publishing left: "%f"' % msg.data[0])
        self.get_logger().info('Publishing right: "%f"' % msg.data[1])
        self.i += 1
        if self.i%10==0:
            e1.pos =0
            e2.pos=0


def main(args=None):
    rclpy.init(args=args)
    encoder_publisher = EncoderPublisher()
    rclpy.spin(encoder_publisher)
    encoder_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
    
    
       


    
    

