"""
主页面处理器
处理主页面路由
"""

from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """主页面"""
    return render_template('index.html')