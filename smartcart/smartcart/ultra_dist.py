import rclpy
from rclpy.node import Node
import RPi.GPIO as GPIO
import time
from std_msgs.msg import Int32

TRIG=21
ECHO=20
GPIO.setmode(GPIO.BCM)
distance=0

class UltraDistanceNode(Node): 

    
    def __init__(self):
        super().__init__("distance_publisher") 
        
        self.distance_=0
        self.distance_publisher_ = self.create_publisher(Int32, "distance", 10)
        self.timer_ = self.create_timer(0.5, self.publish_distance)
       

    def getDistance(self):
        GPIO.setup(TRIG, GPIO.OUT)
        GPIO.setup(ECHO, GPIO.IN)
        GPIO.output(TRIG, False)
        self.get_logger().info("waiting for sensor to settle")
        time.sleep(0.2)
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


    def publish_distance(self):
        
        msg = Int32()
        msg.data = int(self.getDistance())
        self.distance_publisher_.publish(msg)
        self.get_logger().info("Ultra Distance has been started: %d" %msg.data)

def main(args=None):
    rclpy.init(args=args)
    node = UltraDistanceNode() 
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()