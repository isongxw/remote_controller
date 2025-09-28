"""
应用配置模块
包含应用的全局配置和常量定义
"""

import logging
import platform

from pynput.keyboard import Key


# 应用配置
class Config:
    """应用配置类"""

    HOST = "0.0.0.0"
    LOCAL_HOST = "127.0.0.1"
    PORT = 8088
    LOGGER_LEVEL = logging.INFO


# 触摸板配置
TOUCHPAD_CONFIG = {
    "CLICK_DELAY": 0.15,  # 点击延迟时间（秒）
    "DOUBLE_CLICK_TIME": 0.3,  # 双击检测时间窗口（秒）
    "MOVE_THRESHOLD": 5,  # 移动阈值（像素）
    "CURSOR_SENSITIVITY": 2.0,  # 光标移动灵敏度
    "SCROLL_SENSITIVITY": 0.1,  # 滚动灵敏度
}

# Windows系统键位映射
WINDOWS_KEY_MAP = {
    "ctrl": Key.ctrl_l,
    "alt": Key.alt_l,
    "shift": Key.shift_l,
    "win": Key.cmd,
    "tab": Key.tab,
    "enter": Key.enter,
    "space": Key.space,
    "backspace": Key.backspace,
    "delete": Key.delete,
    "escape": Key.esc,
    "f1": Key.f1,
    "f2": Key.f2,
    "f3": Key.f3,
    "f4": Key.f4,
    "f5": Key.f5,
    "f6": Key.f6,
    "f7": Key.f7,
    "f8": Key.f8,
    "f9": Key.f9,
    "f10": Key.f10,
    "f11": Key.f11,
    "f12": Key.f12,
    "up": Key.up,
    "down": Key.down,
    "left": Key.left,
    "right": Key.right,
    "home": Key.home,
    "end": Key.end,
    "page_up": Key.page_up,
    "page_down": Key.page_down,
    "[": "[",
    "]": "]",
    "+": "=",
    "-": "-",
}

# 系统信息
CURRENT_PLATFORM = platform.system()

# 清理键盘状态时需要释放的按键
CLEANUP_KEYS = [
    Key.ctrl_l,
    Key.ctrl_r,
    Key.shift_l,
    Key.shift_r,
    Key.alt_l,
    Key.alt_r,
    Key.cmd,
    Key.esc,
    Key.tab,
    Key.caps_lock,
    Key.num_lock,
    Key.scroll_lock,
]
