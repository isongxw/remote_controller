"""
处理器模块
包含所有API路由处理器
"""

from .keyboard import keyboard_bp
from .main import main_bp
from .mouse import mouse_bp
from .system import system_bp
from .touchpad import touchpad_bp

__all__ = ["main_bp", "keyboard_bp", "mouse_bp", "touchpad_bp", "system_bp"]
