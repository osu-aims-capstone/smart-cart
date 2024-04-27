import rclpy
from rclpy.node import Node

from std_msgs.msg import Float32
from gpiozero import Button

start = Button(2) #GPIO pins
locA = Button(3)
locB = Button(4)
locC = Button(5)
speed1 = Button(19)
speed2 = Button(18)
speed3 = Button(17)
estop = Button(6)

class ButtonPublisher(Node):

    def __init__(self):
        super().__init__('button_publisher')
        self.publisher_location = self.create_publisher(Float32, 'location', 10)
        self.publisher_speed = self.create_publisher(Float32, 'speed', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)


    def timer_callback(self):
        msg_loc = Float32()
        msg_speed = Float32()
        speed = 0.0
        location = 0.0
        turn  = 0.0

        if estop.is_pressed:
            speed = -1.0

        if speed1.is_pressed:
            speed = 1.0
        elif speed2.is_pressed:
            speed = 2.0
        elif speed3.is_pressed:
            speed = 3.0

        if locA.is_pressed:
            location = 1.0
            turn = 0.0
        elif locB.is_pressed:
            location = 2.0
            turn = 1.0
        elif locC.is_pressed:
            location = 3.0
            turn = 0.0

        msg_loc.data = [location, turn]
        msg_speed.data = speed

        self.publisher_location.publish(msg_loc)
        self.get_logger().info('Publishing location: ' % msg_loc.data)

        self.publisher_speed.publish(msg_speed)
        self.get_logger().info('Publishing speed: "%d"' % msg_speed.data)


def main(args=None):
    rclpy.init(args=args)

    button_publisher = ButtonPublisher()

    rclpy.spin(button_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    button_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
