import rclpy
from rclpy.node import Node

from std_msgs.msg import Int32


class DistanceCalculationNode(Node):
    print('distance calculation started')
    distanceR = -1
    distanceL = -1
    
    def __init__(self):
        super().__init__('distance_calculation_node')
        self.subscription = self.create_subscription(Int32, 'distanceR', self.distanceR_callback,10)
        self.subscription = self.create_subscription(Int32, 'distanceL', self.distanceL_callback,10)
        self.publisher_ = self.create_publisher(Int32, "stop", 10)
        self.timer = self.create_timer(0.2, self.publish_motorcommand)


        
    def distanceR_callback(self, msg):
        self.get_logger().info("Distance received(R): %d" % msg.data)
        self.distanceR = msg.data

    def distanceL_callback(self, msg):
        self.get_logger().info("Distance received(L): %d" % msg.data)
        self.distanceL = msg.data


        
    def publish_motorcommand(self):
        max = 100 #cm
        min = 15 #cm
        stop = Int32()
        stop.data=0
        if self.distanceR <=max or self.distanceL <=max:
            stop.data =1
        self.get_logger().info("publishing: %d" % int(stop.data))

def main(args=None):
    rclpy.init(args=args)

    distance_calculation_node = DistanceCalculationNode()
    rclpy.spin(distance_calculation_node)                    #node stays alive

    distance_calculation_node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
