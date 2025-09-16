"""
远程控制器主程序
使用模块化架构重构后的主程序
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.app import create_app
from core.config import Config

def main():
    """主程序入口"""
    # 创建Flask应用
    app = create_app()
    
    # 启动应用
    print(f"远程控制器服务器启动中...")
    print(f"访问地址: http://{Config.HOST}:{Config.PORT}")
    print(f"控制页面: http://{Config.HOST}:{Config.PORT}/")
    
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG,
        threaded=True
    )

if __name__ == '__main__':
    main()