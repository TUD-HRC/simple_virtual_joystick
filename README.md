# simple_virtual_joystick

ROS2 publisher

For when a real controller is just too far away from your desk.   
2D axis, horizontal slider, and vertical slider, publishing on a twist/twiststamped topic  
I (AI) did it because I needed to control x, y, yaw, and altitude of a drone (i.e., 4 DOF), and there was not something available.

![virtual joy](doc/virtualJoy.png)

## Install
- Using tkinter, so `sudo apt install python3-tk`
- clone
- `rosdep install -i --from-path src --rosdistro jazzy -y`
- `colcon build --packages-select simple_virtual_joystick`

## Run
Check the launch for config arguments
- `ros2 launch simple_virtual_joystick simple_virtual_joystick.launch.py`

## alternatives
- https://github.com/amgaber95/rqt_virtual_joystick?tab=readme-ov-file - much fancier, rqt plugin, but no additional sliders for z and yaw