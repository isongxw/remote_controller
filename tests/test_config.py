"""
配置模块测试
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from core.config import Config, TOUCHPAD_CONFIG, KEYBOARD_CONFIG, WINDOWS_KEY_MAP


class TestConfig:
    """测试应用配置"""

    def test_host_config(self):
        assert Config.HOST == "0.0.0.0"
        assert Config.PORT == 8088

    def test_log_level(self):
        assert Config.LOGGER_LEVEL is not None


class TestTouchpadConfig:
    """测试触摸板配置"""

    def test_touchpad_config_keys(self):
        assert "CLICK_DELAY" in TOUCHPAD_CONFIG
        assert "DOUBLE_CLICK_TIME" in TOUCHPAD_CONFIG
        assert "MOVE_THRESHOLD" in TOUCHPAD_CONFIG
        assert "CURSOR_SENSITIVITY" in TOUCHPAD_CONFIG
        assert "SCROLL_SENSITIVITY" in TOUCHPAD_CONFIG

    def test_touchpad_config_values(self):
        assert TOUCHPAD_CONFIG["CLICK_DELAY"] > 0
        assert TOUCHPAD_CONFIG["DOUBLE_CLICK_TIME"] > 0
        assert TOUCHPAD_CONFIG["MOVE_THRESHOLD"] >= 0
        assert TOUCHPAD_CONFIG["CURSOR_SENSITIVITY"] > 0
        assert TOUCHPAD_CONFIG["SCROLL_SENSITIVITY"] > 0


class TestKeyboardConfig:
    """测试键盘配置"""

    def test_keyboard_config_keys(self):
        assert "HOTKEY_PRESS_INTERVAL" in KEYBOARD_CONFIG
        assert "HOTKEY_RELEASE_INTERVAL" in KEYBOARD_CONFIG

    def test_keyboard_config_values(self):
        assert KEYBOARD_CONFIG["HOTKEY_PRESS_INTERVAL"] > 0
        assert KEYBOARD_CONFIG["HOTKEY_RELEASE_INTERVAL"] > 0


class TestWindowsKeyMap:
    """测试Windows键位映射"""

    def test_key_map_basic_keys(self):
        assert "ctrl" in WINDOWS_KEY_MAP
        assert "alt" in WINDOWS_KEY_MAP
        assert "shift" in WINDOWS_KEY_MAP
        assert "win" in WINDOWS_KEY_MAP
        assert "tab" in WINDOWS_KEY_MAP
        assert "enter" in WINDOWS_KEY_MAP

    def test_key_map_function_keys(self):
        assert "f1" in WINDOWS_KEY_MAP
        assert "f12" in WINDOWS_KEY_MAP

    def test_key_map_arrow_keys(self):
        assert "up" in WINDOWS_KEY_MAP
        assert "down" in WINDOWS_KEY_MAP
        assert "left" in WINDOWS_KEY_MAP
        assert "right" in WINDOWS_KEY_MAP
