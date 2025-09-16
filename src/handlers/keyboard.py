"""
键盘处理器模块
处理键盘相关的HTTP请求
"""

from flask import Blueprint, request, jsonify
from services.keyboard_service import KeyboardService

keyboard_bp = Blueprint('keyboard', __name__)
keyboard_service = KeyboardService()

@keyboard_bp.route('/api/keyboard', methods=['POST'])
def handle_keyboard():
    """处理键盘操作请求"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'status': 'error', 'message': '无效的请求数据'}), 400
        
        action = data.get('action')
        
        if action == 'press':
            key = data.get('key')
            if not key:
                return jsonify({'status': 'error', 'message': '缺少按键参数'}), 400
            
            keyboard_service.press_key(key)
            return jsonify({'status': 'success', 'message': f'按键 {key} 已按下'})
        
        elif action == 'release':
            key = data.get('key')
            if not key:
                return jsonify({'status': 'error', 'message': '缺少按键参数'}), 400
            
            keyboard_service.release_key(key)
            return jsonify({'status': 'success', 'message': f'按键 {key} 已释放'})
        
        elif action == 'type':
            text = data.get('text')
            if not text:
                return jsonify({'status': 'error', 'message': '缺少文本参数'}), 400
            
            keyboard_service.type_text(text)
            return jsonify({'status': 'success', 'message': f'文本已输入: {text}'})
        
        elif action == 'hotkey':
            keys = data.get('keys')
            if not keys or not isinstance(keys, list):
                return jsonify({'status': 'error', 'message': '缺少或无效的按键组合参数'}), 400
            
            keyboard_service.execute_hotkey(keys)
            return jsonify({'status': 'success', 'message': f'快捷键组合已执行: {keys}'})
        
        else:
            return jsonify({'status': 'error', 'message': f'不支持的操作: {action}'}), 400
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'键盘操作失败: {str(e)}'}), 500