import rclpy
from rclpy.node import Node
from example_interfaces.srv import SetBool

class ButtonClient(Node):
    def __init__(self):
        super().__init__('button_client')

    def call_ui_service(self):
        client = self.create_client(SetBool, 'ui_service')
        while not client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service not available, waiting again...')
        request = SetBool.Request()
        self.get_logger().info('Calling service to get button states...')
        future = client.call_async(request)
        rclpy.spin_until_future_complete(self, future)
        if future.result() is not None:
            self.get_logger().info('Received button states: %s' % future.result().message)
        else:
            self.get_logger().error('Service call failed!')

def main(args=None):
    rclpy.init(args=args)
    button_client = ButtonClient()
    button_client.call_ui_service()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
