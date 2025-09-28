"""
键盘服务模块
处理所有键盘相关的操作逻辑
"""

import time

from core.config import WINDOWS_KEY_MAP
from utils.security import get_controllers


class KeyboardService:
    """键盘操作服务类"""

    def __init__(self):
        self.mouse_controller, self.keyboard_controller = get_controllers()

    def press_key(self, key):
        """
        按下按键

        Args:
            key: 按键名称
        """
        if key in WINDOWS_KEY_MAP:
            self.keyboard_controller.press(WINDOWS_KEY_MAP[key])
        else:
            self.keyboard_controller.press(key)

    def release_key(self, key):
        """
        释放按键

        Args:
            key: 按键名称
        """
        if key in WINDOWS_KEY_MAP:
            self.keyboard_controller.release(WINDOWS_KEY_MAP[key])
        else:
            self.keyboard_controller.release(key)

    def type_text(self, text):
        """
        输入文本

        Args:
            text: 要输入的文本
        """
        self.keyboard_controller.type(text)

    def execute_hotkey(self, keys):
        """
        执行快捷键组合

        Args:
            keys: 按键列表
        """
        # 处理组合键
        mapped_keys = []
        for k in keys:
            if k in WINDOWS_KEY_MAP:
                mapped_keys.append(WINDOWS_KEY_MAP[k])
            else:
                mapped_keys.append(k)

        # 按下所有键
        for k in mapped_keys:
            self.keyboard_controller.press(k)
            time.sleep(0.1)

        time.sleep(0.1)
        # 释放所有键
        for k in reversed(mapped_keys):
            self.keyboard_controller.release(k)
