"""
系统工具模块
包含系统相关的工具函数
"""

import platform

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
        return {'width': width, 'height': height}
    except:
        return {'width': 1920, 'height': 1080}  # 默认值

def get_system_info():
    """
    获取系统信息
    
    Returns:
        dict: 系统信息字典
    """
    return {
        'platform': platform.system(),
        'version': platform.version(),
        'machine': platform.machine(),
        'screen_size': get_screen_size()
    }