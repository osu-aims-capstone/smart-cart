import rclpy
from rclpy.node import Node

import numpy as np

from std_msgs.msg import Float32MultiArray
from gpiozero import Button


BUTTONS = [
            Button(2),  # GPIO pin numbers
            Button(3),
            Button(4),
            Button(5),
            Button(6),
            Button(7),
            Button(8),
            Button(9),
]

# An array is being sent for the distance and the direction to turn.
# ex. [0, 0] is stop and [1, 1] is go 1m and turn right 
BUTTON_SIGNALS = np.array([      #message data for each button 
            [0, 0],  #estop
            [5, 0],  #loc1
            [3, 1],  #loc2
            [2, 0],  #loc3
            [-1, -1],   #on/off
            [1, 0],  #speed1
            [2, 0],  #speed2
            [3, 0]  #speed3
])

Node.__init__('location_interface')
location_publisher = Node.create_publisher(Float32MultiArray, 'location', 10)

Node.__init__('location_interface')
speed_publisher = Node.create_publisher(Float32MultiArray, 'speed', 10)

msg = Float32MultiArray()
    
def main():
    rclpy.init()

    user_interface = Node()

    msg.data = [0, 0]
    while(True):
    
        for button in BUTTONS:
                if (button.is_pressed):
                    if(button < 5):
                        msg.data = BUTTON_SIGNALS[button]
                        location_publisher.publish(msg)
                    else:
                        msg.data = BUTTON_SIGNALS[button]
                        speed_publisher.publish(msg)
    
        rclpy.spin(user_interface)
    
        rclpy.shutdown()

if __name__ == '__main__':
        main()
