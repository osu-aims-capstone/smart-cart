from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import AnyLaunchDescriptionSource
from launch_ros.actions import Node, PushRosNamespace
from launch_ros.actions.composable_node_container import ComposableNode, ComposableNodeContainer
from launch.substitutions import LaunchConfiguration as LC

import os

from ament_index_python.packages import get_package_share_directory

#cfg_36h11 = {
#    "image_transport": "raw",
#    "family": "36h11",
#    "size": 0.508,
#    "max_hamming": 0,
#    "z_up": True
#}

def generate_launch_description():
    ld = LaunchDescription()

    #tensorrt_wrapper_dir = get_package_share_directory("tensor_detector")

    #params_path = os.path.join(tensorrt_wrapper_dir, 'config', 'tensorrt.yaml')

    #weights_path = os.path.join(   tensorrt_wrapper_dir, 'weights', 'bin300.pt')
    
    #ld.add_action(PushRosNamespace(LC("robot")))

    #ld.add_action(DeclareLaunchArgument(
    #    name="robot",
    #    default_value="tempest",
    #    description="name of the robot"
    #))

    # 
    # Ultrasonic sensors
    #

    ld.add_action(Node(
            package='smartcart',  
            executable='ultra_dist.py',  
            name='ultrasonic_node', 
    )),

    ld.add_action(Node(
            package='smartcart',  
            executable='distance_calculation.py',  
            name='distance_calculation_node', 
    )),
  
    #
    # Motor Control
    #
    ld.add_action(Node(
            package='motor_control',  
            executable='leftMotorPublisher.py',  
            name='left_motor_publisher_node', 
    )),

    ld.add_action(Node(
            package='motor_control',  
            executable='rightMotorPublisher.py',  
            name='right_motor_publisher_node', 
    )),

    ld.add_action(Node(
            package='motor_control',  
            executable='movementSubscriber2.py',  
            name='movement_node', 
    )),

    #
    # Encoder
    #
    ld.add_action(Node(
            package='encoder',  
            executable='publisher_encoder.py',  
            name='publisher_encoder_node', 
    )),

    #
    # APRILTAG STUFF
    #

    # ld.add_action(ComposableNodeContainer(
    #     name='tag_container',
    #     namespace="apriltag",
    #     package='rclcpp_components',
    #     executable='component_container',
    #     composable_node_descriptions=[
    #         ComposableNode(
    #             name='apriltag_36h11',
    #             package='apriltag_ros', plugin='AprilTagNode',
    #             remappings=[
    #                 # This maps the 'raw' images for simplicity of demonstration.
    #                 # In practice, this will have to be the rectified 'rect' images.
    #                 ("image_rect",
    #                 "zed/zed_node/left/image_rect_color"),
    #                 ("camera_info",
    #                 "zed/zed_node/left/camera_info"),
    #             ],
    #             parameters=[cfg_36h11],
    #             extra_arguments=[{'use_intra_process_comms': True}],
    #         )
    #     ],
    #     output='screen'
    # )),

    # ld.add_action(Node(
    #     package='tf2_ros',
    #     executable='static_transform_publisher',
    #     name='surface_frame_node',
    #     arguments=["0", "0.4572", "0", "0", "-1.5707", "-1.5707",
    #             "tag36h11:0", "estimated_origin_frame"]
    # ))

    return ld
