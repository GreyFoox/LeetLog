#!/bin/bash

cd ~/LeetLog

echo "🛑 停止 LeetCode 刷题日志工具..."

if [ -f backend.pid ]; then
    kill -9 $(cat backend.pid) 2>/dev/null && echo "  已停止后端"
    rm backend.pid
fi

if [ -f frontend.pid ]; then
    kill -9 $(cat frontend.pid) 2>/dev/null && echo "  已停止前端"
    rm frontend.pid
fi

# 额外清理
pkill -f "python3 app.py" 2>/dev/null
pkill -f "python3 -m http.server" 2>/dev/null

echo "✅ 所有服务已停止"
