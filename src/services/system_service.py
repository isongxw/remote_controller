"""
系统服务模块
处理所有系统相关的操作逻辑
"""

import ctypes
import subprocess
from core.config import CURRENT_PLATFORM
from utils.system_utils import get_system_info

class SystemService:
    """系统操作服务类"""
    
    def __init__(self):
        pass
    
    def lock_screen(self):
        """
        锁定屏幕
        
        Returns:
            dict: 操作结果
        """
        try:
            if CURRENT_PLATFORM == 'Windows':
                return self._windows_lock_screen()
            else:
                return self._linux_lock_screen()
        except Exception as e:
            return {
                'status': 'error',
                'message': f'锁屏操作失败: {str(e)}'
            }
    
    def _windows_lock_screen(self):
        """Windows系统锁屏"""
        try:
            # 使用Windows API LockWorkStation函数
            user32 = ctypes.windll.user32
            result = user32.LockWorkStation()
            
            if result:
                return {
                    'status': 'success',
                    'message': 'Windows系统锁屏成功'
                }
            else:
                return {
                    'status': 'error',
                    'message': 'Windows系统锁屏失败'
                }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Windows锁屏操作异常: {str(e)}'
            }
    
    def _linux_lock_screen(self):
        """Linux系统锁屏"""
        lock_commands = [
            ['loginctl', 'lock-session'],
            ['gnome-screensaver-command', '--lock'],
            ['xdg-screensaver', 'lock'],
            ['dm-tool', 'lock'],
            ['xscreensaver-command', '-lock']
        ]
        
        for cmd in lock_commands:
            try:
                result = subprocess.run(cmd, 
                                      stdout=subprocess.DEVNULL, 
                                      stderr=subprocess.DEVNULL, 
                                      timeout=5)
                if result.returncode == 0:
                    return {
                        'status': 'success',
                        'message': f'Linux系统锁屏成功: {" ".join(cmd)}'
                    }
            except FileNotFoundError:
                continue
            except subprocess.TimeoutExpired:
                continue
            except Exception:
                continue
        
        return {
            'status': 'error',
            'message': 'Linux系统锁屏失败，所有锁屏命令都不可用'
        }
    
    def get_system_status(self):
        """
        获取系统状态信息
        
        Returns:
            dict: 系统状态信息
        """
        try:
            system_info = get_system_info()
            return {
                'status': 'success',
                'data': system_info
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'获取系统信息失败: {str(e)}'
            }
    
    def shutdown_system(self):
        """
        关闭系统
        
        Returns:
            dict: 操作结果
        """
        try:
            if CURRENT_PLATFORM == 'Windows':
                subprocess.run(['shutdown', '/s', '/t', '0'], check=True)
            else:
                subprocess.run(['shutdown', 'now'], check=True)
            
            return {
                'status': 'success',
                'message': '系统关闭命令已执行'
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'系统关闭失败: {str(e)}'
            }
    
    def restart_system(self):
        """
        重启系统
        
        Returns:
            dict: 操作结果
        """
        try:
            if CURRENT_PLATFORM == 'Windows':
                subprocess.run(['shutdown', '/r', '/t', '0'], check=True)
            else:
                subprocess.run(['reboot'], check=True)
            
            return {
                'status': 'success',
                'message': '系统重启命令已执行'
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'系统重启失败: {str(e)}'
            }