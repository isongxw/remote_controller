"""
鼠标服务模块
处理所有鼠标相关的操作逻辑
"""

import time

from pynput import mouse

from utils.security import get_controllers


class MouseService:
    """鼠标操作服务类"""

    def __init__(self):
        self.mouse_controller, self.keyboard_controller = get_controllers()

    def move_to(self, x, y):
        """
        移动鼠标到指定位置

        Args:
            x: X坐标
            y: Y坐标
        """
        self.mouse_controller.position = (x, y)

    def click(self, button="left", count=1):
        """
        点击鼠标

        Args:
            button: 按钮类型 ('left', 'right', 'middle')
            count: 点击次数
        """
        button_map = {
            "left": mouse.Button.left,
            "right": mouse.Button.right,
            "middle": mouse.Button.middle,
        }

        if button in button_map:
            self.mouse_controller.click(button_map[button], count)

    def press(self, button="left"):
        """
        按下鼠标按钮

        Args:
            button: 按钮类型
        """
        button_map = {
            "left": mouse.Button.left,
            "right": mouse.Button.right,
            "middle": mouse.Button.middle,
        }

        if button in button_map:
            self.mouse_controller.press(button_map[button])

    def release(self, button="left"):
        """
        释放鼠标按钮

        Args:
            button: 按钮类型
        """
        button_map = {
            "left": mouse.Button.left,
            "right": mouse.Button.right,
            "middle": mouse.Button.middle,
        }

        if button in button_map:
            self.mouse_controller.release(button_map[button])

    def scroll(self, dx=0, dy=0):
        """
        滚动鼠标滚轮

        Args:
            dx: 水平滚动量
            dy: 垂直滚动量
        """
        self.mouse_controller.scroll(dx, dy)

    def drag(self, start_x, start_y, end_x, end_y):
        """
        拖拽操作

        Args:
            start_x: 起始X坐标
            start_y: 起始Y坐标
            end_x: 结束X坐标
            end_y: 结束Y坐标
        """
        # 移动到起始位置
        self.move_to(start_x, start_y)
        time.sleep(0.1)

        # 按下左键
        self.press("left")
        time.sleep(0.1)

        # 移动到结束位置
        self.move_to(end_x, end_y)
        time.sleep(0.1)

        # 释放左键
        self.release("left")

    def get_position(self):
        """
        获取当前鼠标位置

        Returns:
            tuple: (x, y) 坐标
        """
        return self.mouse_controller.position
