import rclpy
from rclpy.node import Node

from std_msgs.msg import Int32


class DistanceCalculationNode(Node):

    print('distance calculation started')

    def __init__(self):
        super().__init__('distance_calculation_node')
        self.subscription = self.create_subscription(
            Int32, 
            'distance', 
            self.distance_callback, 
            10)
        self.subscription   

        self.publisher_ = self.create_publisher(Int32, 'motorcommand', 10) 

    def distance_callback(self, msg):
        self.get_logger().info("Receiving distance")
        self.get_logger().info('Distance received: "%d" ' % msg.data)
        timer_period = 0.5 #secs
        self.timer = self.create_timer(timer_period, self.publish_motorcommand(msg=msg))

    def publish_motorcommand(self, msg):

        max = 400 #cm
        min = 0.3 #cm

        #distance needed to stop motor
        if (msg.data <= max and msg.data >= min):
            stopMotor = 1
        else:
            stopMotor = 0

        self.publisher_.publish(int(stopMotor))
        self.get_logger().info('publishing: "%d" ' % int(stopMotor))

def main(args=None):
    rclpy.init(args=args)

    distance_calculation_node = DistanceCalculationNode()
    rclpy.spin(distance_calculation_node)                    #node stays alive
    
    distance_calculation_node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
