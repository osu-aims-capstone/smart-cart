import rclpy
from rclpy.node import Node
import RPi.GPIO as GPIO
import time
from example_interfaces.msg import Int64

TRIG=21
ECHO=20
GPIO.setmode(GPIO.BCM)
distance=0

class UltraDistanceNode(Node): 

    def getDistance():
        GPIO.setup(TRIG, GPIO.OUT)
        GPIO.setup(ECHO, GPIO.IN)
        GPIO.output(TRIG, False)
        print("waiting for sensor to settle")
        time.sleep(0.2)
        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)
        while GPIO.input(ECHO)==0:
           pulse_start=time.time()
        while GPIO.input(ECHO)==1:
            pulse_end=time.time()
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration*17150
        distance=round(distance,2)
        print("distance: ", distance, " cm")
        time.sleep(2)
        

    def __init__(self):
        super().__init__("distance_publisher") 
        
        self.distance_ =  distance
        self.distance_publisher_ = self.create_publisher(Int64, "distance", 10)
        self.timer_ = self.create_timer(1.0, self.publish_distance)
        self.get_logger().info("Ultra Distance has been started")

    def publish_distance(self):
        msg = Int64()
        msg.data = self.distance_
        self.distance_publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = UltraDistanceNode() 
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()