# AGENTS.md - Development Guidelines for AI Agents

This file provides guidelines for AI agents working on the remote_controller project.

## Project Overview

A Python Flask-based remote control application that allows controlling keyboard, mouse, and touchpad via a web interface. Uses pynput for system input control and PyInstaller for building executables.

## Technology Stack

- **Python**: 3.12+
- **Web Framework**: Flask 3.1+, Flask-CORS 6.0+
- **Input Control**: pynput 1.8+
- **Build Tool**: PyInstaller 6.16+
- **Package Manager**: uv (preferred)

## Build, Run, and Test Commands

### Install Dependencies

```bash
# Using uv (recommended)
uv sync

# Using pip
pip install flask flask-cors pynput
```

### Run the Application

```bash
# Development mode
uv run python src/server.py
python src/server.py

# Access at http://localhost:8088
```

### Build Executable

```bash
# Windows using the pack script
.\scripts\pack.bat

# Or manually
uv sync --frozen
uv run pyinstaller .\remote-controller.spec

# Output in dist/ directory
```

### Running Tests

This project uses pytest for testing.

```bash
# Install pytest
python -m pip install pytest

# Run all tests
python -m pytest tests/ -v

# Run a single test file
python -m pytest tests/test_config.py -v

# Run a single test function
python -m pytest tests/test_config.py::TestConfig::test_host_config -v
```

### Linting and Type Checking

No linter or type checker is currently configured. To add in the future:
```bash
# Install ruff
uv add --dev ruff

# Run linting
uv run ruff check .

# Auto-fix
uv run ruff check --fix .
```

## Code Style Guidelines

### General Principles

- Use **Chinese comments and docstrings** (as per existing codebase style)
- Keep code simple and readable
- Use meaningful variable and function names

### Imports

Order imports as follows:
1. Standard library (logging, os, sys, time, etc.)
2. Third-party packages (flask, pynput, etc.)
3. Local application modules (core.*, services.*, handlers.*, utils.*)

Example:
```python
import logging
import os
import sys
import time

from flask import Flask, jsonify, request
from flask_cors import CORS
from pynput import mouse

from core.config import Config
from services.keyboard_service import KeyboardService
```

### Naming Conventions

- **Functions/variables**: snake_case (`handle_keyboard`, `active_touches`)
- **Classes**: PascalCase (`KeyboardService`, `TouchpadService`)
- **Constants**: UPPER_SNAKE_CASE (`LOGGER_LEVEL`, `HOST`, `PORT`)
- **Private methods**: prefix with underscore (`_prepare_delayed_click`)

### Type Hints

Currently not used in the codebase. When adding:
```python
def press_key(self, key: str) -> None:
    ...
```

### File Structure

```
src/
├── server.py           # Application entry point
├── core/
│   ├── app.py         # Flask app factory
│   └── config.py      # Configuration and constants
├── handlers/
│   ├── keyboard.py    # Keyboard API endpoints
│   ├── touchpad.py    # Touchpad API endpoints
│   ├── system.py      # System control endpoints
│   └── main.py        # Main page routes
├── services/
│   ├── keyboard_service.py
│   ├── touchpad_service.py
│   └── system_service.py
├── utils/
│   ├── security.py
│   └── system_utils.py
└── templates/
    └── index.html     # Web UI
```

### Error Handling

- In handlers: wrap logic in try/except, return JSON error responses with appropriate HTTP status codes
- Use descriptive error messages in Chinese
- Log errors appropriately

Example:
```python
@keyboard_bp.route("/api/keyboard", methods=["POST"])
def handle_keyboard():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "无效的请求数据"}), 400
        # ... handle request
    except Exception as e:
        return jsonify({"status": "error", "message": f"键盘操作失败: {str(e)}"}), 500
```

### Logging

Use the logging module for debugging and information:
```python
import logging

logger = logging.getLogger(__name__)

logger.debug("收到触摸移动数据: %s", touches_data)
logger.info("远程控制器服务器启动中...")
```

### Configuration

- Store configuration in `src/core/config.py`
- Use classes for configuration groups (e.g., `Config`, `TOUCHPAD_CONFIG`)
- Constants should be clearly documented with comments

### API Response Format

Use consistent JSON response format:
```python
# Success
return jsonify({"status": "success", "message": "操作描述"})

# Success with data
return jsonify({"status": "success", "mode": "scroll", "dx": 10, "dy": 5})

# Error
return jsonify({"status": "error", "message": "错误描述"}), 400
```

### Blueprint Registration

Register blueprints in `src/core/app.py`:
```python
from handlers.keyboard import keyboard_bp
app.register_blueprint(keyboard_bp)
```

### Working with pynput

- Initialize controllers via `utils.security.get_controllers()`
- Use `keyboard_controller.press()`, `keyboard_controller.release()`, `keyboard_controller.type()`
- Use `mouse_controller.click()`, `mouse_controller.move()`, `mouse_controller.position`, `mouse_controller.scroll()`

## Important Notes

1. **Security**: This application has full system control. Only run on trusted networks.
2. **Platform**: Currently optimized for Windows (key mappings in `config.py`)
3. **Debugging**: Use `logger.debug()` for detailed debugging information
4. **Threading**: `TouchpadService` uses `threading.Timer` for delayed click handling

## Adding New Features

1. Create new service in `src/services/` for business logic
2. Create new handler in `src/handlers/` for HTTP endpoints
3. Register blueprint in `src/core/app.py`
4. Update configuration if needed in `src/core/config.py`
5. Test locally with `uv run python src/server.py`
