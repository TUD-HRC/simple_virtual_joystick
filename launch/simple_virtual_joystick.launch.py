from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    topic = LaunchConfiguration("topic")
    stamped = LaunchConfiguration("stamped")
    frame = LaunchConfiguration("frame")

    return LaunchDescription([
        DeclareLaunchArgument(
            "topic",
            default_value="/cmd_vel"
        ),
        DeclareLaunchArgument(
            "stamped",
            default_value="true"
        ),
        DeclareLaunchArgument(
            "frame",
            default_value="base_link"
        ),

        Node(
            package="steadfast_env",
            executable="virtual_joystick",
            name="virtual_joystick",
            parameters=[{
                "use_sim_time": True,
                "timer_interval_ms": 10,
                "topic_name": topic,
                "stamped": stamped,
                "reference_frame": frame,
            }],
            output="screen",
        ),
    ])