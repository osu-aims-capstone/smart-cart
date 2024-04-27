import rclpy

from rclpy.node import Node
from example_interfaces.srv import SetBool

from gpiozero import Button

class UserInterfaceService(Node):

    def ___init__(self, node_name):
        super().__init__(node_name)
        self.buttons = [
           Button(2),  # GPIO pin numbers
           Button(3),
           Button(4),
           Button(5),
           Button(6)
        ]
        print("button service started")
        self.srv = self.create_service(SetBool, 'ui_service', self.ui_callback)

        def ui_callback(self, request: SetBool.Request, response: SetBool.Response):
            button_states = [button.is_pressed for button in self.buttons]  # determining if button was pressed
            #button_states = button.is_pressed
            response.success = True
            response.message = "Buttons pressed: " + str(button_states)
            print("Buttons pressed: " + str(button_states))
            return response

def main():

    rclpy.init()

    ui_service = UserInterfaceService('ui_service')
    print("Service node created")
    rclpy.spin(ui_service)

    rclpy.shutdown()

    if __name__ == '__main__':
        main()
