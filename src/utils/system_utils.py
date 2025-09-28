"""
系统工具模块
包含系统相关的工具函数
"""

import platform
import socket


def get_screen_size():
    """
    获取屏幕尺寸

    Returns:
        dict: 包含width和height的字典
    """
    try:
        import tkinter as tk

        root = tk.Tk()
        width = root.winfo_screenwidth()
        height = root.winfo_screenheight()
        root.destroy()
        return {"width": width, "height": height}
    except:
        return {"width": 1920, "height": 1080}  # 默认值


def get_system_info():
    """
    获取系统信息

    Returns:
        dict: 系统信息字典
    """
    return {
        "platform": platform.system(),
        "version": platform.version(),
        "machine": platform.machine(),
        "screen_size": get_screen_size(),
    }


def get_local_ip():
    try:
        # 创建一个 UDP 连接到一个外部地址（不真正发送数据）
        # 这会自动绑定一个本地地址
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))  # Google DNS
            local_ip = s.getsockname()[0]
        return local_ip
    except Exception:
        return "127.0.0.1"


if __name__ == "__main__":
    print("本机局域网IP:", get_local_ip())
