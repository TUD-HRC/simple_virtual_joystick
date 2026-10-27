#!/usr/bin/env python3

import rclpy
import tkinter as tk
import math
from geometry_msgs.msg import TwistStamped, Twist
from rclpy.node import Node

class VirtualJoystick:
    def __init__(self, title, size=300):

        self.node = Node("joystick_publisher")

        self.node.declare_parameter("topic_name", "/cmd_vel_teleop")
        topic_name = self.node.get_parameter("topic_name").get_parameter_value().string_value
        self.node.declare_parameter('stamped', True)
        self.stamped = self.node.get_parameter('stamped').get_parameter_value().bool_value
        self.node.declare_parameter('timer_interval_ms', 10)
        self.timer_interval_ms = self.node.get_parameter('timer_interval_ms').get_parameter_value().integer_value
        self.node.declare_parameter("reference_frame", "base_link")
        self.reference_frame = self.node.get_parameter("reference_frame").get_parameter_value().string_value

        if self.stamped:
            self.publisher = self.node.create_publisher(TwistStamped, topic_name, 1)
        else:
            self.publisher = self.node.create_publisher(Twist, topic_name, 1)


        self.root = tk.Tk()
        self.root.title(title)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.after(self.timer_interval_ms, self.publish_velocity)

        self.size = size
        self.radius = size // 2
        self.center = self.radius

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.main_frame, width=size, height=size, bg="white")
        self.canvas.pack(side=tk.LEFT)
        self.canvas.create_oval(5, 5, size-5, size-5)

        self.stick_radius = 10
        self.stick = self.canvas.create_oval(
            self.center - self.stick_radius,
            self.center - self.stick_radius,
            self.center + self.stick_radius,
            self.center + self.stick_radius,
            fill="blue"
        )

        self.canvas.bind("<B1-Motion>", self.move_stick)
        self.canvas.bind("<ButtonRelease-1>", self.reset_stick)

        self.control_frame = tk.Frame(self.main_frame)
        self.control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=8, pady=8)

        self.z_control = tk.Scale(
            self.control_frame,
            label="Linear Z",
            from_=1.0,
            to=-1.0,
            resolution=0.01,
            orient=tk.VERTICAL,
            length=self.size,
            command=self.update_z,
        )
        self.z_control.set(0.0)
        self.z_control.pack()
        self.z_control.bind("<ButtonRelease-1>", self.reset_z)

        self.bottom_frame = tk.Frame(self.root)
        self.bottom_frame.pack(side=tk.TOP, fill=tk.X, pady=5)

        self.label = tk.Label(self.bottom_frame, text="x: 0.00, y: 0.00, z: 0.00, az: 0.00")
        self.label.pack(side=tk.TOP, pady=(0, 5))

        self.angular_z = 0.0
        self.ang_z_control = tk.Scale(
            self.bottom_frame,
            label="Angular Z",
            from_=1.0,
            to=-1.0,
            resolution=0.01,
            orient=tk.HORIZONTAL,
            length=self.size,
            command=self.update_angular_z,
        )
        self.ang_z_control.set(0.0)
        self.ang_z_control.pack()
        self.ang_z_control.bind("<ButtonRelease-1>", self.reset_angular_z)

        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        self.prev_x = 0.0
        self.prev_y = 0.0
        self._stopped = False


    def move_stick(self, event):
        dx = event.x - self.center
        dy = event.y - self.center

        dist = math.sqrt(dx**2 + dy**2)
        if dist > self.radius:
            dx *= self.radius / dist
            dy *= self.radius / dist

        x = self.center + dx
        y = self.center + dy

        self.canvas.coords(
            self.stick,
            x - self.stick_radius,
            y - self.stick_radius,
            x + self.stick_radius,
            y + self.stick_radius,
        )

        self.prev_x = self.x
        self.prev_y = self.y
        self.x = -dy / self.radius
        self.y = -dx / self.radius

        self.label.config(text=f"x: {self.x:.2f}, y: {self.y:.2f}, z: {self.z:.2f}, az: {self.angular_z:.2f}")

    def reset_stick(self, event):
        self.canvas.coords(
            self.stick,
            self.center - self.stick_radius,
            self.center - self.stick_radius,
            self.center + self.stick_radius,
            self.center + self.stick_radius,
        )
        self.prev_x = self.x
        self.prev_y = self.y
        self.x = 0.0
        self.y = 0.0
        self.z_control.set(0.0)
        self.ang_z_control.set(0.0)
        self.label.config(text=f"x: {self.x:.2f}, y: {self.y:.2f}, z: {self.z:.2f}, az: {self.angular_z:.2f}")

    def reset_z(self, event):
        self.z_control.set(0.0)
        return "break"

    def reset_angular_z(self, event):
        self.ang_z_control.set(0.0)
        return "break"

    def update_z(self, value):
        self.z = float(value)
        self.label.config(text=f"x: {self.x:.2f}, y: {self.y:.2f}, z: {self.z:.2f}, az: {self.angular_z:.2f}")

    def update_angular_z(self, value):
        self.angular_z = float(value)
        self.label.config(text=f"x: {self.x:.2f}, y: {self.y:.2f}, z: {self.z:.2f}, az: {self.angular_z:.2f}")

    def publish_velocity(self):
        if self._stopped:
            return

        twist_msg = Twist()
        twist_msg.linear.x = self.x
        twist_msg.linear.y = self.y
        twist_msg.linear.z = self.z
        twist_msg.angular.x = 0.0
        twist_msg.angular.y = 0.0
        twist_msg.angular.z = self.angular_z
        
        if self.stamped:
            msg = TwistStamped()
            msg.header.stamp = self.node.get_clock().now().to_msg()
            msg.header.frame_id = self.reference_frame
            msg.twist = twist_msg
            self.publisher.publish(msg)
        else:
            self.publisher.publish(twist_msg)
        
        self.root.after(self.timer_interval_ms, self.publish_velocity)

    def joystick_velocity(self):
        dx = self.x - self.prev_x
        dy = self.y - self.prev_y
        return math.sqrt(dx*dx + dy*dy)

    def on_close(self):
        self._stopped = True
        try:
            self.node.destroy_node()
        except Exception:
            pass
        self.root.destroy()

    def mainloop(self):
        self.root.mainloop()

def main(args=None):
    rclpy.init(args=args)
    joystick = VirtualJoystick(title="ROS2 Joystick")
    try:
        joystick.mainloop()
    finally:
        rclpy.shutdown()


if __name__ == "__main__":
    main()
