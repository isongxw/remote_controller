# 远程控制器

一个基于Python Flask的远程控制应用，允许通过手机网页界面远程控制电脑的键盘和鼠标操作。

## 功能特性

- 🖱️ **鼠标控制**: 支持鼠标移动、点击、双击、右键、滚动等操作
- ⌨️ **键盘控制**: 支持文字输入、按键操作、快捷键组合
- 📱 **移动端优化**: 响应式设计，完美适配手机触摸操作
- 🔧 **Windows兼容**: 完整支持Windows系统的快捷键操作
- 🌐 **网页界面**: 无需安装客户端，直接通过浏览器使用

## 系统要求

- Python 3.8+
- Windows/Linux/macOS
- 支持现代浏览器的移动设备

## 安装和使用

### 1. 克隆项目
```bash
git clone <repository-url>
cd remote_controller
```

### 2. 安装依赖
```bash
uv sync
```

### 3. 启动服务器
```bash
uv run python src/remote_controller/main.py
```

### 4. 连接使用
1. 确保电脑和手机在同一网络下
2. 在手机浏览器中访问: `http://[电脑IP]:5000`
3. 开始远程控制

## 功能说明

### 鼠标控制
- **触摸板区域**: 在触摸板区域滑动手指控制鼠标移动
- **左键/右键**: 点击对应按钮执行鼠标点击
- **双击**: 快速双击功能
- **滚动**: 在触摸板上使用双指滚动（支持的设备）

### 键盘控制
- **文字输入**: 在输入框中输入文字后点击发送
- **常用按键**: Esc、Tab、Enter、Backspace、Delete等
- **方向键**: 上下左右方向键
- **修饰键**: Ctrl、Alt、Shift、Win键
- **快捷键**: 预设常用快捷键组合

### 支持的快捷键
- `Ctrl+C` / `Ctrl+V`: 复制/粘贴
- `Ctrl+Z` / `Ctrl+Y`: 撤销/重做
- `Ctrl+A`: 全选
- `Ctrl+S`: 保存
- `Alt+Tab`: 程序切换
- `Win+D`: 显示桌面
- `Win+L`: 锁屏
- `Ctrl+Shift+Esc`: 任务管理器

## 技术架构

- **后端**: Python Flask + pynput
- **前端**: HTML5 + CSS3 + JavaScript
- **跨域支持**: Flask-CORS
- **触摸支持**: 原生触摸事件处理

## 安全注意事项

⚠️ **重要提醒**:
- 此应用允许完全控制您的电脑
- 请仅在受信任的网络环境中使用
- 建议仅在本地网络中使用，避免暴露到公网
- 使用完毕后请及时关闭服务器

## 开发和贡献

### 项目结构
```
remote_controller/
├── src/
│   └── remote_controller/
│       ├── main.py              # 主应用文件
│       └── templates/
│           └── index.html       # 网页界面
├── pyproject.toml              # 项目配置
└── README.md                   # 项目说明
```

### 开发环境
```bash
# 安装开发依赖
uv add --dev pytest black flake8

# 运行测试
uv run pytest

# 代码格式化
uv run black src/
```

## 许可证

MIT License

## 更新日志

### v1.0.0
- 初始版本发布
- 支持基本的鼠标和键盘控制
- 移动端优化界面
- Windows系统兼容性