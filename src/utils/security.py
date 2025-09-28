"""
安全工具模块
包含键盘操作安全包装器和状态清理功能
"""

import logging
import threading

from pynput import keyboard, mouse

from core.config import CLEANUP_KEYS

# 全局变量
mouse_controller = mouse.Controller()
keyboard_controller = keyboard.Controller()
input_device_lock = threading.Lock()

logger = logging.getLogger(__name__)


def safe_keyboard_operation(operation_func):
    """
    安全的键盘操作包装器，确保不影响鼠标功能

    Args:
        operation_func: 要执行的键盘操作函数

    Returns:
        操作函数的返回值，如果出错则返回None
    """
    with input_device_lock:
        try:
            # 记录当前鼠标位置
            original_mouse_pos = mouse_controller.position

            # 执行键盘操作
            result = operation_func()

            # 确保鼠标位置没有被意外改变
            current_mouse_pos = mouse_controller.position
            if current_mouse_pos != original_mouse_pos:
                logger.info(f"检测到鼠标位置变化，恢复原位置: {original_mouse_pos}")
                mouse_controller.position = original_mouse_pos

            return result
        except Exception as e:
            logger.error(f"键盘操作错误: {e}")
            # 发生错误时清理所有可能的按键状态
            cleanup_keyboard_state()
            return None


def cleanup_keyboard_state():
    """清理键盘状态，确保所有按键都被释放"""
    for key in CLEANUP_KEYS:
        try:
            keyboard_controller.release(key)
        except:
            pass


def get_controllers():
    """
    获取输入设备控制器

    Returns:
        tuple: (mouse_controller, keyboard_controller)
    """
    return mouse_controller, keyboard_controller
