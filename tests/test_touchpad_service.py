"""
触摸板服务模块测试
"""

import sys
import os
from unittest.mock import Mock, patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from services.touchpad_service import TouchpadService
from core.config import TOUCHPAD_CONFIG


class TestTouchpadService:
    """测试触摸板服务"""

    @patch("services.touchpad_service.get_controllers")
    def test_touchpad_service_init(self, mock_get_controllers):
        mock_mouse = Mock()
        mock_keyboard = Mock()
        mock_get_controllers.return_value = (mock_mouse, mock_keyboard)

        service = TouchpadService()

        assert service.mouse_controller == mock_mouse
        assert service.keyboard_controller == mock_keyboard
        assert service.config == TOUCHPAD_CONFIG
        assert service.touchpad_state["active_touches"] == {}
        assert service.touchpad_state["is_dragging"] is False

    @patch("services.touchpad_service.get_controllers")
    def test_detect_touch_mode_single(self, mock_get_controllers):
        mock_mouse = Mock()
        mock_keyboard = Mock()
        mock_get_controllers.return_value = (mock_mouse, mock_keyboard)

        service = TouchpadService()
        result = service.detect_touch_mode({"touch_count": 1})

        assert result == "single"

    @patch("services.touchpad_service.get_controllers")
    def test_detect_touch_mode_scroll(self, mock_get_controllers):
        mock_mouse = Mock()
        mock_keyboard = Mock()
        mock_get_controllers.return_value = (mock_mouse, mock_keyboard)

        service = TouchpadService()
        result = service.detect_touch_mode({"touch_count": 2})

        assert result == "scroll"

    @patch("services.touchpad_service.get_controllers")
    def test_detect_touch_mode_dragging(self, mock_get_controllers):
        mock_mouse = Mock()
        mock_keyboard = Mock()
        mock_get_controllers.return_value = (mock_mouse, mock_keyboard)

        service = TouchpadService()
        result = service.detect_touch_mode({"touch_count": 3})

        assert result == "dragging"

    @patch("services.touchpad_service.get_controllers")
    def test_handle_touch_start_invalid_data(self, mock_get_controllers):
        mock_mouse = Mock()
        mock_keyboard = Mock()
        mock_get_controllers.return_value = (mock_mouse, mock_keyboard)

        service = TouchpadService()
        result = service.handle_touch_start({})

        assert result["status"] == "error"

    @patch("services.touchpad_service.get_controllers")
    def test_handle_touch_start_valid_data(self, mock_get_controllers):
        mock_mouse = Mock()
        mock_keyboard = Mock()
        mock_get_controllers.return_value = (mock_mouse, mock_keyboard)

        service = TouchpadService()
        result = service.handle_touch_start({
            "touch_id": "test",
            "touches": [{"x": 100, "y": 200}]
        })

        assert result["status"] == "success"
        assert "test" in service.touchpad_state["active_touches"]

    @patch("services.touchpad_service.get_controllers")
    def test_handle_touch_end(self, mock_get_controllers):
        mock_mouse = Mock()
        mock_keyboard = Mock()
        mock_get_controllers.return_value = (mock_mouse, mock_keyboard)

        service = TouchpadService()
        service.touchpad_state["active_touches"]["test"] = {
            "start_x": 100,
            "start_y": 200,
            "current_x": 100,
            "current_y": 200,
            "start_time": 0
        }

        result = service.handle_touch_end({
            "touch_id": "test",
            "touch_count": 1
        })

        assert result["status"] == "success"
        assert "test" not in service.touchpad_state["active_touches"]

    @patch("services.touchpad_service.get_controllers")
    def test_get_touchpad_status(self, mock_get_controllers):
        mock_mouse = Mock()
        mock_keyboard = Mock()
        mock_get_controllers.return_value = (mock_mouse, mock_keyboard)

        service = TouchpadService()
        status = service.get_touchpad_status()

        assert "active_touches_count" in status
        assert "is_dragging" in status
        assert "has_pending_click" in status

    @patch("services.touchpad_service.get_controllers")
    def test_shutdown_cleans_resources(self, mock_get_controllers):
        mock_mouse = Mock()
        mock_keyboard = Mock()
        mock_get_controllers.return_value = (mock_mouse, mock_keyboard)

        service = TouchpadService()
        service.touchpad_state["active_touches"]["test"] = {"x": 100, "y": 200}

        service.shutdown()

        assert len(service.touchpad_state["active_touches"]) == 0
        assert service.touchpad_state["is_dragging"] is False
