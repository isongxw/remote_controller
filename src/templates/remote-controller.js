// 远程控制器 JavaScript 代码
// 从 index.html 中分离出来的所有 JavaScript 功能

// 触摸板相关变量
let touchpad = document.getElementById('touchpad');
let isDragging = false;
let lastX = 0, lastY = 0;


// 触摸事件处理
function handleTouchStart(e) {
    e.preventDefault();
    const touch = e.touches[0];
    const rect = touchpad.getBoundingClientRect();
    lastX = touch.clientX - rect.left;
    lastY = touch.clientY - rect.top;
    isDragging = true;
}

function handleTouchMove(e) {
    e.preventDefault();
    if (!isDragging) return;
    
    const touch = e.touches[0];
    const rect = touchpad.getBoundingClientRect();
    const currentX = touch.clientX - rect.left;
    const currentY = touch.clientY - rect.top;
    
    const deltaX = (currentX - lastX) * 2; // 增加灵敏度
    const deltaY = (currentY - lastY) * 2;
    
    moveMouse(deltaX, deltaY, true);
    
    lastX = currentX;
    lastY = currentY;
}

function handleTouchEnd(e) {
    e.preventDefault();
    isDragging = false;
}

// // 鼠标事件处理（用于桌面测试）
// function handleMouseDown(e) {
//     const rect = touchpad.getBoundingClientRect();
//     lastX = e.clientX - rect.left;
//     lastY = e.clientY - rect.top;
//     isDragging = true;
// }

// function handleMouseMove(e) {
//     if (!isDragging) return;
    
//     const rect = touchpad.getBoundingClientRect();
//     const currentX = e.clientX - rect.left;
//     const currentY = e.clientY - rect.top;
    
//     const deltaX = currentX - lastX;
//     const deltaY = currentY - lastY;
    
//     moveMouse(deltaX, deltaY, true);
    
//     lastX = currentX;
//     lastY = currentY;
// }

// function handleMouseUp(e) {
//     isDragging = false;
// }

// API调用函数
async function apiCall(endpoint, data) {
    try {
        const response = await fetch(`/api/${endpoint}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        if (result.status !== 'success') {
            console.error('API调用失败:', result.message);
            updateStatus('错误: ' + result.message, false);
        }
        return result;
    } catch (error) {
        console.error('网络错误:', error);
        updateStatus('网络连接错误', false);
        return null;
    }
}

// 触摸板交互系统
let touchpadState = {
    activeTouches: new Map(),
    touchStartTime: null,
    touchTimeout: 300, // 300ms
    multiTouchWindow: 100, // 100ms
    lastTouchCount: 0
};

// 触摸板API调用函数
async function touchpadApiCall(data) {
    try {
        console.log('发送触摸板数据:', data); // 添加调试日志
        const response = await fetch('/api/touchpad', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        console.log('触摸板API响应:', result); // 添加调试日志
        
        if (result.status === 'success') {
            // 根据操作类型更新UI反馈
            if (result.action === 'left_click') {
                showTouchFeedback('single-touch');
                updateStatus('单指点击 - 左键', true);
            } else if (result.action === 'right_click') {
                showTouchFeedback('multi-touch');
                updateStatus('双指点击 - 右键', true);
            } else if (result.action === 'move') {
                showTouchFeedback('multi-touch');
                updateStatus('滑动 = 移动鼠标', true);
            }
        } else {
            console.error('触摸板API调用失败:', result.message);
        }
        return result;
    } catch (error) {
        console.error('触摸板网络错误:', error);
        updateStatus('触摸板连接错误', false);
        return null;
    }
}

// 显示触摸反馈效果
function showTouchFeedback(type) {
    const touchpad = document.getElementById('touchpad');
    touchpad.classList.remove('single-touch', 'multi-touch', 'active');
    
    setTimeout(() => {
        touchpad.classList.add('active', type);
    }, 10);
    
    setTimeout(() => {
        touchpad.classList.remove('active', type);
    }, 200);
}

// 重置触摸板状态
function resetTouchpad() {
    touchpadApiCall({
        action: 'reset'
    }).then(() => {
        touchpadState.activeTouches.clear();
        touchpadState.touchStartTime = null;
        touchpadState.lastTouchCount = 0;
        updateStatus('触摸板状态已重置', true);
    });
}

// 处理触摸开始事件
function handleTouchpadStart(e) {
    e.preventDefault();
    
    const touches = Array.from(e.touches || [e]);
    const touchCount = touches.length;
    const currentTime = Date.now();
    
    // 记录触摸开始时间（使用固定ID）
    if (!touchpadState.touchStartTime) {
        touchpadState.touchStartTime = currentTime;
    }
    
    // 构建触摸数据 - 使用一致的ID
    const touchData = {
        action: 'touch_start',
        touch_id: 'touch_' + touchpadState.touchStartTime,
        touch_count: touchCount,  // 添加触摸点数量
        touches: touches.map((touch, index) => ({
            id: index,
            x: touch.clientX,
            y: touch.clientY
        })),
        position: {
            x: touches[0].clientX,
            y: touches[0].clientY
        },
        timestamp: currentTime
    };
    
    console.log('[DEBUG] 触摸开始数据:', touchData);  // 添加调试日志
    
    // 更新触摸状态
    touchpadState.lastTouchCount = touchCount;
    
    // 发送到后端处理
    touchpadApiCall(touchData);
}

// 标签页切换功能
function initTabSystem() {
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    
    // 为每个标签按钮添加点击事件
    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const targetTab = button.getAttribute('data-tab');
            switchTab(targetTab);
        });
    });
    
    // 确保默认显示第一个标签页（键盘控制）
    if (tabButtons.length > 0) {
        switchTab('keyboard');
    }
}

function switchTab(targetTab) {
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    
    // 移除所有活动状态
    tabButtons.forEach(btn => btn.classList.remove('active'));
    tabContents.forEach(content => {
        content.classList.remove('active');
        // 添加淡出效果
        content.style.opacity = '0';
        content.style.transform = 'translateY(20px)';
    });
    
    // 激活目标标签按钮
    const targetButton = document.querySelector(`[data-tab="${targetTab}"]`);
    if (targetButton) {
        targetButton.classList.add('active');
    }
    
    // 激活目标标签内容（带动画效果）
    const targetContent = document.getElementById(`tab-${targetTab}`);
    if (targetContent) {
        setTimeout(() => {
            targetContent.classList.add('active');
            // 添加淡入效果
            setTimeout(() => {
                targetContent.style.opacity = '1';
                targetContent.style.transform = 'translateY(0)';
            }, 50);
        }, 100);
    }
}

// 添加触摸板移动事件处理函数
function handleTouchpadMove(e) {
    e.preventDefault();
    
    const touches = Array.from(e.touches || [e]);
    const currentTime = Date.now();
    
    if (touches.length > 0 && touchpadState.touchStartTime) {
        // 构建触摸移动数据
        const touchData = {
            action: 'touch_move',
            touch_id: 'touch_' + touchpadState.touchStartTime,
            touch_count: touches.length,  // 添加触摸点数量
            touches: touches.map((touch, index) => ({
                id: index,
                x: touch.clientX,
                y: touch.clientY
            })),
            position: {
                x: touches[0].clientX,
                y: touches[0].clientY
            },
            timestamp: currentTime
        };
        
        // 发送到后端处理
        touchpadApiCall(touchData);
    }
}

// 处理触摸结束事件
function handleTouchpadEnd(e) {
    e.preventDefault();
    
    const currentTime = Date.now();
    const touches = Array.from(e.changedTouches || [e]);
    
    // 构建触摸结束数据
    const touchData = {
        action: 'touch_end',
        touch_id: 'touch_' + touchpadState.touchStartTime,  // 使用一致的ID
        touch_count: touchpadState.lastTouchCount || 1,  // 使用记录的触摸点数量
        position: touches.length > 0 ? {
            x: touches[0].clientX,
            y: touches[0].clientY
        } : { x: 0, y: 0 },
        timestamp: currentTime
    };
    
    console.log('[DEBUG] 触摸结束数据:', touchData);  // 添加调试日志
    
    // 发送触摸结束事件
    touchpadApiCall(touchData);
    
    // 重置状态
    isDragging = false;
    touchpadState.touchStartTime = null;
    touchpadState.lastTouchCount = 0;
}


// 键盘控制函数
function pressKey(key) {
    apiCall('keyboard', {
        action: 'press',
        key: key
    }).then(() => {
        setTimeout(() => {
            apiCall('keyboard', {
                action: 'release',
                key: key
            });
        }, 100);
    });
}

function sendText() {
    const text = document.getElementById('textInput').value;
    if (text) {
        apiCall('keyboard', {
            action: 'type',
            text: text
        });
    }
}

function clearText() {
    document.getElementById('textInput').value = '';
}

function sendHotkey(keys) {
    apiCall('keyboard', {
        action: 'hotkey',
        keys: keys
    });
}

function sendSystem(action) {
    apiCall('system', {
        action: action
    })
};

// 状态更新函数
function updateStatus(message, isConnected = true) {
    const statusText = document.getElementById('status-text');
    const statusIndicator = document.querySelector('.connection-status');
    
    statusText.textContent = message;
    statusIndicator.style.background = isConnected ? '#00b894' : '#e17055';
}

// 初始化函数
function initializeRemoteController() {
    // 获取触摸板元素
    touchpad = document.getElementById('touchpad');
    
    updateStatus('远程控制器已就绪');
    
    // 初始化标签页系统
    initTabSystem();
    
    // 绑定触摸板事件监听器
    touchpad.addEventListener('touchstart', handleTouchpadStart, {passive: false});
    touchpad.addEventListener('touchmove', handleTouchpadMove, {passive: false});
    touchpad.addEventListener('touchend', handleTouchpadEnd, {passive: false});
    // touchpad.addEventListener('mousedown', handleTouchpadStart, {passive: false});
    // touchpad.addEventListener('mouseup', handleTouchpadEnd, {passive: false});
    
    // 滚动支持（触摸板）
    touchpad.addEventListener('wheel', function(e) {
        e.preventDefault();
        mouseScroll(e.deltaX / 10, e.deltaY / 10);
    }, {passive: false});
    
    // 只在触摸板区域防止页面滚动，其他区域允许正常滚动
    touchpad.addEventListener('touchmove', function(e) {
        e.preventDefault();
    }, {passive: false});
    
    // 允许页面其他区域正常滚动
    document.addEventListener('touchstart', function(e) {
        // 如果触摸开始在触摸板区域，标记为触摸板操作
        if (e.target === touchpad || touchpad.contains(e.target)) {
            e.target.dataset.isTouchpad = 'true';
        }
    });
    
    document.addEventListener('touchmove', function(e) {
        // 只有在触摸板区域才阻止默认滚动行为
        if (e.target.dataset.isTouchpad === 'true') {
            e.preventDefault();
        }
    }, {passive: false});
}

// DOM加载完成后初始化
document.addEventListener('DOMContentLoaded', initializeRemoteController);