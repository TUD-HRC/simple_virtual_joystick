# Copyright 2024 Davide Torielli
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    topic = LaunchConfiguration('topic')
    stamped = LaunchConfiguration('stamped')
    frame = LaunchConfiguration('frame')
    use_sim_time = LaunchConfiguration('use_sim_time')
    timer_interval_ms = LaunchConfiguration('timer_interval_ms')

    return LaunchDescription([
        DeclareLaunchArgument(
            'topic',
            default_value='/cmd_vel_teleop',
            description='Topic name to publish velocity commands to'
        ),
        DeclareLaunchArgument(
            'stamped',
            default_value='true',
            description='Whether to publish TwistStamped or Twist'
        ),
        DeclareLaunchArgument(
            'frame',
            default_value='base_link',
            description='Frame ID for TwistStamped messages'
        ),
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use simulation time'
        ),
        DeclareLaunchArgument(
            'timer_interval_ms',
            default_value='10',
            description='Publishing interval in milliseconds'
        ),

        Node(
            package='simple_virtual_joystick',
            executable='simple_virtual_joystick',
            name='virtual_joystick',
            parameters=[{
                'use_sim_time': use_sim_time,
                'timer_interval_ms': timer_interval_ms,
                'topic_name': topic,
                'stamped': stamped,
                'reference_frame': frame,
            }],
            output='screen',
        ),
    ])