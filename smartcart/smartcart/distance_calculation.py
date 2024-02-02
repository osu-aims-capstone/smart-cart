import rclpy
from rclpy.node import Node

from std_msgs.msg import Int64


class DistanceCalculationNode(Node):

    def __init__(self):
        super().__init__('distance_calculation_node')
        self.subscription = self.create_subscription(
            Int64, 
            'distance', 
            self.distance_callback, 
            10)
        distance = self.subscription    

    def distance_callback(self, distance):
        self.get_logger().info(distance)
        
    def __init__(self):
        super().__init__('motor_command_publisher')
        self.publisher_ = self.create_publisher(Int64, 'motorcommand', 10)
        timer_period = 0.5 #secs
        self.timer = self.create_timer(timer_period, self.publish_motorcommand)
        self.get_logger().info("Motor Command Publisher has been started")

    def publish_motorcommand(self, distance):
        max = 400 #cm
        min = 0.3 #cm

        #distance needed to stop motor
        if (distance <= max and distance >= min):
            stopMotor = 1
        else:
            stopMotor = 0

        self.publisher_.publish(stopMotor)
        self.get_logger().info("publishing: " % stopMotor)

def main(args=None):
    rclpy.init(args=args)

    distance_calculation_node = DistanceCalculationNode()
    rclpy.spin(distance_calculation_node)                    #node stays alive

    distance_calculation_node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()