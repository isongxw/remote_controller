#!/usr/bin/env python3
"""
远程控制应用主程序
支持通过网页界面远程控制电脑的键盘和鼠标操作
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from pynput import mouse, keyboard
from pynput.mouse import Button, Listener as MouseListener
from pynput.keyboard import Key, Listener as KeyboardListener
import threading
import time
import platform
import os

app = Flask(__name__)
CORS(app)

# 全局控制器实例
mouse_controller = mouse.Controller()
keyboard_controller = keyboard.Controller()

# Windows系统键位映射
WINDOWS_KEY_MAP = {
    'ctrl': Key.ctrl_l,
    'alt': Key.alt_l,
    'shift': Key.shift_l,
    'win': Key.cmd,
    'tab': Key.tab,
    'enter': Key.enter,
    'space': Key.space,
    'backspace': Key.backspace,
    'delete': Key.delete,
    'escape': Key.esc,
    'f1': Key.f1, 'f2': Key.f2, 'f3': Key.f3, 'f4': Key.f4,
    'f5': Key.f5, 'f6': Key.f6, 'f7': Key.f7, 'f8': Key.f8,
    'f9': Key.f9, 'f10': Key.f10, 'f11': Key.f11, 'f12': Key.f12,
    'up': Key.up, 'down': Key.down, 'left': Key.left, 'right': Key.right,
    'home': Key.home, 'end': Key.end, 'page_up': Key.page_up, 'page_down': Key.page_down,
    '[': '[', ']': ']',
}

@app.route('/')
def index():
    """主页面"""
    return render_template('index.html')

@app.route('/api/keyboard', methods=['POST'])
def handle_keyboard():
    """处理键盘操作"""
    try:
        data = request.get_json()
        action = data.get('action')
        key = data.get('key')
        
        if action == 'press':
            if key in WINDOWS_KEY_MAP:
                keyboard_controller.press(WINDOWS_KEY_MAP[key])
            else:
                keyboard_controller.press(key)
        elif action == 'release':
            if key in WINDOWS_KEY_MAP:
                keyboard_controller.release(WINDOWS_KEY_MAP[key])
            else:
                keyboard_controller.release(key)
        elif action == 'type':
            text = data.get('text', '')
            keyboard_controller.type(text)
        elif action == 'hotkey':
            keys = data.get('keys', [])
            # 处理组合键
            mapped_keys = []
            for k in keys:
                if k in WINDOWS_KEY_MAP:
                    mapped_keys.append(WINDOWS_KEY_MAP[k])
                else:
                    mapped_keys.append(k)
            
            # 按下所有键
            for k in mapped_keys:
                keyboard_controller.press(k)
            time.sleep(0.1)
            # 释放所有键
            for k in reversed(mapped_keys):
                keyboard_controller.release(k)
        
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/mouse', methods=['POST'])
def handle_mouse():
    """处理鼠标操作"""
    try:
        data = request.get_json()
        action = data.get('action')
        
        if action == 'move':
            x = data.get('x', 0)
            y = data.get('y', 0)
            relative = data.get('relative', False)
            
            if relative:
                current_pos = mouse_controller.position
                new_x = max(0, current_pos[0] + x)
                new_y = max(0, current_pos[1] + y)
                mouse_controller.position = (new_x, new_y)
            else:
                mouse_controller.position = (max(0, x), max(0, y))
                
        elif action == 'click':
            button_name = data.get('button', 'left')
            clicks = data.get('clicks', 1)
            
            button = Button.left if button_name == 'left' else Button.right
            # 确保鼠标点击后释放，避免卡住
            try:
                mouse_controller.click(button, clicks)
                # 添加短暂延迟确保点击完成
                time.sleep(0.05)
            except Exception as click_error:
                print(f"鼠标点击错误: {click_error}")
                # 强制释放所有按钮
                try:
                    mouse_controller.release(Button.left)
                    mouse_controller.release(Button.right)
                except:
                    pass
            
        elif action == 'scroll':
            dx = data.get('dx', 0)
            dy = data.get('dy', 0)
            mouse_controller.scroll(dx, dy)
            
        elif action == 'drag':
            start_x = data.get('start_x', 0)
            start_y = data.get('start_y', 0)
            end_x = data.get('end_x', 0)
            end_y = data.get('end_y', 0)
            
            try:
                mouse_controller.position = (start_x, start_y)
                mouse_controller.press(Button.left)
                time.sleep(0.1)
                mouse_controller.position = (end_x, end_y)
                mouse_controller.release(Button.left)
            except Exception as drag_error:
                print(f"拖拽操作错误: {drag_error}")
                # 确保释放按钮
                try:
                    mouse_controller.release(Button.left)
                except:
                    pass
        
        elif action == 'reset':
            # 新增重置功能，释放所有按钮
            try:
                mouse_controller.release(Button.left)
                mouse_controller.release(Button.right)
                mouse_controller.release(Button.middle)
            except:
                pass
        
        return jsonify({'status': 'success'})
    except Exception as e:
        print(f"鼠标操作错误: {e}")
        # 发生错误时尝试重置鼠标状态
        try:
            mouse_controller.release(Button.left)
            mouse_controller.release(Button.right)
            mouse_controller.release(Button.middle)
        except:
            pass
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/system', methods=['GET'])
def get_system_info():
    """获取系统信息"""
    return jsonify({
        'platform': platform.system(),
        'version': platform.version(),
        'machine': platform.machine(),
        'screen_size': get_screen_size()
    })

def get_screen_size():
    """获取屏幕尺寸"""
    try:
        import tkinter as tk
        root = tk.Tk()
        width = root.winfo_screenwidth()
        height = root.winfo_screenheight()
        root.destroy()
        return {'width': width, 'height': height}
    except:
        return {'width': 1920, 'height': 1080}  # 默认值

if __name__ == '__main__':
    print("远程控制服务器启动中...")
    print(f"系统平台: {platform.system()}")
    print("请在手机浏览器中访问: http://[电脑IP]:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
