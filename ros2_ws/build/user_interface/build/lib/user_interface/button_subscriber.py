import rclpy
from rclpy.node import Node

from std_msgs.msg import Int32


class ButtonSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            Int32,
            'button',
            self.listener_callback,
            10)
        self.subscription

    def listener_callback(self, msg):
        self.get_logger().info('I heard: "%d"' % msg.data)


def main(args=None):
    rclpy.init(args=args)

    button_subscriber = ButtonSubscriber()

    rclpy.spin(button_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    button_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
