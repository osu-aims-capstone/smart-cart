import rclpy
from rclpy.node import Node
import RPi.GPIO as GPIO
from std_msgs.msg import Int32
import time


GPIO.setmode(GPIO.BCM)

class DistanceCalculationNode(Node):
    print('distance calculation started')
    distanceR = -1
    distanceL = -1
    
    def __init__(self):
        super().__init__('distance_calculation_node')
        self.publisher_ = self.create_publisher(Int32, "stop", 10)
        self.timer = self.create_timer(0.2, self.publish_motorcommand)


    def getDistance(self, TRIG, ECHO):
        GPIO.setup(TRIG, GPIO.OUT)
        GPIO.setup(ECHO, GPIO.IN)
        GPIO.output(TRIG, False)
        #self.get_logger().info("waiting for sensor to settle")
        time.sleep(0.001)
        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)
        while GPIO.input(ECHO)==0:
            pulse_start=time.time()
        while GPIO.input(ECHO)==1:
            pulse_end=time.time()
        pulse_duration = pulse_end - pulse_start
        distance= pulse_duration*17150
        distance=round(distance,2)
        #self.get_logger().info("distance: ", self.distance_, " cm")
        time.sleep(0.1)
        
        return distance
    

        
    def publish_motorcommand(self):
        max = 70 #cm
        min = 15 #cm
        stop = Int32()
        stop.data=0

        TRIGR=21
        ECHOR=20

        TRIGL=23
        ECHOL=24
        self.distanceR = self.getDistance(TRIGR,ECHOR)
        self.get_logger().info("publishingR: %d" % (self.distanceR))
        self.distanceL = self.getDistance(TRIGL,ECHOL)
        self.get_logger().info("publishingL: %d" % (self.distanceL))
        if self.distanceR <=max or self.distanceL <=max:
            stop.data =1
        else:
            stop.data =0
        self.publisher_.publish(stop)
        #self.get_logger().info("publishing: %d" % int(stop.data))

def main(args=None):
    rclpy.init(args=args)

    distance_calculation_node = DistanceCalculationNode()
    rclpy.spin(distance_calculation_node)                    #node stays alive

    distance_calculation_node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
