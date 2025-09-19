"""
主页面处理器
处理主页面路由
"""

from flask import Blueprint, current_app, render_template, send_from_directory

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    """主页面"""
    return render_template("index.html")


@main_bp.route("/remote-controller.js")
def serve_js():
    """提供JavaScript文件"""
    return send_from_directory(current_app.template_folder, "remote-controller.js")
