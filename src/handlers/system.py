"""
系统处理器模块
处理系统相关的HTTP请求
"""

from flask import Blueprint, request, jsonify
from services.system_service import SystemService

system_bp = Blueprint('system', __name__)
system_service = SystemService()

@system_bp.route('/api/system', methods=['POST'])
def handle_system():
    """处理系统操作请求"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'status': 'error', 'message': '无效的请求数据'}), 400
        
        action = data.get('action')
        
        if action == 'lock':
            result = system_service.lock_screen()
            print(result)
            return jsonify(result)
        
        elif action == 'shutdown':
            result = system_service.shutdown_system()
            return jsonify(result)
        
        elif action == 'restart':
            result = system_service.restart_system()
            return jsonify(result)
        
        elif action == 'status':
            result = system_service.get_system_status()
            return jsonify(result)
        
        else:
            return jsonify({'status': 'error', 'message': f'不支持的操作: {action}'}), 400
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'系统操作失败: {str(e)}'}), 500