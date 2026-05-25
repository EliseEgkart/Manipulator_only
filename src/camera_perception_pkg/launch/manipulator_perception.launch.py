import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node


def generate_launch_description():
    # =========================================================
    # Package paths
    # =========================================================
    realsense_share = get_package_share_directory('realsense2_camera')
    camera_perception_share = get_package_share_directory('camera_perception_pkg')

    # =========================================================
    # Config paths
    # =========================================================
    perception_config = os.path.join(
        camera_perception_share,
        'config',
        'manipulator_perception.yaml'
    )

    # =========================================================
    # RealSense launch path
    # =========================================================
    realsense_launch_path = os.path.join(
        realsense_share,
        'launch',
        'rs_launch.py'
    )

    # =========================================================
    # RealSense D435 launch
    # =========================================================
    realsense_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(realsense_launch_path),
        launch_arguments={
            'depth_module.depth_profile': '640x480x15',
            'pointcloud.enable': 'true',
            'align_depth.enable': 'true',
        }.items()
    )

    # =========================================================
    # YOLOv8 detection node
    # =========================================================
    yolov8_node = Node(
        package='camera_perception_pkg',
        executable='yolov8_node',
        name='yolov8_node',
        output='screen'
    )

    # =========================================================
    # Object distance node
    # =========================================================
    # Initial target button is loaded from:
    # config/manipulator_perception.yaml
    #
    # Runtime target change is handled by:
    # /manipulator_perception/target_button
    object_distance_node = Node(
        package='camera_perception_pkg',
        executable='object_distance_node',
        name='object_distance_node',
        output='screen',
        parameters=[
            perception_config
        ]
    )

    # =========================================================
    # YOLOv8 debug node
    # =========================================================
    yolov8_debug_node = Node(
        package='camera_perception_pkg',
        executable='yolov8_debug_node',
        name='yolov8_debug_node',
        output='screen'
    )

    # =========================================================
    # Launch order
    # =========================================================
    return LaunchDescription([
        TimerAction(
            period=1.0,
            actions=[
                realsense_launch
            ]
        ),

        TimerAction(
            period=5.0,
            actions=[
                yolov8_node
            ]
        ),

        TimerAction(
            period=7.0,
            actions=[
                object_distance_node
            ]
        ),

        TimerAction(
            period=8.0,
            actions=[
                yolov8_debug_node
            ]
        ),
    ])