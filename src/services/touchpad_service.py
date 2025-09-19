"""
触摸板服务模块
处理所有触摸板相关的操作逻辑
"""

import logging
import threading
import time

from pynput import mouse

from core.config import TOUCHPAD_CONFIG
from utils.security import get_controllers

logger = logging.getLogger(__name__)


class TouchpadService:
    """触摸板操作服务类"""

    def __init__(self):
        self.mouse_controller, self.keyboard_controller = get_controllers()

        # 触摸板状态变量
        self.touchpad_state = {
            "active_touches": {},
            "last_touch_time": 0,
            "is_dragging": False,
            "drag_start_pos": None,
            "pending_click": None,
            "click_timer": None,
        }

        # 配置参数
        self.config = TOUCHPAD_CONFIG

    def detect_touch_mode(self, touches_data):
        """
        检测触摸模式

        Args:
            touches_data: 触摸数据

        Returns:
            str: 触摸模式 ('single', 'scroll', 'zoom')
        """
        # 优先使用touch_count字段
        if "touch_count" in touches_data:
            touch_count = touches_data["touch_count"]
        elif "touches" in touches_data:
            touch_count = len(touches_data["touches"])
        else:
            touch_count = 1

        logger.debug(f"检测触摸模式: touch_count={touch_count}")

        if touch_count == 1:
            return "single"
        elif touch_count == 2:
            return "scroll"
        elif touch_count >= 3:
            return "dragging"
        else:
            return "single"

    def handle_touch_start(self, touches_data):
        """
        处理触摸开始事件

        Args:
            touches_data: 触摸数据

        Returns:
            dict: 响应数据
        """
        logger.debug(f"收到触摸开始数据: {touches_data}")  # 添加调试日志

        touch_id = touches_data.get("touch_id", "default")
        touches = touches_data.get("touches", [])

        if not touches:
            return {"status": "error", "message": "无效的触摸数据"}

        touch = touches[0]
        x, y = touch.get("x", 0), touch.get("y", 0)

        # 记录触摸状态
        self.touchpad_state["active_touches"][touch_id] = {
            "start_x": x,
            "start_y": y,
            "current_x": x,
            "current_y": y,
            "start_time": time.time(),
        }

        logger.debug(
            f"触摸开始记录: touch_id={touch_id}, 位置=({x}, {y}), 触摸模式={self.detect_touch_mode(touches_data)}"
        )

        # 检测触摸模式
        mode = self.detect_touch_mode(touches_data)

        if mode == "single":
            # 单指触摸，准备延迟点击
            self._prepare_delayed_click()
        elif mode == "scroll":
            # 双指触摸，准备滚动
            self._cancel_pending_click()
        elif mode == "dragging":
            # 三指触摸，准备拖拽
            self._cancel_pending_click()
            self.touchpad_state["is_dragging"] = True
            self.touchpad_state["drag_start_pos"] = (x, y)
            self.mouse_controller.press(mouse.Button.left)

        return {"status": "success", "mode": mode}

    def handle_touch_move(self, touches_data):
        """
        处理触摸移动事件

        Args:
            touches_data: 触摸数据

        Returns:
            dict: 响应数据
        """
        logger.debug(f"收到触摸移动数据: {touches_data}")  # 添加调试日志

        touch_id = touches_data.get("touch_id", "default")
        touches = touches_data.get("touches", [])

        if not touches or touch_id not in self.touchpad_state["active_touches"]:
            logger.debug(
                f"无效的触摸移动: touch_id={touch_id}, touches={len(touches)}, active_touches={list(self.touchpad_state['active_touches'].keys())}"
            )
            return {"status": "error", "message": "无效的触摸移动"}

        touch = touches[0]
        x, y = touch.get("x", 0), touch.get("y", 0)

        # 更新触摸状态
        touch_state = self.touchpad_state["active_touches"][touch_id]
        prev_x, prev_y = touch_state["current_x"], touch_state["current_y"]
        touch_state["current_x"] = x
        touch_state["current_y"] = y

        # 计算移动距离
        dx = x - prev_x
        dy = y - prev_y
        total_distance = (
            (x - touch_state["start_x"]) ** 2 + (y - touch_state["start_y"]) ** 2
        ) ** 0.5

        logger.debug(f"移动计算: dx={dx}, dy={dy}, total_distance={total_distance}")

        # 检测触摸模式
        mode = self.detect_touch_mode(touches_data)

        if mode == "single":
            if total_distance > self.config["MOVE_THRESHOLD"]:
                # 移动距离超过阈值，取消点击，开始拖拽或移动鼠标
                self._cancel_pending_click()

            # 移动鼠标光标
            current_pos = self.mouse_controller.position
            new_x = current_pos[0] + dx * self.config["CURSOR_SENSITIVITY"]
            new_y = current_pos[1] + dy * self.config["CURSOR_SENSITIVITY"]
            logger.debug(f"移动鼠标: 从 {current_pos} 到 ({new_x}, {new_y})")
            self.mouse_controller.position = (new_x, new_y)

        elif mode == "scroll":
            # 双指滚动
            self._cancel_pending_click()
            scroll_dx = dx * self.config["SCROLL_SENSITIVITY"]
            scroll_dy = -dy * self.config["SCROLL_SENSITIVITY"]  # 反转Y轴
            logger.debug(f"滚动: scroll_dx={scroll_dx}, scroll_dy={scroll_dy}")
            self.mouse_controller.scroll(scroll_dx, scroll_dy)
        elif mode == "dragging":
            # 三指拖拽
            self.touchpad_state["is_dragging"] = True
            self.touchpad_state["drag_start_pos"] = (x, y)
            # 移动鼠标光标
            current_pos = self.mouse_controller.position
            new_x = current_pos[0] + dx * self.config["CURSOR_SENSITIVITY"]
            new_y = current_pos[1] + dy * self.config["CURSOR_SENSITIVITY"]
            logger.debug(f"移动鼠标: 从 {current_pos} 到 ({new_x}, {new_y})")
            self.mouse_controller.position = (new_x, new_y)

        return {"status": "success", "mode": mode, "dx": dx, "dy": dy}

    def handle_touch_end(self, touches_data):
        """
        处理触摸结束事件

        Args:
            touches_data: 触摸数据

        Returns:
            dict: 响应数据
        """
        logger.debug(f"收到触摸结束数据: {touches_data}")  # 添加调试日志

        touch_id = touches_data.get("touch_id", "default")

        if touch_id not in self.touchpad_state["active_touches"]:
            logger.debug(f"无效的触摸结束: touch_id={touch_id}")
            return {"status": "error", "message": "无效的触摸结束"}

        # 获取触摸状态
        touch_state = self.touchpad_state["active_touches"][touch_id]

        # 检测触摸模式
        mode = self.detect_touch_mode(touches_data)
        logger.debug(f"触摸结束模式: {mode}")

        # 计算触摸持续时间和移动距离
        touch_duration = time.time() - touch_state["start_time"]
        total_distance = (
            (touch_state["current_x"] - touch_state["start_x"]) ** 2
            + (touch_state["current_y"] - touch_state["start_y"]) ** 2
        ) ** 0.5

        logger.debug(
            f"触摸持续时间: {touch_duration:.3f}s, 移动距离: {total_distance:.1f}px"
        )

        action_performed = None

        # 处理双指右键点击
        if (
            mode == "scroll"
            and touch_duration < self.config["DOUBLE_CLICK_TIME"]
            and total_distance < self.config["MOVE_THRESHOLD"]
        ):
            logger.debug("执行双指右键点击")
            self.mouse_controller.click(mouse.Button.right)
            action_performed = "right_click"
            self._cancel_pending_click()  # 取消任何待处理的左键点击
        elif mode == "single":
            action_performed = "left_click"
        elif mode == "dragging":
            self.mouse_controller.release(mouse.Button.left)
            logger.debug("三指拖拽结束，释放鼠标左键")

        # 移除触摸状态
        self.touchpad_state["active_touches"].pop(touch_id)

        # 更新最后触摸时间
        self.touchpad_state["last_touch_time"] = time.time()

        # 重置拖拽状态
        self.touchpad_state["is_dragging"] = False
        self.touchpad_state["drag_start_pos"] = None

        result = {"status": "success", "message": "触摸结束"}
        if action_performed:
            result["action"] = action_performed

        return result

    def _prepare_delayed_click(self):
        """
        准备延迟点击

        """
        # 取消之前的点击
        self._cancel_pending_click()

        # 设置新的延迟点击
        self.touchpad_state["pending_click"] = True
        self.touchpad_state["click_timer"] = threading.Timer(
            self.config["CLICK_DELAY"], self._execute_delayed_click
        )
        self.touchpad_state["click_timer"].start()

    def _execute_delayed_click(self):
        """执行延迟点击"""
        if self.touchpad_state["pending_click"]:
            # 执行点击
            self.mouse_controller.click(mouse.Button.left)
            logger.debug("执行延迟点击")
            # 清理状态
            self.touchpad_state["pending_click"] = None
            self.touchpad_state["click_timer"] = None

    def _cancel_pending_click(self):
        logger.debug("取消待处理的点击")
        """取消待处理的点击"""
        if self.touchpad_state["click_timer"]:
            self.touchpad_state["click_timer"].cancel()
            self.touchpad_state["click_timer"] = None
        self.touchpad_state["pending_click"] = None

    def get_touchpad_status(self):
        """
        获取触摸板状态

        Returns:
            dict: 触摸板状态信息
        """
        return {
            "active_touches_count": len(self.touchpad_state["active_touches"]),
            "is_dragging": self.touchpad_state["is_dragging"],
            "has_pending_click": self.touchpad_state["pending_click"] is not None,
            "last_touch_time": self.touchpad_state["last_touch_time"],
        }
