"""
远程控制器主程序
使用模块化架构重构后的主程序
"""

import logging
import os
import sys

from core.app import create_app
from core.config import Config

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


logging.basicConfig(
    level=logging.INFO,  # 只显示 INFO 及以上
    format="%(asctime)s [%(levelname)-5s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
    handlers=[logging.StreamHandler(sys.stdout)],  # 显式指定控制台
)

logger = logging.getLogger(__name__)


def main():
    """主程序入口"""
    # 创建Flask应用
    app = create_app()

    # 启动应用
    logger.info("远程控制器服务器启动中...")
    logger.info(f"访问地址: http://{Config.HOST}:{Config.PORT}")
    logger.info(f"控制页面: http://{Config.HOST}:{Config.PORT}/")

    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG, threaded=True)


if __name__ == "__main__":
    main()
