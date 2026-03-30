"""
键盘服务模块测试
"""

import sys
import os
from unittest.mock import Mock, patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from services.keyboard_service import KeyboardService
from core.config import KEYBOARD_CONFIG


class TestKeyboardService:
    """测试键盘服务"""

    @patch("services.keyboard_service.get_controllers")
    def test_keyboard_service_init(self, mock_get_controllers):
        mock_mouse = Mock()
        mock_keyboard = Mock()
        mock_get_controllers.return_value = (mock_mouse, mock_keyboard)

        service = KeyboardService()

        assert service.mouse_controller == mock_mouse
        assert service.keyboard_controller == mock_keyboard
        mock_get_controllers.assert_called_once()

    @patch("services.keyboard_service.get_controllers")
    def test_press_key_with_mapping(self, mock_get_controllers):
        mock_mouse = Mock()
        mock_keyboard = Mock()
        mock_get_controllers.return_value = (mock_mouse, mock_keyboard)

        service = KeyboardService()
        service.press_key("ctrl")

        mock_keyboard.press.assert_called()

    @patch("services.keyboard_service.get_controllers")
    def test_press_key_without_mapping(self, mock_get_controllers):
        mock_mouse = Mock()
        mock_keyboard = Mock()
        mock_get_controllers.return_value = (mock_mouse, mock_keyboard)

        service = KeyboardService()
        service.press_key("a")

        mock_keyboard.press.assert_called_with("a")

    @patch("services.keyboard_service.get_controllers")
    def test_release_key_with_mapping(self, mock_get_controllers):
        mock_mouse = Mock()
        mock_keyboard = Mock()
        mock_get_controllers.return_value = (mock_mouse, mock_keyboard)

        service = KeyboardService()
        service.release_key("ctrl")

        mock_keyboard.release.assert_called()

    @patch("services.keyboard_service.get_controllers")
    def test_type_text(self, mock_get_controllers):
        mock_mouse = Mock()
        mock_keyboard = Mock()
        mock_get_controllers.return_value = (mock_mouse, mock_keyboard)

        service = KeyboardService()
        service.type_text("hello")

        mock_keyboard.type.assert_called_with("hello")

    @patch("services.keyboard_service.get_controllers")
    @patch("services.keyboard_service.time.sleep")
    def test_execute_hotkey(self, mock_sleep, mock_get_controllers):
        mock_mouse = Mock()
        mock_keyboard = Mock()
        mock_get_controllers.return_value = (mock_mouse, mock_keyboard)

        service = KeyboardService()
        service.execute_hotkey(["ctrl", "a"])

        assert mock_keyboard.press.call_count == 2
        assert mock_keyboard.release.call_count == 2
