"""
Flask应用工厂模块
创建和配置Flask应用实例
"""

import logging

from flask import Flask
from flask_cors import CORS

from .config import Config


def create_app():
    """
    创建Flask应用实例

    Returns:
        Flask: 配置好的Flask应用实例
    """
    app = Flask(__name__, template_folder="../templates", static_folder="../templates")

    # 加载配置
    app.config.from_object(Config)

    # 配置Flask应用的日志级别
    app.logger.setLevel(logging.DEBUG)

    # 确保所有logger都使用DEBUG级别
    logging.getLogger().setLevel(logging.DEBUG)

    # 启用CORS
    CORS(app)

    # 注册蓝图
    from handlers.keyboard import keyboard_bp
    from handlers.main import main_bp
    from handlers.system import system_bp
    from handlers.touchpad import touchpad_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(keyboard_bp)
    app.register_blueprint(touchpad_bp)
    app.register_blueprint(system_bp)

    return app
