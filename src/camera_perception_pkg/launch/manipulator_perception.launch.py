import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
# [MODIFIED] DeclareLaunchArgument 추가
from launch.actions import IncludeLaunchDescription, TimerAction, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
# [ADDED] LaunchConfiguration 추가
from launch.substitutions import LaunchConfiguration

from launch_ros.actions import Node


def generate_launch_description():
    # =========================================================
    # Launch arguments
    # =========================================================
    # [ADDED] 실행 시 인식할 버튼 클래스 prefix를 외부에서 넘기기 위한 인자
    target_button = LaunchConfiguration('target_button')

    # =========================================================
    # Package paths
    # =========================================================
    realsense_share = get_package_share_directory('realsense2_camera')

    # =========================================================
    # RealSense launch path
    # =========================================================
    realsense_launch_path = os.path.join(
        realsense_share,
        'launch',
        'rs_launch.py'
    )

    # =========================================================
    # Declare launch arguments
    # =========================================================
    # [ADDED] 기본 타깃 버튼 설정
    declare_target_button = DeclareLaunchArgument(
        'target_button',
        default_value='btn_under1_deactive',
        description='Target button class prefix to detect'
    )

    # =========================================================
    # 2. RealSense D435 launch
    # Equivalent command:
    # ros2 launch realsense2_camera rs_launch.py \
    #   depth_module.depth_profile:=640x480x15 \
    #   pointcloud.enable:=true \
    #   align_depth.enable:=true
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
    # 3. YOLOv8 detection node
    # Equivalent command:
    # ros2 run camera_perception_pkg yolov8_node
    # =========================================================
    yolov8_node = Node(
        package='camera_perception_pkg',
        executable='yolov8_node',
        name='yolov8_node',
        output='screen'
    )

    # =========================================================
    # 4. Object distance node
    # Equivalent command:
    # ros2 run camera_perception_pkg object_distance_node --ros-args \
    #   -p detections_topic:=/detections \
    #   -p depth_image_topic:=/camera/camera/aligned_depth_to_color/image_raw \
    #   -p depth_camera_info_topic:=/camera/camera/color/camera_info \
    #   -p base_frame:=camera_link \
    #   -p target_label_prefixes:="['btn_under1_deactive']"
    # =========================================================
    object_distance_node = Node(
        package='camera_perception_pkg',
        executable='object_distance_node',
        name='object_distance_node',
        output='screen',
        parameters=[
            {
                'detections_topic': '/detections',
                'depth_image_topic': '/camera/camera/aligned_depth_to_color/image_raw',
                'depth_camera_info_topic': '/camera/camera/color/camera_info',
                'base_frame': 'camera_link',

                # [MODIFIED]
                # 기존 target_class_name은 object_distance_node.py에 없는 파라미터이므로 제거.
                # 현재 노드는 target_label_prefixes를 사용하여 class_name.startswith(prefix)로 타깃을 고름.
                'target_label_prefixes': [target_button],
            }
        ]
    )

    # =========================================================
    # 5. YOLOv8 debug node
    # Equivalent command:
    # ros2 run camera_perception_pkg yolov8_debug_node
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
    # 카메라 토픽이 생성된 뒤 perception node들이 붙도록 약간 지연 실행
    return LaunchDescription([
        # [ADDED] launch argument 등록
        declare_target_button,

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