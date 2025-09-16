"""
触摸板处理器模块
处理触摸板相关的HTTP请求
"""

from flask import Blueprint, request, jsonify
from services.touchpad_service import TouchpadService

touchpad_bp = Blueprint('touchpad', __name__)
touchpad_service = TouchpadService()

@touchpad_bp.route('/api/touchpad', methods=['POST'])
def handle_touchpad():
    """处理触摸板操作请求"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'status': 'error', 'message': '无效的请求数据'}), 400
        
        action = data.get('action')
        
        if action == 'touch_start':
            result = touchpad_service.handle_touch_start(data)
            return jsonify(result)
        
        elif action == 'touch_move':
            result = touchpad_service.handle_touch_move(data)
            return jsonify(result)
        
        elif action == 'touch_end':
            result = touchpad_service.handle_touch_end(data)
            return jsonify(result)
        
        elif action == 'status':
            status = touchpad_service.get_touchpad_status()
            return jsonify({'status': 'success', 'touchpad_status': status})
        
        else:
            return jsonify({'status': 'error', 'message': f'不支持的操作: {action}'}), 400
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'触摸板操作失败: {str(e)}'}), 500