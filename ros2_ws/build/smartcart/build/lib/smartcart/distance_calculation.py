import rclpy
from rclpy.node import Node

from std_msgs.msg import Int32


class DistanceCalculationNode(Node):
    print('distance calculation started')
    distance = -1
    
    def __init__(self):
        super().__init__('distance_calculation_node')
        self.subscription = self.create_subscription(
            Int32, 
            'distance', 
            self.distance_callback, 
            10)
        self.publisher_ = self.create_publisher(Int32, "motorcommand", 10)
        self.timer = self.create_timer(0.5, self.publish_motorcommand)
        
    def distance_callback(self, msg):
        self.get_logger().info("Distance received: %d" % msg.data)
        self.distance = msg.data

    def publish_motorcommand(self):
        max = 60 #cm
        min = 0.3 #cm
        stopMotor = Int32()
        
        #distance needed to stop motor
        if (self.distance <= max and self.distance >= min):
            stopMotor.data = 0
        else:
            stopMotor.data = 1

        self.publisher_.publish(stopMotor)
        self.get_logger().info("publishing: %d" % int(stopMotor.data))

def main(args=None):
    rclpy.init(args=args)

    distance_calculation_node = DistanceCalculationNode()
    rclpy.spin(distance_calculation_node)                    #node stays alive

    distance_calculation_node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
