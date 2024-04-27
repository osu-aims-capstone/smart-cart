import rclpy
from rclpy.node import Node

import numpy as np

from std_msgs.msg import Float32MultiArray
from gpiozero import Button


BUTTONS = [
            Button(16),  # GPIO pin numbers
            Button(9),
            Button(7),
            Button(12),
            Button(10),
            Button(14),
           # Button(2),
            Button(8),
]

# An array is being sent for the distance and the direction to turn.
# ex. [0, 0] is stop and [1, 1] is go 1m and turn right 
BUTTON_SIGNALS = [     #message data for each button 
            [0.0, -3.0],  #estop
            [1.0, 0.0],  #loc1
            [2.0, 1.0],  #loc2
            [3.0, 0.0],  #loc3
           # [-1.0, -1.0],   #on/off
            [1.0, -3.0],  #speed1
            [2.0, -3.0],  #speed2
            [3.0, -3.0]  #speed3
]

class UserInterfaceNode(Node): 

    
    def __init__(self):
        super().__init__("location_publisher") 
        self.location_publisher_ = self.create_publisher(Float32MultiArray, 'location', 10)
        self.speed_publisher_ = self.create_publisher(Float32MultiArray, 'speed', 10)
        print('init')
        self.timer_ = self.create_timer(0.5, self.publish_button)

    def getButton(self):
        signal = [-2.0, -2.0]
       # for button in BUTTONS:
        #    print('loop')
         #   if (button.is_pressed):
          #      print('pressed')
           #     signal = BUTTON_SIGNALS[button]
        if (BUTTONS[0].is_pressed):
            signal = BUTTON_SIGNALS[0]
        elif (BUTTONS[1].is_pressed):
            signal = BUTTON_SIGNALS[1]
        elif (BUTTONS[2].is_pressed):
            signal = BUTTON_SIGNALS[2]
        elif (BUTTONS[3].is_pressed):
            signal = BUTTON_SIGNALS[3]
        elif (BUTTONS[4].is_pressed):
            signal = BUTTON_SIGNALS[4]
        elif (BUTTONS[5].is_pressed):
            signal = BUTTON_SIGNALS[5]
        elif (BUTTONS[6].is_pressed):
            signal = BUTTON_SIGNALS[6]
        #elif (BUTTONS[7].is_pressed):
         #   signal = BUTTON_SIGNALS[7]
        return signal
    
    def publish_button(self): 
        msg = Float32MultiArray()
        msg.data = self.getButton()
        if (msg.data[1] == -3.0):
            self.speed_publisher_.publish(msg)
            print("Speed: ", msg.data[0])
        elif (msg.data[0] != -2.0 and msg.data[1] != -2.0):
            self.location_publisher_.publish(msg)
            print("Location: ", msg.data)


def main(args=None):
    rclpy.init(args=args)
    node = UserInterfaceNode() 
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main() 
