"""
鼠标处理器模块
处理鼠标相关的HTTP请求
"""

from flask import Blueprint, jsonify, request

from services.mouse_service import MouseService

mouse_bp = Blueprint("mouse", __name__)
mouse_service = MouseService()


@mouse_bp.route("/api/mouse", methods=["POST"])
def handle_mouse():
    """处理鼠标操作请求"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "无效的请求数据"}), 400

        action = data.get("action")

        if action == "move":
            x = data.get("x")
            y = data.get("y")
            if x is None or y is None:
                return jsonify({"status": "error", "message": "缺少坐标参数"}), 400

            mouse_service.move_to(x, y)
            return jsonify({"status": "success", "message": f"鼠标已移动到 ({x}, {y})"})

        elif action == "click":
            button = data.get("button", "left")
            count = data.get("count", 1)

            mouse_service.click(button, count)
            return jsonify({"status": "success", "message": f"{button}键点击{count}次"})

        elif action == "press":
            button = data.get("button", "left")

            mouse_service.press(button)
            return jsonify({"status": "success", "message": f"{button}键已按下"})

        elif action == "release":
            button = data.get("button", "left")

            mouse_service.release(button)
            return jsonify({"status": "success", "message": f"{button}键已释放"})

        elif action == "scroll":
            dx = data.get("dx", 0)
            dy = data.get("dy", 0)

            mouse_service.scroll(dx, dy)
            return jsonify(
                {"status": "success", "message": f"滚轮滚动 dx={dx}, dy={dy}"}
            )

        elif action == "drag":
            start_x = data.get("start_x")
            start_y = data.get("start_y")
            end_x = data.get("end_x")
            end_y = data.get("end_y")

            if any(coord is None for coord in [start_x, start_y, end_x, end_y]):
                return jsonify({"status": "error", "message": "缺少拖拽坐标参数"}), 400

            mouse_service.drag(start_x, start_y, end_x, end_y)
            return jsonify(
                {
                    "status": "success",
                    "message": f"拖拽操作完成: ({start_x},{start_y}) -> ({end_x},{end_y})",
                }
            )

        elif action == "position":
            pos = mouse_service.get_position()
            return jsonify(
                {"status": "success", "position": {"x": pos[0], "y": pos[1]}}
            )

        else:
            return jsonify(
                {"status": "error", "message": f"不支持的操作: {action}"}
            ), 400

    except Exception as e:
        return jsonify({"status": "error", "message": f"鼠标操作失败: {str(e)}"}), 500
