"""
系统工具模块测试
"""

import sys
import os
import socket

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from utils.system_utils import get_local_ip, get_system_info, get_screen_size


class TestGetLocalIP:
    """测试获取本地IP"""

    def test_get_local_ip_returns_string(self):
        ip = get_local_ip()
        assert isinstance(ip, str)

    def test_get_local_ip_valid_format(self):
        ip = get_local_ip()
        try:
            socket.inet_aton(ip)
            assert True
        except socket.error:
            assert ip == "127.0.0.1"


class TestGetSystemInfo:
    """测试获取系统信息"""

    def test_get_system_info_returns_dict(self):
        info = get_system_info()
        assert isinstance(info, dict)

    def test_get_system_info_keys(self):
        info = get_system_info()
        assert "platform" in info
        assert "version" in info
        assert "machine" in info
        assert "screen_size" in info


class TestGetScreenSize:
    """测试获取屏幕尺寸"""

    def test_get_screen_size_returns_dict(self):
        size = get_screen_size()
        assert isinstance(size, dict)

    def test_get_screen_size_keys(self):
        size = get_screen_size()
        assert "width" in size
        assert "height" in size

    def test_get_screen_size_values(self):
        size = get_screen_size()
        assert size["width"] > 0
        assert size["height"] > 0
